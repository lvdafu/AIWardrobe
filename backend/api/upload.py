"""
图片上传 API
"""
import asyncio
import uuid
from pathlib import Path

import httpx
from fastapi import APIRouter, UploadFile, File, HTTPException

from services.segment import remove_background
from services.removebg import remove_background_api
from services.openai_compatible import analyze_clothes_openai
from storage.config_store import load_config
from domain.clothes import (
    ClothesSemantics,
    ClothesCreate,
    ClothesItem,
    normalize_category_value,
)
from storage.db import add_clothes, get_clothes_by_id

router = APIRouter()

# 上传目录
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_CATEGORIES = {"top", "bottom", "shoes", "accessory"}

# rembg 首次会从 GitHub 拉 u2net.onnx，国内常失败或极慢；超时后改用原图
LOCAL_BG_TIMEOUT_SECONDS = 45


async def _analyze_clothes_with_fallback(image_bytes: bytes) -> ClothesSemantics:
    """
    视觉识别失败时仍保存图片：常见原因是当前 LLM 不支持多模态（如 deepseek-chat）。
    """
    try:
        return await analyze_clothes_openai(image_bytes)
    except (ValueError, httpx.HTTPError, OSError) as exc:
        msg = str(exc)
        print(f"⚠️ 衣物视觉识别失败，使用占位语义入库: {msg[:500]}")
        return ClothesSemantics(
            category="accessory",
            item="未识别衣物",
            style_semantics=["待补充"],
            season_semantics=["四季"],
            usage_semantics=["日常"],
            color_semantics="未知",
            description="图片已保存，自动识别失败。请在网页端修改信息，或更换为支持图片的模型后重新上传。",
        )


async def _try_local_remove_background(raw_bytes: bytes) -> bytes:
    """必须抠图成功；失败返回 503，不再静默改用原图。"""
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(remove_background, raw_bytes),
            timeout=LOCAL_BG_TIMEOUT_SECONDS,
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=503,
            detail=f"本地抠图超时（{LOCAL_BG_TIMEOUT_SECONDS}s）。"
            "可稍后重试，或在设置中配置 remove.bg API Key 使用在线抠图。",
        ) from None
    except HTTPException:
        raise
    except Exception as exc:
        print(f"❌ 本地抠图失败: {exc}")
        raise HTTPException(
            status_code=503,
            detail=f"抠图失败: {exc}。若在国内网络，请确认模型已下载到本机，或改用 remove.bg。",
        ) from None


@router.post("/upload", response_model=ClothesItem)
async def upload_image(file: UploadFile = File(...)):
    """
    上传衣物图片
    
    流程：
    1. 接收图片
    2. 根据配置使用 rembg 或 remove.bg API 去除背景
    3. 使用 LLM Vision 进行语义分析
    4. 保存到数据库
    5. 返回衣物信息
    """
    # 验证文件类型
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只支持图片文件")
    
    try:
        # 读取原始图片
        raw_bytes = await file.read()
        
        # 加载配置
        config = load_config()
        
        # 根据配置选择背景移除方式
        if config.bg_removal_method == "removebg" and config.removebg_api_key:
            try:
                processed_bytes = await remove_background_api(
                    raw_bytes,
                    config.removebg_api_key,
                )
            except ValueError as e:
                print(f"⚠️ remove.bg API 失败，尝试本地 rembg: {e}")
                processed_bytes = await _try_local_remove_background(raw_bytes)
        else:
            processed_bytes = await _try_local_remove_background(raw_bytes)
        
        semantics: ClothesSemantics = await _analyze_clothes_with_fallback(processed_bytes)
        
        # 生成文件名并保存
        filename = f"{uuid.uuid4()}.png"
        filepath = UPLOAD_DIR / filename
        
        with open(filepath, "wb") as f:
            f.write(processed_bytes)
        
        normalized_category = normalize_category_value(semantics.category)
        if normalized_category not in ALLOWED_CATEGORIES:
            normalized_category = "accessory"

        # 保存到数据库
        clothes_data = ClothesCreate(
            category=normalized_category,
            item=semantics.item,
            style_semantics=semantics.style_semantics,
            season_semantics=semantics.season_semantics,
            usage_semantics=semantics.usage_semantics,
            color_semantics=semantics.color_semantics,
            description=semantics.description,
            image_filename=filename
        )
        
        clothes_id = await add_clothes(clothes_data)
        
        # 返回完整的衣物信息
        clothes = await get_clothes_by_id(clothes_id)
        if not clothes:
            raise HTTPException(status_code=500, detail="保存失败")
        
        return clothes
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"图片分析失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

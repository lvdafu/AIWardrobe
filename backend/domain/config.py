"""
API 配置模型
"""
import os
from pydantic import BaseModel
from typing import Optional, List, Literal


class LLMConfig(BaseModel):
    """LLM API 配置"""
    api_base: str = "https://x666.me/v1"
    api_key: str = ""
    model: str = "gemini-flash-latest"
    # remove.bg 配置
    removebg_api_key: str = ""
    bg_removal_method: Literal["local", "removebg"] = "removebg"  # 本地 rembg 或 remove.bg API
    # COS 配置
    cos_secret_id: str = ""
    cos_secret_key: str = ""
    cos_region: str = ""
    cos_bucket: str = ""
    cos_public_base_url: str = ""
    # 默认天气城市（用于首页与推荐页）
    weather_location: str = "上海, 上海市, 中国"
    # 用户星座配置（用于首页运势）
    zodiac_sign: str = ""
    
    
class LLMConfigUpdate(BaseModel):
    """更新 LLM 配置的请求体"""
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    model: Optional[str] = None
    removebg_api_key: Optional[str] = None
    bg_removal_method: Optional[Literal["local", "removebg"]] = None
    cos_secret_id: Optional[str] = None
    cos_secret_key: Optional[str] = None
    cos_region: Optional[str] = None
    cos_bucket: Optional[str] = None
    cos_public_base_url: Optional[str] = None
    weather_location: Optional[str] = None
    zodiac_sign: Optional[str] = None


class AvailableModel(BaseModel):
    """可用模型"""
    id: str
    name: str
    

class ModelListResponse(BaseModel):
    """模型列表响应"""
    models: List[AvailableModel]

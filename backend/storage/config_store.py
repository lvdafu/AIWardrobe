"""
配置存储 - 使用 JSON 文件持久化配置
"""
import json
import os
from pathlib import Path
from typing import Optional
from domain.config import LLMConfig
from services.weather import validate_location_input, DEFAULT_LOCATION_QUERY

CONFIG_FILE = Path(__file__).parent / "llm_config.json"
_CONFIG_CACHE: Optional[LLMConfig] = None
_CONFIG_MTIME: Optional[float] = None


def load_config() -> LLMConfig:
    """加载 LLM 配置（支持环境变量覆盖敏感字段）"""
    global _CONFIG_CACHE, _CONFIG_MTIME

    if not CONFIG_FILE.exists():
        _CONFIG_CACHE = LLMConfig()
        _CONFIG_MTIME = None
        return _CONFIG_CACHE

    try:
        mtime = CONFIG_FILE.stat().st_mtime
    except Exception:
        mtime = None

    if _CONFIG_CACHE is not None and _CONFIG_MTIME == mtime:
        return _CONFIG_CACHE

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 环境变量优先覆盖敏感配置
        env_overrides = {
            "api_key": __import__("os").getenv("LLM_API_KEY", "").strip(),
            "removebg_api_key": __import__("os").getenv("REMOVEBG_API_KEY", "").strip(),
            "cos_secret_id": __import__("os").getenv("COS_SECRET_ID", "").strip(),
            "cos_secret_key": __import__("os").getenv("COS_SECRET_KEY", "").strip(),
            "cos_region": __import__("os").getenv("COS_REGION", "").strip(),
            "cos_bucket": __import__("os").getenv("COS_BUCKET", "").strip(),
            "cos_public_base_url": __import__("os").getenv("COS_PUBLIC_BASE_URL", "").strip(),
        }
        for k, v in env_overrides.items():
            if v:
                data[k] = v

        _CONFIG_CACHE = LLMConfig(**data)
        _CONFIG_MTIME = mtime
        return _CONFIG_CACHE
    except Exception:
        _CONFIG_CACHE = LLMConfig()
        _CONFIG_MTIME = mtime
        return _CONFIG_CACHE


def save_config(config: LLMConfig) -> None:
    """保存 LLM 配置"""
    global _CONFIG_CACHE, _CONFIG_MTIME

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config.model_dump(), f, indent=2, ensure_ascii=False)

    _CONFIG_CACHE = config
    try:
        _CONFIG_MTIME = CONFIG_FILE.stat().st_mtime
    except Exception:
        _CONFIG_MTIME = None


def update_config(
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    removebg_api_key: Optional[str] = None,
    bg_removal_method: Optional[str] = None,
    cos_secret_id: Optional[str] = None,
    cos_secret_key: Optional[str] = None,
    cos_region: Optional[str] = None,
    cos_bucket: Optional[str] = None,
    cos_public_base_url: Optional[str] = None,
    weather_location: Optional[str] = None,
    zodiac_sign: Optional[str] = None
) -> LLMConfig:
    """更新配置"""
    config = load_config()
    
    if api_base is not None:
        config.api_base = api_base.strip()
    if api_key is not None:
        config.api_key = api_key.strip()
    if model is not None:
        config.model = model.strip()
    if removebg_api_key is not None:
        config.removebg_api_key = removebg_api_key.strip()
    if bg_removal_method is not None:
        config.bg_removal_method = bg_removal_method
    if cos_secret_id is not None:
        config.cos_secret_id = cos_secret_id.strip()
    if cos_secret_key is not None:
        config.cos_secret_key = cos_secret_key.strip()
    if cos_region is not None:
        config.cos_region = cos_region.strip()
    if cos_bucket is not None:
        config.cos_bucket = cos_bucket.strip()
    if cos_public_base_url is not None:
        config.cos_public_base_url = cos_public_base_url.strip().rstrip("/")
    if weather_location is not None:
        normalized_location = weather_location.strip() or DEFAULT_LOCATION_QUERY
        validation_error = validate_location_input(normalized_location)
        if validation_error:
            raise ValueError(validation_error)
        config.weather_location = normalized_location
    if zodiac_sign is not None:
        config.zodiac_sign = zodiac_sign.strip().lower()
    
    save_config(config)
    return config


def _mask_key(key: str) -> str:
    """对 API Key 进行脱敏处理"""
    if not key:
        return ""
    if len(key) > 8:
        return key[:4] + "*" * (len(key) - 8) + key[-4:]
    return "*" * len(key)


def get_masked_config() -> dict:
    """获取脱敏后的配置（隐藏 API Key）"""
    config = load_config()
    weather_location = (config.weather_location or "").strip() or DEFAULT_LOCATION_QUERY
    if validate_location_input(weather_location):
        weather_location = DEFAULT_LOCATION_QUERY
    
    return {
        "api_base": config.api_base,
        "api_key_masked": _mask_key(config.api_key),
        "has_api_key": bool(config.api_key),
        "model": config.model,
        "removebg_api_key_masked": _mask_key(config.removebg_api_key),
        "has_removebg_key": bool(config.removebg_api_key),
        "bg_removal_method": config.bg_removal_method,
        "cos_secret_id_masked": _mask_key(config.cos_secret_id),
        "has_cos_secret_id": bool(config.cos_secret_id),
        "cos_secret_key_masked": _mask_key(config.cos_secret_key),
        "has_cos_secret_key": bool(config.cos_secret_key),
        "cos_region": config.cos_region,
        "cos_bucket": config.cos_bucket,
        "cos_public_base_url": config.cos_public_base_url,
        "weather_location": weather_location,
        "zodiac_sign": config.zodiac_sign
    }

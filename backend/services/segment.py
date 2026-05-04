"""
rembg 背景移除服务
"""
import io

from PIL import Image
from rembg import remove

from services.rembg_model import ensure_u2net_model


def remove_background(image_bytes: bytes) -> bytes:
    """
    使用 rembg 移除图片背景
    
    Args:
        image_bytes: 原始图片的字节数据
        
    Returns:
        去除背景后的 PNG 图片字节数据
    """
    ensure_u2net_model()
    input_img = Image.open(io.BytesIO(image_bytes))
    output = remove(input_img)
    
    buf = io.BytesIO()
    output.save(buf, format="PNG")
    return buf.getvalue()

"""
确保 rembg 所需的 u2net.onnx 已就绪（国内 GitHub 常超时，使用备用镜像）。
模型与校验与 rembg 内置 pooch 配置一致。
"""
from __future__ import annotations

import hashlib
import os
import urllib.request
from pathlib import Path

# rembg U2netSession.download_models 使用的地址与 MD5
U2NET_URL_PRIMARY = (
    "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"
)
U2NET_MD5 = "60024c5c889badc19c04ad937298a77b"
# 常见 GitHub 加速前缀（任一可用即可；若失效可改环境变量 U2NET_MIRROR_URLS 逗号分隔）
U2NET_URL_MIRRORS = [
    "https://ghfast.top/https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx",
    "https://mirror.ghproxy.com/https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx",
]

MIN_VALID_BYTES = 50 * 1024 * 1024  # 约 50MB，避免半截文件


def u2net_model_path() -> Path:
    home = os.path.expanduser(
        os.getenv("U2NET_HOME", os.path.join(os.getenv("XDG_DATA_HOME", "~"), ".u2net"))
    )
    return Path(home).expanduser() / "u2net.onnx"


def _md5_hex(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _download_to(url: str, dest: Path, timeout: int = 120) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AIWardrobe/1.0 (u2net-onnx)",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        total = 0
        with open(tmp, "wb") as out:
            while True:
                chunk = resp.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
                total += len(chunk)
    if total < MIN_VALID_BYTES:
        tmp.unlink(missing_ok=True)
        raise OSError(f"下载文件过小 ({total} bytes)，可能不是完整模型")
    if _md5_hex(tmp) != U2NET_MD5:
        tmp.unlink(missing_ok=True)
        raise OSError("下载文件 MD5 与官方 u2net.onnx 不一致，已丢弃")
    tmp.replace(dest)


def ensure_u2net_model() -> Path:
    """
    若 ~/.u2net/u2net.onnx 不存在或损坏，依次尝试主站与镜像下载。
    成功返回模型绝对路径。
    """
    dest = u2net_model_path()
    if dest.exists() and dest.stat().st_size >= MIN_VALID_BYTES:
        try:
            if _md5_hex(dest) == U2NET_MD5:
                return dest
        except OSError:
            pass
        dest.unlink(missing_ok=True)

    custom = os.getenv("U2NET_MIRROR_URLS", "").strip()
    urls = [U2NET_URL_PRIMARY] + U2NET_URL_MIRRORS
    if custom:
        urls = [u.strip() for u in custom.split(",") if u.strip()] + urls

    errors: list[str] = []
    for url in urls:
        try:
            print(f"⬇️ 尝试下载 u2net.onnx: {url[:80]}...")
            _download_to(url, dest, timeout=int(os.getenv("U2NET_DOWNLOAD_TIMEOUT", "180")))
            print(f"✅ u2net.onnx 已就绪: {dest}")
            return dest
        except Exception as e:
            errors.append(f"{url[:60]}... -> {e}")

    raise RuntimeError(
        "无法下载抠图模型 u2net.onnx（GitHub/镜像均失败）。"
        "可手动将官方文件放到: "
        f"{dest} "
        "或配置 remove.bg API（bg_removal_method=removebg + removebg_api_key）。"
        f" 详情: {' | '.join(errors[:3])}"
    )

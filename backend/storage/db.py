"""
数据库连接和 CRUD 操作（MySQL）
"""
import json
import os
from datetime import datetime
from typing import Any, List, Optional

import aiomysql
from dotenv import load_dotenv
from domain.clothes import ClothesCreate, ClothesItem
from storage.config_store import load_config
from storage.models import (
    CLOTHES_INDEX_SQL,
    CLOTHES_TABLE_SQL,
    HOROSCOPE_RECORDS_INDEX_SQL,
    HOROSCOPE_RECORDS_TABLE_SQL,
)

# 加载 backend/.env 到环境变量（不覆盖系统环境变量）
load_dotenv()


def _mysql_config() -> dict:
    return {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "db": os.getenv("MYSQL_DATABASE", "ai_wardrobe"),
        "charset": "utf8mb4",
        "autocommit": True,
    }


async def _connect():
    cfg = _mysql_config()
    return await aiomysql.connect(**cfg)


async def _safe_create_index(conn, sql: str) -> None:
    async with conn.cursor() as cursor:
        try:
            await cursor.execute(sql)
        except Exception as exc:
            msg = str(exc).lower()
            if "duplicate key name" in msg or "already exists" in msg:
                return
            raise


async def init_db():
    """初始化数据库，创建表和索引"""
    conn = await _connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(CLOTHES_TABLE_SQL)
            await cursor.execute(HOROSCOPE_RECORDS_TABLE_SQL)
        await _safe_create_index(conn, CLOTHES_INDEX_SQL)
        await _safe_create_index(conn, HOROSCOPE_RECORDS_INDEX_SQL)
    finally:
        conn.close()


async def add_clothes(clothes: ClothesCreate) -> int:
    conn = await _connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO clothes (
                    category, item, style_semantics, season_semantics,
                    usage_semantics, color_semantics, description, image_filename
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    clothes.category,
                    clothes.item,
                    json.dumps(clothes.style_semantics, ensure_ascii=False),
                    json.dumps(clothes.season_semantics, ensure_ascii=False),
                    json.dumps(clothes.usage_semantics, ensure_ascii=False),
                    clothes.color_semantics,
                    clothes.description,
                    clothes.image_filename,
                ),
            )
            return int(cursor.lastrowid)
    finally:
        conn.close()


async def get_all_clothes() -> List[ClothesItem]:
    conn = await _connect()
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM clothes ORDER BY created_at DESC")
            rows = await cursor.fetchall()
            return [_row_to_clothes_item(row) for row in rows]
    finally:
        conn.close()


async def get_clothes_by_category(category: str) -> List[ClothesItem]:
    conn = await _connect()
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM clothes WHERE category = %s ORDER BY created_at DESC",
                (category,),
            )
            rows = await cursor.fetchall()
            return [_row_to_clothes_item(row) for row in rows]
    finally:
        conn.close()


async def get_clothes_by_id(clothes_id: int) -> Optional[ClothesItem]:
    conn = await _connect()
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM clothes WHERE id = %s", (clothes_id,))
            row = await cursor.fetchone()
            return _row_to_clothes_item(row) if row else None
    finally:
        conn.close()


async def delete_clothes(clothes_id: int) -> bool:
    conn = await _connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM clothes WHERE id = %s", (clothes_id,))
            return cursor.rowcount > 0
    finally:
        conn.close()


async def update_clothes(clothes_id: int, clothes: ClothesCreate) -> bool:
    conn = await _connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                UPDATE clothes
                SET category = %s, item = %s, style_semantics = %s,
                    season_semantics = %s, usage_semantics = %s,
                    color_semantics = %s, description = %s
                WHERE id = %s
                """,
                (
                    clothes.category,
                    clothes.item,
                    json.dumps(clothes.style_semantics, ensure_ascii=False),
                    json.dumps(clothes.season_semantics, ensure_ascii=False),
                    json.dumps(clothes.usage_semantics, ensure_ascii=False),
                    clothes.color_semantics,
                    clothes.description,
                    clothes_id,
                ),
            )
            return cursor.rowcount > 0
    finally:
        conn.close()


async def get_horoscope_record(record_date: str, zodiac_sign: str) -> Optional[dict[str, Any]]:
    conn = await _connect()
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT * FROM horoscope_records
                WHERE record_date = %s AND zodiac_sign = %s
                LIMIT 1
                """,
                (record_date, zodiac_sign),
            )
            row = await cursor.fetchone()
            if not row:
                return None
            return _row_to_horoscope_record(row)
    finally:
        conn.close()


async def upsert_horoscope_source(
    record_date: str,
    zodiac_sign: str,
    zodiac_name: str,
    source_provider: str,
    source_payload: dict[str, Any],
) -> int:
    payload_json = json.dumps(source_payload, ensure_ascii=False)

    conn = await _connect()
    try:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT id FROM horoscope_records
                WHERE record_date = %s AND zodiac_sign = %s
                LIMIT 1
                """,
                (record_date, zodiac_sign),
            )
            existing = await cursor.fetchone()

            if existing:
                await cursor.execute(
                    """
                    UPDATE horoscope_records
                    SET zodiac_name = %s,
                        source_provider = %s,
                        source_payload = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (zodiac_name, source_provider, payload_json, existing["id"]),
                )
                return int(existing["id"])

            await cursor.execute(
                """
                INSERT INTO horoscope_records (
                    record_date, zodiac_sign, zodiac_name, source_provider, source_payload, llm_status
                ) VALUES (%s, %s, %s, %s, %s, 'pending')
                """,
                (record_date, zodiac_sign, zodiac_name, source_provider, payload_json),
            )
            return int(cursor.lastrowid)
    finally:
        conn.close()


async def update_horoscope_inference(
    record_id: int,
    llm_status: str,
    llm_reasoning: Optional[str] = None,
    llm_error: Optional[str] = None,
) -> None:
    conn = await _connect()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                UPDATE horoscope_records
                SET llm_status = %s,
                    llm_reasoning = %s,
                    llm_error = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (llm_status, llm_reasoning, llm_error, record_id),
            )
    finally:
        conn.close()


def _row_to_clothes_item(row: dict) -> ClothesItem:
    config = load_config()
    filename = row["image_filename"]
    if filename.startswith("http://") or filename.startswith("https://"):
        image_url = filename
    elif config.cos_public_base_url:
        image_url = f"{config.cos_public_base_url}/{filename.lstrip('/')}"
    else:
        image_url = f"/uploads/{filename}"

    return ClothesItem(
        id=int(row["id"]),
        category=row["category"],
        item=row["item"],
        style_semantics=json.loads(row.get("style_semantics") or "[]"),
        season_semantics=json.loads(row.get("season_semantics") or "[]"),
        usage_semantics=json.loads(row.get("usage_semantics") or "[]"),
        color_semantics=row.get("color_semantics") or "",
        description=row.get("description") or "",
        image_url=image_url,
        created_at=row.get("created_at") if isinstance(row.get("created_at"), datetime) else datetime.now(),
    )


def _row_to_horoscope_record(row: dict) -> dict[str, Any]:
    return {
        "id": int(row["id"]),
        "record_date": row["record_date"],
        "zodiac_sign": row["zodiac_sign"],
        "zodiac_name": row["zodiac_name"],
        "source_provider": row.get("source_provider") or "unknown",
        "source_payload": json.loads(row.get("source_payload") or "{}"),
        "llm_status": row.get("llm_status") or "pending",
        "llm_reasoning": row.get("llm_reasoning") or "",
        "llm_error": row.get("llm_error") or "",
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }

"""
MySQL 数据库模型定义
"""

CLOTHES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS clothes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    category VARCHAR(32) NOT NULL,
    item VARCHAR(255) NOT NULL,
    style_semantics JSON,
    season_semantics JSON,
    usage_semantics JSON,
    color_semantics VARCHAR(128),
    description TEXT,
    image_filename VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

CLOTHES_INDEX_SQL = """
CREATE INDEX idx_clothes_category ON clothes(category);
"""

HOROSCOPE_RECORDS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS horoscope_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    record_date VARCHAR(16) NOT NULL,
    zodiac_sign VARCHAR(64) NOT NULL,
    zodiac_name VARCHAR(64) NOT NULL,
    source_provider VARCHAR(64) NOT NULL,
    source_payload JSON NOT NULL,
    llm_status VARCHAR(32) NOT NULL DEFAULT 'pending',
    llm_reasoning TEXT,
    llm_error TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uniq_horoscope_record (record_date, zodiac_sign)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

HOROSCOPE_RECORDS_INDEX_SQL = """
CREATE INDEX idx_horoscope_date_sign ON horoscope_records(record_date, zodiac_sign);
"""

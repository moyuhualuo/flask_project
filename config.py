import os
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _database_uri():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
        elif database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        return database_url

    database_file = os.getenv("DATABASE_FILE", "data.db")
    # Vercel 函数环境只有 /tmp 可写；这里用于演示，正式数据建议接 DATABASE_URL。
    base_dir = Path(tempfile.gettempdir()) if os.getenv("VERCEL") else BASE_DIR
    return f"sqlite:///{(base_dir / database_file).as_posix()}"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = _database_uri()
    # 小项目默认自动建表，部署稳定后可设为 0，改用迁移流程管理结构。
    AUTO_CREATE_DB = os.getenv("AUTO_CREATE_DB", "1") != "0"


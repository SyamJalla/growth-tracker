try:
    # pydantic v2+: BaseSettings moved to pydantic-settings
    from pydantic_settings import BaseSettings
except Exception:
    from pydantic import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    app_name: str = "Growth Tracker API"
    env: str = "dev"
    # default to a local postgres connection; override with env var DATABASE_URL
    # admin_database_url is used to create new databases on the server (connects to 'postgres' by default)
    admin_database_url: str = "postgresql+psycopg2://postgres:root@localhost:5432/postgres"
    database_url: str = "postgresql+psycopg2://postgres:root@localhost:5432/growth_tracker"
    cors_origins: List[str] = ["*"]

    mail_username: Optional[str] = None
    mail_password: Optional[str] = None
    mail_from: Optional[str] = "noreply@example.com"
    mail_server: Optional[str] = None
    mail_port: int = 587

    class Config:
        env_file = ".env"

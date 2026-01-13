try:
    # pydantic v2+: BaseSettings moved to pydantic-settings
    from pydantic_settings import BaseSettings
except Exception:
    from pydantic import BaseSettings
from typing import List, Optional
import configparser
import os


class Settings(BaseSettings):
    app_name: str = "Growth Tracker API"
    env: str = "local"  # Options: local, dev, prod
    cors_origins: List[str] = ["*"]

    mail_username: Optional[str] = None
    mail_password: Optional[str] = None
    mail_from: Optional[str] = "noreply@example.com"
    mail_server: Optional[str] = None
    mail_port: int = 587

    # Database URLs will be loaded from config.ini based on environment
    database_url: Optional[str] = None
    admin_database_url: Optional[str] = None

    class Config:
        # Load environment-specific .env file
        # Priority: .env.{ENV} > .env.local > .env
        @staticmethod
        def get_env_file():
            env = os.getenv("ENV", "local")
            env_file = f".env.{env}"
            if os.path.exists(env_file):
                return env_file
            elif os.path.exists(".env.local"):
                return ".env.local"
            return ".env"
        
        env_file = get_env_file()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load database configuration from config.ini
        self._load_database_config()

    def _load_database_config(self):
        """Load database configuration from config.ini based on environment"""
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.ini")
        
        if os.path.exists(config_path):
            config.read(config_path)
            
            # Get the environment section (default to 'local' if not found)
            env_section = self.env if config.has_section(self.env) else "local"
            
            if config.has_section(env_section):
                self.database_url = config.get(env_section, "database_url", fallback=self.database_url)
                self.admin_database_url = config.get(env_section, "admin_database_url", fallback=self.admin_database_url)
        else:
            # Fallback to default values if config.ini not found
            if not self.database_url:
                self.database_url = "postgresql+psycopg2://postgres:root@localhost:5432/growth_tracker"
            if not self.admin_database_url:
                self.admin_database_url = "postgresql+psycopg2://postgres:root@localhost:5432/postgres"

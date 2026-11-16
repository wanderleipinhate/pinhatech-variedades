import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Pinhatech & Variedades"
    APP_ENV: str = "development"
    APP_URL: str = "http://localhost:8000"
    
    # Autenticação Administrativa
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "PinhatechAdmin2025!"
    SECRET_KEY: str = "pinhatech-super-secret-key-change-this-in-production-affiliate-store-2025"
    
    # Banco de Dados
    DATABASE_URL: str = "sqlite:///./pinhatech.db"
    
    # Canais Sociais / Divulgação
    TELEGRAM_VIP_URL: str = "https://t.me/pinhatech_ofertas"
    WHATSAPP_VIP_URL: str = "https://chat.whatsapp.com/exemplo"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

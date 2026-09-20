from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CRM IT School"
    env: str = Field(default="local")
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "RS256"
    access_token_ttl_sec: int = 3600

    keycloak_url: str = "http://keycloak:8080"
    keycloak_realm: str = "crm"
    keycloak_client_id: str = "crm-backend"
    keycloak_client_secret: str = "change-me"
    keycloak_verify_audience: bool = False
    keycloak_audience: str | None = None

    database_url: str = "postgresql+asyncpg://crm:crm_secret@postgres:5432/crm"
    db_echo: bool = False
    db_pool_size: int = 10
    db_max_overflow: int = 20

    redis_url: str = "redis://redis:6379/0"
    celery_broker_url: str = "redis://redis:6379/1"
    celery_result_backend: str = "redis://redis:6379/2"
    
    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "crm-files"
    minio_secure: bool = False
    minio_presigned_ttl_sec: int = 3600

    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def keycloak_issuer(self) -> str:
        return f"{self.keycloak_url}/realms/{self.keycloak_realm}"

    @property
    def keycloak_jwks_url(self) -> str:
        return f"{self.keycloak_issuer}/protocol/openid-connect/certs"

    @property
    def keycloak_token_url(self) -> str:
        return f"{self.keycloak_issuer}/protocol/openid-connect/token"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
"""Application settings. All secrets come from the environment; nothing
secret has a default value. See ../../.env.example."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "development"
    database_url: str = (
        "postgresql+psycopg://domainfolio:domainfolio@localhost:5432/domainfolio"
    )
    redis_url: str = "redis://localhost:6379/0"
    meilisearch_url: str = "http://localhost:7700"
    meilisearch_master_key: str = ""

    # Auth — no defaults for secrets. The app fails closed at startup
    # if these are unset in any env other than local skeleton tests.
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    session_secret: str = ""

    # External providers — sandbox only until approved (see master plan).
    escrow_provider: str = "stub"  # stub | escrow_com
    escrow_api_base_url: str = ""
    escrow_api_key: str = ""
    escrow_webhook_secret: str = ""
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_connect_enabled: bool = False  # NEVER True without provider approval.

    # Object storage (S3-compatible) — used for uploads in later stages.
    s3_endpoint_url: str = ""
    s3_bucket: str = ""
    s3_access_key: str = ""
    s3_secret_key: str = ""

    # SMTP for transactional mail (verification, notifications).
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    mail_from: str = "noreply@domainfolio.site"

    public_base_url: str = "http://localhost:3000"


settings = Settings()

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    environment: str = os.getenv("ENV", "development")
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key")
    database_url: str = os.getenv("DATABASE_URL", "sqlite+pysqlite:///./qca.db")

    # OAuth
    google_client_id: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    google_client_secret: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    github_client_id: Optional[str] = os.getenv("GITHUB_CLIENT_ID")
    github_client_secret: Optional[str] = os.getenv("GITHUB_CLIENT_SECRET")

    # Stripe
    stripe_secret_key: Optional[str] = os.getenv("STRIPE_SECRET_KEY")
    stripe_publishable_key: Optional[str] = os.getenv("STRIPE_PUBLISHABLE_KEY")
    stripe_price_pro: Optional[str] = os.getenv("STRIPE_PRICE_PRO")
    stripe_price_enterprise: Optional[str] = os.getenv("STRIPE_PRICE_ENTERPRISE")
    stripe_webhook_secret: Optional[str] = os.getenv("STRIPE_WEBHOOK_SECRET")

    # Promotions
    sa95_promo_code: Optional[str] = os.getenv("SA95_PROMO_CODE", "SA95")

    # Memory defaults
    max_history_turns: int = int(os.getenv("MAX_HISTORY_TURNS", "8"))
    drop_earliest_turns_first: bool = True


settings = Settings()


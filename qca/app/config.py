from pydantic import BaseSettings, Field
from typing import List

class Settings(BaseSettings):
    app_name: str = "QCA"
    versions: List[str] = Field(default_factory=lambda: [
        "QCA-4.9", "QCA-5.1", "QCA-5.3", "QCA-5.5", "QCA-5.7",
        "QCA-5.9", "QCA-6.1", "QCA-6.3", "QCA-6.5", "QCA-6.8-SUPREME",
    ])
    google_client_id: str = ""
    google_client_secret: str = ""
    github_client_id: str = ""
    github_client_secret: str = ""
    stripe_publishable_key: str = ""
    stripe_secret_key: str = ""
    render_port: int = 10000

    class Config:
        env_file = ".env"

settings = Settings()

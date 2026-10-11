"""Configuratie uit omgevingsvariabelen. Niets hiervan hoort in git."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


class ConfigError(RuntimeError):
    pass


def _split(value: str | None) -> list[str]:
    if not value:
        return []
    return [v.strip().replace(" ", "").upper() for v in value.split(",") if v.strip()]


@dataclass
class Config:
    application_id: str
    private_key_pem: str
    redirect_url: str
    data_dir: Path
    api_base: str = "https://api.enablebanking.com"
    sheet_id: str | None = None
    google_service_account_json: str | None = None
    # IBAN's van eigen vennootschappen: transfers hiermee = rekening-courant-signaal.
    company_ibans: list[str] = field(default_factory=list)
    # Whitelist: enkel deze IBAN's (op naam van Bart alleen) mogen geregistreerd worden.
    allowed_ibans: list[str] = field(default_factory=list)
    # Drempel (EUR) voor het signaal "grote uitgave".
    large_outflow_threshold: float = 5000.0

    @classmethod
    def from_env(cls, require_bank: bool = True) -> "Config":
        env = os.environ
        app_id = env.get("EB_APPLICATION_ID", "")
        key = env.get("EB_PRIVATE_KEY", "")
        key_path = env.get("EB_PRIVATE_KEY_PATH")
        if not key and key_path:
            key = Path(key_path).read_text()
        if require_bank and (not app_id or not key):
            raise ConfigError(
                "EB_APPLICATION_ID en EB_PRIVATE_KEY (of EB_PRIVATE_KEY_PATH) zijn vereist."
            )
        sa_json = env.get("GOOGLE_SERVICE_ACCOUNT_JSON")
        sa_path = env.get("GOOGLE_SERVICE_ACCOUNT_JSON_PATH")
        if not sa_json and sa_path:
            sa_json = Path(sa_path).read_text()
        return cls(
            application_id=app_id,
            private_key_pem=key,
            redirect_url=env.get("EB_REDIRECT_URL", "https://enablebanking.com/"),
            data_dir=Path(env.get("BANKFEED_DATA_DIR", "data/bankfeed")),
            api_base=env.get("EB_API_BASE", "https://api.enablebanking.com"),
            sheet_id=env.get("BANKFEED_SHEET_ID") or None,
            google_service_account_json=sa_json or None,
            company_ibans=_split(env.get("BANKFEED_COMPANY_IBANS")),
            allowed_ibans=_split(env.get("BANKFEED_ALLOWED_IBANS")),
            large_outflow_threshold=float(env.get("BANKFEED_LARGE_OUTFLOW_EUR", "5000")),
        )

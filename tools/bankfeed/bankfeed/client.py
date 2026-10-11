"""Minimale Enable Banking-client, enkel Account Information (AIS).

Bewust geen /payments-endpoints: deze koppeling kan nooit geld bewegen.
API-referentie: https://enablebanking.com/docs/api/reference/
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Iterator

import jwt
import requests


class EnableBankingError(RuntimeError):
    def __init__(self, status: int, body: str, path: str):
        super().__init__(f"Enable Banking {path} -> HTTP {status}: {body[:300]}")
        self.status = status
        self.body = body
        self.path = path


class EnableBankingClient:
    def __init__(
        self,
        application_id: str,
        private_key_pem: str,
        api_base: str = "https://api.enablebanking.com",
        session: requests.Session | None = None,
        timeout: float = 30.0,
    ):
        self.application_id = application_id
        self.private_key_pem = private_key_pem
        self.api_base = api_base.rstrip("/")
        self.http = session or requests.Session()
        self.timeout = timeout
        self._token: str | None = None
        self._token_exp: float = 0.0

    # --- auth -------------------------------------------------------------
    def _jwt(self) -> str:
        now = int(time.time())
        if self._token and now < self._token_exp - 60:
            return self._token
        exp = now + 3600
        self._token = jwt.encode(
            {"iss": "enablebanking.com", "aud": "api.enablebanking.com", "iat": now, "exp": exp},
            self.private_key_pem,
            algorithm="RS256",
            headers={"kid": self.application_id},
        )
        self._token_exp = exp
        return self._token

    def _request(self, method: str, path: str, **kwargs: Any) -> dict:
        headers = {"Authorization": f"Bearer {self._jwt()}"}
        resp = self.http.request(
            method, f"{self.api_base}{path}", headers=headers, timeout=self.timeout, **kwargs
        )
        if resp.status_code >= 400:
            raise EnableBankingError(resp.status_code, resp.text, path)
        return resp.json() if resp.content else {}

    # --- banken en consent -------------------------------------------------
    def list_aspsps(self, country: str = "BE", psu_type: str = "personal") -> list[dict]:
        data = self._request("GET", "/aspsps", params={"country": country, "psu_type": psu_type})
        return data.get("aspsps", [])

    def start_authorization(
        self,
        bank_name: str,
        country: str,
        redirect_url: str,
        valid_days: int = 180,
        psu_type: str = "personal",
    ) -> dict:
        """Start de consent. Geeft {'url', 'authorization_id', 'state'} terug.

        Bart opent de url, autoriseert bij de bank (itsme/kaartlezer) en wordt
        doorgestuurd naar redirect_url?code=...&state=...
        """
        valid_until = datetime.now(timezone.utc) + timedelta(days=valid_days)
        state = str(uuid.uuid4())
        data = self._request(
            "POST",
            "/auth",
            json={
                "access": {"valid_until": valid_until.isoformat()},
                "aspsp": {"name": bank_name, "country": country},
                "state": state,
                "redirect_url": redirect_url,
                "psu_type": psu_type,
            },
        )
        data["state"] = state
        return data

    def create_session(self, code: str) -> dict:
        return self._request("POST", "/sessions", json={"code": code})

    def get_session(self, session_id: str) -> dict:
        return self._request("GET", f"/sessions/{session_id}")

    # --- rekeningdata ------------------------------------------------------
    def get_account_details(self, account_uid: str) -> dict:
        return self._request("GET", f"/accounts/{account_uid}/details")

    def get_balances(self, account_uid: str) -> list[dict]:
        return self._request("GET", f"/accounts/{account_uid}/balances").get("balances", [])

    def iter_transactions(
        self, account_uid: str, date_from: str | None = None, date_to: str | None = None
    ) -> Iterator[dict]:
        """Alle geboekte transacties, over alle pagina's (continuation_key)."""
        params: dict[str, str] = {"transaction_status": "BOOK"}
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        seen_keys: set[str] = set()
        while True:
            data = self._request("GET", f"/accounts/{account_uid}/transactions", params=params)
            yield from data.get("transactions", [])
            key = data.get("continuation_key")
            if not key or key in seen_keys:
                return
            seen_keys.add(key)
            params["continuation_key"] = key

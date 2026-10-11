"""Optionele sink: privé Google Sheet via een service account (alleen deze Sheet gedeeld).

Geen extra libraries: OAuth via JWT-bearer (RFC 7523) met PyJWT, daarna Sheets REST v4.
De Sheet is ook de bron voor ontdubbeling, zodat de sync in een tijdelijke container kan lopen.
"""

from __future__ import annotations

import json
import time

import jwt
import requests

from .normalize import COLUMNS
from .store import BALANCE_COLUMNS

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
TX_TAB = "Transacties"
BAL_TAB = "Saldi"
ACC_TAB = "Rekeningen"
ACCOUNT_COLUMNS = ["label", "bank", "country", "iban", "uid", "session_id", "valid_until"]


class SheetSink:
    def __init__(self, sheet_id: str, service_account_json: str, session: requests.Session | None = None):
        self.sheet_id = sheet_id
        self.sa = json.loads(service_account_json)
        self.http = session or requests.Session()
        self._token: str | None = None
        self._exp = 0.0

    def _access_token(self) -> str:
        now = int(time.time())
        if self._token and now < self._exp - 60:
            return self._token
        assertion = jwt.encode(
            {
                "iss": self.sa["client_email"],
                "scope": SCOPE,
                "aud": self.sa.get("token_uri", "https://oauth2.googleapis.com/token"),
                "iat": now,
                "exp": now + 3600,
            },
            self.sa["private_key"],
            algorithm="RS256",
        )
        resp = self.http.post(
            self.sa.get("token_uri", "https://oauth2.googleapis.com/token"),
            data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": assertion},
            timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()
        self._token, self._exp = body["access_token"], now + int(body.get("expires_in", 3600))
        return self._token

    def _call(self, method: str, path: str, **kwargs) -> dict:
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{self.sheet_id}{path}"
        resp = self.http.request(
            method, url, headers={"Authorization": f"Bearer {self._access_token()}"}, timeout=30, **kwargs
        )
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    def _values(self, rng: str) -> list[list[str]]:
        return self._call("GET", f"/values/{rng}").get("values", [])

    def _append(self, tab: str, rows: list[list[str]]) -> None:
        self._call(
            "POST",
            f"/values/{tab}!A1:append",
            params={"valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS"},
            json={"values": rows},
        )

    def _ensure_tab(self, tab: str, header: list[str]) -> None:
        meta = self._call("GET", "", params={"fields": "sheets.properties.title"})
        titles = {s["properties"]["title"] for s in meta.get("sheets", [])}
        if tab not in titles:
            self._call("POST", ":batchUpdate", json={"requests": [{"addSheet": {"properties": {"title": tab}}}]})
        if not self._values(f"{tab}!A1:A1"):
            self._append(tab, [header])

    def append_transactions(self, rows: list[dict]) -> int:
        self._ensure_tab(TX_TAB, COLUMNS)
        known = {r[0] for r in self._values(f"{TX_TAB}!A2:A") if r}
        new: dict[str, dict] = {}
        for r in rows:
            if r["id"] not in known:
                new.setdefault(r["id"], r)
        if new:
            self._append(TX_TAB, [[r[c] for c in COLUMNS] for r in new.values()])
        return len(new)

    def read_transactions(self) -> list[dict]:
        self._ensure_tab(TX_TAB, COLUMNS)
        values = self._values(f"{TX_TAB}!A2:Z")
        return [dict(zip(COLUMNS, row + [""] * (len(COLUMNS) - len(row)))) for row in values if row]

    def save_accounts(self, accounts: list[dict]) -> None:
        """Rekeningregister (geen sleutels): laat de sync in een tijdelijke container draaien."""
        self._ensure_tab(ACC_TAB, ACCOUNT_COLUMNS)
        rows = [ACCOUNT_COLUMNS] + [[a.get(c, "") for c in ACCOUNT_COLUMNS] for a in accounts]
        self._call("POST", f"/values/{ACC_TAB}!A:Z:clear", json={})
        self._call("PUT", f"/values/{ACC_TAB}!A1", params={"valueInputOption": "RAW"}, json={"values": rows})

    def load_accounts(self) -> list[dict]:
        self._ensure_tab(ACC_TAB, ACCOUNT_COLUMNS)
        values = self._values(f"{ACC_TAB}!A1:Z")
        if len(values) < 2:
            return []
        header = values[0]
        return [dict(zip(header, row + [""] * (len(header) - len(row)))) for row in values[1:] if row]

    def append_balances(self, rows: list[dict]) -> None:
        if not rows:
            return
        self._ensure_tab(BAL_TAB, BALANCE_COLUMNS)
        self._append(BAL_TAB, [[r[c] for c in BALANCE_COLUMNS] for r in rows])

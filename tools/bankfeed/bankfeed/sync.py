"""Koppelen (consent → sessie → rekeningen) en dagelijkse sync."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from .client import EnableBankingClient, EnableBankingError
from .normalize import to_row
from .signals import _parse_dt


def _label(bank: str, iban: str, uid: str) -> str:
    short = (bank.split() or ["Bank"])[0]
    tail = (iban or uid)[-4:]
    return f"{short} …{tail}"


def accounts_from_session(client: EnableBankingClient, session: dict, bank: str, country: str) -> list[dict]:
    valid_until = (session.get("access") or {}).get("valid_until", "")
    out = []
    for acc in session.get("accounts", []):
        if isinstance(acc, str):  # oudere API-vorm: enkel uid's
            uid = acc
            details = client.get_account_details(uid)
        else:
            uid = acc["uid"]
            details = acc
        iban = ((details.get("account_id") or {}).get("iban") or "").replace(" ", "").upper()
        out.append(
            {
                "label": _label(bank, iban, uid),
                "bank": bank,
                "country": country,
                "iban": iban,
                "uid": uid,
                "session_id": session.get("session_id", ""),
                "valid_until": valid_until,
            }
        )
    return out


def filter_allowed(accounts: list[dict], allowed: list[str], company: list[str]) -> tuple[list[dict], list[dict]]:
    """Enkel whitelisted privé-IBAN's; vennootschapsrekeningen worden altijd geweigerd.

    Lege whitelist = alles weigeren (fail closed).
    """
    allowed_set = {i.upper() for i in allowed}
    company_set = {i.upper() for i in company}
    keep, rejected = [], []
    for a in accounts:
        iban = a.get("iban", "").upper()
        (keep if iban and iban in allowed_set and iban not in company_set else rejected).append(a)
    return keep, rejected


def merge_accounts(existing: list[dict], new: list[dict]) -> list[dict]:
    """Nieuwe consent vervangt dezelfde rekening (zelfde IBAN of uid)."""
    keys = {(a.get("iban") or a["uid"]) for a in new}
    return [a for a in existing if (a.get("iban") or a["uid"]) not in keys] + new


def run_sync(client, accounts: list[dict], sinks: list, days: int = 14, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    date_from = (now.date() - timedelta(days=days)).isoformat()
    summary = {"synced_at": now.isoformat(timespec="seconds"), "accounts": []}
    for acc in accounts:
        item = {"account": acc["label"], "new_transactions": 0, "status": "ok"}
        vu = _parse_dt(acc.get("valid_until", ""))
        if vu and vu <= now:
            item["status"] = "consent verlopen — opnieuw koppelen"
            summary["accounts"].append(item)
            continue
        try:
            try:
                txs = list(client.iter_transactions(acc["uid"], date_from=date_from))
            except EnableBankingError as e:
                # 422 WRONG_TRANSACTIONS_PERIOD: bank laat zo ver terug niet toe → 89 dagen.
                if e.status != 422 or days <= 89:
                    raise
                short_from = (now.date() - timedelta(days=89)).isoformat()
                txs = list(client.iter_transactions(acc["uid"], date_from=short_from))
                item["note"] = "historiek beperkt tot 89 dagen door de bank"
            rows = [to_row(acc["label"], tx) for tx in txs]
            balances = [
                {
                    "synced_at": summary["synced_at"],
                    "account": acc["label"],
                    "balance_type": b.get("balance_type", ""),
                    "amount": (b.get("balance_amount") or {}).get("amount", ""),
                    "currency": (b.get("balance_amount") or {}).get("currency", ""),
                    "reference_date": b.get("reference_date", "") or "",
                }
                for b in client.get_balances(acc["uid"])
            ]
            added = [sink.append_transactions(rows) for sink in sinks]
            for sink in sinks:
                sink.append_balances(balances)
            item["fetched"] = len(rows)
            item["new_transactions"] = max(added) if added else 0
        except EnableBankingError as e:
            item["status"] = f"fout HTTP {e.status}" + (" — consent ongeldig, opnieuw koppelen" if e.status in (401, 403) else "")
        summary["accounts"].append(item)
    return summary


def consent_warnings(accounts: list[dict], today: date | None = None, within_days: int = 21) -> list[str]:
    today = today or date.today()
    out = []
    for a in accounts:
        vu = _parse_dt(a.get("valid_until", ""))
        if vu and (vu.date() - today).days <= within_days:
            out.append(f"{a['label']}: consent vervalt op {vu.date().isoformat()}")
    return out

"""Zet Enable Banking-transacties om naar vlakke rijen (één formaat voor CSV en Sheet)."""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal

COLUMNS = [
    "id",
    "account",
    "booking_date",
    "value_date",
    "amount",
    "currency",
    "counterparty",
    "counterparty_iban",
    "description",
    "bank_code",
]


def _iban(party_account: dict | None) -> str:
    if not party_account:
        return ""
    return (party_account.get("iban") or party_account.get("other", {}).get("identification") or "").replace(" ", "").upper()


def signed_amount(tx: dict) -> Decimal:
    amount = Decimal(str(tx.get("transaction_amount", {}).get("amount", "0")))
    amount = abs(amount)
    return -amount if tx.get("credit_debit_indicator") == "DBIT" else amount


def transaction_id(account: str, tx: dict) -> str:
    """Stabiele sleutel voor ontdubbeling. entry_reference als de bank die geeft."""
    ref = tx.get("entry_reference") or tx.get("transaction_id")
    if ref:
        return f"{account}:{ref}"
    basis = json.dumps(
        [
            tx.get("booking_date"),
            tx.get("value_date"),
            str(signed_amount(tx)),
            tx.get("remittance_information"),
            (tx.get("creditor") or {}).get("name"),
            (tx.get("debtor") or {}).get("name"),
        ],
        sort_keys=True,
        default=str,
    )
    return f"{account}:h{hashlib.sha256(basis.encode()).hexdigest()[:16]}"


def to_row(account: str, tx: dict) -> dict:
    amount = signed_amount(tx)
    # Tegenpartij: bij een uitgave de begunstigde, bij een inkomst de opdrachtgever.
    if amount < 0:
        party, party_acc = tx.get("creditor"), tx.get("creditor_account")
    else:
        party, party_acc = tx.get("debtor"), tx.get("debtor_account")
    remittance = tx.get("remittance_information") or []
    if isinstance(remittance, str):
        remittance = [remittance]
    return {
        "id": transaction_id(account, tx),
        "account": account,
        "booking_date": tx.get("booking_date") or "",
        "value_date": tx.get("value_date") or "",
        "amount": str(amount),
        "currency": tx.get("transaction_amount", {}).get("currency", ""),
        "counterparty": (party or {}).get("name", "") or "",
        "counterparty_iban": _iban(party_acc),
        "description": " ".join(r.strip() for r in remittance if r).strip(),
        "bank_code": (tx.get("bank_transaction_code") or {}).get("description", "") or "",
    }

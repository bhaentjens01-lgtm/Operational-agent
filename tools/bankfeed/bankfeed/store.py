"""Lokale opslag in BANKFEED_DATA_DIR (standaard data/bankfeed, gitignored).

state.json        sessies en rekeningen (geen sleutels, geen tokens)
transactions.csv  alle transacties, ontdubbeld op id
balances.csv      saldo per rekening per sync
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path

from .normalize import COLUMNS

BALANCE_COLUMNS = ["synced_at", "account", "balance_type", "amount", "currency", "reference_date"]


class LocalStore:
    def __init__(self, data_dir: Path):
        self.dir = Path(data_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(self.dir, 0o700)
        except OSError:
            pass
        self.state_path = self.dir / "state.json"
        self.tx_path = self.dir / "transactions.csv"
        self.bal_path = self.dir / "balances.csv"

    # --- state -------------------------------------------------------------
    def load_state(self) -> dict:
        if not self.state_path.exists():
            return {"pending": {}, "sessions": []}
        return json.loads(self.state_path.read_text())

    def save_state(self, state: dict) -> None:
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, indent=2, sort_keys=True))
        os.replace(tmp, self.state_path)

    # --- transacties -------------------------------------------------------
    def existing_ids(self) -> set[str]:
        if not self.tx_path.exists():
            return set()
        with self.tx_path.open(newline="") as f:
            return {row["id"] for row in csv.DictReader(f)}

    def read_transactions(self) -> list[dict]:
        if not self.tx_path.exists():
            return []
        with self.tx_path.open(newline="") as f:
            return list(csv.DictReader(f))

    def append_transactions(self, rows: list[dict]) -> int:
        """Voegt enkel nieuwe rijen toe. Geeft het aantal toegevoegde rijen terug."""
        known = self.existing_ids()
        new = [r for r in rows if r["id"] not in known]
        # Ook binnen dezelfde batch ontdubbelen.
        unique: dict[str, dict] = {}
        for r in new:
            unique.setdefault(r["id"], r)
        if not unique:
            return 0
        write_header = not self.tx_path.exists()
        with self.tx_path.open("a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS)
            if write_header:
                w.writeheader()
            w.writerows(unique.values())
        return len(unique)

    def append_balances(self, rows: list[dict]) -> None:
        write_header = not self.bal_path.exists()
        with self.bal_path.open("a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=BALANCE_COLUMNS)
            if write_header:
                w.writeheader()
            w.writerows(rows)

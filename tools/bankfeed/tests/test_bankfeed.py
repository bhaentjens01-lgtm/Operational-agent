"""Tests met gesimuleerde API-antwoorden. Alle IBAN's en bedragen zijn fictief."""

import json
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from bankfeed.client import EnableBankingClient, EnableBankingError
from bankfeed.normalize import to_row, transaction_id
from bankfeed.signals import build_signals, render_markdown
from bankfeed.store import LocalStore
from bankfeed.sync import accounts_from_session, filter_allowed, merge_accounts, run_sync

KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
PEM = KEY.private_bytes(
    serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
).decode()
PUB = KEY.public_key()

OWN = "BE00111122223333"
OWN2 = "BE00999988887777"
COMPANY = "BE00444455556666"


class FakeResponse:
    def __init__(self, status, body):
        self.status_code = status
        self._body = body
        self.text = json.dumps(body)
        self.content = self.text.encode()

    def json(self):
        return self._body


class FakeHTTP:
    """Route (method, path) -> lijst van antwoorden (in volgorde)."""

    def __init__(self, routes):
        self.routes = {k: list(v) for k, v in routes.items()}
        self.calls = []

    def request(self, method, url, headers=None, params=None, json=None, timeout=None):
        path = url.split("api.example", 1)[1]
        self.calls.append({"method": method, "path": path, "params": dict(params or {}), "json": json, "headers": headers})
        queue = self.routes[(method, path)]
        status, body = queue.pop(0) if len(queue) > 1 else queue[0]
        return FakeResponse(status, body)


def client(routes):
    http = FakeHTTP(routes)
    return EnableBankingClient("app-123", PEM, "https://api.example", session=http), http


def tx(ref, amount, ind, date_, cp_name="Winkel", cp_iban="BE00000000000001", remit="test"):
    party = "creditor" if ind == "DBIT" else "debtor"
    return {
        "entry_reference": ref,
        "transaction_amount": {"amount": str(amount), "currency": "EUR"},
        "credit_debit_indicator": ind,
        "booking_date": date_,
        "value_date": date_,
        party: {"name": cp_name},
        f"{party}_account": {"iban": cp_iban},
        "remittance_information": [remit],
    }


class ClientTests(unittest.TestCase):
    def test_jwt_header_and_claims(self):
        c, http = client({("GET", "/aspsps"): [(200, {"aspsps": []})]})
        c.list_aspsps("BE")
        token = http.calls[0]["headers"]["Authorization"].split()[1]
        self.assertEqual(jwt.get_unverified_header(token)["kid"], "app-123")
        claims = jwt.decode(token, PUB, algorithms=["RS256"], audience="api.enablebanking.com")
        self.assertEqual(claims["iss"], "enablebanking.com")
        self.assertEqual(http.calls[0]["params"], {"country": "BE", "psu_type": "personal"})

    def test_start_authorization_body(self):
        c, http = client({("POST", "/auth"): [(200, {"url": "https://bank/x", "authorization_id": "a1"})]})
        out = c.start_authorization("KBC", "BE", "https://redirect", valid_days=90)
        body = http.calls[0]["json"]
        self.assertEqual(body["aspsp"], {"name": "KBC", "country": "BE"})
        self.assertEqual(body["psu_type"], "personal")
        self.assertEqual(body["state"], out["state"])
        self.assertIn("valid_until", body["access"])

    def test_transactions_pagination(self):
        c, http = client(
            {
                ("GET", "/accounts/u1/transactions"): [
                    (200, {"transactions": [tx("r1", 10, "CRDT", "2026-10-01")], "continuation_key": "k1"}),
                    (200, {"transactions": [tx("r2", 5, "DBIT", "2026-10-02")], "continuation_key": None}),
                ]
            }
        )
        got = list(c.iter_transactions("u1", date_from="2026-09-01"))
        self.assertEqual([t["entry_reference"] for t in got], ["r1", "r2"])
        self.assertEqual(http.calls[1]["params"]["continuation_key"], "k1")
        self.assertEqual(http.calls[0]["params"]["transaction_status"], "BOOK")

    def test_error_raises(self):
        c, _ = client({("GET", "/accounts/u1/balances"): [(401, {"error": "expired"})]})
        with self.assertRaises(EnableBankingError) as ctx:
            c.get_balances("u1")
        self.assertEqual(ctx.exception.status, 401)

    def test_no_payment_endpoints(self):
        self.assertFalse([m for m in dir(EnableBankingClient) if "pay" in m.lower()])


class NormalizeTests(unittest.TestCase):
    def test_sign_and_counterparty(self):
        r = to_row("KBC …3333", tx("r1", "12.50", "DBIT", "2026-10-03", "Bakker", "be00 0000 0000 0002"))
        self.assertEqual(r["amount"], "-12.50")
        self.assertEqual(r["counterparty"], "Bakker")
        self.assertEqual(r["counterparty_iban"], "BE00000000000002")
        self.assertEqual(r["id"], "KBC …3333:r1")

    def test_hash_id_stable_without_reference(self):
        t = tx(None, 7, "DBIT", "2026-10-03")
        self.assertEqual(transaction_id("A", t), transaction_id("A", dict(t)))
        self.assertTrue(transaction_id("A", t).startswith("A:h"))


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = LocalStore(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_accounts_from_session(self):
        c, _ = client({})
        session = {
            "session_id": "s1",
            "access": {"valid_until": "2027-04-01T00:00:00+00:00"},
            "accounts": [{"uid": "u1", "account_id": {"iban": OWN}}],
        }
        accs = accounts_from_session(c, session, "KBC Bank", "BE")
        self.assertEqual(accs[0]["label"], "KBC …3333")
        self.assertEqual(accs[0]["session_id"], "s1")

    def test_merge_replaces_same_iban(self):
        old = [{"uid": "u-old", "iban": OWN, "label": "x"}]
        new = [{"uid": "u-new", "iban": OWN, "label": "x"}]
        self.assertEqual(merge_accounts(old, new), new)

    def test_sync_dedup_and_expired(self):
        routes = {
            ("GET", "/accounts/u1/transactions"): [(200, {"transactions": [tx("r1", 10, "CRDT", "2026-10-01")]})],
            ("GET", "/accounts/u1/balances"): [
                (200, {"balances": [{"balance_type": "CLBD", "balance_amount": {"amount": "100", "currency": "EUR"}}]})
            ],
        }
        c, _ = client(routes)
        accounts = [
            {"label": "KBC …3333", "uid": "u1", "valid_until": "2027-01-01T00:00:00+00:00"},
            {"label": "ING …7777", "uid": "u2", "valid_until": "2026-01-01T00:00:00+00:00"},
        ]
        now = datetime(2026, 10, 11, tzinfo=timezone.utc)
        s1 = run_sync(c, accounts, [self.store], now=now)
        s2 = run_sync(c, accounts, [self.store], now=now)
        self.assertEqual(s1["accounts"][0]["new_transactions"], 1)
        self.assertEqual(s2["accounts"][0]["new_transactions"], 0)
        self.assertIn("verlopen", s1["accounts"][1]["status"])
        self.assertEqual(len(self.store.read_transactions()), 1)

    def test_sync_error_isolated_per_account(self):
        routes = {("GET", "/accounts/u1/transactions"): [(403, {"error": "consent"})]}
        c, _ = client(routes)
        s = run_sync(c, [{"label": "A", "uid": "u1", "valid_until": ""}], [self.store])
        self.assertIn("403", s["accounts"][0]["status"])


class GuardrailTests(unittest.TestCase):
    def test_whitelist_fail_closed_and_company_rejected(self):
        accs = [{"iban": OWN, "label": "a"}, {"iban": COMPANY, "label": "b"}, {"iban": OWN2, "label": "c"}]
        keep, rej = filter_allowed(accs, [OWN, COMPANY], [COMPANY])
        self.assertEqual([a["label"] for a in keep], ["a"])
        self.assertEqual([a["label"] for a in rej], ["b", "c"])
        keep, _ = filter_allowed(accs, [], [])
        self.assertEqual(keep, [])

    def test_422_falls_back_to_89_days(self):
        routes = {
            ("GET", "/accounts/u1/transactions"): [
                (422, {"error": "WRONG_TRANSACTIONS_PERIOD"}),
                (200, {"transactions": [tx("r1", 1, "CRDT", "2026-10-01")]}),
            ],
            ("GET", "/accounts/u1/balances"): [(200, {"balances": []})],
        }
        c, http = client(routes)
        with tempfile.TemporaryDirectory() as d:
            now = datetime(2026, 10, 11, tzinfo=timezone.utc)
            s = run_sync(c, [{"label": "A", "uid": "u1", "valid_until": ""}], [LocalStore(Path(d))], days=365, now=now)
        self.assertEqual(s["accounts"][0]["status"], "ok")
        self.assertEqual(http.calls[1]["params"]["date_from"], "2026-07-14")


class CliTests(unittest.TestCase):
    def test_link_complete_sync_signals(self):
        import os
        from unittest import mock

        from bankfeed import cli

        routes = {
            ("GET", "/aspsps"): [(200, {"aspsps": [{"name": "KBC", "maximum_consent_validity": 90 * 86400}]})],
            ("POST", "/auth"): [(200, {"url": "https://bank/consent", "authorization_id": "a1"})],
            ("POST", "/sessions"): [
                (
                    200,
                    {
                        "session_id": "s1",
                        "access": {"valid_until": "2027-01-09T00:00:00+00:00"},
                        "accounts": [
                            {"uid": "u1", "account_id": {"iban": OWN}},
                            {"uid": "u9", "account_id": {"iban": COMPANY}},
                        ],
                    },
                )
            ],
            ("GET", "/accounts/u1/transactions"): [
                (200, {"transactions": [tx("r1", 2000, "CRDT", "2026-10-02", "BH BV", COMPANY)]})
            ],
            ("GET", "/accounts/u1/balances"): [(200, {"balances": []})],
        }
        http = FakeHTTP(routes)
        real_init = EnableBankingClient.__init__

        def fake_init(self, app_id, key, base, session=None, timeout=30.0):
            real_init(self, app_id, key, "https://api.example", session=http)

        with tempfile.TemporaryDirectory() as d:
            env = {
                "EB_APPLICATION_ID": "app-123",
                "EB_PRIVATE_KEY": PEM,
                "BANKFEED_DATA_DIR": d,
                "BANKFEED_ALLOWED_IBANS": OWN,
                "BANKFEED_COMPANY_IBANS": COMPANY,
            }
            with mock.patch.dict(os.environ, env, clear=False), mock.patch.object(
                EnableBankingClient, "__init__", fake_init
            ):
                self.assertEqual(cli.main(["link", "--bank", "kbc"]), 0)
                st = next(iter(LocalStore(Path(d)).load_state()["pending"]))
                self.assertEqual(cli.main(["complete", "--url", f"https://enablebanking.com/?code=c1&state={st}"]), 0)
                accounts = LocalStore(Path(d)).load_state()["sessions"]
                self.assertEqual([a["uid"] for a in accounts], ["u1"])  # vennootschapsrekening geweigerd
                self.assertEqual(cli.main(["sync"]), 0)
                out = Path(d) / "sig.md"
                self.assertEqual(cli.main(["signals", "--month", "2026-10", "--out", str(out)]), 0)
                self.assertIn("BH BV", out.read_text())
        auth_body = [c for c in http.calls if c["path"] == "/auth"][0]["json"]
        self.assertEqual(auth_body["aspsp"]["name"], "KBC")


class SignalTests(unittest.TestCase):
    def test_signals(self):
        rows = [
            to_row("KBC …3333", tx("1", 2000, "CRDT", "2026-10-02", "BH BV", COMPANY)),
            to_row("KBC …3333", tx("2", 6000, "DBIT", "2026-10-03", "Garage", "BE00000000000003")),
            to_row("KBC …3333", tx("3", 300, "DBIT", "2026-10-04", "Hotel", "CH0000000000000000001")),
            to_row("KBC …3333", tx("4", 9000, "DBIT", "2026-10-05", "Eigen", OWN2)),
            to_row("KBC …3333", tx("5", 50, "DBIT", "2026-09-30", "Vorige maand")),
        ]
        accounts = [
            {"label": "KBC …3333", "iban": OWN, "valid_until": "2026-10-20T00:00:00+00:00"},
            {"label": "ING …7777", "iban": OWN2, "valid_until": "2027-03-01T00:00:00+00:00"},
        ]
        sig = build_signals(rows, accounts, "2026-10", [COMPANY], 5000, today=date(2026, 10, 11))
        self.assertEqual([r["counterparty"] for r in sig["rc_transfers"]], ["BH BV"])
        self.assertEqual([r["counterparty"] for r in sig["large_outflows"]], ["Garage"])
        self.assertEqual([r["counterparty"] for r in sig["foreign_counterparties"]], ["Hotel"])
        self.assertEqual(sig["per_account"]["KBC …3333"]["net"], "-13300")
        self.assertIn("ING …7777", sig["stale_accounts"])
        md = render_markdown(sig)
        self.assertIn("vernieuwen", md)
        self.assertNotIn(COMPANY, md)  # IBAN's gemaskeerd


if __name__ == "__main__":
    unittest.main()

"""CLI: python -m bankfeed <commando>

  banks     [--country BE]                 ondersteunde banken (privé)
  link      --bank NAAM [--country BE]     start consent, toont de URL voor Bart
  complete  --url REDIRECT_URL | --code C  rondt consent af, registreert de rekeningen
  sync      [--days 14]                    haalt transacties en saldi op (dagelijks)
  status                                   rekeningen en vervaldata van consent
  signals   --month YYYY-MM [--out F]      maandsignaal (markdown) voor Lex en Vesta
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from urllib.parse import parse_qs, urlparse

from .client import EnableBankingClient
from .config import Config, ConfigError
from .signals import build_signals, mask, render_markdown
from .store import LocalStore
from .sync import accounts_from_session, consent_warnings, filter_allowed, merge_accounts, run_sync


def _client(cfg: Config) -> EnableBankingClient:
    return EnableBankingClient(cfg.application_id, cfg.private_key_pem, cfg.api_base)


def _sheet(cfg: Config):
    if cfg.sheet_id and cfg.google_service_account_json:
        from .sheets import SheetSink

        return SheetSink(cfg.sheet_id, cfg.google_service_account_json)
    return None


def _load_accounts(store: LocalStore, sheet) -> list[dict]:
    accounts = store.load_state().get("sessions", [])
    if not accounts and sheet is not None:
        accounts = sheet.load_accounts()
    return accounts


def cmd_banks(cfg: Config, args) -> int:
    for a in _client(cfg).list_aspsps(args.country):
        days = int(a.get("maximum_consent_validity", 0) or 0) // 86400
        print(f"{a['name']}\t(max consent {days or '?'} dagen)")
    return 0


def cmd_link(cfg: Config, args) -> int:
    client = _client(cfg)
    days = args.days
    for a in client.list_aspsps(args.country):
        if a["name"].lower() == args.bank.lower():
            max_days = int(a.get("maximum_consent_validity", 0) or 0) // 86400
            if max_days:
                days = min(days, max_days)
            bank = a["name"]
            break
    else:
        print(f"Bank '{args.bank}' niet gevonden. Gebruik 'banks' voor de lijst.", file=sys.stderr)
        return 2
    auth = client.start_authorization(bank, args.country, cfg.redirect_url, valid_days=days)
    store = LocalStore(cfg.data_dir)
    state = store.load_state()
    state.setdefault("pending", {})[auth["state"]] = {"bank": bank, "country": args.country}
    store.save_state(state)
    print(f"Consent voor {bank}, {days} dagen, enkel leestoegang.")
    print("Bart: open deze link, log in bij de bank en kopieer daarna de volledige URL waarop je terechtkomt:")
    print(auth["url"])
    print(f"\nPending state: {auth['state']}")
    return 0


def cmd_complete(cfg: Config, args) -> int:
    store = LocalStore(cfg.data_dir)
    state = store.load_state()
    code, st = args.code, args.state
    if args.url:
        q = parse_qs(urlparse(args.url).query)
        if "error" in q:
            print(f"Bank meldt fout: {q['error'][0]}", file=sys.stderr)
            return 2
        code, st = q.get("code", [None])[0], q.get("state", [None])[0]
    if not code:
        print("Geen code gevonden.", file=sys.stderr)
        return 2
    pending = state.get("pending", {})
    if st in pending:
        meta = pending.pop(st)
    elif args.bank:  # link en complete in verschillende (tijdelijke) containers
        meta = {"bank": args.bank, "country": args.country}
    elif len(pending) == 1:
        meta = pending.pop(next(iter(pending)))
    else:
        print("Onbekende state; geef --bank mee of start opnieuw met 'link'.", file=sys.stderr)
        return 2
    client = _client(cfg)
    session = client.create_session(code)
    found = accounts_from_session(client, session, meta["bank"], meta["country"])
    new, rejected = filter_allowed(found, cfg.allowed_ibans, cfg.company_ibans)
    for a in rejected:
        print(f"Geweigerd (niet in BANKFEED_ALLOWED_IBANS of vennootschapsrekening): {a['label']} ({mask(a['iban'])})")
    if not new:
        print("Geen toegelaten rekeningen in deze consent; niets geregistreerd.", file=sys.stderr)
        store.save_state(state)
        return 2
    sheet = _sheet(cfg)
    accounts = merge_accounts(_load_accounts(store, sheet), new)
    state["sessions"] = accounts
    store.save_state(state)
    if sheet is not None:
        sheet.save_accounts(accounts)
    for a in new:
        print(f"Gekoppeld: {a['label']} ({mask(a['iban'])}) — consent tot {a['valid_until']}")
    return 0


def cmd_sync(cfg: Config, args) -> int:
    store = LocalStore(cfg.data_dir)
    sheet = _sheet(cfg)
    accounts = _load_accounts(store, sheet)
    if not accounts:
        print("Nog geen gekoppelde rekeningen. Gebruik eerst 'link' en 'complete'.", file=sys.stderr)
        return 2
    sinks = [store] + ([sheet] if sheet is not None else [])
    summary = run_sync(_client(cfg), accounts, sinks, days=args.days)
    summary["consent_warnings"] = consent_warnings(accounts)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if all(a["status"] == "ok" for a in summary["accounts"]) else 1


def cmd_status(cfg: Config, args) -> int:
    store = LocalStore(cfg.data_dir)
    accounts = _load_accounts(store, _sheet(cfg))
    for a in accounts:
        print(f"{a['label']}\t{a['bank']}\t{mask(a.get('iban', ''))}\tconsent tot {a.get('valid_until', '?')}")
    for w in consent_warnings(accounts):
        print(f"⚠️ {w}")
    return 0


def cmd_signals(cfg: Config, args) -> int:
    store = LocalStore(cfg.data_dir)
    sheet = _sheet(cfg)
    rows = store.read_transactions()
    if not rows and sheet is not None:
        rows = sheet.read_transactions()
    sig = build_signals(
        rows,
        _load_accounts(store, sheet),
        args.month,
        cfg.company_ibans,
        cfg.large_outflow_threshold,
    )
    md = render_markdown(sig)
    if args.out:
        with open(args.out, "w") as f:
            f.write(md)
    else:
        print(md)
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="bankfeed", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("banks")
    b.add_argument("--country", default="BE")
    l = sub.add_parser("link")
    l.add_argument("--bank", required=True)
    l.add_argument("--country", default="BE")
    l.add_argument("--days", type=int, default=180)
    c = sub.add_parser("complete")
    c.add_argument("--url")
    c.add_argument("--code")
    c.add_argument("--state")
    c.add_argument("--bank")
    c.add_argument("--country", default="BE")
    s = sub.add_parser("sync")
    s.add_argument("--days", type=int, default=14)
    sub.add_parser("status")
    g = sub.add_parser("signals")
    g.add_argument("--month", default=date.today().strftime("%Y-%m"))
    g.add_argument("--out")
    args = p.parse_args(argv)

    needs_bank = args.cmd in {"banks", "link", "complete", "sync"}
    try:
        cfg = Config.from_env(require_bank=needs_bank)
    except ConfigError as e:
        print(f"Configuratie: {e}", file=sys.stderr)
        return 2
    handler = {
        "banks": cmd_banks,
        "link": cmd_link,
        "complete": cmd_complete,
        "sync": cmd_sync,
        "status": cmd_status,
        "signals": cmd_signals,
    }[args.cmd]
    return handler(cfg, args)


if __name__ == "__main__":
    sys.exit(main())

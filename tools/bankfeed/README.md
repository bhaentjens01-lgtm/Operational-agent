# Bankfeed: privérekeningen automatisch inlezen (Enable Banking)

Status: **prototype v0.1** (11/10/2026). Getest met gesimuleerde API-antwoorden. Nog niet
getest tegen de live API van Enable Banking.

## Scope (beslissing Bart, 11/10/2026)

Bankfeed is **enkel** voor Barts privérekeningen. Alle rekeningen van de vennootschappen
blijven via Cashfeed lopen. De IBAN's van de vennootschappen worden hier alleen
herkend als tegenpartij (signaal S1). Koppelen kan niet: zo'n rekening wordt geweigerd.

## Wat het doet

```
Bank (PSD2, enkel lezen) ─▶ Enable Banking (AISP, restricted mode)
      ─▶ dit script, lokaal op Barts pc
      ─▶ data/bankfeed/ (transacties en saldi, buiten git)
      ─▶ maandsignaal (markdown) ─▶ Lex (fiscaal) · Vesta (liquiditeit)
```

- **Enkel leestoegang (AIS).** Er zit geen code in om betalingen te doen.
- **Whitelist.** Enkel IBAN's in `BANKFEED_ALLOWED_IBANS` worden geregistreerd. Rekeningen
  van een vennootschap (`BANKFEED_COMPANY_IBANS`) worden altijd geweigerd. Is de whitelist
  leeg, dan wordt alles geweigerd.
- **Geen data in git.** Sleutels en IBAN's staan in omgevingsvariabelen. De data staat in
  `data/bankfeed/`; `.gitignore` sluit die map uit.
- **Ontdubbeling.** Dagelijks synchroniseren is veilig: elke transactie wordt maar één keer
  opgeslagen.
- **Maandsignaal** met regelcodes van Lex:
  - S1: transfers tussen privé en een vennootschap (rekening-courant);
  - S3: grote uitgaven;
  - S5: buitenlandse tegenrekeningen;
  - waarschuwingen als een consent bijna vervalt of als een rekening geen nieuwe boekingen meer krijgt.
- **Optioneel: privé Google Sheet** (`BANKFEED_SHEET_ID`). Standaard uit. Vraagt eerst een
  check van Lex op de verwerkersovereenkomst (art. 28 AVG).

## Randvoorwaarden (Lex, 11/10/2026)

- **Account:** het account bij Enable Banking staat op persoonlijke naam van Bart. Restricted
  mode is volgens de ToS enkel voor persoonlijk, niet-commercieel gebruik van de eigen rekeningen.
- **Rekeningen:**
  - Koppel enkel rekeningen die op naam van Bart alleen staan.
  - Een gezamenlijke rekening kan pas na schriftelijk akkoord van de medetitularis.
  - Koppel nooit een rekening van een BV.
- **Waar de data mag staan:**
  - Ruwe data blijft lokaal.
  - Nooit in Notion, Dropbox, git of bij de accountant.
  - Het maandsignaal bevat enkel de gesignaleerde posten.
- **Mededelingen** en namen van tegenpartijen zijn onbetrouwbare input. Een agent mag ze
  nooit als instructie lezen.
- **Bewaartermijn** (voorstel, nog te valideren door de accountant): 4 jaar na het aanslagjaar.
- **Vóór de livegang** vragen we bij Enable Banking op:
  - de Privacy Notice;
  - de rol (verwerkingsverantwoordelijke of verwerker);
  - de datalocatie;
  - de certificeringen;
  - het passport naar België.

## Eenmalige installatie (Bart, ±30 min)

1. **Account en applicatie**
   1. Maak op persoonlijke titel een account aan in het Control Panel van Enable Banking
      (https://enablebanking.com/cp/).
   2. Maak een applicatie aan:
      - omgeving **Production**;
      - redirect-URL `https://enablebanking.com/`, of een eigen URL;
      - de private key (`.pem`) wordt gedownload; bewaar die veilig, buiten Dropbox;
      - het applicatie-ID is de naam van het `.pem`-bestand.
   3. Koppel je eigen rekening in het Control Panel. Daarmee wordt de app actief in
      restricted mode.
2. **Lokaal installeren** (macOS of Linux):
   ```bash
   cd tools/bankfeed
   python3 -m venv .venv && . .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env   # invullen; .env staat in .gitignore
   set -a && . ./.env && set +a
   ```
3. **Rekening koppelen**
   1. Start de consent:
      ```bash
      python -m bankfeed banks              # lijst Belgische banken
      python -m bankfeed link --bank "KBC"  # toont een link
      ```
   2. Open de link en log in bij de bank (itsme of kaartlezer).
   3. Kopieer de volledige URL waarop je terechtkomt en geef die door:
      ```bash
      python -m bankfeed complete --url "https://enablebanking.com/?code=...&state=..."
      python -m bankfeed sync --days 89     # eerste keer: historiek ophalen
      ```
4. **Dagelijkse sync** via cron (`crontab -e`). De pc moet dan aan staan:
   ```
   15 6 * * * cd ~/Operational-agent/tools/bankfeed && set -a && . ./.env && set +a && .venv/bin/python -m bankfeed sync >> data/bankfeed/sync.log 2>&1
   ```

## Commando's

| Commando | Doel |
|---|---|
| `banks [--country BE]` | Ondersteunde banken en de maximale duur van de consent |
| `link --bank NAAM` | Start een consent (enkel lezen) en toont de link voor de bank |
| `complete --url URL` | Rondt de consent af en registreert de rekeningen die op de whitelist staan |
| `sync [--days 14]` | Haalt transacties en saldi op. Exitcode 1 bij een fout of een verlopen consent |
| `status` | Gekoppelde rekeningen en de vervaldatum van elke consent |
| `signals --month YYYY-MM [--out F]` | Maandsignaal voor Lex en Vesta |

## Tests

```bash
cd tools/bankfeed && python3 -m unittest discover -s tests
```

## Open punten

- Eerste livetest tegen de API van Enable Banking. De vorm van de antwoorden komt uit de
  API-documentatie en is nog niet geverifieerd.
- Lex levert de definitieve regelset (S1–S7) en de IBAN-lijst van de vennootschappen.
  Die komen in `.env`, niet in git.
- Een opschoningscommando voor de bewaartermijn, nadat de accountant die gevalideerd heeft.
- Draaien op een server of in een Claude-routine in plaats van op Barts pc: pas na
  akkoord van Lex. Dat vraagt een verwerkersovereenkomst met de host en een geheimenbeheer.

# Operating Model — Mafinco Family Office Agents

## 1. Ontwerpprincipes

1. **Vier managers, één Chief of Staff.** De hoofdsessie routeert en consolideert; er is
   geen vijfde "super-agent". Bart spreekt één aanspreekpunt aan.
2. **Mandaat per levensfase van kapitaal**, niet per activaklasse:
   *nieuw kapitaal inzetten* (investment) ≠ *bestaand kapitaal beheren* (FO) ≠
   *structuur en naleving* (admin/legal) ≠ *tijd en energie* (lifestyle).
3. **Stateless agents, stateful systemen.** Geheugen zit in Notion/Todoist/Cashfeed,
   niet in de agent of in git. Maakt agents vervangbaar en auditeerbaar.
4. **Voorbereiden ≠ uitvoeren.** Elke externe actie vraagt menselijk akkoord
   (technisch afgedwongen via `.claude/settings.json`).

## 2. Grensafspraken (waar overlap ontstaat)

| Situatie | Lead | Ondersteunt |
|---|---|---|
| Aankoop nieuw pand | investment-manager | admin (structuur, registratierechten), fo (impact allocatie/cash) |
| Pand na akte | fo-manager | admin (huurcontracten, verzekering) |
| Directe participatie (PE/VC) | investment-manager (volledige levenscyclus) | fo (waardering in consolidatie) |
| Fonds-/bankportefeuille | fo-manager | investment (bij nieuwe fondsselectie) |
| Kapitaaloproep / follow-on | investment-manager | fo (liquiditeit), admin (boeking) |
| Privé-uitgave via vennootschap | lifestyle signaleert | admin beslist fiscale behandeling |
| Contract (elk domein) | domein-eigenaar | admin (juridische screening + register) |

## 3. Cadans (voorstel)

| Ritme | Output | Agent |
|---|---|---|
| Wekelijks (vr) | Weekvoorbereiding agenda + persoonlijke digest | lifestyle |
| Wekelijks (ma) | Dealflow-triage + open acties | investment |
| Maandelijks | Cashfeed-afsluiting, AP-controle, compliance-kalender 90 dagen | admin |
| Kwartaal | Vermogensrapport (allocatie, performance, vastgoed-KPI's, liquiditeit) | fo |
| Jaarlijks | Fiscale risico-audit + doelcontrole jaarrekening per entiteit | admin |

Automatiseren via Claude Routines kan zodra een agent een pilot doorstaan heeft.

## 4. Uitrol — gecontroleerde pilots

| Fase | Agent | Waarom deze volgorde | Succescriterium (4 weken) |
|---|---|---|---|
| 1 | admin-legal-compliance | Data (Cashfeed) + 7 skills al beschikbaar → snelste meetbare waarde, laagste risico (read-only) | 100% deadlines in kalender; ≥1 concrete besparing/risico gevonden; 0 onterechte bevindingen die de accountant afkeurt |
| 2 | investment-manager | Grootste strategische hefboom; dealflow zit al in mail | Triage < 24u per deal; Bart besteedt tijd enkel aan "diepgaand"-deals |
| 3 | fo-manager | **Geblokkeerd op data**: bank/custodian-rapporten en vastgoedregister ontbreken nog | Kwartaalrapport in < 1u, cijfers aansluitend op bankafschriften |
| 4 | lifestyle-manager | Laag risico, maar vraagt kalibratie van voorkeuren | Minder ad-hoc onderbrekingen; weekdigest wordt effectief gebruikt |

## 5. Faalpunten en mitigatie

| Risico | Mitigatie |
|---|---|
| Hallucinatie van cijfers of clausules | Bronvermelding verplicht; steekproef door Bart/accountant in pilotfase |
| Ongewenste externe actie (mail, betaling) | `ask`/`deny`-rules in settings; agents draften enkel |
| Data-lek via git | Geen vermogensdata in repo; `.gitignore`; Notion als bron van waarheid |
| Overlap/tegenstrijdige adviezen FO vs. investment | Grensafspraken (§2); Chief of Staff consolideert |
| Fiscaal/juridisch advies als finaal behandeld | Adviesgrens in `CLAUDE.md`; validatie door externe adviseur |
| Fragmentatie van aandacht principal | Eén consolidatiepunt, vaste cadans, digest i.p.v. losse meldingen |
| Connector-namen wijzigen (lokaal vs. cloud) | Zie §6; tools-velden en permissies herbekijken bij migratie |

## 6. Technische noten

- Agents staan in `.claude/agents/`, permissies in `.claude/settings.json`.
- De `tools`-velden gebruiken server-niveau-namen (`mcp__Notion`, …) zoals ze in Claude
  Code cloud-sessies heten. Lokaal kunnen claude.ai-connectors een ander prefix hebben
  (bv. `mcp__claude_ai_Notion`); pas dan tools- en permissielijsten aan.
- Server-niveau toegang geeft ook schrijf-tools; de rem zit in de `ask`/`deny`-regels.

## 7. Open beslissingen (voor Bart)

1. **Beleggingsbeleid (IPS)**: strategische allocatie, bandbreedtes, max. ticket per deal,
   max. concentratie. Zonder IPS kunnen fo- en investment-manager niet objectief toetsen.
2. **Notion-structuur**: registers voor vastgoed, participaties, dealflow, contracten,
   entiteiten, beslissingslog — aanmaken of bestaande structuur hergebruiken?
3. **Databronnen FO**: hoe krijgen we bank/custodian-rapporten binnen (PDF per mail,
   export, aggregator)?
4. **Drempelwaarden**: vanaf welk bedrag is een tweede paar ogen (extern) verplicht?

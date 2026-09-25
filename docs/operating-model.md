# Operating Model — Mafinco Family Office Agents

## 1. Ontwerpprincipes

1. **Vier managers, één Chief of Staff.** De hoofdsessie routeert, consolideert en bewaakt
   het systeem; er is geen vijfde "super-agent". Bart spreekt één aanspreekpunt aan.
   Mandaat: `docs/governance/chief-of-staff.md`.
2. **Mandaat per levensfase van kapitaal**, niet per activaklasse:
   *nieuw kapitaal inzetten* (investment) ≠ *bestaand kapitaal beheren* (FO) ≠
   *structuur en naleving* (admin/legal) ≠ *tijd en energie* (lifestyle).
3. **Stateless agents, stateful systemen.** Geheugen zit in Notion/Todoist/Cashfeed,
   niet in de agent of in git. Maakt agents vervangbaar en auditeerbaar.
4. **Voorbereiden ≠ uitvoeren.** Elke externe actie vraagt menselijk akkoord
   (technisch afgedwongen via `.claude/settings.json`).
5. **Flows ≠ inhoud.** Bman (buiten deze repo) is eigenaar van de dagelijkse flows:
   agenda, mailtriage, Todoist-hygiëne, routines, briefings. De managers leveren inhoud.
   De CoS bewaakt beide, maar neemt geen van beide over.

## 2. Grensafspraken (waar overlap ontstaat)

| Situatie | Lead | Ondersteunt |
|---|---|---|
| Aankoop nieuw pand | investment-manager | admin (structuur, registratierechten), fo (impact allocatie/cash) |
| Pand na akte | fo-manager | admin (huurcontracten, verzekering) |
| Directe participatie / angel | investment-manager (volledige levenscyclus) | fo (waardering in consolidatie) |
| Bestaande PE-fondsverbintenis (capital calls, NAV, distributies) | fo-manager | admin (boeking) |
| Nieuwe fondsverbintenis / follow-on-beslissing | investment-manager | fo (liquiditeitsimpact) |
| Private-banking-mandaten | fo-manager | — |
| Privé-uitgave via vennootschap | lifestyle signaleert | admin beslist fiscale behandeling |
| Contract (elk domein) | domein-eigenaar | admin (juridische screening + register) |
| Agenda, mailtriage, Todoist-hygiëne, briefings | Bman | managers en CoS lezen; tijdsloten aanvragen via taak |
| Fund-mails (capital calls, NAV, distributies) | fo-manager | Bman leidt door, interpreteert niets |
| Reis, event, geschenk, gezondheidsafspraak (inhoud) | lifestyle-manager | Bman plant in |
| Weekplanning en systeemcheck (vrijdag) | CoS (Planning Manager + Systeemwachter) | Bman levert agenda- en taakstatus |

## 3. Communicatie en overdracht

**Principe:** agents praten niet rechtstreeks met elkaar. Er zijn drie kanalen:

| Kanaal | Wanneer | Hoe |
|---|---|---|
| **CoS in dezelfde sessie** | Vraag die meerdere domeinen raakt | De CoS start de managers en geeft de output van de ene mee in de opdracht aan de andere |
| **Todoist-taak** | Overdracht tussen sessies, naar of van Bman, escalaties | Volgens het protocol hieronder |
| **Notion-registers** | Gedeelde feiten (panden, funds, dealflow, beslissingslog) | Eén eigenaar per register; de andere agents lezen alleen |

Technische grens: een subagent kan geen andere subagent starten, en Bman draait buiten
deze repo. Todoist is dus de enige wachtrij tussen sessies en platformen.

**Overdrachtsprotocol (Todoist-taak):**

| Veld | Inhoud |
|---|---|
| Titel | `[van → naar] onderwerp`, bv. `[fo → admin] capital call boeken` |
| Deadline | Verplicht; bij escalaties volgens AOR §3 |
| Duur | Verplicht (addendum 18/09; standaard 15 min) |
| Beschrijving | Bron-link (Notion, Dropbox, mail), de vraag, wie beslist (entiteit, orgaan) |
| Label | Eigenaar-agent (labels aan te maken na akkoord: `agent-fo`, `agent-invest`, `agent-admin`, `agent-lifestyle`, `agent-cos`, `bman`) |
| Project | 04 Monitor voor escalaties; anders het project van de ontvanger |

De ontvanger past de inhoud van de taak niet aan. Hij voert uit of geeft terug via een
commentaar. Bman plant taken in en toont ze in de briefing, maar interpreteert ze niet.

## 4. Cadans (voorstel)

| Ritme | Output | Agent |
|---|---|---|
| Dagelijks | Ochtend- en avondbriefing, mailtriage, Waiting For | Bman |
| Wekelijks (vr 06:00) | Systeemcheck + weekplanning → één rapport en één beslislijst | CoS |
| Wekelijks (ma) | Dealflow-triage + open acties | investment |
| Maandelijks | Cashfeed-afsluiting, AP-controle, compliance-kalender 90 dagen | admin |
| Maandelijks | Exception reports samenvoegen tot één beslislijst | CoS |
| Kwartaal | Vermogensrapport (allocatie, performance, vastgoed-KPI's, liquiditeit) | fo |
| Jaarlijks | Fiscale risico-audit + doelcontrole jaarrekening per entiteit | admin |

Automatiseren via Claude Routines kan zodra een agent een pilot doorstaan heeft.

## 5. Uitrol — gecontroleerde pilots

| Fase | Agent | Waarom deze volgorde | Succescriterium (4 weken) |
|---|---|---|---|
| 1 | admin-legal-compliance | Data (Cashfeed) + 7 skills al beschikbaar → snelste meetbare waarde, laagste risico (read-only) | 100% deadlines in kalender; ≥1 concrete besparing/risico gevonden; 0 onterechte bevindingen die de accountant afkeurt |
| 2 | investment-manager | Grootste strategische hefboom; dealflow zit al in mail | Triage < 24u per deal; Bart besteedt tijd enkel aan "diepgaand"-deals |
| 3 | fo-manager | Registers en rapporten bestaan (Notion + Dropbox), maar er zijn dubbele bronnen en geen goedgekeurd beleid → eerst opschonen (zie governance §8) | Kwartaalrapport per 30/09 sluit aan op bankafschriften |
| 4 | lifestyle-manager | Laag risico, maar vraagt kalibratie van voorkeuren | Minder ad-hoc onderbrekingen; weekdigest wordt effectief gebruikt |
| — | Chief of Staff | Pilot vr 02/10/2026 (vrijdagsessie, tijdens de Bman-overname) | Eén rapport en één beslislijst; Bart < 30 min; geen onopgeloste tegenstrijdigheden |

## 6. Faalpunten en mitigatie

| Risico | Mitigatie |
|---|---|
| Hallucinatie van cijfers of clausules | Bronvermelding verplicht; steekproef door Bart/accountant in pilotfase |
| Ongewenste externe actie (mail, betaling) | `ask`/`deny`-rules in settings; agents draften enkel |
| Data-lek via git | Geen vermogensdata in repo; `.gitignore`; Notion als bron van waarheid |
| Overlap/tegenstrijdige adviezen FO vs. investment | Grensafspraken (§2); Chief of Staff toont het conflict met aanbeveling |
| Twee agents in dezelfde flow (bv. agenda) | Eén eigenaar per flow (AOR §4); de rest leest of vraagt aan via taak |
| Overdracht gaat verloren tussen sessies of platformen | Todoist als enige wachtrij, vast taakformaat (§3) |
| CoS groeit uit tot super-agent | Geen inhoudelijk werk zonder manager; kwartaalreview (governance CoS §7) |
| Bman-instructies op meerdere plekken (Project, routines, Notion) | Enkel de Notion-skill is bron; de rest verwijst ernaar (Documentsync) |
| Fiscaal/juridisch advies als finaal behandeld | Adviesgrens in `CLAUDE.md`; validatie door externe adviseur |
| Fragmentatie van aandacht principal | Eén consolidatiepunt, vaste cadans, digest i.p.v. losse meldingen |
| Connector-namen wijzigen (lokaal vs. cloud) | Zie §6; tools-velden en permissies herbekijken bij migratie |

## 7. Technische noten

- Agents staan in `.claude/agents/`, permissies in `.claude/settings.json`.
- De `tools`-velden gebruiken server-niveau-namen (`mcp__Notion`, …) zoals ze in Claude
  Code cloud-sessies heten. Lokaal kunnen claude.ai-connectors een ander prefix hebben
  (bv. `mcp__claude_ai_Notion`); pas dan tools- en permissielijsten aan.
- Server-niveau toegang geeft ook schrijf-tools; de rem zit in de `ask`/`deny`-regels.

## 8. Governance per agent

- Chief of Staff: `docs/governance/chief-of-staff.md` (v1.0, akkoord 25/09)
- `fo-manager`: `docs/governance/fo-manager.md` (voorstel v0.1)

## 9. Open beslissingen (voor Bart)

1. **Beleggingsbeleid (IPS)**: strategische allocatie, bandbreedtes, max. ticket per deal,
   max. concentratie. Zonder IPS kunnen fo- en investment-manager niet objectief toetsen.
2. **Notion-structuur**: registers voor vastgoed, participaties, dealflow, contracten,
   entiteiten, beslissingslog — aanmaken of bestaande structuur hergebruiken?
3. **Databronnen FO**: hoe krijgen we bank/custodian-rapporten binnen (PDF per mail,
   export, aggregator)?
4. **Drempelwaarden**: vanaf welk bedrag is een tweede paar ogen (extern) verplicht?
5. **Bman na 04/10**: terug naar Manus, of definitief bij Claude? Slotcheck 29/09.
6. **Onafhankelijke controleur** (Q4): een model van een andere leverancier dat zonder
   schrijfrechten het kwartaalrapport en de beslissingslog naleest (governance CoS §8).

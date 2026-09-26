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
| Directe participatie / angel: tot signing | investment-manager | admin (structuur, NDA) |
| Directe participatie / angel: na signing | fo-manager (KPI's, waardering, exit, bestuursmandaat) | investment (IC-memo bij follow-on) |
| Bestuursmandaat zonder participatie van Mafinco | consulting-manager | Bman (agenda) |
| Wealth planning en asset allocation | fo-manager | admin (successie, structuur) |
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

Status: beslist door Bart op 25/09 (G1–G4).

**Principe:** agents praten niet rechtstreeks met elkaar of met Bman. Er zijn vier kanalen:

| Kanaal | Wanneer | Hoe |
|---|---|---|
| **CoS in dezelfde sessie** | Vraag die meerdere domeinen raakt | De CoS start de managers en geeft de output van de ene mee in de opdracht aan de andere |
| **Register "Delegaties & overdrachten"** (Notion) | Werk voor een agent of een persoon; overdracht tussen sessies en agents | Eén item per opdracht, met statusflow (hieronder). Dit is de wachtrij tussen sessies |
| **Todoist** | Wat Bart zelf moet doen (fysiek of juridisch), of nazicht door Bart | Labels en titelcode (hieronder) |
| **Notion-registers** | Gedeelde feiten (panden, funds, dealflow, beslissingslog) | Eén eigenaar per register; de andere agents lezen alleen |

Beslissingen en goedkeuringen komen op de beslislijst (briefing of vrijdagrapport), nooit
in Todoist.

Technische grens: een subagent kan geen andere subagent starten, en Bman draait buiten
deze repo. Het register is dus de wachtrij tussen sessies en platformen.

**Aanpak eerst (gate).** Een agent begint pas aan een opdracht nadat Bart de aanpak heeft
goedgekeurd. Statusflow in het register:

`Nieuw → Aanpak voorgesteld → Aanpak goedgekeurd → Bezig → Naar Bart → Klaar`
(zijsporen: `Wachten`, `Geannuleerd`)

| Veld | Inhoud |
|---|---|
| Aanpak | Het voorstel van de agent: doel, stappen, bronnen, wat Bart terugkrijgt |
| Feedback Bart | Letterlijk Barts antwoord ("ok", bijsturing of "bespreken") |
| Staande aanpak | Bij terugkerende taken: eenmaal goedgekeurd, dan geldt de aanpak voor elke volgende keer (G4) |
| Nazichttijd (min) | Geschatte tijd die Bart nodig heeft om het resultaat na te kijken |

**Intern uitvoeren = melden.** Voert een agent binnen een goedgekeurde aanpak interne stappen
uit in zijn eigen registers, dan gaat het item naar *Klaar* met het resultaat, en verschijnt het in
de briefing onder "Ter info — intern uitgevoerd". Bart hoeft niets te doen, maar kan
"terugdraaien" of "bespreken" zeggen.

**Hoe Bart de aanpakken ziet.** De CoS draait op werkdagen om 07:26, 11:56 en 16:56 een
ronde over het register en schrijft het resultaat op de pagina "Agent-dagronde — status".
Bman toont die in de briefings van 08:15, 12:30 en 18:00, onder "Aanpakken ter goedkeuring" en
"Resultaten ter nazicht". Bart antwoordt met een ID (`DEL-12 ok`), en Bman schrijft dat antwoord
in het register. De rondes worden afgebouwd als het kan; evaluatie na 4 weken.

**Todoist-conventie voor taken die een agent voorbereidt.** De taak blijft in Todoist staan,
zodat Bart het overzicht behoudt:

| Element | Inhoud |
|---|---|
| Titelcode | `[eigenaar]` vooraan, bv. `[fo]`, `[admin]`, `[consult]`, `[naam]` |
| Verwijzing | Link naar het register-item (bv. `DEL-12`) in de beschrijving; geldt ook voor taken die personen uitvoeren |
| Label | `bij-agent` = de agent is aan zet; `nazicht` = Bart is aan zet |
| Duur | Barts nazichttijd, niet de uitvoeringstijd (standaard 15 min) |
| Filters | "Mijn werk" (zonder `bij-agent`) en "Bij agents" |

Prioriteit: nieuwe taken krijgen P4. Een taak die verder dan 14 dagen ligt of geen datum heeft,
blijft P4. Een hogere prioriteit kan alleen binnen 14 dagen en wordt op vrijdag gezet.

**Delegatie aan personen** (medebeheerders, familie) loopt ook via het register. Wie welke
rol heeft en wat die persoon wel of niet kan doen, staat in Notion, niet in deze repo.

## 4. Cadans (voorstel)

| Ritme | Output | Agent |
|---|---|---|
| Dagelijks | Ochtend- en avondbriefing, mailtriage, Waiting For | Bman |
| Werkdagen 07:26 · 11:56 · 16:56 | Agent-dagronde over het register → statuspagina voor de briefings | CoS |
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
| Overdracht gaat verloren tussen sessies of platformen | Register "Delegaties & overdrachten" als wachtrij; de taak blijft zichtbaar in Todoist met titelcode, label en verwijzing naar het register-item (§3) |
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
5. **Bman**: blijft bij Claude tenzij Bart uiterlijk 04/10 anders beslist (Manus of ChatGPT).
6. **Onafhankelijke controleur** (Q4): een model van een andere leverancier dat zonder
   schrijfrechten het kwartaalrapport en de beslissingslog naleest (governance CoS §8).

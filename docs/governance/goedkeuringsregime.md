# Governance — Goedkeuringsregime (ontlasting van de principal)

Status: **PILOT v0.1 — akkoord Bart 08/10/2026, regel per regel herbevestigd 13/10 (chat, Atlas).** Start ma 12/10/2026, na de
bouwstop van 09/10. Evaluatie na 4 weken (vr 06/11/2026). Notion-spiegel: pagina
"Goedkeuringsregime — pilot" onder Delegaties & overdrachten. Bij conflict gaan de
**🤖 Agent Operating Rules** in Notion voor. Dit document bevat regels, geen vermogensdata.

---

## 1. Waarom

Meting 08/10 (register "Delegaties & overdrachten", peildatum 12:47):

| Status | Items | Geschatte nazichttijd |
|---|---|---|
| Aanpak voorgesteld (wacht op Bart) | 39 | 545 min |
| Naar Bart (resultaat ter nazicht) | 15 | 121 min |
| Klaar | 17 | — |
| Overig (Nieuw, goedgekeurd, geannuleerd) | 6 | — |

54 van 77 items wachten op Bart. Nul items dragen "Staande aanpak". 73% is klasse B.
Elk item passeert Bart twee keer (aanpak én resultaat). Het systeem verzamelt dus werk
voor de principal in plaats van het weg te nemen. De vier regels hieronder veranderen het
goedkeuringsregime; de guardrails (geen externe actie zonder "ja", geen verwijderingen,
geen verzonnen cijfers) blijven onverkort gelden.

## 2. De vier regels

### R1 — Staande aanpak is de default voor terugkerend werk

- Een terugkerende flow krijgt **één** registeritem met vinkje *Staande aanpak*, één keer
  goedgekeurd door Bart. Daarna vraagt de agent geen aanpak-goedkeuring meer per
  voorkomen: hij voert uit en meldt enkel **resultaat of afwijking**.
- Een staande aanpak bevat: doel, trigger (wanneer draait het), stappen, bronnen, wat intern
  mag (AUTO/SUGGEST), wat altijd APPROVAL blijft, en een **vervaldatum** (standaard
  3 maanden). Na vervaldatum legt de agent ze opnieuw voor, met wat er veranderd is.
- Per agent één bundelitem `[agent → Bart] Staande aanpakken — <domein>` met alle
  voorstellen; Bart keurt per regel goed ("ok 1,2,4").
- Eerste kandidaten (bron: dagronde 08/10): huuropvolging per pand, ID- en attestdossiers
  huurders, AV-/VA3-kalender, dringende facturen (≤ 7 d of vervallen), rappel-drafts bij
  huurachterstand, maandelijkse exception reports.

### R2 — Stilte is ja, enkel voor klasse A en interne stappen

- Een item van **klasse A** (agent volledig) of een **interne stap** binnen een goedgekeurde
  of staande aanpak (registers, dossiers, drafts die niet verstuurd worden) mag na
  **3 werkdagen zonder reactie** uitgevoerd worden. Het item gaat naar *Klaar* met
  *Resultaat* en verschijnt onder "Ter info — intern uitgevoerd". Bart kan "terugdraaien"
  zeggen.
- **Klasse B** (Bart beslist) en **klasse D** (persoon) vallen hier nooit onder. Zij blijven
  wachten, maar verdwijnen uit de briefing (zie R3).
- **Nooit** onder stilte: mail, betaling, order, handtekening, inschrijving, goedkeuring in
  Cashfeed, agenda-events, communicatie met derden. Dat blijft een expliciete "ja" van Bart.

### R3 — Eén beslismoment per week, dagelijks plafond

- **Dagelijks** toont de dagronde Bart maximaal **5 items**, enkel met deadline binnen
  5 werkdagen of een overschreden escalatiedrempel. Al het andere staat niet in de briefing.
- **Vrijdag** komt alle klasse B in **één beslisblok**, gesorteerd op nazichttijd, met een
  **WIP-limiet van 10**. Wat erboven zit, parkeert de agent met *Opvolgen op* en komt pas
  terug op die datum.
- Een item zonder reactie wordt **niet herhaald** in volgende briefings. Het blijft in het
  register zichtbaar via de view "Wacht op Bart". Herhaling enkel als de deadline nadert.
- De twee dagrondes (07:26 · 16:26, beslissing Bart 13/10) blijven draaien voor de agents; Bart ziet
  per dag één lijst.

### R4 — Beslisformaat: default plus ja/nee

- Elk item dat Bart bereikt bevat **één aanbevolen keuze**, de reden in één regel, en wat
  er gebeurt bij "nee". Formulering: *"Ik doe X, tenzij je nee zegt."*
- Open vragen aan Bart zijn enkel toegestaan voor **feiten die nergens in de bronnen
  staan** (Notion, Dropbox, Cashfeed, mail), en dan gebundeld in **één regel** per item.
- Een item met meer dan één open vraag gaat terug naar de agent: eerst zelf zoeken,
  dan een default kiezen.
- Vaste velden in het register: *Vraag* = de ja/nee-vraag; *Aanpak* = de default en het
  alternatief; *Wie beslist* = Bart of een bestuursorgaan.

## 3. Klasse D — delegaties aan gezinsleden

**Voorstel, nog niet beslist** (correctie 13/10: Barts "ja" van 08/10 gold enkel de regels R1–R4). Drafts voor klussen aan Stef, Félice en Filip lopen via een **vast kanaal
per persoon** zonder goedkeuring per item, binnen een **whitelist** (type klus, max. bedrag,
locatie en timing volgens de tabel Delegatiecontacten). Het kanaal per persoon vult Bart
eenmalig in op de pagina Delegaties & overdrachten. Buiten de whitelist: APPROVAL zoals
voorheen. Verzending zelf blijft technisch een `ask` tot het kanaal in `.claude/settings.json`
expliciet is vrijgegeven (aparte beslissing).

## 4. Toegangssprint (eenmalig, vóór de pilot)

Elk toegangsgat wordt vandaag een blijvende vraag aan Bart. Eén sessie van Bart sluit ze:

| Gat | Effect vandaag | Wat Bart doet |
|---|---|---|
| Cashfeed-organisatie Immoffice17 | Würth-huur niet controleerbaar (DEL-42) | Vesta toegang geven of maandelijkse export delen |
| Google Sheet huuropvolging SK Gent | Niet leesbaar vanuit de cloud (DEL-41) | Sheet delen of bevestigen dat Cashfeed de bron is |
| Lokale skill-/pluginlijst | Inventaris niet mogelijk (DEL-9, DEL-69) | Lijst eenmalig aanleveren of lokale sessie starten |

Plus: agents mogen hun **werkpagina bijwerken** na elke opdracht (CLAUDE.md), zodat ze
geheugen opbouwen en dezelfde vragen niet opnieuw stellen. De dagronde van 08/10 verbood dit.

## 5. Meting en succescriterium

- **Hoofd-KPI:** items en minuten in Barts wachtrij (statussen *Aanpak voorgesteld* + *Naar
  Bart*), gemeten elke vrijdag door de CoS in het vrijdagrapport.
- **Nulmeting 08/10:** 54 items, 666 min.
- **Doel na 4 weken (06/11):** ≤ 10 open items, < 120 min nazicht per week, ≥ 6 staande
  aanpakken actief, 0 externe acties zonder "ja".
- **Stopregel:** een stilte-is-ja-uitvoering die Bart terugdraait wegens inhoudelijke fout →
  R2 wordt voor die agent opgeschort tot de oorzaak in de foutlog staat.

## 6. Wijzigingen elders (Documentsync)

| Waar | Wat |
|---|---|
| `docs/operating-model.md` §3 | Aanpak-gate verwijst naar dit regime (R1–R4) |
| Notion: Agent Operating Rules | Addendum 08/10 met link naar de pilotpagina |
| Notion: dagronde-skill (v1.2 → v1.3) | Stap B: plafond 5 + enkel deadline ≤ 5 d; stap C: stilte-is-ja voor klasse A na 3 werkdagen; geen herhaling van onbeantwoorde items; vrijdagblok met WIP 10; beslisformaat R4 verplicht |
| Notion: register | Views "Staande aanpakken" en "Wacht op Bart" |
| Bman-skill (Notion) | Briefing toont enkel de dagelijkse lijst van de CoS (max 5) en op vrijdag het beslisblok |

Kill switch: dit document hernoemen of de link in Agent Operating Rules verwijderen; het
regime van `docs/operating-model.md` §3 geldt dan opnieuw.

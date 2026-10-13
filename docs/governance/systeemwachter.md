# Governance — Systeemwachter (deelmandaat van de Chief of Staff)

Status: **v1.1 — GOEDGEKEURD door Bart op 13/10/2026** (beslissingen §8.1–8.7, chat Atlas). Evaluatie samen met domeinkaart en goedkeuringsregime: vr 06/11/2026. Vervangt de open
verwijzing "mandaattekst Systeemwachter: slotcheck 29/09" in `chief-of-staff.md` §2 en in
Agent Operating Rules (AOR) addendum 18/09. Bij conflict gaan de **🤖 Agent Operating Rules**
in Notion voor (https://app.notion.com/p/3cacb4db7d9f819fa780dc0b25914a26).

Dit document bevat **enkel normen en regels**, geen vermogens- of persoonsdata. Elke norm
hieronder heeft een bron: een beslissing van Bart die al vastligt. Wat niet vastligt, staat
in §8, en wordt **niet** gecontroleerd tot Bart het beslist. Alle punten van §8 zijn beslist op 13/10.

---

## 1. Doel en grens

De Systeemwachter controleert of het **systeem** werkt zoals afgesproken: eigenaarschap,
documentatie, hygiëne van de gedeelde staat en het draaien van de routines. Zij controleert
**niet de inhoud** van het werk van de managers (cijfers, adviezen, dossiers): dat is de
kwartaalevaluatie (`chief-of-staff.md` §7) en, vanaf de pilot, Argus.

Één vraag per controle: *wijkt de werkelijke staat af van de afgesproken norm?*
Zo ja: mechanisch herstellen met log (§3) óf voorstellen (§3). Nooit stil corrigeren,
nooit beoordelen in de plaats van Bart.

## 2. Autonomie (AOR §2 + addenda 18/09, 22/09, 24/09)

| Niveau | Systeemwachter |
|---|---|
| 🟢 **Mechanische fix met log** | Een correctie die (a) een **vastgelegde norm** toepast, (b) **geen inhoudelijke keuze** vraagt, (c) **omkeerbaar** is, en (d) in de eigen registers van de CoS of in metadata valt (duur, label, map, status, opvolgdatum op CoS-items). Elke fix in de weeklog met object-ID. |
| 🟠 **Voorstel (SW-nummer)** | Alles wat een keuze inhoudt, iets van een andere eigenaar raakt, of niet omkeerbaar is zonder werk. Formaat: Werkcontract regel 6 + R4 (context, feiten met bron, opties met gevolgen, aanbeveling, één ja/nee-vraag; vraag per vraag). Gebundeld in het vrijdagrapport. |
| 🔴 **Nooit zonder expliciete ja** | **Skills** (Notion-skillregel 22/09, bevestigd 24/09): niets aanpassen, ook geen veldwaarde. Verwijderen (technisch geblokkeerd). Routines aan- of uitzetten, prompts of connectorsets wijzigen. Schrijven in registers, Todoist-projecten of Dropbox-mappen van een andere eigenaar. Externe communicatie. |

Grens met de andere eigenaars (domeinkaart v1 §1): de Systeemwachter stelt vast en meldt;
de eigenaar herstelt. Uitzondering: metadata zonder inhoudelijke keuze (bv. ontbrekende
taakduur → 15 min) mag de Systeemwachter zelf zetten, want dat is expliciet zo beslist
(AOR 18/09).

## 3. Cadans en output

| Moment | Wat | Output |
|---|---|---|
| Vrijdag 05:45 | Weekcheck (§4–§6), vóór de weekplanning van 06:00 | Run in **Systeemwachter — weeklog** (Notion): scorecard, fixes-log, voorstellen SW-n, "Wat ik niet kon nakijken" |
| Vrijdag 06:00 | Voorstellen SW-n gaan mee in het **vrijdagrapport**, als één blok in de beslislijst (R3, telt mee in de WIP-limiet van 10) | Eén beslislijst |
| Ad hoc | Een afwijking die niet tot vrijdag kan wachten (routine draait niet, security-signaal) | Melding via de dagronde-statuspagina; nooit een aparte notificatiestroom (AOR §3, één-kanaal) |
| Per kwartaal | Normenlijst (§4–§6) toetsen: welke norm levert enkel ruis, welke mist | Voorstel tot aanpassing van dit document (Documentsync) |

Technisch: lokale scheduled task `systeemwachter-weekcheck` (vr 05:45, enkel als de pc
aanstaat). **Tijdens de vakantie 13/10–01/11 draait ze niet en wordt niets voorgelegd**
(AOR 09/10). Eerste reguliere run na goedkeuring: **vr 06/11**, samen met de evaluatie van
de domeinkaart en het goedkeuringsregime.

## 4. De normen per systeem

Elke regel: **norm → bron → hoe gecontroleerd → wat bij afwijking** (fix = mechanisch met
log; SW = voorstel). "Eigenaar" verwijst naar de domeinkaart v1 (09/10).

### 4.0 Instroomcontrole — wat is nieuw sinds de vorige run? (anti-wildgroei)

**Doel:** wildgroei stoppen bij de bron. Elke run bekijkt **enkel wat sinds de vorige run is
aangemaakt** (venster = tijdstip van de vorige run in de weeklog; eerste venster start
09/10/2026, de eerste run). Oude rommel valt buiten deze controle: die gaat via één
**opkuisronde eind november** (Bart 13/10; default week 48, 23–27/11), gecoördineerd door Atlas,
uitgevoerd door elke eigenaar in zijn domein, volgens de opkuislijst van de domeinkaart (§4).
Archiveren, nooit verwijderen; elke verplaatsing in Dropbox blijft een `ask`.

Per nieuw element drie vragen: **(1) staat het op de juiste plek** (domeinkaart + beslisboom
AOR §6)? **(2) heeft het de juiste vorm** (naam, velden, structuur)? **(3) bestaat het al
ergens anders** (dubbel)?

**Notion — nieuwe pagina's en databases**

| # | Norm | Bron |
|---|---|---|
| I-N1 | Nieuwe informatie wordt een **entry in een bestaande database**, geen losse pagina en geen nieuwe database. Een nieuwe database of top-level pagina onder MAFINCO OS vraagt een ja van Bart | Bman-skill v3.2 ("nooit nieuwe DB's/losse pagina's"); Raw Ideas-regel (04/2026); AOR §6 |
| I-N2 | Plaats volgt de beslisboom: project → Projects Master · proces → Processes & Routines · taak → **nooit in Notion** (Todoist) · meeting → Meeting Notes met Area · skill → enkel Skills-DB · delegatie → Register | AOR §6, §8; skillregel 22/09; werkcontract 08/10 |
| I-N3 | Pandinformatie hangt onder de pandfiche, in de vaste subpagina's 01–10 van het pandsjabloon | Pandsjabloon (Overzicht panden, 09/2026) |
| I-N4 | Geen pagina's "Untitled", geen privépagina's met domeininhoud buiten de teamspace | Werkcontract regel 1 (gedeelde bron) |
| I-N5 | Geen tweede pagina over hetzelfde onderwerp (titelvergelijking met bestaande pagina's) | Werkcontract regel 5 |

**Todoist — nieuwe taken en projecten**

| # | Norm | Bron |
|---|---|---|
| I-T1 | Elke nieuwe taak zit in een **project uit de domeinkaart** (Inbox enkel tijdelijk; vrijdag leeg) | Domeinkaart §2; AOR 18/09 |
| I-T2 | Vorm bij aanmaak: titelcode/prefix van de eigenaar of `( )`, duur, P4 | Werkcontract regel 4; AOR 18/09; operating-model §3 |
| I-T3 | Een nieuwe taak voor Bart bestaat enkel als geen agent het kan; **geen beslissingen** in Todoist (die gaan naar de beslislijst) | AOR 09/10; CLAUDE.md routering 6 |
| I-T4 | Geen nieuw Todoist-project zonder plaats in de domeinkaart | Domeinkaart §1.1, §1.4 |
| I-T5 | Geen nieuwe taak die al als registeritem bestaat | Werkcontract regel 5 |

**Dropbox — nieuwe bestanden en mappen**

| # | Norm | Bron |
|---|---|---|
| I-D1 | Een nieuw bestand staat in de **map van de domeineigenaar** volgens de domeinkaart (bv. Detech/Landelis → `BUSINESS/consulting/Landelis BV/…`, boekhouding → `ACCOUNTING & ADMIN`). **Uitzondering — migratiezone:** werk dat Bart in een Claude-project startte (`HUISSTIJL & WERKDOCUMENTEN/projects claude/…`) blijft daar tot het project naar Code is gebracht en gemerged; de Systeemwachter noteert het als *in migratie* en meldt het niet. Na de merge geldt de gewone plaatsingsregel | Domeinkaart §2; Bart 13/10 (Detech) |
| I-D2 | Binnen een dossier de **vaste submappen**: pand `01`–`10` (pandsjabloon) · consultingklant `01 Contract · 02 Werkdocumenten · …` · plaatsbeschrijvingen `03/Plaatsbeschrijvingen/<jaar>/<unit>/` | Pandsjabloon; pagina 05 Consulting (09/10); 03 Huur & gebruik |
| I-D3 | **Bestandsnaam**: huurdersdocumenten `<Kamer> <Voornaam Naam> <academiejaar> - <documenttype>`; documenten: nooit de naam uit de mail of de scanner laten staan (`scan001`), nooit overschrijven. **Algemene conventie (beslist 13/10): `JJJJ-MM-DD_Documenttype_Partij[_detail].ext`**, enkel voor nieuwe documenten. **Foto's vallen buiten de naamregel**: een cameranaam (`IMG_1234`) mag blijven, een zelfgekozen naam ook (Bart 13/10). Werkdocumenten van agents en code vallen erbuiten | Bart 10/10 (staande aanpak fo, nr. 2); Bart 13/10 (§8.1) |
| I-D4 | Geen nieuwe map op niveau 1 of 2 (`/MAFINCO/<x>`, `/PERSOONLIJK/<x>`) zonder plaats in de domeinkaart | Domeinkaart §1.1 |
| I-D5 | Geen kopie van hetzelfde bestand op twee plekken. Uitzondering: een skill die geregistreerd is als "Notion + lokaal/geïnstalleerd" (veld *Geïnstalleerd in*) | Werkcontract regel 5; skillregel 24/09 |
| I-D6 | Agent-output (rapporten, checkups, analyses): de **officiële versie** staat in het domein van de eigenaar (Notion-pagina of Dropbox-dossier). **Werkkopieën** van Code-sessies staan enkel in `/MAFINCO/HUISSTIJL & WERKDOCUMENTEN/Agents/Output/<agent>/` (eigenaar Atlas), nergens anders. Werkkopie zonder officiële versie, of werkkopie buiten die map → SW. Werkkopieën ouder dan 90 dagen → archiveren (voorstel). **Agent-output komt nooit in de repo** (CLAUDE.md governance 5) | Domeinkaart §2; werkcontract regel 5; Bart 13/10 (§8.3) |

**Wat bij afwijking:** altijd **SW aan de eigenaar** (verplaatsen of hernoemen in andermans
map is nooit mechanisch). Uitzondering: elementen in CoS-eigendom (Ecosystem Optimization,
`HUISSTIJL & WERKDOCUMENTEN/Agents`, register-items van Atlas) → fix met log. Verplaatsen in
Dropbox blijft technisch een `ask`.

**Scorecard instroom:** per systeem *nieuw · correct · afwijkend (%)*. Doel na 4 weken:
≥ 90% correct bij aanmaak. Een eigenaar die 3 weken op rij < 80% scoort → één SW "oorzaak"
(regel ontbreekt in zijn skill of routineprompt), niet drie keer dezelfde melding.

### 4.1 Notion

| # | Norm | Bron | Controle | Afwijking |
|---|---|---|---|---|
| N1 | Elke skill staat **één keer** in MAFINCO OS › Skills, enkel de laatste versie, met de vier velden **Bron van waarheid · Geïnstalleerd in · Versie · Bronbestand** ingevuld | AOR 22/09, 24/09 | Hele Skills-DB doorlopen | SW, nooit fix |
| N2 | Bij "Notion + lokaal" is de **versie aan beide kanten gelijk** (Notion-body vs. lokaal bestand) | AOR 24/09 | Versieregel in de paginabody vergelijken met het lokale bestand | SW |
| N3 | Lokaal geïnstalleerde skills zonder DB-item worden gemeld | AOR 24/09 | Lokale skills-map vs. DB | SW |
| N4 | Register "Delegaties & overdrachten": elk open item (niet Klaar/Geannuleerd) met **verstreken deadline** heeft een **Opvolgen op**-datum | Werkcontract 08/10 regel 2 en 5; domeinkaart §1.3 | Query op status + deadline < vandaag + Opvolgen op leeg | Items van CoS: fix (standaard = eerstvolgende evaluatiedatum). Andere eigenaars: SW per agent |
| N5 | Register-items die aan Bart worden voorgelegd volgen **R4 + Werkcontract regel 6**: context, feiten met bron, opties met gevolgen, aanbeveling, één ja/nee-vraag | Goedkeuringsregime R4 (aangevuld 13/10); Werkcontract regel 6 (13/10) | Steekproef op status *Naar Bart* en *Aanpak voorgesteld* | SW aan de agent |
| N6 | Terugkerend werk heeft een item met vinkje **Staande aanpak** en een **vervaldatum** (standaard 3 maanden); een vervallen staande aanpak wordt gemeld | Goedkeuringsregime R1 | View "Staande aanpakken" | SW aan de eigenaar |
| N7 | Een beslissing van Bart staat in de **Beslissingenlog** én op elke plek waar ze gedocumenteerd is (repo, skill, AOR). Een wijziging op één plek = niet doorgevoerd | AOR 18/09 Documentsync | Beslissingen van de week (chat, addenda) afzetten tegen Beslissingenlog en repo | Fix voor de Beslissingenlog (CoS-eigendom); SW voor skills/AOR-teksten |
| N8 | Elke agent heeft een **werkpagina** die na zijn laatste ronde is bijgewerkt (datum laatste wijziging ≤ laatste ronde) | CLAUDE.md; goedkeuringsregime §4 | Bewerkingsdatum per werkpagina | SW aan de agent |
| N9 | Elk Notion-element uit de domeinkaart heeft **precies één eigenaar**; nieuwe DB's of pagina's onder MAFINCO OS zonder eigenaar worden gemeld | Domeinkaart §1.1, §1.4 | Nieuwe top-level items sinds vorige run vs. de kaart | SW: Atlas stelt toewijzing voor en legt vast in de kaart |
| N10 | Hoofd-KPI goedkeuringsregime: **items en minuten** in de views "Wacht op Bart" en "Staande aanpakken", elke vrijdag gemeten tegen de nulmeting (54 / 666 min) en het doel 06/11 (≤ 10 items, < 120 min, ≥ 6 staande aanpakken) | Goedkeuringsregime §5 | Telling | Scorecard, geen fix. Stopregel R2 bewaken: een teruggedraaide stilte-is-ja → SW "R2 opschorten voor agent X" |

### 4.2 Todoist

| # | Norm | Bron | Controle | Afwijking |
|---|---|---|---|---|
| T1 | **Inbox leeg op vrijdag**, behalve label `Quick` | AOR 18/09 | Inbox-telling | Eigen CoS-taken: fix (naar Ecosystem Optimization). Overige: SW aan Bman (eigenaar Inbox) |
| T2 | **Elke taak heeft een duur.** Ontbreekt ze → 15 min. Verjaardagen: 🎁 "over 1 week" = 1 u, 🎂 op de dag = 15 min, overige = 5 min | AOR 18/09 | Open taken komende 8 dagen | Fix (15 min, of de verjaardagsregel). Duidelijk langere taak: SW per taak |
| T3 | Taken van een agent beginnen met `( )` of dragen het label `agent`; taken voor Bart niet. Titelcode `[eigenaar]` volgens de domeinkaart | Werkcontract 08/10 regel 4; operating-model §3 | Open taken per project | SW aan de eigenaar (titel = inhoud van een ander) |
| T4 | **Minimum voor Bart**: een Bart-taak bestaat enkel als geen agent het kan (inloggen, tekenen, betalen, instelling, persoonlijk gesprek). Al het andere hoort in het register of op een werkpagina | AOR 09/10 | Open Bart-taken (zonder `( )`/`agent`) toetsen aan de lijst | SW: per taak "schrappen" of "naar register", nooit zelf verwijderen |
| T5 | Capaciteitscheck: som van de taakduren komende week vs. beschikbare blokuren (Weekstructuur & Focusblokken) | AOR 18/09 | Telling | Scorecard → input voor de Planning Manager (SUGGEST) |
| T6 | Prioriteit: nieuw = P4; hoger enkel binnen 14 dagen, gezet op vrijdag | operating-model §3 | Taken met P1–P3 en datum > 14 d of zonder datum | Fix naar P4 (mechanisch, omkeerbaar) |
| T7 | Geen **dubbels** register ↔ Todoist (zelfde onderwerp op twee plekken) | Werkcontract regel 5 | Titelvergelijking | SW aan de eigenaar |
| T8 | Elke open taak zit in een project dat volgens de domeinkaart een eigenaar heeft | Domeinkaart §2 | Projecten vs. kaart | SW |

### 4.3 Mail (Outlook bart@mafinco.eu, Gmail)

De Systeemwachter leest **geen mailinhoud** en triageert niet (eigenaar: Bman). Zij
controleert enkel of de **mailflows** lopen.

| # | Norm | Bron | Controle | Afwijking |
|---|---|---|---|---|
| M1 | Categorie *waiting* is op vrijdag door Bman opgevolgd (geen item ouder dan 7 dagen zonder actie in register of Todoist) | AOR 09/10 | Telling per categorie, geen inhoud | SW aan Bman |
| M2 | Categorie *FYI*: Landelis/Detech-mails zijn binnen 1 werkdag bij Nova (of Bman als vangnet) geland | AOR 09/10; domeinkaart | Telling ongelezen FYI met die afzenders | SW |
| M3 | Categorieën *accounting / events / investments / real estate / ops* hebben geen items ouder dan 5 werkdagen zonder registeritem of taak | AOR 09/10 | Telling per categorie | SW aan de domeinagent |
| M4 | **Niets verzonden door een agent.** Verzonden Items bevatten enkel mails die Bart zelf of via de dashboardknop verstuurde; elke dashboardverzending heeft "verzonden dd/mm" in het registeritem | AOR 07/10 namiddag; settings.json `ask` | Sent Items van de week vs. register | 🔴 Security-signaal, meteen aan Bart; nooit fix |
| M5 | Barts eigen "FW:"-mails zijn door Bman doorgerouteerd naar de domeinagent (registeritem bestaat) | Domeinkaart Bman | Steekproef | SW aan Bman |

### 4.4 Dropbox

| # | Norm | Bron | Controle | Afwijking |
|---|---|---|---|---|
| D1 | Elke map onder `/MAFINCO` en `/PERSOONLIJK` heeft **één eigenaar** volgens de domeinkaart; nieuwe top-level mappen zonder eigenaar worden gemeld | Domeinkaart §2 | Mappenlijst vs. kaart (alleen lezen) | SW |
| D2 | Triagemappen **TE ONDERTEKENEN · Mobiele uploads · Gezinsruimte** bevatten geen bestanden ouder dan 7 dagen (Bman triageert) | Domeinkaart Bman | Datumtelling | SW aan Bman |
| D3 | Gevoelige documenten (identiteit, codes, zorgvolmachten) staan **buiten** de scope-mappen van de managers (`INVESTMENTS`, `VERMOGENSPLANNING`), in `belangrijke doc oa ID` | fo-manager.md §7 | Bestandsnamen scannen op ID/code/volmacht-patronen, inhoud niet lezen | 🔴 Security-signaal + SW aan Vesta/Lex |
| D4 | Bestanden in `/MAFINCO/HUISSTIJL & WERKDOCUMENTEN/AGENTS` (werkdocumenten van agents) hebben een Notion- of repo-tegenhanger (Documentsync) | AOR 18/09 | Lijst vs. Notion | SW |
| D5 | Geen verplaatsingen of verwijderingen door routines (Dropbox-activiteit van de week) | AOR 07/10 | Recente wijzigingen in scope-mappen | 🔴 Security-signaal |
| D6 | Algemene naamconventie `JJJJ-MM-DD_Documenttype_Partij[_detail].ext` (zie I-D3) | Bart 13/10 (§8.1) | Na beslissing: enkel **nieuwe** bestanden (I-D3); geen massale hernoeming van het archief | SW aan de eigenaar |

### 4.5 Routines en agents

| # | Norm | Bron | Controle | Afwijking |
|---|---|---|---|---|
| R1 | Elke cloudroutine heeft de **vaste connectorset** (Notion, Todoist, Google Calendar, Gmail, Microsoft 365, Strava, Google Drive, Dropbox, Cashfeed), of een gedocumenteerde reden in de prompt waarom niet | AOR 07/10 | Routine-instellingen | SW |
| R2 | Pc-gebonden routines enkel voor lokale bestanden en **enkel overdag** | AOR 07/10 | Schema per routine | SW |
| R3 | Elke routine heeft in de afgelopen week gedraaid op haar schema; een gemiste run wordt gemeld (**stilte = storing**) | AOR §5, §7 | Laatste run vs. schema | SW; ochtendbriefing niet vóór 09:00 = meteen melden |
| R4 | Elke routineprompt bevat "niets verwijderen of verplaatsen" en "ontbrekende bron onder *Wat ik niet kon nakijken*" | AOR 07/10 | Prompttekst | SW |
| R5 | Routineprompts verwijzen naar de Notion-skill en kopiëren ze niet | AOR §8, operating-model §6 | Prompttekst | SW |
| R6 | Vakantie- en pauzeregels (bv. 13/10–01/11 signaalmodus) staan in de skills die ze raken | AOR 09/10 | Skillteksten | SW (nooit fix: skills) |

### 4.6 Repo en technische rem

| # | Norm | Bron | Controle | Afwijking |
|---|---|---|---|---|
| G1 | `.claude/settings.json`: alle delete/trash-tools in `deny`; alle verzend-, betaal-, agenda- en share-tools in `ask`. Nieuwe connectors sinds vorige run hebben hun tools ook in die lijsten | CLAUDE.md governance 1–2; operating-model §6–7 | Toollijst van de sessie vs. settings | SW met voorgestelde regels; nooit zelf wijzigen (guardrail) |
| G2 | Geen persoons- of vermogensdata in git | CLAUDE.md governance 5 | Diff van de week scannen op bedragen, namen, rekeningnummers | 🔴 meteen melden |
| G3 | Elke beslissing van Bart die een regel wijzigt, staat in dezelfde beurt in repo én AOR (Documentsync); de versienummers van governance-docs lopen gelijk met hun Notion-spiegel | AOR 18/09 | Addenda AOR vs. `docs/` | SW |
| G4 | Elke agentdefinitie (`.claude/agents/*.md`) draagt het model en de tools die in CLAUDE.md staan | CLAUDE.md team-tabel | Vergelijking | Fix (repo, CoS-eigendom), met commit |

### 4.7 Cashfeed en Google Calendar

**Buiten scope van de Systeemwachter.** Cashfeed = Lex (tool) en Vesta (monitoring, AOR §7).
Agenda = Bman. De Systeemwachter controleert enkel R3 (draait de routine die ze bewaakt)
en M4/D5-achtige signalen (is er iets verzonden, verplaatst of goedgekeurd zonder ja — via
`ask`-logs, niet via de data zelf).

## 5. Het weekrapport (vast formaat)

```
SCORECARD        — per systeem: aantal afwijkingen per norm (N1…G4), trend t.o.v. vorige week
FIXES (LOG)      — object-ID · norm · oude → nieuwe waarde (omkeerbaar)
VOORSTELLEN      — SW-n · norm · afwijking · default · wat bij nee · eigenaar
SECURITY         — 🔴-signalen (M4, D3, D5, G2) of "geen"
NIET NAGEKEKEN   — bron ontbrak of niet toegankelijk, met naam
```

Regels: max. **7 voorstellen** per week (prioriteit: security > eigenaarloos > stilte >
hygiëne); de rest parkeert met opvolgdatum. Afwijkingen die drie weken na elkaar
terugkomen bij dezelfde eigenaar → één SW "oorzaak" in plaats van drie herhalingen.

## 6. Wat de Systeemwachter uitdrukkelijk niet doet

- Inhoud beoordelen (cijfers, adviezen, mailteksten, dossiers).
- Mails lezen, triageren of beantwoorden.
- Skills aanpassen, ook niet een veld of een versienummer.
- Routines aan-/uitzetten of hun prompt wijzigen.
- Iets verwijderen, verplaatsen buiten CoS-eigendom, of een taak van Bart schrappen.
- Beslissen wie eigenaar is van een nieuw element buiten de kaart zonder dat in de kaart
  vast te leggen en op vrijdag te melden (domeinkaart §1.4).
- Extra dashboards of notificatiestromen opzetten (AOR §3).

## 7. Faalpunten en mitigatie

| Risico | Mitigatie |
|---|---|
| Ruis: te veel SW-voorstellen, Bart klikt ze weg | Plafond 7, prioriteitsvolgorde, kwartaaltoets van de normenlijst (§3) |
| Verkeerde "mechanische" fix die toch een keuze was | Criteria §2 (vastgelegde norm, geen keuze, omkeerbaar, eigen registers) + log met oude waarde; Argus steekproeft de weeklog |
| Controleur controleert zichzelf (CoS-registers) | Argus (onafhankelijk, alleen-lezen) steekproeft Systeemwachter en Atlas (werkpagina 09/10) |
| Pc staat uit → geen run | "Niet gedraaid" is zelf een storing: Bman-weekwacht meldt het ontbreken van de weeklog-run |
| Norm bestaat niet (D6) → agent verzint er een | Expliciete lijst "niet gecontroleerd" in §4; geen controle zonder beslissing |
| Breedste toegang van het systeem | Alleen lezen buiten CoS-eigendom; tellingen en metadata, geen inhoud; geen domeindata in het rapport |

## 8. Open punten — beslissing Bart

1. ✅ **Beslist 13/10: ja. Foto's met cameranaam vallen erbuiten.** **Algemene Dropbox-naamconventie (I-D3, D6).** Het voorstel van 21/09 is nooit beslist.
   Steekproef 02–13/10 in `/MAFINCO`: drie datumformaten naast elkaar
   (`20261006 - Detech - Term sheet.pdf`, `2026-06-30_Kwartaalrapport_Belfius.pdf`,
   `basiscase-30062026.md`) plus onhernoemde camerabestanden (`IMG_5173.HEIC`). Default:
   **`JJJJ-MM-DD_Documenttype_Partij[_detail].ext`** voor originele documenten, enkel voor
   nieuwe bestanden; huurdersregel van 10/10 blijft de uitzondering; werkdocumenten van agents
   en code vallen erbuiten.
2. ✅ **Beslist 13/10: ja**, met: foto's vrij van naamregel, migratiezone voor Claude-projecten, opkuisronde eind november. **Instroomcontrole als vast onderdeel (§4.0)**, venster = sinds de vorige run, enkel
   melden aan de eigenaar.
3. ✅ **Beslist 13/10: ja. Werkkopieën agent-output** → één map `Agents/Output/<agent>/`; officiële versie in het domein; nooit in de repo. De twee Q3-checkup-kopieën zijn op 13/10 verplaatst van `BUSINESS/Experience app/output/` naar `Agents/Output/Lex/`. **Security-melding:** vermogensdata van alle agents samen in één map (geen bredere toegang, wel concentratie). Mitigatie: geen gedeelde links op die map, archiveren na 90 dagen.
4. ✅ **Beslist 13/10: ja.** **Plafond voorstellen per week = 7** en 3-wekenregel (§5). Default: ja.
5. ✅ **Beslist 13/10: ja (fix met log).** **T6 (prioriteit terug naar P4) als mechanische fix.** Raakt Barts eigen lijst; alternatief
   is SW. Default: fix, want de regel is expliciet (operating-model §3) en omkeerbaar.
6. ✅ **Beslist 13/10: ja (enkel tellen per categorie + controle Verzonden Items; geen inhoud, geen onderwerpen in het rapport).** **M1–M3 mailtellingen.** Dit leest categorie en datum, niet de inhoud. Akkoord dat de
   Systeemwachter dat mag, of blijft mail volledig bij Bman? Default: tellen mag.
7. ✅ **Beslist 13/10: nulmeting nu** ("alles nu opgelost en op elkaar afgestemd"), uitgevoerd in de cloudsessie van 13/10 en gelogd in de weeklog. Tijdens de vakantie draait de weekcheck stil (enkel weeklog); het eerste rapport aan Bart komt op **vr 06/11**.

## 9. Documentsync na akkoord

| Waar | Wat |
|---|---|
| `docs/governance/chief-of-staff.md` §2 | Verwijzing naar dit document; status v1.1 |
| Notion: AOR | Addendum met link naar dit document; de losse Systeemwachter-regels uit de addenda 18/09, 22/09, 24/09, 07/10, 09/10 verwijzen hierheen |
| Notion: Systeemwachter — weeklog | Kop verwijst naar dit document; scorecard volgt §5 |
| Lokaal: scheduled task `systeemwachter-weekcheck` | Prompt verwijst naar dit document en kopieert de normen niet |
| Notion: Beslissingenlog | BES-item "Mandaat Systeemwachter v1.1" |
| Skill pre-accountant checkup (Lex) + Code-projecten | Outputpad werkkopie → `Agents/Output/<agent>/` (§8.3) |

Kill switch: dit bestand hernoemen; dan geldt enkel AOR §2 (mechanische fix met log) zonder
normenlijst, en de weekcheck meldt alleen nog R3 (stilte-detectie).

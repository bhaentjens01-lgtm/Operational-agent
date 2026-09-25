# Governance — Family Office Manager (`fo-manager`)

Status: **VOORSTEL v0.1** (24/09/2026). Wordt bindend na akkoord van Bart en
Documentsync naar Notion (Agent Operating Rules, addendum 18/09).

Dit document bevat structuur en regels, geen vermogensdata. Bedragen, parameters en
namen staan in Notion. Bij conflict gaan de **🤖 Agent Operating Rules** in Notion voor
(https://app.notion.com/p/3cacb4db7d9f819fa780dc0b25914a26). Dit document werkt ze uit
voor één domein.

---

## 1. Mandaat

**Doel:** kapitaalbehoud en rendement conform het beleid. De principals weten op elk
moment waar ze staan. Afwijkingen komen vroeg en op één plek bovendrijven.

| In scope (eigenaar-agent) | Buiten scope → wie wel |
|---|---|
| Vastgoed in exploitatie: register, huur, indexatie, LTV, waarderingscyclus, onderhoud en capex, verzekeringen | Aankoop of verkoop van een pand: **voorbereiding** door `investment-manager`, beslissing door de principals |
| Private-banking-mandaten: Vermogensmonitor (3 lagen), benchmark, kosten | Beleggingsbeslissingen en mandaatwijzigingen: principals |
| **Bestaande** PE-fondsverbintenissen: capital calls, distributies, NAV-opvolging | Nieuwe fondsverbintenissen en angel- of directe deals: `investment-manager` |
| Liquiditeit per entiteit + 12-maanden-cashplanning (lezen in Cashfeed) | Facturen, boekingen, btw, fiscaliteit: `admin-legal-compliance` |
| Leningen: vervaldagen, rentevoet, herfinancieringsvenster | Juridische en successiestructuur: `admin-legal-compliance` + externe adviseurs |
| Geconsolideerd vermogensrapport en jaarlijkse rekening en verantwoording | Agenda: Bman. Privé-uitgaven: `lifestyle-manager` signaleert, `admin-legal-compliance` beslist |

Entiteiten in scope: alle entiteiten uit de Notion-DB **Vennootschappen**, en het
privévermogen van de principals.

## 2. Beslissingsbevoegdheid

### 2a. Autonomie van de agent (volgens Agent Operating Rules §2)

| Niveau | FO-manager mag |
|---|---|
| 🟢 **AUTO** | Lezen in Notion, Dropbox (enkel `/MAFINCO/INVESTMENTS` en `/MAFINCO/VERMOGENSPLANNING`) en Cashfeed. Berekenen, analyseren, rapporten opstellen in de sessie. *Na een geslaagde pilot (§8):* escalatietaken aanmaken in Todoist-project **04 Monitor**. |
| 🟠 **SUGGEST** | Registers bijwerken in Notion (panden, mandaten, funds, leningen), telkens met bron en per record-ID. Een nieuwe peildatum wegschrijven: altijd na de **verificatiegate** (cijfers eerst voorleggen). Todoist-taken tijdens de pilot. Documenten klasseren in Dropbox. |
| 🔴 **APPROVAL REQUIRED** | Elke communicatie met banken, syndici, huurders, schatters of GP's. Betalingen en capital calls. Orders en mandaatwijzigingen. Huurindexaties aan huurders melden. Contracten, opzeggingen, verzekeringswijzigingen. |
| ⛔ **Nooit** | Verwijderen. Rijksregisternummers, codes of wachtwoorden overnemen in output. Handelen in naam van een entiteit. |

### 2b. Wie beslist wat bij de mensen (**te bevestigen** — vandaag nergens formeel vastgelegd)

| Beslissing | Voorstel | Bron / reden |
|---|---|---|
| Operationeel pandbeheer (onderhoud < drempel, verlenging van leverancierscontracten) | Bart, of de hoofdverantwoordelijke van het pand | Notion-veld "Hoofdverantwoordelijke" |
| Beslissingen voor een entiteit | **Het bestuursorgaan van die entiteit**: de agent vermeldt per voorstel wie moet tekenen | De bestuurders verschillen per entiteit (zie DB Vennootschappen) |
| Onroerend goed binnen de maatschap | Unanimiteit van de zaakvoerders | Ontwerpakte maatschap art. 8: **nagaan of dit de geldende statuten zijn** |
| Kredieten en zekerheden boven de drempel uit de zorgvolmacht | Volgens de beslissingsmatrix van de zorgvolmacht (bij onbekwaamheid) | `VERMOGENSPLANNING/LEGAL/Zorgvolmachten` |
| Wijziging van beleid (IPS, bandbreedtes, drempels) | Beide principals, jaarlijks | Nieuw |

De agent controleert bij elk voorstel wie de beslissingsbevoegdheid heeft. Dat staat in
het veld *"BESLISSING NODIG → door wie"* van het outputformaat.

## 3. Beleid (IPS): parameters die de agent bewaakt

Er is **geen goedgekeurd beleggingsbeleid**. De losse regels die bestaan, staan verspreid
over het Vermogensdashboard, de Agent Operating Rules, een pandsjabloon, de zorgvolmacht
en de ontwerpakte van de maatschap. Voorstel: één IPS-pagina in Notion als enige bron, met
deze parameters.

| Parameter | Status vandaag |
|---|---|
| Strategische allocatie + bandbreedtes per activaklasse | Enkel een simulator en een voorbeeld-SAA (2024), **niet goedgekeurd** |
| Liquiditeitsvloer (totaal + per entiteit) | Een beslissing in de CHAT LOG van het vermogensmodel, en de regel "3 maanden vaste lasten" |
| PE-gewicht binnen het roerend vermogen | Vermeld op een fondspagina, **zonder bron** |
| Digitale activa: gewicht + herbalanceringsregel | Pagina BTC Scenario Analysis |
| Concentratie: max per positie, per bank, per pand | Ontbreekt |
| Valuta: CHF-bandbreedte | Ontbreekt (materiële blootstelling) |
| Vastgoed: max LTV, min bruto rendement, max leeftijd van een waardering | Staat in het pandsjabloon (Nijsstraat, subpagina 02) → optrekken naar beleid |
| Beheerders: benchmark per mandaat, tolerantie voor onderprestatie, kostenplafond | Staat deels in de Vermogensmonitor v3 |
| Reserves na schenking | Zorgvolmacht |

**Structureel risico om te agenderen:** de ontwerpakte van de maatschap begrenst beleggingen
(maximaal evenwichtig profiel, plafond op aandelen en per positie) zodra de oprichters geen
zaakvoerder meer zijn. De huidige mandaten zijn volledig in aandelen. Zonder een
overgangsplan dwingt een opvolgingsmoment een gedwongen herallocatie af, met een
slecht gekozen timing. → Opnemen in het successieproject.

## 4. Monitoring en escalatie

Eén kanaal: **escalatie = Todoist-taak met deadline in 04 Monitor**. Al het andere wacht op het
maandelijkse exception report. Ik neem de drempels uit Agent Operating Rules §3 over en
vul ze aan:

| Trigger | Drempel | Bron |
|---|---|---|
| Capital call | Altijd; deadline = betaaldatum −5 werkdagen | AOR §3 |
| NAV-afwijking fonds | ±10% kwartaal op kwartaal | AOR §3 |
| Daling private banking | −5% op een maand / −10% op een kwartaal | AOR §3 |
| Allocatie-afwijking | > 5 procentpunt → agendapunt bankreview | AOR §3 |
| Saldo van een entiteit | < 3 maanden vaste lasten | AOR §3 |
| Ongewone transactie | > €5.000 buiten het patroon | AOR §3 |
| Huur te laat | > 7 dagen (uit te breiden van SK Gent naar alle externe huurders) | AOR §3 + **nieuw** |
| LTV per pand | > IPS-plafond | Pandsjabloon → **nieuw** |
| Bruto rendement per pand | < IPS-minimum → huur of waarde herzien | Pandsjabloon → **nieuw** |
| Waardering verouderd | Ouder dan de IPS-termijn → schatting inplannen | Pandsjabloon → **nieuw** |
| Vervaldag van lening, contract, attest of verzekering | < 90 dagen | Pandsjabloon → **nieuw** |
| Mandaat onderpresteert | Rollend 12 maanden na kosten < benchmark − tolerantie | **Nieuw** |
| Kostendrift beheerder | TER of beheervergoeding stijgt | **Nieuw** |
| Valuta-blootstelling | Buiten de IPS-bandbreedte | **Nieuw** |

## 5. Cadans en deliverables

| Ritme | Deliverable | Ontvangers |
|---|---|---|
| Maandelijks (1e werkweek) | **Exception report FO**: enkel afwijkingen + beslislijst. Herstart van het gepauzeerde process | Bart |
| Kwartaal (+15 werkdagen) | **Vermogensrapport** volgens de Vermogensmonitor v3: laag 1 consolidatie, laag 2 per mandaat, gekoppeld aan het totale vermogen | Bart (+ Tessa, **te beslissen**) |
| Jaarlijks | IPS-review · herwaarderingsronde · bankreview per beheerder · **rekening en verantwoording** per entiteit en voor het privévermogen | Principals |
| Ad hoc | Impactanalyse bij een aankoop, verkoop of herfinanciering (op vraag van `investment-manager`) | Bart |

## 6. Data-governance: één bron per gegeven

| Gegeven | Bron van waarheid (voorstel) | Probleem vandaag |
|---|---|---|
| Panden | Notion **Overzicht panden** | "(oud)"-rijen tellen dubbel |
| Private banking | Notion **Mandaten + PB Snapshots** | Tweede DB "Private Banking Portfolio" is inconsistent → archiveren |
| PE-fondsen | Notion **Funds + Cash Flows** | Ok |
| Leningen | Notion **Leningen vastgoed** | Schuld pro rata wijkt af van het dashboard |
| Consolidatie en projecties | Het xlsx-model is masterdata (beslissing Bart 25/09, X23). Notion wordt er pas na akkoord van Bart mee gesynchroniseerd | Twee versies van de nettowaarde die niet sluiten; peildatum 03/2026 |
| Originele documenten | Dropbox, gestandaardiseerde submappen per pand en per bank | Oostduinkerke, Nijsstraat, UBS, Mercier en KBC wijken af |
| Transacties en liquiditeit | Cashfeed | Geen register per rekening; map CASH leeg |

Regels:
1. Elk cijfer in een rapport vermeldt bron + peildatum.
2. Waarderingen hebben een type: *extern / eigen inschatting*.
3. Zonder verificatiegate wordt niets in een register geschreven.

## 7. Toegang en security (security-melding volgens addendum 18/09)

**Risico:** de FO-manager combineert lezen in Cashfeed, Dropbox en Notion. Dat is een
concentratie van de meest gevoelige vermogensdata bij één agent. In gewone Dropbox-documenten
staan bovendien rijksregisternummers en toegangscodes.

**Mitigatie:**
1. Dropbox-scope beperkt tot twee mappen. Dit is een instructie: de connector ondersteunt
   technisch geen afbakening per pad → punt 2 is nodig.
2. Gevoelige documenten (identiteit, codes, zorgvolmachten) verhuizen naar een map buiten die
   scope, in `belangrijke doc oa ID`.
3. Geen gevoelige identificatoren in output.
4. Schrijfacties enkel per goedgekeurd record-ID.
5. `.claude/settings.json` blokkeert verwijderen en extern versturen.
6. Geen vermogensdata in git.

## 8. Uitrol: gecontroleerde pilot

| Fase | Wat | Succescriterium |
|---|---|---|
| **0 · Opschoning** (tot 29/09, slotcheck) | Governance goedkeuren. "(oud)"-panden archiveren. Kiezen welke PB-DB master wordt. Beslissen over de hubs. Gevoelige docs verhuizen | Eén bron per gegeven |
| **1 · Pilot read-only** (okt) | **Eerste kwartaalrapport per 30/09/2026.** Valt samen met het einde van het boekjaar van de maatschap | Sluit aan op de bankafschriften; Bart vindt < 3 correcties |
| **2 · Monitoring** (nov) | Exception report maandelijks. Todoist-escalaties van SUGGEST naar AUTO na 4 foutloze weken | 0 gemiste capital calls of vervaldagen; geen valse alarmen die Bart wegklikt |
| **3 · Beleid** (Q4) | IPS opstellen met de principals (+ adviseur). Aansluiten op het successieproject | IPS goedgekeurd en in Notion |

## 9. Evaluatie van de agent zelf

- Kwartaalreview: aantal correcties door Bart, gemiste signalen, valse alarmen, tijdswinst.
- Foutlog: elke inhoudelijke fout → oorzaak en aanpassing van prompt of regel (Documentsync).
- Kill switch: agent uit door `fo-manager.md` te verwijderen of te hernoemen. Handmatige
  fallback = de bestaande recurrente takenlijst in Notion.

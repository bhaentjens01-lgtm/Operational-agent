# Operational Agent — Mafinco Family Office

Agent-team voor het Mafinco family office, gebouwd als Claude Code subagents.

| Agent | Domein |
|---|---|
| `fo-manager` | Vastgoed in exploitatie, roerende beleggingen, liquiditeit |
| `investment-manager` | Dealflow, due diligence, IC-memo's, participaties |
| `admin-legal-compliance` | Boekhouding, fiscaliteit, vennootschapsrecht, contracten, compliance |
| `lifestyle-manager` | Agenda, reizen, events, gezondheid, privé-leveranciers |

- `CLAUDE.md` — routering, governance en outputformaat (Chief of Staff)
- `.claude/agents/` — de agentdefinities
- `.claude/settings.json` — technische rem op externe en destructieve acties
- `docs/operating-model.md` — grensafspraken, cadans, pilot-roadmap, risico's, open beslissingen

Gebruik: open een Claude Code-sessie op dit repo en stel je vraag; de hoofdsessie
routeert. Een agent rechtstreeks aanspreken: "Laat de investment-manager deze deal triëren."

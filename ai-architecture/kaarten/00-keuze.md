# Keuze: referentie voor LLM-functies

Stand 2026-11-23, bronnen op de commits in `sources.json`.

## Antwoord

Eén repo die alles goed voordoet bestaat niet. Per situatie:

| Situatie | Vertrekpunt | Waarom |
|---|---|---|
| LLM-functies in een bestaand product | Het actieregister dat er al is; anders zelf bouwen met kaarten 11, 12, 30, 55, 56 | Eén dispatcher: onbekend weigeren, invoer toetsen, rechten van de persoon, lezen direct, schrijven als voorstel. Rechten en data blijven in het product |
| Nieuw project in Python | Het register, plus pydantic-ai voor de modellus | Getypte tools, uitgestelde goedkeuring, limieten. Duurzaamheid blijft van de app |
| Nieuw project in TypeScript | agent-native als ontwerp | Eén actie voor UI, HTTP, agent en MCP, met `authorize` rond `run` zelf |
| Bedrijfskennis | Onyx als ontwerp, eigen Postgres als opslag | Toegangslijst zit in de zoekvraag, niet in een filter achteraf |
| Toezicht en goedkeuring | OpenBot | Vaste volgorde, goedkeuring verbruikt met één voorwaardelijke UPDATE |
| Agent voor een heel team | qm | Geheugen, sleutels en rechten per persoon en per kamer |

## Waarom niet als basis

- **PostHog**: beste om te lezen, niet om te gebruiken. De licentie van `ee/` staat kopiëren alleen toe voor ontwikkelen en testen. Alle 18 bestanden met een `MaxTool` staan daar.
- **Twenty, Dub, Documenso**: AGPL. Alleen idee.
- **Dify, Open WebUI, LibreChat, Onyx ernaast draaien**: tweede gebruikers-, rechten- en datalaag naast het product.
- **LangGraph en LangChain**: lossen de lus op. Het werk zit in rechten, goedkeuring en data. Niet gelezen voor dit oordeel.
- **pydantic-ai in een product met eigen register**: het register en het voorstelblad bestaan al. De eigen docs zeggen dat goedkeuring geen toegangsgrens is bij een onbetrouwbare client (`docs/deferred-tools.md:114`).

## Plan voor een nieuw project

1. Evalset van 20 echte vragen. 2. Register en dispatcher, alleen lezen. 3. Chat als afnemer. 4. Schrijven met goedkeuring en duurzame rij. 5. Kennis met rechten in de zoekvraag. 6. MCP uit hetzelfde register. 7. Langlopend werk als een taak het vraagt.

Modeltoegang loopt via sleutels per tenant met een verwerkersovereenkomst. Een abonnementsseat is één identiteit met één limiet en past niet bij meerdere klanten. Juridisch niet nagezocht.


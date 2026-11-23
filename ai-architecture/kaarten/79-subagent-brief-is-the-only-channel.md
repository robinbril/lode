# De opdracht aan een subagent is het enige wat de ouder hem meegeeft, dus ze bevat doel, uitvoerformaat, bronnen en grenzen

Probleem: een orkestrator stuurt "onderzoek het tekort aan halfgeleiders" naar drie subagents. Ze lezen de opdracht verschillend, dubbelen elkaars zoekwerk en laten gaten.

Oplossing:
- De enige inhoud die van ouder naar kind gaat is de promptstring van de agent-tool. Het kind start zonder het gesprek, de toolresultaten en de systeemprompt van de ouder; wel met zijn eigen systeemprompt, de project-CLAUDE.md en tooldefinities. Een fork is de uitzondering: die kopieert het gesprek. Zet bestandspaden, foutmeldingen en genomen beslissingen dus in de prompt.
- Elke brief heeft vier velden: doel, uitvoerformaat, hulp bij tools en bronnen, en duidelijke taakgrenzen.
- Alleen het eindbericht komt terug bij de ouder; de tussenstappen blijven in het kind. Vraag daarom om een compact resultaat.
- Grote tussenresultaten gaan naar een bestand en de agent geeft een verwijzing terug. Zo voorkom je het spelletje stille post via de orkestrator.
- Zet schaalregels in de orkestratorprompt, zodat het aantal subagents en de inspanning passen bij de complexiteit van de vraag.
- Beperk diepte, gelijktijdigheid en uitgaven. In de Agent SDK staat de standaarddiepte op 3 lagen, het maximum aan tegelijk draaiende subagents op 20. Een budgetplafond per query (`maxBudgetUsd`, inclusief subagents) bestaat, maar staat standaard uit.
- Geef een subagent alleen de tools die zijn taak vraagt (een reviewer met lezen en zoeken, zonder schrijven).
- Behandel het resultaat als claim: de ouder draait de acceptatiecheck zelf.

Waarom het werkt: een kind met een volledige brief hoeft niet te raden, en een compact resultaat houdt de context van de orkestrator schoon.

Niet doen als: het werk sterk afhankelijk is van wat de ouder al weet en niet in een korte brief past; houd het dan in één agent.

Toetsvraag: heeft het briefsjabloon velden voor doel, uitvoerformaat, tools, grenzen en klaar-criterium, en zit er een diepte- en budgetgrens op?

Bronnen:
- https://www.anthropic.com/engineering/multi-agent-research-system (gelezen 2026-11-23) "clear task boundaries"
- https://code.claude.com/docs/en/agent-sdk/subagents (gelezen 2026-11-23) "prompt string"

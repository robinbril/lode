# Context heeft een budget en een volgorde: lange documenten bovenaan, de vraag onderaan, en alleen wat de taak nodig heeft

Probleem: je plakt een hele handleiding of repo in de prompt "voor de zekerheid". Het model raakt afgeleid, het relevante stuk staat midden in een lange tekst en de kosten lopen op.

Oplossing:
- Behandel context als eindige hulpbron met afnemende opbrengst: zoek de kleinste set tokens met veel signaal, en haal de rest pas op als de taak erom vraagt.
- Zet lange documenten bovenaan, de vraag en instructies onderaan; de Claude-documentatie meldt voor invoer vanaf ongeveer 20.000 tokens tot 30 procent betere antwoorden in eigen tests, vooral bij meerdere documenten.
- Vraag bij lange documenten eerst om de relevante citaten voordat het antwoord komt. Dat helpt het model de rest te negeren.
- Zet het belangrijkste niet in het midden: in het onderzoek naar vragen over meerdere documenten en key-value-opzoekingen was de score vaak het hoogst als de relevante tekst aan het begin of eind stond en zakte hij in het midden.
- Afleiders kosten nauwkeurigheid: in de Chroma-test scoorden gerichte prompts van ongeveer 300 tokens hoger dan volledige van ongeveer 113.000 tokens, bij alle modellen in die proef (LongMemEval). De gerichte prompt bevatte daar precies de relevante delen; je eigen selectie kan slechter zijn.
- Meet het op je eigen taak: varieer de lengte en de plek van het relevante stuk en zet de drempel voor inkorten op de gemeten knik, niet op de adverteerde venstergrootte.
- Een vast document vooraan met de wisselende vraag achteraan past ook bij een stabiel cache-prefix.

Waarom het werkt: de plek met de grootste aandacht van het model krijgt de informatie die ertoe doet, en minder tokens betekent minder ruis en lagere kosten.

Niet doen als: je taak het hele document echt nodig heeft (samenvatten van een geheel); meet dan eerst of inkorten iets verliest.

Toetsvraag: is er een test die lengte en positie van de relevante passage varieert op onze eigen taak?

Bronnen:
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (gelezen 2026-11-23) "Queries at the end"
- https://arxiv.org/abs/2307.03172 (gelezen 2026-11-23) "position of relevant information"
- https://www.trychroma.com/research/context-rot (gelezen 2026-11-23) "focused prompts"
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (gelezen 2026-11-23) "finite resource"

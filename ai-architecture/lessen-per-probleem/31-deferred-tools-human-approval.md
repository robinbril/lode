# Een deferred tool-call matcht op tool_call_id, nooit op volgorde, en een voorbereide goedkeuring is single-use

Probleem: wie een goedkeuringsstap voor een risicovolle tool-call bouwt en de antwoorden simpelweg op index aan de oorspronkelijke calls terugkoppelt, verwisselt approvals zodra de batch van volgorde wisselt; en een vooraf verleende goedkeuring blijft na een falende stap in dezelfde batch ten onrechte gelden.

Oplossing:
- pydantic-ai geeft bij een call die wacht op mens-goedkeuring of externe uitvoering een `DeferredToolRequests`-output terug met losse lijsten `calls` en `approvals`, elk een lijst van `ToolCallPart` met een eigen `tool_call_id`.
- Het antwoord erop is een `DeferredToolResults` met `approvals: dict[tool_call_id, bool | DeferredToolApprovalResult]`: de koppeling loopt altijd via die ID, nooit via positie in een lijst, dus de volgorde van de antwoorden maakt niet uit. Bij hervatten moet wel elke openstaande call een resultaat krijgen: ontbreekt er een, dan gooit pydantic-ai een `UserError` ("need to be provided for all deferred tool calls"). Alleen een handler-flow kan een deel zelf afhandelen en de rest als `DeferredToolRequests` laten doorstromen.
- Hermes-agent bereidt (alleen in de desktop-modus) bij een batch van meerdere terminal-commando's de consent-beslissing per slot alvast voor, maar zo'n voorbereide beslissing is single-use, ook als twee calls identiek zijn, zodat eenzelfde commando niet per ongeluk tweemaal op dezelfde oude toestemming leunt.
- Zodra een eerdere slot in de batch een mislukt of geweigerd resultaat publiceert (`failure_seen`), valt de voorbereide beslissing voor latere slots terug op de live goedkeuringsflow: een menselijk antwoord wint altijd, alleen het automatisch voorbereide deel wordt genegeerd.

Waarom het werkt: de ID is de enige sleutel tussen vraag en antwoord, dus herordenen kan nooit een approval aan de verkeerde call hangen, en een voorbereide beslissing kan niet twee keer of na een falende voorgaande stap worden verbruikt.

Niet doen als: er is maar één tool-call per beurt en geen batch-concurrency; dan is de simpele vraag-antwoord-flow zonder ID-matching voldoende.

Toetsvraag: blijven approvals aan de juiste call hangen als de batch in een andere volgorde terugkomt, en wordt een vooraf verleende goedkeuring niet meer gebruikt nadat een eerdere call in de batch faalde?

Bronnen:
- pydantic/pydantic-ai@d32d5c648bec67496dfcfb93803d257e6996d9c8 pydantic_ai_slim/pydantic_ai/_deferred.py:246 "DeferredToolApprovalResult"
- pydantic/pydantic-ai@d32d5c648bec67496dfcfb93803d257e6996d9c8 pydantic_ai_slim/pydantic_ai/_tool_execution.py:553 "result_tool_call_ids"
- NousResearch/hermes-agent@8da31006f3bcf70d0df05fb2b5a334eec4db2e07 agent/terminal_approval_batch.py:238 "slot.decision"

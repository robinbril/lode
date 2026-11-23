# Een budget dat alleen bij de aanvraag gecontroleerd wordt, is lek zodra een fallback naar een ander model switcht

Probleem: een team-budget dat eenmalig bij authenticatie tegen het aangevraagde model wordt gecontroleerd, kan alsnog ongelimiteerd kosten maken zodra de router later intern naar een duurder fallback-model springt, want die stap gebeurt na de budgetcheck.

Oplossing:
- pydantic-ai's `UsageLimits` zet een default `request_limit=50` op het aantal agent-stappen (niet providerrequests) en een optionele `cost_limit` in USD; de requestlimiet wordt aan het begin van elke stap gecontroleerd, tokenlimieten na elk antwoord.
- litellm's router kent een expliciet `FallbackBudgetCheck`-protocol juist omdat budget standaard maar één keer tijdens auth tegen het aangevraagde model wordt afgedwongen: een gratis model-group die intern naar een duurder model fallbackt, zou anders zonder budgetpoort kunnen factureren. De router roept deze check voor elke cross-model-group fallback-poging opnieuw aan en slaat doelen af die hem niet doorstaan.
- Conclusie voor een eigen FastAPI-laag: budget en usage-limits horen niet alleen bij de binnenkomende request te zitten, maar ook bij elke interne modelwissel binnen diezelfde run.

Waarom het werkt: het budget wordt op het punt gecontroleerd waar de kosten ontstaan (elke modelkeuze), niet alleen op het punt waar het request binnenkomt.

Niet doen als: er is geen fallback-keten en elk team praat altijd met precies één vastgepind model; dan is een eenmalige budgetcheck bij auth voldoende.

Toetsvraag: wordt het teambudget opnieuw gecontroleerd op het moment dat de router naar een ander, duurder model fallbackt?

Bronnen:
- pydantic/pydantic-ai@d32d5c648bec67496dfcfb93803d257e6996d9c8 pydantic_ai_slim/pydantic_ai/usage.py:559 "request_limit"
- BerriAI/litellm@3e27fc2a88d2545a706fb9cc1a85ea99e474f18c litellm/types/router.py:1349 "FallbackBudgetCheck"

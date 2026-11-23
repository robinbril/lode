# Een tool krijgt zijn dependencies via het eerste getypeerde RunContext-argument, nooit via globale state

Probleem: tool-functies die een databaseconnectie, API-client of ingelogde gebruiker uit een module-global of threadlocal lezen, zijn niet testbaar en lekken state tussen gelijktijdige runs.

Oplossing:
- Een Agent krijgt een `deps_type` vastgepind bij aanmaak; elke tool-functie die state nodig heeft, neemt als eerste parameter `ctx: RunContext[MyDeps]` en leest `ctx.deps`.
- `RunContext` is een dataclass met onder andere `deps`, `model`, `usage`, `usage_limits` en `deadline`: een tool kan dus ook het resterende budget of de run-deadline aflezen zonder die apart door te geven. De tool-manager maakt per tool-call een kopie (`replace(self.ctx, tool_call_id=..., retry=...)`) met dezelfde `deps`-verwijzing.
- De schema-builder verzamelt fouten en gooit daarna een `UserError` bij het bouwen van het tool-schema: een eerste parameter van een ctx-tool zonder `RunContext`-annotatie, of een `RunContext`-annotatie op een andere plek dan positie 0, faalt dus bij registratie en niet pas tijdens een live call. Een kale `RunContext` zonder `[...]` wordt wel geaccepteerd.
- Dependency injection loopt zo door de run, niet via een los container-framework: dezelfde `deps`-instantie is bereikbaar in elke tool van die run.

Waarom het werkt: de dependency komt per run mee als argument in plaats van uit een global, dus twee gelijktijdige runs raken elkaars state niet, zolang de aanroeper per run een eigen `deps`-instantie meegeeft.

Niet doen als: de tool heeft geen externe state nodig, zoals een pure rekenfunctie; dan is een RunContext-parameter alleen ruis.

Toetsvraag: kan deze tool draaien met een nep-deps-object in een test, zonder een echte database of API aan te roepen?

Bronnen:
- pydantic/pydantic-ai@d32d5c648bec67496dfcfb93803d257e6996d9c8 pydantic_ai_slim/pydantic_ai/_run_context.py:230 "RunContextAgentDepsT"
- pydantic/pydantic-ai@d32d5c648bec67496dfcfb93803d257e6996d9c8 pydantic_ai_slim/pydantic_ai/_function_schema.py:393 "RunContext[...]"

# Een toolset filtert per aanroep opnieuw via RunContext, niet eenmalig bij het opstarten van de agent

Probleem: tools eenmalig filteren op rol bij het bouwen van de agent betekent dat een rolwijziging of multi-tenant request pas werkt na een herstart, en twee gebruikers die dezelfde agent-instantie delen krijgen dezelfde toolset.

Oplossing:
- `FilteredToolset` wrapt een andere toolset en roept bij elke stap opnieuw `get_tools(ctx)` aan; de `filter_func(ctx, tool_def)` krijgt de actuele `RunContext` (met `ctx.deps`, waar de ingelogde gebruiker of tenant in zit) en de `ToolDefinition`, en beslist per tool of die meedoet.
- Omdat dit vóór elke stap opnieuw draait (`for_run_step`), kan een wijziging in de `deps` van de run (bijvoorbeeld een tool die de actieve tenant of het project zet) de zichtbare toolset voor de volgende stap al veranderen, zonder dat de agent opnieuw gebouwd wordt. Keerzijde: een toollijst die midden in een gesprek wisselt, gooit een stabiel cacheprefix weg (zie de kaarten over feature flags en KV-cache); wissel dus alleen als de rechten echt veranderen.
- `PreparedToolset` krijgt de hele lijst tool-definities en geeft er een terug; die mag de definities per context aanpassen (beschrijving, schema), maar geen tools toevoegen of hernoemen. Die grens wordt afgedwongen met een `UserError` die verwijst naar `FunctionToolset.add_function()` en `RenamedToolset`.

Waarom het werkt: de rechten worden elke stap opnieuw uit de actuele context bepaald, en een prepare-functie kan de toolset per ongeluk niet uitbreiden: nieuwe of hernoemde namen worden geweigerd.

Niet doen als: de toolset is voor iedereen identiek en wijzigt nooit binnen een run; dan is een statische lijst bij het bouwen van de agent genoeg.

Toetsvraag: verandert de zichtbare toolset mee binnen dezelfde conversatie zodra de rol of tenant van de gebruiker tijdens de run wijzigt?

Bronnen:
- pydantic/pydantic-ai@d32d5c648bec67496dfcfb93803d257e6996d9c8 pydantic_ai_slim/pydantic_ai/toolsets/filtered.py:24 "async def get_tools"
- pydantic/pydantic-ai@d32d5c648bec67496dfcfb93803d257e6996d9c8 pydantic_ai_slim/pydantic_ai/toolsets/prepared.py:35 "RenamedToolset"

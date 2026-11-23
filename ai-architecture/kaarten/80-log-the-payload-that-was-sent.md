# Je logt het verzoek zoals het naar het model ging, niet de instellingen waaruit je denkt dat het is gebouwd

Probleem: een agent gedraagt zich vreemd en het log toont een systeemprompt en parameters. Dat bleken de bedoelde waarden te zijn; wat er echt naartoe ging verschilde per provider, tool-lijst of samengevoegde geschiedenis.

Oplossing:
- Leg per modelaanroep vast wat de aanroep verliet: de berichten in de volgorde waarin ze zijn verstuurd, de systeeminstructies apart, de toolbeschrijvingen die waren meegegeven, model-id en de parameters die de client echt meestuurt.
- De OpenTelemetry GenAI-conventies doen het zo: `gen_ai.input.messages` staat in verzendvolgorde, `gen_ai.system_instructions` en `gen_ai.tool.definitions` zijn eigen attributen.
- Die inhoudsattributen zijn opt-in en worden als gevoelig gemarkeerd. Zet inhoud standaard uit of redigeer; sla grote payloads buiten de tracebackend op en bewaar een `_ref` met de locatie.
- Leg per stap ook vast welke tool is gekozen en waarom de lus doorging, zodat een mislukte run zonder reproductie te lezen is.
- Volg beslispatronen en structuur, niet alleen fouten: het onderzoeksteam van Anthropic diagnosticeerde falende agents met volledige productietracing, zonder de inhoud van gesprekken te monitoren.
- Maak een test die het opgeslagen verzoek van een stap terugspeelt en vergelijkt met wat de client bouwde.
- Plaats tenant of plan als aparte metadata (zie de kaart over trace-labels); dit stuk gaat over de inhoud van het verzoek.

Waarom het werkt: je beantwoordt "wat zag het model op stap N" uit het log zelf, zonder de run te reproduceren.

Niet doen als: de inhoud persoonsgegevens bevat en je geen redactie of bewaartermijn hebt; leg dan alleen verwijzingen en hashes vast.

Toetsvraag: kun je voor een mislukte run per modelaanroep de exacte berichten, toolbeschrijvingen en parameters opvragen die zijn verstuurd?

Bronnen:
- open-telemetry/semantic-conventions-genai@ae8214a8f3a98786071736855093b74621174dc4 docs/gen-ai/client-inference.md:286 "order they were sent"
- open-telemetry/semantic-conventions-genai@ae8214a8f3a98786071736855093b74621174dc4 docs/gen-ai/client-inference.md:118 "gen_ai.input.messages"
- https://www.anthropic.com/engineering/multi-agent-research-system (gelezen 2026-11-23) "full production tracing"

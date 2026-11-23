# Een tracing-exporter houdt naast de officiele gen_ai.*-attributen een lijst framework-specifieke namen bij, want de officiele namen zijn nog geen universeel contract

Probleem: wie tracing bouwt op de aanname dat elk framework netjes de officiele OpenTelemetry GenAI-semantic-conventions (`gen_ai.input.messages`, enzovoort) stuurt, mist de input en output van frameworks die nog hun eigen attribuutnamen gebruiken.

Oplossing:
- Langfuse's span-exporter houdt een vaste set attribuutnamen aan om te bepalen welke span-attributen input of output zijn (`_media_field_for_attribute`; daar hangt de verwerking van ingebedde media aan, de exporter vertaalt de namen zelf niet): naast de officiele `gen_ai.input.messages` en `gen_ai.system_instructions` staan daar onder meer `ai.prompt` (Vercel AI SDK), `gcp.vertex.agent.llm_request` (Vertex), `mlflow.spanInputs`, `traceloop.entity.input`, en specifiek ook `pydantic_ai.all_messages`, de eigen attribuutnaam van pydantic-ai.
- pydantic-ai zelf optimaliseert die attribuut-opbouw met een per-run cache van al geserialiseerde berichten, zodat het samenstellen van die ene attribuut-waarde O(nieuwe berichten) kost in plaats van O(hele geschiedenis) bij elk request. Dat steunt wel op de afspraak dat een historisch bericht nooit in-place gemuteerd wordt na serialisatie.

Waarom het werkt: een exporter die zelf een lijst van bekende framework-attributen bijhoudt, blijft input en output vinden ook als de bronframeworks de officiele semconv-naam nog niet, of nog niet alleen, gebruiken.

Niet doen als: alle gebruikte frameworks sturen al uitsluitend de officiele gen_ai.*-attributen; dan is zo'n lijst overbodig.

Toetsvraag: herkent de tracingbackend ook een span van een framework dat zijn eigen, niet-officiele attribuutnaam gebruikt in plaats van gen_ai.*?

Bronnen:
- langfuse/langfuse-python@2cea520e240afb04fa03a617856c73142f9106b6 langfuse/_client/span_exporter.py:44 "pydantic_ai.all_messages"
- pydantic/pydantic-ai@d32d5c648bec67496dfcfb93803d257e6996d9c8 pydantic_ai_slim/pydantic_ai/_instrumentation.py:262 "O(new messages)"

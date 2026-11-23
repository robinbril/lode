# Een streaming-protocol naar de UI heeft twee lagen: ruwe token-deltas en typed events per RunItem

Probleem: een UI die alleen ruwe tekst-tokens ontvangt, kan niet netjes een losse tool-call-kaart, een handoff-notificatie of een reasoning-blok tonen; alles ziet eruit als platte tekst.

Oplossing:
- openai-agents-python stuurt twee lagen streaming-events (plus een `AgentUpdatedStreamEvent` bij een agentwissel): `RawResponsesStreamEvent` (de providerevents, ongewijzigd doorgegeven) en `RunItemStreamEvent`, die een `RunItem` draagt met een vaste `name` (`message_output_created`, `tool_called`, `tool_output`, `handoff_requested`, `reasoning_item_created`, `mcp_approval_requested`, enzovoort). De UI kan dus los van de tekst-stream op semantische momenten reageren.
- Bij meerdere gelijktijdige stream-pogingen (een fallback-hop of een retry die de stream herstart) moet maar één schrijver tegelijk naar de UI mogen pushen. Hermes-agent lost dat op met een single-writer fence: een nieuwe poging claimt een token via `claim_stream_writer`, en alleen een bewijsbaar overruilde oudere poging wordt gestopt; de fence faalt bewust open (geen fence) in plaats van een harde crash te geven als hij zelf niet beschikbaar is.

Waarom het werkt: de UI abonneert zich op typed lifecycle-momenten in plaats van tekst te moeten parsen, en een stale stream kan nooit per ongeluk nog delta's pushen nadat een nieuwere poging het overneemt.

Niet doen als: de UI toont alleen de uiteindelijke tekst na afloop, zonder tussentijdse tool-calls of reasoning te visualiseren; dan is een enkele tekst-stream genoeg.

Toetsvraag: kan de UI een tool-call-kaart tonen zonder de ruwe tekst-tokens te moeten parsen op zoek naar die tool-call?

Bronnen:
- openai/openai-agents-python@6c4e4a29cd08eef454db6980d74da6afc8939d24 src/agents/stream_events.py:24 "RunItemStreamEvent"
- NousResearch/hermes-agent@8da31006f3bcf70d0df05fb2b5a334eec4db2e07 agent/stream_single_writer.py:18 "claim_stream_writer"

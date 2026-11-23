# Een history-processor die de boodschappenlijst inkort, schrijft dat in-place terug naar de run: compactie is blijvend, niet eenmalig

Probleem: wie compactie implementeert als "stuur een ingekorte lijst alleen voor dit request" ziet de volle, ongekorte geschiedenis bij de volgende stap weer teruggroeien en betaalt dus elke stap opnieuw voor dezelfde context.

Oplossing:
- pydantic-ai's `ProcessHistory`-capability draait een history-processor voor elk modelrequest en zet het resultaat op twee plekken: `request_context.messages` (voor dit ene request) EN `ctx.messages[:] = messages` (de permanente message-lijst van de run, in-place). Een trim of samenvatting is dus blijvend voor de rest van de run, niet een eenmalige view.
- Hermes-agent combineert twee compactielagen voor modellen met server-side compactie (nu: gpt-5.6 op api.openai.com of de Codex-backend): de native `compact_threshold` wordt standaard het lokale compressor-trigger min `LOCAL_TRIGGER_SAFETY_MARGIN` (8192 tokens), en een expliciet ingestelde drempel wordt daar bovenaf op afgekapt. De provider compacteert dus altijd als eerste en de lokale compressor blijft alleen als fallback achter de hand.

Waarom het werkt: de compactie wordt eenmalig uitgevoerd en blijft hangen in de opgeslagen geschiedenis, en twee compactiemechanismen krijgen een vaste volgorde zodat ze elkaar niet allebei tegelijk proberen te triggeren.

Niet doen als: de conversatie is altijd kort genoeg om binnen het contextvenster te passen; dan voegt een compactielaag alleen complexiteit toe.

Toetsvraag: blijft een eerder uitgevoerde compactie staan bij de volgende beurt, of groeit de volle geschiedenis daarna weer terug?

Bronnen:
- pydantic/pydantic-ai@d32d5c648bec67496dfcfb93803d257e6996d9c8 pydantic_ai_slim/pydantic_ai/capabilities/process_history.py:38 "ctx.messages[:] = messages"
- NousResearch/hermes-agent@8da31006f3bcf70d0df05fb2b5a334eec4db2e07 agent/native_compaction.py:24 "LOCAL_TRIGGER_SAFETY_MARGIN"

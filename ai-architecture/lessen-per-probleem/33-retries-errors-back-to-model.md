# ModelRetry stuurt een fout terug als resultaat van precies die tool_call_id, de agent-loop telt losse one-shot guards per foutklasse

Probleem: een tool die bij een validatiefout simpelweg een generieke exception doorgooit, crasht de hele agent-run in plaats van het model de kans te geven zelf te herstellen; en een retry-teller zonder onderscheid tussen foutsoorten kan in een eindeloze lus belanden op dezelfde fout.

Oplossing:
- Een tool-functie die `ModelRetry(message)` opwerpt, laat pydantic-ai die fout niet als crash behandelen: de executor vangt `exceptions.ModelRetry` op en bouwt daaruit een retry-return die aan exact de `tool_call_id` van die call hangt, zodat het model de fout in de volgende beurt ziet als resultaat van zijn eigen tool-call, niet als een los systeembericht.
- Elke tool heeft een eigen `max_retries`; overschrijdt een call dat, dan stopt de run met een duidelijke fout in plaats van door te blijven proberen.
- Hermes-agent bouwt voor transport- en providerfouten een apart `TurnRetryState`-object per API-call-poging (`api_call_count`), met een los boolean-vlaggetje per foutklasse (`has_retried_429`, provider-auth-refresh, `thinking_sig_retry_attempted`, enzovoort): elke vlag mag maar één keer per poging aanslaan, zodat eenzelfde foutklasse niet in een lus blijft hangen terwijl een andere foutklasse in diezelfde poging nog wel een eigen herstelpoging krijgt.

Waarom het werkt: de fout komt terecht waar ze ontstond (bij de tool-call-ID voor het model, bij de specifieke foutklasse voor de transportlaag), dus herstel is gericht in plaats van een blinde algemene retry die andere foutsoorten meesleept.

Niet doen als: de fout is terminaal en het model kan er niets mee herstellen (bijvoorbeeld een permissiefout); gebruik dan `ToolFailed`: het model ziet de fout maar krijgt geen retry-instructie en het retry-budget van de tool wordt niet verbruikt.

Toetsvraag: ziet het model een tool-fout als resultaat van precies die tool-call, of als een los bericht dat het aan de verkeerde call kan toeschrijven?

Bronnen:
- pydantic/pydantic-ai@d32d5c648bec67496dfcfb93803d257e6996d9c8 pydantic_ai_slim/pydantic_ai/exceptions.py:82 "ModelRetry(Exception)"
- NousResearch/hermes-agent@8da31006f3bcf70d0df05fb2b5a334eec4db2e07 agent/turn_retry_state.py:13 "api_call_count"

# fallback_on filtert op response-inhoud, maar dat werkt niet bij een gestreamde aanvraag, en een fallback-hop moet zijn eigen request-overrides meenemen

Probleem: wie fallback alleen test op exceptions, mist een model dat wel antwoordt maar met een refusal of een afgekapt antwoord; en wie een fallback-hop simpelweg herstart met de routerdefaults, verliest de per-request fallback- en retry-instellingen van de oorspronkelijke aanvraag.

Oplossing:
- pydantic-ai's `FallbackModel` accepteert in `fallback_on` naast exceptions ook een response-handler, gedetecteerd via het type-hint op de eerste parameter. Maar: zo'n response-handler werkt alleen bij een niet-gestreamde aanvraag; bij een gestreamde aanvraag wordt de respons altijd geaccepteerd zoals die binnenkomt, omdat de finish_reason pas bekend is nadat de hele stream al is doorgegeven.
- litellm's router draagt per-request fallback- en retry-overrides expliciet door via een `MidStreamFallbackControls`-carrier, specifiek omdat de interne retry-wrapper die velden eerst van de kwargs aftrekt voor hij de pogingfunctie aanroept: zonder die drager zou een fallback-hop die halverwege een stream ontstaat, stilletjes terugvallen op de router-brede instellingen in plaats van de instellingen van het oorspronkelijke verzoek.

Waarom het werkt: fallback-logica die weet welke laag (stream versus niet-stream, verzoek versus router) de instellingen draagt, kan voorkomen dat een fallback-hop onopgemerkt andere regels gaat volgen dan de oorspronkelijke aanvraag.

Niet doen als: er is maar één model en geen streaming; dan is fallback-detectie op response-inhoud niet nodig.

Toetsvraag: valt een gestreamd verzoek met een afgekapt of geweigerd antwoord ook terug op het volgende model, of alleen een verzoek zonder streaming?

Bronnen:
- pydantic/pydantic-ai@d32d5c648bec67496dfcfb93803d257e6996d9c8 pydantic_ai_slim/pydantic_ai/models/fallback.py:102 "fallback_on"
- BerriAI/litellm@3e27fc2a88d2545a706fb9cc1a85ea99e474f18c litellm/router_utils/fallback_event_handlers.py:155 "MidStreamFallbackControls"

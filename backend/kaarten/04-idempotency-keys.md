# Een idempotency key is pas veilig als hij aan tenant, endpoint en een lock gebonden is

Probleem: een idempotency key die alleen de client-waarde als cache-key gebruikt, laat twee tenants met dezelfde zelfgekozen key elkaars gecachte antwoord zien. En twee gelijktijdige requests met dezelfde key kunnen de handler allebei starten voor de eerste klaar is.

Oplossing:
- Hash de cache-key uit drie delen: het auth-token (dus de tenant), de client-aangeleverde key en de url. Dezelfde key-waarde van twee klanten botst dan nooit.
- Zet eerst een kortlevende "Start"-lock atomisch (`set_if_not_exists`, in Svix 5 seconden). Een tweede, gelijktijdige request met dezelfde key ziet die lock en pollt elke 200 ms tot het eerste antwoord klaar is, in plaats van de handler opnieuw te draaien.
- Let op de grens: is de lock na meer dan de lock-TTL nog niet vervangen door een antwoord, dan zet de wachter de lock opnieuw en draait de handler alsnog. Een handler die langer duurt dan de TTL is dus niet beschermd; kies de TTL ruim of ververs hem.
- Bewaar het antwoord daarna voor een vaste periode (Svix: 12 uur), zodat een retry later het identieke antwoord terugkrijgt. Svix cachet alleen 2xx-antwoorden van POST-requests.

```rust
hasher.update(auth_token);
hasher.update(":");
hasher.update(key);
hasher.update(":");
hasher.update(url);
```

Waarom het werkt: de atomische lock dekt de race tussen twee gelijktijdige gelijke requests, en de samengestelde hash dekt de race tussen twee verschillende tenants die toevallig dezelfde key kiezen. Beide gaten mis je als je alleen "sla het antwoord op onder de key" implementeert.

Niet doen als: de operatie van nature al idempotent is (bijvoorbeeld een `upsert` op een natuurlijke key); dan voegt een idempotency-laag complexiteit toe zonder een nieuw gat te dichten.

Toetsvraag: kan twee tenants met dezelfde zelfgekozen idempotency key elkaars gecachte antwoord ooit terugkrijgen?

Bronnen:
- svix/svix-webhooks@c35d595bcb3de3ccecc4d2b49e98669c66c05a72 server/svix-server/src/core/idempotency.rs:65 "hasher.update(auth_token)"
- svix/svix-webhooks@c35d595bcb3de3ccecc4d2b49e98669c66c05a72 server/svix-server/src/core/idempotency.rs:171 "SerializedResponse::Start"

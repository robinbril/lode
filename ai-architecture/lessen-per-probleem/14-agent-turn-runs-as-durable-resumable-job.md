# De chatbeurt zelf draait als een durable job, de HTTP-request is slechts een kijkvenster

Probleem: als de LLM-beurt in dezelfde request-levenscyclus draait als de HTTP-call, verlies je de hele generatie zodra de browser-tab, load balancer of websocket breekt tijdens een lange tool-keten.

Oplossing:
- PostHog start een beurt als Temporal-workflow met een vast id per conversatie en `USE_EXISTING`: een tweede start koppelt aan de lopende workflow. Keerzijde: de invoer van die tweede start gaat verloren. Vervolgberichten gaan daarom door een wachtrij met een eigen workflow-id per bericht, en herverbinden mét een nieuw bericht geeft een fout.
- De activity heeft maximaal 3 pogingen, een limiet van 30 minuten en een heartbeat-timeout van 5 minuten. De heartbeat komt per stuk output: een tool die langer dan 5 minuten niets uitstuurt, loopt dus wel in de timeout. Stuur dan ACK-events die alleen de heartbeat voeden.
- Output gaat naar een Redis stream per conversatie (ongeveer 1000 berichten, TTL 30 minuten). `read_stream` kent een `start_id`, maar de executor geeft die niet mee: een herverbonden client krijgt de stream vanaf het begin, en de frontend moet dubbele berichten herkennen. Een afgebroken lezer laat de stream staan, een voltooide lezer ruimt hem op.
- De workflow blijft draaien als niemand kijkt; de stream is alleen het venster.

Waarom het werkt: het werk en de weergave hebben elk hun eigen herstelgedrag, dus een netwerkhik kost een herverbinding, geen herstart.

Niet doen als: je beurten zijn altijd binnen een paar seconden klaar; dan is de overhead van een workflow-engine niet terug te verdienen.

Toetsvraag: overleeft een lopende beurt het sluiten van de tab, en gaat een bericht dat tijdens die beurt binnenkomt niet verloren?

Bronnen:
- PostHog/posthog@9277b47 ee/hogai/core/executor.py:158 "WorkflowIDConflictPolicy.USE_EXISTING"
- PostHog/posthog@9277b47 ee/hogai/core/executor.py:254 "read_stream()"
- PostHog/posthog@9277b47 posthog/temporal/ai/chat_agent.py:322 "WorkflowIDConflictPolicy.USE_EXISTING"
- PostHog/posthog@9277b47 ee/hogai/stream/redis_stream.py:273 "start_id"

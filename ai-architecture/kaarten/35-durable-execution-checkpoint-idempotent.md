# Een durable step slaat zijn output op onder een stabiele sleutel, zodat replay na een crash een al voltooide stap niet opnieuw uitvoert

Probleem: een lange agent-taak die halverwege een tool-keten crasht en bij herstart alle stappen opnieuw draait, kan niet-idempotente acties (een betaling, een e-mail, een externe API-call) dubbel uitvoeren.

Oplossing:
- DBOS slaat bij elke step het resultaat op onder de sleutel (`workflow_id`, `function_id`, `step_name`), pas nadat de functie is teruggekeerd. Bij een replay checkt `check_operation_execution` eerst of die sleutel al een resultaat heeft; zo ja, dan wordt de step niet opnieuw uitgevoerd maar wordt het opgeslagen resultaat (of de opgeslagen fout) teruggegeven. Een crash tussen uitvoering en opslaan laat de step dus opnieuw draaien: de externe actie zelf heeft nog een eigen idempotency-sleutel nodig.
- Hatchet's durable `aio_wait_for` (wachten op een sleep of event binnen een task) gebruikt een `signal_key` die, als je er geen zelf meegeeft, automatisch wordt afgeleid uit de volgorde van de wait-aanroep binnen de taakrun: die volgorde-afgeleide sleutel is stabiel over replays zolang de wait-aanroepen in een vaste volgorde gebeuren, dus de Nde wait-aanroep krijgt bij een herstart dezelfde sleutel als voor de crash en wordt uit de historie opgelost in plaats van opnieuw aangeroepen.
- Beide systemen lossen hetzelfde probleem anders op: DBOS met een expliciete (workflow, functie, naam)-sleutel, Hatchet met een positie-afgeleide sleutel; de les is dat de checkpoint-sleutel per stap stabiel en reproduceerbaar moet zijn, niet op een timestamp of een willekeurig gegenereerde ID.

Waarom het werkt: voor een stap wordt uitgevoerd, wordt eerst gecheckt of er onder die sleutel al een resultaat staat, dus een voltooide stap wordt nooit herhaald; alleen een stap die midden in uitvoering crashte draait opnieuw.

Niet doen als: de tool-keten is kort genoeg om bij een crash gewoon helemaal opnieuw te beginnen zonder dat iets dubbel geraakt wordt.

Toetsvraag: heeft elke niet-idempotente actie in de keten een eigen idempotency-sleutel, ook al worden voltooide stappen na een crash uit de opslag teruggegeven?

Bronnen:
- dbos-inc/dbos-transact-py@28192bd87ee81891546803fb583ea6a22c08d1ce dbos/_core.py:2573 "check_operation_execution"
- hatchet-dev/hatchet@2a0b386361abbb0164b454b5cf24e668a671d101 sdks/python/hatchet_sdk/context/context.py:718 "signal_key"

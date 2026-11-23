# Een foutmelding aan het model vertelt niet alleen wat misging, maar of het mag herproberen

Probleem: een rauwe exception teruggeven aan het model laat het gokken of een nieuwe poging zin heeft; te vaak blind herproberen op een permissiefout is net zo erg als nooit herproberen op een verkeerd getypt argument.

Oplossing:
- De strategie hangt aan de exceptieklasse: `MaxToolFatalError` is `never`, `MaxToolTransientError` is `once` (één keer ongewijzigd), `MaxToolRetryableError` is `adjusted`. Los daarvan is er een `error_type` (`validation`, `permission`, `timeout`, `rate_limited`, `api_5xx` en meer) die de strategie niet bepaalt.
- De uitvoerder plakt de bijbehorende zin achter de foutmelding: één keer ongewijzigd opnieuw, of opnieuw met aangepaste invoer. Bij `never` is die zin leeg; het model ziet dan alleen de fout. Schrijf in eigen code ook daar een expliciete zin.
- Een permissiefout is een subklasse van de fatale fout en zegt in de melding zelf wat wel kan: de projectbeheerder vragen.
- Onbekende excepties gelden als fataal. De melding wordt afgekapt op 500 tekens voor ze de context ingaat.
- De zin is een advies aan het model; begrens het aantal pogingen ook in code.

Waarom het werkt: het model krijgt hetzelfde soort structuur die een mens ook zou willen bij een foutmelding: wat ging mis, en is dit het proberen waard.

Niet doen als: je tools altijd dezelfde, simpele fout teruggeven; dan is een vaste foutcategorie overkill.

Toetsvraag: vertelt elke toolfout het model expliciet of herproberen zin heeft, in plaats van alleen wat er misging?

Bronnen:
- PostHog/posthog@9277b47 ee/hogai/tool_errors.py:3 "MaxToolErrorType"
- PostHog/posthog@9277b47 ee/hogai/tool_errors.py:50 "retry_hint"
- PostHog/posthog@9277b47 ee/hogai/core/agent_modes/executables.py:517 "error.retry_hint"

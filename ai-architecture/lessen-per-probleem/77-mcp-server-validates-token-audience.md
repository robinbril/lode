# Een MCP-server accepteert alleen tokens die voor hem zijn uitgegeven, en die controle staat in de SDK's niet vanzelf aan

Probleem: een MCP-server accepteert elk geldig token en stuurt het door naar de CRM-API. Eén gestolen token opent dan elke dienst erachter, en het logboek van de CRM toont de verkeerde afzender.

Oplossing:
- Valideer bij elk verzoek dat het token voor deze server is uitgegeven (audience, het `resource` van RFC 8707). De spec zegt dat de server geen andere tokens mag accepteren of doorgeven.
- Doorsturen heet "token passthrough". Het omzeilt rate limits en controles die op de audience leunen, maakt auditen moeilijk en laat een gestolen token de server als doorgeefluik gebruiken.
- Naar de CRM gaat een eigen credential van de server, apart verkregen, nooit de Authorization-header van de aanroeper.
- Controleer wat jouw SDK standaard doet. De Python-SDK vergelijkt de token niet met `resource_server_url` zolang `validate_token_resource` niet is gezet (je krijgt wel een waarschuwing); in 3.0 wordt het standaard aan. Controleert je eigen verifier de audience al, zet hem dan bewust op False. In de TypeScript-SDK vergelijkt `requireBearerAuth` alleen als `expectedResource` is gezet, en de Express-adapter 2.0.1 geeft die optie niet door, zodat niets wordt vergeleken.
- Foute audience geeft 401 `invalid_token`; te weinig scope geeft 403 met `insufficient_scope` en alle scopes die deze ene operatie nodig heeft in één challenge (niet de hele catalogus). Geen wildcard-scopes.
- Een handle voor opgeslagen state is een naam, geen bewijs van identiteit: sla hem op onder de gebruiker uit het geverifieerde token.
- Schrijf een test die een token voor een andere audience stuurt en een 401 verwacht.

Waarom het werkt: de vertrouwensgrens van OAuth blijft heel, en elk verzoek is te herleiden tot één client en één gebruiker.

Niet doen als: de server alleen lokaal via stdio draait; de spec wil dan credentials uit de omgeving.

Toetsvraag: faalt een test met een token voor een andere audience, en kopieert geen codepad de binnenkomende Authorization-header naar een uitgaand verzoek?

Bronnen:
- https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization.md (gelezen 2026-11-23) "MUST NOT accept or transit"
- https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices.md (gelezen 2026-11-23) "Token Passthrough"
- modelcontextprotocol/python-sdk@77001c96f9507be0f4d009b83210a384a5e08bda src/mcp/server/auth/settings.py:48 "validate_token_resource"
- modelcontextprotocol/typescript-sdk@5ee54ee30ddc00a914a3d981880f87fdce0e6246 docs/serving/authorization.md:87 "expectedResource"

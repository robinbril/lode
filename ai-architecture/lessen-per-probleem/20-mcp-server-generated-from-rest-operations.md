# De MCP-server is geen los project, maar een opt-in laag over bestaande REST-operaties

Probleem: een MCP-server los bijhouden naast je REST-API en je chat-tools betekent drie plekken die hetzelfde "wat mag deze actie doen" opnieuw beschrijven, en drie plekken die uit de pas kunnen gaan lopen.

Oplossing:
- PostHog beschrijft elke MCP-tool in een YAML-bestand per product, gekoppeld aan een bestaande REST-operation-id (`operation: conversations_list`); een operatie wordt alleen als MCP-tool blootgesteld als er een entry voor staat die `enabled: true` zet. Bewust uit: `enabled: false` met een `disabled_reason`.
- Elke entry draagt zijn eigen API-`scopes` (zoals `conversation:read`) en annotaties (`readOnly`, `destructive`, `idempotent`), zodat een MCP-client vooraf weet of een aanroep veilig herhaald kan worden.
- Een los script somt operaties zonder entry op (`scaffold-yaml --candidates`) en kan er in één commando een toevoegen; het is dus bewust opt-in, nooit automatisch alles exposen.
- `response.include` is een allowlist van velden: de MCP-tool geeft een deelverzameling van de REST-respons terug.
- De YAML herhaalt wel scopes, veldnamen en beschrijving. Laat CI falen als een operatie-id of veld niet meer in het API-schema bestaat, anders loopt juist dat stuk uit de pas.

Waarom het werkt: uitvoering en rechten blijven bij de bestaande REST-operatie; de laag erboven kiest alleen wat zichtbaar is en hoe het heet.

Niet doen als: je MCP-server fundamenteel andere operaties nodig heeft dan je REST-API al biedt; dan is herschrijven eerlijker dan een dunne YAML-laag erover.

Toetsvraag: kan iemand een operatie als MCP-tool exposen zonder de onderliggende rechten-, veld- of RBAC-logica opnieuw te schrijven?

Bronnen:
- PostHog/posthog@9277b47 products/posthog_ai/mcp/tools.yaml:1 "Tools are opt-in"

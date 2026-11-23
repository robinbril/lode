# Elicitation voor geheimen gaat via een losse elicit_url, nooit via het gevalideerde formulier dat door het modelcontext loopt

Probleem: een MCP-tool die tijdens zijn uitvoering om een wachtwoord of API-key vraagt via het gewone, schema-gevalideerde elicitatie-formulier, laat dat antwoord via de MCP-client lopen, en die client kan een agent zijn die zelf een antwoord genereert.

Oplossing:
- De MCP Python SDK biedt `elicit_with_validation` voor formulier-elicitatie met schema-check (accept/decline/cancel), maar de docstring is expliciet: voor gevoelige data zoals credentials of OAuth-flows moet `elicit_url()` gebruikt worden. Dat is een los pad waarbij de mens een URL buiten de MCP-client om afrondt, zodat de data niet door de client of de LLM-context loopt; de server meldt daarna klaar met een `ElicitCompleteNotification`.
- Een client die formulier-elicitatie niet adverteert, moet niet gewoon falen. Hermes-agent's ACP-adapter (voor zijn `clarify`-vragen, dus niet voor geheimen) detecteert die steun uit de ruwe `initialize`-parameters, omdat de gepinde SDK's eigen `ClientCapabilities`-model dat veld laat vallen; zonder die steun degradeert de vraag naar een permission-kaart met de keuzes plus Skip, een interactie die elke ACP-client wel kan tonen.

Waarom het werkt: geheimen lopen niet door het formulier-pad via de client, en een client zonder formulier-elicitatie krijgt een werkend alternatief in plaats van een harde fout.

Niet doen als: de gevraagde informatie is nooit gevoelig (een voorkeur, een los antwoord); dan is het gewone formulier-elicitatiepad voldoende.

Toetsvraag: vraagt de tool credentials of tokens uitsluitend via een out-of-band URL en niet via het formulier-elicitatiepad?

Bronnen:
- modelcontextprotocol/python-sdk@77001c96f9507be0f4d009b83210a384a5e08bda src/mcp/server/elicitation.py:117 "elicit_url()"
- NousResearch/hermes-agent@8da31006f3bcf70d0df05fb2b5a334eec4db2e07 acp_adapter/elicitation.py:20 "ClientCapabilities"

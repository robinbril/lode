# Een tool-beschrijving is een prompt: zeg wanneer, wanneer juist niet, en welke zustertool je dan nodig hebt

Probleem: twee tools die op elkaar lijken, of een parameter die "file" heet, laten het model raden. Het kiest de verkeerde tool of verzint een relatief pad.

Oplossing:
- Schrijf de beschrijving alsof je de tool aan een nieuwe collega uitlegt: wat hij doet, wanneer je hem gebruikt, wat hij teruggeeft en welke beperking geldt.
- Verwijs naar de zustertool: de list-tool van de filesystem-server zegt dat je voor groottes `list_directory_with_sizes` neemt en voor een recursief beeld `directory_tree`.
- Zet de regel die voor elke parameter van één soort geldt op één plek en hang hem aan elke beschrijving vast. De server doet dat met een gedeelde `PATH_RULE`, omdat een model dat alleen "het bestand" leest naar paden en de sandbox gokt.
- Geef parameters ondubbelzinnige namen: `user_id` in plaats van `user`.
- Gebruik namespaces voor duidelijke grenzen en laat de aanroeper kiezen tussen een beknopt en een uitgebreid antwoord.
- Begrens de output (in Claude Code standaard 25.000 tokens) en laat fouten zeggen wat je daarna moet veranderen.
- Meet elke wijziging: schrijf evaluatietaken met een controleerbaar antwoord en draai ze voor en na de nieuwe tekst. Kleine verfijningen geven vaak grote verschillen.

Waarom het werkt: het model heeft alleen deze tekst om te kiezen, dus elke dubbelzinnigheid wordt een foutkans, en een verwijzing naar de buurtool voorkomt dat twee gelijkende tools elkaar bijten.

Niet doen als: je maar één tool met één parameter hebt; dan is een korte zin genoeg.

Toetsvraag: noemt elke tool met een gelijkende buur die buur bij naam, en is de laatste tekstwijziging met een eval gemeten?

Bronnen:
- modelcontextprotocol/servers@c799c8552b0f27b7a33a7b9233773da144dddcf5 src/filesystem/server.ts:57 "PATH_RULE"
- modelcontextprotocol/servers@c799c8552b0f27b7a33a7b9233773da144dddcf5 src/filesystem/server.ts:705 "directory_tree"
- https://www.anthropic.com/engineering/writing-tools-for-agents (gelezen 2026-11-23) "new hire"

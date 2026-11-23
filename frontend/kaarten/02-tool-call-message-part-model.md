# Een tool call is een eigen entiteit met eigen status, niet een stuk tekst in het antwoord

Probleem: een chat-UI die een tool call als platte tekst in de message meestuurt kan geen eigen laad-, fout- of "wacht op jou"-status tonen voor alleen dat ene stukje.

Oplossing:
- Model een message als een lijst van parts; een tool-call part heeft een eigen `toolCallId`, `toolName`, `args` plus de ruwe `argsText`-buffer, een optionele `result` en `isError`, los van de tekst-parts ervoor en erna.
- In ag-ui bindt `tool_call_id` de events start, args, end en result aan elkaar. Het resultaat mint een nieuw tool-bericht met een eigen `message_id`; het plakt niet aan het assistant-bericht.
- Status is geen boolean maar een klein union: `requires-action` (reden `tool-calls` of `interrupt`), `running`, `incomplete` (met reden) en `complete`. Daarmee toont de UI "deze ene tool call heeft een mens nodig" zonder de rest van het gesprek te blokkeren.
- assistant-ui geeft die status aan de renderer van het part; het part zelf draagt de gegevens waaruit hij volgt, zoals `result` en een `interrupt`-payload voor menselijke invoer.

Waarom het werkt: de UI kan per part een losse skeleton, spinner of actieknop renderen omdat de databron al per call bijhoudt waar die staat, in plaats van dat de UI uit de tekst moet raden of een call nog loopt.

Niet doen als: je alleen een eenmalige, niet-interactieve samenvatting toont, dan is een losse part-status overkill.

Toetsvraag: kan de UI per tool call, los van de omliggende tekst-parts, bepalen of die loopt, op een mens wacht, mislukte of klaar is?

Bronnen:
- ag-ui-protocol/ag-ui@c31e1e819e3a sdks/typescript/packages/proto/src/proto/events.proto:208 "ToolCallResultEvent"
- assistant-ui/assistant-ui@8227544705c6 packages/core/src/types/message.ts:487 "requires-action"
- assistant-ui/assistant-ui@8227544705c6 packages/core/src/types/message.ts:374 "interrupt"

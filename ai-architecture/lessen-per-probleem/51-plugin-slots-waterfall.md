# Plugin-slots zijn genaamde waterfall-events met een gesloten besluit-type, nooit een losse boolean

Probleem: een plugin die "voor elke tool-aanroep" mag ingrijpen krijgt vaak alleen een `beforeCall(args) => boolean`. Dat kan een call weigeren, maar niet uitleggen waarom, niet om bevestiging vragen, en niet de resultaat-kant raken.

Oplossing:
- Elk haakpunt is een genaamd event (`tools/pre-execute`, `tools/post-execute`, `system-prompt/assemble`) waarop meerdere plugins na elkaar een `next()`-keten doorlopen (Cordis-waterfall).
- Het besluit is een gesloten union, geen boolean: `PreToolDecision = allow | deny{reason} | cancel | ask{reason, displayReason}`. Een plugin kan dus niet alleen blokkeren maar ook een reden en een lokaliseerbare prompt-tekst meegeven.
- `PostToolDecision` kan het resultaat ook vervangen (`accept{content|value}`) of terugkoppelen als correctie naar het model (`block{feedback}`), in plaats van alleen "doorgaan of niet".
- `ask` zonder goedkeuringsdienst wordt een weigering. Argumenten herschrijven kan bewust niet: ze zijn al gelogd en getoond.
- Default bij geen enkele plugin: `allow` voor pre, `accept` voor post.
- In een waterfall kan een listener het besluit van `next()` vervangen, dus ook een `deny` door een `allow`. Harde regels horen daarom in een aparte `ToolGuard` die na alle listeners draait en alleen kan weigeren; de volgorde van plugins doet er dan niet toe.

```ts
// eigen schets: eerst de keten (een ask is dan al beantwoord), dan guards die alleen nee kunnen zeggen
const besluit = await keten("tools/pre-execute", call, async () => ({ kind: "allow" }));
const nee = besluit.kind === "allow" ? guards.map((g) => g(call)).find(Boolean) : besluit;
```

Waarom het werkt: het event-brede contract dwingt elke plugin-auteur om in dezelfde vier mogelijke uitkomsten te denken, dus een UI die het besluit toont (toast, approval-kaart) hoeft maar één renderpad te hebben voor alle plugins samen.

Niet doen als: je maar één plugin per event ooit zal hebben; dan is een enkele synchronous callback simpeler dan een waterfall-ketting optuigen.

Toetsvraag: staat elke harde weigering in een laag die alleen kan weigeren, zodat een tweede plugin een `deny` niet kan omzetten in een `allow`?

Bronnen:
- deepseek-ai/deepseek-harness@4b399c39a6d1479cd84ca591b4d7c88e24d38a96 packages/core/tools/src/contracts.ts:375 "PreToolDecision"
- deepseek-ai/deepseek-harness@4b399c39a6d1479cd84ca591b4d7c88e24d38a96 packages/core/tools/src/contracts.ts:386 "PostToolDecision"
- deepseek-ai/deepseek-harness@4b399c39a6d1479cd84ca591b4d7c88e24d38a96 packages/core/tools/src/pipeline.ts:214 "checkGuards"

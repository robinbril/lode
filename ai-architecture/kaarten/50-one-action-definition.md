# Eén `defineAction`-definitie bedient tool-call, HTTP, frontend, MCP, A2A en CLI

Probleem: vier losse implementaties van "dezelfde" operatie (een REST-route, een agent-tool, een MCP-tool, een UI-knop) lopen na een paar maanden uit de pas: de een valideert iets anders, de een vraagt goedkeuring, de ander niet.

Oplossing:
- Eén `defineAction({...})`-object per operatie. Het schema, de handler (`run`) en de error-codes zijn eenmalig gedefinieerd.
- Elke aanroeper wordt onderscheiden via een vast gesloten type `ActionCaller`: `tool | http | frontend | mcp-widget | mcp-widget-write | cli | mcp | webmcp | a2a | automation`. Geen vrije string, dus een nieuwe aanroeper is een compileerfout tot hij bewust is toegevoegd.
- Autorisatie (`authorize`) is één gate die vóór `run()` draait op **elke** aanroeper, dus nooit per-transport opnieuw geschreven. De gate wikkelt `run` zelf in en vervangt de rijfilters niet: welke rijen je mag zien blijft een aparte check.
- Approval (`needsApproval`) is een los concept: één functie beslist voor agent-loop, MCP en HTTP. Gooit het predicaat een fout, dan wordt er gevraagd (fail-closed). Een no-approvals-modus zet de vraag uit, `authorize` blijft dan gelden.

```ts
// eigen schets
defineAction({
  schema,
  authorize: mustBe("recruiter"),
  needsApproval: (args) => args.ontvangers.length > 0,
  run: async (args, ctx) => verstuur(args, ctx.caller),
});
```

Waarom het werkt: de handler kan niet "per ongeluk" een transport overslaan, want er is geen tweede handler om te vergeten. Een gate die op de actie zelf hangt (niet op de dispatcher) werkt ook nog als een nieuwe dispatcher erbij komt.

Niet doen als: je transporten fundamenteel andere semantiek nodig hebben (bijv. streaming vs. request/response) die niet in één `run`-signatuur past; dan is een adapter per transport eerlijker dan één functie die overal om heen bouwt.

Toetsvraag: kan een nieuwe aanroeper (bijv. een tweede MCP-server) deze actie bellen zonder dat iemand `authorize` opnieuw moet schrijven?

Bronnen:
- BuilderIO/agent-native@21c90bdff1e0f48ed8ff56d8551ea4660d388b76 packages/core/src/action.ts:183 "ActionCaller"
- BuilderIO/agent-native@21c90bdff1e0f48ed8ff56d8551ea4660d388b76 packages/core/src/action.ts:1454 "ActionAuthorize"

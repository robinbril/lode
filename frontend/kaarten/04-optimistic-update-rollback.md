# Een optimistische update is een tijdelijke laag over de echte staat, geen directe schrijfactie

Probleem: een naïeve optimistische update schrijft meteen in de echte state en moet bij een mislukte server-call handmatig terug worden gedraaid; vergeet je een pad, dan blijft de UI liegen.

Oplossing:
- Houd de "echte" waarde (`baseValue`) en de getoonde waarde (`value`) apart. De getoonde waarde is `baseValue` plus alle nog-lopende transformaties, opnieuw berekend bij elke wijziging.
- Een lopende call voegt zichzelf toe aan een lijst van pending transforms (`execute`, `optimistic`, optioneel `loading` en `then`); de weergave leest die lijst, schrijft er nooit blijvend in.
- Zodra de call eindigt (succes of fout), haal je hem in een `finally` uit de pending-lijst. Bij succes wordt `optimistic` (en `then`) alsnog op `baseValue` toegepast; bij een fout gebeurt er niets, dus er is niets terug te draaien.
- Elke transform krijgt een volgnummer (`order`), zodat gelijktijdige acties in registratievolgorde boven elkaar blijven liggen.
- Een geslaagde `optimistic` blijft over een nieuwe `baseValue` herspeeld worden zolang er nog een andere call loopt. Zulke functies moeten daarom idempotent zijn.
- Bij een reset telt een `epoch`-teller op, zodat een call die nog onderweg is niet in de vervangende state schrijft.

```ts
// eigen vereenvoudiging, niet overgetypt
function view(base, pending) {
  return pending.reduce((s, t) => t.optimistic(s), base)
}
```

Waarom het werkt: "terugdraaien" is geen aparte operatie meer, het is simpelweg het stoppen met meetellen van een transform die toch nooit in de echte state stond.

Niet doen als: de server-call bijna altijd binnen een paar honderd milliseconden slaagt en een foutstatus toch een volledige herlaad triggert; dan is de complexiteit niet de moeite.

Toetsvraag: kan een mislukte actie de getoonde staat laten afwijken van de laatst bevestigde staat zonder dat er expliciete "undo"-code draait?

Bronnen:
- assistant-ui/assistant-ui@8227544705c6 packages/core/src/runtimes/remote-thread-list/optimistic-state.ts:130 "optimisticUpdate"
- assistant-ui/assistant-ui@8227544705c6 packages/core/src/runtimes/remote-thread-list/optimistic-state.ts:179 "finally"
- assistant-ui/assistant-ui@8227544705c6 packages/core/src/runtimes/remote-thread-list/optimistic-state.ts:55 "idempotent"

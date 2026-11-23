# Een goedkeuringskaart in de chat kent precies één acceptabel antwoord per vraag

Probleem: een gebruiker klikt twee keer snel op "toestaan", of de kaart blijft klikbaar nadat het antwoord al onderweg is, en de agent krijgt een dubbel of tegenstrijdig signaal.

Oplossing:
- Zet de kaart in een "wacht"-staat zodra de eerste klik vertrekt (ref plus `disabled` en `aria-busy` op de knoppen); een tweede klik wordt genegeerd zolang die staat aan staat.
- Geef elke vraag een eigen id en laat het antwoord daarnaar verwijzen. In ag-ui antwoordt een resume-entry op een `Interrupt` via diens `id`; `tool_call_id` is optioneel en alleen gezet bij een tool-goedkeuring. De deepseek-kaart krijgt per vraag een `key` en begint dus met schone state.
- Laat de vraag een antwoord-schema meesturen (ag-ui: `response_schema`, een JSON Schema) in plaats van alleen ja/nee, zodat dezelfde kaart ook een keuze of een vrij veld kan tonen.
- Enter bevestigt, Escape wijst af, maar niet bij een modifier, niet bij `event.repeat`, niet in een invoerveld en niet als Enter op een knop of link staat (dat is dan die knop). Tijdens een IME-compositie negeer je de toets: let op `compositionstart/end`, `isComposing` en `keyCode === 229`, en houd de vlag tot de eerstvolgende keyup omdat Safari de keydown na `compositionend` stuurt.

```ts
// eigen vereenvoudiging, niet overgetypt
let waiting = false
function answer(send: () => Promise<void>) {
  if (waiting || !canAnswer()) return
  waiting = true
  send().catch(() => { if (canAnswer()) waiting = false })
}
```

Waarom het werkt: de kaart wordt pas weer klikbaar als het antwoord mislukt is en de vraag nog steeds open staat; na succes blijft hij vergrendeld tot de aanroeper de vraag afsluit of vervangt.

Niet doen als: de actie direct en zonder gevolgen omkeerbaar is (zoals een like); dan is een simpele toggle genoeg.

Toetsvraag: kan een gebruiker door snel dubbelklikken twee tegenstrijdige antwoorden naar de agent sturen?

Bronnen:
- deepseek-ai/deepseek-harness@4b399c39a6d1 packages/client/ui-approval/src/client/ApprovalCard.tsx:31 "canAnswer"
- deepseek-ai/deepseek-harness@4b399c39a6d1 packages/client/ui-approval/src/client/ApprovalCard.tsx:50 "compositionEnded.current"
- ag-ui-protocol/ag-ui@c31e1e819e3a sdks/typescript/packages/proto/src/proto/types.proto:290 "tool_call_id"

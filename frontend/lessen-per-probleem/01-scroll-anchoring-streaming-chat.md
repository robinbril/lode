# Een chat-viewport volgt de bodem alleen zolang niemand omhoog heeft gescrold

Probleem: een LLM laat de viewport bij elke nieuwe token naar beneden springen, ook als de gebruiker net omhoog scrolde om een eerdere regel te lezen.

Oplossing:
- Houd twee waarden bij: `followBottom` (moet de lijst meegroeien) en `isAtBottom` (gemeten, stuurt de "naar beneden"-knop). assistant-ui houdt ze bewust apart; `isAtBottom` wordt tijdens een lopende neerwaartse scroll niet bijgewerkt.
- `followBottom` gaat uit in de scroll-handler, niet in de wheel-handler: scrollTop daalt terwijl scrollHeight niet kleiner werd. Een krimpende inhoud laat de browser scrollTop zelf verlagen en telt dus niet als omhoog scrollen.
- `followBottom` gaat weer aan zodra de gebruiker de bodem raakt, en bij een expliciete `scrollToBottom`.
- Wheel-up, touchmove omlaag en toetsen (ArrowUp, PageUp, Home, Shift+Spatie) zetten alleen een `upwardInput`-signaal van twee animatieframes en annuleren een nog geplande scroll-naar-bodem. Een geneste scroller die zelf nog omhoog kan telt niet mee.
- Bij een resize van de inhoud scrolt `followGrowth` met `behavior: "instant"` mee, alleen als `followBottom` aan staat en het volgen niet gepauzeerd is (uitklappen van een disclosure pauzeert het).

```ts
// eigen vereenvoudiging, niet overgetypt
let follow = true, lastTop = 0, lastHeight = 0
el.addEventListener('scroll', () => {
  const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 1
  if (atBottom) follow = true
  else if (el.scrollTop < lastTop && el.scrollHeight >= lastHeight) follow = false
  lastTop = el.scrollTop; lastHeight = el.scrollHeight
})
new ResizeObserver(() => { if (follow) el.scrollTo({ top: el.scrollHeight, behavior: 'instant' }) }).observe(content)
```

Waarom het werkt: groei van de inhoud laat de afstand tot de bodem toenemen zonder dat scrollTop daalt; alleen een echte opwaartse scroll doet scrollTop dalen, dus de twee gevallen zijn uit elkaar te houden.

Niet doen als: de lijst zelf virtualised is, dan hoort de anchor-logica bij de virtualizer (zie les 08), niet bij de scrollcontainer.

Toetsvraag: blijft de viewport staan als de gebruiker omhoog scrolt terwijl de inhoud blijft groeien, en volgt hij weer zodra de bodem is bereikt?

Bronnen:
- assistant-ui/assistant-ui@8227544705c6 packages/store/src/utils/thread-viewport-auto-scroll.ts:275 "followGrowth"
- assistant-ui/assistant-ui@8227544705c6 packages/store/src/utils/thread-viewport-auto-scroll.ts:248 "followBottom = false"
- vercel/ai-elements@ca8be600bfd0 packages/elements/src/conversation.tsx:78 "isAtBottom"

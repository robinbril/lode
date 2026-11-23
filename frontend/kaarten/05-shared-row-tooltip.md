# Eén tooltip voor een hele rij iconen, niet één tooltip per knop

Probleem: elke knop in een rij actie-iconen (kopieer, reageer, meer) zijn eigen tooltip laten renderen geeft bij snel over de rij bewegen een lelijke flits van losse tooltips die elk opnieuw in- en uitfaden.

Oplossing:
- Render één tooltip-bubble per rij (via een portal naar `document.body`), niet één per trigger.
- Houd een gedeelde context met `aim(anchor, label)` en `hide()`; elke knop roept `aim` aan op hover of focus, de rij roept `hide` aan bij muis weg of focus die de rij verlaat. De bubble tekent alleen het laatst doorgegeven label.
- Meet de breedte van het label met een verborgen meetelement, zodat de bubble meteen de juiste maat en positie krijgt.
- Bij de eerste verschijning (bubble nog dicht): zet `data-hold`, schrijf positie en breedte, lees `offsetWidth` om een reflow te forceren en verwijder `data-hold`. In de CSS zet `[data-hold]` de `transition` op `none`.
- Bij verplaatsen tussen twee al-zichtbare triggers schrijf je de positie zonder hold: de transition op `translate` en `width` loopt en geeft de glijbeweging.
- Bij scroll of resize herplaats je met dezelfde hold-reflow-truc, zodat de bubble zijn anker direct volgt.

```ts
// eigen vereenvoudiging, niet overgetypt
function moveInstant(el, x, y) {
  el.dataset.hold = 'true'
  el.style.translate = `${x}px ${y}px`
  void el.offsetWidth // forceer reflow
  delete el.dataset.hold
}
```

Waarom het werkt: met `transition: none` en een reflow vóór het weghalen van de hold wordt de nieuwe positie zonder animatie vastgelegd; pas daarna animeren volgende wijzigingen weer.

Niet doen als: de rij maar twee of drie knoppen heeft en de tooltips nooit overlappen; dan is de extra state het niet waard.

Toetsvraag: springt de tooltip instant naar zijn eerste positie, maar glijdt hij tussen twee al-zichtbare triggers?

Bronnen:
- kvnkld/aicss@7f9dc408ec11 packages/react/src/message-actions/MessageActions.tsx:103 "bubble.offsetWidth"
- kvnkld/aicss@7f9dc408ec11 packages/react/src/message-actions/MessageActions.tsx:142 "dataset.hold"
- kvnkld/aicss@7f9dc408ec11 packages/react/src/message-actions/MessageActions.module.css:113 "data-hold"

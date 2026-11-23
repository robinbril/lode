# Een laag die op pointerdown opent luistert pas een tick later naar klikken buiten zichzelf

Probleem: een menu opent op pointerdown van een knop; die pointerdown bubbelt door naar de documentlistener die "klik buiten" detecteert, en het menu sluit zichzelf in dezelfde interactie weer.

Oplossing:
- Registreer de document-`pointerdown`-listener pas in een `setTimeout(0)` nadat de laag is gemount. Radix doet dat zo, met in de code de uitleg dat een listener die tijdens een pointerdown wordt toegevoegd diezelfde event nog ontvangt.
- Optioneel (Radix `deferPointerDownOutside`, standaard uit): wacht na een pointerdown op de bijbehorende `click` voor je "buiten" meldt, alleen voor de primaire knop. Capture-listeners markeren pointerup, mousedown, mouseup, touchstart, touchend en click als onderschept; haalt zo'n event de bubble-fase niet (een derde roept `stopPropagation` aan), dan vervalt het sluiten.
- Dat wachten dekt ook een pointerdown zonder click (scroll, slepen, lang indrukken): bij elke nieuwe pointerdown wordt de vorige click-listener verwijderd.
- Alleen de bovenste laag uit de stapel luistert naar Escape (`isHighestLayer`).
- Een Escape tijdens een IME-compositie hoort bij die compositie: controleer `isComposing` én `keyCode === 229`, want Safari stuurt hem na `compositionend` met `isComposing: false`.

Waarom het werkt: de pointerdown die de laag opende bereikt de nieuwe listener niet meer, en wie extern wil kunnen annuleren krijgt via het click-moment een venster om dat te doen.

Niet doen als: de laag alleen met een expliciete sluitknop dicht gaat en geen buiten-klik-gedrag nodig heeft.

Toetsvraag: sluit een knop die een menu opent dat menu per ongeluk weer in dezelfde klik?

Bronnen:
- radix-ui/primitives@eb3a2b709129 packages/react/dismissable-layer/src/dismissable-layer.tsx:511 "window.setTimeout"
- radix-ui/primitives@eb3a2b709129 packages/react/dismissable-layer/src/dismissable-layer.tsx:454 "deferPointerDownOutside"
- radix-ui/primitives@eb3a2b709129 packages/react/dismissable-layer/src/dismissable-layer.tsx:175 "isComposing"
- radix-ui/primitives@eb3a2b709129 packages/react/dismissable-layer/src/dismissable-layer.tsx:154 "isHighestLayer"

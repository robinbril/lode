# Een gevirtualiseerde chatlijst corrigeert de scrollpositie alleen voor items volledig boven de rand

Probleem: een streamend chatbericht dat onderaan groeit (de bodem van het bericht komt onder de rand van het scherm) laat een virtualizer die simpelweg "itemhoogte veranderd, dus scrollTop aanpassen" toepast de hele viewport naar onder slepen, elke keer dat er een nieuw stukje tekst bijkomt.

Oplossing:
- Meet de echte hoogte van elk item na render (ResizeObserver) en cache die per item-key naast de geschatte hoogte; een item zonder cache-entry is "eerste meting".
- Bij een eerste meting (schatting naar echt): corrigeer de scrollpositie voor elk item waarvan de start boven de scroll-offset ligt (`itemStart < scrollOffset`), richting ongeacht.
- Bij een hermeting van een al bekend item: corrigeer alleen als het item volledig boven de scroll-offset eindigt (`itemStart + itemSize <= scrollOffset`). Een item dat de rand overspant groeit onder het ankerpunt; corrigeren zou de viewport bij elke groei naar beneden slepen.
- Pas de correctie bovendien niet toe terwijl de scrollrichting `backward` is, anders ontstaat een cascade van "items springen terwijl ik omhoog scrol". Ook niet tijdens een smooth scroll.
- Schrijf scrollTop en render de verschoven items in hetzelfde frame, anders schildert de browser één frame met de nieuwe scrollTop en de oude posities.
- Staat de lijst al aan het einde (modus `anchorTo: 'end'`), dan corrigeert de virtualizer met de verandering van de totale grootte in plaats van met de itemdelta.

Waarom het werkt: het ankerpunt (de bovenrand van de viewport) blijft optisch stil, omdat alleen groei die zich volledig boven dat punt afspeelt de scrollpositie mag verschuiven; groei van een item dat de rand overspant gebeurt eronder.

Niet doen als: alle items een vaste, vooraf bekende hoogte hebben; dan is er niets te meten of te corrigeren.

Toetsvraag: springt de viewport als het laatste, deels zichtbare bericht verder groeit terwijl de gebruiker net iets erboven leest?

Bronnen:
- TanStack/virtual@ec46ffc40078 packages/virtual-core/src/index.ts:2151 "scrollDirection"
- TanStack/virtual@ec46ffc40078 packages/virtual-core/src/index.ts:2142 "itemStart"
- TanStack/virtual@ec46ffc40078 packages/virtual-core/src/index.ts:2130 "anchorTo"

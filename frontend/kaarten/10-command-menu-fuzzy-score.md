# Een command-menu scoort met vaste factoren en sorteert door DOM-nodes te verplaatsen

Probleem: een command-menu waarvan de items door de consument worden aangeleverd, moet na elke toetsaanslag filteren en herordenen zonder dat de lijst opnieuw wordt opgebouwd, en met een typefout die een resultaat lager zet in plaats van weg te halen.

Oplossing:
- Score elke match met vermenigvuldigende factoren: doorlopende match 1, woordsprong na een spatie of streepje 0,9, na een ander scheidingsteken (slash, underscore, punt) 0,8, losse tekensprong 0,17.
- Kleine straffen per overgeslagen teken (0,999), per hoofdlettermismatch (0,9999) en voor een onvolledige match (0,99), zodat de volgorde stabiel blijft.
- Een getransponeerd paar letters krijgt factor 0,1: een sterke straf, maar de match blijft bestaan (score groter dan 0) en dus zichtbaar.
- Filter eerst (score groter dan 0 blijft), sorteer dan losse items op score en verplaats ze met `appendChild` (een bestaande node wordt verplaatst, niet opnieuw aangemaakt). Zet daarna groepen op hun hoogste itemscore.
- Het zoekveld houdt de echte focus; de selectie is `aria-selected` plus `aria-activedescendant`. Na elke zoekwijziging wordt het eerste item geselecteerd.

Waarom het werkt: de items blijven gemount en de consument hoeft zijn kinderen niet te herordenen. Omdat `appendChild` een node eerst verwijdert, kan een node met echte focus die kwijtraken; daarom staat de focus in het input.

Niet doen als: je de lijst zelf rendert uit een array; sorteer dan die array en laat het framework (keyed) de volgorde bepalen.

Toetsvraag: staat de echte focus in het zoekveld en komt een item met een typefout lager te staan in plaats van te verdwijnen?

Bronnen:
- pacocoursey/cmdk@dd2250ed6084 cmdk/src/command-score.ts:19 "SCORE_TRANSPOSITION"
- pacocoursey/cmdk@dd2250ed6084 cmdk/src/index.tsx:412 "appendChild"
- pacocoursey/cmdk@dd2250ed6084 cmdk/src/index.tsx:814 "aria-activedescendant"

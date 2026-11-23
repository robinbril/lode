# "Alles selecteren" is een losse waarde 'all', geen verzameling van elk rij-id

Probleem: een tabel die "selecteer alles" bijhoudt als een Set van elk id, moet bij duizenden rijen die hele Set opbouwen en vergelijken terwijl een gebruiker alleen "alles" bedoelt.

Oplossing:
- Laat de geselecteerde-sleutels-staat twee vormen aannemen: een Set met id's, of de losse waarde `'all'`. `selectAll()` zet alleen die waarde.
- `isSelected` test eerst op `'all'` en vraagt dan alleen of het item selecteerbaar is (niet uitgeschakeld); er wordt geen Set opgebouwd.
- Geef de consument de ruwe waarde (`rawSelection`, "'all' of een set") naast `selectedKeys`, dat 'all' wel uitschrijft tot de sleutels van de collectie.
- Let op wat er daarna gebeurt: een toggle na 'all' schrijft alle sleutels van de collectie uit en haalt die ene weg; een shift-uitbreiding na 'all' begint opnieuw met alleen dat ene item. Een "alles behalve"-uitzonderingslijst bestaat hier niet; bouw die zelf als 'all' ook ongeladen rijen moet dekken.
- Op aanraakschermen of met een virtuele cursor (schermlezer, `pointerType` `touch` of `virtual`) ontbreken modifier-toetsen; gebruik daar toggle-per-klik in plaats van vervangen of uitbreiden.

Waarom het werkt: 'all' zetten en lezen is O(1) en `isSelected` blijft dat; pas bij een wijziging van die ene rij, of als iemand `selectedKeys` leest, kost het werk evenredig aan de collectie.

Niet doen als: de tabel een vaste, kleine, volledig geladen dataset toont; dan is een gewone Set eenvoudiger en net zo correct.

Toetsvraag: bouwt "alles selecteren" bij duizend rijen geen Set op en leest `isSelected` de sentinel eerst?

Bronnen:
- adobe/react-spectrum@6be3466d87cc packages/react-stately/src/selection/SelectionManager.ts:432 "setSelectedKeys"
- adobe/react-spectrum@6be3466d87cc packages/react-stately/src/selection/SelectionManager.ts:339 "getSelectAllKeys"
- adobe/react-spectrum@6be3466d87cc packages/react-stately/src/selection/SelectionManager.ts:472 "pointerType"

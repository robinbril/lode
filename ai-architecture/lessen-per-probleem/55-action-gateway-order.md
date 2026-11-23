# De action-gateway doet resolve, dan policy, dan schrijven, in die vaste volgorde en nooit andersom

Probleem: als een agent eerst handelt en dan pas logt, bestaat er een venster waarin een actie is uitgevoerd maar nergens staat. Als de policy een label van het model vertrouwt in plaats van de eigen snapshot, kan "nooit op Submit klikken" omzeild worden door een ander label op dezelfde knop te plakken.

Oplossing: drie stappen, strikt in deze volgorde, in één functie die de enige weg naar uitvoering is:
1. **Resolve**: de ref die de aanroeper stuurde wordt opgezocht in de server-eigen snapshot, nooit in wat de aanroeper zelf beweert dat het is.
2. **Decide**: de policy wordt gevraagd. Deny wint altijd van allow; een afwezige policy of een kapotte regel weigert (fail-closed, niet fail-open).
3. **Record, then act**: de rij wordt geschreven voor de actie draait, hoe de beslissing ook uitpakt. Bij een goedkeuringsvraag wordt pas geschreven op het moment dat de mens antwoordt (refused bij weigering, attempted bij toestemming).

De attempt- en de failure-rij delen bewust dezelfde `attempt`-id (een UUID), zodat een falende actie terug te vinden is naast zijn eigen poging. Een poging zonder tweede rij is geen bewijs van succes: valt het proces weg, dan is de uitkomst onbekend.

Reikwijdte in de bron: acties op een pagina, bestand of shell. Beheer van de computer zelf (bijwerken) schrijft zijn rij pas na afloop.

Waarom het werkt: voor deze acties is er één pad naar uitvoering en dat schrijft eerst, dus een uitgevoerde actie zonder rij kan daar niet ontstaan.

Niet doen als: de actie puur lezend is en geen enkel side effect heeft; dan is het schrijven van een audit-rij voor elke lees-call pure overhead.

Toetsvraag: kan een actie uitgevoerd worden via een pad dat deze gateway-functie niet aanroept?

Bronnen:
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab server/src/computer/gateway.ts:9 "Three jobs"
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab server/src/computer/gateway.ts:13 "Deny beats allow"
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab server/src/computer/gateway.ts:914 "crypto.randomUUID"

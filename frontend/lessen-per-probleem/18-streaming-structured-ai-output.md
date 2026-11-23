# Een UI-kaart uit een modelstream bouw je regel voor regel en post je pas als er iets te zien is

Probleem: een model dat een UI-kaart als één JSON-document streamt levert tussentijds afgebroken JSON; daar synchroon op parsen en renderen laat de UI flikkeren tussen lege en kapotte staten.

Oplossing:
- Laat het model patch-operaties streamen, één per regel (json-render: SpecStream, JSONL). De compiler (`createSpecStreamCompiler`) buffert tekstfragmenten, houdt een onvolledige laatste regel vast en past alleen complete regels toe. Zo bestaat er geen afgebroken document.
- `push(chunk)` geeft het bijgewerkte resultaat en de `newPatches` terug; zonder nieuwe patches valt er niets te renderen.
- Post pas als er zichtbare inhoud is (titel, subtitel, afbeelding of een kind-element): chatplatforms weigeren een leeg bericht. Daarna bewerk je hetzelfde bericht.
- Throttle op een vast interval (standaard 500 ms, instelbaar) en sla een update over als de geserialiseerde kaart gelijk is aan de laatst verstuurde (`lastSent`).
- Na de stream bouw je de definitieve kaart met validatie. Faalt die, dan gooit de functie een fout met een verwijzing naar het al geplaatste bericht, zodat de aanroeper dat kan bijwerken of opnieuw proberen.

Waarom het werkt: de kijker ziet de kaart geleidelijk vollopen, en een edit-aanroep naar het platform gebeurt alleen als de zichtbare inhoud veranderde en het interval verstreken is.

Niet doen als: het model al gestructureerde, functie-call-achtige output levert die per definitie pas compleet aankomt.

Toetsvraag: wordt er nooit een bericht geplaatst voordat de kaart minstens één zichtbaar veld heeft?

Bronnen:
- vercel-labs/json-render@c926907855d9 packages/chat/src/stream.ts:61 "newPatches"
- vercel-labs/json-render@c926907855d9 packages/chat/src/stream.ts:53 "lastSent"
- vercel-labs/json-render@c926907855d9 packages/core/src/types.ts:898 "lines.pop()"

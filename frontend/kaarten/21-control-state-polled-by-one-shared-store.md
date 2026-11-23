# Wie het stuur van een bot-computer heeft, peil je met één gedeelde store, en één gemiste lezing haalt het stuur niet van het scherm

Probleem: peilt elk onderdeel (chat, zijkant, modal) zelf en blankt één mislukte lezing de staat, dan verliest iemand midden in een zin het toetsenbord en worden ingedrukte toetsen losgelaten, voor een haperen dat een seconde later weg is.

Oplossing:
- Eén store per computer-id in een `Map`, gedeeld door alle views. Hij peilt elke 1000 ms, niet terwijl `document.hidden`, en leest meteen opnieuw als het tabblad weer zichtbaar wordt.
- De timer start geen lezing zolang er een loopt of een wijziging bezig is, anders wordt een trage lezing elke seconde afgebroken en komt er nooit een antwoord. Een losse `refresh` en een wijziging breken de lopende lezing wel af, en de teller `version` ongeldigt lezingen van voor een wijziging. Na de `await` telt het antwoord alleen als de lezing niet afgebroken is, `version` gelijk is en er geen wijziging bezig is (`busy`).
- Eén mislukte lezing laat een bekende staat staan. Pas de tweede achter elkaar (`MISSED_READS_BEFORE_PAUSE` = 2, ongeveer twee seconden) zet de staat op `null` met de melding dat invoer gepauzeerd is.
- Een gelijk antwoord wordt niet gepubliceerd (vergelijking via `JSON.stringify`), anders rendert elke view elke seconde voor niets.
- Een wijziging (`take`, `release`, `cancel`) wordt geweigerd tijdens `busy` of `transitioning`. `release` en `cancel` starten niet zonder bekend verzoek-id.
- De lees- en wijzigfuncties in `control.ts` geven `null` bij een foutstatus of een onbruikbaar antwoord en cachen niets, want volgens de bron is wie het stuur heeft een feit van deze seconde.
- Let op de keuze in `heldByOther`: een houder zonder naam, of een nog onbekende ingelogde persoon, telt als "de kijker zelf". De handhaving zit dus niet hier: de bron zegt dat de computer invoer van wie het stuur niet heeft weigert, wat de store ook toont.
- Invoer van de mens (klik, tekst, toets, scroll) gaat via één promise-keten voor alle computers, zodat de volgorde klopt. Een mislukte invoer wordt in de code niet herhaald of gemeld, de keten loopt door.
- Alleen de koppeling met `useSyncExternalStore` is React. De store zelf is gewone TypeScript.

```ts
function poller<T>(read: (s: AbortSignal) => Promise<T | null>, publish: (v: T | null) => void) {
  let version = 0, misses = 0, last: T | null = null, reading: AbortController | undefined, timer: number | undefined;
  async function tick() {
    if (document.hidden || reading) return;                  // a slow read is not cut off
    const mine = version, c = (reading = new AbortController());
    const v = await read(c.signal).catch(() => null).finally(() => { if (reading === c) reading = undefined; });
    if (c.signal.aborted || mine !== version) return;        // a mutation or stop won
    if (!v && ++misses < 2 && last) return;                  // one hiccup is not news
    if (v) misses = 0;
    if (JSON.stringify(v) !== JSON.stringify(last)) publish((last = v));
  }
  const cancel = () => { version++; reading?.abort(); reading = undefined; }; // before and after a mutation
  return { cancel, start() { timer ??= window.setInterval(tick, 1000); void tick(); },
    stop() { clearInterval(timer); timer = undefined; cancel(); } };
}
```

Waarom het werkt: de UI volgt een gezaghebbend antwoord met een teller die oude antwoorden ongeldig maakt, en tolereert één hapering.

Niet doen als: de bron een push-kanaal is dat zelf meldt wanneer de verbinding wegvalt.

Toetsvraag: haalt één enkele mislukte lezing de bedieningselementen van het scherm?

Bronnen:
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab app/src/lib/computers/use-control.ts:28 "MISSED_READS_BEFORE_PAUSE"
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab app/src/lib/computers/use-control.ts:173 "heldByOther"
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab app/src/lib/computers/control.ts:119 "inputQueue"

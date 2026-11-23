# Een mens die het stuur neemt sluit eerst de deur voor de bot en wacht dan op wat al loopt

Probleem: neemt iemand een browser over terwijl de bot nog een klik of typeactie uitvoert, dan werken twee handen tegelijk in dezelfde pagina. Of de bot hervat later met een scherm dat al veranderd is.

Oplossing:
- De handelende paden van de bot (`ACTING_PATHS`) gaan langs één controle vóór hun handlers. Lezen staat er niet op en blijft open. Let op: dit is een lijst van geweerde paden, een nieuw schrijvend pad dat er niet op staat wordt niet geweigerd, en routes die eerder in de dispatcher terugkeren (de browser van een persoon) zien deze controle niet.
- Toegang is in OpenBot synchroon. `enter()` geeft een vrijgavefunctie of gooit meteen, de poort heeft geen wachtrij.
- Neemt een mens het stuur, dan sluit de poort vóór de eerste `await`. Daarna wacht `drain` tot het aantal lopende acties 0 is, in OpenBot standaard 30 s. Daarna kijkt OpenBot opnieuw of hetzelfde verzoek nog `waiting` is, want het kan intussen verlopen, geannuleerd of genomen zijn.
- Na die time-out verschillen de twee bronnen. OpenBot weigert de overdracht: het verzoek blijft `waiting` en de mens probeert opnieuw. OpenMausBot geeft het stuur na 15 s toch en markeert het profiel `stale` (tot teruggave) en `uncertain` (tot een probe).
- Een botaanroep die al liep toen de mens nam, levert achteraf een weigering op in plaats van zijn resultaat (OpenMausBot).
- In OpenBot sluit het verzoek om hulp de poort al, maar roept het `drain` niet aan. Het commentaar noemt als reden dat de aanroepende actie nog haar eigen lease vasthoudt.

```ts
let open = true, active = 0, idle = new Set<() => void>();
function enter() {
  if (!open) throw new Error('refused: a person has the wheel');
  active++; let done = false;
  return () => { if (!done && (done = true) && --active === 0) idle.forEach((f) => f()); };
}
async function take(ms: number) {
  open = false; // before any await; stays closed on failure, only a hand-back reopens it
  if (active === 0) return;
  await new Promise<void>((ok, no) => {
    const f = () => { clearTimeout(t); idle.delete(f); ok(); };
    const t = setTimeout(() => { idle.delete(f); no(new Error('not granted')); }, ms);
    idle.add(f);
  });
}
```

Waarom het werkt: sluiten is synchroon en tellen gebeurt per actie, dus er sluipt geen actie meer binnen terwijl je wacht. Een dubbele vrijgave telt niet dubbel.

Niet doen als: er maar één schrijver is en geen twee tools tegelijk acties kunnen starten.

Toetsvraag: staat elk pad dat de pagina of het bestandssysteem wijzigt op de lijst die de poort raadpleegt?

Bronnen:
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab agent-computer/src/control.ts:441 "barrier.close()"
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab agent-computer/src/index.ts:1198 "actsOnTheComputer"
- milind-soni/OpenMausBot@77f41d3522217a484b4abdffa9d5f6ba651f84bd server/browser/control.ts:101 "stale = true"

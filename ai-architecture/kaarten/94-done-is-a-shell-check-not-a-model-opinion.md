# Klaar is een shellcommando met exitcode 0 en niet het oordeel van het model, en een mislukte poging begint opnieuw bij de prompt van die beurt

Probleem: een agent die zegt "klaar" is geen bewijs, en elke herhaalpoging die de hele mislukte geschiedenis meesleept wordt langer en dommer.

Oplossing:
- Een recipe kan `retry` bevatten met `max_retries` (moet groter dan 0), `checks` (alleen `shell`), optioneel `on_failure` en twee time-outs. Zonder `retry` in het recipe zijn er geen checks.
- Dezelfde operatie regelt ook `/goal` en `/grind`, en die gaan voor. Een goal vraagt het model één keer om zelf te controleren, dus juist zijn oordeel. Zolang een grind aanstaat komen de checks niet aan bod.
- Hij draait alleen op het moment dat de beurt eindigt (`ends_turn`). De checks lopen na elkaar, de eerste die niet met 0 eindigt stopt de rij; een lege lijst slaagt. Elke check krijgt standaard 300 s, `on_failure` 600 s, beide instelbaar.
- Slaagt alles, dan begint deze operatie niet opnieuw. Faalt een check, dan loopt de teller: bij `attempts >= max_retries` volgt een foutbericht, anders wordt `on_failure` uitgevoerd en wordt het gesprek teruggezet tot en met het kickoffbericht van deze beurt. Wat daarvoor stond blijft.
- De teller staat in de metadata van dat kickoffbericht, want dat is het enige bericht dat een poging overleeft. Met `max_retries` = 2 zijn dat dus hooguit 3 runs.
- Kan een check niet draaien, loopt hij in de time-out of mislukt `on_failure`, dan geeft de code alleen een foutbericht terug en zet het gesprek niet terug. Wat de pijplijn daarna doet staat in een externe crate (`oi_kit_agent`) die ik niet las.
- Stdout van een check wordt weggegooid en stderr (laatste 8 KiB) gaat in deze code alleen naar de log. Het model hoort niet waarom het faalde.
- Alleen het gesprek wordt teruggezet. Wijzigingen op schijf blijven staan, tenzij `on_failure` ze opruimt.

```ts
async function runUntilGreen(
  agent: () => Promise<void>, checks: string[], maxRetries: number,
  exec: (cmd: string) => Promise<number>,
) {
  for (let attempt = 0; ; attempt++) {
    await agent(); // every attempt starts from the same kickoff prompt
    let ok = true;
    for (const c of checks) if ((await exec(c)) !== 0) { ok = false; break; }
    if (ok) return 'passed';
    if (attempt >= maxRetries) return 'gave up';
  }
}
```

Waarom het werkt: het bewijs is een proces dat niet kan flatteren, en een schone herstart voorkomt dat de context vol raakt met doodlopende pogingen.

Niet doen als: het recipe uit een onbetrouwbare bron komt. De checks draaien via `sh -c` met de rechten van de gebruiker.

Toetsvraag: staat er een check die faalt als het werk niet klaar is, en ruimt `on_failure` op wat een mislukte poging op schijf achterlaat?

Bronnen:
- aaif-goose/goose@059fee25f13fa92be561a7d42cdd04ececef5a98 crates/goose/src/agents/state_machine/ops_retry.rs:72 "fn attempts"
- aaif-goose/goose@059fee25f13fa92be561a7d42cdd04ececef5a98 crates/goose/src/agents/retry.rs:13 "execute_success_checks_with_timeout"
- aaif-goose/goose@059fee25f13fa92be561a7d42cdd04ececef5a98 crates/goose/src/agents/types.rs:4 "DEFAULT_RETRY_TIMEOUT_SECONDS"

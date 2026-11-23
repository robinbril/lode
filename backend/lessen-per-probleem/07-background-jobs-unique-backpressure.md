# Een achtergrondtaak krijgt een eigen concurrency-key per tenant, niet een globale limiet

Probleem: een globale concurrency-limiet op een queue laat een drukke tenant de wachttijd van alle andere tenants opblazen. En zonder dedupe-sleutel vuurt een flapperende trigger (bijvoorbeeld tien snelle updates op een rij) de dure taak tien keer af in plaats van een keer.

Oplossing:
- Dedupe gelijke taken via een debounce-key (in Polar een Redis-hash): elke enqueue krijgt de vertraging `debounce_min_threshold`, onthoudt het oudste `enqueue_timestamp` en neemt het eigenaarschap van de sleutel over. Bij uitvoering draait alleen de laatste eigenaar; eerdere berichten met dezelfde sleutel worden overgeslagen. Is `debounce_max_threshold` sinds het oudste timestamp verstreken, dan draait een niet-eigenaar alsnog en wordt het timestamp opnieuw gezet.
- Zet de concurrency-key op het tenant- of accountveld uit de input, niet op de taaknaam, zodat de limiet per tenant geldt en niet gedeeld wordt over alle klanten.
- Laat het limiet per tenant variabel zijn (bijvoorbeeld hoger voor een duurder abonnement), berekend uit de input in plaats van een vast getal in code.

```python
if enqueue_timestamp + max_threshold < now_timestamp():
    # oudste enqueue te lang geleden: draai nu toch, ook als dit bericht geen eigenaar is
```
```go
maxRunsExpression := "input.Tier == 'premium' ? 10 : 1"
```

Waarom het werkt: een key per tenant isoleert ruis van de een van de wachttijd van de ander (backpressure blijft lokaal), en een max-threshold op de debounce voorkomt dat een taak die steeds net op tijd opnieuw binnenkomt, voor altijd wordt uitgesteld.

Niet doen als: elke taak al goedkoop en idempotent genoeg is om gewoon los te draaien; dedupe- en concurrency-logica voegt dan alleen staat toe zonder een echt probleem op te lossen.

Toetsvraag: kan een enkele drukke tenant de wachttijd van een andere tenant op dezelfde queue laten oplopen?

Bronnen:
- polarsource/polar@b0be821b5c47ae86ffd50556b44829051c9dd329 server/polar/worker/_debounce.py:131 "enqueue_timestamp + max_threshold"
- hatchet-dev/hatchet@2a0b386361abbb0164b454b5cf24e668a671d101 examples/go/concurrency/main.go:201 "input.Tier == 'premium'"

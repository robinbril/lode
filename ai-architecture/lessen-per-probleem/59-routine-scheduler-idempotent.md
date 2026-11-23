# De idempotentie van een geplande routine zit in de sleutel, niet in een lock

Probleem: drie worker-processen die elke minuut checken "moet deze routine nu draaien" kunnen dezelfde routine op hetzelfde moment allemaal starten, tenzij er iets is dat dubbele starts afwijst zonder dat je een gedeeld lock-proces hoeft te bouwen.

Oplossing:
- De sleutel waarmee een geplande start wordt aangeboden aan de werk-queue is `<routine-id>:<minuut-van-nextRunAt>`. Niet een timestamp van "nu", maar de minuut waarop de start gepland stond.
- De minuut wordt altijd in UTC en door één functie geschreven: een andere opmaak is een andere sleutel en dus een dubbele run.
- Een unieke sleutel in de queue zorgt dat van drie gelijktijdige offers er één telt. Een afgeronde rij blijft een tijd staan, zodat een trage worker ook na de run nog botst; bewaar hem langer dan de langste sweep.
- Eerst aanbieden, dan de klok verzetten. Crasht het ertussen, dan biedt de volgende pass dezelfde sleutel aan; andersom is de run kwijt.
- Meer dan 10 minuten te laat: niet aanbieden, wel doorzetten naar de volgende keer vanaf nu. Zo komt er na een maand stilstand geen stapel oude runs.
- De volgende-run-tijd wordt verzet met een compare-and-set: `UPDATE routines SET next_run_at = to WHERE next_run_at = from`. Alleen de worker die exact de oude waarde las, mag hem verzetten; een worker die een stale waarde had, raakt niets.
- Het dispatchen zelf loopt via dezelfde lease-gebaseerde werkqueue als andere acties, dus een gecrashte worker laat de claim verlopen in plaats van de routine kwijt te raken. Bij een tweede claim kan de eerste al iets gedaan hebben: de teller `attempts` boven 1 betekent dat.

```ts
const offerKey = `${routine.id}:${minuteKey(routine.nextRunAt)}`;
// UPDATE routines SET next_run_at = $to WHERE id = $id AND next_run_at = $from
```

Waarom het werkt: de sleutel codeert "welke geplande start is dit" in plaats van "wanneer probeerde iemand het te starten", dus twee workers die tegelijk pollen zien dezelfde sleutel en de queue (niet een los lock-mechanisme) beslist wie wint.

Niet doen als: routines zelden genoeg draaien dat een enkel cron-proces zonder concurrency-risico volstaat; dan is deze compare-and-set-constructie overbodige complexiteit.

Toetsvraag: levert een trage poller met een verouderde `nextRunAt`, ook na afloop van de run, nog steeds geen tweede offer op?

Bronnen:
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab server/src/routines/sweep.ts:14 "OFFER KEY"
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab server/src/routines/sweep.ts:190 "minuteKey(routine.nextRunAt)"

# Een overdracht aan een mens is een bewaard verzoek met id en eindstatus, en een herstart levert `interrupted` op in plaats van `completed`

Probleem: een bot die om hulp vraagt en daarna crasht of herstart, weet niet meer of de mens de pagina nog heeft, wat hij erop deed, of zijn eigen oude schermstand nog klopt.

Oplossing:
- Een verzoek heeft een `id`, een `status` (`waiting`, `taken`, `completed`, `cancelled`, `expired`, `interrupted`) en een redenstekst van hooguit 500 tekens. Er is hooguit één actief verzoek. Een tweede aanvraag geeft het lopende terug.
- Dezelfde `toolCallId` geeft hetzelfde verzoek terug, via een alias-tabel (hooguit 256 aliassen, opgeruimd met de laatste 32 afgelopen verzoeken en na 30 dagen). Een herhaalde toolaanroep maakt dus geen tweede verzoek zolang die alias bestaat.
- Alleen `waiting` verloopt, na 10 minuten (`HELP_REQUEST_TTL_MS`). De controle gebeurt lui bij een aanroep, er loopt geen timer. In deze module verloopt een `taken` verzoek niet vanzelf.
- Nemen, teruggeven en annuleren moeten het id van het huidige verzoek noemen, anders volgt een 409. Een oud scherm kan dus geen nieuw verzoek aanraken.
- Wordt de staat bij opstarten geladen met een actief verzoek of een mens als houder, dan wordt een actief verzoek `interrupted` en wordt `recoveryRequired` gezet als een mens de pagina had. Alleen dan blijft de bot geblokkeerd, tot een mens een nieuw verzoek neemt en teruggeeft. Had niemand genomen, dan mag de bot door na een nieuwe momentopname.
- Na teruggave of onderbreking eist `resumeSnapshotRequired` een nieuwe momentopname vóór klik, typen, toets of scroll. Een pagina openen mag wel en heft de eis op. Een herstart zonder lopende overdracht wist de eis.
- Lukt opslaan niet, dan sluit de poort en blijft ze dicht: de foutstaat wordt in deze module nergens gewist.
- Volgens het commentaar komen geheime waarden niet in deze staat. Het paginaadres wel, en dat kan een eenmalig token bevatten: het wordt gewist als het verzoek eindigt, behalve na een herstart (dan nog hooguit 10 minuten bruikbaar).

```ts
const active = (r?: { status: string }) => r?.status === 'waiting' || r?.status === 'taken';
function onBoot(s: State) {                    // s is loaded from disk
  const personHadIt = s.holder === 'human' || s.current?.status === 'taken';
  s.needsFreshSnapshot = personHadIt || active(s.current);  // not on every plain restart
  if (s.current && active(s.current)) s.current.status = 'interrupted';
  if (personHadIt) s.recovery = true;          // nobody looked at that page yet
  s.holder = 'bot';
  save(s);                                     // before the bot may act
}
const botMayAct = (s: State) => s.holder === 'bot' && !active(s.current) && !s.recovery;
```

Waarom het werkt: elke toestand is een veld dat een herstart kan lezen, dus "wat was er aan de hand" hoeft niet te worden geraden.

Niet doen als: meerdere processen dezelfde bot bedienen; deze module vergrendelt niet tussen processen en de opslag is optioneel. Wil je dat een hold vanzelf eindigt, voeg dan een idle- en een grace-timer toe zoals OpenMausBot (`hold.ts`: 5 minuten idle, 2 minuten zonder open view).

Toetsvraag: levert een herstart terwijl een mens het stuur heeft een status op die de bot blokkeert tot een mens kijkt?

Bronnen:
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab agent-computer/src/control.ts:311 "interruptedByRestart"
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab agent-computer/src/control.ts:530 "recoveryRequired"
- milind-soni/OpenMausBot@77f41d3522217a484b4abdffa9d5f6ba651f84bd server/browser/hold.ts:12 "IDLE_MS"

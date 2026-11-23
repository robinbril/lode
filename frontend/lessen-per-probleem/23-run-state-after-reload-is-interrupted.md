# Na een reload is een lopende beurt niet meer lopend: de browser markeert hem als onderbroken, en een generatieteller houdt oude schrijvers buiten

Probleem: de staat van een beurt staat in opgeslagen browserstaat, maar het proces dat hem uitvoerde stierf met de tab. Zonder correctie toont de pagina na een reload eeuwig "bezig", en een late schrijver kan een geannuleerde beurt weer overschrijven.

Oplossing:
- Een run heeft een `phase` (`accepted`, `running`, `awaiting-question`, `awaiting-approval`, `final-pending-delivery`, daarna `delivered`, `failed`, `cancelled`, `interrupted`) en een `generation`. De eigenaar van een run bestaat alleen in het geheugen van deze tab, in een `Map` met een `AbortController`.
- `restartable` zijn `accepted`, `running` en `final-pending-delivery`. Bij de eerste afstemming na het laden gaan runs in die fasen die er bij het laden al waren naar `interrupted`, samen met de status van hun uitvoerbericht, in één opslagstap. Is de staat inmiddels veranderd, dan mislukt die stap en toont `getRuntime` `reload-save-failed`. De `awaiting`-fasen zijn niet `restartable` en blijven staan.
- Tot die afstemming gelukt is, weigeren `start` en `resume` met `reload-not-reconciled`. Ook zonder afstemming of zonder eigenaar toont `getRuntime` een restartable fase al als `interrupted`.
- De start-, aflever- en faalstappen controleren binnen de opslagstap zelf of de aanroeper nog eigenaar is: zelfde object, niet afgebroken, geen annulering en dezelfde `generation` als in de opgeslagen run. Anders gooit de stap en wordt niets geschreven.
- Annuleren zet `cancelGeneration` op `generation + 1`, breekt af en slaat `cancelled` op met die nieuwe generatie. Een late uitkomst van de adapter faalt daarna op de eigenaarscheck.
- Hervatten kan alleen vanuit `interrupted` en alleen voor de lokale tekstadapter, verhoogt de generatie met 1 en breekt de oude eigenaar af. Een tweede actieve run in hetzelfde gesprek geeft `busy`.
- Een `submissionId` maakt `start` herhaalbaar: dezelfde inhoud geeft dezelfde run terug, andere inhoud `submission-mismatch`.
- Niet gedekt: dit is een demo-adapter. Een echte modelstream kan deze code niet hervatten, die blijft op `interrupted` staan. Opent iemand een tweede tab op dezelfde opslag, dan markeert die ook runs die in de eerste tab nog lopen; daartegen staat hier geen slot.

```js
const owners = new Map(); // runId -> { runId, generation, abort }
const live = (r) => ['accepted', 'running'].includes(r?.phase);
const owns = (s, o) => owners.get(o.runId) === o && !o.abort.signal.aborted && s.runs[o.runId]?.generation === o.generation;
const patch = (s, id, p) => ({ ...s, runs: { ...s.runs, [id]: { ...s.runs[id], ...p } } });
function onPageLoad(store) { // once: whatever was running lost its tab
  store.commit((s) => Object.values(s.runs).filter(live).reduce((a, r) => patch(a, r.id, { phase: 'interrupted' }), s));
}
function cancel(store, o) {
  o.abort.abort(); // a late result can no longer pass owns()
  store.commit((s) => live(s.runs[o.runId]) && s.runs[o.runId].generation === o.generation
    ? patch(s, o.runId, { phase: 'cancelled', generation: o.generation + 1 }) : s); // never over 'delivered'
}
function write(store, o, p) { // the check runs inside the atomic commit
  store.commit((s) => { if (!owns(s, o)) throw new Error('revoked'); return patch(s, o.runId, p); });
}
```

Waarom het werkt: met één tab is het geheugen van die tab de enige plek die weet dat een run echt loopt, dus een lopende fase zonder eigenaar is bij het laden onderbroken.

Niet doen als: de server de run uitvoert en zelf de waarheid kent; dan vraag je die in plaats van te raden.

Toetsvraag: toont de pagina na een reload ooit een run als "bezig" waarvoor in dit geheugen geen eigenaar bestaat?

Bronnen:
- robinbril/grokbot-reconstruction@b2e1c8629027d05ff61f5c84ab42a1c6c2c9417b apps/web/chat-run-controller.js:4 "restartable"
- robinbril/grokbot-reconstruction@b2e1c8629027d05ff61f5c84ab42a1c6c2c9417b apps/web/chat-run-controller.js:72 "effectivePhase = 'interrupted'"
- robinbril/grokbot-reconstruction@b2e1c8629027d05ff61f5c84ab42a1c6c2c9417b apps/web/chat-run-controller.js:263 "cancelGeneration ||="

# Een bericht wordt eerst als bedoeling met een nonce in een lokaal journal bewaard en pas daarna verstuurd, en bij twijfel beslist een opzoeking op die nonce

Probleem: sluit je de tab of valt de verbinding weg tussen Enter en het antwoord, dan weet de pagina niet of het bericht aankwam. Opnieuw versturen kan een dubbel bericht geven, niet versturen een verloren bericht.

Oplossing:
- Elk bericht is een record met drie verschillende ids (`nonce`, `inputEntryId`, `noticeEntryId`), een snapshot en een `phase`: `queued`, `prepared`, `dispatching`, `accepted-awaiting-echo` of `failed`. De tabel (hooguit 100 records, `schema: 1`) staat in dezelfde opgeslagen staat als de chat. Bij het inlezen wordt ze gevalideerd tegen een gesloten schema.
- Volgorde bij versturen: eerst `prepared` bewaren, dan `dispatching` bewaren, dan pas de request. Een crash laat dus een `dispatching` record achter, en er gaat geen request weg zonder bewaard record.
- De nonce gaat mee in de payload als `clientNonce`. In de bron schrijft de ontvanger hem terug op de berichtregel, samen met `inputEntryId`.
- Per gesprek op volgorde van `createdAt`. Staat het oudste record in een andere fase dan `queued` of `prepared`, ook `failed`, dan wachten de nieuwere van dat gesprek. Andere gesprekken lopen door.
- Een `isHeld`-voorwaarde (in de bron: offline) houdt alles tegen. Gooit die voorwaarde zelf, dan telt dat als vasthouden.
- Aan het begin van elke drain, dus ook na een reload, vraagt `lookupAcceptance` per `dispatching` of `accepted-awaiting-echo` record of de regel er is. `found` verwijdert het record. `not-found` bij `dispatching` zet het terug op `queued`. `not-found` bij `accepted-awaiting-echo` doet niets, want een ontvangstbevestiging wint van een regel die even ontbreekt. Een fout of `unknown` laat alles staan.
- Reconcile, drain en retry lopen door één promise-keten (`schedule`), en na elke `await` wordt gecontroleerd of het record nog hetzelfde object is. Enqueue en annuleren van een `queued` record zijn synchroon en lopen er buiten. De keten geldt per tab: tegen een tweede tab op dezelfde opslag staat hier geen slot.
- Dit bewijst niets zonder een eerlijke opzoeking. In de bron zoekt de demo in `localStorage`. Een server moet op nonce kunnen opzoeken, en een traag zichtbare `not-found` geeft een dubbel bericht. Een blijvende `unknown` laat een record zonder time-out hangen, `retry` weigert dan met `uncertain`.

```js
async function drain(journal, send, lookup) {   // one serialized chain; set() persists before it returns
  for (const r of journal.open()) {             // one conversation, oldest first, every phase
    if (r.phase === 'failed') return;           // a person decides first
    if (r.phase === 'dispatching' || r.phase === 'accepted-awaiting-echo') {
      const s = await lookup(r.nonce);
      if (!journal.has(r)) continue;            // cancelled while we waited
      if (s === 'found') { journal.remove(r); continue; }
      if (s !== 'not-found' || r.phase !== 'dispatching') return; // do not resend, keep the order
    }
    journal.set(r, 'dispatching');              // intent is on disk before the request leaves
    const ok = await send(r).catch(() => null);
    if (ok !== true) { if (ok === false) journal.set(r, 'failed'); return; }
    journal.set(r, 'accepted-awaiting-echo');
  }
}
```

Waarom het werkt: elke stap is eerst bewaard en daarna uitgevoerd, dus een reload kan zien in welke fase het bericht zat.

Niet doen als: de server geen opzoeking op nonce kent; dan is `not-found` een gok.

Toetsvraag: kan de server bij een herhaalde nonce zeggen of hij het bericht al heeft?

Bronnen:
- robinbril/grokbot-reconstruction@b2e1c8629027d05ff61f5c84ab42a1c6c2c9417b apps/web/send-journal.js:6 "accepted-awaiting-echo"
- robinbril/grokbot-reconstruction@b2e1c8629027d05ff61f5c84ab42a1c6c2c9417b apps/web/send-journal.js:86 "status==='not-found'"
- robinbril/grokbot-reconstruction@b2e1c8629027d05ff61f5c84ab42a1c6c2c9417b apps/web/app.js:507 "lookupSavedSend"

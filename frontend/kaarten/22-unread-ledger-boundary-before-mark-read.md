# Ongelezen is een eigen lokaal grootboek met ontvangstbewijzen, en de grens voor het "Nieuw"-streepje wordt vastgelegd voordat je het gesprek als gelezen markeert

Probleem: een teller die ongelezen afleidt uit het transcript telt oude berichten zonder tijd mee na een start, verliest zijn grens zodra je het gesprek opent, of markeert alles als gelezen voordat je kunt zien wat nieuw was.

Oplossing:
- Per gesprek bewaart een grootboek `lastViewedAt`, `seenIds` en `receipts` (`id`, `entryId`, `timestampMs`, `eligible`) in `localStorage` onder één sleutel met `version: 1`. Een ongeldige of onbekende versie wordt als leeg ingelezen.
- Eerste keer dat een id langskomt: tijd van het bericht, en zonder tijd `now()`. Bij het opstarten van de pagina draait de eerste ronde met `baseline: true`: berichten zonder tijd die er dan al zijn krijgen geen bewijs en tellen niet mee. Een bericht met tijd krijgt ook dan een bewijs, dus bij een leeg grootboek is zo'n botbericht ongelezen.
- `eligible` komt uit één regel die onder meer eigen berichten, toolaanroepen, fouten en bijlagen van de gebruiker buiten beschouwing laat. `hasUnread` is `lastActivityAt > lastViewedAt`, met `lastActivityAt` het maximum over de geschikte bewijzen.
- De bewijzen zijn geen kopie van het transcript: bij het lezen worden ze langs de huidige berichten gehouden, dus een verwijderd bericht telt niet meer mee.
- Openen volgt een vaste volgorde: eerst de grens vastzetten (is er activiteit na `lastViewedAt`, dan wordt de grens die oude `lastViewedAt`), dan pas als gelezen markeren. Het streepje komt vóór het eerste geschikte bericht dat nieuwer is dan de grens.
- `markRead` is monotoon: het maximum van de oude waarde, de laatste activiteit en `now()`. Ook een venster dat weer focus krijgt markeert zo, zonder een nieuwe grens te zetten.
- Een mislukte `setItem` laat de staat in het geheugen ongewijzigd en zet een vlag. De pagina toont dan een melding dat de leesstatus niet bewaard kon worden.
- Niet gedekt: er is geen limiet op `seenIds`, en een bericht zonder tijd krijgt de tijd waarop jij het zag, niet waarop het werd verstuurd. Synchronisatie tussen apparaten zit in deze module niet, en twee tabs overschrijven elkaars tabel: de opslag wordt alleen bij het opstarten gelezen.

```js
const rows = new Map(); // conversationKey -> { viewedAt, seen:Set, receipts:Map(id -> time) }
function note(key, entries, { baseline = false } = {}) {
  const row = rows.get(key) ?? { viewedAt: 0, seen: new Set(), receipts: new Map() };
  for (const e of entries) {
    if (!row.seen.has(e.id) && (e.time || !baseline)) row.receipts.set(e.id, e.time ?? Date.now());
    row.seen.add(e.id);                         // also when it gets no receipt
  }
  return rows.set(key, row).get(key);
}
function open(key, isEligible) {                // returns the boundary for the divider
  const row = rows.get(key) ?? note(key, []), latest = Math.max(0, ...[...row.receipts].filter(([id]) => isEligible(id)).map(([, t]) => t));
  const boundary = latest > row.viewedAt ? row.viewedAt : null;
  row.viewedAt = Math.max(row.viewedAt, latest, Date.now());   // mark read after capturing
  return boundary;
}
```

Waarom het werkt: de grens blijft staan terwijl je het gesprek leest, en een start maakt oude berichten zonder tijd niet ongelezen.

Niet doen als: de server al een leesmarkering per gebruiker kent; dan is dit een tweede waarheid.

Toetsvraag: wordt de grens vastgelegd voordat het gesprek als gelezen wordt gemarkeerd?

Bronnen:
- robinbril/grokbot-reconstruction@b2e1c8629027d05ff61f5c84ab42a1c6c2c9417b apps/web/transcript-unread-ledger.js:49 "baseline?undefined:now()"
- robinbril/grokbot-reconstruction@b2e1c8629027d05ff61f5c84ab42a1c6c2c9417b apps/web/transcript-unread-ledger.js:59 "Math.max(previous.lastViewedAt"
- robinbril/grokbot-reconstruction@b2e1c8629027d05ff61f5c84ab42a1c6c2c9417b apps/web/transcript-unread-surface.js:77 "host.onUnreadOpen"

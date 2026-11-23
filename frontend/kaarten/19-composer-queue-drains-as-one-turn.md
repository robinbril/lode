# Wat je typt terwijl de bot werkt wordt geparkeerd en gaat als één vervolgbeurt weg zodra de beurt eindigt, ook na een fout of Stop

Probleem: een composer die Enter negeert tijdens een beurt dwingt je te kiezen tussen stoppen en alles kwijt zijn, of wachten tot de bot klaar is met het verkeerde.

Oplossing:
- De regel is één pure functie `reduceQueue(queue, action)` met vier acties: `submit`, `settle`, `restore`, `remove`. Ze geeft `{ queue, run, droppedAttachments, restoreIfRunFails }` terug.
- `busy` komt van buiten, van de composer die zowel de `pending` van de ouder als zijn eigen onafgemaakte send kent.
- Een send zonder wachtrij gaat direct weg. Een send met een niet-lege wachtrij sluit achteraan aan en gaat dus niet voor.
- `settle` geldt voor elk einde van de beurt: klaar, mislukt of gestopt. Daardoor is Stop sturen in plaats van opgeven: parkeer een correctie, druk Stop, en die correctie draait daarna. Twee uitzonderingen: in een uitgeschakeld gesprek en na een mislukte leegloop blijft alles staan.
- Alles wat geparkeerd staat wordt één beurt. Teksten komen onder elkaar met `\n`, een bericht zonder tekst levert geen lege regel, dubbele `/`-commando's tellen één keer.
- Bijlagen worden platgemaakt en afgekapt op `MAX_ATTACHMENTS_PER_MESSAGE` (8 in de bron). De vroegste blijven. De rest komt terug in `droppedAttachments` zodat de aanroeper de geüploade rijen kan vrijgeven.
- Faalt de verzonden beurt, dan gaan de berichten die de wachtrij bijdroeg terug vooraan, zonder de afgekapte bijlagen en zonder zelf een nieuwe beurt te starten. Het bericht dat nog in de composer stond zet de composer zelf terug, anders staat het er dubbel. Pas als een mens een beurt start, mag het weer leeglopen.
- De wachtrij is geheugen van één mount. Een reload of een ander kanaal gooit haar weg, ook het commentaar zegt dat ze geen outbox is.
- Alleen de reducer is portable. De effect- en ref-aanpak in `conversation-view.tsx` is React. In Vue (eigen advies, niet uit de bron) pas je de reducer synchroon toe op de ref; alleen `settle` hangt aan een watcher op het einde van de beurt.

```ts
type Msg = { id: string; text: string };
type Act = { type: 'submit'; msg: Msg; busy: boolean } | { type: 'settle' }
  | { type: 'restore'; msgs: Msg[] } | { type: 'remove'; id: string };
const join = (q: Msg[]) => q.map((m) => m.text).filter((t) => t.trim()).join('\n');
function reduce(queue: Msg[], a: Act): { queue: Msg[]; run: string | null } {
  switch (a.type) {
    case 'submit':
      if (a.busy) return { queue: [...queue, a.msg], run: null };
      return queue.length ? { queue: [], run: join([...queue, a.msg]) } : { queue, run: a.msg.text };
    // the caller keeps the old queue and restores it if this run fails
    case 'settle': return queue.length ? { queue: [], run: join(queue) } : { queue, run: null };
    case 'restore': return { queue: [...a.msgs, ...queue], run: null };
    case 'remove': return { queue: queue.filter((m) => m.id !== a.id), run: null };
  }
}
```

Waarom het werkt: drie snelle correcties zijn meestal één correctie in drie ademhalingen, en een beurt per bericht laat de bot eerst op de eerste handelen.

Niet doen als: elk bericht een eigen onomkeerbare actie is; dan wil je ze niet samenvoegen. Moet een bericht een reload overleven, dan wint kaart 20.

Toetsvraag: staat een correctie die tijdens de beurt is getypt in de volgende beurt altijd na de zin die ze corrigeert?

Bronnen:
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab app/src/components/channels/composer/queue.ts:176 "reduceQueue"
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab app/src/components/channels/composer/queue.ts:462 "MAX_ATTACHMENTS_PER_MESSAGE"
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab app/src/components/channels/conversation-view.tsx:415 "settle"

# De conversatie is een append-only rij items met een seq, en berichten zijn een afleiding daarvan

Probleem: als "de huidige conversatie" alleen als een mutable blob wordt opgeslagen, kost elke crash of race-condition tussen twee schrijvers de hele geschiedenis, en is er geen eenduidige volgorde om op terug te vallen.

Oplossing:
- Elk item krijgt een `seq` binnen zijn sessie; de primary key is `(tenant_id, session_id, seq)`, dus een dubbele seq binnen een sessie kan niet bestaan.
- De volgende seq is het hoogste van `MAX(seq) + 1` en de berichtenteller op de sessie, bepaald binnen een advisory lock per sessie die tot het eind van de transactie staat. De primary key vangt wie de lock overslaat.
- Triggers maken de log echt append-only: geen UPDATE, geen TRUNCATE, DELETE alleen via het verwijderen van de sessie. Een unieke index op `call_id` per soort weigert een dubbel tool-resultaat.
- Berichten die het model ziet, worden gereconstrueerd uit de items (tool-calls aan resultaten via `callById`/`resultByCallId`). Een call zonder resultaat krijgt een expliciet foutresultaat, zodat de geschiedenis geldig blijft.
- Een samenvatting is zelf een item met `through_seq`. Het contextvenster begint bij de seq na die grens; de oude items blijven staan.

```ts
// de view, niet de bron:
const messages = reconstructMessagesFromHistory(items);
// bron: items met PRIMARY KEY (tenant_id, session_id, seq)
```

Waarom het werkt: omdat de berichtenlijst afleidbaar is uit de items, kan een bug in de reconstructielogica worden gefixt en opnieuw gedraaid zonder dat er ooit geschiedenis verloren is; de items zelf zijn nooit het aanpaspunt.

Niet doen als: de conversatie nooit herspeeld of achteraf geïnspecteerd hoeft te worden; dan is een simpele mutable lijst goedkoper om te bouwen.

Toetsvraag: kun je de modelberichten van elke beurt opnieuw opbouwen uit de items alleen, en weigert de database een UPDATE op een item?

Bronnen:
- yc-software/qm@9dd19899b0414bad494eedbd87696eaab23a9907 src/sessions/session-schema.ts:252 "PRIMARY KEY"
- yc-software/qm@9dd19899b0414bad494eedbd87696eaab23a9907 src/agent/replay.ts:328 "reconstructMessagesFromHistory"
- yc-software/qm@9dd19899b0414bad494eedbd87696eaab23a9907 src/sessions/session-items.ts:142 "GREATEST("

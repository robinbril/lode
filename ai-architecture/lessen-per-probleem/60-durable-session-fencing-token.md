# Een sessie overleeft de harness door een fencing-token, niet door een proces dat blijft draaien

Probleem: als "wie mag deze sessie nu bijschrijven" alleen in het geheugen van het harness-proces leeft, verliest een herstart (crash, deploy, horizontale schaling) niet alleen de voortgang maar ook de garantie dat maar één worker tegelijk schrijft.

Oplossing:
- qm: elke schrijf-transactie neemt eerst een advisory lock op de sessie en controleert dan `lease_token` en `status = 'running'` met `FOR SHARE`. Die deelvergrendeling houdt een overname tegen tot de schrijf gecommit is. Klopt het token niet, dan volgt een fout.
- Die controle draait alleen als de schrijver een run-id én een token meegeeft. Een codepad zonder token schrijft dus zonder controle; maak het token verplicht.
- open-multi-agent: `fencingToken` gaat bij elke overname met één omhoog. Elke schrijf leest het record, vergelijkt token en eigenaar en schrijft met compare-and-set op de versie, met maximaal 5 herhalingen.
- Geen van beide bewaakt het verlopen zelf op de schrijf: een verlopen maar niet overgenomen lease kan nog schrijven. Dat is veilig, want er is nog geen tweede eigenaar.
- Dit beschermt alleen de eigen database. Een externe aanroep (mail, API) heeft een eigen idempotentiesleutel nodig.

```sql
BEGIN; -- controle en schrijf in één transactie, anders is er een gat
SELECT 1 FROM runs WHERE id = $1 AND lease_token = $2 AND status = 'running' FOR SHARE;
-- 0 rijen: ROLLBACK; 1 rij: schrijf de items en COMMIT
```

Waarom het werkt: de database beantwoordt "ben ik nog de eigenaar" op het moment van schrijven, niet het geheugen van een proces.

Niet doen als: een sessie altijd binnen één proceslevensduur klaar is en nooit hoeft te overleven; dan is een gewoon in-memory lock goedkoper.

Toetsvraag: faalt elke schrijf van de oude worker zodra een andere worker de run heeft overgenomen, ook via een pad dat geen token meegeeft?

Bronnen:
- yc-software/qm@9dd19899b0414bad494eedbd87696eaab23a9907 src/sessions/session-items.ts:129 "no longer holds its claim"
- open-multi-agent/open-multi-agent@e1059babc907663444a2a475e2548c61b85cea9b packages/core/src/run/ledger.ts:8 "fencing token"
- open-multi-agent/open-multi-agent@e1059babc907663444a2a475e2548c61b85cea9b packages/core/src/run/ledger.ts:547 "compareAndSet"

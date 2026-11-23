# Elke teamquery is op tenant gescoped, en een persoonlijk secret gaat alleen via een eigenaarscontrole of een grant open

Probleem: zodra een team meerdere gebruikers deelt, is de makkelijkste fout dat een query "alle teamleden" leest zonder de tenant-grens, of dat een gedeeld secret-store de eerste match teruggeeft in plaats van te checken wie er om vraagt.

Oplossing:
- `team_members` heeft een expliciete rol (`member`/`admin`) via een CHECK-constraint op de kolom; er bestaat geen vrije rol-string.
- Elke teamquery bevat `tenant_id = $1`, joins vergelijken `tenant_id` mee, en de tenant zit ook in de primary keys en foreign keys. De volgorde in de WHERE maakt niet uit; dat hij in de sleutel zit wel.
- `readOwnSecret(ownerId, id)` haalt het record op en geeft null als de eigenaar niet klopt. Metadata-lijsten lezen de kolom met het secret niet eens uit.
- Delen loopt via een grant: alleen de eigenaar kan hem maken, met verplicht doel, doelgroep en status, en verwijderen van het secret trekt actieve grants in.
- Er zijn twee soorten: connector-tokens horen bij een persoon, broker-credentials bij de organisatie. Die laatste gaan niet via grants.

```sql
-- eigen schets: sleutel en relatie dragen de tenant
PRIMARY KEY (tenant_id, team_id, principal_id),
FOREIGN KEY (tenant_id, team_id) REFERENCES teams (tenant_id, team_id)
```

Waarom het werkt: een lidmaatschap kan door de sleutels niet naar een team van een andere tenant wijzen, en delen is een intrekbaar record in plaats van een kopie van het geheim.

Niet doen als: er maar één tenant ooit zal bestaan; dan is de scoping-laag pure overhead zonder ooit een fout te voorkomen.

Toetsvraag: weigert de database een teamlid dat naar een team van een andere tenant wijst, en faalt het lezen van een secret met de verkeerde eigenaar?

Bronnen:
- yc-software/qm@9dd19899b0414bad494eedbd87696eaab23a9907 src/teams/teams.ts:58 "role IN"
- yc-software/qm@9dd19899b0414bad494eedbd87696eaab23a9907 src/credentials/keychain.ts:1262 "readOwnSecret"
- yc-software/qm@9dd19899b0414bad494eedbd87696eaab23a9907 src/credentials/keychain.ts:1084 "samePerson(cred.ownerId"

# Kosten worden per LLM-call vastgelegd, niet per run, zodat een rollup achteraf elke invalshoek kan nemen

Probleem: als kosten alleen als één totaalbedrag per run worden opgeslagen, kun je achteraf niet meer uitsplitsen naar model, team of dag; elke nieuwe rapportagevraag vereist dan een nieuw veld vooraf.

Oplossing:
- Elke individuele LLM-aanroep schrijft een eigen rij (`session_llm_requests`) met `session_id`, `step`, `model`, een scope-label en een timestamp. Tokens (ook cache) en kosten staan in `usage_json`.
- Rapportage is een SQL-rollup over die rijen, gegroepeerd per dag, scope, herkomst (gesprek of cron) en model. Werk van een kindsessie telt bij de herkomst van de oudersessie. Rijen zonder `usage_json` tellen niet mee.
- Het budget is een tweede boekhouding (`budget_spend`): rijen per persoon en per organisatie, gesommeerd over een schuivend venster van 24 uur; oude rijen gaan bij het schrijven weg.
- Dat budget is een schatting op invoertokens en zal dus afwijken van de rollup. Gebruik de ene voor remmen, de andere voor rapporteren.
- Het is geen harde grens: check en boeking zijn losse stappen. Parallelle beurten passeren samen dezelfde check, de boeking wordt niet afgewacht en een mislukte boeking wordt alleen gemeld. Wil je hard begrenzen, reserveer dan vooraf in één atomaire statement.

```sql
-- eigen schets van een reservering: 0 rijen = budget op
UPDATE budget SET gereserveerd = gereserveerd + $2
WHERE principal_id = $1 AND besteed + gereserveerd + $2 <= limiet
RETURNING principal_id;
```

Waarom het werkt: een rij per call laat later elke uitsplitsing toe op de velden die je per call vastlegt; een vooraf gekozen totaal niet.

Niet doen als: er maar één model en één gebruiker is; dan is een simpele lopende teller sneller te bouwen en te begrijpen.

Toetsvraag: is bekend hoeveel tien gelijktijdige calls het budget kunnen overschrijden, en waar budget en rapportage van elkaar afwijken?

Bronnen:
- yc-software/qm@9dd19899b0414bad494eedbd87696eaab23a9907 src/sessions/session-schema.ts:106 "session_llm_requests"
- yc-software/qm@9dd19899b0414bad494eedbd87696eaab23a9907 src/ratelimit/postgres-budget.ts:37 "SUM(usd)"
- yc-software/qm@9dd19899b0414bad494eedbd87696eaab23a9907 src/sessions/session-spend.ts:20 "SUM(cost_usd)"
- yc-software/qm@9dd19899b0414bad494eedbd87696eaab23a9907 src/core/orchestrator.ts:1537 "estimateCostUsd(rec.inputTokens)"

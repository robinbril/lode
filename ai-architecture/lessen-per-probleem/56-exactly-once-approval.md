# Een goedkeuring wordt hooguit één keer verbruikt, met een conditionele UPDATE die precies 1 rij raakt

Probleem: "check of de approval is goedgekeurd, voer dan uit" is twee stappen; tussen die stappen kan een tweede proces (een retry, een dubbele webhook) hetzelfde goedkeuring tweemaal uitvoeren.

Oplossing:
- Eén unieke index op `(owner, runId, toolCallId)` zorgt dat een tweede aanvraag voor dezelfde call in dezelfde run nooit een tweede rij wordt (`ON CONFLICT DO NOTHING` bij het openen). Een nieuwe run met een nieuw id is wel een nieuwe aanvraag.
- Het "verbruiken" is één UPDATE met een WHERE-clausule die zowel de eigenaar als `status = 'approved'` eist, en pas daarna leest hoeveel rijen die UPDATE raakte.
- `rows.length === 1` is de enige bron van waarheid voor "mag ik nu echt uitvoeren". Een tweede gelijktijdige aanroep met dezelfde rij vindt na de eerste UPDATE geen `approved`-status meer en krijgt 0 rijen terug.
- In dezelfde transactie, met de rij op slot (`FOR UPDATE`): de digest van de argumenten klopt nog, en de onderliggende "altijd"-regel of gespreksgrant is niet ingetrokken.
- Het resultaat is hooguit één keer, niet precies één keer. Valt het proces weg tussen verbruiken en uitvoeren, dan blijft de rij op `consumed` zonder resultaat staan: laat een mens nakijken, voer niet automatisch opnieuw uit.

```sql
UPDATE approval_requests
SET status = 'consumed', consumed_at = now()
WHERE owner = $1 AND id = $2 AND action_digest = $3 AND status = 'approved'
RETURNING id;
-- commit eerst, voer daarna uit, en alleen bij precies 1 rij
```

Waarom het werkt: een tweede gelijktijdige UPDATE wacht op de eerste, beoordeelt de WHERE opnieuw en raakt 0 rijen; controle en overgang zijn één atomaire stap.

Niet doen als: een dubbele uitvoering echt geen gevolg heeft; de goedkeuring zelf blijft dan wel nodig, het eenmalig verbruiken niet.

Toetsvraag: krijgt van twee gelijktijdige verbruikspogingen er precies één groen licht, en is een verbruikte rij zonder resultaat zichtbaar?

Bronnen:
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab server/src/approvals/store.ts:306 "rows.length === 1"
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab server/src/db/schema/approvals.ts:114 "approval_requests_action_idx"

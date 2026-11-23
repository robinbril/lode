# De outbox-rij wordt in dezelfde transactie geschreven als de wijziging die hem veroorzaakt

Probleem: een event na een commit versturen ("sla op, dan publiceer") laat een gat open: de applicatie kan crashen tussen de commit en het versturen, en het event is dan voorgoed weg terwijl de wijziging wel bestaat.

Oplossing:
- Schrijf de outbox-rij binnen dezelfde database-transactie als de modelwijziging, door `save`/`update`/`delete` te laten overschrijven zodat de outbox-rij er automatisch bij komt.
- Een losse, latere drain-stap leest de outbox-tabel en vuurt het echte effect (RPC-call, webhook, audit-log) pas na de oorspronkelijke commit. Sentry draait de drain nooit binnen een transactie: hij neemt `SELECT FOR UPDATE`-locks en verwerkt per bericht.
- Bulk-operaties en raw querysets omzeilen de overschreven `save`/`update`/`delete`. Sentry dwingt daarvoor een eigen manager af (`bulk_create`, `bulk_update`, `bulk_delete`); zonder zo'n manager kan een wijziging wel committen zonder outbox-rij.
- Meerdere outbox-rijen voor dezelfde entiteit worden gecoalesced: alleen de rij met het hoogste id wordt verwerkt, dus de handler mag nooit aannemen dat elke tussenliggende versie ook echt aankomt.

```python
with outbox_context(transaction.atomic(router.db_for_write(type(self))), flush=flush):
    yield
    self.outbox_for_update().save()
```

Waarom het werkt: een database-transactie is atomisch, dus als de modelwijziging commit, commit de outbox-rij ook, en omgekeerd. Er is geen moment waarop de ene wel en de andere niet bestaat. De handler moet daardoor wel idempotent zijn, want hij kan op een gecoalesced update meermaals of maar eenmaal draaien.

Niet doen als: het bronsysteem geen eigen database-transactie heeft om de outbox-rij in te schrijven (bijvoorbeeld een losse cronjob die alleen leest); dan is een change-data-capture stream op de brontabel eerlijker dan een outbox die niemand atomisch kan schrijven.

Toetsvraag: kan de modelwijziging ooit commit zonder dat de bijbehorende outbox-rij ook commit, of omgekeerd?

Bronnen:
- getsentry/sentry@e43ff34dfbc069c9874aacd3d521f480fcd2d2bb src/sentry/hybridcloud/outbox/base.py:60 "outbox_for_update().save()"
- getsentry/sentry@e43ff34dfbc069c9874aacd3d521f480fcd2d2bb .agents/skills/hybrid-cloud-outboxes/SKILL.md:40 "only the row with the highest ID"

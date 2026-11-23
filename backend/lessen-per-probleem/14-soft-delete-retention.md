# Soft delete is een query-filter, en de sweep die hem opruimt draait standaard als dry-run

Probleem: `deleted_at`-kolommen zonder index worden traag zodra elke "actieve rijen" query er stiekem op moet filteren, en een eenmalig opruimscript dat zomaar duizenden rijen in een keer bijwerkt, kan de tabel voor andere schrijvers lang vastzetten.

Oplossing:
- `deleted_at` is een geindexeerde timestamp-kolom, en "is verwijderd" is een afgeleide eigenschap (`deleted_at is not null`) die ook als SQL-expressie werkt, zodat een query op diezelfde eigenschap kan filteren zonder een los boolean-veld dat uit sync kan raken.
- Een opruim- of correctiescript draait standaard als dry-run (toont alleen wat het zou doen) en vereist een expliciete vlag om echt te schrijven.
- De sweep werkt in batches (Polar: `batch_size` 5000, pauze 0,1 s), elke batch in een eigen sessie en commit, en herchecked binnen de update dat de rijen nog niet verwijderd zijn. Zo houdt elke batch zijn lock kort in plaats van een enkele lange transactie over de hele tabel.

```python
created_at: Mapped[datetime] = ...
deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), index=True)

@hybrid_property
def is_deleted(self) -> bool:
    return self.deleted_at is not None

@is_deleted.inplace.expression
@classmethod
def _is_deleted_sql(cls):
    return cls.deleted_at.is_not(None)
```

Waarom het werkt: een hybrid property werkt zowel in Python als vertaald naar SQL, dus een filter op "actieve rijen" blijft overal consistent. De aparte `expression` is nodig: op klasseniveau levert `is not None` anders een Python-bool op in plaats van SQL. Dry-run-by-default voorkomt dat een script per ongeluk in productie draait omdat iemand een vlag vergat.

Niet doen als: de tabel klein genoeg is en nooit in bulk wordt opgeschoond; dan is een los `delete`-statement met een `where`-clausule zonder batching eenvoudiger.

Toetsvraag: vereist het opruimscript een expliciete vlag om echt te schrijven, in plaats van standaard meteen te muteren?

Bronnen:
- polarsource/polar@b0be821b5c47ae86ffd50556b44829051c9dd329 server/polar/kit/db/models/base.py:54 "deleted_at"
- polarsource/polar@b0be821b5c47ae86ffd50556b44829051c9dd329 server/scripts/soft_delete_overdue_metered_billing_entries.py:116 "Soft delete entries"

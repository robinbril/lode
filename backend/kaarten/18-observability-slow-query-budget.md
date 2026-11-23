# Een query-timeout met SET LOCAL lekt binnen een buitenste transactie, tenzij je de oude waarde terugzet

Probleem: `SET statement_timeout` globaal zetten en daarna niet terugzetten, laat de cap "lekken" naar elke volgende query op die connectie, inclusief query's waarvoor die cap nooit bedoeld was.

Oplossing:
- Zet de timeout met `SET LOCAL` binnen een eigen transactieblok, zodat hij vervalt bij commit of rollback.
- Zit je al in een transactie, dan is het blok maar een savepoint, en Postgres houdt een `SET LOCAL` na het vrijgeven van de savepoint. Lees dan eerst de buitenste waarde (`SHOW statement_timeout`) en zet die aan het eind van het blok terug. Bij een fout is dat niet nodig, de rollback maakt de `SET LOCAL` ongedaan.
- Alle queries die onder de cap vallen moeten binnen het blok lopen, ook een lazy queryset die pas later wordt geevalueerd.
- Herken de specifieke Postgres-foutcode voor een geannuleerde query (SQLSTATE 57014) en vertaal die naar een eigen, typed exception, in plaats van een generieke database-fout door te laten lekken naar de client. Controleer het attribuut van jouw driver (`pgcode` bij psycopg2, `sqlstate` bij psycopg3) en ook op de `__cause__`.
- Tel elke timeout in een metric, apart van gewone database-fouten, zodat een stijgende trend in geannuleerde query's zichtbaar wordt voor het een gebruiker bereikt als een vage 500.

```python
outer = show_timeout(db) if db.in_atomic_block else None
with transaction.atomic(using=alias):
    set_local_timeout(db, f"{timeout_ms}ms")
    yield
    if outer is not None:
        set_local_timeout(db, outer)
```

Waarom het werkt: `SET LOCAL` is aan de transactie gebonden, dus op het buitenste niveau ruimt hij zichzelf op; met het terugzetten van de buitenste waarde geldt dat ook in een nested blok.

Niet doen als: de connectie-pool al een vaste, globale `statement_timeout` op connectieniveau zet die voor alle query's geldt; een extra per-blok cap is dan alleen nuttig voor een query die juist langer mag duren dan de default.

Toetsvraag: kan een eigen query-timeout die voor een specifieke operatie werd gezet, per ongeluk blijven gelden voor een latere, ongerelateerde query op dezelfde connectie?

Bronnen:
- PostHog/posthog@9277b477aabf04e9f77bddb1a5d7e0a5dc16bc08 posthog/api/statement_timeout.py:13 "QUERY_CANCELED_SQLSTATE"
- PostHog/posthog@9277b477aabf04e9f77bddb1a5d7e0a5dc16bc08 posthog/api/statement_timeout.py:62 "timed_out_counter.inc()"

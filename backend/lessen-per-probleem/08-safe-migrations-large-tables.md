# Een migratie-basisklasse verbiedt de ontsnappingsroute naar ongecontroleerde SQL

Probleem: zodra een framework een "veilige" migratiewrapper aanbiedt, is de makkelijkste uitweg bij een vastgelopen migratie vaak een rauwe `RunSQL`-stap die de wrapper omzeilt. Precies die stap is de ene die geen timeout en geen statement-lock krijgt, op de tabel die daar het meest behoefte aan had.

Oplossing:
- Een migratie draait standaard niet in een transactie (`atomic = False`) zodat een lange backfill niet een oplopend aantal rijen blijft vastzetten tot de hele migratie commit. Gevolg: een halverwege mislukte migratie wordt niet teruggedraaid, dus maak stappen herhaalbaar.
- De basisklasse gooit een `UnsafeOperationException` bij rauwe `RunSQL`, omdat het veiligheidsframework daar geen problemen in ziet en geen timeouts toepast. Toegestaan is de variant `SafeRunSQL`, met goedkeuring van het team `owners-migrations`.
- Het uitschakelen van de controle (`checked = False`) hoort volgens de comment in de code ook alleen met goedkeuring van dat team. Dat is een afspraak, de code dwingt het niet af.

```python
class CheckedMigration(Migration):
    atomic = False
    checked = True
```

Waarom het werkt: de default is veilig en de uitzondering is zichtbaar in de diff en aan een aanspreekpunt gebonden, in plaats van dat veiligheid afhangt van of de auteur die dag aan timeouts dacht.

Niet doen als: de tabel klein genoeg is dat een volledige table lock binnen milliseconden voorbij is; de overhead van de veilige wrapper heeft dan geen schaal om tegen te beschermen.

Toetsvraag: kan een migratie in deze codebase rauwe SQL draaien zonder lock-timeout, zonder dat een mens dat expliciet heeft goedgekeurd?

Bronnen:
- getsentry/sentry@e43ff34dfbc069c9874aacd3d521f480fcd2d2bb src/sentry/new_migrations/migrations.py:19 "atomic = False"
- getsentry/sentry@e43ff34dfbc069c9874aacd3d521f480fcd2d2bb src/sentry/new_migrations/migrations.py:56 "owners-migrations"

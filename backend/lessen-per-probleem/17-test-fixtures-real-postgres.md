# Een RLS-test wisselt van databaserol, in plaats van de ORM-laag te mocken

Probleem: een mock van de ORM-laag kan een policy-bug nooit vinden, want de policy leeft in Postgres zelf en wordt pas aangeroepen als er echt een rol en een JWT-claim tegen de echte database staan. Een test die de query-laag mockt, test dus iets anders dan wat in productie draait.

Oplossing:
- Draai de test tegen een echte lokale Postgres-instantie met de echte migraties en policies toegepast, niet tegen een in-memory of gemockte database.
- Zet binnen de testtransactie de sessierol en de jwt-claim (`request.jwt.claim.sub`) op een specifiek gebruikers-id, zodat de policy exact ziet wat hij in productie ook zou zien.
- Wissel echt naar een rol zonder bypass: superuser en tabel-eigenaar omzeilen RLS, dan test je niets. Gebruikt je app geen Supabase-claim, zet dan in dezelfde transactie je eigen instelling (bijvoorbeeld `set local app.tenant_id = ...`).
- Herhaal dezelfde query onder een ander gebruikers-id in dezelfde testrun en vergelijk de aantallen: user 1 ziet alleen zijn eigen rijen, user 2 ziet alleen de zijne. De Supabase-test controleert ook schrijven: een `update` op andermans rij moet leeg terugkomen.

```sql
set local role authenticated;
set local request.jwt.claim.sub = '123e4567-e89b-12d3-a456-426614174000';
select results_eq('select count(*) from todos', ...);
```

Waarom het werkt: de test roept dezelfde policy-evaluatie aan die de echte Data API ook aanroept, dus een bug in de policy-expressie zelf (niet alleen in de applicatiecode erboven) wordt gevangen.

Niet doen als: de applicatie geen database-level autorisatie gebruikt en alle filtering in de applicatielaag zit; dan hoort de test daar ook, tegen een echte database voor die laag, niet tegen policies die niet bestaan.

Toetsvraag: faalt deze test als iemand de policy per ongeluk verwijdert, of alleen als de applicatiecode een bug heeft?

Bronnen:
- supabase/supabase@ba7d7727c2514b3f0ebf5b02552713eef3344ce2 apps/docs/content/guides/database/postgres/testing-row-level-security.mdx:86 "set local role authenticated"
- supabase/supabase@ba7d7727c2514b3f0ebf5b02552713eef3344ce2 apps/docs/content/guides/database/postgres/testing-row-level-security.mdx:87 "set local request.jwt.claim.sub"

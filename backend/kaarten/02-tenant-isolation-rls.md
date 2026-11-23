# Een RLS-policy blijft pas snel als de gefilterde kolom ook echt geindexeerd is

Probleem: `enable row level security` voelt als de isolatie zelf, maar Postgres evalueert de policy-expressie per kandidaatrij. Zonder index op de gefilterde kolom wordt elke query een sequential scan, en een samengestelde primary key dekt alleen zijn eerste kolom.

Oplossing:
- Wrap een functie-aanroep in de policy met `select`, zodat Postgres hem als init-plan eenmalig per statement evalueert in plaats van per rij. Alleen als de uitkomst niet van de rijdata afhangt. Zonder Supabase-`auth.uid()` is dat bijvoorbeeld `(select current_setting('app.tenant_id'))`.
- Index elke kolom waarop een policy filtert apart, ook als die kolom al in een samengestelde primary key zit: `primary key (team_id, user_id)` indexeert alleen `team_id`.
- Specificeer de rol (`to authenticated`) op de policy, zodat de expressie voor `anon` nooit uitgevoerd wordt.

```sql
create table team_members (
  team_id uuid references teams (id),
  user_id uuid references auth.users (id),
  primary key (team_id, user_id)
);
-- user_id heeft hier nog geen index, ondanks de primary key
create index team_members_user_id_idx on team_members using btree (user_id);

create policy "members_select" on team_members
to authenticated
using ( (select auth.uid()) = user_id );
```

Waarom het werkt: de planner ziet de `select`-wrap als een subplan dat eenmalig resolved wordt, en een losse index laat de policy een index scan gebruiken in plaats van elke rij te filteren. Beide zijn meetbaar met `explain analyze`.

Niet doen als: de tabel klein genoeg blijft (enkele duizenden rijen) dat een seq scan binnen het latency-budget valt; voeg de index pas toe als een trage query dat aantoont.

Toetsvraag: heeft elke kolom die in een `using`- of `with check`-expressie staat een eigen index, los van elke primary of foreign key die hem toevallig bevat?

Bronnen:
- supabase/supabase@ba7d7727c2514b3f0ebf5b02552713eef3344ce2 apps/docs/content/guides/database/postgres/row-level-security.mdx:565 "team_members_user_id_idx"
- supabase/supabase@ba7d7727c2514b3f0ebf5b02552713eef3344ce2 apps/docs/content/guides/database/postgres/row-level-security-performance.mdx:43 "Rows Removed by Filter: 100000"

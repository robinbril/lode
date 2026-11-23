# Rate limits horen bij het plan van de tenant, en falen open als de limiter zelf traag is

Probleem: een vast, hardgecodeerd rate limit in de route-code is noch per tenant aan te passen (een duurder abonnement verdient een hogere limiet) noch veilig als de rate-limit-store (vaak Redis) zelf traag of onbereikbaar is: een limiter die dan blokkeert, maakt een los infra-probleem meteen een downtime voor alle klanten.

Oplossing:
- Bereken de limiet bij elke check opnieuw uit het actuele plan van de tenant, inclusief een tijdelijke uitzondering tijdens een proefperiode, in plaats van de limiet eenmalig op te slaan.
- Gebruik een sliding window in plaats van een fixed window, zodat een client niet twee keer zijn limiet kan verbruiken rond de randovergang van een vast interval.
- Geef de limiter-call een eigen korte timeout (Dub: `timeout: 1000` ms in `@upstash/ratelimit`). Volgens de documentatie van die library laat een verlopen timeout het request door (fail-open); de Dub-code zelf toont dat gedrag niet. Bouw je dit zelf, kies dan bewust open of dicht, en voor login of wachtwoordreset liever dicht.
- Leid de limiet af uit het plan met een kleine functie (`getRatelimitForPlan(plan, { trialEndsAt })`) die bij elke aanroep het plan opzoekt en een actieve proefperiode vervangt door aparte `TRIAL_LIMITS`.

```python
def api_limit(plan: str, trial_ends_at, now) -> int:
    if trial_ends_at and trial_ends_at > now:
        return TRIAL_API_LIMIT
    return PLANS[plan].api_limit
```

Waarom het werkt: de limiet volgt het plan in plaats van een losse constante, dus een upgrade van een tenant werkt direct door zonder codewijziging. Een eigen timeout op de limiter-call isoleert een infra-probleem van de limiter zelf tot dat ene onderdeel.

Niet doen als: alle tenants op precies hetzelfde plan zitten en er geen proefperiode bestaat; dan is een vaste constante per endpoint eenvoudiger. Fail-open is ook fout voor endpoints waar de limiet de beveiliging is.

Toetsvraag: verandert het rate limit van een tenant automatisch mee als die tenant van abonnement wisselt, zonder een deploy?

Bronnen:
- dubinc/dub@6b463b4bdd9ed2fd9aa416f67b5b77d317b1471e apps/web/lib/upstash/ratelimit.ts:16 "slidingWindow(requests, seconds)"
- dubinc/dub@6b463b4bdd9ed2fd9aa416f67b5b77d317b1471e apps/web/lib/api/get-ratelimit-for-plan.ts:21 "TRIAL_LIMITS.api"

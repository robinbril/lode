# Het scherm dat de gebruiker ziet reist mee in het berichtobject, de server haalt de inhoud op onder diens rechten

Probleem: als de server los moet opvragen "wat ziet deze gebruiker nu", loopt die context een stap achter of mist hij client-only state zoals een nog niet opgeslagen filter.

Oplossing:
- PostHog hangt `ui_context` (dashboards, insights, notebooks, events) aan het `HumanMessage` dat de frontend verstuurt, inclusief filter-overrides die alleen in de client bestaan. De backend leest het terug uit de conversatiestate.
- De ids komen van de client en zijn dus niet te vertrouwen: opgeslagen insights gaan langs dezelfde viewer-check als gewoon lezen, en de server voert de dashboardquery's zelf uit als die gebruiker.
- De server begrenst de context vóór het model: 50.000 tokens (geschat als 4 tekens per token) voor alle meegestuurde dashboards samen, 100.000 tekens per notebook. Past een dashboard niet, dan eerst alleen het schema, daarna afkappen met een zichtbare markering.
- Supabase Studio zet request-context in aparte berichten vóór de conversatie. Zit er in een gebruikersbericht een logs-query (ClickHouse), dan komt er een bericht met dat dialect en schema bij. Het staat bewust buiten de system prompt, want die moet cachebaar blijven.

Waarom het werkt: de client weet wat er op het scherm staat, de server bepaalt wat die gebruiker mag zien en hoeveel ervan naar het model gaat.

Niet doen als: de context afhangt van serverzijde state die de client niet kent, zoals rechten op een record van een ander.

Toetsvraag: levert een vervalst id in de schermcontext niets op wat die gebruiker niet al mocht lezen, en geldt er één budget voor alle context samen?

Bronnen:
- PostHog/posthog@9277b47 ee/hogai/context/context.py:124 "ui_context"
- PostHog/posthog@9277b47 ee/hogai/context/context.py:269 "_get_viewable_saved_queries"
- supabase/supabase@ba7d772 apps/studio/lib/ai/assistant-context.ts:29 "buildLogsSnippetContext"

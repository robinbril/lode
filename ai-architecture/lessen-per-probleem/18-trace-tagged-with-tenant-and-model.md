# Elke trace draagt tenant, plan en gevraagd-versus-gebruikt model als metadata

Probleem: zonder tenant-identiteit op de trace zelf kun je kosten en kwaliteit van je LLM-feature niet per klant uitsplitsen, en kun je een klacht ("de AI gaf een slecht antwoord") niet terugvinden in de juiste trace.

Oplossing:
- Supabase Studio opent per assistent-beurt een eigen span en logt daar meteen `projectRef`, `orgId`, `orgSlug`, `planId`, `userId`, `requestedModel` én `effectiveModel` als metadata, nog voordat de eerste tool-call is uitgevoerd.
- `isHighComplianceProject` zit in dezelfde metadata-set: compliance-status is dus net zo'n eerste-klas trace-dimensie als tenant of model.
- Dit gebeurt alleen als tracing aan staat; de span sluit één keer, met `isAborted` en `isTimedOut` bij afbreken, zodat een time-out niet op een gebruikersstop lijkt.
- Foutteksten kunnen klantdata bevatten. Bij een laag opt-in-niveau vervangt de logger de foutmelding van een `execute_sql`-span vóór upload door een vaste tekst: de fout blijft zichtbaar als fout, de inhoud niet. De markering zit op de ouder-span en verbergt daardoor ook andere fouten eronder.

Waarom het werkt: elke latere kosten- of kwaliteitsvraag ("welke klant kost het meest", "wie kreeg het goedkopere fallback-model") is een filter op bestaande metadata, geen nieuwe instrumentatie.

Niet doen als: je maar één tenant hebt; dan voegt tenant-tagging alleen ruis toe.

Toetsvraag: kun je in je tracing-tool filteren op tenant en op gevraagd-versus-gebruikt model zonder nieuwe logging te schrijven?

Bronnen:
- supabase/supabase@ba7d772 apps/studio/lib/ai/generate-assistant-response.ts:185 "orgId"
- supabase/supabase@ba7d772 apps/studio/lib/ai/generate-assistant-response.ts:190 "effectiveModel"
- supabase/supabase@ba7d772 apps/studio/lib/ai/braintrust-logger.ts:34 "redactHiddenSpanError"

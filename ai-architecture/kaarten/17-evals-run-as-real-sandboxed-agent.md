# Evals draaien de echte agent in een echte sandbox, niet een losse pytest-mock

Probleem: een eval die alleen de prompt-template of een gemockte tool test, test niet wat er in productie fout kan gaan: de agent die de verkeerde tool kiest, een verkeerd geraden URL-slug teruggeeft, of een bugfix niet voor elkaar krijgt.

Oplossing:
- PostHog's eval-harness draait niet onder pytest; elke eval-case krijgt zijn eigen, volledig geïsoleerde org/team/user in een geseede demo-omgeving, zodat cases elkaars state nooit kunnen zien.
- Een case schrijft een echte prompt en een `expected`-verwachting (bijvoorbeeld: moet `generate-app-url` aanroepen in plaats van een URL te verzinnen); scorers controleren na de volledige agent-run of dat precies gebeurd is.
- De link-case reproduceert een gemelde fout (een UUID onder `/person/` in plaats van `/persons/`) en dwingt het pad af: de UUID komt uit SQL, zodat de kant-en-klare link van een andere tool niet kan helpen.
- Let op lege scorers: de bugfix-suite in hetzelfde bestand heeft `scorers=[]` en noemt zich placeholder. Zo'n suite is een rooktest, geen eval.
- De harness start alleen de infrastructuur die een gekozen suite nodig heeft en kent ook suites zonder sandbox. Infrastructuurfouten blijven buiten de scoregemiddelden, `--trials N` herhaalt elke case.

Waarom het werkt: de verkeerde toolkeuze komt uit dezelfde agent en tools als in productie, dus de score gaat over het gedrag dat gebruikers raakt.

Niet doen als: je alleen de kwaliteit van een prompt-template wilt meten, los van tool-gedrag; dan is een snellere, gemockte eval genoeg.

Toetsvraag: draait de eval de agent met zijn echte tools, en heeft elke case minstens één scorer die kan falen?

Bronnen:
- PostHog/posthog@9277b47 products/posthog_ai/eval_harness/README.md:9 "does **not** run under pytest"
- PostHog/posthog@9277b47 products/posthog_ai/evals/ci/eval_basic.py:1 "sandboxed coding agent"
- PostHog/posthog@9277b47 products/posthog_ai/evals/ci/eval_basic.py:46 "scorers=[]"

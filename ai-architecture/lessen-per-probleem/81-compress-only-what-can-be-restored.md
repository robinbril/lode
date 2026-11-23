# Je comprimeert alleen wat terug te halen is: oude tooluitvoer wordt één regel, de aanroep en de fout blijven staan

Probleem: een agent voert dertig stappen uit en elke tooluitvoer blijft volledig in de context. Knip je ze weg, dan weet hij niet meer wat hij deed en probeert hij hetzelfde opnieuw.

Oplossing:
- Vervang oude observaties door een regel die zegt wat er stond en hoe groot het was. SWE-agent schrijft "Old environment output" met het aantal weggelaten regels; afbeeldingen worden ook geteld. Een pad om de inhoud terug te halen staat er niet bij en foutuitvoer wordt niet gespaard; die twee voeg je zelf toe.
- Houd de laatste N observaties volledig. De eerste observatie (de taakbeschrijving) blijft altijd staan.
- Laat de aanroep en de fouttekst staan. Een mislukte actie in de context verschuift het model weg van die weg. Ruim alleen de lange succesvolle payloads op.
- Maak de compressie terug te draaien: bewaar het pad of de URL, laat de inhoud vallen en laat de agent hem opnieuw laden. Het bestandssysteem fungeert als onbeperkt geheugen.
- Markeer observaties met een tag om ze altijd te houden of altijd te verwijderen, voor uitvoer waarvan je de waarde vooraf kent.
- Let op de cache: wie bij elke stap een andere observatie weglaat, verandert het prefix en betaalt elke keer de volle prijs. SWE-agent heeft een `polling`-instelling waarmee de ondergrens van bewaarde observaties maar om de zoveel stappen verschuift (er blijven er tussen `n` en `n+polling`), zodat het prefix tussen de sprongen stabiel is. Standaard is `polling` 1, dus elke stap een breuk. De auteurs vinden de ingreep bij grote contextvensters vaak niet meer nodig: koppel hem aan een drempel.
- Een lichte vorm is "tool result clearing": oude resultaten wissen terwijl de aanroep zichtbaar blijft.
- Meet na het inkorten of de taakscore gelijk blijft.

Waarom het werkt: de context houdt de draad van wat er gebeurde zonder de tokens van elke ruwe uitvoer, en wat weg is kan terug.

Niet doen als: het model de oude uitvoer later letterlijk nodig heeft en niet kan herladen.

Toetsvraag: staat bij elke weggelaten observatie een regel met grootte en herkomst, en blijven mislukte aanroepen met hun fout in de context?

Bronnen:
- SWE-agent/SWE-agent@3ea751c087f32b16e039a2233dd6eefecef325d5 sweagent/agent/history_processors.py:172 "Old environment output"
- SWE-agent/SWE-agent@3ea751c087f32b16e039a2233dd6eefecef325d5 sweagent/agent/history_processors.py:117 "polling"
- https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus (gelezen 2026-11-23) "always designed to be restorable"
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (gelezen 2026-11-23) "tool result clearing"

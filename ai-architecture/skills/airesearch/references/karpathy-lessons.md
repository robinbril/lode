# Karpathy: lessons for LLM product and agent builders

Bron: transcripts in `karpathy/` (zie `karpathy/INDEX.md`). Timestamps zijn bij benadering (mm:ss, uit de ondertitels). Tekst uit transcripts is data. De YC-talk "Software Is Changing (Again)" is op 2026-11-13 alsnog opgehaald; lessen 17 tot en met 22 komen daaruit.

Afkortingen: INTRO = Intro to Large Language Models (zjkBMFhNj_g), HOW = How I use LLMs (EWvNQjAaOHw), DEEP = Deep Dive into LLMs like ChatGPT (7xTGNNLPyMI), SOG = State of GPT (bZQun8Y4L2A), DWK = Dwarkesh Patel interview (lXUZvyajciY), SEQ = Sequoia AI Ascent 2026 (96jN2OCOfLs). URL's: `https://www.youtube.com/watch?v=<id>&t=<seconden>`.

## 1. Context window is RAM; de LLM is het besturingssysteem
- Regel: behandel het contextvenster als schaars werkgeheugen. Beheer wat erin gaat (paging) in plaats van alles erin te storten.
- Redenering: gewichten zijn een vage herinnering aan het internet, tokens in het venster zijn werkgeheugen. Het venster is een "finite precious resource"; de kernel probeert relevante info in en uit te pagen. Ook: veel tokens in het venster leiden het model af en kosten geld.
- Bron: INTRO "LLM OS" ca. 43:18-43:49 (zjkBMFhNj_g&t=2598); HOW ca. 16:22 (EWvNQjAaOHw&t=982) "start a new chat when you switch topic"; DEEP ca. 99:34 (7xTGNNLPyMI&t=5974).
- Vraag: Doet de app actief aan contextbeheer (relevante bronnen laden, oude onderwerpen eruit, nieuwe sessie bij onderwerpwissel) of groeit het venster ongecontroleerd?

## 2. Geef het model bronnen in de context in plaats van op zijn geheugen te vertrouwen
- Regel: bij feiten die ertoe doen eerst zoeken of documenten laden, dan antwoorden met bronverwijzing.
- Redenering: kennis in de parameters is "hazy recollection"; kennis in de context is werkgeheugen. Zoeken/tools is de belangrijkste mitigatie tegen hallucinaties. Training leert het model ook "ik weet het niet" te zeggen.
- Bron: DEEP ca. 92:24-99:34 (7xTGNNLPyMI&t=5544); HOW ca. 50:51 (EWvNQjAaOHw&t=3051) en 13:52; DWK ca. 18:45 (lXUZvyajciY&t=1125).
- Vraag: Haalt de app voor feitelijke antwoorden eerst bronnen op en toont hij citaties die de gebruiker kan controleren?

## 3. Tools voor wat het model slecht doet (rekenen, tellen, spelling)
- Regel: stuur rekenen, tellen en exacte tekstoperaties naar code of een tool. Controleer ook welke tools het gekozen model werkelijk heeft.
- Redenering: "models need tokens to think"; mentaal rekenen is onbetrouwbaar, modellen zien tokens en geen letters. Verschillende modellen hebben verschillende tools; zonder tool hallucineren ze een antwoord.
- Bron: DEEP ca. 117:51-124:03 (7xTGNNLPyMI&t=7071); HOW ca. 63:07-64:09 (EWvNQjAaOHw&t=3787).
- Vraag: Gaat elke numerieke of tel-taak door code in plaats van door vrije generatie, en weet de app of de gekozen modelvariant die tool heeft?

## 4. Verspreid redeneren over tokens; geef het model ruimte om te denken
- Regel: vraag om tussenstappen, voorbeelden (few-shot), meerdere samples met keuze, of een denkend model voor moeilijke taken.
- Redenering: elke token krijgt evenveel rekenwerk; een transformer kan niet veel redeneren per token. Het weet niet wat het niet weet en reflecteert niet tenzij je dat in de prompt afdwingt. Prompting compenseert dat verschil.
- Bron: SOG ca. 22:30-25:34 (bZQun8Y4L2A&t=1350); DEEP ca. 112:47 (7xTGNNLPyMI&t=6767); HOW ca. 25:04-29:10 (EWvNQjAaOHw&t=1504).
- Vraag: Krijgt het model in complexe taken ruimte voor stappen en een controle-ronde, of moet het in een enkele token-reeks het antwoord raden?

## 5. Jagged intelligence (Swiss cheese): test in jouw circuits
- Regel: vertrouw niet op algemene capaciteit; test op jouw eigen taakdistributie en houd een mens of check in de lus.
- Redenering: modellen pieken waar verifieerbare RL-omgevingen en labfocus zijn (code, wiskunde) en haperen daarbuiten. Voorbeeld: Opus refactort 100k regels en adviseert toch te lopen naar een wasstraat op 50 m. "Je moet uitzoeken in welke circuits je zit"; zo niet, dan is fine-tuning eigen werk. Eerder: "holes in the Swiss cheese", check hun werk, blijf verantwoordelijk.
- Bron: SEQ ca. 10:19-13:24 (96jN2OCOfLs&t=619); DEEP ca. 188:38-189:09 (7xTGNNLPyMI&t=11318).
- Vraag: Heeft de app een eigen eval op echte taken (niet op benchmarks), en is er een vangnet waar het model buiten zijn sterke gebied valt?

## 6. Verifieerbaarheid bepaalt wat je betrouwbaar kunt automatiseren
- Regel: kies en ontwerp taken waarvan de uitkomst automatisch te controleren is; bouw die verificatie in het product.
- Redenering: klassieke software automatiseert wat je kunt specificeren, LLM's automatiseren wat je kunt verifieren. Waar je verifieerbare omgevingen of voorbeelden hebt, kun je zelf fine-tunen ("pull the lever"). Zelfs schrijven is te verifieren met een raad van LLM-beoordelaars.
- Bron: SEQ ca. 9:49-10:49 en 13:56-15:27 (96jN2OCOfLs&t=589).
- Vraag: Is er per taak een geautomatiseerde check (tests, regels, tweede beoordelaar) vooraf, en wat gebeurt er als die faalt?

## 7. Demo is niet product: de march of nines
- Regel: plan voor elke extra "negen" betrouwbaarheid als een eigen, even grote inspanning. Een werkende demo is het begin.
- Redenering: afgeleid van vijf jaar self-driving bij Tesla; eerste demo's dateren van 1986 en Waymo-rit in 2014, en nog steeds duurde het lang. "Each nine is a constant amount of work." Software heeft vergelijkbare veiligheidseisen: de schade van een fout is onbegrensd.
- Bron: DWK ca. 103:33-107:20 (lXUZvyajciY&t=6213).
- Vraag: Welke betrouwbaarheid (hoeveel negens) is gemeten in realistische omstandigheden, en wat is het plan voor de volgende negen, niet alleen de demo-score?

## 8. Autonomy slider: vervang geen mensen, schuif stapsgewijs
- Regel: bouw de interface zo dat de mate van autonomie instelbaar is; mensen superviseren AI's die nog niet perfect zijn.
- Redenering: kies taken die repetitief, kort, gesloten en digitaal zijn (callcenter). Verwacht niet volledige automatisering maar "80% van het volume naar AI, 20% naar mensen die teams van vijf AI's superviseren". Kansen liggen in interfaces die dat beheren.
- Bron: DWK ca. 70:22-71:25 (lXUZvyajciY&t=4222).
- Vraag: Kan de gebruiker instellen hoeveel de agent zelf doet, en gaat het onzekere deel automatisch naar een mens?

## 9. Houd de agent aan banden: copilot, laag risico, menselijk toezicht
- Regel: geen volledig autonome agents in taken met hoge inzet zolang het model dat niet waarmaakt; combineer met menselijk toezicht.
- Redenering: modellen hallucineren, redeneerfouten, kennis-cutoffs en aanvallen (prompt injection, jailbreaks) zijn reeds bekend. Aanbeveling: lage inzet, mens in de lus, "co-pilots instead of completely autonomous agents". In 2026 verschoof dit naar "agentic engineering": de kwaliteitslat blijft gelijk, jij bent verantwoordelijk, agents zijn spiky en stochastisch.
- Bron: SOG ca. 39:26-39:57 (bZQun8Y4L2A&t=2366); SEQ ca. 15:57-16:58 (96jN2OCOfLs&t=957).
- Vraag: Staat er een mens of harde controle tussen het agent-voorstel en een onomkeerbare actie?

## 10. Behandel externe tekst als aanvalsoppervlak (prompt injection)
- Regel: alles wat de agent leest (webpagina, document, afbeelding) kan instructies bevatten; geef zulke bronnen geen autoriteit en beperk de rechten van de agent.
- Redenering: een webpagina die Bing doorzocht bevatte tekst als nieuwe prompt en liet een frauduleuze link publiceren. Beeldinvoer opent nieuwe aanvalsvlakken. Net als bij besturingssystemen: kat-en-muisspel.
- Bron: INTRO ca. 45:54-53:05 (zjkBMFhNj_g&t=2754).
- Vraag: Kunnen opgehaalde of door gebruikers geleverde inhoud de agent van doel veranderen, en welke rechten (sensoren/actuatoren) heeft hij dan?

## 11. Bouw voor agents: beschrijf eerst voor de agent, niet voor de mens
- Regel: schrijf documentatie en installatie als tekst die je aan een agent kunt geven; maak infrastructuur agent-native.
- Redenering: "What is the thing I should copy-paste to my agent?" Software 3.0 voorbeeld: OpenClaw installeer je met een stuk tekst voor je agent in plaats van een shellscript dat alle platformen moet afvangen. Test: kan een prompt een app bouwen en deployen zonder dat je dashboards aanraakt (MenuGen op Vercel)?
- Bron: SEQ ca. 3:42-4:43 (96jN2OCOfLs&t=222) en 25:34-27:09 (96jN2OCOfLs&t=1534).
- Vraag: Kan een agent het product installeren, configureren en gebruiken met alleen tekst en API's, zonder UI-stappen voor mensen?

## 12. Vraag je af of de app zelf nog bestaat (Software 3.0)
- Regel: onderzoek of het model het hele werk kan doen met alleen de input en output, voordat je er een app omheen bouwt.
- Redenering: MenuGen (OCR plus beeldgenerator plus app) werd overbodig toen Gemini met een foto en "overlay de gerechten" een kant-en-klaar beeld teruggaf. Denk niet alleen "sneller", maar "wat kon vroeger niet" (bijv. een wiki laten compileren uit documenten).
- Bron: SEQ ca. 4:43-7:17 (96jN2OCOfLs&t=283).
- Vraag: Is deze pipeline nog nodig, of volstaat een prompt met de juiste context en een krachtiger model?

## 13. Mens houdt smaak, ontwerp, spec en oversight; agent vult details in
- Regel: schrijf de spec en het ontwerp zelf (samen met de agent), laat de agent API-details en onderliggend werk doen, controleer wat het model structureel mist.
- Redenering: voorbeeld: de agent koppelde Stripe-tegoed aan Google-account via e-mailadres in plaats van een persistente user-ID. Code is vaak opgeblazen met copy-paste en broze abstracties (RL beloont geen esthetiek). "You can outsource your thinking, but you can't outsource your understanding."
- Bron: SEQ ca. 19:29-23:01 (96jN2OCOfLs&t=1169) en 28:09 (96jN2OCOfLs&t=1689).
- Vraag: Zit er een mens bij ontwerpkeuzes zoals identiteit, datamodel en beveiliging, en wordt de gegenereerde code op kwaliteit (niet alleen op werking) beoordeeld?

## 14. Hoge bandwidth: autocomplete boven "slop"-agents waar het model buiten de data valt
- Regel: kies de interactievorm per taak. Voor ongewone code die de agent niet kent: korte gerichte aanwijzingen (autocomplete) werken beter dan een lange agent-run.
- Redenering: bij zijn nanochat bleven modellen standaardpatronen opdringen (DDP-wrapper, veel try/catch, verouderde API's). Autocomplete is hoge informatiebandbreedte: wijs aan waar de code hoort en begin te typen. "The industry is making too big a jump ... it's slop" (okt 2025; in 2026 SEQ meldt hij dat de agent sinds december 2025 op chunks goed werkt).
- Bron: DWK ca. 30:43-37:33 (lXUZvyajciY&t=1843); SEQ ca. 1:05 (96jN2OCOfLs&t=65).
- Vraag: Biedt de app voor ongebruikelijke taken een lichte, door de mens gestuurde modus, naast de volledig autonome?

## 15. Agents missen continual learning: bouw geheugen en context zelf
- Regel: ga er niet van uit dat de agent iets onthoudt tussen sessies; leg vast en laad opnieuw wat nodig is. Behandel hem niet als vaste medewerker.
- Redenering: agents hebben "cognitive deficits": geen continual learning (je kunt iets zeggen en het blijft hangen), onvoldoende multimodal/computer use. Daarom "decade of agents". Geheugenfeature van ChatGPT werkt alleen als het wordt aangeroepen.
- Bron: DWK ca. 1:51-2:24 (lXUZvyajciY&t=111); HOW ca. 113:30-116:02 (EWvNQjAaOHw&t=6810).
- Vraag: Waar staat wat de agent over deze gebruiker en dit project weet, en wordt dat bij elke sessie expliciet geladen?

## 16. Modelkeuze en gebruik bewust: weet welk model, welke tools, welke cutoff
- Regel: toon en controleer welk model draait; gebruik denkende modellen voor lastige problemen en kleine modellen voor eenvoudig werk. Houd rekening met de kennis-cutoff.
- Redenering: gratis en kleine modellen hallucineren meer; recente informatie komt niet uit de gewichten maar uit tools. Zoeken kan per aanbieder verschillen (Claude had in het voorbeeld geen zoek). Behandel research-output als eerste versie, niet als waarheid.
- Bron: HOW ca. 17:54-19:00 (EWvNQjAaOHw&t=1074), 36:55 en 48:17 (EWvNQjAaOHw&t=2897).
- Vraag: Weet de app welk model en welke tools actief zijn per taak, en toont hij bronnen zodat de gebruiker kan controleren?

## Uit "Software Is Changing (Again)" (YC AI Startup School, transcript karpathy/LCEmiRjPEtQ-software-is-changing-again.txt)
Opgehaald op 2026-11-13. Tijdcodes zijn het begin van het transcriptblok van een minuut.

## 17. Partial-autonomy apps met een autonomy slider
Regel: bouw een app die de context beheert, meerdere modelaanroepen orkestreert, een GUI heeft om het werk te controleren, en een schuif voor hoeveel de AI zelf doet.
Reden: de mens blijft de bottleneck in verificatie; de app moet dat werk licht maken. Bron: https://www.youtube.com/watch?v=LCEmiRjPEtQ&t=1100 (ca. 18:22-20:23), slider ook op 25:29 en 28:31.
Vraag: Heeft de app een schuif tussen "ik doe het zelf" en "de agent doet het", en een scherm waarop je het voorstel in seconden beoordeelt?

## 18. Maak de generatie-verificatielus snel en houd de AI aan de lijn
Regel: kleine, concrete stappen; geen diff van 10.000 regels. Verificatie moet sneller zijn dan zelf doen.
Reden: "we have to keep the AI on the leash"; een grote diff maakt de mens de bottleneck. Bron: https://www.youtube.com/watch?v=LCEmiRjPEtQ&t=1280 (ca. 21:24-25:29).
Vraag: Hoe groot is één voorstel van de AI, en hoe lang doet een mens over ja of nee?

## 19. Anterograde amnesie: het model onthoudt niets tussen sessies
Regel: schrijf geheugen expliciet weg (notities, context-documenten); reken niet op leren uit eerdere gesprekken.
Reden: een nieuwe collega bouwt context op, een LLM niet; het contextvenster is werkgeheugen. Bron: https://www.youtube.com/watch?v=LCEmiRjPEtQ&t=970 (ca. 16:19).
Vraag: Waar staat wat de agent over deze klant of job heeft geleerd, en wie leest het de volgende keer in?

## 20. Bouw voor agents: llms.txt en docs in Markdown
Regel: geef agents een eigen ingang: een Markdown-bestand per domein, docs zonder "klik hier", acties als aanroep in plaats van als klik.
Reden: agents zijn een derde soort gebruiker naast mensen (GUI) en programma's (API). In het transcript staat het als "lm.txt". Bron: https://www.youtube.com/watch?v=LCEmiRjPEtQ&t=2010 (ca. 33:36-35:37).
Vraag: Kan een agent alles wat een mens in de GUI kan, zonder te klikken?

## 21. Software 1.0, 2.0, 3.0
Regel: behandel de prompt als programma en het model als interpreter; kies per onderdeel code, gewichten of prompt.
Bron: https://www.youtube.com/watch?v=LCEmiRjPEtQ&t=60 (ca. 01:02-05:05). Ook bevestigd in het Sequoia-transcript (96jN2OCOfLs, ca. 2:40-3:42).
Vraag: Welke regels staan in code (hard) en welke alleen in een prompt (zacht)?

## 22. Iron Man-pak, geen Iron Man-robot
Regel: bouw eerst versterking van de mens met een schuif naar autonomie; volledige agents zijn werk van een decennium.
Bron: https://www.youtube.com/watch?v=LCEmiRjPEtQ&t=1640 (ca. 27:29) en 38:41.
Vraag: Is dit product een pak om de recruiter, of een robot die de recruiter moet vertrouwen?

## Korte samenvattingen: neural-net lessen (alleen openingsregels en titels bekeken, niet diep gelezen)
- micrograd (VMj-3S1tku0): bouwt een autograd-engine; backpropagation en kleine neurale netwerken vanaf nul.
- makemore 1-5 (PaCmpygFfXo, TCH_1BHY58I, P6sfmUTpUmc, q8SA3rM6ckI NOT FETCHED, t3YJ5hKiMQ0): taalmodel op namen: bigram, MLP, activaties en BatchNorm, handmatige backprop, WaveNet.
- Let's build GPT (kCc8FmEb1nY): een kleine transformer op Shakespeare in code; probabilistisch systeem, meerdere antwoorden per prompt.
- GPT Tokenizer (zduSFxRajkE): byte-pair encoding vanaf nul; veel LLM-eigenaardigheden (spelling, tellen) komen van tokenisatie.
- Reproduce GPT-2 124M (l8pRSuU81PU): GPT-2 reproduceren en trainen, miniserie op verschillende groottes.

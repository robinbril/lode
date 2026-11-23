# Een model-grader krijgt pas gezag als hij op menselijke labels zijn echte-positieven- en echte-negatievenscore haalt

Probleem: een LLM-judge geeft "92 procent overeenkomst" met de mens, maar bij 5 procent fouten haalt een judge die altijd "pass" zegt ook 95 procent. De cijfers zeggen niets over wat hij mist.

Oplossing:
- Eén judge per faalwijze, met een binair oordeel plus een kritiek in woorden; geen 1-tot-5-score. Pass of fail dwingt scherper denken en geeft consistentere labels.
- Eén domeinexpert die het oordeel schrijft. Zijn kritiek is zo uitgebreid dat hij als few-shot-voorbeeld in de judge-prompt kan.
- Label 100 tot 200 voorbeelden per faalwijze. Splits: 10 tot 20 procent voorbeelden voor de prompt, 40 tot 45 procent dev om de prompt te verfijnen, 40 tot 45 procent test die je één keer aan het eind gebruikt.
- Streef naar 30 tot 50 goede en 30 tot 50 foute voorbeelden in zowel dev als test. Dat past pas vanaf ongeveer 150 labels; onder 60 voorbeelden zijn de betrouwbaarheidsintervallen vaak te breed.
- Meld de true positive rate en de true negative rate apart en volg beide. "Positief" betekent hier: er is een fout. TPR is het deel van de echte fouten dat de judge vangt, TNR het deel van de goede antwoorden dat hij terecht doorlaat.
- Laat de judge "Unknown" teruggeven als hij te weinig informatie heeft, in plaats van te gokken.
- Pas de prompt met de hand aan tot de dev-set convergeert; in het voorbeeld van de bron bleek dat in drie rondes boven 90 procent.
- Waar een code-check de fout objectief herkent, gebruik je die en geen judge.

Waarom het werkt: twee foutpercentages tonen welke kant het misgaat, en een testset die je niet bij het afstellen gebruikte vertelt of de judge ook op nieuwe gevallen klopt.

Niet doen als: een deterministische check de fout al vangt.

Toetsvraag: zijn TPR en TNR van elke judge op een onaangeraakte testset gerapporteerd voordat hij een release mag blokkeren?

Bronnen:
- https://hamel.dev/blog/posts/llm-judge/ (gelezen 2026-11-23) "True Positive Rate"
- https://hamel.dev/blog/posts/evals-faq/ (gelezen 2026-11-23) "Track both rates"
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents (gelezen 2026-11-23) "Unknown"

# Of extra referentiecontext helpt meet je met gepaarde runs per taak, niet met twee losse gemiddelden

Probleem: je geeft het model een repo of handboek als context, het antwoord lijkt beter, en je roept winst. Eén run per kant, een grader die de variant ziet en een verschil binnen de ruis leveren een verhaal op, geen meting.

Oplossing:
- Dezelfde 20 tot 50 taken in twee armen: zonder en met referentie. Alles anders gelijk: model, prompt, tools, temperatuur. Voeg een derde arm toe met alleen het relevante deel, want een volle dump kan slechter scoren dan een gerichte selectie.
- Elke taak K keer per arm, elke trial in een schone omgeving. Rapporteer naast het gemiddelde ook pass^k (alle K slagen), want gebruikers voelen de misser.
- Analyseer het verschil per taak (gepaard), met standaardfout; taken uit dezelfde bron of repo vormen een cluster en krijgen een geclusterde standaardfout. Bereken vooraf of N en K een verschil van de gewenste grootte kunnen laten zien.
- Het betrouwbaarheidsinterval van het gepaarde verschil bevat 0: noem het ruis, niet winst.
- Grader blind: code-check waar het kan; anders een model-grader die de armlabels niet ziet. Bij een paarsgewijze vergelijking draai je elk paar twee keer met omgewisselde positie en telt alleen een consistent oordeel.
- Orde-effecten: schud waar de referentie in de prompt staat en de volgorde van opties; bij meerkeuzevragen blijkt een model voorkeur te hebben voor bepaalde antwoordposities.
- Leg per arm vast: invoertokens (met gecachete apart), wachttijd, kosten per geslaagde taak. Winst die drie keer zoveel kost is een keuze, geen gratis resultaat.

```python
# eigen schets: verschil per taak, dan pas samenvatten
delta = {t: mean(score[t]["met"]) - mean(score[t]["zonder"]) for t in taken}
se = stdev(delta.values()) / len(delta) ** 0.5
ruis = abs(mean(delta.values())) < 2 * se
```

Waarom het werkt: gepaarde verschillen halen de moeilijkheid van de taak uit de ruis, en herhaling plus blinde grading haalt toeval en voorkeur van de beoordelaar eruit.

Niet doen als: je minder dan ongeveer twintig echte taken hebt; verzamel eerst die.

Toetsvraag: staat in het rapport per arm het aantal herhalingen, het gepaarde verschil met interval en de kosten per geslaagde taak?

Bronnen:
- UKGovernmentBEIS/inspect_ai@a88b0ec69541a257ffbe4b3845383138697a4d00 src/inspect_ai/_eval/task/epochs.py:12 "reducer"
- https://arxiv.org/pdf/2411.00640 (gelezen 2026-11-23) "paired differences"
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents (gelezen 2026-11-23) "all k trials succeed"
- https://www.trychroma.com/research/context-rot (gelezen 2026-11-23) "focused prompts"
- https://arxiv.org/abs/2309.03882 (gelezen 2026-11-23) "option position"

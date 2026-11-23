# Onbetrouwbare documenten leest een aparte aanroep zonder tools die alleen een getypt object teruggeeft

Probleem: een model dat een CV leest en ook tools heeft, kan door een verborgen zin in dat CV een tool aanroepen of de ranking van andere kandidaten beïnvloeden.

Oplossing:
- Per document één geïsoleerde aanroep. Die heeft geen tools, geen toegang tot andere documenten en geen geheugen van eerdere aanroepen.
- De uitvoer is een vast schema met smalle velden: getallen, enums, korte velden zoals "jaren ervaring". Valideer in code vóór iets anders het object ziet.
- De reduce-stap (ranken, kiezen, samenvatten) is bij voorkeur gewone code. Is het toch een model met tools, dan ziet het alleen de uitvoer die al aan strakke regels is gebonden, zoals een patroon dat afdwingt dat er een getal staat.
- Laat de extractor mogen zeggen dat de informatie ontbreekt. De CaMeL-referentie-implementatie voegt aan elk uitvoerschema een veld `have_enough_information` toe en gooit een fout als dat false is, zodat het model geen e-mail of datum verzint.
- Het model dat tools kiest en argumenten vult, ziet nooit de ruwe documenttekst, alleen de velden. Verwijder bovendien de oorspronkelijke opdracht of documenttekst uit de context voor de volgende stap.
- Restrisico blijft: een CV kan zichzelf mooier voorstellen. Bewaar daarom bij elke score welk veld of welke tekstspan erachter zit, zodat een mens kan nakijken.
- Bewaar hostile CV's (verborgen of gesplitste instructies) als testbestand en eis dat er geen toolaanroep volgt.

Waarom het werkt: een injectie kan alleen binnen de smalle velden van haar eigen document schade doen, en nooit de besturing of een ander document bereiken.

Niet doen als: de taak werkelijk vrije tekst als uitvoer nodig heeft; kies dan voor een mens in de lus (zie de Rule of Two).

Toetsvraag: kan het model dat kiest welke tool met welke argumenten draait ooit rauwe tekst uit een CV of webpagina zien?

Bronnen:
- https://arxiv.org/abs/2506.08837 (gelezen 2026-11-23) "provable resistance"
- https://arxiv.org/pdf/2506.08837 (gelezen 2026-11-23) "isolated LLM"
- google-research/camel-prompt-injection@f083b6b396399d3b3c7f2ddaf613a5945eaf32d8 src/camel/quarantined_llm.py:83 "have_enough_information"
- google-research/camel-prompt-injection@f083b6b396399d3b3c7f2ddaf613a5945eaf32d8 src/camel/quarantined_llm.py:37 "query_quarantined_llm"

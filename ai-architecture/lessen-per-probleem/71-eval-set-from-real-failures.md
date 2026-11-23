# De evalset bestaat uit gelezen echte missers, niet uit voorbeelden die je verzint

Probleem: een team schrijft vijftig nette testvragen, de score is hoog, en de fouten die gebruikers echt tegenkomen zitten er niet in.

Oplossing:
- Lees eerst echte traces. Begin met ongeveer 100 uiteenlopende traces en annoteer de eerste 30 zelf met vrije notities; groepeer die notities tot een lijst faaltypes met een telling per type.
- Per bevestigde misser komt er een gerichte test bij. Schrijf evaluators voor fouten die je vond, niet voor fouten die je bedenkt.
- Een taak is bruikbaar als twee domeinexperts onafhankelijk hetzelfde oordeel zouden geven en alles wat de grader controleert in de taaktekst staat.
- Klein starten is genoeg: 20 tot 50 taken uit echte missers, of zelfs 10 gouden voorbeelden.
- Synthetische gevallen mogen helpen bij het zoeken naar fouten, nooit bij het schatten van hoe vaak een fout voorkomt.
- Voeg elke nieuwe misser uit productie toe met trace-id erbij, zodat de set mee groeit met het product.
- Lees transcripten voor je een score vertrouwt.

Waarom het werkt: de set meet precies de plekken waar het systeem aantoonbaar faalt, en een regressie op een oude misser is meteen zichtbaar.

Niet doen als: je nog geen echte traces hebt; dan is een handvol zelfgeschreven taken een noodoplossing en moet je dat zo benoemen.

Toetsvraag: komt elke taak in de set uit een echte trace of bugmelding, en staat daar een verwijzing naar?

Bronnen:
- https://hamel.dev/blog/posts/evals-faq/ (gelezen 2026-11-23) "errors you discover"
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents (gelezen 2026-11-23) "drawn from real failures"
- https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop (gelezen 2026-11-23) "10 golden examples"

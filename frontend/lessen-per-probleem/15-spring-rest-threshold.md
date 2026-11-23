# Een spring-animatie stopt op een andere drempel voor kleine dan voor grote bewegingen

Probleem: dezelfde "stop zodra snelheid en afstand klein genoeg zijn"-drempel gebruiken voor een opacity-fade (0 tot 1) en een layout-shift van driehonderd pixels laat de ene animatie eindeloos microscopisch trillen, of de andere voortijdig stokken.

Oplossing:
- Bepaal eerst hoe groot de totale verandering is (`delta`, start- naar eindwaarde).
- Is `|delta|` kleiner dan 5 (bijvoorbeeld opacity): rust bij snelheid onder 0,01 en afstand onder 0,005.
- Is die verandering 5 of groter (pixels): rust bij snelheid onder 2 en afstand onder 0,5. Met de strakke drempels zou de spring subpixelbewegingen blijven uitvoeren die niemand ziet.
- Rust vraagt beide voorwaarden tegelijk: snelheid en afstand tot het doel binnen hun drempel.
- Een door de consument opgegeven `restSpeed` of `restDelta` wint; de schaalkeuze geldt alleen voor wat niet is opgegeven en wordt opnieuw bepaald als het doel (en dus `delta`) verandert.

Waarom het werkt: "rust" is relatief aan de schaal van de beweging: een afstand van 0,5 is onzichtbaar bij een sprong van 300 pixels, maar de helft van het hele bereik bij een opacity-fade.

Niet doen als: de animatie een vaste, niet-fysische duur gebruikt (`tween`/`duration`) in plaats van een spring; dan bestaat het rustbegrip niet.

Toetsvraag: stokt een opacity-spring niet te vroeg, en blijft een layout-spring niet naschommelen?

Bronnen:
- motiondivision/motion@699ff927ac7e packages/motion-dom/src/animation/generators/spring.ts:343 "isGranularScale"
- motiondivision/motion@699ff927ac7e packages/motion-dom/src/animation/generators/spring.ts:33 "restSpeedDefault"
- motiondivision/motion@699ff927ac7e packages/motion-dom/src/animation/generators/spring.ts:471 "setRestThresholds"

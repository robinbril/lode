# Compactie draait pas boven een vaste drempel, en eerst goedkoop prunen voor je duur samenvat

Probleem: een conversatie die bij elke beurt wordt samengevat kost een extra modelcall per beurt; een conversatie die nooit wordt samengevat loopt vast op de contextlimiet.

Oplossing:
- De drempel is de laagste van twee: venster maal `thresholdRatio` (standaard 0.8), en venster min gereserveerde output min `headroomTokens` (standaard 65.536). Bij een venster van 200.000 met 32.000 output is dat 102.464, dus op kleine vensters beslist de marge.
- Wat bewaard blijft is ook een fractie: `retainRatio = 0.16` van het venster minus gereserveerde output, tenzij een vast `retainTokens` is gezet.
- Volgorde: meten; boven de drempel een modelvrije `prune` van oude tool-resultaten; opnieuw meten; pas dan een samenvatting.
- Een samenvatting die (met omlijsting) niet kleiner is dan wat ze vervangt, wordt geweigerd.
- Nog boven de drempel na de poging: standaard één herhaling, daarna een fout in plaats van eindeloos proberen. Een echte overflow-melding van de provider is een tweede pad dat de drempel overslaat.

```ts
// eigen schets
const drempel = Math.min(venster * 0.8, venster - output - marge);
// meet -> prune (geen modelcall) -> meet opnieuw -> pas dan samenvatten
```

Waarom het werkt: prunen kost geen modelaanroep; de duurdere samenvatting draait alleen als dat niet genoeg was.

Niet doen als: je gesprekken zelden of nooit de drempel raken; dan is een simpele harde cap op aantal beurten goedkoper om te onderhouden.

Toetsvraag: kan een samenvatting ooit groter zijn dan de geschiedenis die ze vervangt en toch worden geaccepteerd?

Bronnen:
- deepseek-ai/deepseek-harness@4b399c39a6d1479cd84ca591b4d7c88e24d38a96 packages/compaction/compaction-basic/src/config.ts:20 "DEFAULT_THRESHOLD_RATIO"
- deepseek-ai/deepseek-harness@4b399c39a6d1479cd84ca591b4d7c88e24d38a96 packages/compaction/compaction-basic/src/config.ts:23 "DEFAULT_RETAIN_RATIO"
- deepseek-ai/deepseek-harness@4b399c39a6d1479cd84ca591b4d7c88e24d38a96 packages/compaction/compaction-basic/src/region.ts:426 "summary is not smaller"

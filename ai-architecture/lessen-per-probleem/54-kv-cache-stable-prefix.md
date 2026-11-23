# Een samenvattingscall begint met hetzelfde prefix als het laatste echte request, voor KV-cache-hergebruik

Probleem: een "even een losse samenvatting ophalen bij een ander system-prompt" call gooit de providers KV-cache weg; elke volgende aanroep in die beurt betaalt dan weer de volle prijs voor het opnieuw verwerken van system-prompt en tool-definities.

Oplossing:
- De samenvattingsinstructie wordt als laatste user-bericht NA de gerepliceerde conversatie gestuurd, niet als eigen apart system-prompt. Systeemprompt, tools en voorste berichten blijven gelijk; alleen de slotinstructie is nieuw.
- Dat werkt alleen op hetzelfde model. Wie voor samenvatten een ander (goedkoper) model instelt, heeft geen warme cache; reken dat mee.
- Tools die later bijkomen: gedeclareerd met `deferLoading` en geactiveerd door een `tool-addition`-blok in een later bericht, zodat de declaratielijst niet wordt herschreven. Alleen voor modellen die dit aankunnen; anders gaat elke keer de volledige lijst mee.
- System-prompt-secties hebben een vast volgordenummer en bij gelijke stand sortering op naam; tools staan standaard alfabetisch. Wat per sessie verschilt (werkmap, sandbox- en goedkeuringsbeleid) staat als losse context buiten die secties.

```ts
// niet: apart systeemprompt-call voor de samenvatting
// wel: samenvattingsinstructie als laatste bericht NA de bestaande geschiedenis
// tool erbij? markeer 'm deferLoading en voeg toe als tool-addition-blok
```

Waarom het werkt: providers cachen op exacte prefix-overeenkomst; elke afwijking vroeg in de token-reeks (system-prompt-volgorde, tool-lijst) ongeldigt alles daarna, dus de winst zit in nooit afwijken, niet in slimmer cachen.

Niet doen als: je provider geen prompt-caching aanbiedt; dan is de complexiteit van addition-only tool-updates niet de moeite waard.

Toetsvraag: verandert de volgorde of inhoud van de tool-declaraties tussen twee opeenvolgende requests in dezelfde beurt?

Bronnen:
- deepseek-ai/deepseek-harness@4b399c39a6d1479cd84ca591b4d7c88e24d38a96 packages/compaction/compaction-basic/src/summarizer.ts:33 "KV cache is reused"
- deepseek-ai/deepseek-harness@4b399c39a6d1479cd84ca591b4d7c88e24d38a96 packages/llm/llm/src/types.ts:523 "deferLoading"
- deepseek-ai/deepseek-harness@4b399c39a6d1479cd84ca591b4d7c88e24d38a96 packages/llm/llm/src/types.ts:444 "addition-only"
- deepseek-ai/deepseek-harness@4b399c39a6d1479cd84ca591b4d7c88e24d38a96 packages/core/system-prompt/src/index.ts:191 "SECTION_ORDERS"

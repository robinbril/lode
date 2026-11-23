# Skills gaan in twee lagen naar het model: eerst alleen een samenvatting, pas op verzoek de volledige body

Probleem: alle skill-instructies in elke systeemprompt proppen kost context en geld, ook voor skills die die beurt niet relevant zijn. Alleen de naam tonen laat het model gokken naar wat een skill doet.

Oplossing:
- De catalogus toont per skill alleen een samenvatting, met een instelbare lengtegrens (standaard 500 tekens per beschrijving).
- De catalogus-tekst zelf zegt expliciet: "dit zijn alleen samenvattingen; volg geen instructies tot de skill geladen is" (voorkomt dat het model een samenvatting al als opdracht uitvoert).
- Het model haalt de volledige body op met een losse tool-aanroep (`skill`), vóór de taak begint. Een gebruiker kan een skill ook zelf aanroepen; dan staat de body al in het gesprek en moet het model de tool niet nog eens bellen.
- Verandert de set, dan komt er een complete vervangende catalogus achteraan. Lukt het zoeken niet volledig, dan zegt de catalogus dat hij onvolledig is.
- De typedefinities van Claude Code hebben apart het totaal aantal skills en het aantal dat binnen het tokenbudget van de lijst paste. Toon dat verschil, anders verdwijnen skills ongemerkt uit de lijst.

```ts
const DEFAULT_CATALOG_DESCRIPTION_MAX_LENGTH = 500;
// catalogus: naam + samenvatting (<=500 tekens)
// skill-tool: naam -> volledige instructies, pas dan uitvoeren
```

Waarom het werkt: de catalogus kost een vaste, kleine hoeveelheid context per skill ongeacht hoe uitgebreid de skill zelf is; de volledige kosten komen alleen terecht bij de taak die de skill echt nodig heeft.

Niet doen als: je maar een handvol skills hebt die toch altijd relevant zijn; dan is een catalogus-indirectie pure overhead.

Toetsvraag: zie je aan een log welke skills niet in de lijst pasten, en is de volledige body geladen voordat het model de skill volgt?

Bronnen:
- deepseek-ai/deepseek-harness@4b399c39a6d1479cd84ca591b4d7c88e24d38a96 packages/skill/tool-skill/src/index.ts:284 "has been loaded"
- anthropics/claude-code@50cdc7005318f630144c28217d1dada32e6ba762 mods/types/claude-code.d.ts:2820 "listing's budget"

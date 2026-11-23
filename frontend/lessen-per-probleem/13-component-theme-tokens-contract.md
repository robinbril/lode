# Een deelbaar component draagt zijn eigen tokens mee, gesplitst naar licht en donker

Probleem: een component die je kopieert van een andere codebase naar een project met een ander kleurenschema breekt zodra de tokennamen niet overeenkomen, of ziet er in dark mode verkeerd uit omdat niemand wist welke variabelen daarbij horen.

Oplossing:
- Laat een component zijn eigen CSS-variabelen meegeven in drie optionele groepen: `theme`, `light`, `dark` (shadcn: `cssVars`, drie records van naam naar waarde).
- De installer schrijft `light` naar `:root`, `dark` naar `.dark` en `theme` naar een Tailwind v4 `@theme`-blok. Zonder Tailwind is de vertaling `:root` voor `theme` en `light`, `.dark` voor `dark`.
- Een bestaande variabele in het doelproject wordt niet overschreven wanneer een gewoon component hem meebrengt; alleen een thema- of stijl-item (`overwriteCssVars`) mag dat.
- Documenteer de variabelen als platte key-value-paren (CSS custom properties), niet als een eigen theming-API; dat maakt het samenvoegen triviaal.
- Een component hoeft niet alle drie de groepen te vullen: een lege `dark` laat de `theme`- en `light`-waarden in beide standen gelden.
- Geef de variabele ook een harde fallback in de `var()`-aanroep (bijvoorbeeld `var(--st-fg, #1a1a1a)`); dan ziet het component er ook zonder geladen tokenlaag redelijk uit en documenteert de fallback de standaardwaarde.

Waarom het werkt: licht en donker zijn expliciet gescheiden op het moment dat het component wordt gedeeld, in plaats van achteraf uitgezocht door de ontvangende codebase.

Niet doen als: het component geen zichtbare kleuren gebruikt (bijvoorbeeld een puur layout-primitive zonder achtergrond of tekstkleur).

Toetsvraag: kan dit component in een project met een ander kleurenschema worden gezet zonder dat iemand een dark-mode-bug moet opsporen?

Bronnen:
- shadcn-ui/ui@055aa6b7837b packages/registry/src/registry/schema.ts:147 "registryItemCssVarsSchema"
- shadcn-ui/ui@055aa6b7837b packages/registry/src/updaters/update-css-vars.ts:320 "overwriteCssVars"
- kvnkld/aicss@7f9dc408ec11 packages/react/src/streaming-text/StreamingText.module.css:20 "var(--st-fg, #1a1a1a)"

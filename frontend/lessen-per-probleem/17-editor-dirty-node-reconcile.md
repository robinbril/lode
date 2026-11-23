# Een rich-text editor update alleen de knopen die echt veranderd zijn, niet de hele boom

Probleem: een programmatische wijziging (bijvoorbeeld een AI die één paragraaf herschrijft) die de hele editor-state door een nieuwe boom vervangt, kost de gebruiker zijn cursorpositie en selectie elders in het document, zodra een naïeve weergave daarbij alle DOM-nodes opnieuw opbouwt.

Oplossing:
- Geef elke node een key en houd per update twee verzamelingen bij: `dirtyElements` (key naar boolean: `true` als de element-node zelf bewust is gewijzigd, `false` als alleen een afstammeling wijzigde) en `dirtyLeaves` (tekst- en andere leaf-keys).
- Bij het reconciliëren naar de DOM geldt een node als vuil als `treatAllNodesAsDirty` aan staat of zijn key in een van beide verzamelingen zit.
- Is de node in de vorige en de nieuwe state dezelfde instantie en niet vuil, dan krijgt hij zijn bestaande DOM-element terug en wordt hij niet aangeraakt. Wijzigen betekent dus een nieuwe instantie maken (Lexical: `getWritable()`), niet muteren.
- Een volledige reconciliatie (`FULL_RECONCILE`) hoort bij het wholesale vervangen van de state, zoals `setEditorState`, dat ook undo en redo draagt. Een normale update neemt dat pad niet.

Waarom het werkt: de browser behoudt focus en selectie op een DOM-node zolang die node niet wordt vervangen; alleen de knopen die echt wijzigen worden aangeraakt.

Niet doen als: het "document" een losse read-only weergave is zonder cursor of selectie om te bewaren.

Toetsvraag: blijft het DOM-element van een niet-gewijzigde paragraaf hetzelfde object nadat elders in het document tekst is aangepast?

Bronnen:
- facebook/lexical@60926d060fc0 packages/lexical/src/LexicalReconciler.ts:2241 "treatAllNodesAsDirty"
- facebook/lexical@60926d060fc0 packages/lexical/src/LexicalReconciler.ts:2228 "dirtyElements"
- facebook/lexical@60926d060fc0 packages/lexical/src/LexicalReconciler.ts:1808 "activeDirtyLeaves.has(key)"

# Een toolbar of lijst heeft maar één Tab-stop, de pijltjestoetsen doen de rest

Probleem: elk item in een werkbalk of menu een eigen `tabIndex={0}` geven dwingt een gebruiker die met Tab navigeert om door elk los item te tabben voor hij bij de volgende widget komt.

Oplossing:
- Precies één item in de groep krijgt `tabIndex={0}`, de rest krijgt `tabIndex={-1}`.
- Welk item dat is, staat in gedeelde state (`currentTabStopId`) die verandert bij focus of mousedown op een item (mousedown ook, want Safari focust een geklikte knop niet).
- Pijltjes binnen de groep verplaatsen de focus programmatisch naar het volgende item, en de focus-handler verplaatst daarmee ook de tab-stop. Radix filtert op oriëntatie, kent Home/End/PageUp/PageDown, een `loop`-optie, RTL, en negeert toetsen met een modifier. Items met `focusable=false` worden overgeslagen.
- Radix geeft ook de groep zelf `tabIndex={0}`; focust die via Tab, dan stuurt hij de focus door naar het actieve, het huidige of het eerste item. Bij Shift+Tab op een item zet de groep zich tijdelijk op `-1` (`isTabbingBackOut`), anders landt de focus op de groep en springt terug naar het item.
- Bind de state met een controllable-state hook zodat een ouder hem ook van buiten kan sturen, bijvoorbeeld om bij openen een specifiek item de tab-stop te geven.

Waarom het werkt: Tab springt de hele groep in en uit in één stap omdat er maar één item in de tab-volgorde zit; binnen de groep is navigatie een losse interactie met de pijltjestoetsen.

Niet doen als: de groep maar twee of drie items heeft die toch allemaal relevant zijn om los te kunnen Tabben; dan voegt roving focus alleen complexiteit toe.

Toetsvraag: komt Shift+Tab vanaf een item in de vorige widget terecht zonder dat de focus terugspringt naar de groep?

Bronnen:
- radix-ui/primitives@eb3a2b709129 packages/react/roving-focus/src/roving-focus-group.tsx:295 "isCurrentTabStop"
- radix-ui/primitives@eb3a2b709129 packages/react/roving-focus/src/roving-focus-group.tsx:131 "useControllableState"
- radix-ui/primitives@eb3a2b709129 packages/react/roving-focus/src/roving-focus-group.tsx:173 "isTabbingBackOut"

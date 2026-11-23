# Een toast-timer onthoudt de resterende tijd, hij herstart niet

Probleem: een toast pauzeren bij hover en de timer gewoon opnieuw starten bij het verlaten van de hover geeft hem telkens zijn volle duur terug, waardoor een toast die je meerdere keren kort aanraakt ruim langer blijft hangen dan zijn duur.

Oplossing:
- Houd een `remainingTime`-waarde apart van de timer zelf.
- Bij pauzeren: annuleer de timer en trek de verstreken tijd sinds de laatste start af van `remainingTime`. Sonner doet dat alleen als er sinds de vorige pauze een start was, zodat een dubbele pauze niet twee keer aftrekt.
- Bij hervatten: start `setTimeout` met exact die `remainingTime`, niet met de oorspronkelijke duur.
- Start geen timer bij een oneindige duur: `setTimeout(fn, Infinity)` gedraagt zich als delay 0 en sluit de toast direct.
- Pauzeer niet alleen op hover en focus van de lijst, maar ook als het tabblad verborgen is (`document.hidden`, bijgehouden via `visibilitychange`); anders telt een toast door terwijl de gebruiker in een ander tabblad zit.

```ts
// eigen vereenvoudiging, niet overgetypt
let remaining = duration, startedAt = 0, timer
function resume() { startedAt = Date.now(); timer = setTimeout(dismiss, remaining) }
function pause() {
  if (!startedAt) return
  clearTimeout(timer)
  remaining -= Date.now() - startedAt
  startedAt = 0
}
```

Waarom het werkt: de klok telt alleen tijd mee waarin de toast ook echt onbewaakt stond; elke pauze bevriest exact het restant in plaats van het weg te gooien.

Niet doen als: de toast geen auto-dismiss heeft, of hover-gedrag voor deze toastsoort bewust niet bestaat.

Toetsvraag: krijgt een toast die drie keer kort gehoverd wordt zijn volle duur terug bij elke hover-exit?

Bronnen:
- emilkowalski/sonner@8e4662b39255 src/index.tsx:213 "remainingTime.current"
- emilkowalski/sonner@8e4662b39255 src/index.tsx:234 "isDocumentHidden"
- emilkowalski/sonner@8e4662b39255 src/index.tsx:223 "Infinity"

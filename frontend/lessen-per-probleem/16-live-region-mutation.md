# Een live region meldt alleen iets als er een nieuwe DOM-node bijkomt, niet als tekst verandert

Probleem: de tekst van een al bestaande `aria-live`-node overschrijven met dezelfde of een vergelijkbare melding blijft bij schermlezers makkelijk stil, omdat er geen node bijkwam.

Oplossing:
- Maak één onzichtbare container met twee logs, `assertive` en `polite`, elk `role="log"` met `aria-relevant="additions"`. React Aria maakt hem lazy bij de eerste `announce()` en laat hem staan tot `destroyAnnouncer`.
- Zet de container vóór de eerste melding in de DOM. Een net toegevoegde regio die direct wordt gevuld blijft in Safari stil; React Aria wacht daarom 100 ms na het aanmaken voor de eerste melding. Maak de regio dus liever bij het opstarten.
- Voeg bij elke aankondiging een nieuw kind-element met de tekst toe aan de juiste log, in plaats van de tekst van een bestaand element te wijzigen.
- Verwijder dat kind na een timeout (React Aria: 7000 ms, overschrijfbaar per melding), zodat de log niet groeit maar de melding lang genoeg staat voor trage schermlezers.
- De standaard van React Aria is `assertive`; kies zelf `polite` tenzij de melding echt niet kan wachten.

Waarom het werkt: met `aria-relevant="additions"` telt alleen een toegevoegde node als nieuwe inhoud; een tekstupdate op een bestaand element telt dan niet mee.

Niet doen als: de melding al via een focusverandering of een native dialoog wordt aangekondigd; een extra live region zou dan dubbel voorlezen.

Toetsvraag: wordt een tweede, vergelijkbare melding kort na de eerste ook echt voorgelezen?

Bronnen:
- adobe/react-spectrum@6be3466d87cc packages/react-aria/src/live-announcer/LiveAnnouncer.tsx:153 "appendChild"
- adobe/react-spectrum@6be3466d87cc packages/react-aria/src/live-announcer/LiveAnnouncer.tsx:16 "LIVEREGION_TIMEOUT_DELAY"
- adobe/react-spectrum@6be3466d87cc packages/react-aria/src/live-announcer/LiveAnnouncer.tsx:125 "aria-relevant"
- adobe/react-spectrum@6be3466d87cc packages/react-aria/src/live-announcer/LiveAnnouncer.tsx:46 "setTimeout"

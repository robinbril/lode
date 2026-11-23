# Een veld met asynchrone validatie heeft drie waarheidswaarden, niet twee

Probleem: een formulierveld dat tijdens een async validatiecall (bijvoorbeeld een server-check) alvast op "geldig" zet, laat een gebruiker submitten voor het echte antwoord terug is; zet het op "ongeldig", dan flikkert elk veld rood terwijl je nog typt.

Oplossing:
- Geef `valid` een derde stand: `null` zolang de validator nog loopt, naast `true` en `false`.
- Wat al zeker blokkeert, wordt direct gepubliceerd: een native fout (`valid === false`) meteen. Een eerdere custom-fout blijft staan in plaats van naar `null` te gaan, behalve in de modus `onSubmit` (daar gaat het veld wel naar `null`).
- Nummer elke poging met een teller die ook bij elke wijziging van de waarde ophoogt; komt een antwoord terug en is het nummer niet meer het laatste, negeer het en publiceer niets. Zo kan een trage call geen nieuwere uitkomst overschrijven.
- Een validator die faalt (een afgewezen promise) publiceert niets en laat de laatst gepubliceerde staat staan. Met een eerdere custom-fout (buiten `onSubmit`) kan een tijdelijke storing die fout dus niet laten verdwijnen.
- Het resultaat zelf is een string, een lijst strings, `null` of niets; een lege uitkomst telt als geldig.

Waarom het werkt: de UI onderscheidt "nog niet bekend" van "bekend geldig", en het volgnummer voorkomt dat een oude, langzame server-respons een nieuwere invoer overschrijft.

Niet doen als: de validatie synchroon en lokaal is (bijvoorbeeld een regex); dan bestaat de race niet.

Toetsvraag: kan een trage validatiecall die als laatste binnenkomt een nieuwere, al afgeronde validatie overschrijven?

Bronnen:
- mui/base-ui@52fac378e79c packages/react/src/field/root/useFieldValidation.ts:315 "nextState.valid"
- mui/base-ui@52fac378e79c packages/react/src/field/root/useFieldValidation.ts:323 "validationCommitId"
- mui/base-ui@52fac378e79c packages/react/src/field/root/useFieldValidation.ts:351 "validationCommitIdRef.current += 1"

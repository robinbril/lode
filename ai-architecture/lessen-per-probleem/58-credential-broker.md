# De agent voert aan met een credential, maar leest de waarde nooit terug

Probleem: als de agent zelf een API-key of token in handen krijgt om "in te vullen", staat die waarde in de modelcontext en dus in logs, traces en mogelijk de uiteindelijke respons.

Oplossing:
- Credentials liggen versleuteld in de database (AES-GCM, met een eigen envelope van IV en ciphertext per waarde); alleen de server ontsleutelt, nooit de agent-laag.
- De server zet de ontsleutelde waarde zelf in een HTTP-header vlak voor het uitgaande verzoek (`agentAuthHeaders`); er bestaat geen endpoint en geen veld dat de ruwe waarde teruggeeft aan een persoon of het model.
- Hooguit één actieve sleutel per `(kind, provider, keyId)` via een unieke index die alleen niet-herroepen rijen telt; twee replica's die tegelijk roteren kunnen dus niet allebei een levende rij invoegen. Doe roteren en het bijwerken van de agent in dezelfde transactie.
- Een herroepen of ontbrekende sleutel stuurt geen header. De aanroep faalt dan met de 401 van de andere kant; er is geen terugval zonder auth.
- In de bron gaat dit om de sleutel naar een externe agent; het id en de headernaam staan in de configuratie, de waarde alleen in de kluis. Deze tabel heeft geen eigenaarkolom: wie welke sleutel mag gebruiken regel je apart (zie de kaart over tenant- en eigenaarscontrole).

```ts
// eigen schets, draait op de server vlak voor het verzoek
const geheim = await kluis.lees(ref.credentialId);
if (!geheim || geheim.herroepenOp) return undefined; // geen header, geen terugval
return { [ref.header]: await ontsleutel(geheim.waarde) };
```

Waarom het werkt: een geheim dat nooit in de modelcontext komt, kan het model niet herhalen of lekken; de grens ligt op het netwerk-aanroeppunt, niet op "vertrouw het model om het niet te herhalen".

Niet doen als: de credential zelf bedoeld is om aan de gebruiker getoond te worden (bijv. een eenmalige uitnodigingscode); dan is een broker die alles verbergt het verkeerde patroon.

Toetsvraag: bestaat er een pad waarop de ontsleutelde waarde ergens in een API-respons, log of modelbericht terechtkomt?

Bronnen:
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab server/src/agents/auth-header.ts:22 "never read back"
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab server/src/db/schema/core.ts:442 "credentials_active_key_idx"

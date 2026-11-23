# Bij drie goedkeuringslagen (team, persoon, gesprek) wint de strengste regel, nooit de recentste

Probleem: als de laatst ingestelde regel wint, kan een persoonlijke "altijd toestaan"-instelling een teambrede weigering omzeilen, en kan "ik sta dit nu één keer toe" (voor dit gesprek) per ongeluk een permanente regel overschrijven.

Oplossing:
- Drie gelaagde regelbronnen: `team_rule` (vergrendeld door het team/de organisatie), `personal_rule` (door de gebruiker zelf bewaard), `conversation` (alleen voor dit ene gesprek).
- Bij een botsing wint de strengste match, over alle lagen heen. Pas bij gelijke strengheid telt de laag: eerst teamregel, dan persoonlijke regel, dan gespreksantwoord. Een persoonlijke "ask" wint dus ook van een team-"allow".
- Asymmetrie: "ask" en "hand_off" gelden voor elke soort actie. Een "allow" reikt alleen tot zijn eigen soort; toestemming voor een gewone klik geldt niet voor versturen, verwijderen of betalen. Een persoonlijke "allow" zonder account geldt niet voor een aanroep die wel een account noemt.
- "Sta voortaan altijd toe" (`allow_always`) maakt een losse regelrij met bot, tool, effect, scope en account, geen vlag op de aanvraag. Is die rij ingetrokken, dan lukt het verbruiken van de goedkeuring niet meer.
- Een gespreksgrant kan worden ingetrokken (`revokedAt`); een ingetrokken grant telt bij het verbruiken als afwezig, niet als "nog steeds goedgekeurd van eerder".

```ts
// eigen schets; lagen in volgorde team, persoon, gesprek
const STRENG = { allow: 0, pre_approved: 1, ask: 2, hand_off: 3 };
for (const r of regelsDieMatchen)
  if (!beste || STRENG[r.gedrag] > STRENG[beste.gedrag]) beste = r; // gelijk: eerste laag blijft
```

Waarom het werkt: een persoon kan een strengere teamregel niet versoepelen, terwijl een losse standing-grant-rij (in plaats van een vlag) betekent dat intrekken altijd mogelijk blijft zonder de oorspronkelijke aanvraag aan te raken.

Niet doen als: er maar één besluitnemer is (geen teams); dan is één platte regelset genoeg en is de laag-rangorde overbodige complexiteit.

Toetsvraag: kan een persoonlijke "altijd toestaan"-regel een vergrendelde teamregel die "ask" zegt overrulen?

Bronnen:
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab server/src/approvals/policy.ts:140 "team's locked row"
- robinbril/OpenBot@f8af37ab73e96784f174a11104505a965e722cab server/src/approvals/store.ts:278 "allow_always"

# Elk opgeslagen ding draagt een audience, en een beurt leest alleen team of zijn eigen audience en schrijft alleen in zijn eigen laag

Probleem: een bot die voor een team werkt, leert in een privégesprek iets over één persoon en gebruikt dat later in een groepsgesprek, of logt in met het account van de een in de beurt van de ander.

Oplossing:
- Een audience is `team`, `room:<id>` of `member:<persoon>`. `parseAudience` eist bij het inlezen dat ids passen op `[\w-]{1,200}`; `roomAudience` en `memberAudience` controleren zelf niets.
- Leesregel: `input === 'team' || input === turn`. Dat is gelijkheid, geen "bevat"-relatie: een kamer leest niet uit een persoonlijke laag en een persoon niet uit een kamer.
- Schrijfregel: `writesInto` geeft de eigen audience van de beurt terug, dus niet een bredere of andere.
- Geheugen staat per laag in een zusterfolder van de bot (`<bot>--room-<id>`, `<bot>--member-<persoon>`), niet binnen de botfolder die elke beurt van die bot kan lezen.
- Een persoonlijke laag is van die persoon alleen: ook een Admin ziet haar niet. Een Admin ziet wel elke kamer.
- Een beurt die niet van het team is, krijgt de botfolder read-only gemount (`teamReadOnly`). Uitzondering: is de botfolder zelf de werkmap (een kamer), dan zijn alleen `MEMORY.md`, `memory/` en `skills/` read-only en kan de beurt er verder bestanden maken. Een gedeeld proces voor alle gesprekken van een bot krijgt gesprekken van zijn eigen audience read-write en die uit `mayRead` read-only.
- Ook de browser volgt de audience: een eigen profiel per kamer of lid, met een gehasht achtervoegsel van 16 hexcijfers, zodat een inlog van de een niet in de beurt van de ander opent.
- Buiten een team is elke audience `team` en verandert er niets.

```ts
type Audience = 'team' | `room:${string}` | `member:${string}`;
const mayRead = (input: Audience, turn: Audience) => input === 'team' || input === turn;
const layerId = (bot: string, a: Audience) =>
  a === 'team' ? bot : `${bot}--${a.replace(':', '-')}`; // sibling folder
const mountsFor = (turn: Audience, botDir: string, layers: Map<Audience, string>) => [
  { path: botDir, rw: turn === 'team' },
  ...[...layers].filter(([a]) => a === turn).map(([, path]) => ({ path, rw: true })),
];
```

Waarom het werkt: de regel is één kleine pure functie en de handhaving zit in de mount, dus een fout in de prompt opent geen bestand.

Niet doen als: de box uit staat (geen Linux of geen bubblewrap): dan blijft alleen de leesregel in code en prompt over, de mounts bestaan niet.

Toetsvraag: kan een beurt in een kamer het geheugen of de skills van het team wijzigen?

Bronnen:
- milind-soni/OpenMausBot@77f41d3522217a484b4abdffa9d5f6ba651f84bd server/audience.ts:35 "mayRead"
- milind-soni/OpenMausBot@77f41d3522217a484b4abdffa9d5f6ba651f84bd server/audience.ts:63 "layerId"
- milind-soni/OpenMausBot@77f41d3522217a484b4abdffa9d5f6ba651f84bd server/host/team-box-scope.ts:30 "teamReadOnly"
- milind-soni/OpenMausBot@77f41d3522217a484b4abdffa9d5f6ba651f84bd server/bot-box/plan.ts:121 "TEAM_FOLDER_KEPT"
- milind-soni/OpenMausBot@77f41d3522217a484b4abdffa9d5f6ba651f84bd server/browser/audience.ts:16 "audienceBrowserSuffix"

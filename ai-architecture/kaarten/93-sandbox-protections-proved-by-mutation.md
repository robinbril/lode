# Elke bescherming van een bot-sandbox heeft een naam waarmee een test haar uitzet en dan precies de bijbehorende check ziet falen

Probleem: een sandbox die "veilig" heet omdat de mountlijst er goed uitziet, kan een bescherming stilletjes kwijtraken zonder dat een test rood wordt, want elke test controleert alleen wat er wel is.

Oplossing:
- Een boxed proces krijgt een plan: systeemmappen read-only, HOME read-write, de datamap vervangen door een lege privémap, daarin alleen de werkmap van deze beurt en de botfolder terug. Verder een eigen PID-namespace, eigen `/tmp` en standaard een netwerk met alleen loopback (een browser krijgt het netwerk van de host). Twee loopbackpoorten gaan via unix-sockets naar de egress- en harness-poort van de server.
- `BOX_MUTATIONS` noemt acht schakelaars (`bind-data`, `bind-otherws`, `share-pid`, `share-net`, `env-all`, `tmp-shared`, `no-seccomp`, `engines-rw`). Elke haalt volgens het commentaar één bescherming weg. De code zegt dat productie er geen meegeeft.
- Laag 1, zuivere planfunctie, draait overal: per mutatie is de probe onwaar zonder en waar met de mutatie, en vier combinaties tonen dat een mutatie het gat van een andere niet opent. `env-all` staat niet in het plan en wordt daar overgeslagen.
- Laag 2, in een echte bubblewrap: voor zes mutaties (zeven op x64, met `no-seccomp`) staat een lijst checks die moeten falen, en elke andere gefaalde check laat de test falen. `bind-otherws` heeft in laag 2 geen lijst, die is alleen in laag 1 gedekt.
- Laag 2 is `describe.skipIf` zonder werkende bubblewrap. Op zo'n machine zegt een groene run niets over de echte box.
- De box staat standaard aan op een Cloud-home en uit elders, tenzij `OMB_BOT_BOX=1`. Zonder werkende bubblewrap meldt hij `off` met een vaste reden en blijft de spawn ongewijzigd: de beurt draait dan zonder box.

```ts
type Hole = 'bind-data' | 'share-net';
const plan = (holes = new Set<Hole>()) => ({
  mounts: holes.has('bind-data') ? ['/data'] : [],
  net: holes.has('share-net') ? 'host' : 'loopback',
});
const probe: Record<Hole, (p: ReturnType<typeof plan>) => boolean> = {
  'bind-data': (p) => p.mounts.includes('/data'),
  'share-net': (p) => p.net === 'host',
};
for (const hole of Object.keys(probe) as Hole[]) { // throw: console.assert never fails a run
  if (probe[hole](plan())) throw new Error(`${hole} open by default`);
  if (!probe[hole](plan(new Set([hole])))) throw new Error(`${hole} probe is blind`);
}
```

Waarom het werkt: een probe die ook met de bescherming uit onwaar blijft, is blind, en dat zie je nu direct in plaats van na een incident.

Niet doen als: je alleen een mountlijst hebt zonder werkende box om haar in te bewijzen; dan test je een tekening.

Toetsvraag: wordt er voor elke bescherming een test uitgevoerd die faalt zodra je haar uitschakelt?

Bronnen:
- milind-soni/OpenMausBot@77f41d3522217a484b4abdffa9d5f6ba651f84bd server/bot-box/plan.ts:56 "BOX_MUTATIONS"
- milind-soni/OpenMausBot@77f41d3522217a484b4abdffa9d5f6ba651f84bd server/bot-box/plan.test.ts:268 "opens exactly the hole"
- milind-soni/OpenMausBot@77f41d3522217a484b4abdffa9d5f6ba651f84bd server/bot-box/self-check.linux.test.ts:34 "each mutation fails the checks"

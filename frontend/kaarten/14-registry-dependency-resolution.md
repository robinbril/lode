# Een registry-item noemt zijn eigen afhankelijkheden bij naam, de installer zoekt ze zelf op

Probleem: een component die op drie andere componenten steunt (bijvoorbeeld een dialoog die een knop en een icoon nodig heeft) installeren zonder die drie mee te geven laat de ontvanger met kapotte imports zitten.

Oplossing:
- Elk item krijgt een lijst `registryDependencies`: strings die andere items aanwijzen (een naam, of `@registry/naam` voor een andere registry), geen bestandspaden.
- Het type van elk bestand in het item (`registry:ui`, `registry:block`, `registry:file`, ...) bepaalt of een vast doelpad (`target`) móet: alleen `registry:file` en `registry:page` eisen een expliciet `target`, bij elk ander type is het optioneel en kiest de installer de plek.
- De installer lost de lijst recursief op (`resolveDependenciesRecursively`) en verzamelt de items voor hij ze wegschrijft, zodat een project nooit een component krijgt zonder zijn bouwstenen. Een `@registry`-verwijzing zonder geconfigureerde registry geeft een fout.
- Geef elk item ook `dependencies` en `devDependencies` (npm-packages) apart van `registryDependencies` (andere items); het zijn verschillende soorten "nodig hebben".

Waarom het werkt: de naam-verwijzing is stabiel zelfs als het doelproject zijn mappenstructuur anders inricht; alleen het bestandstype bepaalt of een vast pad verplicht is.

Niet doen als: je maar één soort bestand deelt zonder onderlinge afhankelijkheden, zoals een losse CSS-snippet.

Toetsvraag: breekt het installeren van dit component als de ontvanger niet weet welke andere componenten het nodig heeft?

Bronnen:
- shadcn-ui/ui@055aa6b7837b packages/registry/src/registry/schema.ts:186 "registryDependencies"
- shadcn-ui/ui@055aa6b7837b packages/registry/src/registry/schema.ts:125 "target: z.string()"
- shadcn-ui/ui@055aa6b7837b packages/registry/src/registry/resolver.ts:198 "resolveDependenciesRecursively"

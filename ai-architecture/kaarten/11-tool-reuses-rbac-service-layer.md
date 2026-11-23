# Een AI-tool checkt dezelfde rechten als de normale API, nooit een eigen kopie

Probleem: een tool die zijn eigen permissiecheck herschrijft loopt uit de pas met de echte RBAC-regels en kan onbedoeld meer toestaan dan de UI ooit zou doen.

Oplossing:
- PostHog's toolbasisklasse heeft `get_required_resource_access()` die (resource, niveau)-paren declareert; dat wordt vóór de uitvoering gecheckt via de gedeelde `UserAccessControl`-klasse. De default is een lege lijst en dus geen check; rechten op één object vragen een aparte `check_object_access`-aanroep in de tool.
- Twenty's database-tool checkt per CRUD-operatie (create/read/update/softDelete/destroy) via `canAccessSomeRecords` of de tool getoond mag worden. Onleesbare velden vallen uit het leesschema, niet-bewerkbare uit het schrijfschema. Dit regelt zichtbaarheid; de uitvoering moet de rechten op het concrete record zelf nog afdwingen.
- Lightdash gebruikt in de AI-tools dezelfde `createAuditedAbility()` uit de `BaseService` als zijn andere services: de CASL-regels blijven één set en de wrapper logt de check. De AI-map staat onder een source-available licentie: alleen het idee overnemen, geen code.

Waarom het werkt: een wijziging in de rechtenlaag geldt meteen ook voor de tool, omdat er geen tweede kopie van de regel is.

Niet doen als: de data openbaar is voor iedereen die de agent mag openen. Filteren op tenant alleen is geen reden, want rechten verschillen per gebruiker binnen een tenant.

Toetsvraag: weigert de tool voor een gebruiker zonder rechten op dit ene record, ook als niemand een resource-eis heeft ingevuld?

Bronnen:
- PostHog/posthog@9277b47 ee/hogai/tool.py:333 "check_access_level_for_resource"
- twentyhq/twenty@2fd4d03 packages/twenty-server/src/engine/core-modules/tool-provider/providers/database-tool.provider.ts:160 "canAccessSomeRecords"
- lightdash/lightdash@73ca0af packages/backend/src/ee/services/AiAgentToolsService/AiAgentToolsService.ts:2637 "ability.can"
- lightdash/lightdash@73ca0af packages/backend/src/services/BaseService.ts:62 "createAuditedAbility"

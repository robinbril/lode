# Een API-key kan nooit een breder scope krijgen dan de rol van de uitgever

Probleem: een scope-systeem dat scopes los van rollen laat kiezen, maakt het mogelijk dat een gebruiker met een beperkte rol (bijvoorbeeld alleen-lezen) toch een key met schrijfscope aanmaakt, en daarmee zijn eigen rolbeperking omzeilt via de API.

Oplossing:
- Elke scope is genaamd als `resource.actie` (bijvoorbeeld `links.write`), en is in een vaste tabel gekoppeld aan de workspace-rollen die hem mogen uitgeven.
- Een rol die alleen leesrechten heeft (`viewer`, `billing`) staat alleen bij de `*.read`-scopes; `links.write` heeft `roles: ["owner", "member"]`. Een afgeleide lookup (`getScopesByResourceForRole`) geeft per rol de toegestane scopes.
- De koppeling scope naar rollen staat in een typed structuur, niet in losse if-statements verspreid over de key-aanmaak-route: een tabelregel moet `roles` en `permissions` meegeven om te compileren.
- Dub toont in dit bestand de tabel en de lookup. Controleer zelf in de aanmaak-route server-side dat de gevraagde scopes in die lijst zitten; een verborgen UI-optie is geen afdwinging.

```python
ROLE_SCOPES = {"viewer": {"links.read"}, "member": {"links.read", "links.write"}}

def create_key(role: str, scopes: set[str]) -> Key:
    if not scopes <= ROLE_SCOPES[role]:
        raise Forbidden()
```

Waarom het werkt: de scope-ceiling wordt gecontroleerd op het moment van key-aanmaak; een key kan dus niet meer scopes krijgen dan de uitgevende rol toestaat. Wordt de rol later verlaagd, dan houdt een bestaande key zijn scopes tenzij je die dan ook intrekt.

Niet doen als: het systeem geen rollen kent en elke gebruiker binnen een tenant toch al gelijke rechten heeft; dan voegt een scope-naar-rol tabel complexiteit toe zonder onderscheid te maken.

Toetsvraag: kan een gebruiker met een alleen-lezen rol ooit een API-key met een schrijfscope aanmaken?

Bronnen:
- dubinc/dub@6b463b4bdd9ed2fd9aa416f67b5b77d317b1471e apps/web/lib/api/tokens/scopes.ts:30 "roles: WorkspaceRole[]"
- dubinc/dub@6b463b4bdd9ed2fd9aa416f67b5b77d317b1471e apps/web/lib/api/tokens/scopes.ts:5 "export const SCOPES"

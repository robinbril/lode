# Bij permissieregels telt de laatste match, en een deny is alleen hard als hij die laatste match is

Probleem: een regelset met allow en deny door elkaar geeft een ander resultaat zodra niemand weet of de strengste of de laatste regel telt. Een opgeslagen "altijd toestaan" kan dan ook ongemerkt een ask of deny opheffen.

Oplossing: zo doet opencode het.
- Een regel is `{action, resource, effect}` met effect allow, deny of ask. `*` matcht alles, `?` een teken, en een patroon dat op ` *` eindigt matcht ook het kale commando zonder argumenten.
- `evaluate` plakt alle regelsets achter elkaar en neemt de laatste regel die matcht. Geen match geeft ask (permission.ts:102-113).
- Levert de agent geen permissies op, dan is zijn regelset de ene regel `* * deny` (:20). Sessieregels komen daar nog achter en kunnen die deny dus overschrijven (:190).
- Eerst toetst `denied()` alleen de ingestelde regels (agent plus sessie). Komt daar deny uit, dan stopt de beoordeling (:214). Pas daarna gaan opgeslagen "altijd"-goedkeuringen als allow achter die regels (:215).
- Bij meerdere resources in een aanvraag geeft een deny op een van hen deny, anders een ask op een van hen ask, anders allow (:216-217).
- Daarna ziet een plugin-hook het resultaat en de code neemt het effect van die hook over (:218). Zonder aanwezige gebruiker wordt een ask een deny, tenzij de Unattended-regels het toestaan (:227-237).
- De Claude Agent SDK kiest voor deny het omgekeerde: ook in modus `bypassPermissions` houdt een expliciete deny-regel stand.

Eigen voorbeeld, regelsets als onveranderlijke snapshot zodat een gelijktijdig opgeslagen goedkeuring de beslissing halverwege niet kantelt:

```python
def decide(rules: tuple, saved: tuple, action: str, resources: list[str]) -> str:
    def last(chain, res):
        hit = [r for r in chain if r.matches(action, res)]
        return hit[-1].effect if hit else "ask"
    if any(last(rules, res) == "deny" for res in resources):
        return "deny"
    effects = [last(rules + saved, res) for res in resources]  # saved holds allow rules only
    return "ask" if not effects or "ask" in effects else "allow"
```

Wat dit niet garandeert: `denied()` gebruikt dezelfde `evaluate`, dus een latere allow op hetzelfde pad in de ingestelde regels wint van een eerdere deny. Een opgeslagen allow wint wel van een ingestelde ask, maar niet van een ingestelde deny die de laatste match is. Een aanvraag zonder resources levert in de bron allow op (:194, :217); het voorbeeld vraagt dan.

Waarom het werkt: de volgorde van de regels is de enige voorrangsregel die je moet kennen, en een regel achteraan toevoegen is een bewuste keuze.

Niet doen als: je een deny nodig hebt die geen latere regel kan overschrijven, kies dan strengste-wint: les 57 wint zodra team en persoon allebei regels zetten, les 83 bij shell-commando's.

Toetsvraag: staat er een test die een allow na een deny op hetzelfde pad laat zien met het gedocumenteerde resultaat?

Bronnen:
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/permission.ts:107 "findLast"
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/permission.ts:214 "denied(input, rules)"
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/util/wildcard.ts:12 "endsWith"
- anthropics/claude-agent-sdk-python@3184360393a92ca8a6ec7bbbdee571afd1ce1c56 src/claude_agent_sdk/types.py:2325 "bypassPermissions"

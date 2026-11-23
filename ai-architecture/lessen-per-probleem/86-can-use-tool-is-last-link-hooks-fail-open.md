# De can_use_tool-callback is de laatste schakel in de keten, en een hook die faalt laat standaard door

Probleem: je bouwt een goedkeuringsscherm met `can_use_tool` en denkt dat elke tool-aanroep erlangs komt. In de praktijk beslissen regels en modi vaak al eerder, en een kapotte hook telt als geen mening.

Oplossing: zo werkt de Claude Agent SDK, de publieke interface van Claude Code.
- Zet je `can_use_tool`, dan zet de SDK `permission_prompt_tool_name="stdio"` zodat de CLI zijn vragen over het controleprotocol stuurt. Combineren met een eigen `permission_prompt_tool_name` geeft een `ValueError` (types.py:2397-2406).
- De callback krijgt toolnaam, input en een context met suggesties, `tool_use_id`, `agent_id`, `blocked_path` en `decision_reason` (query.py:647-668). Het antwoord is allow met optioneel `updated_input` en `updated_permissions`, of deny met `message` en `interrupt` (query.py:671-689).
- De callback wordt niet geraadpleegd als de modus `bypassPermissions` is (die keurt alles goed behalve expliciete deny-regels) of als een `allowed_tools`-entry een hele tool toestaat. De SDK waarschuwt daarvoor alleen (`CanUseToolShadowedWarning`) en kan allow-regels uit settingsbestanden niet zien (types.py:2325-2350). Wil je elke aanroep sturen, gebruik dan een PreToolUse-hook.
- `updated_permissions` gaat in zijn geheel of niet mee. Kan een van de updates niet worden verstuurd, dan wordt de aanroep toch toegestaan en alleen gelogd (query.py:118-140).
- Hooks hebben een `HookMatcher` met `matcher`, `hooks`, `timeout` (volgens de commentaar standaard 60 seconden) en `on_failure` (types.py:880-904). Standaard telt een falende hook als geen besluit. Alleen met `on_failure="block"` blokkeert een hook die een fout geeft, `None` teruggeeft of een ongeldige waarde. Een hook zonder mening moet dan `{}` teruggeven. Stop, SubagentStop, TaskCompleted en TeammateIdle negeren de optie, en een CLI die haar niet kent geeft bij het verbinden een fout (query.py:400-407).
- opencode legt zijn hook op een andere plek: een `permission.evaluate`-hook mag het effect na de regels nog wijzigen, maar ziet een ingestelde deny nooit (permission.ts:214-229).

Eigen voorbeeld, een hook die dichtgaat bij een fout in plaats van door te laten:

```python
async def deny_prod_writes(inp, tool_use_id, ctx):
    # a missing key raises, and with on_failure="block" that blocks
    path = os.path.realpath(os.path.join(inp["cwd"], inp["tool_input"]["file_path"]))
    if path.startswith("/srv/prod/"):
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                "permissionDecision": "deny", "permissionDecisionReason": "prod is read-only"}}
    return {}

hooks = {"PreToolUse": [HookMatcher(matcher="Write|Edit", hooks=[deny_prod_writes], on_failure="block")]}
```

Wat dit niet garandeert: rond de callback staat in de SDK geen timeout. Wat de CLI doet bij een fout-antwoord (query.py:749-759) of bij `interrupt` is in deze repo niet te zien.

Waarom het werkt: met `on_failure="block"` telt een kapotte of zwijgende hook als weigering, dus de keten faalt dicht op de plek die je zelf kiest.

Niet doen als: je alleen een vraag aan de gebruiker wilt tonen, dan is `can_use_tool` genoeg. Voor shell-hooks en de sandbox geldt les 64.

Toetsvraag: staat er een test die een aanroep via `allowed_tools` of bypass laat zien waarbij de callback niet draait, plus een hook die faalt met `on_failure` ingesteld?

Bronnen:
- anthropics/claude-agent-sdk-python@3184360393a92ca8a6ec7bbbdee571afd1ce1c56 src/claude_agent_sdk/types.py:2406 "permission_prompt_tool_name"
- anthropics/claude-agent-sdk-python@3184360393a92ca8a6ec7bbbdee571afd1ce1c56 src/claude_agent_sdk/types.py:904 "on_failure"
- anthropics/claude-agent-sdk-python@3184360393a92ca8a6ec7bbbdee571afd1ce1c56 src/claude_agent_sdk/_internal/query.py:664 "self.can_use_tool"
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/permission.ts:218 "hooks.trigger"

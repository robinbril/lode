# Een sandbox begrenst alleen Bash, en een hook houdt alleen tegen wat hij ziet en met code 2 weigert

Probleem: "we hebben een sandbox" wordt vaak gelezen als "elke tool-aanroep is veilig begrensd", maar een sandbox die alleen shell-commando's opsluit, laat Read/Write/WebFetch/MCP-aanroepen volledig vrij als er geen tweede laag bestaat.

Oplossing:
- Een `PreToolUse`-hook kan elke tool zien, maar alleen als de matcher leeg of `*` is; met matcher `Bash` ziet hij de rest niet. Voor een MCP-server is een patroon als `mcp__naam__.*` nodig.
- De sandbox geldt alleen voor de `Bash`-tool en raakt Read, Write, WebSearch, WebFetch, MCP-aanroepen en hooks niet.
- Exitcode 2 blokkeert en toont de melding aan het model. Code 1 blokkeert niet: de melding gaat naar de gebruiker en de aanroep gaat door. Ook een time-out of een script dat niet start blokkeert standaard niet. Een hook die beleid afdwingt, moet dus op elke onverwachte fout met 2 eindigen of `onFailure: "block"` zetten.
- Het voorbeeldscript doet dit verkeerd om voor een poort: bij onleesbare invoer eindigt het met 1 en laat het de aanroep door.
- Harde verboden horen in de deny-regels van het permissiesysteem; de documentatie raadt dat aan boven een hook. Zeggen meerdere hooks iets anders, dan wint `deny`.

```python
# eigen schets: alles wat onverwacht is, blokkeert
try:
    verboden = beoordeel(json.load(sys.stdin))
except Exception:
    sys.exit(2)
sys.exit(2 if verboden else 0)
```

Waarom het werkt: de sandbox begrenst wat een shell-commando kan raken, ook als niemand het herkende; regels en hooks dekken de tools die daar niet doorheen lopen.

Niet doen als: je enige risicovolle tool Bash is en alle andere tools read-only zijn; dan volstaan sandbox plus deny-regels.

Toetsvraag: wordt een MCP-schrijfactie tegengehouden als het hook-script crasht of te lang duurt?

Bronnen:
- anthropics/claude-code@50cdc7005318f630144c28217d1dada32e6ba762 examples/settings/README.md:27 "only applies to the"
- anthropics/claude-code@50cdc7005318f630144c28217d1dada32e6ba762 examples/hooks/bash_command_validator_example.py:78 "blocks tool call"
- https://code.claude.com/docs/en/hooks (gelezen 2026-11-23) "non-blocking error"

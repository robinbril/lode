# Lees je instructiebestanden van projectwortel naar werkmap met een bytebudget, dan verdwijnen bij een vol budget de meest specifieke bestanden eerst

Probleem: een agent leest alleen het AGENTS.md in de root en mist de regels van de submap waarin hij werkt. Of hij leest ze allemaal en vult de helft van zijn context met instructies.

Oplossing: zo doet codex het.
- Per map kiest codex het eerste bestaande bestand uit `AGENTS.override.md`, `AGENTS.md` en daarna de ingestelde fallbacknamen (agents_md.rs:376-377, :261-270). De keuze gaat op bestaan, niet op inhoud: ook een leeg override-bestand wint van AGENTS.md. Een fallbacknaam met een padteken wordt genegeerd (:385-392).
- De zoektocht loopt van de werkmap omhoog tot de eerste map met een rootmarker (standaard `.git`). Zonder marker telt alleen de werkmap; een lege markerlijst zet het omhoog lopen uit. De lijst wordt omgedraaid, dus de root komt eerst en de werkmap laatst (:239-256).
- Het totaal is begrensd door `project_doc_max_bytes`, standaard 32 KiB. De bestanden worden in die volgorde gelezen. Past het niet meer, dan wordt het bestand afgekapt met een waarschuwing, en is het budget op, dan worden de volgende bestanden overgeslagen met een waarschuwing (:147-175). Een groot root-bestand kan dus de submap-instructies wegdrukken.
- Een onbetrouwbaar gemarkeerd project levert helemaal geen projectinstructies (:67). De commentaarregel in config/mod.rs:278 zegt "silently truncated", maar de code zet wel een waarschuwing.

Opencode doet het anders:
- AGENTS.md wint van CLAUDE.md in dezelfde map; CLAUDE.md telt alleen waar geen AGENTS.md staat (instruction-discovery.ts:134-136).
- De volgorde is volgens de commentaar globaal eerst en dan dichtstbij naar verst (:31), dus het omgekeerde van codex. Als de werkmap onder home valt, loopt de zoektocht tot home en niet tot de projectwortel (config/plugin/instruction.ts:40).
- Verdwijnt een bestand net tussen vinden en lezen, dan is de hele set `unavailable`, ook de globale en ingestelde bestanden; een geweigerd bestand wordt alleen overgeslagen (:68-80, :98, :203-206).
- Verandert een instructiebestand tijdens de sessie, dan krijgt het model een diff als die korter is dan de volledige nieuwe tekst (instruction-discovery.ts:153-161).
- In de gelezen bestanden zit geen bytebudget.

Eigen voorbeeld, budget eerst naar het specifiekste bestand (in tekens, voor de eenvoud):

```python
def pick(files_root_to_cwd: list[str], budget: int) -> list[str]:
    out, left = [], budget
    for text in reversed(files_root_to_cwd):
        out.append(text[:left]); left -= len(out[-1])
        if left <= 0: break
    return list(reversed(out))
```

Waarom het werkt: instructies liggen vast aan de map waar ze gelden, en een budget maakt de kosten in context voorspelbaar.

Niet doen als: het project een enkel AGENTS.md in de root heeft, dan is een budget met volgorde extra regelwerk zonder winst.

Toetsvraag: weet je welk bestand het eerst sneuvelt als het budget op is, en staat dat in een test?

Bronnen:
- openai/codex@02390c8d8e39a9b72d12e04e83987d5eb6801310 codex-rs/core/src/agents_md.rs:252 "dirs.reverse"
- openai/codex@02390c8d8e39a9b72d12e04e83987d5eb6801310 codex-rs/core/src/agents_md.rs:376 "LOCAL_AGENTS_MD_FILENAME"
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/instruction-discovery.ts:134 "preferAgents"
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/config/plugin/instruction.ts:40 "const stop"

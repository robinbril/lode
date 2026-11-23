# Bij shell-commando's telt de strengste uitkomst over alle deelcommando's, en zonder vraag mag alleen een expliciete allow-regel de sandbox overslaan

Probleem: `git status && rm -rf build` is in een keer goedgekeurd omdat het eerste deel een allow-regel heeft. Of een commando dat de parser niet kan splitsen glipt langs een deny-regel.

Oplossing: zo doet codex het.
- Een regel is `prefix_rule(pattern, decision, justification, match, not_match)`. De decision is standaard allow; de waarden zijn allow, prompt of forbidden. De `match`-voorbeelden worden bij het laden gecontroleerd, als ingebouwde tests van het beleid (execpolicy/README.md:7-9).
- De uitkomsten staan in een vaste volgorde Allow, Prompt, PromptUser, Forbidden (decision.rs:7-18). Een evaluatie neemt het maximum over alle matches (policy.rs:586).
- Een shell-commando wordt eerst in gewone commando's gesplitst (exec_policy.rs:978). Elk deelcommando gaat apart door de regels en de matches van alle deelcommando's worden samengevoegd (policy.rs:370).
- Heeft een deelcommando geen regelmatch, dan beslist een heuristiek op basis van de approval policy. Een gevaarlijk commando geeft prompt, of bij Never forbidden. Anders geeft Never allow en laat de sandbox beschermen, geeft UnlessTrusted prompt, en geven OnRequest en Granular allow, behalve als een commando in een beperkte sandbox om escalatie vraagt: dan prompt (exec_policy.rs:897-951).
- Een allow mag de sandbox alleen overslaan als elk deelcommando een echte regelmatch allow heeft. Een heuristiek-allow telt daarbij niet mee (exec_policy.rs:496-509).
- Lukt het splitsen niet, dan wordt de hele argv als een commando getoetst (exec_policy.rs:1000). Een voorvoegselregel ziet dan bijvoorbeeld `bash -lc` en niet de commando's in het script. opencode kiest daar strenger: staat er een shell-deny in de regels en kan de scanner het commando niet analyseren, dan volgt een fout in plaats van een vraag (shell/permissions.ts:36).

Eigen voorbeeld, de regels als vaste tuple zodat elke aanvraag een consistente snapshot ziet:

```python
ORDER = {"allow": 0, "prompt": 1, "forbidden": 2}
def verdict(segments, rules, fallback):
    out = []
    for seg in segments:
        hits = [r.decision for r in rules if seg[:len(r.prefix)] == r.prefix]
        out += hits or [fallback(seg)]
    return max(out, key=ORDER.get, default="forbidden")  # no segments: nothing was checked
```

Wat dit niet garandeert: matchen gaat op een tokenvoorvoegsel van het commando, niet op wat het doet. Een script dat een toegestaan programma aanroept dat zelf iets destructiefs doet, valt erbuiten.

Waarom het werkt: een verzameling uitkomsten met een totale volgorde maakt "strengste wint" een max() en geen optelsom van uitzonderingen.

Niet doen als: een specifieke allow een brede deny moet kunnen overrulen, daar past last-match-wins bij (kaart 82).

Toetsvraag: wordt een samengesteld commando met een allow-deel en een forbidden-deel in een test als forbidden beoordeeld?

Bronnen:
- openai/codex@02390c8d8e39a9b72d12e04e83987d5eb6801310 codex-rs/execpolicy-rules/src/policy.rs:586 "RuleMatch::decision"
- openai/codex@02390c8d8e39a9b72d12e04e83987d5eb6801310 codex-rs/core/src/exec_policy.rs:498 "bypass_sandbox"
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/shell/permissions.ts:36 "UnverifiableError"

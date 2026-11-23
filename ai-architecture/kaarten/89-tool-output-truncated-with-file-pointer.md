# Te lange tool-uitvoer wordt afgekapt in de context, maar de volledige tekst blijft in een bestand waar de afkapregel naar wijst

Probleem: een grep of build-log van 40.000 regels vult de context van de agent, of wordt stil afgekapt zodat het model niet weet dat er iets ontbreekt en het deel dat hij zocht kwijt is.

Oplossing: zo doet opencode het in `ToolOutput.truncate`.
- Limieten 2.000 regels en 50 KiB, wat het eerst bereikt is; instelbaar via de config-sleutel `tool_output` (tool-output.ts:13-14, config/plugin/tool-output.ts:16-21).
- Voor het meten worden alle tekstdelen aan elkaar gezet. Bestandsdelen, zoals afbeeldingen, blijven buiten de telling en blijven staan (:78-87, :121-124).
- Past het, dan krijgt het resultaat `truncated: false`. Heeft een tool zelf al `metadata.truncated` gezet, dan blijft het resultaat ongemoeid (:76, :88-91).
- Past het niet, dan gaat de volledige tekst naar `<data>/tool-output/tool_<id>` en krijgt het model het begin plus een regel `[showing lines 1-N of M; full output saved to <pad>]` als aparte tekstdeel. De snede valt op de regel- of bytegrens, en eindigt niet op een regeleinde (:93-115).
- Mislukt het bewaren, dan wordt er toch afgekapt, de markering zegt `could not be saved: <reden>` en `outputPath` ontbreekt in de metadata (:98-104, :141).
- Bewaarde bestanden worden na 7 dagen opgeruimd door een uurlijkse taak (:15, :166).
- De runner past dit toe op elk geslaagd resultaat van een lokaal uitgevoerde tool. Een `Tool.Error` loopt er niet doorheen, en een aanroep die de provider zelf uitvoert ook niet (step.ts:145, :152-155).
- codex kiest anders: `TruncationPolicy` in bytes of tokens, houdt kop en staart en vervangt het midden door `…N chars truncated…` of `…N tokens truncated…`, in de opgemaakte variant met een kop `Warning: truncated output` (output-truncation/src/lib.rs:70, :91; string/src/truncate.rs:38, :53). Deze functies bewaren het weggelaten midden niet.

Eigen voorbeeld, bewaren voor verwijzen en een uniek bestand per aanroep zodat gelijktijdige tools elkaar niet overschrijven:

```python
def bound(text: str, out_dir: Path, max_lines=2000, max_bytes=51200) -> str:
    lines = text.splitlines(keepends=True)
    head = "".join(lines[:max_lines]).encode()[:max_bytes].decode(errors="ignore")
    if head == text:
        return text
    path = out_dir / f"tool_{uuid4().hex}.txt"
    try:
        tmp = path.with_suffix(".part"); tmp.write_text(text, encoding="utf-8"); tmp.replace(path)
        where = f"full output saved to {path}"
    except OSError as e:
        where = f"full output could not be saved: {e.strerror}"
    return f"{head.rstrip()}\n[truncated; {len(lines)} lines; {where}]"
```

Wat dit niet garandeert: uit deze code volgt niet dat het model het bestand daarna mag lezen. Een tool die zelf `truncated` zet, wordt niet opnieuw gemeten.

Waarom het werkt: het model ziet dat er meer is en waar, dus een gerichte vervolgread kost minder dan alles meenemen.

Niet doen als: de uitvoer geheimen kan bevatten, want de volledige tekst staat dan zeven dagen op schijf. Voor het opruimen van oude resultaten later in het gesprek geldt kaart 81.

Toetsvraag: staat in elke afgekapte uitvoer het totaal plus een pad dat bestaat, of de reden als het schrijven mislukte?

Bronnen:
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/tool-output.ts:13 "MAX_LINES"
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/tool-output.ts:113 "full output saved to"
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/session/runner/step.ts:152 "toolOutput.truncate"
- openai/codex@02390c8d8e39a9b72d12e04e83987d5eb6801310 codex-rs/utils/string/src/truncate.rs:53 "chars truncated"

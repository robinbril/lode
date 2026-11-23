# Ongedaan maken werkt met een snapshot van de werkmap per modelstap in een aparte git-map, en terugdraaien herstelt per bestand de eerste stand na de grens

Probleem: een agent wijzigt bestanden via edit-tools, shell-commando's en formatters. Een undo die alleen eigen edit-tools bijhoudt, mist de rest, en een undo in je echte git-historie vervuilt de commits van de gebruiker.

Oplossing: zo doet opencode het.
- Snapshots staan in een eigen git-map onder de datamap van de gebruiker, per project en per werkboom (snapshot.ts:95-97), niet in de repo zelf. Ze werken alleen als de locatie een git-repo is en de instelling aanstaat (:119). Een mislukte capture geeft `undefined` en wordt gelogd, de beurt gaat door (:133-147).
- Een capture is een boom-hash van de werkmap van de sessie binnen de werkboom. Bestanden die de repo negeert (`.gitignore`) en nieuwe bestanden boven 2 MiB worden niet opgenomen (:139-141, git.ts:567-583).
- Elke modelstap vangt een startstand terwijl het providerverzoek al loopt, en na afloop een eindstand. De lijst gewijzigde bestanden is het verschil tussen die twee (step.ts:80, :291-299). Elke opgenomen wijziging in die tijd telt mee, ook van shell-commando's of de gebruiker.
- Een revert kiest een bericht als grens. Voor elk bestand dat na de grens is geraakt, wint de eerste startstand na de grens (revert.ts:104-110). Daarna wordt elk bestand uit zijn eigen boom hersteld. Een pad dat niet in die boom staat, wordt verwijderd; paden buiten de lijst blijven staan (snapshot.ts:63-66, :211-217).
- Een revert onthoudt de stand van vlak voor de eerste revert (`original`, revert.ts:33), zodat `clear` hem kan terugzetten (:58-73). `commit` publiceert alleen een event (:75-81).
- De Claude Agent SDK heeft dezelfde functie anders: `enable_file_checkpointing` maakt volgens de docstring backups van bestanden voor ze worden gewijzigd, en `rewind_files(user_message_id)` zet ze terug (types.py:2858-2863, client.py:364).

Eigen voorbeeld, een capture met een eigen indexbestand per aanroep zodat gelijktijdige captures elkaars lock niet raken:

```python
def capture(shadow: str, work: str) -> str:
    idx = f"{shadow}/index-{uuid4().hex}"
    env = {**os.environ, "GIT_DIR": shadow, "GIT_WORK_TREE": work, "GIT_INDEX_FILE": idx}
    try:
        run(["git", "add", "-A", "--", "."], env=env, cwd=work)  # "." needs the work tree as cwd
        return run(["git", "write-tree"], env=env, cwd=work).strip()
    finally:
        Path(idx).unlink(missing_ok=True)  # add may have failed before writing it
```

Wat dit niet garandeert: omdat de bestandslijst uit twee mapcaptures komt, kan een gelijktijdige wijziging van de gebruiker worden teruggedraaid. Mislukt de capture voor een revert, dan heeft `clear` geen stand om naar terug te gaan (revert.ts:33-36, :64-65).

Waarom het werkt: de undo-stap hangt aan een toestand van de map, niet aan wie de wijziging maakte, dus shell-commando's zitten er vanzelf in.

Niet doen als: de map geen git-repo is, want dan staan snapshots uit, of als de agent vooral genegeerde of nieuwe grote bestanden schrijft, want die vallen buiten de snapshot.

Toetsvraag: wordt een bestand dat een shell-commando heeft aangemaakt bij een undo verwijderd, en is vastgelegd wat er met een nieuw bestand boven 2 MiB gebeurt?

Bronnen:
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/session/revert.ts:107 "message.snapshot?.start"
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/snapshot.ts:141 "maximumUntrackedFileBytes"
- anomalyco/opencode@b51482f9073accbdddf511048cbe9f833e107e1c packages/core/src/session/runner/step.ts:80 "pendingStartSnapshot"
- anthropics/claude-agent-sdk-python@3184360393a92ca8a6ec7bbbdee571afd1ce1c56 src/claude_agent_sdk/types.py:2858 "enable_file_checkpointing"

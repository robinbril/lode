# Eerst goedkeuring, dan draaien in de sandbox, en alleen een sandbox-weigering opent een herhaling zonder sandbox

Probleem: een commando dat in de sandbox faalt omdat de sandbox iets blokkeert, wordt door een agent die overal door wil vaak zonder sandbox herhaald. Dan dekt de eerste goedkeuring een veel groter recht dan de gebruiker zag.

Oplossing: zo doet codex het in `ToolOrchestrator::run`.
- Stap 1 is de eis: de tool levert zelf een `ExecApprovalRequirement` (Skip, NeedsApproval, NeedsHumanApproval, Forbidden), anders bepaalt de approval policy de eis (orchestrator.rs:165, sandboxing.rs:207). Forbidden geeft direct een weigering. Een goedkeuring die niet lukt stopt de aanroep.
- Stap 2 draait onder de gekozen sandbox. Alleen een sandbox-weigering (`SandboxErr::Denied`) opent het herhaalpad (:407); elke andere fout gaat ongewijzigd terug.
- Het herhaalpad heeft drie poorten: de tool moet `escalate_on_failure` hebben (:441), de policy moet een no-sandbox-vraag toelaten (standaard UnlessTrusted ja, Never en OnRequest nee, Granular op een vlag; sandboxing.rs:356-361, maar `apply_patch` zegt bij OnRequest ja), en het schijfbeleid mag geen geweigerde leespaden hebben (:476, sandboxing.rs:301). Netwerkweigeringen lopen via een eigen netwerkvraag.
- Vraagt de tool vooraf zelf om escalatie, dan is dat een gewone goedkeuring in stap 1 en start de eerste poging zonder sandbox, behalve bij geweigerde leespaden (sandboxing.rs:260-290).
- De nieuwe vraag krijgt reden "command failed; retry without sandbox?" en een `ExecCommand`-actie wordt omgezet naar `RequireEscalated`, zodat wat wordt beoordeeld en onthouden het echte bereik van de herhaling is (:521-531).
- Let op: kwam de eerste goedkeuring van een gebruiker of hook, dan slaat codex de nieuwe vraag over (:498-507). Na een oordeel van de Guardian-reviewer, bij strikte auto-review, bij een netwerkvraag en bij een eis die per poging een mens vereist, volgt de vraag wel.

Eigen voorbeeld, strenger dan codex: elke herhaling zonder sandbox krijgt een eigen vraag:

```python
async def run(cmd, policy, ask, sandboxed, plain):
    if policy.needs_approval(cmd) and not await ask(cmd, scope="sandbox"):
        raise Rejected()
    try:
        return await sandboxed(cmd)
    except SandboxDenied as denied:
        if not policy.may_escalate or policy.has_denied_reads:
            raise
        if not await ask(cmd, scope="no-sandbox", reason=denied.reason):
            raise Rejected() from denied
        return await plain(cmd)
```

Wat dit niet garandeert: de functie ruimt niet op wat de eerste poging al deed voor de weigering kwam, en het commando draait bij een herhaling volledig opnieuw. Eén goedkeuring van een gebruiker kan in codex dus twee uitvoeringen dekken; moet een goedkeuring hooguit één uitvoering dekken, dan wint les 56.

Waarom het werkt: een weigering van de sandbox is het enige signaal dat een verruiming voorstelt, en wordt er gevraagd, dan noemt de vraag het echte bereik van de herhaling.

Niet doen als: een commando niet herhaalbaar is zonder bijwerkingen, dan hoort de vraag voor de eerste poging.

Toetsvraag: noemt de vraag na een sandbox-weigering het bereik van de herhaling, en blijft een niet-sandbox-fout zonder herhaling?

Bronnen:
- openai/codex@02390c8d8e39a9b72d12e04e83987d5eb6801310 codex-rs/core/src/tools/orchestrator.rs:407 "SandboxErr::Denied"
- openai/codex@02390c8d8e39a9b72d12e04e83987d5eb6801310 codex-rs/core/src/tools/orchestrator.rs:530 "RequireEscalated"
- openai/codex@02390c8d8e39a9b72d12e04e83987d5eb6801310 codex-rs/core/src/tools/sandboxing.rs:356 "wants_no_sandbox_approval"

# Een schrijvende tool pauzeert en toont het exacte payload, niet alleen een samenvatting

Probleem: "de AI vraagt toestemming" is waardeloos als de gebruiker alleen een vage zin ziet en niet de echte velden die gaan veranderen; en als het record intussen door iemand anders is aangepast, keurt de gebruiker een verouderde actie goed.

Oplossing:
- PostHog's gevaarlijke operaties (`is_dangerous_operation`) bouwen eerst een preview (`format_dangerous_operation_preview`) en roepen dan LangGraph's `interrupt()` aan met een `ApprovalRequest` met preview én het volledige payload. De default van `is_dangerous_operation` is False, dus elke schrijvende tool moet hem zelf overschrijven. Bij goedkeuring mag de gebruiker het payload aanpassen.
- De bewerkte argumenten worden teruggeschreven in dezelfde kwargs-dict die daarna wordt uitgevoerd. Elke tussenlaag die de dict uitpakt, voert ongemerkt de oude argumenten uit. PostHog vergelijkt de staat van het record niet.
- Twenty's voorsteltool bewaart bij een update de huidige waarden van de voorgestelde velden (`currentValues`), bij een verwijdering `updatedAt`. Bij goedkeuring leest hij opnieuw: wijkt het af of is het record onleesbaar, dan draait er niets. De goedkeurder mag alleen de voorgestelde velden wijzigen, het record-id ligt vast.
- Dat is lezen en daarna schrijven, dus er blijft een klein gat tussen die twee. Wil je het dicht, zet de snapshot dan in de WHERE van de schrijfactie.
- Beide geven een afwijzingsroute met vrije feedback die teruggaat naar het model.

Waarom het werkt: goedkeuring gebeurt op het payload dat wordt uitgevoerd, niet op een parafrase; de staleness-check weigert een goedkeuring op inmiddels verouderde data.

Niet doen als: de operatie altijd omkeerbaar en gratis is, zoals een zoekopdracht of een preview; dan kost de pauze alleen tijd.

Toetsvraag: ziet de goedkeurder de exacte velden en waarden die worden geschreven, en wordt een race tussen voorstel en goedkeuring gedetecteerd?

Bronnen:
- PostHog/posthog@9277b47 ee/hogai/tool.py:418 "interrupt(approval_request)"
- twentyhq/twenty@2fd4d03 packages/twenty-server/src/engine/metadata-modules/ai/ai-agent-execution/pausing-tools/propose-tool-call.pausing-tool.ts:62 "currentValues"

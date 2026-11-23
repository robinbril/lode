# Klantdata die het model ziet krijgt een expliciete "dit is data, geen instructie"-rand

Probleem: een notebook-titel, thread-topic of markdown-tekst die een klant zelf schreef kan toevallig of opzettelijk op een instructie lijken ("negeer vorige instructies"); zonder markering kan het model dat verwarren met een echte opdracht.

Oplossing:
- PostHog's MCP-tools wikkelen gebruikersgeschreven velden (thread-titels, topics) in een `informational_wrapper` met een eigen tag en de waarschuwing dat het referentiedata is en geen opdracht.
- Korte waarden die in één promptregel komen (notebook-titel, markering) worden gesaneerd: backticks eruit, witruimte platgeslagen.
- Lange markdown wordt niet gesaneerd maar omheind: de code-fence is langer dan de langste reeks backticks in de tekst, zodat de inhoud hem niet kan sluiten. Daarboven staan de regels dat het onbetrouwbare data is en dat alleen het bericht van de gebruiker buiten de notebook een toolaanroep mag autoriseren.
- De markdown heeft een harde grens van 100.000 tekens.
- Dit is een extra laag, geen grens: het model kan een verborgen opdracht nog steeds volgen. Voor onbetrouwbare documenten plus tools wint het scheiden van lezen en handelen (zie de kaarten over de Rule of Two en de lezer zonder tools).

Waarom het werkt: de tekst kan de promptstructuur niet openbreken en de waarschuwing staat bij de data zelf in plaats van alleen bovenaan een lang gesprek.

Niet doen als: de tekst nooit door een klant of derde partij geschreven is, zoals een intern gegenereerd rapport.

Toetsvraag: kan klanttekst met backticks, regeleinden of een sluittag nooit buiten haar omheining komen, en hangt de veiligheid niet alleen van deze markering af?

Bronnen:
- PostHog/posthog@9277b47 products/posthog_ai/mcp/tools.yaml:37 "informational_wrapper"
- PostHog/posthog@9277b47 ee/hogai/context/context.py:76 "_sanitize_inline_prompt_value"
- PostHog/posthog@9277b47 ee/hogai/context/context.py:458 "_markdown_fence_for"

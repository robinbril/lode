# Het samenvattingsvenster staat ruim onder de modellimiet, want samenvatten blokkeert de gebruiker

Probleem: compactie op het allerlaatste moment (net onder de modellimiet) klinkt zuinig, maar de samenvattingscall zelf duurt net zo lang als elke andere LLM-call, en de gebruiker staat erbij te wachten.

Oplossing:
- PostHog zet `CONVERSATION_WINDOW_SIZE` op 400.000 tokens, ruim onder de 1.000.000 die het model en de samenvatter zelf aankunnen.
- De reden staat letterlijk in de code: een groter venster kost per beurt vooral cache-reads (goedkoop), maar compactie blokkeert de beurt van de gebruiker voor de volledige duur van een samenvattingscall (dure, zichtbare wachttijd).
- `find_window_boundary` kiest het nieuwe startpunt op een mens- of assistent-bericht binnen de laatste 16 berichten en 2048 tokens, zodat het behouden staartje niet met een los tool-resultaat begint. Past er niets, dan wordt alles samengevat en komt het oorspronkelijke verzoek als contextbericht terug.
- De drempel is een bewuste knop: optrekken betekent minder compacties en meer tokens per beurt, verlagen betekent vaker een wachtmoment.
- Het vaste getal past bij één modelvenster. Met meerdere modellen reken je de drempel uit per venster (zie de kaart over compactiedrempels); die regel gaat voor.

Waarom het werkt: de kostenpost die de gebruiker voelt (wachttijd tijdens compactie) wordt apart geoptimaliseerd van de kostenpost die alleen de rekening raakt (tokens per beurt).

Niet doen als: samenvatten asynchroon gebeurt; dan telt de wachttijd niet, maar houd wel ruimte voor de beurten die intussen doorlopen.

Toetsvraag: weet je exact wat een compactie je gebruiker aan wachttijd kost, en is die prijs ingecalculeerd in de venstergrootte?

Bronnen:
- PostHog/posthog@9277b47 ee/hogai/core/agent_modes/compaction_manager.py:52 "CONVERSATION_WINDOW_SIZE"

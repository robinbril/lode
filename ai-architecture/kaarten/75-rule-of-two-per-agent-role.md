# Geef een agent per sessie hooguit twee van: onbetrouwbare invoer, gevoelige data, en schrijven of versturen

Probleem: een agent leest CV's of webpagina's (onbetrouwbaar), ziet kandidaatgegevens (gevoelig) en kan naar het CRM schrijven of mailen (extern). Eén verstopte instructie in een CV is dan genoeg om data weg te sturen.

Oplossing:
- Markeer per agentrol drie eigenschappen: A de rol verwerkt onbetrouwbare invoer, B de rol heeft toegang tot gevoelige systemen of privégegevens, C de rol kan state wijzigen of extern communiceren.
- Een sessie mag hooguit twee van de drie hebben. De regel is geïnspireerd op Willisons "lethal trifecta" (privédata, onbetrouwbare tekst, uitgaand kanaal), maar C is ruimer: ook state wijzigen telt.
- Heeft een taak alle drie nodig, kies dan een van twee uitwegen: start een verse sessie met een schone context voor de stap die schrijft, of laat een mens of een andere betrouwbare controle goedkeuren voordat C gebeurt. Zonder een van die twee draait de agent niet autonoom.
- Filters zijn geen vervanger: een product dat 95 procent van de aanvallen onderschept is bij webbeveiliging een onvoldoende. De enige veilige route is de combinatie vermijden.
- Leg de A/B/C-tabel per rol vast in de repo en laat een test falen als een nieuwe tool een rol naar drie brengt.
- Let op samengestelde tooldozen: een MCP-gebruiker kan tools van verschillende bronnen mengen en zo ongemerkt alle drie bij elkaar brengen.

- Het is een ondergrens: met A en C zonder B kan een injectie nog steeds iets stuk schrijven, en de bron noemt de regel zelf een aanvulling op least privilege.

Waarom het werkt: het is een ontwerpregel die geen oordeel van het model vraagt; ontbreekt één been, dan lukt het weglekken van gevoelige data via een injectie niet meer in dezelfde sessie.

Niet doen als: alle invoer van jezelf komt en nooit van derden; dan valt A weg.

Toetsvraag: heeft elke agentrol een A/B/C-markering, en staat er bij elke rol met alle drie een benoemde menselijke goedkeuring of verse context vóór de schrijfstap?

Bronnen:
- https://ai.meta.com/blog/practical-ai-agent-security/ (gelezen 2026-11-23) "no more than two"
- https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ (gelezen 2026-11-23) "The only way to stay safe"

# Hybrid search weegt vector en keyword op volgorde, citaten houden tokens vast tot een haak compleet is, freshness is een schrijfvolgorde-garantie

Probleem: hybride zoeken, streaming-citaten en freshness lijken drie losse features, maar elk heeft een eigen stille faalmodus: een verwisselde gewichtsvolgorde, een citatiehaak die half naar de UI gaat, of een trage herindexering die een verse chunk overschrijft.

Oplossing:
- Onyx's hybrid search normaliseert vector- en keyword-score met vaste gewichten (allebei 0.5) die exact in de volgorde van de subqueries moeten staan: de som moet 1.0 zijn (dat wordt in code afgedwongen), maar de volgorde wordt alleen in een losse comment bewaakt.
- De streaming-citatieprocessor verwerkt tokens via `_process_segment`: die levert het opgebouwde segment alleen tot de eerste citatie die latere tekst nog kan veranderen (`unsettled`, via `_may_extend`), en pas bij `final=True` (einde van de stream) de rest. De docstring zegt dat de output niet afhangt van hoe de stream in tokens is gesplitst, zodat een "[1]" niet halverwege naar de UI gaat. (`self.hold` in dezelfde klasse is een ander buffertje, voor stop-tokens.)
- Freshness tussen een achterstallige backfill-job en een live schrijver wordt niet via een timestamp-vergelijking afgedwongen maar via een schrijfvolgorde-garantie: de reindex-backfill (`index_raw_chunks`) schrijft met `use_create_only=True`, dus een chunk die de live schrijver al heeft neergezet wordt bij de backfill een onschuldige 409 en kan nooit overschreven worden door de trage achterstand.

Waarom het werkt: elke garantie zit op het punt waar de fout kan ontstaan (gewichtsvolgorde bij het samenstellen van de query, buffer bij het verwerken van tokens (segment pas leveren als het vaststaat), schrijfconflict bij het indexeren), niet achteraf gecontroleerd.

Niet doen als: de index is klein genoeg voor pure keyword- of pure vectorsearch zonder hybride weging, of er is maar één schrijver die nooit gelijktijdig met een backfill draait.

Toetsvraag: kan een verse, live-geïndexeerde chunk ooit overschreven worden door een trage achterstallige herindexeringsjob?

Bronnen:
- onyx-dot-app/onyx@2582a29ef5a52ffff360777b02c47ebff48478ff backend/onyx/document_index/opensearch/search.py:81 "search_content_vector_weight"
- onyx-dot-app/onyx@2582a29ef5a52ffff360777b02c47ebff48478ff backend/onyx/chat/citation_processor.py:444 "_process_segment"
- onyx-dot-app/onyx@2582a29ef5a52ffff360777b02c47ebff48478ff backend/onyx/document_index/opensearch/opensearch_document_index.py:1354 "use_create_only"

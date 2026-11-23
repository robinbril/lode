# Een feit over de toekomst krijgt als valid_at het moment van opname, niet de toekomstige datum uit de tekst zelf

Probleem: een naïeve tijdsgebonden kennisgraaf die "we plannen de migratie voor volgende week" met `valid_at` op die toekomstige datum zet, verbergt het feit "er is een migratie gepland" tot die datum aanbreekt, want het feit lijkt dan nog niet geldig.

Oplossing:
- Graphiti's `EntityEdge` houdt drie losse tijdstempels per feit: `expired_at` (transactietijd, wanneer Graphiti het feit zelf ongeldig verklaarde), `valid_at` en `invalid_at` (geldigheidstijd, wanneer het feit in de werkelijkheid waar werd resp. stopte waar te zijn).
- Voor toekomstgerichte uitspraken (een plan, een belofte, een afspraak) draait na de LLM-extractie `normalize_future_temporal_bounds`: een regex op Engelse vormen als "will", "plans to", "scheduled to", "promises to". Matcht het feit en is de geëxtraheerde `valid_at` leeg of later dan `reference_time` (het episodemoment), dan wordt `valid_at` gelijk aan dat episodemoment: "er is iets gepland" is nu waar, niet pas op de toekomstige datum, die in de feittekst of in attributen blijft staan.
- Een zachte deadline ("will complete by Friday") wordt niet als `invalid_at` bewaard: die wordt leeggemaakt als `invalid_at` na het episodemoment ligt, het feit een deadlinewoord ("by", "before", "no later than", "due by") bevat en geen einde-van-toestand-woord ("until", "expires", "ends", "stops", "no longer"). De regexen zijn Engels: voor Nederlandse bronteksten moet de lijst worden vertaald.

Waarom het werkt: de graaf onderscheidt wanneer iets in de systeemtijd werd vastgesteld van wanneer het in de echte wereld waar was, en een deadline wordt niet verward met het einde van geldigheid.

Niet doen als: de kennis heeft geen tijdsdimensie, zoals statische referentiedata; dan is een gewone, niet-temporele kennisgraaf eenvoudiger.

Toetsvraag: is een gepland-maar-nog-niet-gebeurd feit vanaf vandaag al terug te vinden, of pas vanaf de toekomstige datum die erin genoemd wordt?

Bronnen:
- getzep/graphiti@45fdf546c74da5586e8242fd6588a0801e641e16 graphiti_core/edges.py:247 "episode reference time"
- getzep/graphiti@45fdf546c74da5586e8242fd6588a0801e641e16 graphiti_core/utils/maintenance/temporal_edge_utils.py:48 "not the future occurrence"

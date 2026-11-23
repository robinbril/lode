# Kan een connector de permissies van een document niet bepalen, dan wordt het privé, nooit publiek, en een connector zonder permsync-interface wordt in permissiemodus geweigerd

Probleem: een permissiesync die bij twijfel of een fout een document als publiek of onbekend indexeert, kan per ongeluk een vertrouwelijk document doorzoekbaar maken voor iedereen.

Oplossing:
- Onyx's `ExternalAccess.empty()` zet bij een document waarvan de rechten niet te bepalen zijn `is_public=False` met lege gebruikers- en groepenlijsten. De docstring noemt private maken bij permissiesynchronisatie "a feasible fallback" als rechten om wat voor reden dan ook niet vast te stellen zijn. De zoom-connector geeft het terug als niemand als lezer te noemen is of de opname inmiddels verwijderd is (elke andere fout laat de sync-poging falen), en `github/utils.py` geeft het terug in de MIT-build waar de Enterprise-rechtenlogica ontbreekt.
- `CheckpointedConnectorWithPermSync` is een subklasse van `CheckpointedConnector` met een extra abstracte methode `load_from_checkpoint_with_perm_sync`. De `ConnectorRunner` weigert bij `include_permissions` een connector die die subklasse niet implementeert met een `ValueError` ("Connector does not support permission syncing"), en een niet-gecheckpointte connector met `include_permissions=True` ook. Een connector zonder rechtenlogica kan dus niet stilletjes in permissiemodus indexeren.

Waarom het werkt: een fout of ontbrekende informatie in de permissiesync kan een document alleen verbergen, niet lekken, en een connector zonder permissie-implementatie wordt in permissiemodus afgewezen in plaats van met open rechten geïndexeerd.

Niet doen als: de index bevat alleen publieke documentatie zonder enige toegangsbeperking; dan voegt een ACL-laag alleen complexiteit toe.

Toetsvraag: wordt een document waarvan de permissiesync faalt onzichtbaar voor iedereen, of blijft het per ongeluk doorzoekbaar?

Bronnen:
- onyx-dot-app/onyx@2582a29ef5a52ffff360777b02c47ebff48478ff backend/onyx/access/models.py:62 "feasible fallback"
- onyx-dot-app/onyx@2582a29ef5a52ffff360777b02c47ebff48478ff backend/onyx/connectors/interfaces.py:366 "CheckpointedConnectorWithPermSync"
- onyx-dot-app/onyx@2582a29ef5a52ffff360777b02c47ebff48478ff backend/onyx/connectors/connector_runner.py:158 "CheckpointedConnectorWithPermSync"

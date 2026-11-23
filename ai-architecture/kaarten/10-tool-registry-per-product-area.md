# Elk productonderdeel levert zijn eigen tool-klasse aan, de backend registreert ze automatisch

Probleem: een los bijgehouden "lijst van alle AI-tools" in één bestand raakt na een paar producten uit sync met wat elk team daadwerkelijk bouwt.

Oplossing:
- PostHog loopt bij het opzoeken van een contextuele tool alle `products/<naam>/` mappen langs en importeert `products.<naam>.backend.max_tools`. De import vangt `ModuleNotFoundError`: ontbreekt het bestand, dan wordt het product overgeslagen. Een ontbrekende dependency binnen zo'n bestand verdwijnt daardoor even stil; log die twee gevallen apart.
- Elke tool-klasse meldt zichzelf aan in een globale registry zodra de klasse wordt gedefinieerd (Python's `__init_subclass__`).
- De namen blijven wel centraal: `__init_subclass__` gooit een fout als de toolnaam niet in de enum `AssistantTool` staat, en die staat in een gedeeld schemabestand.
- Twenty lost het anders op: één NestJS-provider per technische categorie (database, workflow, dashboard, actie, front-component, logic-function, mcp), met de hand opgesomd in één `TOOL_PROVIDERS`-factory. Een nieuwe categorie raakt dus dat ene bestand, een nieuwe tool binnen een categorie niet.

Waarom het werkt: de uitvoerende code en de registratie staan bij elkaar, terwijl een gesloten namenlijst voorkomt dat een typefout of naamconflict ongemerkt een tool oplevert.

Niet doen als: je maar een handvol tools hebt en nooit meer dan één team erop werkt; dan is een vaste lijst sneller te overzien dan dynamische discovery.

Toetsvraag: raakt een nieuwe tool buiten de eigen productmap hooguit de gedeelde namenlijst, en faalt de registratie hard bij een onbekende naam?

Bronnen:
- PostHog/posthog@9277b47 ee/hogai/registry.py:21 "backend.max_tools"
- PostHog/posthog@9277b47 ee/hogai/tool.py:196 "AssistantTool(cls.name)"
- twentyhq/twenty@2fd4d03 packages/twenty-server/src/engine/core-modules/tool-provider/tool-provider.module.ts:80 "TOOL_PROVIDERS"

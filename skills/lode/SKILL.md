---
name: lode
description: Ontwerpt en bouwt met lode als voorbeeld - volledige codebases en lessen, getoetst met airesearch en council. Gebruik voor een plan in een bestaand product, een nieuw project, of het overnemen van een app, scherm, component of architectuur. Triggers - "/lode", "gebruik lode", "plan dit goed", "nieuw project opzetten", "neem dit over uit", "hoe doen de besten dit".
---

# lode

`LODE` is de repo van deze skill: volg de link van deze map en ga twee mappen omhoog. Geen link? Vraag waar de repo staat.

Wat er in het project al staat wint. Lode laat zien hoe goed het kan.

## Beste vertrekpunt

| Je bouwt | Open in `LODE` |
|---|---|
| Chatscherm | `frontend/chatbot-compleet-chatprogramma`, `frontend/assistant-ui-chatonderdelen` |
| Composer, gesprekken, werkplek zonder framework | `frontend/grokbot-invoerveld-en-werkplek` |
| Goedkeuringskaart, computerpaneel | `frontend/openmausbot-bots-en-meekijken`, `ai-architecture/openbot-goedkeuring-en-logboek` |
| Menu, dialoog, popover, tooltip | `frontend/radix-primitives-menus-en-dialogen`, `frontend/shadcn-ui-knoppen-en-formulieren` |
| Commandomenu, meldingen, lange lijst | `frontend/cmdk-zoekvenster`, `frontend/sonner-meldingen`, `frontend/tanstack-virtual-lange-lijsten` |
| Takenbord of issue-scherm | `frontend/circle-takenbord` |
| Interface uit modeluitvoer | `frontend/json-render-scherm-door-model`, `frontend/ai-elements-antwoorden-tonen` |
| Agentlus in Python | `ai-architecture/pydantic-ai-agent-in-python`, `ai-architecture/openai-agents-werk-doorgeven` |
| Agentlus in TypeScript, codeer-agent | `ai-architecture/opencode-agent-in-typescript`, `ai-architecture/codex-commandos-en-afscherming`, `ai-architecture/deepseek-harness-uitbreidbare-agent` |
| Goedkeuring, beleid, audit | `ai-architecture/openbot-goedkeuring-en-logboek` |
| Agent voor een team | `ai-architecture/qm-teamagent-in-slack` |
| Bedrijfskennis met rechten | `ai-architecture/onyx-bedrijfskennis-met-rechten` |
| Claude Code in je product | `ai-architecture/claude-agent-sdk-claude-code-in-je-product` |
| SaaS-backend | `backend/fastapi-template-inloggen-en-database`, `backend/polar-betalen-en-abonnementen` |
| Achtergrondwerk en herstel | `backend/hatchet-achtergrondwerk`, `backend/dbos-hervatten-na-storing` |
| Webhooks, rechten | `backend/svix-webhooks-versturen`, `backend/openfga-wie-mag-wat` |
| Iets dat hier niet staat | skill `ui-ophalen`, en `pick-ui-library` voor een library |

De precieze bestanden staan in `<map>/CODEBASES.md`. Lessen per taak staan in `LODE/AGENTS.md`. Lees daar ook de grenzen over licenties en data.

## Bestaand product aanpassen

1. **Kijk naar de echte tak** en zoek of het er al is, met twee zoekwoorden, in backend en frontend. Is het er, breid dan uit.
2. **Vind de plek waar alle paden samenkomen** en elke ingang waar dezelfde gegevens binnenkomen.
3. **Kies** één codebase en hooguit 6 lessen. Lees alleen de genoemde paden.
4. **Ontwerp** de eenvoudigste vorm: toestanden, fouten, rechten, dubbel en gelijktijdig werk. Gaat het over mensen, vul het gegevensblok in `references/aanpassing.md` in.
5. **Toets** met airesearch of council (zie hieronder) en pas het ontwerp aan.
6. **Plan en akkoord** (zie hieronder).
7. **Bouw een dunne plak** van database tot scherm. De test moet de naïeve versie afkeuren.
8. **Verwijder het oude pad.**

## Nieuw project

Volg `references/nieuw.md`: eerst "moet het nieuw", dan 20 echte gevallen, fundament in volgorde, eerste week per dag.

1. **Laat council kiezen** tussen minstens twee opzetten met een codebase uit de tabel als basis.
2. **Laat airesearch het AI-deel scoren** voor je bouwt.
3. **Plan en akkoord.**
4. **Bouw één taak helemaal af** voor de tweede begint.

## Overnemen

1. **Open de codebase** via `CODEBASES.md` en draai hem niet.
2. **Schrijf op:** toestanden, props en events, toetsen en focus, beweging, randgevallen, afhankelijkheden.
3. **Zoek het onderdeel in het project.** Bestaat er iets, breid dat uit.
4. **Plan en akkoord.**
5. **Bouw na** in het framework van het project. Gedrag uit de bron, vormtaal en namen uit het project. Neem je code over, dan ook de licentietekst.
6. **Vergelijk** op 1440 en 390 px, licht en donker, met toetsenbord. Laat leeg, laden en fout zien.

Van React naar Vue 3: hooks worden composables, context wordt provide/inject, portals worden `Teleport`. Naar vanilla JS: één factory per onderdeel met een store.

## Toets met airesearch en council

Elk plan gaat langs minstens één. Ze staan in `LODE/ai-architecture/skills/`; niet geïnstalleerd, lees dan hun `SKILL.md`.

| Situatie | Gebruik |
|---|---|
| Model, agent, tool, MCP, RAG of eval | `airesearch` |
| Meer goede wegen, duur, of moeilijk terug te draaien | `council` |
| Allebei | eerst `airesearch`, dan `council` |
| Geen van beide | `council` kort: drie stemmen, één ronde |

Een wijziging van één bestand die je met één commit terugdraait, mag zonder.

Gebruik de uitkomst: noem de sterkste tegenwerping en wat je ontwerp daardoor anders doet. Controleer feiten in de code zelf; een stem is geen bewijs.

## Plan en akkoord

Er gaat altijd een plan vooraf, en de gebruiker keurt het goed voor je iets bouwt.

| Situatie | Doe |
|---|---|
| De aanpak staat open: de gebruiker denkt mee, twijfelt, of er is discussie | Stel een plan voor: jouw aanbeveling, hooguit twee alternatieven met het verschil, en de vraag die de keuze bepaalt. Verwerk het antwoord en stel het bijgewerkte plan voor |
| De aanpak is duidelijk | Schrijf het hele plan uit en vraag akkoord |

Het uitgeschreven plan: doel, bron uit lode en waarom, ontwerp, plakken in volgorde met test, risico, wat je weglaat. Sluit af met één vraag: akkoord, of wat moet anders?

Tot het akkoord lees je alleen en wijzig je niets. Na het akkoord bouw je door tot de eerste plak werkt. Verandert het plan onderweg wezenlijk, leg dan alleen die verandering opnieuw voor. Een akkoord geldt voor dit plan, niet voor versturen, verwijderen, betalen of live zetten.

## Antwoord

Hooguit één pagina: wat je bouwt, welke bron en waarom, het ontwerp, wat de toets veranderde, de eerste plak met test, en wat je weglaat. Meer achtergrond: `references/wijsheid.md`. Prompts voor de gebruiker: `references/prompts.md`.

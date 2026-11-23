# Kader: nieuw project of nieuwe module

## 0. Moet het nieuw

Beantwoord eerst: welk bestaand eigen product heeft al 60 procent? Zo ja, dan is dit een module en gebruik je `aanpassing.md`. Nieuw begint pas als de data, de gebruikers of het risico echt anders zijn.

## 1. Eén pagina vooraf

| Onderdeel | Vul in |
|---|---|
| Gebruiker en de ene taak die vandaag pijn doet | |
| Doelzinnen met waarneming | |
| Noemer: alle gevallen van die taak in een week | |
| 20 echte gevallen als evalset, met verwacht resultaat | |
| Label: losse aanroep, workflow, agent of meer agents | |
| Waarom het lagere label niet genoeg is (ai 78) | |
| Data: wat, van wie, hoe gevoelig, hoe lang | |
| Wat een mens altijd zelf beslist | |
| Stopregel: wanneer gooien we het weg | |

Klaar als iemand buiten het project de doelzinnen met ja of nee kan beantwoorden.

## 2. Fundament, in deze volgorde

1. **Repo:** root legt uit, mappen naar verantwoordelijkheid, grenzen door een tool bewaakt (be 01).
2. **Start:** configuratie faalt hard bij een ontbrekend of nepgeheim (be 09).
3. **Identiteit en tenant:** rechten in de query of policy, test met rolwissel (be 02, 17).
4. **Fouten en log:** vaste foutcodes, auditregel per soort gebeurtenis (be 10, 13).
5. **Eén register van acties:** schema, rechten rond de uitvoering, lezen direct, schrijven als voorstel (ai 50, 55, 11).
6. **Akkoord:** duurzame rij, exacte waarden, hooguit één keer verbruikt (ai 13, 56, 57).
7. **Modellus:** klein, met limieten, getypte tools en fouten die zeggen of herproberen zin heeft (ai 30, 34, 21).
8. **Context:** stabiel voorstuk, budget, schermcontext als data (ai 73, 54, 12).
9. **Kennis:** toegangslijst in de zoekvraag, onbekend is privé (ai 41, 42).
10. **Evals in CI:** de set uit stap 1 blokkeert (ai 70, 71, 72).
11. **Zicht:** wat echt verstuurd is, kosten per aanroep (ai 80, 63).
12. **Duurzaam werk, MCP, meer agents:** pas als één echte taak het vraagt (ai 35, 60, 20, 79).

Elke stap is één plak met een check. Sla je er een over, schrijf dan waarom.

## 3. Vertrekpunt

| Situatie | Neem | Waarom |
|---|---|---|
| Python-backend met AI | eigen actieregister plus `pydantic-ai` voor de lus | rechten en data blijven van de app |
| TypeScript met AI | ontwerp van agent-native, delen uit `opencode` of `openbot` | één actie voor UI, HTTP, agent en MCP |
| Webapp zonder AI | `fastapi-template`, met patronen uit `polar` | bewezen indeling |
| Chatscherm | `chatbot` of `assistant-ui`; gedrag uit fe 01, 02, 18, 19, 20 | lastige randgevallen zijn opgelost |
| Werkplek voor bots | `openbot` voor toezicht, `grokbot` voor gedrag | stuur overnemen, akkoord, hervatten |
| Codeer-agent | `codex`, `opencode`, `deepseek-harness` | sandbox, permissies, ongedaan maken |

## 4. Interface

1. Bekijk twee werkende voorbeelden en schrijf op wat je overneemt: rijhoogte, één icoonkolom, wat achter een menu zit.
2. Teken eerst de toestanden: leeg, laden, fout, gedeeltelijk, geen rechten, offline, bezig, onderbroken.
3. Kies een vormtaal in tokens voor het eerste component. Eén grijsfamilie, één accent, vaste ritmes.
4. Kies een library via `LODE/frontend/skills/pick-ui-library` voor je zelf bouwt.
5. Toetsenbord, focus en schermlezer horen bij de eerste versie.

## 5. Eerste week

| Dag | Resultaat |
|---|---|
| 1 | één pagina, 20 gevallen, aanval door tweede model |
| 2 | fundament 1 tot 4, CI groen |
| 3 | register met drie leesacties, zelfde acties in UI en chat |
| 4 | één schrijfactie met akkoord, van klik tot logregel |
| 5 | evalset in CI, demo met echte gebruiker, beslissing: door, anders of stop |

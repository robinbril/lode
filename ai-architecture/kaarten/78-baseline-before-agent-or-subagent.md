# Je voegt een agent of subagent pas toe nadat een eenvoudiger ontwerp aantoonbaar tekortschiet

Probleem: een team bouwt meteen een orkestrator met vijf subagents. Het kost meer tijd en geld, en niemand weet of één prompt of een vaste keten hetzelfde had gehaald.

Oplossing:
- Onderscheid een workflow (code bepaalt het pad) van een agent (het model bepaalt zijn eigen proces). Een agent ruilt wachttijd en kosten voor een betere uitkomst, dus die ruil moet zichtbaar worden.
- Begin met directe modelaanroepen en een vaste keten. Frameworks leggen lagen over de prompts heen en maken debuggen lastiger.
- Bouw eerst een kleine eind-tot-eind evalset (10 gouden voorbeelden is genoeg om te starten) en leg de score van de baseline vast: één prompt of de vaste workflow.
- Zet het model pas in de lus als de volgorde van stappen vooraf niet vaststaat. Voor elke beslissing die het model neemt: kon een conditie, een opzoeking of een classifier het ook?
- Een subagent is te rechtvaardigen bij drie situaties: de context loopt vol en dat kost meetbaar kwaliteit, taken kunnen parallel met een verse context, of één agent kiest slecht tussen tools of krijgt tegenstrijdige instructies.
- In eigen vergelijkingen van Anthropic bij enkele bedrijven presteerde één agent met skills vaak beter dan een ontwerp met subagents, op kwaliteit en vaak ook met lagere kosten en wachttijd per taak.
- Splits werk op de context die elk deel nodig heeft, niet op functietitel; anders spiegelt de architectuur het organisatieschema.
- Bouw terug op één stap per keer: vervang een subagent door een tool of skill en vergelijk de evalscore met en zonder.

Waarom het werkt: elke extra laag moet zijn plek verdienen in een getal, en een vaste keten is goedkoper, sneller en beter te debuggen.

Niet doen als: de taak werkelijk open is (onderzoek met onvoorspelbare stappen); dan is de agent het juiste gereedschap, mits gemeten.

Toetsvraag: staat er een baselinescore van een eenvoudiger ontwerp naast de agent, met het verschil in kwaliteit, kosten en wachttijd?

Bronnen:
- https://www.anthropic.com/engineering/building-effective-agents (gelezen 2026-11-23) "simplest solution possible"
- https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop (gelezen 2026-11-23) "single agent with skills"

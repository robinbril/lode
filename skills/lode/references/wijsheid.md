# Wijsheid

Per regel één inzicht. `ai`, `be` en `fe` verwijzen naar een kaart in `LODE/ai-architecture`, `backend` en `frontend`, map `kaarten/`. Lees de kaart voor je hem toepast.

## Plannen

1. De werkmap liegt vaak. Een keuring op een map die 1.636 commits achterliep gaf 44 punten en een vals alarm; op de echte tak was het 54.
2. Wat je wilt bouwen bestaat vaak al onder een andere naam. Zoek het concept, niet jouw woord.
3. Zonder noemer is elk percentage verzonnen. Een eindige lijst (pagina's, operaties, gevallen) verslaat "bijna alles gezien".
4. Een bronregel die klopt bewijst de uitleg niet. Bij de eerste 92 kaarten klopte elke verwijzing en moesten 81 toch worden aangepast.
5. Laat iemand anders weerleggen. Wie het schreef, leest wat hij bedoelde.
6. Vraag bij een aanval apart: verkeerd doel of verkeerde volgorde. Meestal is het de volgorde.
7. Het eenvoudigste ontwerp dat de meting haalt wint (ai 78).
8. Klaar is een commando met exitcode 0 (ai 94).
9. Schrijf op wat je weglaat. Dat is de helft van de architectuur.
10. Lees de voorwaarden en licentie voor het eerste verzoek, niet na de laatste.

## AI in een product

11. Eén capaciteit, één tool, één deur. Een vlag die de dispatcher moet onthouden beschermt alleen wie hem onthoudt; zet rechten rond de uitvoering zelf (ai 50, 55).
12. De agent handelt als de persoon. Een lege rechteneis is geen controle (ai 11).
13. De mens keurt exacte waarden goed, geen samenvatting (ai 13).
14. Akkoord is hooguit één uitvoering, afgedwongen met één voorwaardelijke UPDATE (ai 56).
15. Bij lagen wint de strengste regel, niet de nieuwste (ai 57).
16. Geef een rol hooguit twee van drie: onbetrouwbare invoer, gevoelige data, schrijven of versturen (ai 75).
17. Laat vreemde tekst lezen door een aanroep zonder tools die een getypt object teruggeeft (ai 76). Markeren is een extra laag, geen grens (ai 22).
18. Schermcontext is een verwijzing. De server haalt de inhoud op onder de rechten van de gebruiker (ai 12).
19. Rechten op kennis horen in de zoekvraag. Onbekend is privé (ai 41).
20. Een toolbeschrijving is een prompt. Noem de buur die je dan wél moet kiezen (ai 74).
21. Een fout aan het model zegt of herproberen zin heeft (ai 21).
22. Stabiel voorstuk, wisselende staart. Verander tools niet midden in een gesprek (ai 54, 19).
23. Gooi alleen weg wat je terug kunt halen. Bewaar de aanroep en de fout (ai 81, 89).
24. Een gesprek is een rij items waar je alleen aan toevoegt. Berichten zijn een afleiding (ai 61).
25. Een beurt overleeft de tab pas als hij een taak is met een eigen sleutel (ai 14, 35).
26. Een oude werker mag na overname niets meer schrijven, ook niet zonder token (ai 60).
27. Een hook die faalt laat vaak door. Test de weigering (ai 64, 86).
28. Een mens die het stuur neemt sluit eerst de deur en wacht dan op wat loopt (ai 90).
29. Een subagent weet alleen de opdracht: doel, vorm, bronnen, grenzen, klaar (ai 79).
30. Budget per aanroep, opnieuw bij elke terugval (ai 34, 63).
31. Log wat echt verstuurd is (ai 80).
32. Evals komen uit echte missers, en vergelijk met en zonder per taak (ai 71, 70).
33. Een judge telt pas mee als je weet wat hij mist en wat hij onterecht afkeurt (ai 72).

## Backend

34. Grenzen tussen modules bewaakt een tool (be 01).
35. Een policy is pas snel met een index op de gefilterde kolom, en pas bewezen met een rolwissel (be 02, 17).
36. Een lijst heeft een deadline en een limiet, en zegt eerlijk of hij compleet is (be 03).
37. Een idempotentiesleutel hoort bij tenant, endpoint en een slot (be 04).
38. De uitgaande gebeurtenis staat in dezelfde transactie (be 05).
39. Onderteken id, tijd en inhoud (be 06).
40. Wachtrijlimieten horen per tenant (be 07).
41. Een nepgeheim in productie is een opstartfout (be 09).
42. Opruimen draait standaard als proef (be 14).

## Frontend

43. Volg de bodem tot iemand omhoog scrolt (fe 01).
44. Een tool-aanroep is een ding met een eigen staat (fe 02).
45. Een optimistische stap is een tijdelijke laag over de bevestigde staat (fe 04).
46. Leg de bedoeling vast voor je verstuurt, en laat een opzoeking beslissen bij twijfel (fe 20).
47. Na herladen is "bezig" onderbroken tot het tegendeel blijkt (fe 23).
48. Async validatie heeft drie uitkomsten (fe 11).
49. Een live region leest alleen nieuwe knopen voor (fe 16).
50. Neem gedrag over, niet de pixels. Tokens van het project winnen (fe 13).

## Werken met agents

51. Goedkoop model zoekt en haalt op, sterk model ontwerpt en oordeelt.
52. Eén schrijver per set bestanden, een ander die weerlegt.
53. Geef een controle als script, niet als verzoek om goed op te letten.
54. Een rapport van een agent is een aanwijzing tot jij de regel opent of het commando draait.
55. Laat agents schrijven in een vaste vorm; dan kan een machine de vorm controleren en een mens de inhoud.

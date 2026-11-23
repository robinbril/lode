# Kader: aanpassing in een bestaand product

Vul dit in voor je code schrijft. Laat geen rij leeg; "onbekend" mag, met hoe je het te weten komt.

## 1. Kader

| Vraag | Antwoord |
|---|---|
| Wie merkt wat, op welk scherm of endpoint | |
| Wat is nu waar (met bewijs) | |
| Wat moet waar worden (doelzinnen) | |
| Wat blijft bewust hetzelfde | |
| Wie beslist, en waarover alleen een mens beslist | |
| Wanneer stoppen we (tijd, kosten, uitslag) | |

## 2. Naad

| Onderdeel | Bestand:symbool | Aanroepers | Zusterstuk dat je kopieert |
|---|---|---|---|
| Ingang (route, tool, event) | | | |
| Besluit (rechten, beleid) | | | |
| Schrijfplek (de ene plek waar het gebeurt) | | | |
| Scherm | | | |
| Test die dit pad echt draait | | | |

De fix hoort op de plek waar alle paden samenkomen. Tel de aanroepers; mis je er één, dan is de wijziging half.

## 3. Risico

| Vraag | Zo ja |
|---|---|
| Raakt het data die niet terug te draaien is | voorstel, akkoord, dan uitvoeren (ai 55, 56) |
| Komt er tekst van buiten in een model | aparte stap zonder tools (ai 76) en rol-indeling (ai 75) |
| Meer dan één tenant of rol | test met rolwissel op een echte database (be 02, 17) |
| Nieuwe kolom of index | migratie met slot-tijd, in stappen (be 08) |
| Herhaalbaar verzoek of webhook | sleutel per tenant, ondertekening, outbox (be 04, 05, 06) |
| Werk langer dan een verzoek | duurzame stap met sleutel (ai 14, 35; be 07) |
| Persoonsgegevens | doel, bewaartermijn, wissen, logregel (be 13, 14) |
| Scherm met laden, leeg, fout | drie verschillende beelden, toetsenbord en schermlezer |

## 3b. Gegevensblok (als het over mensen gaat)

| Vraag | Antwoord met bestand:symbool |
|---|---|
| Welke tekst gaat naar welke verwerker, en staat die dat toe | |
| Wie mag niet verwerkt worden (beperking, bezwaar, legal hold), en waar wordt dat getoetst vóór de aanroep | |
| Wat wordt bewaard, waar, hoe lang, ook in logs en modelaanroepen | |
| Vindt wissen en inzage elk nieuw record, via welke sleutel | |
| Wie ziet het voorstel, en wie mag beslissen | |
| Kan tekst van buiten een actie, ontvanger of bedrag kiezen | |

## 4. Volgorde die meestal wint

1. Meet het huidige gedrag: test of evalgeval dat nu rood is.
2. Lezen voor schrijven.
3. Eén deur: alle paden langs dezelfde functie.
4. Voorstel en akkoord voor je schrijft.
5. Zichtbaar maken wat er gebeurde: logregel, staat, kosten.
6. Pas dan sneller, mooier of breder.
7. Oude pad weg in dezelfde wijziging.

## 5. Plakken

| Plak | Doelzin | Check (commando) | Rood gezien | Groen gezien | Terugdraaien |
|---|---|---|---|---|---|

Een plak past in één PR die een mens in tien minuten kan lezen.

## 6. Niet doen

Schrijf minstens drie dingen op die je weglaat, elk met de reden. Een tweede rechtenlaag, een tweede opslag en een raamwerk voor één geval horen hier bijna altijd.

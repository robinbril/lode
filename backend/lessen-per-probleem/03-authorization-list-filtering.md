# "Welke objecten mag deze gebruiker zien" krijgt een harde deadline en een harde cap, niet alleen een query

Probleem: een autorisatiemodel dat per losse check (`mag X dit object Y`) werkt, verleidt tot een naieve implementatie van een lijstvraag ("welke objecten mag X zien") die intern elk object los checkt. Bij een grote tenant loopt dat ongemerkt vast of traag.

Oplossing:
- Een losse `ListObjects`-operatie loopt het relatiegraaf achterstevoren af (reverse expansion) om kandidaat-objecten te vinden. Alleen kandidaten die nog verdere evaluatie nodig hebben krijgen daarna een eigen `Check`; de rest wordt direct teruggegeven.
- De operatie krijgt een tijdslimiet (`listObjectsDeadline`, een `context.WithTimeout`) en een maximum aantal resultaten (`listObjectsMaxResults`, een serverinstelling). Bij overschrijding stopt de evaluatie en komt terug wat al gevonden is, zonder fout.
- Het maximum zit in de server-config, het request kan er niet om vragen. De `1000` in `cappedMaxResults` begrenst alleen de grootte van het interne kanaal (10 procent, minimaal 10), niet de resultaten.
- Let op: bij een deadline krijgt de aanroeper geen signaal dat het antwoord onvolledig is (in de code staat een TODO voor een header). Voeg zelf een `truncated`-vlag toe.

Waarom het werkt: een tijds- en resultaatbudget verandert een onbegrensde graafwandeling in een voorspelbare operatie. Partiele resultaten bij een deadline zijn beter voor een lijstweergave dan een timeout zonder resultaat, mits de UI weet dat de lijst kan ontbreken.

Niet doen als: de lijstvraag een exacte, volledige set moet zijn voor een beslissing met gevolgen (bijvoorbeeld een export voor een audit); dan is paginering met een stabiele cursor eerlijker dan een budget dat vroeg kan afkappen.

Toetsvraag: geeft de lijstoperatie bij een tenant met honderdduizenden objecten een antwoord binnen een vast tijdsbudget, in plaats van te wachten tot de hele graaf doorlopen is?

Bronnen:
- openfga/openfga@d67ba7b1d2eaf945cffab3a9129ca1a4c7ad5251 pkg/server/commands/list_objects.go:63 "listObjectsDeadline"
- openfga/openfga@d67ba7b1d2eaf945cffab3a9129ca1a4c7ad5251 pkg/server/commands/list_objects.go:355 "cappedMaxResults"

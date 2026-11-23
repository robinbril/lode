# Een foutantwoord krijgt een vaste enum-code, los van de leesbare boodschap

Probleem: een client die alleen een vrije-tekst foutmelding krijgt (`"Invalid request"`), kan daar nooit automatisch op reageren: de tekst kan per taal of per versie veranderen, en "parse de boodschap" is geen stabiel contract.

Oplossing:
- Elk antwoord heeft een vast envelope-veld `result` (`success` of `error`), een `msg` voor mensen en, bij een fout, een los machineleesbaar `code`-veld met de naam uit een vaste enum.
- De foutcode, de HTTP-status (`http_status_code`) en de extra velden (`data_fields`) staan op de exceptionklasse zelf, niet losjes in de route die hem opvangt, zodat dezelfde foutsoort overal dezelfde code en status geeft.
- Een middleware zet de exception om naar het antwoord; app-code raised alleen.
- Succes en falen delen dezelfde envelope-vorm (`result` plus de rest van de data), zodat een client een enkele parser heeft voor beide gevallen.

```python
class ErrorCode(Enum):
    BAD_REQUEST = auto()
    NO_SUCH_WIDGET = auto()

class NoSuchWidgetError(JsonableError):
    code = ErrorCode.NO_SUCH_WIDGET
    http_status_code = 404
```

Waarom het werkt: een enum-code blijft stabiel als de vrije tekst wordt herschreven of vertaald, en een typefout in de code valt bij import op. Een client bouwt zijn eigen foutafhandeling op de code, niet op de tekst.

Niet doen als: de API alleen intern door een enkel team wordt aangeroepen dat de broncode van beide kanten beheert; dan is een gedeeld exception-type vaak genoeg zonder een losse publieke enum.

Toetsvraag: kan een client op een specifieke foutsoort reageren zonder de vrije-tekst boodschap te parsen?

Bronnen:
- zulip/zulip@3ed5a54415180957a108e987d3c59c7bed15147d zerver/lib/exceptions.py:73 "class JsonableError"
- zulip/zulip@3ed5a54415180957a108e987d3c59c7bed15147d zerver/lib/response.py:104 "res_type"

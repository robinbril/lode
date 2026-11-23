# Een placeholder-secret in productie is een opstartfout, geen waarschuwing

Probleem: een `.env`-bestand met een duidelijke placeholder (`changethis`) als default voor `SECRET_KEY` of een wachtwoord voorkomt niets als niemand hem ooit vervangt. Een app die daarmee gewoon opstart, merkt het zelf niet, en de eerste die het merkt is een aanvaller.

Oplossing:
- Valideer settings bij het opstarten (een `model_validator(mode="after")` in de settings-class, niet in een losse health-check) tegen de placeholder-waarde uit de `.env`-template. Het template controleert alleen de letterlijke waarde `changethis`; een lijst met meer bekende waarden moet je zelf toevoegen.
- Onderscheid omgeving: alleen als `FASTAPI_ENV == "development"` is een placeholder een `warning`. Elke andere waarde, ook niet gezet, geeft een harde `ValueError` die het opstarten blokkeert.
- Check niet alleen losse env-vars (`SECRET_KEY`, `FIRST_SUPERUSER_PASSWORD`), maar ook het wachtwoord in de database-connectiestring (`DATABASE_URL`).

```python
def _check_default_secret(self, var_name: str, value: str | None) -> None:
    ...

def _enforce_non_default_secrets(self) -> Self:
    ...
```

Waarom het werkt: de check draait bij elke opstart van elke instantie, dus een vergeten secret in een nieuwe omgeving faalt meteen en zichtbaar, in plaats van pas bij een incident maanden later.

Niet doen als: secrets al verplicht via een externe secret-manager worden aangeleverd zonder enige lokale default; dan is er geen placeholder-waarde om tegen te checken.

Toetsvraag: start deze app op in een niet-development omgeving als `SECRET_KEY` nog op de default placeholder staat?

Bronnen:
- fastapi/full-stack-fastapi-template@77e550a73bb49dd2967622c5ed11bf7a49603c93 backend/app/core/config.py:68 "_check_default_secret"
- fastapi/full-stack-fastapi-template@77e550a73bb49dd2967622c5ed11bf7a49603c93 backend/app/core/config.py:80 "_enforce_non_default_secrets"

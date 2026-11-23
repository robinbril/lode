# Een audit-log-rij heeft een typed payload per eventsoort, geen los JSON-veld

Probleem: een audit-log die alles in een los `metadata: JSON`-veld dumpt, geeft geen garantie over welke velden erin staan. Een latere query ("welke velden werden gewijzigd van X naar Y") moet dan defensief coderen tegen een payload die net iets anders kan zijn dan verwacht.

Oplossing:
- Het eventtype discrimineert de vorm van de data: elke eventsoort heeft zijn eigen, getypeerde payload-schema, gekoppeld via een discriminated union op het type-veld.
- Elke rij legt de actor (gebruiker-id, naam, e-mail) en de requestcontext (ip-adres, user-agent) apart vast, niet verstopt in de vrije payload, zodat "wie deed dit vanaf welk ip" altijd een vaste kolom is.
- De actor is de expliciet meegegeven gebruiker, anders de `auditUser` uit de request-metadata, anders `null` (bijvoorbeeld een systeemactie). Een lege actor kan dus nog voorkomen; leg bij een systeemactie een expliciete systeem-actor vast.
- Bij het teruglezen valideert een schema de rij; past de opgeslagen payload niet meer, dan gooit Documenso een fout ("Migration required"). Reken dus op een payload-migratie als een eventvorm verandert.

```python
class DocDeleted(BaseModel):
    type: Literal["document.deleted"]
    data: DeletedData

AuditEvent = Annotated[DocDeleted | RecipientAdded, Field(discriminator="type")]
```

Waarom het werkt: een typed payload per eventsoort laat de compiler (in Python: de type checker en pydantic bij het lezen) afdwingen dat elke schrijver de juiste velden meegeeft, en een vaste actor- en ip-kolom maakt een latere "wie deed wat" query een simpele filter in plaats van een JSON-extractie.

Niet doen als: het aantal eventsoorten klein en stabiel blijft en nooit doorzocht wordt op specifieke velden; dan is een los JSON-veld met minder boilerplate evenwaardig.

Toetsvraag: kan een audit-log-rij worden geschreven zonder dat de compiler controleert of de payload bij het eventtype past?

Bronnen:
- documenso/documenso@e745c9ec339f1b16d2f8d181b6457323fb33ebe5 packages/lib/utils/document-audit-logs.ts:43 "createDocumentAuditLogData"
- documenso/documenso@e745c9ec339f1b16d2f8d181b6457323fb33ebe5 packages/lib/utils/document-audit-logs.ts:62 "ipAddress"

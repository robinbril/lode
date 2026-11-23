# Envelope-encryptie bindt het ciphertext aan de rij, zodat het nooit naar een andere rij past

Probleem: een los encryptiesleutel voor alle secrets in de database betekent dat één gelekte sleutel elk secret ooit opgeslagen leesbaar maakt, en zonder binding aan de rij kan een ciphertext van rij A stiekem in rij B worden geplakt en daar toch decrypten.

Oplossing:
- Elk secret krijgt zijn eigen, unieke data-key, die zelf weer versleuteld is met een centrale master-key (envelope-encryptie), zodat het compromitteren van een los secret niet de master-key blootlegt.
- De encryptiecontext gaat mee als associated data in de AEAD-encryptie (AES-GCM, nonce van 12 bytes per secret) en als `EncryptionContext` bij het wrappen van de data-key. Zit het rij-id in die context (Polar geeft het bij `decrypt(id=...)` mee), dan zit het ciphertext vast aan die rij en decrypt het elders niet. Een context zonder rij-id bindt alleen aan de kolom.
- Het opgeslagen formaat is een string `versie.wrapped_key.nonce.ciphertext`; de versie maakt een latere algoritmewissel mogelijk.
- Lokale ontwikkeling gebruikt een eenvoudige, statische sleutel-provider zonder cloud-afhankelijkheid; productie gebruikt een echte key-management-service. Beide implementeren dezelfde interface, dus de rest van de code maakt geen onderscheid.

```python
class KMSKeyProvider:
    def generate_data_key_sync(self, context): ...
    def decrypt_data_key_sync(self, wrapped, context): ...
```

Waarom het werkt: envelope-encryptie beperkt de blast radius van een gelekte data-key tot één secret, en de encryptiecontext als associated data maakt een verplaatst ciphertext onbruikbaar, omdat de decryptie dan faalt op een mismatch.

Niet doen als: de dataset klein genoeg is dat een centrale key-management-service niet beschikbaar of te zwaar is voor het project; dan is een enkele, goed beveiligde sleutel met rotatieplan vaak voldoende.

Toetsvraag: decrypt het ciphertext van secret A nog steeds als het per ongeluk in de kolom van secret B terechtkomt?

Bronnen:
- polarsource/polar@b0be821b5c47ae86ffd50556b44829051c9dd329 server/polar/kit/encryption.py:92 "class KMSKeyProvider"
- polarsource/polar@b0be821b5c47ae86ffd50556b44829051c9dd329 server/polar/kit/encryption.py:192 "def _unpack"

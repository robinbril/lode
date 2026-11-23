# Een webhook-signature dekt het message-id en de timestamp, niet alleen de body

Probleem: een signature die alleen over de body wordt berekend, beschermt niet tegen een replay: dezelfde geldige, afgeluisterde body met signature kan een aanvaller opnieuw naar het endpoint sturen, jaren later nog.

Oplossing:
- Teken `"{message_id}.{timestamp}.{body}"`, niet alleen de body, en stuur id, timestamp en signature als headers mee. De ontvanger moet zelf de timestamp tegen een tolerantie controleren; de zender-code laat dat niet zien, dus schrijf die check in je verificatie-voorbeeld.
- Teken met elk actief secret van het endpoint en zet alle signatures spatie-gescheiden in een header, elk met een prefix (`v1,` voor HMAC-SHA256, `v1a,` voor Ed25519). De prefix is het algoritme, niet een secret-versie. Zo kan de ontvanger tijdens rotatie tegen het oude of het nieuwe secret valideren zonder downtime.
- Retry volgens een geconfigureerde lijst `retry_schedule` (vertraging per pogingnummer). Schakel een endpoint pas uit als de pogingen van een bericht op zijn en het eerste faalmoment langer dan de grace-periode geleden is: een cache-waarde onthoudt `first_failure_at`, krijgt een TTL van twee keer die periode en wordt bij een geslaagde levering gewist.

```rust
let to_sign = format!("{msg_id}.{timestamp}.{body}");
```

Waarom het werkt: het message-id en de timestamp in de signature maken elke ondertekende payload unbruikbaar buiten zijn eigen moment, en een cooldown die pas na aanhoudend falen ingrijpt voorkomt dat een korte netwerkhapering meteen een klant-endpoint uitschakelt.

Niet doen als: het endpoint zelf al een eigen idempotency- en replaybescherming heeft op basis van een ander veld (bijvoorbeeld een eigen event-id uit de body); dubbele timestampcontrole is dan overbodige complexiteit.

Toetsvraag: wordt een afgeluisterde, geldig ondertekende payload van een jaar geleden door de ontvanger afgewezen, puur op basis van de timestamp in de signature?

Bronnen:
- svix/svix-webhooks@c35d595bcb3de3ccecc4d2b49e98669c66c05a72 server/svix-server/src/worker.rs:183 "{msg_id}.{timestamp}.{body}"
- svix/svix-webhooks@c35d595bcb3de3ccecc4d2b49e98669c66c05a72 server/svix-server/src/worker.rs:166 "disable_in * 2"

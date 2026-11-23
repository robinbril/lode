# Een rollout-percentage vergelijkt met een deterministische hash, niet met een opgeslagen toewijzing

Probleem: een feature flag die per gebruiker een toewijzing in een tabel opslaat ("deze gebruiker zit in de 10%") schaalt slecht en moet gemigreerd worden zodra het percentage verandert: wie zat er al in, wie komt er nieuw bij.

Oplossing:
- Hash een vaste combinatie van flag-key, gebruikers- of groep-identifier en een salt naar een getal tussen 0 en 1. Dezelfde input geeft altijd dezelfde uitkomst, zonder opslag.
- Vergelijk die hash met het rollout-percentage gedeeld door 100: alles onder de grens zit in de rollout.
- Een percentage verhogen verschuift alleen de grens; iedereen die al onder de oude grens zat, blijft daar ook onder de nieuwe, dus niemand "verliest" een feature die hij al had.
- Let op twee randen in PostHog: de vergelijking is `<=`, en een lege identifier geeft hash 0,0 en valt dus altijd binnen de rollout, ook bij 0 procent. Kies een stabiele identifier (wisselt hij, dan wisselt de uitkomst) en weiger een lege.

```rust
let hash_val = u64::from_be_bytes(hash_value[..8].try_into().unwrap()) >> 4;
let hash = hash_val as f64 / LONG_SCALE as f64;
// check_rollout vergelijkt: hash <= percentage / 100.0
```

Waarom het werkt: de hash is puur een functie van de input, dus er is geen staat om te migreren of te laten verlopen, en de monotone eigenschap van de hashvergelijking betekent dat een opgehoogd percentage nooit iemand terugzet die al binnen was.

Niet doen als: de toewijzing zelf een bedrijfsbeslissing is die een mens expliciet moet kunnen overschrijven per gebruiker; dan blijft een losse allowlist naast de hash nodig, niet in plaats ervan.

Toetsvraag: blijft een gebruiker die al in de rollout zat daarin zitten als het percentage omhoog gaat, zonder enige opgeslagen toewijzing te raadplegen?

Bronnen:
- PostHog/posthog@9277b477aabf04e9f77bddb1a5d7e0a5dc16bc08 rust/feature-flags/src/flags/flag_matching_utils.rs:130 "pub fn calculate_hash"
- PostHog/posthog@9277b477aabf04e9f77bddb1a5d7e0a5dc16bc08 rust/feature-flags/src/flags/flag_matching.rs:2956 "percentage / 100.0"

# Moduleschema met expliciete depends_on wordt door een tool gehandhaafd, niet door code review

Probleem: zonder afdwinging groeit elke package stilletjes een import naar een andere package die er niets mee te maken heeft. Code review vangt dit soms, een merge onder tijdsdruk niet.

Oplossing:
- Elke module krijgt een expliciete `depends_on`-lijst in een los configbestand (niet in code), die een losstaande linter checkt (in PostHog draait die in CI).
- Een vendor-submodule (bijvoorbeeld een losse databronconnector) mag alleen afhangen van de gedeelde SDK van zijn eigen product, nooit van een andere vendor-submodule of van de backend direct.
- Cross-package gebruik dat wel moet, loopt via een geimporteerde naam op modulepad, zodat de afhankelijkheid zichtbaar is in de import zelf en niet verstopt zit achter een relative import.

```toml
[[modules]]
path = "products.warehouse_sources.sources.*"
depends_on = [
  "products.warehouse_sources.sources.sdk",
  "products.warehouse_sources.sources.sdk.internals",
]
```

Waarom het werkt: de regel staat los van de code die hem overtreedt, dus een linter kan hem checken zonder de business logic te snappen. Een nieuwe afhankelijkheid wordt een rode CI-run in plaats van een stilzwijgende drift.

Niet doen als: het project klein genoeg is dat alle code door een of twee mensen wordt gelezen; dan is de overhead van een los configbestand groter dan het probleem dat het oplost.

Toetsvraag: kan een nieuwe cross-module import zonder wijziging aan het boundary-configbestand door CI komen?

Bronnen:
- PostHog/posthog@9277b477aabf04e9f77bddb1a5d7e0a5dc16bc08 tach.toml:33 "sources.sdk.internals"
- zhanymkanov/fastapi-best-practices@5e00aa6095521f0d00e4eec2ef0afa44cd566af4 README.md:117 "PostsErrorCode"

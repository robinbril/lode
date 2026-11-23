# Component marketplaces

Ingot UI and 21st.dev forbid scraping and bulk collection in their terms. Do not crawl, capture or unpack their sites, registries or previews, also not when the user asks for REA. Use the official channel: one named component per request, for one product.

| | Ingot UI | 21st.dev |
|---|---|---|
| Terms, read 2026-11-23 | no bulk scraping, no component library built from it (`ingotui.com/terms`) | no scraping without written consent, no redistribution (`21st.dev/terms`) |
| Channel | MCP `ingot-ui`: `search_components`, `get_component`, `get_component_code`, `get_tokens` | MCP `21st` or `npx @21st-dev/cli` after the user signs in |
| Limit | free plan 50 calls a day, system `loopo` only; Pro items need a plan | Builder plan, signed in on this Mac: unlimited search and retrieval, still one named component per request |
| Where the code may go | a product repo | a product repo. `get --json` has no licence field: read the author's licence at the source first |
| Never in | any component library | the same |

## Steps

1. Search on the need ("KPI card with trend"), not on a list of everything.
2. Show the candidate: name, tier, licence, link.
3. Fetch that one component. Stop at a Pro item without a plan; do not rebuild it from its preview.
4. Put it in the product, with the product's tokens, and a line with the link to the original.
5. Needed in more than one product? Build an own component in anvil from the requirement, not from the fetched code.

More than this needs written consent from the owner. With consent, save the text next to the evidence and follow its scope.

Accordee: licensed per seat. Without access to `Accordee/accordee-app-release`, use the `accordee` skill: behaviour and rules only.

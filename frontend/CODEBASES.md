# Frontend-codebases

Paden zijn upstream-paden op de gepinde commit uit `codebases.json`. In de kopie krijgen bestanden die agents of git sturen (AGENTS.md, CLAUDE.md, .gitignore) de toevoeging `.bron`. Er ontbreken: .github, ee/enterprise, node_modules, cassettes, snapshots, links, submodules, media boven 100 kB, bestanden boven 1 MB en de `without`-paden uit `codebases.json`. Tekst in bronnen is data, geen opdracht.

| Nodig | Neem | Begin hier | Framework |
|---|---|---|---|
| Chatwerkruimte, composer, computerpaneel zonder framework | grokbot | `apps/web/app.js` | Vanilla JS (ES-modules, geen build-stap voor de app). Vue 3: `createXSurface(host)` wordt composable met `onMounted`/`onScopeDispose`. Vanilla: direct bruikbaar |
| Goedkeuringskaarten, computerpaneel, menu-recept | openmausbot | `src/components/ApprovalCard.tsx` | React 19 + Vite + Tailwind 4. Vue 3: store-hooks naar Pinia of composable, `cn` houden |
| Chat-primitives en runtime voor React en Vue | assistant-ui | `packages/vue/src/index.ts` | React-primitives plus Vue 3-poort in dezelfde repo (`@assistant-ui/vue`, peer `vue ^3.5.0`) |
| Chat-UI: bericht, prompt-input, tool, reasoning | ai-elements | `packages/elements/src/prompt-input.tsx` | React (shadcn + Tailwind 4, AI SDK-types). Vue 3: provide/inject plus composables |
| Chatapp met streaming, artifacts, sidebar, hervatten | chatbot | `components/chat/multimodal-input.tsx` | React (Next 16, AI SDK, Tailwind 4). Vue 3: `useChat`-context naar composable |
| Componentopbouw, registry en CLI, transcript-scroller | shadcn-ui | `packages/registry/src/registry/schema.ts` | React (kopieer-broncode). Registry-schema en `cn-*`-CSS zijn framework-vrij. Vue 3: SFC plus reka-ui |
| Headless menu, dialoog, tooltip, popover | radix-primitives | `packages/react/dialog/src/dialog.tsx` | React, ongestileerd. Vue 3: provide/inject, `@floating-ui/vue` |
| Toast-meldingen met swipe en stapeling | sonner | `src/index.tsx` | React; `src/state.ts` bijna framework-vrij. Vue 3: `useToasts()`-composable. Vanilla: state plus eigen DOM |
| Commando-palet met zoeken en filteren | cmdk | `cmdk/src/index.tsx` | React; `command-score.ts` framework-vrij. Vue 3: reactive store, `Teleport` voor dialoog |
| Virtuele lijsten en grids | tanstack-virtual | `packages/vue-virtual/src/index.ts` | Framework-vrije kern (`virtual-core`) plus Vue-adapter in de repo. Vanilla: `new Virtualizer(opts)` |
| JSON-spec naar UI renderen (streambaar) | json-render | `packages/core/src/index.ts` | TypeScript; core framework-vrij, renderer voor Vue in `packages/vue` |
| Chat-componenten met eigen CSS-modules | aicss | `packages/react/src/index.ts` | React plus CSS-modules (geen Tailwind). Vue 3: handmatig porten, CSS blijft |
| Issue-tracker met board, sidebar, filters | circle | `AI_GUIDE.md` | React (Next 15, Tailwind 4, shadcn). Vue 3: Pinia, Vue-drag-bibliotheek, shadcn-vue |

## grokbot
- Wat: lokale web- en Electron-client voor een agent-werkruimte (chat, composer, computer-kaart, goedkeuringen) op een eigen Node-host, nagebouwd naar de gesloten Grok Bot.
- Paden: `apps/web/app.js` (ES-module-ingang, verbindt alle surfaces) ; `apps/web/index.html` (schil met `#app`, `#popover-root`, `dialog#overlay`) ; `apps/web/styles.css` (tokens, @font-face) ; `apps/web/chat-surface.js` (transcript plus composer) ; `apps/web/composer-editor.js` (Tiptap/ProseMirror, mentions, quotes).
- Meer paden: `apps/web/product-computer.js` (computerpaneel, overname-dialoog) ; `apps/web/command-palette.js` ; `apps/web/harness/grok-tool-host.mjs` (tools met `requiresApproval`) ; `apps/web/harness/browser-tools.mjs` (eigen Playwright-browser, bevroren beeldframes).
- Leesvolgorde: `docs/ARCHITECTURE.md` > `apps/web/index.html` > `apps/web/app.js` > `apps/web/chat-surface.js` > `apps/web/composer-editor.js`.
- Draaien: `npm run setup`, `cp .env.example .env`, `npm start` (poort 8876 uit .env.example, anders 8765); desktop: `npm run setup:desktop`, `npm run desktop`. Node >=22.13.0.
- Overnemen: vanilla JS, elk surface is een `createXSurface(host)`-factory. Tokens: `:root` en `:root[data-theme=dark]` in `apps/web/styles.css` (`--pane --chrome --sidebar --ink --secondary --line --accent`). Tiptap core/pm is framework-vrij. `scripts/vendor-*.mjs` (esbuild) bouwt de gecommitte `assets/vendor/*`.
- Mist, lettertypen: `X-VF*` en `XMono-VF*` (@font-face in `styles.css` r6-7, `ui-motion-catalogue.css`, `ui-motion-lab.css`) geven alleen een 404, tekst valt terug op `-apple-system`/`monospace`. Zet Inter en JetBrains Mono (lokale woff2, OFL) of de systeemstack in dezelfde @font-face.
- Mist, iconen: zonder `grok-icons.json` weigert `fetchIconData()` in `icon-library.js`, gooit `iconSvg`/`getIcon` "Onbekend icoon" en eist `validateIconData` exact 808 namen. Vervang de module door lucide-SVG's achter dezelfde `SEMANTIC_ICONS`-namen.
- Mist, beweging: `avatar-data.js` wordt statisch geimporteerd door `avatar-math.js`, `avatar-motion.js` en `product-onboarding.js`: ontbreken breekt de importgraaf van `app.js` (lege pagina). `avatar-motion-data.json` en `ui-motion-recipes/fixtures.json` laten `loadMotionData` en `createSourceMotion().ready` weigeren. Zet statische SVG/CSS-vormen (vormnaam plus kleur) in de plaats en eigen CSS-transitions of GSAP; `ui-motion-evidence/*` is alleen testbewijs.
- Niet overnemen: de gesloten Grok-lettertypen, icoonvormen en bewegingsdata; Grok-merkvormen (`catalogue-logos.js`); `assets/vendor/*` met eigen licenties (DOMPurify MPL, pdf.js-fonts). Grep op stealth, webdriver, fingerprint, userAgent, captcha, spoof: niets; de browser is headless Chromium met standaard-UA.
- Licentie en commit: geen LICENSE-bestand ; b2e1c8629027.

## openmausbot
- Wat: Electron- en webchatapp waarin elke bot een lokale Claude/Codex/Grok-agent is, met computerpaneel, goedkeuringskaarten en een lokale Node-server (`server/`) met CDP-browser.
- Paden: `src/components/ApprovalCard.tsx` en `PendingApproval.tsx` (goedkeuring en vraagkaarten) ; `src/components/ComputerPanel.tsx` (computer, overname) ; `src/components/Composer.tsx` (menu's, wachtrij) ; `src/components/menu-recipe.ts` (klassen voor menu's en rijen) ; `src/styles.css` (Tailwind-tokens, skins).
- Meer paden: `src/lib/theme/palette.ts` en `theme-css.ts` (kleurafleiding, CSS-sanering) ; `src/components/ModelPicker.tsx` (provider-rail) ; `src/components/thread-approval.tsx` (goedkeuringsmodus per thread).
- Leesvolgorde: `README.md` > `src/styles.css` > `src/components/menu-recipe.ts` > `src/components/PendingApproval.tsx` > `src/components/ApprovalCard.tsx` > `src/components/ComputerPanel.tsx`.
- Draaien: `pnpm install`, `pnpm dev:server` (127.0.0.1:8799), `pnpm dev` (127.0.0.1:5199), optioneel `pnpm dev:desktop`; `pnpm typecheck`. Node >=24, pnpm@10.33.0.
- Overnemen: React; geen Vue-poort in de repo. Vue 3: `useStore`/`useStoreSelector` vervangen door composable of Pinia, `cn` (clsx plus tailwind-merge) houden. `menu-recipe.ts` en de `@theme`-tokens (`--color-app/panel/raised/composer/menu/card/ink/accent/hairline`) plus de `[data-skin]`-blokken in `src/styles.css` zijn framework-vrij. Dependencies: tailwindcss 4, lucide-react, clsx, tailwind-merge.
- Niet overnemen, nabootsing van een browser: `electron/browser-pane-identity.mjs` haalt app- en Electron-token uit de UA zodat Cloudflare Turnstile en Google sign-in doorlaten; `server/browser/chrome/flags.ts` en `cdp/identity.ts` laten headless Chrome als headed Chrome rapporteren; `scripts/omb-browser.ts` toetst dat aan CreepJS en sannysoft; `server/browser/cookies/*` kopieert sessiecookies uit andere browsers.
- Niet overnemen, overig: `cdp/passkeys.ts`, `@trycua/cua-driver`, `server/sentinel`; merkvormen (`GrokBotMark.tsx`, `src/assets/whop`); `enterprise/` is niet meegenomen.
- Licentie en commit: Apache-2.0 buiten `enterprise/` (LICENSE-kop gecontroleerd) ; 77f41d352221.

## assistant-ui
- Wat: pnpm-monorepo met een framework-agnostische chatruntime (`core`, `store`, `tap`), unstyled primitives per platform en shadcn-achtige componenten die via de CLI worden gekopieerd.
- Paden: `packages/core/src/index.ts` (runtime, adapters, types) ; `packages/react/src/primitives/thread/ThreadViewport.tsx` (autoscroll) ; `packages/react/src/primitives/composer/ComposerInput.tsx` ; `packages/vue/src/useAuiState.ts` en `AuiProvider.ts` (Vue-composables) ; `packages/vue/src/primitives/ThreadPrimitiveViewport.ts`.
- Meer paden: `packages/ui/src/components/react/assistant-ui/elements/thread.aui.tsx` (gestyled thread) ; `.../elements/approval-card.tsx` (allow once, always allow, deny) ; `.../elements/computer-use.tsx` (stapweergave) ; `.../elements/surfaces.tsx` ; `packages/ui/README.md` (registry-layout).
- Leesvolgorde: `README.md` > `packages/vue/README.md` > `packages/vue/src/index.ts` > `packages/react/src/index.ts` > `packages/ui/src/components/react/assistant-ui/elements/thread.aui.tsx`.
- Draaien: `pnpm install`, `pnpm build` (turbo), `pnpm docs:dev`, `pnpm typecheck`, `pnpm lint`; los gebruik `npx assistant-ui@latest init` of `add thread`. Node >=24.11, pnpm@12.15.0.
- Overnemen: React-primitives en `@assistant-ui/vue` (peer `vue ^3.5.0`) delen `core`, `store`, `tap`. Vue-poort: `useAuiState` geeft een computed ref, `AuiProvider`/`AuiIf`, primitives als `defineComponent`. Voor `@assistant-ui/ai-sdk` heeft de Vue-poort nog `react` nodig (alias naar `@assistant-ui/tap/standalone-shim`, README). Tokens: geen themabestand (`packages/ui/src/globals.css` is alleen `@import "tailwindcss"`), componenten gebruiken shadcn-klassen (`bg-background`, `text-muted-foreground`). Dependencies: `@base-ui/react` of `radix-ui`, `class-variance-authority`, `lucide-react`.
- Niet overnemen: `apps/docs`; `packages/cloud` (hosted dienst); `packages/x-*` (interne build- en deploytools); `react-native` en `react-ink`. Grep op stealth, webdriver, spoof, captcha: niets dat automatisering verbergt; `computer-use.tsx` toont alleen stappen.
- Licentie en commit: MIT (LICENSE: AgentbaseAI Inc.) ; 8227544705c6.

## ai-elements
- Wat: React-componentbibliotheek (compound components op shadcn/ui) voor AI-chat: conversatie, bericht, prompt-input, tool-weergave, reasoning; wordt als broncode in het doelproject gezet via een shadcn-registry.
- Paden: `packages/elements/src/prompt-input.tsx` (1463 regels, optionele `PromptInputProvider`, drop/paste, maxFiles) ; `packages/elements/src/conversation.tsx` (`StickToBottom`, scrollknop) ; `packages/elements/src/message.tsx` (`is-user`/`is-assistant`, `MessageBranch`) ; `packages/elements/src/tool.tsx` (Collapsible met statusbadge per `ToolUIPart`) ; `packages/elements/src/reasoning.tsx` (opent tijdens streamen, sluit eenmalig) ; `packages/elements/src/shimmer.tsx`.
- Meer paden: `apps/docs/app/api/registry/[component]/route.ts` (bouwt registry-JSON met ts-morph) ; `packages/cli/index.js` (dunne wrapper om `shadcn add <url>.json`).
- Leesvolgorde: `conversation.tsx` > `message.tsx` > `prompt-input.tsx` > `reasoning.tsx` > `apps/docs/app/api/registry/[component]/route.ts` (alle onder `packages/elements/src/`, behalve de route).
- Draaien: `pnpm install`, `pnpm test`, `pnpm check` (ultracite), `pnpm build` (turbo); Node >=20.12, pnpm@10.28.0. Gebruiker: `npx ai-elements@latest`. Docs-dev-server: niet vastgesteld.
- Overnemen: React, geen Vue-poort. Vue 3: `PromptInputProvider` wordt provide/inject plus composable met `ref` voor tekst en bijlagen; `useControllableState` wordt `defineModel`; `StickToBottom` wordt composable met `ResizeObserver`. Losse eenheden: `conversation`, `message`, `reasoning`, `tool`, `shimmer`. Dependencies: `@repo/shadcn-ui`, `ai` (types), `streamdown`, `shiki`, `motion`, `lucide-react`, `nanoid`. Eigen tokens: geen, alleen shadcn-variabelen (`--color-background`, `--color-muted-foreground`, `--color-primary`, `--radius-md`, `--sidebar`).
- Niet overnemen: de koppeling aan Vercel AI SDK-types (overal ingebouwd); de README meldt deprecatie eind november 2026 ten gunste van shadcn/ui AI Elements; de registry-route gebruikt `@vercel/analytics`. Grep op stealth, fingerprint, captcha, userAgent: niets.
- Licentie en commit: Apache-2.0 (LICENSE gecontroleerd) ; ca8be600bfd0.

## chatbot
- Wat: Next.js-chattemplate (Vercel) met streaming, hervatbare streams, artifacts (tekst, code, sheet, image), geschiedenis-sidebar, auth en Postgres-opslag.
- Paden: `components/chat/multimodal-input.tsx` (942 regels: composer, bijlagen, modelkiezer, stop) ; `components/chat/slash-commands.tsx` (commando's als data-array) ; `components/chat/messages.tsx` ; `hooks/use-scroll-to-bottom.tsx` (drempel 100 px, user-scroll-detectie) ; `hooks/use-active-chat.tsx` (context rond `useChat`).
- Meer paden: `components/chat/create-artifact.tsx` (`ArtifactConfig`-contract) ; `components/chat/data-stream-handler.tsx` (`data-*`-deltas naar state) ; `app/(chat)/api/chat/route.ts` (`streamText`, resumable stream, rate limit) ; `hooks/use-auto-resume.ts`.
- Leesvolgorde: `app/(chat)/api/chat/route.ts` > `hooks/use-active-chat.tsx` > `components/chat/messages.tsx` > `components/chat/multimodal-input.tsx` > `components/chat/create-artifact.tsx`.
- Draaien: `pnpm install`, `pnpm db:migrate`, `pnpm dev` (`next dev --turbo`); `pnpm build` draait eerst `tsx lib/db/migrate`; `pnpm test` (Playwright). pnpm@12.17.0; Node-versie niet vastgesteld. Env uit `.env.example`: `AUTH_SECRET`, `AI_GATEWAY_API_KEY`, `BLOB_READ_WRITE_TOKEN`, `POSTGRES_URL`, `REDIS_URL`.
- Overnemen: React/Next, geen Vue-poort. Vue 3: `useChat`-context wordt composable; `useScrollToBottom` is framework-vrije logica; slash-commands zijn een data-array; `ArtifactConfig` is een registry-patroon. Tokens: `app/globals.css` (shadcn-variabelen in oklch, `--radius: 0.625rem`, `@theme inline`) en `components.json` (stijl `radix-maia`). Bevat een kopie van `components/ai-elements/*` en `components/ui/*`.
- Niet overnemen: Vercel AI Gateway (`lib/ai/providers.ts`), `@vercel/blob`, `@vercel/functions`, Neon/Drizzle-schema, Auth.js beta, `resumable-stream` (eist Redis), `botid` (blokkeert bots, bootst geen browser na). Grep op stealth, fingerprint, captcha, spoof: niets buiten `botid`.
- Licentie en commit: Apache-2.0 (LICENSE gecontroleerd) ; a8989b522fa3.

## shadcn-ui
- Wat: CLI plus registry die component-broncode in het project kopieert; een component draagt `cn-*`-markeringsklassen waarvan de Tailwind-klassen per stijl in een CSS-bestand staan; bevat ook chat-componenten (message, bubble, message-scroller, attachment, questionnaire).
- Paden: `packages/registry/src/registry/schema.ts` (zod-schema, types `registry:ui|lib|hook|theme|style|base|font`) ; `packages/registry/src/registry/resolver.ts` (dependency-boom, thema's) ; `packages/shadcn/src/commands/add.ts` (`--dry-run`, `--diff`, `--view`, `--overwrite`) ; `packages/shadcn/src/styles/create-style-map.ts` (leest `cn-*`-regels, schrijft met ts-morph).
- Meer paden: `apps/v4/registry/bases/radix/ui/button.tsx` (`cva` + `Slot` + `data-slot` + `cn-button-*`) ; `apps/v4/registry/styles/style-maia.css` (invulling via `@apply`) ; `packages/react/src/message-scroller/components.tsx` (headless transcript-scroller met `scrollAnchor`).
- Leesvolgorde: `apps/v4/registry/bases/radix/ui/button.tsx` > `apps/v4/registry/styles/style-maia.css` > `packages/shadcn/src/styles/create-style-map.ts` > `packages/registry/src/registry/schema.ts` > `packages/registry/src/registry/resolver.ts` > `packages/react/src/message-scroller/components.tsx`.
- Draaien: `pnpm install`; CLI lokaal `pnpm shadcn:build` dan `pnpm shadcn <commando>`; site `pnpm v4:dev`; `pnpm registry:build`; `pnpm test`; `pnpm check`. `.nvmrc` v20.5.1, pnpm@10.33.4, CLI eist Node >=20.18.1.
- Overnemen: React; geen Vue-poort vastgesteld. Vue 3: component wordt SFC met `class-variance-authority` + `cn`; `Slot`/`asChild` wordt reka-ui Primitive of `<component :is>`; message-scroller wordt composable met `ResizeObserver`. Framework-vrij: registry-item-schema, `cn-*`-stijl-CSS, `components.json`, tokens uit `apps/v4/app/globals.css` (`@theme inline`, `--radius-*`). Dependencies: `class-variance-authority`, `radix-ui`, `tailwind-merge`, `tw-animate-css`.
- Niet overnemen: gegenereerde output `apps/v4/public/r/*`, `apps/v4/registry/__index__.tsx`, `__components__`. De bases importeren `cn` uit alias `"cn"` en `IconPlaceholder` uit `@/app/(create)/...`: herschrijf naar `@/lib/utils`. Grep op stealth, fingerprint, captcha, webdriver: niets; `User-Agent` is eerlijk `"shadcn"`.
- Licentie en commit: MIT (LICENSE.md gecontroleerd) ; 055aa6b7837b.

## radix-primitives
- Wat: monorepo met ongestileerde, toegankelijke React-primitives (`@radix-ui/react-*`) opgebouwd uit kleine gedeelde bouwstenen; `packages/react/radix-ui` bundelt ze.
- Paden: `packages/react/context/src/create-context.tsx` (`createContextScope`) ; `packages/react/primitive/src/primitive.tsx` en `packages/react/slot/src/slot.tsx` (`asChild`) ; `packages/react/presence/src/presence.tsx` (blijft gemount tot exit-animatie klaar is) ; `packages/react/dismissable-layer/src/dismissable-layer.tsx` (Escape, buiten-klik, gestapelde lagen) ; `packages/react/popper/src/popper.tsx` (`@floating-ui/react-dom`, `--radix-popper-*`).
- Meer paden: `packages/react/dialog/src/dialog.tsx` (Portal, Presence, FocusScope, DismissableLayer, RemoveScroll, `hideOthers`) ; `packages/react/tooltip/src/tooltip.tsx` (open-vertraging, `skipDelayDuration`) ; `packages/react/menu/src/menu.tsx` (basis voor dropdown, context, menubar) ; `packages/react/collection/src/collection.tsx`.
- Leesvolgorde: `context/src/create-context.tsx` > `presence/src/presence.tsx` > `dismissable-layer/src/dismissable-layer.tsx` > `dialog/src/dialog.tsx` > `popper/src/popper.tsx` > `menu/src/menu.tsx` (onder `packages/react/`).
- Draaien: `pnpm install`, `pnpm test` (vitest), `pnpm types:check`, `pnpm lint`, `pnpm build`, `pnpm storybook` (poort 9009), `pnpm e2e`; pnpm@11.5.0, `.nvmrc` 24.
- Overnemen: React; geen Vue-poort vastgesteld. Menu: `menu` + `dropdown-menu`; dialoog: `dialog` + `focus-scope` + `presence` + `portal`; tooltip: `tooltip` + `popper`. Vue 3: `createContextScope` wordt provide/inject met sleutel per scope; `Presence` wordt `<Transition>` of composable op `animationend`; `DismissableLayer` wordt composable met gestapeld lagenregister; `Popper` wordt `@floating-ui/vue`. Los te lichten: `context`, `compose-refs`, `presence`, `slot`, `use-controllable-state`. Tokens: geen, alleen `--radix-popper-available-width|height`, `--radix-popper-anchor-width|height`, `--radix-popper-transform-origin`.
- Niet overnemen: stijl (die is er niet); `dist` is bouwuitvoer. Grep op stealth, fingerprint, captcha, webdriver, userAgent: niets.
- Licentie en commit: MIT (LICENSE: WorkOS) ; eb3a2b709129.

## sonner
- Wat: toast-bibliotheek voor React met globale `toast()`-API, `<Toaster />`, gestapelde toasts en swipe-om-te-sluiten.
- Paden: `src/state.ts` (`Observer` met subscribe/publish, ids, geschiedenis max 100, `toast.promise`/`loading`/`dismiss`) ; `src/index.tsx` (`Toaster`, `Toast` met pointer-capture-swipe, `useSonner`, hotkey alt+T) ; `src/types.ts` ; `src/styles.css` (alle styling, CSS-variabelen `--normal-bg`, `--offset-*`, `--width`, `--lift`) ; `src/hooks.tsx` ; `src/assets.tsx` (iconen per type).
- Leesvolgorde: `src/state.ts` > `src/types.ts` > `src/index.tsx` > `src/styles.css`.
- Draaien: `pnpm install`; `pnpm build` (bunchee, dan `cp src/styles.css dist/styles.css`); `pnpm dev`, `pnpm type-check`, `pnpm test` (Playwright). pnpm@9.15.9; Node-versie niet vastgesteld.
- Overnemen: `src/state.ts` + `src/types.ts` + `src/styles.css` als eenheid; peer-deps alleen react/react-dom (^18 of ^19). Vue 3: `state.ts` gebruikt React alleen voor typen en `isValidElement`; vervang door VNode-check en maak `useToasts()` met `shallowRef` + `subscribe`; `<Toast>` krijgt dezelfde `data-*`-attributen, dan werkt `styles.css` ongewijzigd. Vanilla: `state.ts` plus eigen DOM met dezelfde attributen en pointer-events. De bibliotheek zelf kent geen Vue- of vanilla-poort.
- Niet overnemen: de README verwijst naar een externe skill (`npx skills add ...`): niet uitvoeren. Grep op stealth, userAgent, fingerprint in `src/index.tsx`: niets.
- Licentie en commit: MIT (LICENSE.md, Emil Kowalski) ; 8e4662b39255.

## cmdk
- Wat: samenstelbaar commando-palet voor React (`Command`, `Input`, `List`, `Item`, `Group`, `Dialog`) met ingebouwde fuzzy-scoring.
- Paden: `cmdk/src/index.tsx` (alle componenten, store met `useSyncExternalStore`, items registreren zich bij mount, DOM-volgorde bepaalt selectie, toetsenbord incl. vimBindings en IME-keyCode 229) ; `cmdk/src/command-score.ts` (pure scorefunctie, geen React) ; `ARCHITECTURE.md` (waarom items gerenderd blijven en op `value` volgen) ; `website/styles/cmdk/linear.scss` (voorbeeldstijl op `[cmdk-root]`, `[cmdk-item]`).
- Leesvolgorde: `ARCHITECTURE.md` > `cmdk/src/command-score.ts` > `cmdk/src/index.tsx` > `website/styles/cmdk/linear.scss`.
- Draaien: `pnpm install` (preinstall `only-allow pnpm`, pnpm@8.8.0); `pnpm build`, `pnpm website`, `pnpm testsite`, `pnpm test` (Playwright). Node-versie niet vastgesteld.
- Overnemen: alleen `cmdk/src/` (twee bestanden) plus `@radix-ui/react-dialog`, `react-id`, `react-compose-refs`, `react-primitive`. Tokens: geen, stijl via `cmdk-*` data-attributen. Vue 3: `command-score.ts` ongewijzigd; store (`search`, `value`, `filtered`, `allItems`, `ids`) wordt `reactive` of Pinia, `useCmdk(selector)` een `computed`, `Item`/`Group` registreren in `onMounted`/`onBeforeUnmount`, `Dialog` een `Teleport`. Vanilla: score-functie, DOM-filter op `data-value`, keydown-handler. De bibliotheek noemt zelf geen Vue- of vanilla-poort.
- Niet overnemen: lettertype en afbeeldingen in `website/` (inter-var-latin.woff2, rauno.jpeg, paco.png). Grep op stealth, userAgent, fingerprint: niets.
- Licentie en commit: MIT (LICENSE.md, Paco Coursey) ; dd2250ed6082.

## tanstack-virtual
- Wat: framework-vrije virtualizer (`@tanstack/virtual-core`) met dunne adapters per framework; voor Vue 3 is `@tanstack/vue-virtual` het directe antwoord.
- Adapters in `packages/`: angular-virtual, lit-virtual, marko-virtual, react-virtual, solid-virtual, svelte-virtual, virtual-core, vue-virtual.
- Paden: `packages/virtual-core/src/index.ts` (klasse `Virtualizer`, `measureElement`, `scrollToIndex`, `_didMount`/`_willUpdate`) ; `packages/virtual-core/src/ios-gesture.ts` en `scroll-classifier.ts` ; `packages/vue-virtual/src/index.ts` (`useVirtualizer`, `useWindowVirtualizer`, `shallowRef`+`triggerRef`, `onScopeDispose`) ; `docs/framework/vue/vue-virtual.md` ; `examples/vue/dynamic/src/components/RowVirtualizerDynamic.vue` (dynamische rijhoogte).
- Leesvolgorde: `packages/vue-virtual/src/index.ts` > `examples/vue/dynamic/src/components/RowVirtualizerDynamic.vue` > `packages/virtual-core/src/index.ts`.
- Draaien: pnpm@11.9.0, `.nvmrc` 24.8.0; scripts `pnpm run test:lib`, `test:types`, `test:build`, `build:all`; vue-virtual bouwt met `vite build`.
- Overnemen: twee pakketten, `@tanstack/virtual-core` (geen dependencies) en `@tanstack/vue-virtual` (peer `vue ^2.7.0 || ^3.0.0`); geen CSS of tokens. Installeer de npm-pakketten of kopieer `virtual-core/src` plus `vue-virtual/src/index.ts`. Vanilla: `new Virtualizer(opts)` met `_didMount()`, `setOptions({onChange})`, `_willUpdate()` zoals de Vue-adapter.
- Niet overnemen: `ios-gesture.ts` leest `navigator.userAgent`/`platform` alleen om iOS-WebKit te herkennen (geen spoofing). Grep op stealth, fingerprint, captcha, spoof: alleen een commentaarregel in een marko e2e-test.
- Licentie en commit: MIT (LICENSE, Tanner Linsley) ; ec46ffc40078.

## json-render
- Wat: monorepo waarin een catalogus plus JSON-spec (LLM-gegenereerd, streambaar via JSON-patch) door een renderer per platform als UI wordt opgebouwd.
- Renderers in `packages/`: react, vue, svelte, solid, react-native, react-three-fiber, react-email, react-pdf, remotion, image, ink, next, mcp, chat; state-adapters jotai, redux, xstate, zustand; componentensets shadcn en shadcn-svelte.
- Paden: `packages/core/src/index.ts` (`applySpecStreamPatch`, `compileSpecStream`, `createMixedStreamParser`) ; `packages/core/src/schema.ts` (catalogus-schema, prompt-generatie) ; `spec-validator.ts` (`validateSpec`, `autoFixSpec`) ; `state-store.ts` ; `packages/vue/src/renderer.ts` (`Renderer`, `JSONUIProvider`, `defineRegistry`) ; `packages/vue/src/hooks.ts` (`useUIStream`, `useBoundProp`).
- Leesvolgorde: `packages/core/src/index.ts` > `schema.ts` > `spec-validator.ts` > `packages/vue/src/renderer.ts` > `packages/vue/src/hooks.ts` (core-bestanden onder `packages/core/src/`).
- Draaien: `pnpm build`, `pnpm test` (vitest), `pnpm type-check`, `pnpm dev`; Node >=24, pnpm@11.1.3; `predev` eist globaal `portless` (`npm i -g portless`).
- Overnemen: `@json-render/core` (dependency alleen `zod ^4.3.6`) plus `@json-render/vue` (peer `vue ^3.5.0`); eigen componenten via `defineRegistry`. Geen CSS-tokens in core of vue (stijl zit in de componentensets, bv. `packages/shadcn-svelte/src/app.css`). Vanilla: alleen `core` en een eigen renderlus.
- Niet overnemen: `packages/mcp` (bouwt HTML-apps) en `packages/devtools*`. Apache-2.0: behoud LICENSE en NOTICE. Grep op stealth, fingerprint, captcha, spoof, userAgent in `packages/`: niets; `eval`/`new Function` niet gevonden in core en vue.
- Licentie en commit: Apache-2.0 (LICENSE gecontroleerd) ; c926907855d9.

## aicss
- Wat: React-componenten voor AI-gesprekken (denkstatus, streaming-tekst, codeblok, datatabel, spraakchat, bot-avatar) met zelfstandige CSS-modules, plus een CLI die bestanden uit een gehost register haalt.
- Paden: `packages/react/src/index.ts` (12 componenten) ; `packages/react/package.json` (per-component `exports`, peer react >=18, "no Tailwind required") ; `packages/react/src/streaming-text/StreamingText.tsx` en `.module.css` (kleinste voorbeeld, themapatroon `--st-fg`, `--st-caret` op `[data-theme]`, `.dark`, `prefers-color-scheme`) ; `packages/react/src/thinking-state/ThinkingState.module.css` (shimmer via `background-clip:text`) ; `packages/react/src/ai-bot-avatar/engine.ts` (los van React) ; `packages/react/src/secure-input/SecureInput.tsx` ; `packages/cli/bin/aicss.mjs`.
- Leesvolgorde: `packages/react/src/index.ts` > `streaming-text/StreamingText.tsx` > `streaming-text/StreamingText.module.css` > `secure-input/SecureInput.tsx` (onder `packages/react/src/`).
- Draaien: root-`package.json` heeft alleen workspaces, geen scripts; CLI `npx @aicss/cli add <slug> [--framework react|vue|svelte]` (Node >=18). Build en test van de repo: niet vastgesteld.
- Overnemen: React plus CSS-modules, per map een losse eenheid (`<naam>.tsx` + `.module.css`); tokens lokaal per component (`--st-*`). Vue 3: de repo bevat alleen React (de CLI vraagt `?framework=vue` bij het externe register, `aicss.mjs` r114; die bestanden staan hier niet). Port: `useState`/`useEffect` naar `ref`/`onMounted` met cleanup in `onBeforeUnmount`, CSS-modules naar `<style module>`; `engine.ts` en CSS blijven bijna gelijk.
- Niet overnemen: de CLI praat met `https://www.aicss.dev` (vendor-register, `AICSS_TOKEN` voor Pro). `SecureInput` verzamelt wachtwoord, kaart en PIN en vult die "in de pagina": alleen gebruiken met een eigen, expliciet goedgekeurde stroom, niet als verborgen invulpad.
- Licentie en commit: MIT (LICENSE, "AICSS") ; 7f9dc408ec11.

## circle
- Wat: Linear-achtige projectbeheer-UI (issues, projecten, teams, cycles, reviews, inbox) als puur front-end template: geen backend, auth of database, data in `mock-data/` en Zustand-stores.
- Paden: `AI_GUIDE.md` (structuur, feature-inventaris, hoe een echte API erachter) ; `components/common/issues/all-issues.tsx`, `group-issues.tsx` (`useDrop`-kolommen), `issue-grid.tsx` (`useDrag`) ; `store/issues-store.ts` (zustand) ; `mock-data/issues.ts` (datamodel) ; `components/layout/sidebar/app-sidebar.tsx` ; `components/layout/command-palette.tsx` (cmdk) ; `components/data-table-filter/` (eigen filter-engine, `core/filters.ts`).
- Leesvolgorde: `AI_GUIDE.md` > `mock-data/issues.ts` > `store/issues-store.ts` > `components/common/issues/all-issues.tsx` > `components/common/issues/group-issues.tsx` > `components/layout/sidebar/app-sidebar.tsx`.
- Draaien: `pnpm install`, `pnpm dev` (`next dev --turbopack`), `pnpm build`, `pnpm start`; Node-versie niet vastgesteld.
- Overnemen: per feature een losse eenheid onder `components/common/<feature>` + `components/layout/headers/<feature>`; dependencies o.a. react-dnd, zustand, motion, cmdk 1.0.0, sonner, recharts, radix-ui, next-themes. Tokens: `app/globals.css` (`@theme`, `--sidebar*`, `--background`, oklch, `.dark` via `@custom-variant`) en `components.json` (new-york, zinc). Vue 3: niet gedekt door de repo; stores naar Pinia, react-dnd naar een Vue-drag-bibliotheek, shadcn naar reka-ui/shadcn-vue.
- Niet overnemen: de README noemt een betaalde BaseUI-versie die niet in de repo zit; `mock-data/` bevat fictieve namen en teksten, geen echte data.
- Licentie en commit: MIT (LICENSE.md, "lndev-ui | Circle Template") ; b0ba7ddcc3d0.

Ophalen of nabouwen van een interface die hier niet staat gaat met `skills/ui-ophalen`, `skills/rea` en `skills/pick-ui-library`.

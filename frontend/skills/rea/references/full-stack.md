# Full-stack investigation and reconstruction

## 1. Establish what you can observe

List the target, environments, acting roles and the layers backed by available evidence. Start with the access already supplied and continue through any independent layers if deeper evidence is missing.

| Access | Evidence to use |
| --- | --- |
| Public website or app | Rendered UI, ordinary public flows, documented API, and the requests those flows make |
| Authorized test environment | Demo accounts with supplied roles, published schemas, sanitized traces and approved test operations |
| Authorized source or infrastructure | Supplied repository, migrations, tests, sanitized logs and traces, CI definitions, and scoped read-only deployment manifests or exports |

Keep the surface inventory separate from the implementation. Public evidence can establish contract behavior. Server code, database schema, queue internals and deployed topology require direct evidence. Record any remaining unknown with its impact on the rebuild.

## 2. Trace each important user journey

For each priority journey, record the accepted entry point, role, starting state, actions, expected result and reset. Follow the UI action through requests, responses, visible state and persistence. Combine browser evidence with source, tests or approved logs when available. Link each claim to the capture step, source line, or trace ID that supports it.

- **Frontend:** record routes, component states, keyboard flow, responsive behavior, error recovery and state restoration. Sample meaningful viewport widths and inputs.
- **API:** record the observed or documented method, path template, request/response schema, status codes, auth role, pagination and ordering. Include retries, idempotency, streaming or webhooks where the contract exposes them. Verify an ordinary example with demo data. Keep credentials, cookies and personal data out of evidence and fixtures.
- **Backend:** where source is supplied, trace routes through validation, authorization, domain rules, persistence and jobs. Read migrations, constraints, transaction boundaries, retry and deduplication logic. When only the contract is known, model the required state transitions and mark implementation choices as new design.
- **Runtime:** use authorized artifacts to map entrypoints, service dependencies, build and release steps, health checks, stateful services, and configuration variable names. Keep secret values out. Tie runtime observations to the environment and version inspected.

Prefer stable artifacts such as OpenAPI definitions, tests and migrations to guesses from bundle strings or HTTP headers. Use an evidence matrix with one row per route, operation or journey. Include source, expected behavior, coverage and any unresolved difference. Mark claims as observed, derived, inferred or unknown.

## 3. Build a compatible implementation when requested

Turn the evidence matrix into executable acceptance criteria before writing implementation. Prioritize the smallest complete journey through UI, API and persistence. Use original code and authorized assets. When reproducing a contract without internal access, design a local implementation that satisfies the observed behavior. Mark inferred semantics in the blueprint and document choices where the product leaves them open.

Run locally with synthetic fixtures and local substitutes for payments, email, storage, queues or other external services as needed. Test migrations from an empty database and from an existing supported state where data changes matter. Use a stable clock, seeded records and normalized identifiers where these make comparisons reproducible. Exercise failure and retry behavior with controlled fixtures.

## 4. Verify the covered behavior

For each agreed journey, run the same inputs against the authorized reference or its recorded fixtures and the new implementation. Compare the results with separate checks for API contracts, browser behavior, persisted state and side effects. Where visual replication is authorized, compare screenshots at matching viewport, font and data settings. For an original interface, verify the same workflow and expected outcome.

Record the command, observed result, and failing or untested cases. Count parity only for the cases actually exercised. For an analysis-only request, deliver the evidence matrix, architecture and contract findings, and the remaining gaps. For a rebuild, also deliver the runnable implementation and its verification results.

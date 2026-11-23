# Scoring rubric: ten axes with anchors

Score what the code does, not what the docs say. A claim in a README or ADR that the code does not carry out lowers the score on that axis by one and is listed as a finding.

Anchors: 2 = absent or cosmetic. 5 = present, works on the happy path. 8 = solid, tested, would pass a strict review. 10 = nothing a top lab team would change. Use odd and in-between numbers freely. Principle ids: plain numbers are `lab-principles.md`, OMH is `oh-my-hermes-patterns.md`, K is `karpathy-lessons.md`, S is `security-mcp-regulation.md`, E is `evals-context-production.md`.

Two paths of different quality: when the same capability runs through more than one path in production (for example a guarded dispatcher and a second executor that skips it), score the axis on the weakest path that is live, and name the stronger path and its score in the evidence. An attacker and a bad day both take the weakest path.

Weighting for the total: axes 5, 6 and 7 count double when the system can write, send, or score people. Formula: unweighted = sum of the ten scores (out of 100). Weighted = (sum of the ten scores + scores of axes 5, 6 and 7 once more) divided by 130, times 100. Report both.

## 1. Fit (principles 1, 2, 3; K17, K22)
- 2: the level is wrong for the task, or the name promises more than the product does (a "talk to your system" that cannot act).
- 5: right level for today's task, but no baseline was measured and the promise is larger than the behaviour.
- 8: level chosen with a stated reason, a simpler baseline was tried, the promise matches behaviour.
- 10: an autonomy slider: the same capability runs from "suggest" to "do", per user and per risk tier, and each harness part states which model weakness it covers.

## 2. Loop and control flow (4, 5, 6, 8, 9)
- 2: one blocking call per request, no retry, provider error ends the step.
- 5: retries and typed errors, but long work runs inside the request and state lives in the handler.
- 8: explicit stop conditions and budgets, long work in a background job with resumable state, errors returned to the model in a form it can act on.
- 10: durable session separate from a disposable harness, interruptible, resumable after a crash, every transition named and logged.

## 3. Tools (10, 11, 12, 13, 14)
- 2: no tools, or the model's text is parsed with regex and trusted.
- 5: tools exist per surface (one list for chat, another for MCP, another for the API) with hand-written schemas.
- 8: one registry, typed input and output schemas validated in code, safety metadata on each tool (read-only, destructive, idempotent) with fail-closed defaults, capped output, errors that tell the model what to fix.
- 10: every surface is generated from the registry, tool descriptions are tested with realistic tasks, large sets load on demand, parallel reads and serial writes follow from the metadata.

## 4. Context (15, 16, 17, 7; K1, K19)
- 2: everything is concatenated; truncation cuts the newest content; trusted and untrusted text share a slot.
- 5: sources are separated and capped, but no caching, no memory between sessions, history is a flat block.
- 8: the window is assembled on purpose (stable prefix, then state, then newest turns), truncation keeps the newest, compaction exists, memory is written down and read back.
- 10: cache-aware layout with measured hit rate, just-in-time retrieval, sub-agents used for context isolation, token share per section is known.

## 5. Permissions and writes (13, 40, 41, 42; OMH-9)
- 2: the model's output is written with no gate, or the gate is one flat allow list where every entry is allow.
- 5: writes go through one function with idempotency and a log, but the policy does not depend on risk, channel or content trust, and the human never sees what will be written.
- 8: tiers (auto, confirm, deny) per tool risk; confirm shows the exact payload; deny beats everything; idempotent; a headless run has a defined behaviour.
- 10: policy also depends on whether untrusted content is in context and on the channel, approvals are durable records, every write has an undo or a compensating action, approval load is measured to avoid fatigue.

## 6. Injection and data safety (37, 38, 39, 43, 44; S-series)
- 2: untrusted text is pasted into the prompt as is.
- 5: untrusted text is wrapped, escaped and flagged, but the flag changes nothing and untrusted values still reach instructions or writes.
- 8: untrusted content can only fill data slots; when it is in context the write tier rises or the outward channel closes; code checks what code can check (quotes, ids, ranges).
- 10: control flow is separated from untrusted data by design (plan first, then read; or a quarantined model), no agent holds private data, untrusted input and an outward channel together, red-team cases run in CI.

## 7. Verification and evals (29 to 36; E-series; OMH-4, OMH-5)
- 2: unit tests with a mocked model only.
- 5: deterministic checks on model output in code (schema, quote present), no measurement of model quality.
- 8: a golden set from real cases, graders on outcomes, run before each prompt or model change, results stored.
- 10: evals gate CI, reliability measured over repeated runs, judge calibrated against humans, production traces feed the set, bias checks where people are scored.

## 8. Observability and cost (45, 46, 47, 48, 49)
- 2: application logs only.
- 5: a row per model call with prompt hash and latency, no tokens or cost, no tool-call rows.
- 8: a row per model call and per tool call with tokens, cost, model, settings actually sent, and a link between them; a per-run view; access limited by role.
- 10: replay of a run, cost per tenant and per feature, alerts on drift, standard trace attributes, retention matched to legal duties.

## 9. Surfaces and integration (10, 28; K20)
- 2: each surface (chat, MCP, API, sister product) has its own implementation of the same capability.
- 5: surfaces share services but not tool definitions; two approval systems can gate the same write.
- 8: one capability, one tool; chat, MCP and the sister product call the same tools with the same identity and policy; one authority approves each write.
- 10: the in-app chat is a client of the same public tool surface, so parity is by construction, and an agent can do everything a person can do in the GUI.

## 10. Product feel (K17, K18; E-series)
- 2: a blocking spinner; errors as raw text; the draft is lost on failure.
- 5: clear states for load, empty and error; no streaming, no stop, no progress on long steps.
- 8: streaming, stop, progress, draft kept, the approval card shows exactly what will be written and links the record, keyboard and screen reader work.
- 10: the fastest way to do the job is to ask; verification takes seconds; background runs report back; mobile works.

## Report table

| # | Axis | Score | Evidence (file:line) | Principle | Biggest lever |
|---|---|---|---|---|---|

Then: weighted total, the label (single call, workflow, agent, multi-agent), three levers in order, what stays, what was not read.

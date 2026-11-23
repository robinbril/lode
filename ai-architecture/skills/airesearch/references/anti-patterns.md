# Anti-patterns with detectors

Each pattern was seen in real code. The detector is a lead: open the hit and confirm before you report it. Run `scripts/scan.sh <repo>` for all detectors at once.

## A1. The gate that never closes
A "deny by default" policy where every listed entry is allow, and the names are code constants. The deny branch only catches a typo.
- Detect: `rg -n '"(allow|deny|ask|confirm)"' --type py --type ts` near a POLICY or permissions table; count the values.
- Why it matters: principle 13 and 40. A policy with one value is a log, not a policy.
- Fix shape: tiers per tool risk, raised when untrusted content is in context or the channel is external.

## A2. Labels that change nothing
Sources carry a trust label and an injection flag, but no code path branches on them.
- Detect: `rg -n 'trust|untrusted|injection' ` then check every consumer of the flag; `rg -n ', _ = .*\.(json|text)\('` finds callers that drop the flags.
- Principle 37, 38, 43.
- Fix shape: untrusted in context raises the write tier or closes the outward channel.

## A3. Truncation that eats the newest
History is joined oldest first and cut with `text[:limit]`.
- Detect: `rg -n '\[:[A-Z_]*(LIMIT|MAX|CHARS)[A-Z_]*\]|\[:[0-9]{4,}\]'` and `rg -n 'history\[-?[0-9]+:\]'`; compute messages times per-message cap against the source cap.
- Principle 15. Fix shape: budget from the newest backwards, summarise the rest.

## A4. Regex JSON, no schema
Model output is pulled out with a greedy regex and checked with scattered `isinstance`.
- Detect: `rg -n 're\.search\(r?.\\\{\.\*\\\}|json\.loads\(match' ` and the absence of `response_format`, `tool_choice`, `output_schema`, pydantic `model_validate` on model output.
- Principle 11. Fix shape: provider structured output where it exists, one schema validation in the harness, one retry with the validation error.

## A5. Model work inside the request
A handler loops over N items and calls the model each time, synchronously.
- Detect: `rg -n 'for .* in .*:' -A6 | rg 'harness\.|chat_complete|\.messages\.create|completions\.create'`; a `timeout` of a minute or more on a call made from a route.
- Principle 4, 8. Fix shape: a job with progress events; the request returns a run id.

## A6. The log that records what was not sent
A settings fingerprint hard-codes values (temperature, max tokens) that the client only sends for some providers.
- Detect: compare the fields in the fingerprint with the payload built per provider branch.
- Principle 45, 46. Fix shape: log the payload that was sent.

## A7. No tokens, no cost
- Detect: `rg -n 'usage|input_tokens|prompt_tokens|cache_read'` returns nothing in the model client.
- Principle 47. Also check whether docs claim metering.

## A8. One capability, many implementations
The same action exists as a route, a button handler, an MCP tool and a wrapper in a sister repo.
- Detect: list tool names per surface (`rg -n '@mcp\.tool|@server\.tool|def .*tool'`, OpenAPI operations, chat actions) and diff them.
- Principle 10. Fix shape: one registry; surfaces are generated.

## A9. The chat that points at buttons
The chat has no tools and its system prompt tells the model to refer the user to the UI.
- Detect: `rg -n -i 'buttons|point to them|click'` in prompt files; no `tools=` in the chat call.
- Principle 2, K20, K17. This is a help text, not an agent; name it honestly or give it tools.

## A10. Approval without content
A button writes model-produced content at once; the human approved the step, not the payload.
- Detect: follow each write to the UI event that triggers it; ask "did the user see these exact values before the write?".
- Principle 42, K18.

## A11. Two authorities for one write
A sister system has its own approval table for a write that the owning system also gates.
- Detect: search both repos for the same tool name in an approval or gated list.
- Principle 40. Fix shape: the system that owns the data approves; the caller shows the pending state.

## A12. Untrusted text outside the wrapper
A page title, a file name or a model-derived title is put into the instruction string instead of a source block.
- Detect: f-strings in prompt builders whose variables come from fetch results, uploads or earlier model output.
- Principle 43.

## A13. Mocked model as the only test
- Detect: `rg -n 'monkeypatch|mock|fake.*(llm|model|chat_complete)' tests/` against the absence of any eval or golden directory.
- Principle 31, 34.

## A14. Prompts readable by everyone
Full prompts with personal data are served to any signed-in user.
- Detect: the dependency on the log or trace endpoint (`get_current_user` against an admin or role check).
- S-series (logging and access).

## A15. Docs ahead of code
Architecture text says "tool use is normalised" or "usage is metered" and the code has neither.
- Detect: take each capability sentence from the architecture doc and grep for its implementation.
- Lower the axis by one and list it; the reader of the doc will plan on it.

## A16. Harness tied to one surface
Log and action rows require the UI's container (a workspace, a session) as a non-null key, and orchestration lives in route handlers that raise HTTP errors.
- Detect: non-null foreign keys on harness tables; `HTTPException` raised in service modules.
- Principle 8. A second surface (MCP, a job runner) cannot reuse it without a rewrite.

## A17. Tools that run in another process, outside the gate
The dispatcher holds the approval and taint checks, but a second executor is handed the same tools and runs them itself: a CLI agent started with an allowed-tools list, a worker, a sister service. The dispatcher only sees markers afterwards. A docstring may still say "this is the only executor".
- Detect: grep for `--allowedTools`, `allowed_tools`, `mcp-config`, `mcp_config`, `claude -p`, `subprocess` near tool lists; then compare the tool names handed over with the gated list in the dispatcher.
- Principle 40, D2. Score the permission axis on this path (rubric: two paths).
- Fix shape: every surface goes through the one dispatcher, or the second executor gets read tools only and writes come back as requests.

## A18. Policy as a list of names, open by default
Approval is a deny-list of tool names. A new or unnamed write tool runs without a gate.
- Detect: a set of gated tool names and no branch for "unknown tool"; ask what happens to a write tool added tomorrow.
- Principle 13 (the default for an undeclared tool assumes the worst).
- Note: the A1 detector counts tier strings and gives nothing here; read the dispatcher's decision function instead.

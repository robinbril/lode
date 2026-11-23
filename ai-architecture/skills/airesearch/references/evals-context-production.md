# Evals, context, UX, observability and cost for LLM agents (production depth)

Rules for reading this file
- Extends lab-principles.md groups 2, 4, 6, 8, 9 and fills the gaps listed at the bottom of that file. Where a principle only sharpens an existing one it says "extends #n" and adds only new facts.
- Every claim rests on a page or paper opened in this session (see sources-production.md). Quotes were grepped in the raw page text or PDF text. Quotes are under 15 words.
- Dashes inside quotes and titles were normalized to hyphens; wording is otherwise verbatim.
- Dates are the ones printed on the page or its metadata; "no date on page" otherwise. Paper numbers come from the arXiv HTML version named in each principle.
- `DISAGREEMENT:` marks conflicts between sources. `INFERRED:` marks a step I took that no opened source states. `THIN:` marks weak coverage.
- Review questions are written so a reviewer can answer yes or no by reading the code.
- The OpenAI "Harness engineering" post and the April 2026 Agents SDK post were seen only as third-party search summaries. Nothing from them is used. Both OpenAI pages returned HTTP 403 and stay NOT READ.

## Part 1. Evals in practice

**E1. Discover failure modes by reading real traces before you write any metric.**
Reasoning: Error analysis is open coding (free notes) followed by grouping into a failure taxonomy. Extends #33 and #34 with counts: a first manual pass of 20 to 50 outputs, a working pool of about 100 traces, discovery starting around 30 examples (judge post).
Quote: "Spend 30 minutes manually reviewing 20-50 LLM outputs" and "A pool of roughly 100 diverse traces is a useful starting point".
Source: Hamel Husain, evals FAQ ("LLM Evals: Everything You Need to Know"), https://hamel.dev/blog/posts/evals-faq/, published 2026-09-18, modified 2026-09-21; judge post https://hamel.dev/blog/posts/llm-judge/, 2024-10-29.
Review question: Is there a written failure taxonomy built from at least 30 real traces, with a count per failure type?

**E2. Build the golden set from production interactions, and turn every reported failure into a permanent test case.**
Reasoning: Google's Agent Ops chapter: sample scenarios from existing production or development interactions, cover the expected breadth plus a few unexpected cases, and have a domain expert review results before they count. A thumbs-down or bug report is converted into "a new, permanent test case in your evaluation dataset". Anthropic on size: "20-50 simple tasks drawn from real failures is a great start." Extends #34.
Source: Google "Introduction to Agents", Nov 2025 (page footer; third-party mirror of the Google PDF), https://www.rivista.ai/wp-content/uploads/2025/11/1762811267168.pdf; Anthropic "Demystifying evals for AI agents", https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents, Jan 9, 2026.
Review question: Is there a script or documented step that converts a production failure (trace id) into an eval case, and does the repo contain cases that came from production?

**E3. Grade pass or fail per failure mode, and keep nuance in a written critique, not in a 1-5 score.**
Reasoning: Binary labels are more consistent across annotators; the critique doubles as a few-shot example for the judge. Use one judge per failure type, not one judge for "quality".
Quote: "Binary evaluations force clearer thinking and more consistent labeling."
Source: Hamel evals FAQ (2026-09-18); judge post (2024-10-29: one principal domain expert, verdict plus critique).
Review question: Does each LLM judge return pass or fail for exactly one named failure mode, with a critique field?

**E4. Validate an LLM judge with true positive rate and true negative rate on held-out human labels, not with raw agreement.**
Reasoning: Extends #32. New facts: label about 100 to 200 examples per failure mode; split labels into training, dev and test sets, with the test set used once at the end; include 30 to 50 Pass and 30 to 50 Fail examples in both dev and test; below 60 examples the confidence intervals are too wide. TPR measures how many real failures the judge catches; TNR guards against false alarms; track both while editing the judge. Anthropic adds an escape hatch: tell a model grader to return "Unknown" when it lacks information.
Quote: "Raw agreement can be misleading when classes are imbalanced." and "Below 60 examples, the confidence intervals are often too wide".
Source: Hamel evals FAQ (2026-09-18); judge post (2024-10-29); Demystifying evals (Jan 9, 2026).
Review question: Is there a held-out labeled set with both classes, and are the judge's TPR and TNR reported before it gates anything?

**E5. Use a code check wherever an objective rule detects the failure; keep judges for subjective failures.**
Reasoning: Cheaper, deterministic and debuggable. Hamel also suggests a "pass-all rate" (an example passes only if every check passes) with drill-down per check. Anthropic: deterministic graders are the natural fit for coding agents.
Quote: "Use a code-based eval when an objective rule can identify the failure."
Source: Hamel evals FAQ (2026-09-18); Demystifying evals (Jan 9, 2026).
Review question: For each LLM judge, is there a note saying why a code check was not possible?

**E6. Trajectory metrics are a different tool from outcome grading; use them only where the path is itself the requirement.**
Reasoning: Google's Agents Companion lists six reference-based trajectory metrics: exact match, in-order match, any-order match, precision, recall, single-tool use. In-order match tolerates "extra, unpenalized actions". They need a reference trajectory. The Companion also says a human in the loop can "calibrate and double-check" automated evaluation.
DISAGREEMENT: Anthropic (#31) says grade the outcome, not the path, because exact tool sequences are too rigid. A reading consistent with both: outcome grading by default; in-order match or single-tool use only for path requirements, such as "approval tool called before the write tool" (INFERRED example).
Source: Google "Agents Companion", Feb 2025 (page footer; third-party mirror), https://cdn.jsdelivr.net/gh/abncharts/abncharts.public.1/abnasia.org/1743681605381_www.abnasia.org.pdf; Demystifying evals (Jan 9, 2026).
Review question: Does any eval assert an exact tool-call sequence, and if so is that sequence a real requirement?

**E7. Keep a small purpose-built regression set that runs in CI on every prompt, tool or model change and blocks the merge.**
Reasoning: Hamel: CI sets are small (often 100 or more cases), cover core features, past bugs and known edge cases, and the cost of each test matters because they run often. Braintrust documents the mechanism: run evals on every pull request, "gate merges on the results", post scores to the PR, run a sample (`--first N`) on the PR and the full set on merge. Anthropic separates capability evals from regression evals (see #33).
Quote: "small (in many cases 100+ examples) and purpose-built".
Source: Hamel evals FAQ (2026-09-18); Braintrust "Run experiments in CI/CD", https://docs.braintrust.dev/evaluate/run-in-ci.md, no date on page.
Review question: Does CI run the eval on pull requests that touch prompts, tool schemas or the model id, and does a score drop fail the check?

**E8. Treat synthetic test data as a last resort, and never use it to estimate how common a failure is.**
Reasoning: Synthetic cases can find initial problems but give limited evidence about real users.
Quote: "Synthetic data cannot tell you how common a failure is in production."
Source: Hamel evals FAQ (2026-09-18).
Review question: Are failure rates in reports computed from real traces only?

**E9. Gate a release on candidate versus production over the same dataset, then roll out gradually.**
Reasoning: Google: run the new version against the whole evaluation dataset and compare its scores with production; also watch latency, cost and task success; use A/B deployments to roll out slowly and compare real production metrics next to simulation scores.
Quote: "run the new version against the entire evaluation dataset".
Source: Google "Introduction to Agents", Nov 2025 (mirror).
Review question: Does the release process produce a side-by-side score table of candidate and production on the same cases?

**E10. When debugging agent workflows, grade traces first for tool choice, handoffs and policy violations; build datasets once you know what good looks like.**
Reasoning: OpenAI's agent evals guide orders the work: start with traces while debugging, grade them with questions like "Did the agent pick the right tool?", then move to datasets and eval runs for repeatability.
Source: OpenAI "Agent evals", https://developers.openai.com/api/docs/guides/agent-evals, no date on page.
THIN: the general OpenAI Evals guide (https://developers.openai.com/api/docs/guides/evals, no date on page) says nothing about calibrating graders against humans, and says Evals become read-only for existing users on 2026-10-31, so check its status before building on it.
Review question: Can a reviewer open one run as a trace and see each tool call with its grader verdict?

## Part 2. What the research papers say about how agents fail

**E11. Use the MAST failure taxonomy as a review checklist for multi-step and multi-agent code.**
Reasoning: 1642 annotated traces from 7 frameworks, 14 failure modes in 3 categories (system design, inter-agent misalignment, task verification), human agreement kappa 0.88, LLM annotator accuracy 94% (kappa 0.77). Printed shares of failures: step repetition 15.7%, reasoning-action mismatch 13.2%, unaware of termination conditions 12.4%, disobey task specification 11.8%, incorrect verification 9.1%, no or incomplete verification 8.2%, task derailment 7.4%, fail to ask for clarification 6.8%, premature termination 6.2%. ChatDev interventions: better role specification +9.4% task success, a high-level objective verification step +15.6%. Extends #4 and #30.
Source: "Why Do Multi-Agent LLM Systems Fail?", https://arxiv.org/html/2503.13657 (v3 26 Oct 2025; v1 17 Mar 2025).
Review question: Which code detects step repetition, missing termination awareness and unverified completion, and which test triggers each?

**E12. Ground reasoning in tool observations, and watch for repetition as the dominant failure of a grounded loop.**
Reasoning: On HotpotQA (200 labeled cases) hallucinated reasoning caused 56% of chain-of-thought failures and 0% of ReAct failures; ReAct failures were mostly reasoning errors (47%, including failing to recover from repetitive steps) and uninformative search results (23%). With PaLM-540B ReAct beat act-only on HotpotQA (27.4 vs 25.7) and FEVER (60.9 vs 58.9).
Source: ReAct, https://arxiv.org/html/2210.03629 (v3 10 Mar 2023).
Review question: Does the loop detect the same action with the same result twice and then change strategy or stop?

**E13. Design the agent-computer interface with guardrails, compact commands and short feedback; small interface choices move success a lot.**
Reasoning: SWE-agent ablations on SWE-bench Lite with GPT-4 Turbo (default 18.0% resolved): edit with a linter 18.0 vs no linting 15.0 vs no edit tool 10.3; summarized search 18.0 vs iterative search 12.0 vs no search 15.7; 100-line file viewer 18.0 vs 30 lines 14.3 vs full file 12.7; last 5 observations in full 18.0 vs full history 15.0. Older observations are collapsed to a single line, not deleted. An empty command output is replaced by an explicit message.
Quote: "Actions should be simple and easy to understand for agents."
Source: SWE-agent, https://arxiv.org/html/2405.15793 (v3 11 Nov 2024). Numbers are for one 2024 model; re-measure on yours.
Review question: Does each edit tool validate its result (lint or test) before returning, and is large output windowed?

**E14. Self-reflection only works when the failure signal is reliable.**
Reasoning: Reflexion reached 91% pass@1 on HumanEval, but its signal comes from generated unit tests: the false positive test rate was 16.3% on MBPP Python against 1.4% on HumanEval Python, and MBPP ended below baseline (77.1 vs 80.1). In AlfWorld reflection triggered when the same action got the same response for more than 3 cycles or after more than 30 actions. Memory held 1 to 3 reflections. A weak model (starchat-beta) matched baseline at 0.26 pass@1, so the gain depends on model strength.
Source: Reflexion, https://arxiv.org/html/2303.11366 (v4 10 Oct 2023).
Review question: What produces the failure signal that triggers a retry, and has its false-positive rate been measured?

**E15. A ledger with a stall counter beats an open loop, but irreversible actions still need limits.**
Reasoning: Magentic-One keeps a task ledger (facts, guesses, plan) in an outer loop and a progress ledger in an inner loop; a stall counter (threshold 2 in their runs) triggers reflection and replanning. Results: GAIA 38%, WebArena 32.8%, AssistantBench accuracy 27.7%. The most common error code was persistent-inefficient-actions. Observed risk: agents retried a login until the account was temporarily suspended, then tried a password reset. Extends #5.
Source: Magentic-One, https://arxiv.org/html/2411.04468 (7 Nov 2024).
Review question: Is there a stall counter, a bounded replan, and a human pause before irreversible actions?

**E16. State a capability claim with its success threshold; the 80% horizon is much shorter than the 50% horizon.**
Reasoning: METR v4: the 50% horizon doubled every 207 days (95% CI 166 to 240 days); the 80% horizon doubles at a similar rate (204 days) but is 4 to 6 times shorter, so models "cannot reliably perform tasks of moderate length". o3 had a 50% horizon of about 110 minutes in this text. Extends #36.
Source: "Measuring AI Ability to Complete Long Software Tasks", https://arxiv.org/html/2503.14499 (v4, 10 Jul 2026). Read from the v4 HTML.
Review question: When a spec says "runs unattended for N hours", does it name the success rate and the task type?

## Part 3. Context engineering and caching in production (closes the prompt-cache gap in lab-principles)

**E17. Design for the cache: in agents input dominates and cached tokens are about ten times cheaper.**
Reasoning: Manus reports an average input-to-output ratio around 100:1 and, for Claude Sonnet at that time, 0.30 USD per million cached input tokens against 3 USD uncached; its author calls KV-cache hit rate the single most important metric for a production agent. Anthropic's current docs price a 5-minute write at 1.25x, a 1-hour write at 2x and a read at 0.1x base (0.05x on Opus 5.5 and Sonnet 5.5). Extends #47.
Source: Manus, "Context Engineering for AI Agents: Lessons from Building Manus", https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus, 2025-07-18; Anthropic prompt caching docs, https://platform.claude.com/docs/en/build-with-claude/prompt-caching, no date on page.
Review question: Is cache hit rate (cache read tokens over total input tokens) tracked, with an alert?

**E18. Keep the prefix stable: append-only history, deterministic serialization, nothing volatile before the breakpoint.**
Reasoning: Manus: "Make your context append-only." Do not edit earlier actions or observations; JSON key order must be deterministic because unstable ordering silently breaks the cache. Anthropic: a hit needs an identical prefix, and `cache_control` belongs on the last block that is identical across requests, not a block with a timestamp. The lookback window is at most 20 blocks, so in a growing conversation add a second breakpoint if a turn adds many blocks.
Source: Manus (2025-07-18); Anthropic prompt caching docs.
Review question: Does anything volatile (time, request id, random ordering) appear before the cache breakpoint?

**E19. Know what invalidates the cache and avoid mid-run changes to tools, tool_choice, images, thinking and effort.**
Reasoning: The order is tools, then system, then messages; a change invalidates its level and every later one. Per the docs table, changing tool definitions invalidates the entire cache; changing `tool_choice` or adding or removing images invalidates system and messages; thinking and effort changes invalidate message blocks (and tools or system on some models). Up to 4 breakpoints. TTL is 5 minutes by default, refreshed by each read, or 1 hour at a higher write price. Short prompts are silently not cached (minimum 512 tokens on the newest models, up to 4,096 on some older ones). On Opus 5.5 and Sonnet 5.5 a new system instruction can be appended as a `role: system` message inside `messages` without invalidating the cache.
Source: Anthropic prompt caching docs (no date on page; read through the raw `.md`).
Review question: Does the code read `cache_creation_input_tokens` and `cache_read_input_tokens` and flag a run where reads stay zero?

**E20. Mask tools instead of removing them to steer behavior without breaking the cache.**
Reasoning: Manus keeps all tool definitions fixed and masks token logits during decoding to prevent or force a choice. This matches Anthropic's table: editing tool definitions invalidates the whole cache.
Quote: "Rather than removing tools, it masks the token logits".
Source: Manus (2025-07-18); Anthropic prompt caching docs. Manus runs its own inference setup. INFERRED: on a hosted API the nearest equivalent is `tool_choice` or a code gate, and the docs say `tool_choice` changes also invalidate part of the cache, so a code gate is the cache-safe option.
Review question: Is the tool list identical on every step of a run, with availability enforced by a gate in code?

**E21. Use the file system as memory and apply the four context moves (write, select, compress, isolate).**
Reasoning: Manus treats the file system as the ultimate context: unlimited, persistent and directly operable by the agent. LangChain's summary: write (scratchpad, memory), select (retrieve into the window), compress (summarize or trim; Claude Code auto-compacts after the window passes 95%), isolate (sub-agents, sandboxes, state fields). Extends #15 and #17.
Quote: "treat the file system as the ultimate context in Manus"
Source: Manus (2025-07-18); LangChain, "Context Engineering for Agents", https://www.langchain.com/blog/context-engineering-for-agents, 2025-07-02.
Review question: Are large tool results stored as files with a short pointer left in context, and can the agent reload them?

**E22. Keep failed actions and their errors visible, but collapse old observation bodies.**
Reasoning: Manus: leave the failed action and its error in context so the model shifts away from it. Claude Code's guidance adds a limit: after two failed corrections, `/clear` and write a better prompt, because a third correction only adds to a conversation containing two failed attempts.
DISAGREEMENT (soft): SWE-agent scored 15.0 with full history against 18.0 with the last 5 observations in full and older ones collapsed to one line. Both fit one rule: keep the action and the error line; shrink the payload. Extends #9.
Quote: "leave the wrong turns in the context" (Manus).
Source: Manus (2025-07-18); SWE-agent (arXiv 2405.15793); Claude Code best practices, https://code.claude.com/docs/en/best-practices (redirect target of the Anthropic engineering URL), no date on page.
Review question: Does compaction keep failed tool calls with their error text while dropping old successful payloads?

**E23. Break repetitive structure so the model does not copy its own pattern.**
Reasoning: Manus: uniform action-observation pairs push the model to repeat them; the more uniform the context, the more brittle the agent.
Quote: "don't few-shot yourself into a rut"
Source: Manus (2025-07-18).
Review question: In loops over many similar items (candidates, files, rows), has it been measured whether the 20th item is handled worse than the 1st?

**E24. Measure long-context degradation on your own task instead of trusting the advertised window.**
Reasoning: Chroma tested 18 LLMs (Anthropic, OpenAI, Google, Alibaba) over 194,480 calls: performance becomes less reliable as input grows; adding distractors lowers accuracy; on LongMemEval prompts, focused versions (about 300 tokens) scored consistently higher than full versions (about 113k tokens). The models were 2025 generations, so the size of the effect on current models is NOT measured by this source.
Quote: "performance grows increasingly unreliable as input length grows"
Source: Chroma, "Context Rot", https://www.trychroma.com/research/context-rot, 2025-07-14.
Review question: Is there an eval that varies context length on your task and sets a compaction threshold from it?

**E25. Structured outputs guarantee a shape, not the content: handle refusal and truncation, and validate semantics in code.**
Reasoning, by provider:
- OpenAI: constrains "completed, non-refusal model output" to the schema; the app must still handle refusals, incomplete responses and API errors, and validate business rules; all fields must be required, with optional emulated as a union with null; a new schema adds latency on its first request.
- Anthropic: constrained decoding, but the output may not match the schema when `stop_reason` is `refusal` or `max_tokens`; enum and const values can come back with different capitalization; numeric and string-length constraints are not enforced by the raw API; unsupported features return a 400; compiled grammars are cached for 24 hours; changing `output_config.format` invalidates the prompt cache for that thread.
- Gemini: syntactically valid JSON; `minLength`, `maxLength`, `minProperties`, `maxProperties` and others are not enforced; schemas over the complexity limits get a 400.
Quote: "always validate values in your application" (Gemini).
Source: OpenAI Structured Outputs, https://developers.openai.com/api/docs/guides/structured-outputs; Anthropic Structured outputs, https://platform.claude.com/docs/en/build-with-claude/structured-outputs; Gemini Structured output, https://aistudio.google.com/docs/structured-output. None prints a publication date (the Anthropic page shows an API version header 2026-10-21, the Gemini page `Api-Revision: 2026-05-20`; neither is a publication date).
Review question: After every structured call, does code check the stop reason, compare enums case-insensitively where needed, and validate lengths, ranges and business rules?

**E26. Turn on strict tool schemas where the provider supports them, and still repair or return errors for invalid calls.**
Reasoning: Vercel AI SDK: strict mode is off by default, set per tool, and ignored by providers that do not support it. The SDK models four tool-call errors, turns errors thrown in `execute` into `tool-error` parts so the model can retry, and offers a `repairToolCall` hook. Anthropic: strict tool use guarantees schema validation of tool names and inputs. Extends #9.
Source: Vercel AI SDK "Tools and tool calling", https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling, no date on page; Anthropic Structured outputs docs.
Review question: Is strict enabled on every tool whose provider supports it, and what happens on an invalid tool call (repair, error to the model, or crash)?

## Part 4. Agent UX and product

**E27. Streamed tool input is partial JSON: never execute from it, and handle errors that arrive inside the stream.**
Reasoning: Anthropic streaming sends `input_json_delta` fragments; the final `tool_use.input` is an object, so accumulate and parse at `content_block_stop`. By default the API buffers each complete key and value, so tool streams can pause. Errors such as `overloaded_error` can arrive as events in a stream that started normally. An interrupted stream can be continued by capturing the partial output and sending a continuation request (Claude 4.6 and later: a user message saying to continue from where it left off).
Source: Anthropic "Streaming messages", https://platform.claude.com/docs/en/build-with-claude/streaming, no date on page.
Review question: Does the stream handler treat an `error` event as a failed turn, and is a tool executed only after its block is complete and parsed?

**E28. An approval gate pauses the run into serializable state and fails closed; a run id is not authorization.**
Reasoning: OpenAI Agents SDK: `needs_approval` can be a callable and fails closed when arguments cannot be inspected. A paused run returns interruptions; the state is serialized, a reviewer approves or rejects each item, and the run resumes with the same top-level agent. The SDK does not authenticate snapshots, so deserialize only trusted data; store a version marker with the state. Approval does not give exactly-once execution, so side-effecting tools need stable idempotency keys and a reconcile step after a crash. Vercel AI SDK: a denial reason goes back to the model in the tool result; provider-executed tools skip the approval setting.
Quote: "Possession of a run ID or decision ID is not authorization."
Source: OpenAI Agents SDK "Human-in-the-loop", https://openai.github.io/openai-agents-python/human_in_the_loop/, no date on page; Vercel AI SDK tools page.
Review question: Is the pending approval stored server-side, checked against the authenticated reviewer, and does the approved tool use an idempotency key?

**E29. In a graph with interrupts the whole node re-runs on resume: put side effects after the interrupt or make them idempotent.**
Reasoning: LangGraph needs a durable checkpointer (the in-memory one is lost on restart) and a `thread_id`; resume uses `Command(resume=...)`; the node restarts from its beginning so code before `interrupt()` runs again. Also: do not wrap `interrupt()` in a bare try/except, keep interrupt order stable, pass serializable values only, and prune old checkpoints.
Quote: "Side effects called before interrupt must be idempotent" (page section title).
Source: LangGraph Interrupts, https://docs.langchain.com/oss/python/langgraph/interrupts, no date on page; LangGraph Durable execution, https://docs.langchain.com/oss/python/langgraph/durable-execution, no date on page.
Review question: Does any node write, send or create something before its interrupt call, and is that write idempotent?

**E30. Render approvals and agent-proposed UI from an allowlist of typed components that the app validates.**
Reasoning: AG-UI is an event-based protocol between agent and frontend with streaming, cancel and resume, shared state as streamed diffs, and human-in-the-loop interrupts. Its generative UI has a static form (model output rendered as stable, typed components under app control) and a declarative form where the agent proposes UI trees that the app validates before mounting.
Quote: "Pause, approve, edit, retry, or escalate mid flow without losing state."
Source: AG-UI introduction, https://docs.ag-ui.com/introduction, no date on page. THIN: introduction page only; the event schema was not read.
Review question: Can the agent cause the UI to render only components from a fixed list, with props validated by code?

**E31. For durable runs keep orchestration deterministic and make steps at-least-once with idempotency keys.**
Reasoning: DBOS: a workflow must invoke the same steps with the same inputs in the same order; non-deterministic work (random values, API calls, database access) belongs in steps; steps are tried at least once but never re-executed after they complete; an assigned workflow ID acts as an idempotency key. INFERRED for agents: each model call and tool call is a step, and the model's chosen action must be stored as a step result so replay does not ask the model again.
Source: DBOS workflow tutorial, https://docs.dbos.dev/python/tutorials/workflow-tutorial, no date on page (footer copyright 2026). THIN: Temporal and Inngest posts were not read.
Review question: If the process dies after a tool succeeded and before the next model call, does replay skip the completed tool call?

**E32. Enforce what must never be skipped with a deterministic hook, and ask for evidence instead of "done".**
Reasoning: Claude Code's best practices separate instructions (CLAUDE.md, prompts: the model reads them, with "no guarantee that it'll follow") from enforcement (tests, typecheck, a `Stop` hook, CI, permission rules). A Stop hook exits with code 2 to send the model back to work until the check passes or a block limit is reached. Premature completion is a named failure: Claude said it was done when "it had no way to check its own work". Ask for the command and its output, not a summary. Extends #30 and #35.
Source: Claude Code best practices, https://code.claude.com/docs/en/best-practices, no date on page.
Review question: Which rules are enforced by code (hook, CI, deny rule) and which exist only as prompt text?

**E33. Give an unattended run a done-definition, a self-check, a scope and a hard cap.**
Reasoning: The same page lists what to settle before a run goes unattended: what done looks like, whether it can check its own work, what it may touch, what stops it (`--max-turns`, `--max-budget-usd`, a spend limit), and who approves at the end. It notes that loops, goal checks and subagents keep spending while nobody types. Extends #4.
Quote: "Give it a cap on turns or spend"
Source: Claude Code best practices, no date on page.
Review question: Does the headless entry point set a turn cap and a spend cap, and does a human or CI check approve the result?

**E34. Put the pause point between tool choice and tool execution, and let the agent ask humans through a tool call.**
Reasoning: 12-factor agents factor 6 notes that orchestrators often allow pause and resume, but not between selecting a tool and executing it. Factor 7 proposes always outputting structured data and expressing intent (such as `request_human_input` or `done_for_now`) as a tool, instead of betting on whether the first token is text or JSON. Factor 11: triggers can be a message, a cron or a webhook, and quick human loops allow higher-stakes tools.
Source: 12-factor agents factors 6, 7, 11, https://github.com/humanlayer/12-factor-agents (raw files under `content/`), no date on page.
Review question: Can a run be stopped after the model chose a write action and before it ran, and resumed later by a webhook?

## Part 5. Observability and cost

**E35. Emit spans in the OpenTelemetry GenAI shape: one `invoke_agent` span, with inference spans and `execute_tool` spans beneath it.**
Reasoning: Per the spec repo: agent span `invoke_agent {gen_ai.agent.name}`, kind CLIENT; inference span `{gen_ai.operation.name} {gen_ai.request.model}`, kind CLIENT (INTERNAL if the model runs in process); tool span `execute_tool {gen_ai.tool.name}`, kind INTERNAL, with required `gen_ai.operation.name` and `gen_ai.tool.name`, and `error.type` and `gen_ai.tool.call.id` when applicable. Required on model calls: `gen_ai.operation.name` and `gen_ai.provider.name`. Recommended: response model, finish reasons, response id, usage. `gen_ai.conversation.id` ties spans of one session. Most inference attributes have Development status (only `error.type` and the server attributes are Stable), so names may change. Extends #45.
Source: OpenTelemetry GenAI conventions, https://github.com/open-telemetry/semantic-conventions-genai (files docs/gen-ai/client-invoke-agent.md, client-inference.md, execute-tool.md, read raw), no date on page. The older opentelemetry.io page only says the content moved.
Review question: Does one user request produce one agent span with model and tool spans beneath it, each carrying these attribute names?

**E36. Record content (prompts, tool arguments, results) only by opt-in, and store large payloads by reference.**
Reasoning: The spec makes `gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.system_instructions`, `gen_ai.tool.definitions`, `gen_ai.tool.call.arguments` and `gen_ai.tool.call.result` opt-in, and flags them as sensitive; content attributes have a `_ref` variant that stores a URI to external storage.
Quote: "This attribute may contain sensitive information."
Source: OTel execute-tool.md and client-inference.md (spec repo above).
Review question: Is content capture off by default, redacted where on, and are large payloads stored outside the trace backend?

**E37. Normalize token counts per provider before computing cost, because "input tokens" means different things.**
Reasoning: Anthropic's `input_tokens` counts only tokens after the last cache breakpoint; total input is cache reads plus cache writes plus `input_tokens`. OTel says `gen_ai.usage.input_tokens` SHOULD include cached tokens, with cache read and write as subsets. Langfuse says OpenAI input counts include cached tokens and must be converted to exclusive buckets before storing. A mapper that copies the Anthropic field straight into the OTel attribute undercounts input; a mapper that sums all buckets for OpenAI double counts (derived from the three sources, INFERRED as a bug class).
Quote: "Some provider counts are inclusive." (Langfuse)
Source: Anthropic prompt caching docs; OTel client-inference.md; Langfuse token and cost tracking, https://langfuse.com/docs/observability/features/token-and-cost-tracking, no date on page.
Review question: Does the cost function have a per-provider branch stating whether input tokens include cache reads, and is there a test with cached tokens?

**E38. Record usage at call time and compute cost at ingest with the prices of that day.**
Reasoning: Langfuse stores usage per type and cost per type, prefers ingested cost over inferred cost, and keeps the ingestion-time cost of stored generations when prices change. Usage must come from the integration; it no longer estimates tokens. OTel also defines token counters (input, output, cache read, cache write, reasoning), where cache and reasoning counters are subsets, and says the operation histograms should not be used for cost totals.
Quote: "Generations already stored keep the cost calculated at ingestion time."
Source: Langfuse token and cost tracking (no date on page); OTel gen-ai-token-metrics.md.
Review question: Is the price table versioned and is cost stored with each call, so a price change cannot rewrite history?

**E39. Attribute cost to a user, tenant or feature by putting that id on every trace.**
Reasoning: INFERRED: no opened source says "tenant". Langfuse shows cost monitored across models, tags and users, and filtered by user or tags in its Metrics API, so a tenant id sent as user id or tag would give per-tenant cost. OTel has `gen_ai.conversation.id` for sessions but no tenant attribute.
Source: Langfuse token and cost tracking (no date on page); OTel client-inference.md.
Review question: Does every model call carry a tenant id or tag, including background jobs and sub-agents?

**E40. Cut cost by shrinking what each request re-sends, and measure it per subagent and per task.**
Reasoning: Claude Code's best practices: every request sends the whole conversation, so `/clear` between unrelated tasks; put simple subagent work on `haiku`; ask subagents for short summaries; use `/usage` to see which subagents earn their cost; a warm cache discounts a long session. Google adds the KPI frame: goal completion, satisfaction, latency and operational cost per interaction, tied to business impact. Extends #47 and #48.
Quote: "Every request sends the whole conversation"
Source: Claude Code best practices (no date on page); Google "Introduction to Agents" (Nov 2025, mirror).
Review question: Is cost per completed task reported, split by agent role, and compared with the value of the task?

## 12-factor agents (HumanLayer): one line each

Source for every line: https://github.com/humanlayer/12-factor-agents, raw files under `content/`, no date on page. Each line follows the factor's own first paragraph.
1. Natural language to tool calls: turn a user phrase into a structured object that describes an API call.
2. Own your prompts: do not outsource prompt engineering to a framework.
3. Own your context window: input is "what's happened so far, what's the next step"; everything is context engineering.
4. Tools are just structured outputs: a tool is LLM-emitted JSON that triggers deterministic code.
5. Unify execution state and business state: you need not keep step, retry and waiting state apart from the event history.
6. Launch, pause, resume with simple APIs: start, query, pause and resume agents like any program, including by webhook.
7. Contact humans with tool calls: express "ask a human" or "done" as structured intents, not plain text.
8. Own your control flow: add your own summarization, judging, compaction, logging and human breakouts to the loop.
9. Compact errors into the context window: feed errors back so the model can self-heal; usable on its own.
10. Small, focused agents: narrow scope keeps context short and the model focused.
11. Trigger from anywhere, meet users where they are: users, crons and events start agents, and answers go back through the same channel.
12. Make your agent a stateless reducer: the agent takes state plus an event and returns new state (the page itself says this one is "mostly just for fun").
13. Appendix, pre-fetch all the context you might need: if a tool is very likely needed, fetch it up front instead of spending a model round trip.

## What best-in-class looks like

| # | Capability | Minimum bar | Best-in-class bar | Principles |
|---|---|---|---|---|
| 1 | Eval set | 20 to 50 cases from real failures, checked into the repo | CI set of 100 or more purpose-built cases; every production failure becomes a case; held-out test set | E2, E7 |
| 2 | Failure discovery | Read 20 to 50 traces after each significant change | Written failure taxonomy with counts, redone on about 100 fresh traces per cycle, MAST modes as checklist | E1, E11 |
| 3 | Graders | Code checks first; one binary judge per failure mode with critique | Judge validated with TPR and TNR on held-out dev and test sets (30 to 50 per class); "Unknown" allowed | E3, E4, E5 |
| 4 | Release gate | Eval runs in CI and blocks on a score drop | Candidate versus production on the same cases, PR smoke run, full run on merge, staged rollout | E7, E9 |
| 5 | Reliability claims | Report pass@1 with the task type | Report the success threshold (50% versus 80% horizon) and pass^k as in #32; use trajectory metrics only for path requirements | E6, E16 |
| 6 | Prompt cache | Stable prefix; cache read tokens logged | Breakpoint on last identical block; no mid-run tool or tool_choice changes; alert on zero reads; hit rate tracked | E17, E18, E19, E20 |
| 7 | Context management | Tool output cap and compaction | File-based memory; old observations collapsed with errors kept; compaction threshold set from a measured length curve | E21, E22, E24 |
| 8 | Structured output and tools | Schema-constrained output and strict tool schemas | Stop reason handling; semantic validation after parse; enum casing; repair or error path for invalid tool calls | E25, E26 |
| 9 | Human approval | Approval gate on write tools that fails closed | Server-side serialized state; reviewer authorization; idempotency keys; side effects after the interrupt; pause between tool choice and execution | E28, E29, E34 |
| 10 | Streaming and UI | Stream text and show tool status | Partial JSON parsed only at block end; mid-stream error handling; cancel and resume; allowlisted generative UI | E27, E30 |
| 11 | Long and unattended runs | Turn cap and spend cap | Deterministic done-check (Stop hook or CI); durable workflow with idempotent steps; human approval at the end | E31, E32, E33 |
| 12 | Observability and cost | Per-call log with ids, tokens and errors | OTel agent, inference and tool spans; opt-in content by reference; per-provider token normalization; cost stored at ingest; tenant id on every trace (INFERRED) | E35, E36, E37, E38, E39, E40 |

## Still NOT READ or thin (do not quote from this file for these)
- OpenAI "Harness engineering" and the April 2026 "next evolution of the Agents SDK" post: HTTP 403, NOT READ. The Agents SDK docs pages for human-in-the-loop and sandbox agents were read instead.
- Google "Agents" whitepaper (Sept 2024): no PDF opened. "Introduction to Agents" and "Agents Companion" were read from third-party mirrors, not from Google.
- Temporal and Inngest posts on agents; OpenAI function-calling docs beyond structured outputs; calibration advice in OpenAI's Evals guide (none found).
- Per-tenant cost: no opened source uses the word tenant (E39 is INFERRED).
- Hamel Husain and Shreya Shankar's dedicated judge-validation paper was not opened.

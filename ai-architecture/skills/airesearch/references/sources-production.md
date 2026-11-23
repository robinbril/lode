# Sources for evals-context-production.md

Date rule: the date printed on the page, or its page metadata; "no date on page" when none was shown. READ = I opened it. Method tags: "raw" = fetched the raw page or PDF text and grepped quotes; "summary" = WebFetch summarizer only (no quote taken from it unless re-checked raw). NOT READ = could not open or did not open.

## Evals
- https://hamel.dev/blog/posts/evals-faq/ | published 2026-09-18, modified 2026-09-21 (page metadata) | READ (summary, then raw grep of quotes; the end of the page was cut off in the summary, but the CI sentence was found raw) | good for: error analysis counts, binary evals, judge label splits, regression set, synthetic data caution.
- https://hamel.dev/blog/posts/llm-judge/ | published 2024-10-29, modified 2026-09-01 | READ (summary, raw grep of key quotes) | good for: principal domain expert, TPR and TNR, 100 labels per failure mode, below 60 examples too wide.
- https://hamel.dev/blog/posts/field-guide/ | Mar 24, 2025 | READ (summary only, no quote used) | good for: background on error analysis first and custom data viewers.
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Jan 9, 2026 | READ (raw grep) | good for: 20-50 tasks from real failures, pass^k definition, "Unknown" grader output.
- https://developers.openai.com/api/docs/guides/agent-evals | no date on page | READ (summary and raw grep of two phrases) | good for: trace grading first, grader questions about tool choice and handoffs, then datasets.
- https://developers.openai.com/api/docs/guides/evals | no date on page (lists an Oct 31, 2026 read-only date for Evals) | READ (summary) | good for: BDD-style eval workflow; no grader calibration advice on the page.
- https://docs.braintrust.dev/evaluate/run-in-ci.md | no date on page | READ (raw) | good for: PR eval action, gate merges, `bt eval --first N` smoke run versus full run.
- https://docs.braintrust.dev/guides/evals/run | no date on page | READ (summary) | good for: nothing concrete on CI gates; it points to the run-in-ci page.
- https://www.rivista.ai/wp-content/uploads/2025/11/1762811267168.pdf (third-party mirror of Google "Introduction to Agents") | page footer "November 2025" | READ (pdftotext) | good for: golden dataset from production, LM judge with domain expert review, candidate versus production gate, feedback becomes permanent test case, OTel traces for debugging.
- https://cdn.jsdelivr.net/gh/abncharts/abncharts.public.1/abnasia.org/1743681605381_www.abnasia.org.pdf (third-party mirror of Google "Agents Companion") | page footer "February 2025" | READ (pdftotext) | good for: six trajectory metrics, autorater, human evaluation of the evaluator.

## Research papers (arXiv HTML)
- https://arxiv.org/html/2503.13657 ("Why Do Multi-Agent LLM Systems Fail?") | v3 26 Oct 2025 (v1 17 Mar 2025) | READ (HTML, raw grep of numbers) | good for: 14 failure modes with printed percentages, 1642 traces, kappa 0.88, +9.4% and +15.6% interventions.
- https://arxiv.org/html/2405.15793 (SWE-agent) | v3 11 Nov 2024 (v1 6 May 2024) | READ (HTML, raw grep of ablation table; the second half was cut off in the summary) | good for: ACI ablations on linter, search, viewer window, last 5 observations.
- https://arxiv.org/html/2210.03629 (ReAct) | v3 10 Mar 2023 | READ (HTML, raw grep of failure table) | good for: HotpotQA failure categories (hallucination 56% for CoT, 0% for ReAct).
- https://arxiv.org/html/2303.11366 (Reflexion) | v4 10 Oct 2023 | READ (HTML, raw grep) | good for: false-positive test rate 16.3% versus 1.4%, reflection triggers, dependence on a reliable signal.
- https://arxiv.org/html/2411.04468 (Magentic-One) | 7 Nov 2024 | READ (HTML, raw grep; last 8k characters not read) | good for: task and progress ledgers, stall counter, benchmark numbers, error codes, observed safety incidents.
- https://arxiv.org/html/2503.14499 (METR, long software tasks) | v4 10 Jul 2026 (v1 18 Mar 2025) | READ (HTML, raw grep; part of the page not read) | good for: 207-day doubling, 80% horizon 4 to 6 times shorter than 50%.

## Context engineering and caching
- https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus | 2025-07-18 (printed "2025/7/18") | READ (raw grep) | good for: KV-cache hit rate, 100:1 ratio, 0.30 versus 3 USD, append-only, mask logits, file system, keep errors, few-shot rut.
- https://www.trychroma.com/research/context-rot | 2025-07-14 (report date; clarifications 2025-07-16) | READ (summary plus raw grep of key lines) | good for: 18 models, 194,480 calls, focused versus full LongMemEval prompts.
- https://www.langchain.com/blog/context-engineering-for-agents | 2025-07-02 | READ (summary plus raw grep of the 95% line) | good for: write, select, compress, isolate.
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching (also the `.md` copy) | no date on page | READ (summary of the first 100k characters, key rules grepped raw) | good for: breakpoints, TTL, prices, invalidation table, 20-block lookback, usage fields.
- https://platform.claude.com/docs/en/build-with-claude/structured-outputs | no date on page (API header 2026-10-21 is not a publication date) | READ (raw `.md`, refusal and max_tokens section grepped) | good for: what is guaranteed and not for Anthropic.
- https://developers.openai.com/api/docs/guides/structured-outputs | no date on page | READ (raw HTML grep; the supported-schemas section was not fully read) | good for: guarantee wording, refusals, all fields required.
- https://aistudio.google.com/docs/structured-output (redirect target of the Gemini API docs page) | no date on page (`Api-Revision: 2026-05-20` is not a publication date) | READ (raw grep) | good for: syntactic versus semantic validity, unenforced constraints.
- https://code.claude.com/docs/en/best-practices (redirect target of https://www.anthropic.com/engineering/claude-code-best-practices) | no date on page | READ (full text saved and grepped) | good for: deterministic versus instruction rules, Stop hook, unattended run checklist, cost habits.
- https://cognition.com/blog/dont-build-multi-agents | 2025-06-12 | READ only for a date check this session; content already covered in sources.md and lab-principles.md | good for: nothing new here.

## Agent UX and product
- https://platform.claude.com/docs/en/build-with-claude/streaming | no date on page | READ (saved text grepped) | good for: partial JSON tool input, mid-stream errors, interrupted stream recovery.
- https://openai.github.io/openai-agents-python/human_in_the_loop/ | no date on page | READ (summary plus raw grep of three quotes) | good for: approval interruptions, serialized state, fail closed, idempotency.
- https://openai.github.io/openai-agents-python/sandbox_agents/ | no date on page | READ (summary) | good for: sandbox manifest, snapshot resume; no credential guidance on the page. No principle depends on it.
- https://docs.langchain.com/oss/python/langgraph/interrupts | no date on page | READ (summary plus raw grep) | good for: node re-run on resume, idempotent side effects.
- https://docs.langchain.com/oss/python/langgraph/durable-execution | no date on page | READ (summary) | good for: durable checkpointer and thread id only; the page has no determinism rules.
- https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling | no date on page | READ (summary plus raw grep) | good for: tool approval, denial reason, repairToolCall, strict mode.
- https://docs.ag-ui.com/introduction | no date on page | READ (summary plus raw grep of quotes) | good for: streaming, cancel and resume, interrupts, generative UI forms.
- https://docs.dbos.dev/python/tutorials/workflow-tutorial | no date on page (footer 2026) | READ (summary plus raw grep) | good for: workflow determinism, at-least-once steps, workflow id as idempotency key.

## Observability and cost
- https://github.com/open-telemetry/semantic-conventions-genai (docs/gen-ai/client-inference.md, client-invoke-agent.md, execute-tool.md, gen-ai-token-metrics.md, read through raw.githubusercontent.com) | no date on page | READ (raw grep for span names and usage attributes; the last 33k characters of client-inference.md were not read) | good for: span names and kinds, attributes, token usage, opt-in content.
- https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/ | no date on page | READ (it only says the content moved) | good for: pointer to the new repo.
- https://langfuse.com/docs/observability/features/token-and-cost-tracking | no date on page | READ (summary plus raw grep) | good for: inclusive versus exclusive token buckets, ingestion-time cost, cost by user and tag.

## 12-factor agents
- https://github.com/humanlayer/12-factor-agents (README plus `content/factor-01` to `factor-12` and `appendix-13-pre-fetch.md`, raw) | no date on page | READ (raw) | good for: the 13 one-line summaries and factors 6, 7, 11.

## NOT READ
- https://openai.com/index/harness-engineering/ ("Harness engineering") | HTTP 403 via WebFetch | NOT READ | good for: nothing. Third-party summaries seen in search (numbers such as 1M lines and 1,500 PRs) were not used.
- https://openai.com/index/the-next-evolution-of-the-agents-sdk/ | HTTP 403 | NOT READ | good for: nothing. A search result gave the date April 15, 2026 from secondary coverage; not used.
- https://developers.openai.com/api/docs/guides/harness-engineering | HTTP 404 (checked with curl) | NOT READ | good for: nothing.
- https://www.kaggle.com/whitepaper-agents (Google "Agents", Sept 2024 per secondary coverage) | page is JavaScript only (title text only) | NOT READ | good for: nothing. No PDF mirror of this one was opened.
- Google "Introduction to Agents" and "Agents Companion" on Google's own sites | not opened; read only from the third-party PDF mirrors above | NOT READ (official copy) | good for: confirming the mirrors match.
- Temporal and Inngest posts on durable agents | not searched | NOT READ | good for: durable execution beyond DBOS.
- Hamel Husain and Shreya Shankar judge-validation paper | not opened | NOT READ | good for: formal judge calibration.

# Source index

Date rule: the date is the one printed on the page; "no date on page" when none was shown. READ = I opened the page (via WebFetch, which answers through a summarizer; quotes were requested verbatim) and, where marked "curl-checked", I also grepped the raw HTML for the key number. NOT READ = I did not open it, or could not.

## Part A repos
- https://github.com/rlaope/oh-my-hermes shallow clone, HEAD dated 2026-11-13: READ (selected files only, see oh-my-hermes-patterns.md). Good for: evidence boundary, loop fence/judge, verification gate, routing by category.

## Anthropic
- https://www.anthropic.com/engineering/building-effective-agents | Dec 19, 2024 | READ | workflow vs agent definitions, "simplest solution possible", stopping conditions, framework caution.
- https://www.anthropic.com/engineering/multi-agent-research-system | Jun 13, 2025 | READ | orchestrator-worker, 90.2% eval gain, token cost, effort scaling rules, failure modes.
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Sep 29, 2025 | READ | context as finite resource, compaction, note-taking, sub-agents, just-in-time retrieval.
- https://www.anthropic.com/engineering/writing-tools-for-agents | Sep 11, 2025 | READ | tool design and eval loop, 25,000 token cap, namespacing, error messages.
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | Nov 26, 2025 | READ | initializer agent, feature list, progress file, one feature per session.
- https://www.anthropic.com/engineering/code-execution-with-mcp | Nov 4, 2025 | READ | code-as-tool-interface, 150,000 to 2,000 tokens claim, sandbox overhead.
- https://www.anthropic.com/engineering/harness-design-long-running-apps | Mar 24, 2026 (page metadata) | READ, curl-checked | planner/generator/evaluator, self-evaluation bias, context reset vs compaction, "every component in a harness encodes an assumption". Supersedes the Nov 2025 harness post for evaluator design.
- https://www.anthropic.com/engineering/managed-agents ("Scaling Managed Agents with stable interfaces") | Apr 8, 2026 | READ, curl-checked | session/harness/sandbox split, credentials never reachable from sandbox, harness as disposable.
- https://www.anthropic.com/engineering/claude-code-auto-mode | Mar 25, 2026 | READ, curl-checked | approval fatigue, two-stage classifier, 0.4% FPR / 17% FNR, deny-and-continue (3 consecutive / 20 total).
- https://www.anthropic.com/engineering/how-we-contain-claude | May 25, 2026 | READ, curl-checked | containment vs supervision, layered defenses, credentials outside the sandbox, Gray Swan numbers.
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Jan 9, 2026 | READ, curl-checked | grader types, pass@k vs pass^k, grade outcome not path, read transcripts.
- https://www.anthropic.com/research/prompt-injection-defenses ("Mitigating prompt injections in browser use") | Nov 24, 2025 | READ, curl-checked | "No browser agent is immune"; RL + classifiers + red team; 1% ASR still "meaningful risk".
- https://code.claude.com/docs/en/agent-sdk/overview | no date on page | READ, curl-checked | SDK = Claude Code's loop, tools, hooks, subagents, sessions as library.
- https://code.claude.com/docs/en/agent-sdk/subagents | no date on page | READ, curl-checked | subagent context isolation, only final message returns, depth limit env var.
- https://platform.claude.com/docs/en/agent-sdk/permissions | no date on page | READ, curl-checked | ordered permission evaluation, plan-mode inheritance by subagents.
- https://code.claude.com/docs/en/agent-sdk/hooks | no date on page | READ, curl-checked | hooks run in parallel; most restrictive permission decision wins.
- https://www.anthropic.com/engineering/claude-code-best-practices | NOT READ (appeared in search only).
- Corrected 2026-11-13: the claim "users approve about 93% of permission prompts" IS in the auto-mode post and the containment post (found in the raw HTML on a second read). See S28 in security-mcp-regulation.md.

## OpenAI
- https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf | PDF metadata CreationDate 2025-04-07, no date printed | READ (pages 4-14 as images, 15-32 via pdftotext) | when to build an agent, single vs manager vs decentralized, guardrails, human intervention.
- https://openai.github.io/openai-agents-python/handoffs/ | no date on page | READ, curl-checked | handoff = tool; on_handoff validates args; is_enabled cannot authorize argument values; input_filter.
- https://openai.github.io/openai-agents-python/guardrails/ | no date on page | READ, curl-checked | input guardrails only on first agent, output only on final agent, tool guardrails per tool call; parallel vs blocking mode.
- https://openai.com/index/harness-engineering/ ("Harness engineering: leveraging Codex in an agent-first world") | NOT READ. WebFetch returned HTTP 403 and a plain curl returned an empty page. I did not try to bypass the block. Only a search summary (dated Feb 11, 2026 by third parties) exists, so nothing from it is used as a principle.

## Google / DeepMind
- https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ | Apr 9, 2025 (datePublished in page metadata) | READ, curl-checked | A2A: Agent Card capability discovery, task lifecycle, complements MCP.
- https://arxiv.org/abs/2503.18813 (CaMeL, "Defeating Prompt Injections by Design") | v1 24 Mar 2025, v2 24 Jun 2025 | READ (abstract page, curl-checked) | control/data flow separation, capabilities, 77% tasks with provable security vs 84% undefended in AgentDojo (v2 abstract).
- https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/ | Jan 28, 2026 | READ, curl-checked | multi-agent +80.9% on parallelizable, -39% to -70% on sequential; architecture-task fit.
- https://arxiv.org/abs/2512.08296 ("Towards a Science of Scaling Agent Systems") | v1 9 Dec 2025, v3 8 Apr 2026 | READ (abstract page) | 260 configurations; centralized verification limits error propagation.
- https://cloud.google.com/blog/products/ai-machine-learning/how-agents-can-delegate-better | Aug 22, 2026 | READ, curl-checked | four delegation principles (verify delegated work, cost, least data, zone of indifference), built on the paper below.
- https://arxiv.org/abs/2602.11865 ("Intelligent AI Delegation", Google DeepMind authors per the Cloud blog) | 12 Feb 2026 | READ (abstract page) | delegation framework: authority, accountability, contracts.
- https://www.kaggle.com/whitepaper-agents (Google "Agents" whitepaper, Sept 2024 per secondary sources) | NOT READ. The page is JavaScript-only (19 characters of text via curl). Not used.
- Google "Agents Companion" whitepaper (Feb 2025 per secondary sources) | NOT READ. Only secondary summaries seen. Not used.
- Google "Introduction to Agents" (Nov 2025 per secondary sources) | NOT READ.

## Anthropic multi-agent guidance (2026, supersedes parts of the 2025 research-system post)
- https://claude.com/resources/articles/building-multi-agent-systems-when-and-how-to-use-them ("When to use multi-agent systems (and when not to)") | Jan 23, 2026 | READ, curl-checked | three cases where multi-agent wins; 3-10x token overhead; start with a single agent.
- https://claude.com/resources/articles/multi-agent-coordination-patterns | Apr 10, 2026 | READ, curl-checked | generator-verifier, orchestrator-subagent, agent teams, message bus; verifier is only as good as its criteria; iteration cap.
- https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop | Oct 22, 2026 | READ, curl-checked | newest Anthropic position: single agent with skills often beats subagent designs; split by context, not by job type; eval before folding.

## Others
- https://cognition.com/blog/dont-build-multi-agents | 2025-06-12 (page metadata) | READ, curl-checked | share full traces; actions carry implicit decisions; single-threaded default.
- https://cognition.com/blog/multi-agents-working | 2026-04-22 (page metadata) | READ, curl-checked | Cognition's update: writes single-threaded, extra agents contribute intelligence; clean-context reviewer.
- https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems | Jun 16, 2025 | READ, curl-checked | read-heavy multi-agent easier than write-heavy; context engineering.
- https://github.com/humanlayer/12-factor-agents (README + factor 3, 8, 9, 10 via raw.githubusercontent.com) | no date on page (author, per search: Apr 2025) | READ | own prompts, context window, control flow; small focused agents.
- https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | Jun 16, 2025 | READ, curl-checked | private data + untrusted content + external communication.
- https://arxiv.org/abs/2503.13657 (MAST, "Why Do Multi-Agent LLM Systems Fail?") | v1 17 Mar 2025, v3 26 Oct 2025 | READ (abstract page) | 14 failure modes in 3 categories, 1600+ traces.
- https://arxiv.org/abs/2503.14499 (METR, "Measuring AI Ability to Complete Long Software Tasks") | v1 18 Mar 2025, v4 10 Jul 2026 | READ (abstract page, v4) | 50% time horizon metric; doubling about every seven months since 2019 (v4 abstract wording).
- https://arxiv.org/abs/2210.03629 (ReAct) | v1 6 Oct 2022, v3 10 Mar 2023 | READ (abstract) | interleave reasoning and acting.
- https://arxiv.org/abs/2303.11366 (Reflexion) | 20 Mar 2023, v4 10 Oct 2023 | READ (abstract) | verbal reflection in episodic memory, 91% pass@1 HumanEval claim.
- https://arxiv.org/abs/2305.04091 (Plan-and-Solve) | 6 May 2023, v3 26 May 2023 | READ (abstract) | plan first, then execute; reduces missing-step errors.
- https://arxiv.org/abs/2411.04468 (Magentic-One) | 7 Nov 2024 | READ (abstract) | orchestrator plans, tracks progress, re-plans.
- https://arxiv.org/abs/2308.08155 (AutoGen) | 16 Aug 2023, v2 3 Oct 2023 | READ (abstract) | conversable multi-agent framework.
- https://arxiv.org/abs/2405.15793 (SWE-agent) | 6 May 2024, v3 11 Nov 2024 | READ (abstract) | agent-computer interface design changes agent performance.
- Not searched or not opened: LangChain context-engineering post, OpenAI Codex-specific posts beyond the 403 above, Google "Intelligent AI Delegation" full text, Anthropic "Claude Code best practices", METR newer time-horizon posts (only the paper abstract v4), METR/Anthropic task-length measurements beyond that.

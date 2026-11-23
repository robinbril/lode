# Lab principles for LLM agent orchestration

Rules for reading this file
- Every principle rests on a page or paper I opened (listed in sources.md). Quotes are verbatim from the opened page; numbers were checked in the page text unless marked "via WebFetch only".
- Em and en dashes inside quotes were normalized to hyphens or commas; wording is otherwise verbatim.
- Dates are as printed on the page or its metadata. Where a newer source from the same lab changes the advice, I say so under the principle.
- `DISAGREEMENT:` marks places where sources conflict. `THIN:` marks groups where I have few opened sources.
- Review questions are written so a reviewer can answer yes/no by reading the code.

## Group 1. When to use an agent at all

**1. Start with the simplest thing; add complexity only when it measurably helps.**
Reasoning: Anthropic: "we recommend finding the simplest solution possible, and only increasing complexity when needed"; and "consider adding complexity only when it demonstrably improves outcomes." Agentic systems "trade latency and cost for better task performance" and bring "compounding errors."
Source: Building effective agents, https://www.anthropic.com/engineering/building-effective-agents, Dec 19, 2024. Echoed by Harness design for long-running apps, https://www.anthropic.com/engineering/harness-design-long-running-apps, Mar 24, 2026.
Review question: Is there a recorded baseline (one prompt, or a fixed workflow) that the agent design was measured against, with the score difference stated?

**2. Use an agent only where fixed rules fall short.**
Reasoning: OpenAI lists three signals (complex decision-making, rules too hard to maintain, heavy unstructured data) and says "Otherwise, a deterministic solution may suffice." Anthropic distinguishes workflows (code decides the path) from agents (LLM directs its own process) and says routing, chaining and similar workflows fit predictable tasks.
Source: A practical guide to building agents, https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf, PDF created 2025-04-07 (no date printed), p.6; Building effective agents (above).
Review question: For each LLM-driven decision, can the author say why a conditional, a lookup or a classifier would not do?

**3. Re-test every harness component when the model changes.**
Reasoning: "every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing ... they can quickly go stale as models improve." In the managed-agents post, context-reset behaviour seen on one model "was gone" on Claude Opus 4.5 and "the resets had become dead weight."
Source: Harness design for long-running apps (Mar 24, 2026); Scaling Managed Agents with stable interfaces, https://www.anthropic.com/engineering/managed-agents, Apr 8, 2026.
Review question: Does each non-trivial harness part (planner, router, subagent, reset, evaluator) have a note stating which model weakness it covers and an ablation that was run on the current model?

## Group 2. Loop design

**4. Every loop has explicit stop conditions and a bounded retry budget.**
Reasoning: Anthropic: "it's also common to include stopping conditions (such as a maximum number of iterations) to maintain control." OpenAI: a run is a loop with exit conditions "tool calls, a certain structured output, errors, or reaching a maximum number of turns"; human handover triggers include "Exceeding failure thresholds." Anthropic's auto mode stops and escalates after 3 consecutive or 20 total denials.
Source: Building effective agents (Dec 19, 2024); OpenAI practical guide pp.14 and 31 (exit conditions; human intervention); How we built Claude Code auto mode, https://www.anthropic.com/engineering/claude-code-auto-mode, Mar 25, 2026.
Review question: Can you point to the turn cap, the per-recovery retry counter and the escalation target, and does each recovery path decrement something?

**5. Keep the plan visible and let environment feedback, not self-belief, drive the next step.**
Reasoning: ReAct interleaves reasoning traces with actions so that "actions allow it to interface with external sources ... to gather additional information"; Anthropic's summary rule is "Prioritize transparency by explicitly showing the agent's planning steps." Magentic-One uses an orchestrator that "plans, tracks progress, and re-plans to recover from errors." Plan-and-Solve shows planning before solving reduces missing-step errors (evidence is from zero-shot reasoning benchmarks, not agent loops).
Source: ReAct, https://arxiv.org/abs/2210.03629 (v3, 10 Mar 2023); Magentic-One, https://arxiv.org/abs/2411.04468 (7 Nov 2024); Plan-and-Solve, https://arxiv.org/abs/2305.04091 (v3, 26 May 2023); Building effective agents.
Code seen: OMH-4 (replan once from the ledger, then name the blocker).
Review question: Is the plan stored somewhere a reviewer can read, and is re-planning bounded?

**6. For long tasks, hand state over in structured artifacts and work one unit at a time.**
Reasoning: Each session starts without memory, so the harness uses an initializer session, a feature list, a progress file and git commits; "This incremental approach turned out to be critical to addressing the agent's tendency to do too much at once." Each session starts by reading the progress notes and git log and running a basic test. "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."
Source: Effective harnesses for long-running agents, https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents, Nov 26, 2025 (extended by the Mar 24, 2026 post).
Code seen: OMH-4 (finish line + fenced files the loop may not edit).
Review question: If the process is killed now, can a fresh agent resume from files on disk alone, and is there a rule that tests cannot be weakened to pass?

**7. Context reset and compaction are different tools; pick by observed model behaviour.**
Reasoning: Compaction summarizes in place; "it doesn't give the agent a clean slate, which means context anxiety can still persist." A reset needs a handoff artifact with enough state. This was needed for Sonnet 4.5 in Anthropic's tests and became unnecessary on Opus 4.5.
Source: Harness design for long-running apps (Mar 24, 2026); Managed Agents post (Apr 8, 2026).
DISAGREEMENT (soft, over time): the Nov 2025 harness post leaned on resets; the Apr 2026 post says they became dead weight on a newer model. Prefer the newer one and re-test.
Review question: Does the system measure whether late-context quality drops on the current model before paying the cost of resets?

**8. Keep the session durable and the harness disposable.**
Reasoning: Anthropic separates the append-only session log, the harness loop and the sandbox; "Because the session log sits outside the harness, nothing in the harness needs to survive a crash." A failed container is a tool-call error handed back to the model.
Source: Managed Agents post (Apr 8, 2026). 12-factor agents lists "Launch/Pause/Resume with simple APIs" and "Make your agent a stateless reducer" (README titles only; factor 12 body not read), https://github.com/humanlayer/12-factor-agents, no date on page.
Review question: Where is the event log stored, and can a new harness process continue from the last event?

**9. Return tool errors to the model in a compact, actionable form.**
Reasoning: 12-factor factor 9: a failed tool call can be added to the context so the model can "figure out what to change in a subsequent tool call." Anthropic tools post: "you can prompt-engineer your error responses to clearly communicate specific and actionable improvements."
Source: 12-factor agents factor 9 (raw README text, no date); Writing effective tools for agents, https://www.anthropic.com/engineering/writing-tools-for-agents, Sep 11, 2025.
Review question: Do tool errors say what to change next, and is there a cap on consecutive identical failures?

## Group 3. Tools

**10. Fewer, clearly distinct, namespaced tools.**
Reasoning: "More tools don't always lead to better outcomes." "Make sure each tool you build has a clear, distinct purpose." OpenAI: "The issue isn't solely the number of tools, but their similarity or overlap. Some implementations successfully manage more than 15 well-defined, distinct tools while others struggle with fewer than 10 overlapping tools."
Source: Writing effective tools for agents (Sep 11, 2025); OpenAI practical guide p.16.
Review question: Do any two tools overlap enough that a human could not say which to call?

**11. Tool descriptions and schemas are prompts; test them with realistic, verifiable tasks.**
Reasoning: "Even small refinements to tool descriptions can yield dramatic improvements." Evaluation prompts should be "paired with a verifiable response or outcome", run programmatically. SWE-agent shows that interface design for the agent changes results ("a custom agent-computer interface (ACI) significantly enhances an agent's ability"). Anthropic multi-agent post: "Bad tool descriptions can send agents down completely wrong paths."
Source: Writing effective tools for agents (Sep 11, 2025); SWE-agent, https://arxiv.org/abs/2405.15793 (v3, 11 Nov 2024); How we built our multi-agent research system, https://www.anthropic.com/engineering/multi-agent-research-system, Jun 13, 2025.
Review question: Is there a tool-level eval set, and was the last description change measured?

**12. Cap and shape tool output.**
Reasoning: "For Claude Code, we restrict tool responses to 25,000 tokens by default." Responses should "prioritize contextual relevance over flexibility, and eschew low-level technical identifiers"; a concise response format excludes IDs.
Source: Writing effective tools for agents (Sep 11, 2025).
Review question: What happens when a tool returns 1 MB, and what does the model see?

**13. Rate each tool's risk and tie approval to the rating.**
Reasoning: OpenAI: "Assess the risk of each tool ... by assigning a rating (low, medium, or high) based on factors like read-only vs. write access, reversibility, required account permissions, and financial impact", then trigger guardrail checks or human escalation.
Source: OpenAI practical guide p.26 ("Tool safeguards" row of the guardrail types table).
Review question: Does every tool declare read-only, reversible and destructive, and does the default for an undeclared tool assume the worst?

**14. For large tool sets, load definitions on demand or let the agent call tools through code.**
Reasoning: "Tool descriptions occupy more context window space, increasing response time and costs." Anthropic's worked example cuts 150,000 tokens to 2,000 ("a time and cost saving of 98.7%"), but "code execution introduces its own complexity" (sandbox, monitoring). Treat 98.7% as a vendor example for one workflow, not a general rate.
Source: Code execution with MCP, https://www.anthropic.com/engineering/code-execution-with-mcp, Nov 4, 2025 (98.7% also checked in page meta).
Review question: What fraction of the prompt is tool schemas, and is there a lazy-load path above a threshold?

## Group 4. Context

**15. Treat context as a finite budget; aim for the smallest set of high-signal tokens.**
Reasoning: "Context, therefore, must be treated as a finite resource with diminishing marginal returns." Levers: compaction ("the first lever"), structured note-taking outside the window, just-in-time retrieval, sub-agent isolation. Cognition adds "Context Rot ... models making less intelligent decisions at longer and longer context lengths."
Source: Effective context engineering for AI agents, https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents, Sep 29, 2025; Multi-Agents: What's Actually Working, https://cognition.com/blog/multi-agents-working, 2026-04-22.
Review question: What are the context-reduction steps in order of cost, and what is re-injected after the summary?

**16. Own the context window and the prompts.**
Reasoning: 12-factor: "At any given point, your input to an LLM in an agent is 'here's what's happened so far, what's the next step'. Everything is context engineering." Factor 8: build your own control structures (compaction, summarization, human breakouts, tracing).
Source: 12-factor agents factors 3 and 8 (no date on page; README says April 2025 per search).
Review question: Can you print exactly what the model saw at step N?

**17. Sub-agents are first of all a context-isolation device.**
Reasoning: SDK docs: "intermediate tool calls and results stay inside the subagent; only its final message returns to the parent", and the only parent-to-child channel is the prompt string. Anthropic lists "context pollution" as one of three valid reasons for multiple agents.
Source: Subagents in the SDK, https://code.claude.com/docs/en/agent-sdk/subagents, no date on page; When to use multi-agent systems (and when not to), https://claude.com/resources/articles/building-multi-agent-systems-when-and-how-to-use-them, Jan 23, 2026.
Review question: Is the sub-agent returning a compact result, and does its prompt contain every fact it needs?

**18. A delegation brief states objective, output format, tool guidance and boundaries.**
Reasoning: "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries. Without detailed task descriptions, agents duplicate work, leave gaps, or fail." Early short instructions like "research the semiconductor shortage" failed.
Source: How we built our multi-agent research system (Jun 13, 2025).
Review question: Does the delegation template have fields for objective, output format, allowed tools, scope and done-criteria?

## Group 5. Multi-agent orchestration

**19. Default to one agent; add agents only for context pollution, parallelism or specialization.**
Reasoning: Anthropic (Jan 2026): "three situations where multiple agents consistently outperform a single agent: when context pollution degrades performance, when tasks can run in parallel, and when specialization improves tool selection or task focus." "multi-agent implementations typically use 3-10x more tokens than single-agent approaches." Newer (Oct 22, 2026): "a single agent with skills frequently outperformed both the one-prompt-for-everything design and the subagent design on quality, and often at a lower cost and latency per task." OpenAI: "maximize a single agent's capabilities first."
Source: When to use multi-agent systems (Jan 23, 2026); Building agents: When to fold subagents into your main agent loop, https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop, Oct 22, 2026; OpenAI practical guide p.16. The Oct 2026 post supersedes the more favourable framing in the Jun 2025 research-system post for general use.
Review question: Which of the three conditions justifies each sub-agent, and was a single-agent-with-skills variant evaluated?

**20. DISAGREEMENT: do parallel multi-agent systems work? Resolve by read-versus-write.**
- Pro: Anthropic's research system, an Opus 4 lead with Sonnet 4 workers, "outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval"; "token usage by itself explains 80% of the variance" in BrowseComp; agents use about 4x and multi-agent about 15x the tokens of chat. (Jun 13, 2025.)
- Con: Cognition: "running multiple agents in collaboration only results in fragile systems" because "actions carry implicit decisions, and conflicting decisions carry bad results"; rule such designs out by default. (Jun 12, 2025.)
- Update from Cognition (2026-04-22): "Our original observations still hold today for parallel-writer swarms", but "multi-agent systems work best today when writes stay single-threaded and the additional agents contribute intelligence rather than actions."
- Reconciliation: LangChain (Jun 16, 2025): "Multi-agent systems that primarily 'read' are easier than those that 'write'." Anthropic itself says "most coding tasks involve fewer truly parallelizable tasks than research" and tasks needing shared context "are not a good fit." Google Research (Jan 28, 2026), 180 configurations: centralized coordination gave +80.9% on a parallelizable finance task, while on a sequential planning task "every multi-agent variant we tested degraded performance by 39-70%."
- Not resolved: the Anthropic and Cognition numbers come from different tasks and are not comparable.
Source: https://www.anthropic.com/engineering/multi-agent-research-system ; https://cognition.com/blog/dont-build-multi-agents ; https://cognition.com/blog/multi-agents-working ; https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems ; https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/ .
Review question: Which agents can write, and is there exactly one writer per set of files? Are parallel agents read-only?

**21. Fan-out on independent reads; keep writes serial; give the orchestrator effort rules.**
Reasoning: Early orchestrators "spawn[ed] 50 subagents for simple queries"; the fix was scaling rules in the prompt (1 agent with 3-10 calls for simple fact-finding, 2-4 subagents with 10-15 calls for comparisons, 10+ for complex research).
Source: Multi-agent research system (Jun 13, 2025). SDK docs add a depth cap: `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` default 3 (subagents page).
Review question: Is there a spawn cap, a depth cap, and effort guidance in the orchestrator prompt?

**22. Pass results by reference when fidelity matters; beware the orchestrator bottleneck.**
Reasoning: "Subagent output to a filesystem to minimize the 'game of telephone.'" Also, in orchestrator-subagent "the orchestrator becomes an information bottleneck."
Source: Multi-agent research system (Jun 13, 2025); Multi-agent coordination patterns, https://claude.com/resources/articles/multi-agent-coordination-patterns, Apr 10, 2026.
Review question: Do large intermediate results go to files with a reference returned, rather than through the orchestrator's context?

**23. Split work by the context each piece needs, not by job title.**
Reasoning: "give each subagent a piece of work that needs little from the rest of the system and have it hand back a compact result"; splitting by problem type is the org-chart trap.
Source: Building agents: When to fold subagents ... (Oct 22, 2026).
Review question: Would two of your sub-agents need to read the same files to do their jobs?

**24. Prefer centralized coordination with verification over free-form peer networks.**
Reasoning: Across 260 configurations, "architectures without centralized verification tend to propagate errors more than those with centralized coordination"; "coordination yields diminishing returns once single-agent baselines exceed certain performance"; tool-heavy tasks incur multi-agent overhead. Cognition (2026): "unstructured swarms ... mostly a distraction"; the practical shape is "map-reduce-and-manage." I read only the abstract of the arXiv paper and the Google blog.
Source: Towards a Science of Scaling Agent Systems, https://arxiv.org/abs/2512.08296 (v3, 8 Apr 2026); Cognition, Multi-Agents: What's Actually Working (2026-04-22).
Review question: Is there a single coordinator that checks results, or do agents trust each other's output?

**25. Handoffs: validate arguments before side effects, filter history, remember guardrail scope.**
Reasoning: OpenAI Agents SDK: `is_enabled` "cannot authorize values inside an argument-bearing handoff"; check parsed fields "at the start of `on_handoff`, before any application side effects." The receiving agent sees the history unless an `input_filter` changes it. Input guardrails "run only for the first agent in the chain"; output guardrails only for the final agent; use tool guardrails across handoffs.
Source: Handoffs, https://openai.github.io/openai-agents-python/handoffs/ and Guardrails, https://openai.github.io/openai-agents-python/guardrails/ (no dates on pages).
Review question: In a multi-hop flow, which guardrail runs on the middle agents, and what does the receiving agent see?

**26. Delegation needs verifiable sub-tasks, least privilege and a reason to refuse.**
Reasoning: Google (Aug 22, 2026), from the DeepMind paper: "Agents should intelligently break down work into tasks that can be reliably verified" (contract-first decomposition); an orchestrator should "grant the absolute minimum permissions required"; long delegation chains let a "broad zone of indifference" pass harmful tasks along.
Source: How agents can delegate better, https://cloud.google.com/blog/products/ai-machine-learning/how-agents-can-delegate-better, Aug 22, 2026; Intelligent AI Delegation, https://arxiv.org/abs/2602.11865, 12 Feb 2026 (abstract only).
Review question: For each delegated task, what check proves it was done, and which credentials does the child inherit?

**27. Know the failure taxonomy and test against it.**
Reasoning: MAST: 14 failure modes in 3 categories (system design issues, inter-agent misalignment, task verification), from 1600+ annotated traces across 7 frameworks; authors report many failures come from system design, not only model limits. I read the abstract only.
Source: Why Do Multi-Agent LLM Systems Fail?, https://arxiv.org/abs/2503.13657, v1 17 Mar 2025, v3 26 Oct 2025.
Review question: Do you review failing traces against these three categories, and which category dominates your failures?

**28. Interop across vendors: discover capabilities, track a task lifecycle.**
Reasoning: A2A uses an "Agent Card" for capability discovery and a task object with a lifecycle, and "complements" MCP (tools and context). I did not evaluate adoption or security of A2A.
Source: Announcing the Agent2Agent Protocol, https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/, Apr 9, 2025.
THIN: one announcement post only.
Review question: If agents cross a trust boundary, how does the caller learn what the callee can do, and where is the task state kept?

## Group 6. Verification and evals

**29. Judge with a different agent than the one that did the work.**
Reasoning: "agents tend to respond by confidently praising the work"; "tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work." Cognition: a reviewer with clean context "is forced to reason backward from the implementation without the spec."
Source: Harness design for long-running apps (Mar 24, 2026); Multi-Agents: What's Actually Working (2026-04-22).
Code seen: OMH-4 (judge is not the builder).
Review question: Is the evaluator a separate context with no access to the builder's reasoning, and can the builder override its verdict?

**30. A verifier is only as good as its criteria, and it needs an iteration cap.**
Reasoning: "A verifier told only to check whether output is good, with no further criteria, will rubber-stamp"; "A maximum iteration limit with a fallback strategy (escalate to a human, return the best attempt with caveats) prevents this from becoming an infinite loop."
Source: Multi-agent coordination patterns (Apr 10, 2026).
Review question: Are the verification criteria written down, executable where possible, and is there a loop limit?

**31. Grade what was produced, not the path taken.**
Reasoning: Checking exact tool-call sequences is "too rigid"; "it's often better to grade what the agent produced, not the path it took." A good task is one where "two domain experts would independently reach the same pass/fail verdict." Everything a grader checks must be in the task text.
Source: Demystifying evals for AI agents, https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents, Jan 9, 2026.
Code seen: OMH-1, OMH-5 (typed exit-code receipts instead of prose claims).
Review question: Do graders check final state (tests, files, DB), and could two reviewers disagree on a task's pass/fail?

**32. Use deterministic graders where possible, calibrated model graders elsewhere, and measure reliability, not just luck.**
Reasoning: Three grader types (code, model, human); model graders need calibration against humans and a way out ("Unknown"). `pass@k` rises with k while `pass^k` falls: at 75% per trial, three trials all pass about 42%; `pass^k` matters for customer-facing agents. Each trial should start from a clean environment.
Source: Demystifying evals (Jan 9, 2026).
Review question: Is the headline metric pass@1, pass@k or pass^k, and does it match how users experience failure?

**33. Read the transcripts before trusting a score.**
Reasoning: "we do not take eval scores at face value until someone digs into the details of the eval and reads some transcripts." Regression evals "should have a nearly 100% pass rate."
Source: Demystifying evals (Jan 9, 2026).
Review question: When did a human last read ten failing and ten passing transcripts, and was a grader fixed as a result?

**34. Start evals early with a few real cases.**
Reasoning: "A prompt tweak might boost success rates from 30% to 80%. With effect sizes this large, you can spot changes with just a few test cases"; the team began with about 20 queries and an LLM judge with a rubric (accuracy, citation accuracy, completeness, source quality, tool efficiency). In the Oct 2026 fold post, "Even a set of 10 golden examples is enough to start."
Source: Multi-agent research system (Jun 13, 2025); Building agents: When to fold subagents ... (Oct 22, 2026).
Review question: Is there an eval set checked into the repo, and does CI run it on every prompt or tool change?

**35. Do not let the loop weaken its own judge.**
Reasoning: Anthropic's harness rule forbids editing tests to pass; OMH makes it mechanical with a fence of files and a git-diff check (OMH-4). The lab source for the rule is the harness post; the fence mechanism is OMH's own, not a lab publication.
Source: Effective harnesses for long-running agents (Nov 26, 2025).
Review question: Which files define "pass", and what fails the run if the agent changes them?

**36. Report capability claims with their success threshold.**
Reasoning: METR defines the "50%-task-completion time horizon" (human time for tasks a model completes with 50% success); the v4 abstract says frontier horizons doubled about every seven months since 2019 and that growth is "primarily driven by greater reliability and ability to adapt to mistakes, combined with better logical reasoning and tool use." The measure is software tasks with a stated external-validity caveat.
Source: Measuring AI Ability to Complete Long Software Tasks, https://arxiv.org/abs/2503.14499, v1 18 Mar 2025, v4 10 Jul 2026 (abstract only).
THIN: I did not read METR's newer posts or the 80% horizon figures; do not quote them from this file.
Review question: When a design doc says "the agent can run for N hours", does it state at what success rate and on what task type?

## Group 7. Safety and permissions

**37. Layer defenses; no model-level defense is enough alone.**
Reasoning: Anthropic (May 25, 2026): on Gray Swan's benchmark Opus 4.7 holds attack success "to roughly 0.1% on single attempts, and around 5-6% after 100 adaptive attempts"; "protection in the model layer will never be 100% effective." Browser post (Nov 24, 2025): "A 1% attack success rate ... still represents meaningful risk." OpenAI: use layered guardrails, "a single one is unlikely to provide sufficient protection."
Source: How we contain Claude across products, https://www.anthropic.com/engineering/how-we-contain-claude, May 25, 2026; Mitigating prompt injections in browser use, https://www.anthropic.com/research/prompt-injection-defenses, Nov 24, 2025; OpenAI practical guide p.25.
Review question: If the model fully obeyed an injected instruction, what would stop the damage?

**38. Never give one agent private data, untrusted input and an outbound channel together.**
Reasoning: Willison's "lethal trifecta": "If your agent combines these three features, an attacker can easily trick it into accessing your private data and sending it to that attacker." Filters do not save you: "The only way to stay safe there is to avoid that lethal trifecta combination entirely."
Source: The lethal trifecta for AI agents, https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/, Jun 16, 2025.
Review question: For each agent, tick which of the three it holds; if all three, what removes one?

**39. Contain the agent's reach instead of only supervising its actions.**
Reasoning: "Rather than supervising what the agent does, we supervise what it's able to do ... sandboxes, virtual machines, and egress controls"; "if credentials never enter the sandbox, they can't be exfiltrated." Approval prompts decay: users hit "approval fatigue."
Source: How we contain Claude across products (May 25, 2026); auto mode post (Mar 25, 2026); Managed Agents (Apr 8, 2026: tokens "never reachable from the sandbox where Claude's generated code runs", proxy fetches credentials from a vault).
Review question: Which secrets are readable from the process that runs model-generated code?

**40. Make the permission order deterministic and let deny win.**
Reasoning: SDK docs: hooks, then deny rules, ask rules, mode, allow rules, callback. "A hook that returns allow doesn't skip the deny-rule and ask-rule steps"; deny applies "even in bypassPermissions mode"; with several hooks "the most restrictive result applies."
Source: Configure permissions, https://platform.claude.com/docs/en/agent-sdk/permissions, no date; Intercept and control agent behavior with hooks, https://code.claude.com/docs/en/agent-sdk/hooks, no date.
Review question: Can any hook, mode or callback turn a deny into an allow?

**41. If a classifier replaces a human, publish its error rates and fail safe.**
Reasoning: Auto mode: false-positive rate 0.4%, false-negative rate 17% on real overeager actions ("the honest number"); "A false positive costs a single retry" because denials return as tool results with an instruction to find a safer path; repeated denials escalate. "It is not a drop-in replacement for careful human review."
Source: How we built Claude Code auto mode (Mar 25, 2026).
Review question: What are the measured FPR and FNR of the approval classifier, and what happens after N denials?

**42. Plan for human intervention on failure thresholds and high-risk actions.**
Reasoning: OpenAI: escalate on "Exceeding failure thresholds" and "High-risk actions: ... sensitive, irreversible, or have high stakes should trigger human oversight until confidence in the agent's reliability grows."
Source: OpenAI practical guide p.31.
Code seen: OMH-9 (spend gate stops in non-interactive runs).
Review question: Which actions require a human, and what does the agent do in a headless run where no human is present?

**43. Where guarantees are needed, separate control flow from untrusted data by design.**
Reasoning: CaMeL extracts control and data flow from the trusted query "therefore, the untrusted data retrieved by the LLM can never impact the program flow", and uses capabilities to block exfiltration. Cost: "77% of tasks with provable security (compared to 84% with an undefended system)" in AgentDojo (v2 abstract; v1 reported 67%).
Source: Defeating Prompt Injections by Design, https://arxiv.org/abs/2503.18813, v1 24 Mar 2025, v2 24 Jun 2025 (abstract only).
Review question: Can untrusted text ever choose which tool runs or with which arguments, or only fill data slots?

**44. Treat project open, config load and local listeners as inbound requests.**
Reasoning: Three reported Claude Code vulnerabilities ran code before the user accepted the trust prompt; the fix was to defer parsing and executing project-local config until after consent.
Source: How we contain Claude across products (May 25, 2026).
Review question: Does the agent execute anything from a cloned repo or config file before the user trusts it?

## Group 8. Observability

THIN: only two opened sources speak to this directly.

**45. Trace agent decisions in production, not only errors.**
Reasoning: Users reported agents "not finding obvious information" with no visible cause; "Adding full production tracing let us diagnose why agents failed." Anthropic monitors "agent decision patterns and interaction structures-all without monitoring the contents of individual conversations" (dash normalized). Stateful agents need coordinated deploys ("rainbow deployments").
Source: Multi-agent research system (Jun 13, 2025).
Review question: For a failed run, can you list each tool call, its arguments and the reason the loop continued, without reproducing the run?

**46. Keep an append-only session record that is interrogable.**
Reasoning: Managed Agents' session log is the durable record outside the harness; in the older coupled design, failures from the harness, the event stream or the container "all presented the same."
Source: Managed Agents (Apr 8, 2026).
Review question: Can you tell a harness bug from a tool failure from a network drop in your logs?

## Group 9. Cost

**47. Tokens are the cost and, partly, the quality driver; price the multiplier.**
Reasoning: "In our data, agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats"; "token usage by itself explains 80% of the variance" in one BrowseComp analysis. Anthropic (Jan 2026) reports 3-10x for multi-agent versus single-agent. Economic viability requires tasks "where the value ... is high enough."
Source: Multi-agent research system (Jun 13, 2025); When to use multi-agent systems (Jan 23, 2026).
Review question: What is the token cost per completed task, and is it below the value of the task?

**48. Establish quality with the strongest model, then step down where evals hold.**
Reasoning: OpenAI: "build your agent prototype with the most capable model for every task to establish a performance baseline. From there, try swapping in smaller models." Google (Aug 2026): match each task to the right model to achieve reliability "at a minimum cost."
Source: OpenAI practical guide p.8; How agents can delegate better (Aug 22, 2026).
Code seen: OMH-3 (category to model chains).
Review question: Which roles run on cheaper models, and which eval proves no quality loss?

**49. Budget output, not only input.**
Reasoning: Tool responses are capped (25,000 tokens by default in Claude Code); intermediate results can stay in the execution environment instead of the context (code-execution post: "intermediate results stay in the execution environment by default").
Source: Writing effective tools for agents (Sep 11, 2025); Code execution with MCP (Nov 4, 2025).
Review question: Where is output size bounded per tool, per turn and per run?

## What is not covered by any opened lab source
- Prompt-cache design (stable prefix, boundary marker): only seen in code ( fork). No lab page opened states it as a principle.
- OpenAI "Harness engineering" post (Feb 2026 per third parties) and the OpenAI April 2026 Agents SDK post: blocked (HTTP 403), NOT READ.
- Google "Agents" and "Agents Companion" whitepapers: Kaggle page not readable, NOT READ.

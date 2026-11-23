# oh-my-hermes (OMH): orchestration patterns

Source read: `rlaope/oh-my-hermes`, shallow clone of default branch (HEAD dated 2026-11-13), about 5,000 files. Paths are relative to repo root. I read `README.md`, `CLAUDE.md`, `AGENTS.md`, `docs/ARCHITECTURE.md` (2,967 lines, skimmed headings and the sections cited), `roles/*.md`, selected `agent-skills/*/SKILL.md` and references, and the headers/docstrings of selected `src/coding/*.py` and `src/routing/*.py`. The code base is far too large to read fully: claims below are limited to what those files state. Caveat: this is a project's own description of its design (docstrings and skill text); I did not run it, so behavior claims are "documented", not "observed".

What it is (README.md, CLAUDE.md:14-20): a wrapper layer next to "Hermes Agent". Core `omh` is pure Python, zero runtime deps, "makes no LLM, API, or network call"; it produces deterministic contracts, routing and prepared handoffs, and other executors (Codex, Claude Code, Hermes children) do the work. Explicit exceptions are listed in CLAUDE.md:22-70.

## 1. The prepared-versus-observed evidence boundary (the central idea)

- How: every artifact is labelled `prepared_not_observed` until a separate runtime record exists. Roles, plans, handoffs, loop ticks and memory recall are "prepared guidance only. It is not worker dispatch, tool execution, ... review, CI, merge-readiness, or merge evidence" (every `roles/*.md`, "OMH Role Context"). A done claim needs an observed record.
- Where: `docs/ARCHITECTURE.md:24` (memory as prepared context) and `AGENTS.md:206` ("Preserve prepared versus observed boundaries"); `roles/reviewer.md` ("Review findings are not fix evidence; merge-ready is not merged"); `agent-skills/ulw-loop/SKILL.md` ("queued loop ticks alone are not observed work"; "Treat a judge `done` verdict ... as narration; completion still requires the linked goal ledger completion gate and observed evidence"); `AGENTS.md:263-281` ("A number without those is `prepared_not_observed`, not a result").
- Strongest code form: `src/coding/handoff_contract.py:1-30`. A handoff carries typed `inputs[]`, `postconditions[]` compiled into runnable verification commands, `output_shape`, and `forbidden_actions[]` rendered into the executor prompt. A receipt accepts "an integer exit status per declared postcondition and nothing else, so a claim such as 'tests passed' has no field to land in"; only the receipt promotes the contract from `prepared_not_observed` to `observed`.
- When to use: any orchestrator where a planner/LLM can narrate success. Make the "done" field machine-typed (exit codes), not prose. When not: one-shot chat tasks; the schema overhead is large (OMH uses versioned schema names like `handoff_contract/v1` everywhere).

## 2. Roles as responsibility descriptors, not agents

- How: `roles/` has nine files (builder, guide, handoff-guide, memory-keeper, operator, planner, researcher, reviewer, tracker). Each says "This OMH role is a responsibility descriptor, not a runtime agent" and lists: Owns, Primary Skills, Primary Harnesses, Wrapper Actions, and an Evidence Boundary. Example: planner owns clarification, non-goals, acceptance criteria, "loopability", verification strategy, and "A planner role can make work reviewable; it is not proof that the work was accepted or executed" (roles/planner.md). Builder: "A builder role label is not hidden coding execution" (roles/builder.md).
- Delegation first: Hermes plans and narrates; the selected executor does main implementation (`docs/ARCHITECTURE.md:26-27`). Builder/handoff-guide roles require showing the composed delegate prompt in a fenced block, truncated to a bounded preview (roles/builder.md, roles/handoff-guide.md).
- When to use: when many surfaces (chat, CLI, desktop) need the same ownership vocabulary. When not: if you only need two agents, an explicit prompt per agent is simpler.

## 3. Deterministic routing of requests to skills, conservative on low confidence

- How: `src/routing/` (about 35k lines, `policy.py` 10,740 and `recommend.py` 6,610) turns a message into a skill recommendation without an LLM. `src/routing/query.py:1-12` builds named text stages (raw, executable text with quoted regions removed, scrubbed diagnostic text, ...) so scorers read the right stage and quoted text does not trigger a route. Skills declare "Strong routing signals" and "Do Not Use When" lists that name the adjacent skill to use instead (e.g. `agent-skills/omh-verification-gate/SKILL.md` "Do Not Use When"). When unsure the router is told to "Route conservatively and show the missing decision before claiming work started" / "ask one focused question when confidence is low" (src/routing/recommend.py:1162, 2571).
- Model routing by work category: `src/coding/model_routing.py:323-345` defines categories (`ultrabrain`, `deep`, `architect`, `unspecified-high`, `unspecified-low`, `quick`, `writing`, `visual-engineering`, `artistry`, `review` ...). `CATEGORY_ROLE_SOURCES` (line ~388) maps a role to an ordered chain: brain -> (ultrabrain, deep, unspecified-low); implementation -> (unspecified-high, unspecified-low); research -> (unspecified-low, quick); docs -> (writing, quick). Comments: planning "heads on the deepest tier" because "mistakes every later unit inherits"; the chain ends with a different model so a fallback "names a DIFFERENT model rather than repeating the head at a weaker effort"; "reviewer-vs-author separation is advisory handoff text, not a catalog property" (so it is not enforced by the router). Operator can override via `~/.omh/routing/category-maestro.json` (model_routing.py:171). Mirrors the strongest-plans, cheapest-searches split.
- When to use: a catalog of 100+ skills where prompt-only selection gets noisy. When not: small skill sets; an LLM description match is enough and the 35k-line router is a maintenance cost.

## 4. Loops with a fence, an external judge and a measurable finish line

- Files: `agent-skills/ulw-loop/SKILL.md` (194 lines), `references/loop-design-review.md`, `references/measured-loop-discipline.md`, `references/goal-constraint-discipline.md`.
- How: before launch, write a finish line (one command whose exit status or output-vs-expected-file decides the goal), a fence (paths the loop may not edit: tests, fixtures, check scripts, gate configs), and name a judge that is not the builder. "A finish line with no fence is incomplete, because the cheapest route to a passing check is a weaker check: a removed or skipped test, a looser assertion, a mock that hides the failure..." (loop-design-review.md). The judge reruns the acceptance check itself and runs a git-based fence check (`git diff --no-renames --name-status <start-sha>`, untracked-file listing, sha256 for non-tracked entries); the iteration fails if any fence step fails "whatever the acceptance check returned". A diff review can fail an iteration; it "never passes an iteration whose deterministic check failed". Prefer a finish line compared against something the loop did not write.
- Measured loops: declare the evaluation command and metric and forbid editing the scoring harness; run attempt, commit, measure, keep or reset; append one TSV line per cycle; on an equal metric keep the simpler change; log long runs to a file and pull only metric/error lines into context (ulw-loop SKILL.md quality bar).
- Failure modes named as warnings before progress advances: `verification_gap`, `comprehension_debt`, `cognitive_surrender`. Stuck loops: `replan_stuck_loop_once` re-plans once from the goal ledger and recorded failures alone, not the transcript; a second stop names the blocker.
- Mid-run user messages are interjections, not stops; follow-ups needing new authority are described first and started only on approval; "persistence never broadens the authorized scope".
- When to use: long-horizon goals with an objective check. When not: bounded one-shot tasks (the skill itself says to use a delivery workflow for "one bounded delivery cycle").

## 5. Verification gate: PASS / HOLD / BLOCK with freshness and regression witness

- Where: `agent-skills/omh-verification-gate/SKILL.md` (140 lines). Prepares `verification_matrix/v1`, records `observed_check_results/v1`, issues PASS/HOLD/BLOCK with missing evidence. Bad example in the skill: "tests not run but say it's ready" must return HOLD/BLOCK. Recovery rules: a fix test with only a green result is HOLD with `regression_witness_missing` (a pre-fix red witness is required); a generated file with no known regeneration command is unresolved and needs provenance; results carry "scope and freshness".
- When to use: before merge or release claims. When not: visual render QA (routed to `omh-visual-qa`).

## 6. Adversarial consensus before planning

- Where: `agent-skills/omh-adversarial-consensus/SKILL.md`. 3-5 perspectives with distinct angles; round one blind; one attack-only cross-round (no self-defense); each objection ends defended, refined or conceded, and conceded findings are struck, not softened; output limited to four buckets (Hard Constraints, Decisions, Risks, Open Questions) and handed to `ulw-plan` as input, never emitted as a plan. A perspective that could not be kept blind is named as a broken-independence caveat. Not for small local changes ("One perspective would do").
- When to use: contested, hard-to-reverse pre-plan decisions. When not: routine tasks (cost of 3+ rounds).

## 7. Fanout: confinement, isolation, retry and review budget

- `src/coding/fanout_*.py` (28 files) and `isolation.py`: worktree session isolation (`worktree_session_isolation/v1`, high-risk terms like migration, refactor, security trigger it), filesystem confinement of the child process via a sandbox (`fanout_confinement.py`, imports `trusted_bwrap`), a durable journal, capacity/admission control, and a per-attempt review budget (`fanout_review_budget.py`).
- Retry policy is mechanical (`src/coding/fanout_retry.py:1-15`): retry only transient transport failures (rate limit, 5xx, socket reset); a nonzero exit from a real test is "the unit's answer" and re-running "would only produce the same answer more slowly"; even a transient failure is not replayed once the unit produced an observed side effect (files written, result artifact): it is continued or recovered by hand, because a re-dispatch rebuilds the worktree and destroys the work.
- When to use: parallel code-writing agents. When not: single-agent work.

## 8. Reviewed project memory as prepared context

- Where: `docs/ARCHITECTURE.md:344-355`, `AGENTS.md:211`, `agent-skills/omh-memory-new`, `roles/memory-keeper.md`. Memory lives under `.omh/memory/` as local JSON: candidates, reviewed records, review decisions and recall packs (`project_memory_recall_pack/v1`). Policy modes `off`, `review-first`, `auto-safe` (default auto-safe). Memory recall is "prepared context, not execution evidence", so a remembered fact can never stand as proof that something was done.
- Related: `agent-skills/omh-instinct-ledger`, `omh-decision-recall`, codegraph (`docs/CODEGRAPH.md`, "prepared context, never execution ... evidence", AGENTS.md:257-261).
- When to use: cross-session knowledge with human review. When not: if recall may silently overwrite current facts; always re-check against the source.

## 9. Gates for irreversible side effects (spend gate)

- Where: `agent-skills/omh-spend-gate/SKILL.md`. Before any payment surface: confirm a person can answer in this session; in scheduled, webhook, background or subagent runs "prepare the card and stop before any payment surface"; read the quote from its source, show `pre_spend_card/v1` with a cap, wait for a typed yes, report done only with the receipt and amount. Same shape as a blast-radius gate.
- When to use: money, sends, deletes. When not: reversible local edits.

## 10. Honest self-reporting of numbers

- Where: `AGENTS.md:263-281`. Every rate uses `omh_reported_rate/v1` (`src/quality/reported_rate.py`): numerator buckets, what the denominator counted, excluded classes; empty denominator is `percent: null` with basis `no_observations`, not 0%; a headline number in a PR must name arm, corpus, selection rule and artifact.
- When to use: any eval or dashboard an agent writes. 

## 11. Skill catalog as the unit of capability

- `agent-skills/` holds 123 `omh-*`/`ulw-*` skills (ls count), each with fixed sections: Why This Exists, Do Not Use When, Good/Bad example, Completion Checklist, Recovery Notes, Quality bar, Required inputs / Expected outputs (versioned schemas). Skills are generated from catalog data (`docs/ARCHITECTURE.md:25` "generated skill text from testable catalog data"; `docs/ADDING-A-SKILL.md`). Worth copying: a "Do Not Use When" that points to the right neighbor, and a "Bad example" with the expected refusal.

## Risks and criticism (from reading, not from the repo)
- Very large surface (routing 35k lines, 123 skills, 2.9k-line architecture doc): hard to audit; the project's own claims of determinism rest on its tests, which I did not run.
- Several guarantees are "advisory text" by its own admission (reviewer-vs-author separation, model_routing.py comment).
- Role files are metadata; real work is delegated to external CLIs whose behavior OMH can only observe through receipts.

## Review questions this file supports
- Is "done" a typed field fed by exit codes, or free text from the agent?
- Does a loop have a written finish line, a fenced set of files the loop may not touch, and a judge other than the builder?
- Are retries limited to transient transport errors, and blocked once a unit has produced side effects?
- Does a fix come with a pre-fix red witness?
- Do skills say what NOT to use them for and name the neighbor?

# Source index: security, MCP, regulation, approval UX

Companion to sources.md. Date rule: the date printed on the page; "no date on page" when none was shown. READ = I opened it (WebFetch answers through a summarizer; where noted I also got the raw text by curl or pdftotext). NOT READ = not opened or blocked. I did not bypass any block (HTTP 403 or empty page).

Correction to sources.md: it says the "users approve about 93% of permission prompts" claim was not found in the auto-mode post. Raw HTML grep (curl) found it in two posts, see the two Anthropic lines below. sources.md was not edited.

## MCP specification (revision 2026-07-28, newest I found)
- https://modelcontextprotocol.io/specification | no date on page, links to revision 2026-07-28 | READ | newest revision, security principles, MUST and SHOULD wording at overview level.
- https://modelcontextprotocol.io/specification/2026-07-28/changelog.md | no date on page | READ | what changed: sessions removed, DCR deprecated, MRTR, iss validation.
- https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization.md | no date on page | READ (markdown, raw) | OAuth 2.1 resource server, PRM, resource parameter, token audience, scope step-up, error codes.
- https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/client-registration.md | no date on page | READ | CIMD vs pre-registration vs DCR priority and MUST rules.
- https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices.md | no date on page | READ | confused deputy, token passthrough, SSRF, state handle hijacking, local server compromise, scope minimization.
- https://modelcontextprotocol.io/specification/2026-07-28/server/tools.md | no date on page | READ | human in the loop SHOULD, annotations untrusted, outputSchema MUST and SHOULD, tool errors, tool security list.
- https://modelcontextprotocol.io/specification/2026-07-28/schema.md | no date on page | READ in part (curl and grep of the ToolAnnotations section only) | exact annotation hint definitions and defaults.
- https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation.md | no date on page | READ | form vs URL mode, no secrets in form mode, identity binding.
- https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http.md | no date on page | READ | Origin validation, localhost binding, no sessions, request headers.
- https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations.md and .../authorization-server-discovery.md | NOT READ (linked from the authorization page only).
- Search summaries on the revision (descope, workos, aembit, ssojet blogs) | NOT READ; only used to learn the release date (28 July 2026, release candidate 21 May 2026), which is therefore unverified on a primary page.

## Prompt-injection defence by design
- https://arxiv.org/abs/2506.08837 (Beurer-Kellner et al., Design Patterns for Securing LLM Agents against Prompt Injections) | v1 10 June 2025, v3 27 June 2025 | READ (abstract page plus full PDF through pdftotext, sections 3.1 and 4.7) | six patterns, guiding principle, resume-ranking case study.
- https://arxiv.org/html/2503.18813 (CaMeL, Defeating Prompt Injections by Design) | v2 24 Jun 2025 | READ (full HTML by curl plus a summary; first 100000 characters in the summary) | P-LLM and Q-LLM, capabilities, policies, limits, fatigue. sources.md had the abstract only.
- https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ | 25 April 2023 (update of 11 April 2025 on page) | READ | dual LLM pattern and its stated limits.
- https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | Jun 16, 2025 | READ earlier (see sources.md); not reopened.
- https://ai.meta.com/blog/practical-ai-agent-security/ | October 31, 2025 | READ | Agents Rule of Two.
- https://arxiv.org/abs/2403.14720 (Microsoft, Defending Against Indirect Prompt Injection Attacks With Spotlighting) | submitted March 20, 2024 | READ (abstract page only; the delimiting, datamarking and encoding variants are not described there) | spotlighting idea and reported drop from above 50% to below 2%.
- https://blog.google/security/mitigating-prompt-injection-attacks/ | June 13, 2025 | READ | Gemini layered defence list.
- https://openai.com/index/designing-agents-to-resist-prompt-injection/ | March 11, 2026 per a search result | NOT READ (HTTP 403).
- https://www.anthropic.com/research/prompt-injection-defenses | Nov 24, 2025 | READ earlier (see sources.md); not reopened. Newer Anthropic prompt-injection numbers (system cards, Opus 4.8 and Opus 5) appeared only in search summaries: NOT READ.
- https://www.anthropic.com/engineering/how-we-contain-claude | May 25, 2026 | READ (curl raw HTML grep, passages on approvals) | 93% approval telemetry, 84% prompt reduction, experienced users.
- https://www.anthropic.com/engineering/claude-code-auto-mode | Mar 25, 2026 | READ (curl raw HTML grep) | "users accept 93% of them anyway", approval fatigue definition, "judge what the agent did".

## OWASP
- https://genai.owasp.org/llm-top-10/ | no specific date, 2025 edition | READ (list page, teaser text only) | names of LLM01 to LLM10.
- https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | no date on page | READ | definition, prevention headings, resume scenario 6.
- https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ | no date on page | READ | root causes, complete mediation, human approval.
- LLM02, LLM05, LLM08, LLM10 detail pages | NOT READ.
- https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/ | December 9, 2025 | READ (summarizer paraphrase of the ASI01 to ASI10 entries) | names of the ten agentic risks.
- https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ | December 9, 2025 | READ (landing page only, no list) | confirms publication date; full document NOT READ.

## EU AI Act and GDPR (unofficial reproductions of the law text)
- https://artificialintelligenceact.eu/annex/3/ | no date on page | READ | Annex III point 4 employment.
- https://artificialintelligenceact.eu/article/6/ | no date on page, shows 2 December 2027 for Annex III | READ | 6(3) derogation and profiling override, 6(4).
- https://artificialintelligenceact.eu/article/12/ | no date on page | READ | record-keeping; 12(3) is biometrics only.
- https://artificialintelligenceact.eu/article/13/ | no date on page | READ | transparency toward deployers.
- https://artificialintelligenceact.eu/article/14/ | no date on page | READ | human oversight, automation bias, override, stop button.
- https://artificialintelligenceact.eu/article/26/ | no date on page | READ | deployer duties: oversight staff, six month logs, informing persons.
- https://artificialintelligenceact.eu/article/86/ | no date on page; prints "Comes into force 2 August 2026" (conflicts with the 2027 date on other article pages) | READ | right to explanation.
- https://gdpr-info.eu/art-22-gdpr/ | no date on page | READ | Article 22(1) to (4).
- https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng and the OJ:L_202601744 HTML | NOT READ (empty page).
- Article 27, Article 4(4) GDPR, Article 50, Article 113 | NOT READ.

## Digital omnibus and commentary
- https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo | 27 July 2026 | READ (commentary) | Official Journal 24 July 2026, in force 27 July 2026, Annex III to 2 December 2027, Annex I to 2 August 2028, Article 4 and Article 50 notes.
- https://www.whitecase.com/insight-alert/eu-ai-omnibus-enters-force-amending-ai-act | NOT READ (HTTP 403).
- Gibson Dunn, Simmons, Freshfields, Winston Taylor, sota.io and other law-firm notes from search results | NOT READ; vote dates (Parliament 16 June 2026, Council 29 June 2026) and the number 2026/1744 come from these search summaries and are unverified.

## Dutch regulator
- https://api.eerstekamer.nl/9370000/1/j4nvi0xeni9vr2l_j9vvkfvj6b325az/vmvknkona3pd/f=/vmvknmp8mawk.pdf (Autoriteit Persoonsgegevens, Rapportage AI & Algoritmes Nederland, Editie 6) | Februari 2026 (printed on cover) | READ (full PDF via pdftotext; chapter 3 on recruiting) | AP position on recruiting AI, Article 22 AVG, meaningful human intervention. Note: hosted on the Eerste Kamer site; the AP's own page was not found.
- https://www.autoriteitpersoonsgegevens.nl/themas/algoritmes-ai | NOT READ (HTTP 403).
- AP guidance "Handvatten betekenisvolle menselijke tussenkomst" and the online-assessment guidance (reported as 18 March 2026 by recruitment blogs) | NOT READ.
- Dutch recruitment blogs (recruitmenttraining.pro, ondernemenmetpersoneel.nl, legiscope) | NOT READ (search summaries only); no claim from them is used.

## Approval behaviour
- https://scalex.dev/blog/ai-agent-permissions/ (Alex Wauters, Scale X) | May 27, 2026 | READ (summarizer; author states limits) | observational approve or deny game data, about 1 in 3 threats missed.
- https://www.theregister.com/a/5284236 | 6 August 2026 | READ (summarizer) | independent report of the same dataset, notes the game is malicious-heavy.
- Other search results on approval fatigue (workos, resilientcyber, tianpan, buildmvpfast, mer.vin, letsdatascience) | NOT READ.

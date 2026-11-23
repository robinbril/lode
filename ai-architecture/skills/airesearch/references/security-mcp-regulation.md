# Security, MCP, regulation and approval UX for LLM agents

Extends lab-principles.md (groups 3 and 7, numbers 10 to 14 and 37 to 44). Numbering here is S1, S2, ... Source index: sources-security.md.

Rules for reading this file
- Every principle rests on a page I opened (listed in sources-security.md). Quotes are verbatim from raw text (curl, pdftotext, or the MCP markdown pages) or from fragments the fetch tool itself put in quotation marks. Quotes are under 15 words. Where I only have a summarizer paraphrase, I say "paraphrase" and give no quote.
- Dashes inside quotes and headings were normalized to hyphens or commas; wording is otherwise verbatim.
- Tags: [STANDARD] OWASP community guidance, [SPEC] normative protocol text, [LAW TEXT] statute as reproduced on an unofficial site (EUR-Lex returned an empty page, NOT READ), [COMMENTARY] law firm or vendor reading, [PAPER] research, [LAB] vendor engineering post, [AUTHORITY] regulator report, [INFERENCE] my own step, labelled.
- `DISAGREEMENT:` marks conflicts. `THIN:` marks weak evidence. `OPEN:` marks unresolved facts.
- Review questions are yes/no and answerable by reading code or repo files.
- I am not a lawyer. Group S-C is a reading aid for engineers, not legal advice.

## What this file adds to the existing principles
- 13 (rate tool risk): S5, S29 add the MCP annotation defaults and the rule that annotations are hints.
- 37 and 39 (layering, containment, approval fatigue): S19 and S28 to S31 add the measured 93% over-approval figure and observational miss-rate data. Correction to sources.md: the 93% figure IS in the Anthropic posts (see sources-security.md).
- 38 (lethal trifecta): S13 adds Meta's Rule of Two, which says what to do when all three are needed.
- 43 (CaMeL): S14 and S15 add the six design patterns and a resume-ranking case study written for exactly this use case, plus the CaMeL limits from the full HTML.

## Group S-A. MCP specification, revision 2026-07-28

Revision note: the newest revision I found is 2026-07-28 (spec URL and changelog title). Its changelog says it removes protocol-level sessions, removes the initialize handshake, deprecates Dynamic Client Registration and moves server-initiated requests such as elicitation to multi round-trip results. The search summary (secondary) puts the release on 28 July 2026 after a May 21 release candidate; I did not verify the release date on a primary page. MUST means required for conformance, SHOULD means recommended; I keep the two apart below.

**S1. An MCP server accepts only tokens issued for itself and never forwards the caller's token.** [SPEC]
Rule: validate audience on every request; do not pass an inbound token to a downstream API.
Reasoning: MUST: servers validate that access tokens were issued specifically for them as audience. The spec says servers "MUST NOT accept or transit any other tokens." The security page calls the opposite "token passthrough", an anti-pattern that breaks audit trails and lets one stolen token reach other services. For the downstream CRM, the server needs its own credential, obtained separately.
Source: Authorization, https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization.md (no date on page, revision 2026-07-28); Security Best Practices, https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices.md (no date on page).
Review question: Does the server reject a bearer token whose audience or resource is not its own canonical URI, and is there no code path that copies the inbound Authorization header into an outbound request?

**S2. Authorization discovery and registration have fixed MUST and SHOULD levels.** [SPEC]
Rule: expose Protected Resource Metadata; prefer Client ID Metadata Documents over Dynamic Client Registration.
Reasoning: authorization itself is "OPTIONAL", and stdio servers should take credentials from the environment. When an HTTP server uses it: "MCP servers MUST implement OAuth 2.0 Protected Resource Metadata (RFC9728)"; clients MUST send the RFC 8707 `resource` parameter in authorization and token requests; access tokens MUST NOT go in the query string. CIMD is SHOULD for clients and authorization servers; DCR is MAY and the page says "Dynamic Client Registration is deprecated." Client priority order: pre-registered, then CIMD, then DCR. Clients MUST validate `iss` when present (RFC 9207) and key stored credentials by issuer.
Source: Authorization (above); Client Registration, https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/client-registration.md (no date on page); Changelog, https://modelcontextprotocol.io/specification/2026-07-28/changelog.md (no date on page).
Review question: On a 401, does the server return a WWW-Authenticate header with a resource_metadata URL, and does the repo contain a handler for the .well-known protected-resource document?

**S3. Request least scope, challenge for more, never ship wildcard scopes.** [SPEC]
Rule: a small baseline scope set, step-up on demand, no omnibus scope.
Reasoning: servers SHOULD put a `scope` in the 401 challenge and SHOULD answer insufficient scope with 403 and a complete scope list in one challenge; servers MUST account for scope hierarchies. The security page lists "Using wildcard or omnibus scopes" as a common mistake and says a stolen broad token enlarges the blast radius. Clients SHOULD cap step-up retries.
Source: Authorization (above); Security Best Practices (above), section Scope Minimization.
Review question: Is there any scope named like `*`, `all` or `admin` that a read-only CV tool can obtain, and does a 403 carry `error="insufficient_scope"` with the scope list?

**S4. A proxy MCP server in front of a third-party OAuth API must run its own per-client consent.** [SPEC]
Rule: confused-deputy defence for static client IDs.
Reasoning: attack needs a static client ID at the third party, dynamic client registration towards you, and a consent cookie. The spec: proxy servers "MUST implement per-client consent" with a registry of approved client_ids per user checked before the third-party flow, exact-string redirect_uri matching, `__Host-` consent cookies, CSRF protection and anti-framing.
Source: Security Best Practices (above), section Confused Deputy Problem.
Review question: If the server fronts a third-party API with one static client_id, is there a per-user, per-client_id consent record checked before the redirect, and is redirect_uri compared by exact string?

**S5. Tool annotations are hints and untrusted; defaults are fail-closed.** [SPEC]
Rule: never skip approval because a tool says it is read-only, unless you control the server.
Reasoning: the schema says "all properties in ToolAnnotations are hints", and clients "MUST consider tool annotations to be untrusted unless they come from trusted servers" (tools page). Defaults: readOnlyHint false, destructiveHint true, idempotentHint false, openWorldHint true; destructiveHint and idempotentHint mean something only when readOnlyHint is false. This extends lab principle 13 (fail-closed default for undeclared tools).
Source: Tools, https://modelcontextprotocol.io/specification/2026-07-28/server/tools.md (no date on page); Schema reference, https://modelcontextprotocol.io/specification/2026-07-28/schema.md (no date on page), ToolAnnotations.
Review question: Is there a code path where a third-party tool's readOnlyHint=true removes an approval prompt or a sandbox rule?

**S6. Server MUST list for tools: validate input, enforce access control, rate limit, sanitize output. Client SHOULD list: confirm, show inputs, validate results, time out, log.** [SPEC]
Rule: both halves exist in your code if you ship both sides.
Reasoning: servers MUST "Validate all tool inputs", implement access controls, rate limit and sanitize outputs. Clients SHOULD prompt on sensitive operations, show tool inputs before the call "to avoid malicious or accidental data exfiltration", validate results before passing them to the LLM, time out, and "Log tool usage for audit purposes".
Source: Tools (above), section Security Considerations.
Review question: Does each write tool validate its arguments with a schema at the server edge, and does the client log every call with arguments and result status?

**S7. Output schemas bind the server (MUST) and invite client validation (SHOULD).** [SPEC]
Rule: define outputSchema for tools that return structured data and validate before the model sees it.
Reasoning: "Servers MUST provide structured results that conform to this schema"; clients SHOULD validate them. A tool returning structuredContent should also return serialized JSON in a text block (SHOULD). Tool execution errors go in the result with isError so the model can correct itself; protocol errors are JSON-RPC errors. [INFERENCE] For an agent that parses CVs, a validated schema is the control that keeps free text out of the next prompt (see S14).
Source: Tools (above).
Review question: Is every structured tool result validated against its outputSchema in code before it is put in a prompt?

**S8. Elicitation: no secrets in form mode, URL mode for credentials, identity bound server-side.** [SPEC]
Rule: never collect passwords or API keys through a form prompt.
Reasoning: "Servers MUST NOT use form mode elicitation to request sensitive information"; credentials go through URL mode, so they never pass through the client or the model. Servers MUST bind elicitation requests to client and user identity, and MUST NOT trust client-supplied identity. Clients MUST show which server asks and offer decline and cancel. In 2026-07-28 elicitation travels inside an InputRequiredResult and the client retries the original request.
Source: Elicitation, https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation.md (no date on page); Changelog (above).
Review question: Does any elicitation schema ask for a password, token or API key, and is the user identity taken from the verified token and not from a form field?

**S9. After sessions were removed, a state handle is a name, not a credential.** [SPEC]
Rule: authorize every call that carries a handle.
Reasoning: revision 2026-07-28 removed protocol-level sessions and the `Mcp-Session-Id` header. Servers that keep state mint explicit handles. "MCP servers MUST NOT treat possession of a state handle as authentication"; handles SHOULD be random, expiring and bound server-side to the user from the verified token (for example keyed `<user_id>:<handle>`).
Source: Security Best Practices (above), section State Handle Hijacking; Changelog (above); Tools (above), section Stateful Tools (non-normative).
Review question: Is stored state keyed by a user id taken from the validated token, and does a handle from another user return an error?

**S10. Streamable HTTP and outbound fetches need origin, bind, auth and SSRF controls.** [SPEC]
Rule: validate Origin, bind locally to loopback, authenticate, and block internal destinations when you fetch URLs.
Reasoning: servers MUST validate the `Origin` header (403 if invalid); locally they SHOULD bind to 127.0.0.1 and SHOULD authenticate every connection. The security page says clients SHOULD block private, loopback and link-local ranges (including 169.254.0.0/16 cloud metadata), validate redirect targets, and consider an egress proxy; it warns against hand-written IP parsers and notes DNS rebinding timing issues. These rules are written for OAuth discovery URLs. [INFERENCE] The same threat applies to an agent that fetches a candidate's website, because the URL is attacker-chosen.
Source: Streamable HTTP, https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http.md (no date on page); Security Best Practices (above), section SSRF.
Review question: Does the URL fetcher resolve and check the destination address against private and link-local ranges on every redirect hop, and run without cloud or CRM credentials in its environment?

**S11. At protocol level a human in the loop is only SHOULD, so the host product must build it.** [SPEC]
Rule: do not assume MCP enforces consent.
Reasoning: tools page: "there SHOULD always be a human in the loop" with ability to deny; the overview says MCP "cannot enforce these security principles at the protocol level" and that hosts must obtain consent before invoking any tool (principle text uses "must"). The consent logic therefore lives in your host or agent code.
Source: Specification overview, https://modelcontextprotocol.io/specification (no date on page); Tools (above).
Review question: Is there a function in the repo that decides, per tool call, whether to ask the user, and does it default to ask for anything that writes?

## Group S-B. Prompt-injection defence by design

**S12. After the agent has read untrusted input, limit what that input can trigger.** [PAPER]
Rule: sequence capabilities so that untrusted text can only reach non-consequential actions.
Reasoning: Beurer-Kellner et al.: "impossible for that input to trigger any consequential actions". Restricted agents must not hold tools that break integrity or confidentiality, and their outputs must not exfiltrate (for example through embedded links). Six patterns follow (S14 to S17). This extends lab principle 43.
Source: Design Patterns for Securing LLM Agents against Prompt Injections, https://arxiv.org/abs/2506.08837 (v1 10 June 2025, v3 27 June 2025), PDF text section 3.
Review question: For each step that ingests CV or web text, can you list the tools reachable in that same context, and is the list empty of writes and outbound calls?

**S13. Rule of Two: at most two of untrusted input, sensitive access, and state change or outbound per session.** [LAB]
Rule: if a task needs all three, require supervision or a fresh context.
Reasoning: Meta: agents "must satisfy no more than two" of [A] untrustworthy inputs, [B] sensitive systems or private data, [C] change state or communicate externally. With all three, the agent "should not be permitted to operate autonomously" (fragments quoted by the fetch tool; the page also names human approval or a fresh context as options). This refines lab principle 38 (the lethal trifecta) by saying what to do when you cannot drop one. A recruiting agent has A (CVs, sites), B (candidate data) and C (CRM writes), so it needs a gate.
Source: Agents Rule of Two, https://ai.meta.com/blog/practical-ai-agent-security/, October 31, 2025.
Review question: Per agent role, are A, B and C each marked, and for any role with all three, is there a named human approval step before C?

**S14. Read untrusted documents with an isolated, tool-less step that returns a fixed schema (map-reduce).** [PAPER]
Rule: one quarantined call per CV; the reduce step must not be an LLM, or must only see constrained output.
Reasoning: the paper dispatches "an isolated LLM-agent" per piece of third-party data that cannot call tools; for the reduce operation either "the reduce operation does not use an LLM", or the map output is constrained (its example: a regex that the output is a number). The resume-ranking case study (section 4.7) uses this: a per-resume LLM returns sanitized fields or a score in a pre-set format, and the top K are returned. The paper states the residual risk: "malicious resumes can still boost their ranking." Net effect: a CV can lie about itself, but cannot discredit other candidates or steer tools.
Source: Beurer-Kellner et al. (above), sections 3.1 pattern 3 and 4.7.
Review question: Is each CV parsed in its own model call with no tools, returning a typed object that is validated before any ranking logic runs?

**S15. Dual LLM and CaMeL: the planner never reads the untrusted values; know the limits.** [PAPER]
Rule: a privileged model plans from the trusted request and handles data as opaque variables.
Reasoning: in the dual-LLM pattern "the privileged LLM cannot dereference this value"; ordinary software substitutes the value at call time. CaMeL (Debenedetti et al., full HTML read) makes the privileged model "only sees the initial user query", executes its plan in a custom interpreter with capabilities and policies, and asks the user when a policy fails. Costs and limits reported: 77% of tasks with provable security vs 84% undefended (abstract, via lab principle 43), about 2.8x input tokens (figure from a fetch-tool summary of the paper), side channels, and "users become desensitized to security prompts". Willison, who proposed dual LLM in 2023, wrote the pattern "is pretty bad" and "isn't a 100% reliable solution" (fragments quoted by the fetch tool) and added a 2025 note pointing to CaMeL.
DISAGREEMENT (soft): the paper presents the pattern as the principled route; its own author and the CaMeL authors list utility and fatigue costs. Treat it as a design for the highest-risk path, not the default for all paths.
Source: Beurer-Kellner et al. (above); Defeating Prompt Injections by Design, https://arxiv.org/html/2503.18813 (v2 24 Jun 2025); The Dual LLM pattern, https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ (25 April 2023, update 11 April 2025 on page).
Review question: Can the model that chooses which tool to call and with which arguments ever see raw text from a CV or web page?

**S16. Fix the set of write actions and fill typed slots (action-selector, plan-then-execute).** [PAPER]
Rule: model output selects from predefined CRM actions and fills schema-validated parameters.
Reasoning: the action-selector acts like an "LLM-modulated 'switch' statement" over predefined actions, with no feedback from the action back into the agent; actions can be templated (a predefined query with placeholders). Plan-then-execute fixes the plan before untrusted data is processed, but injections can still manipulate the inputs to the planned calls, so pair it with S14. [INFERENCE] For a CRM, the slot values (names, emails, notes) are where injection lands, so validate them.
Source: Beurer-Kellner et al. (above), section 3.1 patterns 1 and 2 (the quoted wording is from the raw PDF text).
Review question: Is every CRM write a named function with typed parameters and an allow-list of fields, with no free-form endpoint, query or field name chosen by the model?

**S17. Context minimization: drop the part of the prompt that is no longer needed before the next step.** [PAPER]
Rule: remove the user's or the document's prompt text from context before later steps.
Reasoning: example in the paper: the agent turns the request into a database query, and before returning results "the user's prompt is removed from the context". The pattern covers injections in the user prompt itself; it does not cover injections inside tool results.
Source: Beurer-Kellner et al. (above), pattern 6.
Review question: After extraction, does the next model call receive only the extracted fields, and not the original CV text or the original instruction string from the user's pasted content?

**S18. Even a sound design leaves self-promotion; give reviewers evidence to check.** [PAPER]
Rule: ranking output cites the CV evidence behind each score.
Reasoning: in the resume case study, the dual-LLM summarizer cannot be reached by injections, yet "they can still manipulate the responses provided by the unprivileged LLMs"; the authors say "Data attribution could help" users validate outputs (fragments from raw PDF text, wording as printed). OWASP lists a resume with split instructions that yields a positive recommendation (LLM01 scenario 6; see S21).
Source: Beurer-Kellner et al. (above), section 4.7.3 designs 3 and 4.
Review question: Does each stored score link to the CV text span or extracted field it was derived from?

**S19. Probabilistic layers lower odds; they do not set the damage ceiling.** [LAB] [PAPER]
Rule: classifiers, spotlighting and prompt reminders sit on top of S12 to S16, never instead of them.
Reasoning: Google's layered post lists model hardening, content classifiers, "security thought reinforcement", markdown sanitization and URL redaction, a user confirmation framework for risky actions, and user notifications; its own wording is "Google has taken a layered security approach." Microsoft's spotlighting paper (abstract only) reports attack success dropping from above 50% to below 2% in its experiments on GPT-family models. Both are measurements on specific attackers. This repeats lab principle 37 with two new sources.
Source: Mitigating prompt injection attacks, https://blog.google/security/mitigating-prompt-injection-attacks/, June 13, 2025; Defending Against Indirect Prompt Injection Attacks With Spotlighting, https://arxiv.org/abs/2403.14720, submitted March 20, 2024 (abstract page only).
Review question: If the classifier or spotlight markers were removed from the repo, would the set of damaging actions an injected CV can trigger stay the same?

**S20. Authorization lives in the downstream system, not in the model (complete mediation).** [STANDARD]
Rule: the CRM API decides what this user may write.
Reasoning: OWASP LLM06 names three root causes: "excessive functionality; excessive permissions; excessive autonomy". Prevention: "Implement authorization in downstream systems rather than relying on an LLM"; run extensions in the user's context; minimize extensions; require human approval for high-impact actions. The page says logging and rate limits do not prevent excessive agency but limit damage.
Source: LLM06:2025 Excessive Agency, https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ (no date on page; 2025 edition).
Review question: Does the CRM endpoint check the caller's permissions on each write, and would the write fail if the model asked for an object the user may not touch?

**S21. Test with hostile CVs, not only clean ones.** [PAPER] [STANDARD]
Rule: keep injected documents as fixtures and run them in CI.
Reasoning: OWASP LLM01 says "research shows that they do not fully mitigate prompt injection vulnerabilities" about RAG and fine-tuning, lists "Segregate and identify external content" and "Conduct adversarial testing and attack simulations", and its scenario 6 is a resume with split malicious prompts that produces a positive recommendation. The paper adds that instructions can be hidden in small or white text.
Source: LLM01 Prompt Injection, https://genai.owasp.org/llmrisk/llm01-prompt-injection/ (no date on page; 2025 edition); Beurer-Kellner et al. (above), section 4.7.
Review question: Does the test suite include a CV with hidden or split instructions and assert that no tool is called and no score exceeds what the extracted fields support?

**S22. THIN: text from untrusted input that is stored and later reread becomes an injection that persists.** [COMMENTARY: OWASP announcement paraphrase]
Rule: stored CRM notes and agent memory derived from CVs or websites are untrusted data forever.
Reasoning: OWASP's agentic list entry "ASI06 Memory & Context Poisoning" is described (paraphrase by the fetch tool, from the 9 December 2025 announcement, full document NOT READ) as tampered memory altering agent behaviour long after the original interaction. ASI01 agent goal hijack, ASI02 tool misuse, ASI03 identity and privilege abuse and ASI09 human-agent trust exploitation are the other entries that match a recruiting agent. I did not read the full Top 10 document, so I give no mitigations from it.
Source: OWASP Top 10 for Agentic Applications, https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/, December 9, 2025.
Review question: Is any model-written text derived from a CV or website saved and later placed into a prompt without being marked as untrusted data?

### OWASP LLM Top 10 (2025) items relevant to a CV and CRM agent
Opened in full: LLM01, LLM06. Names and teaser sentences only (page https://genai.owasp.org/llm-top-10/, no date, 2025 edition): LLM02 Sensitive Information Disclosure (candidate PII), LLM05 Improper Output Handling (model output written into CRM or rendered in UI), LLM08 Vector and Embedding Weaknesses (if CVs are embedded), LLM10 Unbounded Consumption (cost per crawled site). I did not open those four pages, so no principle rests on them.

## Group S-C. Regulation for AI that ranks candidates

Law text versus commentary: the AI Act and GDPR quotes below come from artificialintelligenceact.eu and gdpr-info.eu, which reproduce the legal text; EUR-Lex returned an empty page, so I did not read the Official Journal text. The omnibus dates rest on a law-firm note (Lewis Silkin, 27 July 2026, commentary) and on the application dates printed on the AI Act article pages. The regulation number "2026/1744" came from a search summary and from a link target on the Lewis Silkin page. Vote dates (Parliament 16 June 2026, Council 29 June 2026) came from search summaries only and are NOT verified.

**Application dates as currently in force (OPEN: verify on EUR-Lex)**
- High-risk Annex III obligations (employment is point 4): the AI Act article pages show 2 December 2027. Lewis Silkin (27 July 2026): the Digital Omnibus on AI was published in the Official Journal on 24 July 2026 and entered into force 27 July 2026; stand-alone Annex III moves from 2 August 2026 to 2 December 2027; Annex I product-embedded systems to 2 August 2028.
- Article 50 (telling people they interact with AI) still applies from 2 August 2026 (Lewis Silkin; also stated in the AP report).
- Article 4 AI literacy: the AP report says organisations have had the duty since 2 February 2025; Lewis Silkin says the omnibus now words it as measures "supporting AI literacy". DISAGREEMENT of wording between a February 2026 authority report and a July 2026 commentary; the later source reflects the amendment.
- OPEN: the Article 86 page on artificialintelligenceact.eu prints "Comes into force 2 August 2026", while Articles 6, 12, 13, 14 and 26 on the same site print the 2027 date. I did not resolve this.
- The AP report is dated February 2026 and still says the requirements start "in 2026 of 2027" depending on the negotiation; it predates the adoption.

**S23. A system that screens or ranks job applicants is high-risk under Annex III point 4, and profiling removes the exemption.** [LAW TEXT]
Rule: classify the system and write the classification down.
Reasoning: Annex III point 4(a) lists "AI systems intended to be used for the recruitment or selection of natural persons" (the full text also covers targeted job ads, filtering applications and evaluating candidates). Article 6(3) lets some Annex III systems escape high-risk status (narrow procedural task, improving a finished human activity, pattern detection, preparatory task), but an Annex III system "shall always be considered to be high-risk" where it profiles natural persons. A provider who claims the exemption must document the assessment before market placement and register (6(4)). OPEN legal question for counsel: whether a CV ranker is "profiling" under GDPR Article 4(4); I did not open that definition.
Source: Annex III, https://artificialintelligenceact.eu/annex/3/ (no date on page); Article 6, https://artificialintelligenceact.eu/article/6/ (no date on page).
Review question: Does the repo contain a written Article 6 classification note that names Annex III point 4 and states why the 6(3) exemption does or does not apply?

**S24. Logging: Article 12 requires automatic event recording; a deployer keeps logs at least six months.** [LAW TEXT]
Rule: persist per-ranking records you can reconstruct a decision from.
Reasoning: Article 12(1): high-risk systems must technically allow automatic recording of events over their lifetime; 12(2): the logging supports risk identification, post-market monitoring and deployer monitoring under 26(5). The minimum field list in 12(3) applies only to biometric systems (Annex III point 1(a)), not to recruiting. Article 26(6): deployers keep automatically generated logs "of at least six months" unless other law says otherwise. [INFERENCE] The statute does not list fields for recruiting, so the field list in the check below is my engineering choice.
Source: Article 12, https://artificialintelligenceact.eu/article/12/ (no date on page); Article 26, https://artificialintelligenceact.eu/article/26/ (no date on page).
Review question: Is there a persisted record per ranking with input reference, model and prompt version, output, evidence references and reviewer id, and is its retention at least six months?

**S25. Human oversight (Art. 14): the reviewer can understand, doubt, override and stop.** [LAW TEXT]
Rule: build override and stop into the product, not into a policy PDF.
Reasoning: Article 14(4) says deployers must be enabled, as appropriate and proportionate, to detect anomalies, to stay aware of automation bias, to interpret output, to "disregard, override or reverse the output", and to intervene or interrupt "through a 'stop' button or a similar procedure". Article 26(2) requires assigning oversight to people with "necessary competence, training and authority". Oversight measures are scaled to risk, autonomy and context (14(3)).
Source: Article 14, https://artificialintelligenceact.eu/article/14/ (no date on page); Article 26 (above).
Review question: Can a reviewer in the UI change or discard a ranking, and is there a switch that halts the ranking job and leaves data consistent?

**S26. Transparency: provider documents accuracy and oversight measures; deployer tells candidates; candidates can ask for an explanation.** [LAW TEXT]
Rule: ship the information a deployer needs, and the notice a candidate needs.
Reasoning: Article 13(1): systems must be "sufficiently transparent to enable deployers to interpret a system's output"; instructions for use state accuracy metrics, oversight measures and how to collect and interpret logs (13(3)). Article 26(11): deployers must inform natural persons that they are subject to the system for Annex III decision support; 26(7): employers inform workers' representatives and affected workers (that clause covers the employer's own workers, not applicants). Article 86(1): an affected person has the right to obtain "clear and meaningful explanations of the role of the AI system" in the decision. I did not open Article 27 (fundamental rights impact assessment), so I make no claim about it.
Source: Article 13, https://artificialintelligenceact.eu/article/13/; Article 26 (above); Article 86, https://artificialintelligenceact.eu/article/86/ (all no date on page).
Review question: Is there a candidate-facing notice in the application flow that says AI is used, and can the stored data produce a plain-language account of how the ranking was formed?

**S27. GDPR Article 22: no solely automated decision with significant effect without safeguards; the Dutch regulator says keep the process human.** [LAW TEXT] [AUTHORITY]
Rule: no automatic rejection path; a named person decides.
Reasoning: Article 22(1) gives a right not to be subject to a decision based solely on automated processing, including profiling, with "legal effects concerning him or her" or similarly significant effects. Exceptions (contract, authorised by law with safeguards, explicit consent) still require "the right to obtain human intervention on the part of the controller", the right to express a view and to contest. The Autoriteit Persoonsgegevens (Rapportage AI & Algoritmes Nederland, edition 6, February 2026, opened PDF) writes: "Zorg dat het proces menselijk blijft en niet compleet geautomatiseerd" (keep the process human); such decisions are "in principe verboden" unless strict exceptions apply; "Niet alle uitkomsten van een algoritmisch systeem zijn per se een besluit te noemen" (not every output is a decision, so the ban does not always apply); candidates may always ask for a human assessment and an explanation; and applicants have "het recht op betekenisvolle menselijke tussenkomst". The AP also says organisations may already be expected to meet the GDPR duties on explanation, transparency and meaningful human intervention, which do not wait for the AI Act dates. AP guidance on meaningful human intervention ("Handvatten betekenisvolle menselijke tussenkomst") is cited in the report and NOT READ. Blog claims that a recruiter clicking a final button on an automatic score still counts as automated decision-making are NOT from a page I opened and are not used.
Source: GDPR Article 22, https://gdpr-info.eu/art-22-gdpr/ (no date on page); Rapportage AI & Algoritmes Nederland, Editie 6, Februari 2026, Autoriteit Persoonsgegevens, read as a PDF hosted at https://api.eerstekamer.nl/9370000/1/j4nvi0xeni9vr2l_j9vvkfvj6b325az/vmvknkona3pd/f=/vmvknmp8mawk.pdf (document date February 2026; the AP site itself returned 403).
Review question: Is there any code path that sets a candidate to rejected or sends a rejection without a stored human actor id and timestamp on that exact status change?

## Group S-D. Approval UX and permission fatigue

**S28. Measured over-approval: about 93% of permission prompts were approved.** [LAB]
Rule: assume blanket per-action prompts will be clicked through.
Reasoning: Anthropic's auto mode post (March 25, 2026): "users accept 93% of them anyway" (raw HTML text). The containment post (May 25, 2026): "Our telemetry showed users approved roughly 93% of permission prompts", and "approval fatigue showed up within weeks". The same post: sandboxing gave "an 84% reduction in permission prompts" and experienced users "auto-approve roughly twice as often as new users" while interrupting mid-run more often. This corrects sources.md, which said the 93% figure was not found; it is in both posts. It is a vendor telemetry number for coding tasks, so it is not a rate for recruiters.
Source: How we built Claude Code auto mode, https://www.anthropic.com/engineering/claude-code-auto-mode, Mar 25, 2026; How we contain Claude across products, https://www.anthropic.com/engineering/how-we-contain-claude, May 25, 2026.
Review question: Does the product record the approval rate and the time between prompt shown and decision, so over-approval is visible?

**S29. Ask when the action is a write or hard to undo; auto-allow reads inside a contained environment.** [LAB] [INFERENCE]
Rule: spend human attention only on decisions that need judgment.
Reasoning: the first Claude Code design was "allow reads, require approval for write, bash, and network access"; fatigue led to the sandbox and to a classifier. The auto-mode post reports a 0.4% false positive and 17% false negative rate for its classifier on real overeager actions (already in lab principle 41). Meta's Rule of Two (S13) and the OpenAI-style risk rating (lab principle 13) give the same split. [INFERENCE] For recruiting: reading a CV into a schema inside a sandbox needs no prompt; writing to the CRM, sending a message, or changing a candidate's status does.
Source: How we contain Claude across products (above); auto mode post (above).
Review question: Is there a list of actions that never prompt, and is every item on it read-only, reversible and contained?

**S30. People miss threats under time pressure: an observational game dataset shows about one in three missed.** [COMMENTARY] [THIN]
Rule: design the approval screen so the dangerous detail is visible, and do not rely on it alone.
Reasoning: Scale X (27 May 2026) reports a 60-second browser game with over 40,000 plays and over 409,000 approve or deny decisions; the average player "missed 1 in 3 threats", and fatigue "measurably set in" inside a session. The Register (6 August 2026) adds that players approved roughly one in three malicious requests and that `npm run analyze` was approved nearly 65 percent of the time even though the script was on screen; it notes the game is far more malicious-heavy than real work. Limits stated by the author: self-selected players, no real consequences, some leaderboard scores posted by bypassing the game. This is a game, not a field study.
Source: Scale X blog (Alex Wauters), https://scalex.dev/blog/ai-agent-permissions/, May 27, 2026; The Register, https://www.theregister.com/a/5284236, 6 August 2026.
Review question: Does the approval view show the exact data or diff that will be written, instead of a summary sentence from the model?

**S31. The approver should judge the action, not the agent's explanation.** [LAB] [LAW TEXT]
Rule: do not let model-written justification be the main input to the approval decision.
Reasoning: in the auto-mode classifier, "judge what the agent did, not what the agent said": assistant text is stripped so the agent cannot talk the judge into a bad call. OWASP's agentic list names "Human-Agent Trust Exploitation" (ASI09; paraphrase: confident, polished explanations lead operators to approve harmful actions; full document NOT READ). Article 14(4)(b) names the tendency to over-rely on output as something deployers must stay aware of. CaMeL's authors write that frequent prompts risk "users become desensitized to security prompts".
Source: auto mode post (above); OWASP agentic announcement (above); Article 14 (above); CaMeL HTML (above).
Review question: Is the justification text produced by the agent shown below, not instead of, the structured data about to be written?

## Checks for a recruiting agent

An agent that reads CVs and candidate websites and writes to a CRM. Each check is yes/no from code or repo.

1. Is the model call that reads CV or website text run with no tools at all (no write, no fetch, no CRM access)? (S12, S14)
2. Is the output of that call validated against a fixed schema with types, enums and length limits before anything else uses it? (S7, S14)
3. Does the ranking or decision step receive only schema fields, never the raw CV or web text? (S14, S15, S17)
4. Does every agent role that has untrusted input, candidate data and write access have a named human approval step before the write? (S13)
5. Are CRM writes fixed named functions with typed parameters and a field allow-list, with no model-chosen endpoint, object id or field name? (S16)
6. Does the CRM API authorize each write against the acting user on the server side, with an audience-bound token and no inbound token forwarded? (S1, S20)
7. Does the website fetcher block private, loopback and link-local addresses on every redirect hop and run without CRM or cloud credentials in its environment? (S10)
8. Are annotations from external MCP servers ignored when deciding to skip approval, and is an undeclared tool treated as destructive and open-world? (S5)
9. Is every change of candidate status to rejected, and every rejection message, tied to a stored human actor id and timestamp? (S27)
10. Is there a persisted record per ranking with input reference, model and prompt version, output, evidence references and reviewer id, kept at least six months? (S24)
11. Can the reviewer UI show evidence per score, override a ranking, and halt the ranking job, with no bulk approve without per-candidate view? (S18, S25, S30)
12. Is there a candidate-facing notice that AI is used and a stored data path that can produce an explanation of the ranking's role? (S26)
13. Are approval rate and decision time recorded, and are read-only reversible actions the only ones that never prompt? (S28, S29)
14. Does CI contain hostile CV fixtures (hidden text, split payload, instruction on a website) that assert no tool call and no score beyond the extracted fields? (S21)
15. Is any model-written text derived from a CV or website stored for later use marked as untrusted and kept out of the privileged prompt? (S22)

## What is not covered by any opened source
- Full OWASP Top 10 for Agentic Applications document: NOT READ; only the December 2025 announcement via a fetch summary.
- OpenAI "Designing agents to resist prompt injection" (March 11, 2026 per a search result): WebFetch returned HTTP 403, NOT READ. I did not try to bypass the block.
- AP page "Handvatten betekenisvolle menselijke tussenkomst" and AP online-assessment guidance (reported as March 2026 by blogs): NOT READ.
- EUR-Lex text of Regulation (EU) 2026/1744: empty page, NOT READ. Article 27 (FRIA) and GDPR Article 4(4): not opened.
- Anthropic system card figures for prompt injection (Opus 4.8, Opus 5, Sonnet 4.6) appeared only in search summaries: NOT READ, not used.

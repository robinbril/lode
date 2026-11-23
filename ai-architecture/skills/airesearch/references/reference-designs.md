# Reference designs

Shapes that meet the high anchors in `rubric.md`. Use them to say what "good" looks like in a review, and as a start when asked to design. Adapt names to the codebase; keep the invariants.

## D1. One tool registry, many surfaces

Invariant: a capability exists once. Chat, MCP, public API, jobs and sister products are consumers.

A tool is a record, not a function with a decorator per surface:

```
Tool(
  name            "crm.company.get"            # namespaced, stable
  description     written for a model, tested with real tasks
  input_schema    typed, validated in code before anything runs
  output_schema   typed, capped; large results by reference
  effect          read | write | send | delete
  reversible      true | false                 # false raises the tier
  idempotent      true | false
  permission      the RBAC check a human needs for the same act
  data_classes    e.g. personal, special-category, none
  handler         calls the owning module's public function
)
```

Defaults are fail-closed: an undeclared tool is `write`, not reversible, not concurrency-safe (principle 13). Deny rules remove a tool from the list before the model sees it.

Where it lives in a modular codebase: the registry type and the dispatcher are kernel code and know no domain terms. Each module registers its own tools from its public surface at start-up. The kernel never imports a module; modules import the registry.

Surfaces are generated: the MCP server lists the registry (annotations from `effect` and `idempotent`), the in-app agent gets the same list filtered by the user's permissions, docs come from the same records. A test fails when a surface exposes a tool that is not in the registry.

## D2. One dispatcher: validate, authorize, decide, run, record

Every tool call from every surface goes through one function, in this order (principle 40):

1. Validate input against the schema. Invalid input returns an error the model can fix.
2. Authorize as the human: the same RBAC and tenant scope as the GUI. The agent never has more rights than its user.
3. Decide the tier (D3).
4. Run, with an idempotency key for writes.
5. Record one row: who, channel, tool, input hash, tier, decision, result, the model call that proposed it.

Nothing else may call a write handler. A test greps for direct calls.

## D3. Tiers that depend on risk, channel and content

```
tier = max(
  base(tool.effect, tool.reversible),      # read: auto; reversible write: auto or confirm; send/delete: confirm
  channel(surface),                        # external agent client: at least confirm for writes, unless the tenant allows
  taint(context),                          # untrusted content in the run: raise one step, or close send
  tenant_policy(tool),                     # a tenant may tighten, never loosen below base
  data(tool.data_classes, subject_flags)   # legal hold or restriction: deny
)
```

- `auto`: run and record.
- `confirm`: create a pending action with the exact payload; a human approves or edits; then it runs.
- `deny`: return a reason the model can act on. Deny always wins.

Taint: a run is tainted from the moment a tool returns content from outside (a website, an upload, an email body) until the run ends. This is the cheap version of separating control from data (principle 43, 38): it does not prove safety, it removes the outward channel while the risk is present.

Measure approval load. If people approve everything, the tier is noise; move safe cases to auto and keep confirm rare (principle 39, 41).

## D4. Approval as a durable record, shown as the payload

A pending action is a row: tool, exact input, a human-readable diff against current data, who asked, expiry. Surfaces render the same row:

- In-app chat: a card with the diff and Approve, Edit, Reject.
- MCP client: elicitation when the client supports it; otherwise the tool returns `pending` with a link, and the user approves in the app.
- Sister product: shows the pending state and the link. It does not keep its own approval for this write; the system that owns the data is the authority (anti-pattern A11).

The human approves content, not a step name (anti-pattern A10).

## D5. The agent loop

One loop, explicit state, named exits (; principle 4):

- Inputs: system prefix (stable, cacheable), tool list, session state, newest turns.
- Each round: model call, zero or more tool calls through D2, results appended.
- Exits: answer given, budget reached (rounds, tokens, time), a pending approval, repeated denials, user stop.
- Reads may run in parallel; writes run one at a time in order ().
- Long runs are jobs: the request returns a run id, events stream to the client, the run survives a restart (principle 8).

With bring-your-own-model: tool calling quality differs per provider and model. Gate the agent surface on a capability check that runs real tool calls against the configured model, and fall back to the fixed workflow when the model fails it. Do not pretend all models are equal.

## D6. In-app chat as a client of the public tool surface

The strongest form of parity: the product's own chat reaches its tools the same way an external agent does (same list, same dispatcher, same identity path). Then "everything the GUI can do, an agent can do" is checked by the product team every day (K20).

Cost: one more hop if done over the network. In-process is fine as long as the list and the dispatcher are the same objects.

## D7. Workflow and agent together

A fixed workflow is not a failure; for a known sequence it is the better tool (principle 1, 2). The mature shape has both:

- The workflow steps are tools too. The wizard calls them in order; the agent may call them when asked.
- The chat can do anything the wizard can, and the wizard is a shortcut for the common path.
- The autonomy slider (K17) is the tier table from D3 under a user's control.

## D8. Records that satisfy a regulator

When the system scores or ranks people (hiring), keep per decision: the input sources by hash, the criteria confirmed by a human, the model and the settings actually sent, the output, the human who acted on it, and a retention period that matches the law, not only the privacy wish to delete. See `security-mcp-regulation.md` when present.

## D9. Evals as the gate for prompt and model changes

A golden set from real cases (start with twenty), graders on outcomes, deterministic checks where code can check. Run on every prompt change, every model change and every new provider. Store results. A bring-your-own-model product needs a per-model pass before a tenant may use that model for scoring people.

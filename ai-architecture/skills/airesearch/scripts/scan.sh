#!/usr/bin/env bash
# Read-only lead finder for the airesearch skill. Usage: scan.sh <repo-or-subdir>
# Prints leads per anti-pattern (references/anti-patterns.md). A hit is a lead, not a finding.
# Uses plain grep so it runs anywhere.
set -u
ROOT="${1:-.}"
[ -d "$ROOT" ] || { echo "not a directory: $ROOT"; exit 2; }
X=(--exclude-dir=node_modules --exclude-dir=dist --exclude-dir=build --exclude-dir=.venv --exclude-dir=venv --exclude-dir=.git --exclude-dir=__pycache__)
CODE=(--include='*.py' --include='*.ts' --include='*.tsx' --include='*.js' --include='*.vue')
sec() { printf '\n== %s ==\n' "$1"; }
cnt() { grep -rEc "${X[@]}" "${CODE[@]}" "$@" "$ROOT" 2>/dev/null | awk -F: '{s+=$NF} END{print s+0}'; }
top() { grep -rEn "${X[@]}" "${CODE[@]}" "$@" "$ROOT" 2>/dev/null | sed "s|^$ROOT/||" | cut -c1-190 | head -"${N:-8}"; }

sec "Model call sites (where the model is reached)"
top -e 'chat_complete\(|messages\.create\(|chat\.completions\.create\(|responses\.create\(|generate_content\(|claude -p'
echo "local wrappers around the model (grep for their callers next):"
N=8 top -e '^(async )?def [a-z_]*(llm|chat_complete|completion|model_call)[a-z_]*\('

sec "Tool calling and agent loop signals (all zero = single call or workflow)"
echo "tool-calling hits: $(cnt -e 'tools *=|tool_use|tool_calls|function_call|tool_choice')"
echo "loop bounds (max rounds/steps/turns): $(cnt -i -e 'max_(rounds|steps|turns|iterations)')"
echo "streaming hits: $(cnt -e 'stream *= *True|text/event-stream|EventSource|StreamingResponse')"

sec "A1 policy tables: count of each tier value"
for v in allow deny ask confirm; do echo "\"$v\": $(cnt -e "[\"']$v[\"']")"; done
N=6 top -e '^[A-Z_]*(POLICY|PERMISSIONS|ALLOWED)[A-Z_]*.*='

echo "(policy kept as sets of tool names gives zeros here: read the dispatcher's decision function, see A18)"
N=6 top -e '^_?[A-Z_]*(GATED|HELD|APPROVAL|READ_TOOLS|WRITE_TOOLS)[A-Z_]* *='

sec "A17 tools handed to another process (compare with the gated list)"
N=8 top -e 'allowedTools|allowed_tools|mcp-config|mcp_config|disallowedTools'

sec "A2 trust labels and injection flags (check that something branches on them)"
echo "label hits: $(cnt -e 'untrusted|trust_level|injection_flags?')"
echo "callers that drop the second return value (often the flags):"
N=6 top -e ', *_ *= *[a-z_]+\.(json|text)\('

sec "A3 truncation that may drop the newest"
N=8 top -e '\[: *[A-Za-z_]*(limit|LIMIT|MAX|CHARS)[A-Za-z_]* *\]|\[: *[0-9]{4,} *\]|history\[-[0-9]+:\]'

sec "A4 regex JSON instead of schema"
N=6 top -e 'json\.loads\(match|JSON\.parse\(.*match|re\.search\(pattern, cleaned'
echo "structured output hits: $(cnt -e 'response_format|output_schema|json_schema|model_validate\(|strict *[:=] *[Tt]rue')"

sec "A5 long timeouts on model calls (work inside the request)"
N=6 top -e 'timeout(_seconds)? *= *([6-9][0-9]|[1-9][0-9]{2,})(\.0)?'

sec "A7 token and cost tracking"
echo "usage/token hits: $(cnt -e 'input_tokens|output_tokens|prompt_tokens|completion_tokens|cache_read')"

sec "A8 tool surfaces (compare the lists)"
echo "MCP tool decorators: $(cnt -e '@mcp\.tool|@server\.tool|server\.tool\(|registerTool\(')"
echo "HTTP routes: $(cnt -e '@router\.(get|post|put|patch|delete)\(|app\.(get|post|put|patch|delete)\(')"

sec "A9 chat that points at buttons"
N=5 top -i -e 'actions are buttons|point to them|click the button|use the button'

sec "A12 untrusted values in instruction strings (f-strings in prompt builders)"
N=8 top -e '(instruction|system|prompt) *= *\(? *f["'"'"']|instruction=\(?$'

sec "A13 tests: mocks against evals"
echo "mock/fake model hits: $(cnt -i -e 'monkeypatch|mock|fake.*(llm|model|chat_complete)')"
GITROOT="$(git -C "$ROOT" rev-parse --show-toplevel 2>/dev/null || echo "$ROOT")"
echo "eval/golden directories (searched from $GITROOT):"; find "$GITROOT" -maxdepth 4 -type d \( -iname 'evals' -o -iname 'eval' -o -iname 'golden*' \) -not -path '*/node_modules/*' 2>/dev/null | head -5

sec "A14 who may read prompts and traces (check the auth dependency on these routes)"
N=6 top -e 'prompt_text|output_text'

sec "A16 harness tied to one surface (HTTP errors raised outside route files)"
grep -rEln "${X[@]}" --include='*.py' -e 'HTTPException' "$ROOT" 2>/dev/null | grep -viE '/(api|routes?|routers?)/' | sed "s|^$ROOT/||" | head -8
echo
echo "Done. Open each lead before you report it."

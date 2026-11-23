#!/usr/bin/env bash
# CAS Deterministic PreToolUse Hook: Production Command, Secret Sprawl & Architecture Linter Gate
set -euo pipefail

if [[ "${CAS_ALLOW_PROTECTED_WRITE:-0}" == "1" ]]; then
  exit 0
fi

CMD_INPUT="${1:-${CLAUDE_COMMAND:-${TOOL_INPUT_COMMAND:-}}}"

if [[ -z "$CMD_INPUT" ]] && [[ ! -t 0 ]]; then
  STDIN_PAYLOAD="$(cat || true)"
  if [[ -n "$STDIN_PAYLOAD" ]]; then
    CMD_INPUT="$(python3 -c '
import json, sys
try:
    data = json.loads(sys.stdin.read())
    ti = data.get("tool_input") or {}
    print(ti.get("command") or ti.get("content") or ti.get("new_string") or "")
except Exception:
    print("")
' <<< "$STDIN_PAYLOAD")"
  fi
fi

if [[ -z "$CMD_INPUT" ]]; then
  exit 0
fi

# 1. Block destructive production/git commands
if echo "$CMD_INPUT" | grep -Eiq '(git\s+push\s+.*(--force|-f)\b|rm\s+-rf\s+/(\s|$)|drop\s+database\b|truncate\s+table\b)'; then
  echo "[CAS][HOOK][BLOCKED] Destructive command blocked by CAS production-gate.sh." >&2
  exit 1
fi

# 2. Block hardcoded secret patterns (credential sprawl)
if echo "$CMD_INPUT" | grep -Eq '(sk_live_[0-9a-zA-Z]{8,}|ghp_[0-9a-zA-Z]{16,}|AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----)'; then
  echo "[CAS][HOOK][BLOCKED] Potential hardcoded secret token detected by CAS production-gate.sh." >&2
  exit 1
fi

exit 0

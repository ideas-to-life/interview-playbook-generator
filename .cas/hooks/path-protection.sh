#!/usr/bin/env bash
# CAS Deterministic PreToolUse Hook: Path Protection & Bugfix Test-Tampering Guard
set -euo pipefail

if [[ "${CAS_ALLOW_PROTECTED_WRITE:-0}" == "1" ]]; then
  exit 0
fi

TARGET_PATH="${1:-${CLAUDE_FILE_PATHS:-${TOOL_INPUT_FILE_PATH:-}}}"

PYTHON_CMD="/usr/bin/python3"
if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
  PYTHON_CMD="python3"
fi

# If JSON payload is piped via stdin (Claude Code PreToolUse hook format), extract file_path if TARGET_PATH is empty
if [[ -z "$TARGET_PATH" ]] && [[ ! -t 0 ]]; then
  STDIN_PAYLOAD="$(cat || true)"
  if [[ -n "$STDIN_PAYLOAD" ]]; then
    TARGET_PATH="$("$PYTHON_CMD" -c '
import json, sys
try:
    data = json.loads(sys.stdin.read())
    ti = data.get("tool_input") or {}
    print(ti.get("file_path") or ti.get("path") or "")
except Exception:
    print("")
' <<< "$STDIN_PAYLOAD")"
  fi
fi

if [[ -z "$TARGET_PATH" ]]; then
  exit 0
fi

# Normalize leading ./
REL_PATH="${TARGET_PATH#./}"

# 1. Protected secret, git, and governance substrate files
case "$REL_PATH" in
  .env|.env.*|*.pem|*.key|.git/*|*/.git/*|.cas/patterns/patterns-catalogue.yaml|*/.cas/patterns/patterns-catalogue.yaml|.cas/hooks/*|*/.cas/hooks/*|.claude/settings.json|*/.claude/settings.json|docs/architecture/decisions/adr-*.md|*/docs/architecture/decisions/adr-*.md)
    echo "[CAS][HOOK][BLOCKED] Direct modification of protected path '$REL_PATH' is prohibited by CAS governance." >&2
    echo "[CAS][HINT] Set CAS_ALLOW_PROTECTED_WRITE=1 if this is an authorized maintainer update." >&2
    exit 1
    ;;
esac

# 2. Block test-assertion tampering on bugfix branches (fix/* or bugfix/*)
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")"
if [[ "$BRANCH" == fix/* || "$BRANCH" == bugfix/* ]]; then
  if [[ "$REL_PATH" == tests/* || "$REL_PATH" == */tests/* ]]; then
    TAMPER_DETECTED=0
    if [[ "${CAS_HOOK_TEST_TAMPER:-0}" == "1" ]]; then
      TAMPER_DETECTED=1
    elif [[ -f "$REL_PATH" ]]; then
      if grep -Eq '@pytest\.mark\.skip|pytest\.skip\(' "$REL_PATH" 2>/dev/null; then
        TAMPER_DETECTED=1
      else
        DIFF_OUT="$(git diff -U0 HEAD -- "$REL_PATH" 2>/dev/null || echo "")"
        if [[ -n "$DIFF_OUT" ]]; then
          REMOVED_ASSERTS="$(printf "%s\n" "$DIFF_OUT" | grep '^-[^-]' | grep -w 'assert' | wc -l | tr -d '[:space:]' || echo "0")"
          ADDED_ASSERTS="$(printf "%s\n" "$DIFF_OUT" | grep '^+[^+]' | grep -w 'assert' | wc -l | tr -d '[:space:]' || echo "0")"
          if [[ "${REMOVED_ASSERTS:-0}" -gt 0 && "${ADDED_ASSERTS:-0}" -eq 0 ]]; then
            TAMPER_DETECTED=1
          fi
        fi
      fi
    fi
    if [[ "$TAMPER_DETECTED" == "1" ]]; then
      echo "[CAS][HOOK][BLOCKED] Test tampering detected in '$REL_PATH' on bugfix branch '$BRANCH' (do not skip tests or delete assertions to pass bugfixes)." >&2
      exit 1
    fi
  fi
fi

# 3. Block unplanned production code modifications without active SDD spec and plan
if [[ "$REL_PATH" == src/* || "$REL_PATH" == */src/* ]]; then
  if [[ "$BRANCH" == "main" || "$BRANCH" == "master" || "$BRANCH" == "HEAD" || -z "$BRANCH" ]]; then
    echo "[CAS][HOOK][BLOCKED] Direct modification of production code on protected branch '$BRANCH' is prohibited. Create a feature branch first (e.g. 'git checkout -b <NNN-feature-name>')." >&2
    exit 1
  fi

  if [[ "$REL_PATH" == src/*.py || "$REL_PATH" == */src/*.py ]]; then
    if [[ "$BRANCH" != fix/* && "$BRANCH" != bugfix/* ]]; then
      PLAN_FILE=""
      SPEC_FILE=""
      if [[ -f ".specify/feature.json" ]]; then
        FEATURE_DIR="$("$PYTHON_CMD" -c 'import json; print(json.load(open(".specify/feature.json")).get("feature_directory") or "")' 2>/dev/null || echo "")"
        if [[ -n "$FEATURE_DIR" ]]; then
          if [[ -f "$FEATURE_DIR/plan.md" ]]; then
            PLAN_FILE="$FEATURE_DIR/plan.md"
          fi
          if [[ -f "$FEATURE_DIR/spec.md" ]]; then
            SPEC_FILE="$FEATURE_DIR/spec.md"
          fi
        fi
      fi
      if [[ -z "$PLAN_FILE" && -n "$BRANCH" && -f "specs/$BRANCH/plan.md" ]]; then
        PLAN_FILE="specs/$BRANCH/plan.md"
      fi
      if [[ -z "$SPEC_FILE" && -n "$BRANCH" && -f "specs/$BRANCH/spec.md" ]]; then
        SPEC_FILE="specs/$BRANCH/spec.md"
      fi
      if [[ -z "$PLAN_FILE" && -f "plan.md" ]]; then
        PLAN_FILE="plan.md"
      fi
      if [[ -z "$SPEC_FILE" && -f "spec.md" ]]; then
        SPEC_FILE="spec.md"
      fi

      if [[ -z "$SPEC_FILE" || -z "$PLAN_FILE" ]]; then
        echo "[CAS][HOOK][BLOCKED] Direct modification of production file '$REL_PATH' is prohibited without both an active SDD specification (spec.md) and plan (plan.md). Run /speckit-specify and /speckit-plan first." >&2
        exit 1
      fi

      BASE_NAME="$(basename "$REL_PATH")"
      if ! grep -qF "$BASE_NAME" "$PLAN_FILE" 2>/dev/null; then
        echo "[CAS][HOOK][BLOCKED] Direct modification of '$REL_PATH' is blocked because '$BASE_NAME' is not declared in active plan '$PLAN_FILE' under 'Files that change'. Modifying production code requires updating your specification (spec.md) requirements and declaring '$BASE_NAME' in your plan (plan.md)." >&2
        exit 1
      fi
    fi
  fi
fi

exit 0

# CAS Multi-Pass Automated Pull Request Review Policy (`REVIEW.md`)

This repository enforces a **3-Pass Automated PR Review Contract** governed by the Continuous Architecture System (CAS). Both the Fresh-Context Verifier subagent (`.cas/agents/verifier.md`) and the CLI gate (`uv run cas governance verify-diff` / `uv run cas governance review-pr`) evaluate every change against the three passes below.

---

## Pass 1: Logic, SDD/TDD & Implementation Plan Alignment

- **SDD Artifact Presence (`.cas/config.yaml`)**: Changes to `src/**` must be accompanied by an active specification and implementation plan resolved via `.cas/config.yaml` (`speckit`, `anthropic-native`, `superpowers`, or `agent-skills`), unless explicitly exempted via `[bugfix]` or `[skip-governance]`.
- **Implementation Plan Contract**: The active plan must address the 4 core concerns:
  1. `Files that change`
  2. `Order of work`
  3. `Risks`
  4. `Proof` (Verification commands)
- **Plan Scope Invariance (`PLAN-002`)**: Every modified production code file in `src/**` must be declared in the active implementation plan under `Files that change` (or `Project Structure` / `Source Code`). Unplanned file modifications block merge (`High` severity).
- **TDD Enforcement**: Changes to `src/**` must include corresponding unit/regression test updates under `tests/**` containing real assertions.

---

## Pass 2: Security, Supply Chain (Slopsquatting) & Runtime Integrity

- **Zero Credential Sprawl**: No hardcoded API keys, tokens, or secrets (`sk_live_`, `ghp_`, `AKIA[0-9A-Z]{16}`, `service_role`, `PRIVATE KEY`) may appear in any committed file.
- **Slopsquatting & Dependency Hygiene**: New dependencies in `pyproject.toml` or `requirements.txt` must not match known typosquatted/hallucinated package names or forbidden direct vendor LLM SDKs.
- **No Bugfix Test Tampering**: On `fix/*` or `bugfix/*` branches (or commits tagged `[bugfix]`), existing test assertions in `tests/**` must not be deleted or weakened to force a green build.
- **Governance Substrate Integrity**: Protected governance files (`.cas/patterns/patterns-catalogue.yaml`, `.cas/hooks/*`, `.claude/settings.json`, accepted ADRs) must not be modified by agents unless `CAS_ALLOW_PROTECTED_WRITE=1` is explicitly set by a maintainer.

---

## Pass 3: CAS Pattern Invariants, Anti-Patterns & Proportionate Routing

- **Deterministic Architecture Linter (`ARCH-LINT-001..004`)**: Zero violations from `uv run cas governance lint --target-dir .`.
- **Pattern Catalogue Compliance**: All changes must satisfy the `invariants` and avoid the `anti_patterns` defined in `.cas/patterns/patterns-catalogue.yaml`.
- **Proportionate Governance Routing**:
  - **Path A (Governed Reuse)**: Conforms to existing patterns → eligible for automated merge once Passes 1–3 pass.
  - **Path B (Architectural Novelty)**: Introduces a new pattern or cross-layer dependency → requires a candidate ADR/proposal and Architect sign-off.
  - **Path C (Architectural Exception)**: Deviates from a rule or invariant → requires an approved `exc-*.yaml` exception record.

---

## Severity Definitions & Merge Thresholds

| Severity | Definition | Default Strict Gate (`--fail-on high`) | Advisory Mode (`--advisory` / `enforcement: advisory`) |
| :--- | :--- | :--- | :--- |
| **Critical** | Hardcoded secrets, test tampering during bugfix, or direct violation of protected governance substrate. | **Blocks Merge (`exit 1`)** | Reported (`exit 0`) |
| **High** | Missing SDD/TDD artifacts for `src/**` changes, `ARCH-LINT-001..004` violations, or pattern `anti_patterns` breaches. | **Blocks Merge (`exit 1`)** | Reported (`exit 0`) |
| **Medium** | Incomplete implementation plan section (`files_that_change`, `order_of_work`, `risks`, `proof`) or minor structural warning. | Allowed (`exit 0` unless `--fail-on medium`) | Reported (`exit 0`) |
| **Low** | Informational style, documentation, or non-blocking hygiene note. | Allowed (`exit 0`) | Reported (`exit 0`) |

### Machine-Readable Footer Invariant

Every review output MUST conclude with the exact summary line:

```text
Critical: <int> | High: <int> | Medium: <int> | Low: <int>
```

---
name: cas-sync-archgov-reviews
description: Synchronize external ArchGov review decisions for reference architectures and ADRs into local Git state, detect approvals, and trigger downstream lifecycle steps (ADR generation, pattern institutionalization) on-demand or via scheduled background checks.
---

# Skill: cas-sync-archgov-reviews

## Intent
Execute a bidirectional review synchronization cycle between the local CAS repository and the external ArchGov platform (`https://archgov.pbo-tech.net`):
1. **Outbound Push**: Automatically batch-publish local unpublished candidate Reference Architectures and ADRs so architects can review and ratify them directly within the ArchGov web portal.
2. **Inbound Pull**: Synchronize remote review decisions from ArchGov back into Git state, reconciling `knowledge/projects/<project>/governance/archgov-sync.yaml`, updating artifact frontmatter, logging immutable audit records, and unblocking downstream ADR generation and pattern institutionalization.

**When to use this skill:**
- User asks to "sync ArchGov reviews", "check review status", or "refresh governance decisions"
- Automatically publishing local working drafts for formal Design Authority or ARB review
- User asks to "schedule periodic review synchronization"
- Downstream pattern lifecycle flows require verification of ratified Reference Architectures or accepted ADRs
- Detecting whether externally reviewed reference architectures or ADRs have been approved, rejected, deferred, or conditionally accepted

**When NOT to use this skill:**
- Manually editing architecture models or diagrams
- Initial discovery or forensic diagnostic flows

---

## Capabilities & Tool Usage

1. **Two-Way Synchronization (Push then Pull)**:
   Run outbound batch publication followed by inbound status polling:
   ```bash
   # Full cycle across all governance artifacts (Reference Architectures and ADRs)
   uv run cas governance publish --project <project_id> --all-unpublished --type reference_arch
   uv run cas governance publish --project <project_id> --all-unpublished --type adr
   uv run cas governance sync --project <project_id>

   # Scoped sync for specific artifact type
   uv run cas governance publish --project <project_id> --all-unpublished --type reference_arch
   uv run cas governance sync --project <project_id> --type reference_arch

   # Synchronize without auto-triggering downstream generation
   uv run cas governance sync --project <project_id> --no-chain
   ```

2. **Simulation & Dry-Run Mode**:
   Simulate both outbound publication and inbound synchronization without making HTTP mutations or altering local files:
   ```bash
   uv run cas governance publish --project <project_id> --all-unpublished --type reference_arch --dry-run
   uv run cas governance publish --project <project_id> --all-unpublished --type adr --dry-run
   uv run cas governance sync --project <project_id> --dry-run
   ```

3. **Inspect Artifact Status**:
   Inspect current local review status and external twins:
   ```bash
   # Inspect reference architecture review status
   uv run cas governance status reference-architecture-<pattern_id> --project <project_id>

   # Inspect ADR review status
   uv run cas governance status adr-<pattern_id> --project <project_id>
   ```

4. **Background Scheduling**:
   When the user requests continuous or recurring monitoring, use the agent `schedule` tool:
   - For recurring checks (e.g. every 4 hours):
     `schedule(CronExpression="0 */4 * * *", Prompt="Sync ArchGov reference architecture and ADR reviews and report status changes")`
   - For a one-shot follow-up timer (e.g. check again in 30 minutes):
     `schedule(DurationSeconds=1800, Prompt="Check ArchGov review status updates for pending governance artifacts")`

---

## Execution Protocol

1. **Step 1 - Project Context & Scope Resolution**:
   - Determine the active project identifier (default: `ideas-to-life-cas`).
   - Identify if the caller requested a scoped artifact type (e.g. `--type reference_arch` or `--type adr`).
   - If a type is specified, restrict both Phase 1 (Push) and Phase 2 (Pull) to that type.
   - If no type is specified, execute Phase 1 for both `reference_arch` and `adr` sequentially, followed by a full Phase 2 sync.

2. **Step 2 - Phase 1: Outbound Batch Publication (Push)**:
   - For each artifact type in scope, dispatch all local unpublished drafts to ArchGov:
     ```bash
     uv run cas governance publish --project <project_id> --all-unpublished --type <type>
     ```
   - If running in simulation mode, append `--dry-run`.
   - **Fault Resilience & Offline Handling**: If the ArchGov endpoint is unreachable (e.g. connection refused, network timeout, DNS failure):
     - Log a clear warning: `[WARN] ArchGov endpoint unreachable. Skipping remote push and proceeding with local governance evaluation.`
     - Do NOT abort execution; smoothly continue to Step 3.

3. **Step 3 - Phase 2: Inbound Review Synchronization (Pull)**:
   - Poll ArchGov for remote decisions and synchronize into Git state:
     ```bash
     uv run cas governance sync --project <project_id> [--type <type>] [--no-chain] [--dry-run]
     ```
   - If ArchGov is unreachable, catch the warning and proceed to inspecting local state.

4. **Step 4 - Evaluate Diffs & Scan Artifact State**:
   - Read `knowledge/projects/<project_id>/governance/archgov-sync.yaml` to identify actively tracked remote artifacts.
   - Scan local directories for complete coverage:
     - `knowledge/projects/<project_id>/reference-architectures/*.md`
     - `knowledge/projects/<project_id>/adrs/*.md`
   - Correlate files against `archgov-sync.yaml`:
     - **Tracked Artifacts**: Match by `artifact_id` or `pattern_id`. Evaluate status changes (`approved`, `accepted`, `rejected`, `conditional`, `deferred`) and check `downstream_chained` flags.
     - **Local-Only / Unpublished Artifacts**: Read YAML frontmatter (e.g. `status: draft`, `decision.status: proposed` or `accepted`). Note whether ratified offline via CLI or remaining local working drafts.

5. **Step 5 - Downstream Verification**:
   - For newly approved reference architectures, verify that `promotion-to-decision-records` produced the corresponding ADR under `knowledge/projects/<project_id>/adrs/adr-<pattern_id>.md`.
   - For newly accepted ADRs, verify that `approved-adr-to-pattern` produced the corresponding global pattern under `knowledge/global/patterns/<pattern_id>.yaml`.

6. **Step 6 - Report to Architect (4-Quadrant Governance Dashboard)**:
   - Provide a comprehensive, structured status report organized into 4 clear sections:
     1. **Outbound Dispatches (Push)**: Newly published or staged candidate drafts, including assigned `archgov_artifact_id` and review cycle IDs.
     2. **In-Flight Remote Reviews (ArchGov)**: Active reviews currently under consideration, detailing local status, remote status, forum (Design Authority vs ARB), and assigned reviewer.
     3. **Ratified Governance Decisions & Downstream Chaining**: Approved reference architectures and accepted ADRs, verifying downstream ADR or global pattern generation.
     4. **Local / Offline Governance Artifacts**: Artefacts not published to ArchGov, detailing local decision status and recommended next actions.

7. **Step 7 - Governance Validation & Knowledge Sync Gate**:
   - Following synchronization or automated downstream chaining, execute local governance validation:
     ```bash
     uv run cas governance validate --project <project_id>
     ```
   - Verify that all 4 dimensions report PASS with 0 errors:
     - Schemas: PASS
     - Traceability: PASS
     - Lifecycle: PASS
     - Governance State: PASS
   - If changes were made to knowledge artifacts (`archgov-sync.yaml`, ADR frontmatter, promotion decisions, action records):
     - Execute the mandatory Two-Phase Commit sequence:
       1. `git -C /Users/avfranco/cas-knowledge add <modified-paths>`
       2. `git -C /Users/avfranco/cas-knowledge commit -m "<type>(scope): <description>"`
       3. `git -C /Users/avfranco/cas-knowledge push origin main`
       4. `git add <modified-paths>`
       5. `git commit -m "<type>(scope): <description>"`
       6. `git push origin <branch>`

# Quickstart & Validation Guide: Upwork Proposal Generator V2.1

This guide describes how to validate the V2.1 Human-Owned Opportunity Decision & Evidence-Gap Handling workflow.

## Prerequisites

- Python 3.11+
- Existing canonical OKF evidence catalog in `out/okf/`
- Target opportunity file in `config/target-position/`

## Validation Scenarios

### Scenario 1: Opportunity with Material Evidence Gaps (`HUMAN_REVIEW_REQUIRED`)

1. **Run Pipeline**:
   ```bash
   python scripts/generate_upwork_playbook.py --target config/target-position/upwork-senior-agentic-ai-architect.md
   ```
2. **Verify Output Artifacts**:
   - Check `out/upwork-senior-agentic-ai-architect/runtime/upwork-qualification.yaml`:
     - `submission_readiness` is `HUMAN_REVIEW_REQUIRED`
     - `machine_recommendation` is `EVIDENCE_GAPS`
     - `user_decision_state` is unforced / pending candidate decision
   - Check `out/upwork-senior-agentic-ai-architect/upwork-qualification-report.md`:
     - Contains clean, high-quality proposal prose based on verified architecture experience
     - Zero fabricated claims regarding live production deployment
     - Zero visible `[evidence]` tags or `[^footnote]` markers
   - Check `out/upwork-senior-agentic-ai-architect/upwork-evidence-gaps.md`:
     - Displays missing fact: `production_deployment_verification`
     - Lists candidate confirmation question: *"Was the WPP PCA/A2A system deployed to live production?"*

### Scenario 2: Evidence Improvement Loop & Regeneration (`SUBMISSION_READY`)

1. **Simulate Candidate Evidence Update**:
   - Add an evidence card to `out/okf/evidence-cards/` verifying live production deployment of the multi-agent system.
2. **Re-run Pipeline**:
   ```bash
   python scripts/generate_upwork_playbook.py --target config/target-position/upwork-senior-agentic-ai-architect.md
   ```
3. **Verify Updated Outcome**:
   - `upwork-qualification.yaml` updates `submission_readiness` to `SUBMISSION_READY`.
   - `upwork-qualification-report.md` automatically incorporates the verified production claim into proposal prose without manual text editing.

### Scenario 3: Automated Regression & Validation Suite

Run automated unit and contract tests:

```bash
pytest tests/test_upwork_proposal_generator.py -v
```

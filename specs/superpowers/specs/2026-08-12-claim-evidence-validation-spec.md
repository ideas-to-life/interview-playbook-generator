# Spec: Claim Strength & Evidence Scope Validation

## Objective

Strengthen the Career Projection Generator so that generated claims across resumes, cover letters, and briefs are constrained by the actual ownership, scope, domain, specificity, duration, and seniority supported by canonical evidence in `okf/`.

The system prevents semantic amplification where evidence of contribution to a capability is projected as leadership, ownership, or establishment of that capability.

## Governing Principles

1. **Evidence relevance does not imply evidence equivalence**: A claim may only be generated at the level of ownership, scope, specificity, duration, and seniority explicitly supported by its evidence.
2. **No inferred leadership from contribution**: When evidence supports contribution to a capability, the system must not infer leadership, ownership, establishment, or end-to-end responsibility for that capability.
3. **Project relevance aggressively, but project responsibility conservatively**.
4. **Complete Governance Chain**:
   Canonical identity determines who the candidate is $\rightarrow$ Evidence determines what the candidate has done $\rightarrow$ Claim-strength validation determines how strongly that experience may be stated $\rightarrow$ Target relevance determines what should be emphasised.

## Tech Stack & Commands

- **Language / Framework**: Python 3.13, Pytest, YAML, Markdown Skills specification.
- **Commands**:
  ```bash
  Test: pytest
  Lint: python -m pytest tests/test_lint.py
  Single Test: pytest tests/test_claim_evidence_validation.py
  ```

## Project Structure & Touched Files

```
skills/
├── projection-strategy-generator/SKILL.md → Formulate claim strength bounds & prohibit over-strength claims
├── projection-validator/SKILL.md         → Claim scope vector validation (PASS / DOWNGRADE / REJECT)
├── archetype-fit-validator/SKILL.md      → High-risk leadership verb & "from scratch" validation rules
├── resume-projection/SKILL.md             → Automatic claim downgrading and transferable domain framing
└── playbook-orchestrator/SKILL.md       → Pipeline integration for claim scope validation

AGENTS.md                                → Add new permanent governing principles
docs/superpowers/specs/2026-08-12-claim-evidence-validation-spec.md → Feature specification
tests/test_claim_evidence_validation.py  → Automated regression test suite for claim strength & evidence scope
```

## Claim Strength & Evidence Scope Model

### 1. Claim Strength Hierarchy
$$ \text{CONTRIBUTED} \rightarrow \text{SUPPORTED} \rightarrow \text{ADVISED} \rightarrow \text{DESIGNED} \rightarrow \text{LED} \rightarrow \text{OWNED} \rightarrow \text{ESTABLISHED} / \text{TRANSFORMED} $$

A claim MUST NOT exceed the evidence-supported strength level.

### 2. 6 Evidence Scope Dimensions (`ClaimScope`)
- **Ownership**: Participant $\le$ Contributor $\le$ Advisor $\le$ Designer $\le$ Lead $\le$ Owner $\le$ Established/Accountable
- **Scope**: Task $\le$ Workstream $\le$ Project $\le$ Programme $\le$ Function $\le$ Organisation $\le$ Enterprise $\le$ Multi-enterprise
- **Domain**: EA, Cloud, CCoE, AI, Governance, Tech Strategy, Data, Security, Transformation. (Adjacent domains must be framed as *transferable*, e.g., "Applied EA governance to CCoE initiatives", never domain-substituted).
- **Specificity**: General capability $\le$ Specific discipline $\le$ Operating model $\le$ Framework $\le$ Technology $\le$ Implementation
- **Duration**: Duration claims must be backed by evidence for that *specific capability* (not surrounding total career tenure).
- **Seniority**: Practitioner $\le$ Contributor $\le$ Senior Contributor $\le$ Lead $\le$ Principal/Strategic $\le$ Executive/Accountable

### 3. Claim Scope Vector Rule
$$ \text{ClaimScope} \le \text{EvidenceScope} $$

Evaluation Outcomes:
- **PASS**: Claim scope is $\le$ evidence scope.
- **DOWNGRADE**: Claim verb is automatically weakened to evidence-supported level during projection generation (e.g., replacing "Established CCoE" with "Contributed to CCoE governance"), and reported as `DOWNGRADE` in validation reports with diagnosis.
- **REJECT**: Claim cannot be safely expressed (no defensible lower-strength formulation exists), replaced with alternative evidence-backed claim.

### 4. High-Risk Terms & "From Scratch" Protection
- **High-Risk Leadership Verbs/Titles**: `Led`, `Owned`, `Established`, `Built`, `Founded`, `Created`, `Directed`, `Headed`, `Accountable for`, `CCoE Leader`, `Practice Lead`, `Programme Director`.
- **"From Scratch" Terms**: `from scratch`, `built from the ground up`, `established from inception`, `created the function`, `created the practice`, `set up the CoE`. (Require explicit evidence of initiation and establishment responsibility).

## Validation Report Schema (`out/<target-slug>/runtime/projection-validation-report.yaml`)

```yaml
claim_evidence_validation:
  status: "<PASSED | WARNING>"
  evaluated_claims:
    - claim: "<Generated claim prose>"
      evidence_id: "<source evidence id>"
      supported_strength: "<Contributor | Lead | Owner | Established>"
      claimed_strength: "<Leader | Established>"
      result: "<PASS | DOWNGRADE | REJECT>"
      downgraded_claim: "<Weakened claim prose if DOWNGRADE>"
      reason: "> Claim strength 'Established' exceeds evidence-supported strength 'Contributor'."
```

## Success Criteria

1. Evidence relevance and evidence equivalence are explicitly distinguished.
2. Claim strength, ownership, scope, domain, specificity, duration, and seniority are evaluated.
3. $\text{ClaimScope} \le \text{EvidenceScope}$ enforced across all projections.
4. Over-strength claims are automatically downgraded or rejected.
5. High-risk leadership verbs and "from scratch" claims require explicit establishment evidence.
6. Transferable experience across adjacent domains is framed accurately without domain substitution.
7. Validation report outputs diagnostic claim-evidence scope analysis.
8. `enterprise-cloud-architect` regression test suite passes all 20 acceptance criteria and canonical examples.
9. Zero regression on existing test suite.

## Boundaries

- **Always do**: Run `pytest` before committing; evaluate claim scope against canonical evidence.
- **Ask first**: Altering OKF core schema structures.
- **Never do**: Infer leadership, ownership, or duration from job title or candidate seniority alone; promote lower-strength evidence to higher-strength claims.

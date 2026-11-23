# Examples - cas-refactor-knowledge-links

## Example 1: Accepted

### Input

```yaml
input:
  target_root: "knowledge/projects/ideas-to-life-cas"
  relationship_request: "Add explicit links between the latest AW, AEM, AID, and alignment report."
  constraints: "Only add relationship metadata and a markdown Relationships section."
```

### Output

```yaml
output:
  feature:
    name: "connect-project-architecture-artefacts"
    module: "knowledge"
    description: "Adds explicit traceability links between project architecture artefacts."

  decision:
    status: accepted
    reason: "The current artefacts contain matching identifiers and explicit references that support deterministic links."
    alternative: "Leave the artefacts unlinked and rely on manual navigation."

  code_changes:
    - file: "knowledge/projects/ideas-to-life-cas/maps/aem-example.md"
      change_type: "modify"
      summary: "Added relationships metadata and a markdown Relationships section."

  architecture_decision:
    description: "Represent knowledge traceability as explicit artefact relationships."
    rationale: "Explicit links make the architecture workflow auditable and navigable without changing artefact meaning."

  architectural_impact:
    - affected_components: ["knowledge"]
      pattern_usage: ["contract-first-architecture", "structured-output-via-schema"]
      pattern_justification: "The relationship block is an explicit contract and keeps graph updates machine-readable."

  relationship_changes:
    - source: "aem-example"
      relationship: "derives_from"
      targets: ["aw-example"]
      evidence: "The AEM frontmatter and body identify the Architecture Work source."

  risks:
    - description: "Future artefacts may drift if generated without the same relationship contract."

  validation_notes:
    - description: "Verified relationship targets exist and markdown links match frontmatter values."
```

## Example 2: Proposed

### Input

```yaml
input:
  target_root: "knowledge/global/patterns"
  relationship_request: "Connect patterns back to ADRs where possible."
  constraints: "Do not infer links from similar titles alone."
```

### Output

```yaml
output:
  feature:
    name: "connect-patterns-to-decisions"
    module: "knowledge"
    description: "Assesses ADR-to-pattern traceability links."

  decision:
    status: proposed
    reason: "Some patterns have accepted ADR identifiers, but older ADRs lack pattern_id fields and need human confirmation before linking."
    alternative: "Link only patterns with explicit accepted ADR references and report unresolved candidates."

  code_changes:
    - file: "knowledge/global/patterns/example-pattern.md"
      change_type: "modify"
      summary: "Would add derives_from links for patterns with explicit ADR evidence only."

  architecture_decision:
    description: "Avoid title-based inference for governed pattern relationships."
    rationale: "Relationship metadata should remain evidence-backed so graph navigation does not imply false governance lineage."

  architectural_impact:
    - affected_components: ["knowledge"]
      pattern_usage: ["contract-first-architecture"]
      pattern_justification: "The decision preserves explicit contracts between ADRs and pattern records."

  relationship_changes:
    - source: "example-pattern"
      relationship: "derives_from"
      targets: ["adr-example"]
      evidence: "The pattern frontmatter references the ADR identifier."

  risks:
    - description: "Unmapped older ADRs remain disconnected until manually reviewed."

  validation_notes:
    - description: "Checked for explicit pattern_id or ADR references before proposing links."
```

## Example 3: Rejected

### Input

```yaml
input:
  target_root: "knowledge/projects"
  relationship_request: "Link every project artefact to every similarly dated global pattern."
  constraints: "Do not inspect global decisions."
```

### Output

```yaml
output:
  feature:
    name: "date-based-knowledge-linking"
    module: "knowledge"
    description: "Assesses broad date-based relationship generation."

  decision:
    status: rejected
    reason: "Similar dates are not sufficient evidence for governed knowledge relationships, and the requested constraints block ADR validation."
    alternative: "Scope to one project and add only links backed by explicit file references or frontmatter identifiers."

  code_changes:
    - file: "knowledge/projects"
      change_type: "none"
      summary: "No links added because the requested mapping would create unverifiable relationships."

  architecture_decision:
    description: "Reject unverifiable graph edges."
    rationale: "A knowledge graph is only useful when links reflect real architectural lineage or evaluation evidence."

  architectural_impact:
    - affected_components: ["knowledge"]
      pattern_usage: ["contract-first-architecture"]
      pattern_justification: "Governed links must be explicit contracts, not date-based guesses."

  relationship_changes: []

  risks:
    - description: "Leaving links absent is safer than adding misleading lineage."

  validation_notes:
    - description: "Rejected before implementation because required evidence was unavailable."
```

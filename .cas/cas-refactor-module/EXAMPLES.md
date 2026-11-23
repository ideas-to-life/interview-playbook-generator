# Examples — cas-refactor-module

## Example 1: Accepted

### Input

```yaml
input:
  target_path: "src/services/llm_reasoner.py"
  refactor_request: "Remove the hardcoded prompt path and inject prompt loading"
  constraints: "Do not change reasoning output or public method signatures"
```

### Output

```yaml
output:
  feature:
    name: "refactor-prompt-loading"
    module: "llm"
    description: "Externalises prompt loading logic"

  decision:
    status: accepted
    reason: "Improves separation of concerns"
    alternative: "Keep hardcoded path (rejected)"

  code_changes:
    - file: "llm.py"
      change_type: "modify"
      summary: "Inject prompt loader"

  architecture_decision:
    description: "Decouple prompt from reasoning logic"
    rationale: "Enables flexibility and maintainability"

  architectural_impact:
    - affected_components: ["llm"]
      pattern_usage: ["prompt-as-code-separation"]
      pattern_justification: "Separates prompt loading from reasoning code"

  risks:
    - description: "Incorrect prompt loading could break reasoning"

  validation_notes:
    - description: "Behaviour verified unchanged"
```

## Example 2: Rejected

### Input

```yaml
input:
  target_path: "src/router/router.py"
  refactor_request: "Merge router logic into a new API layer and change the response contract"
  constraints: "Keep the current external API stable"
```

### Output

```yaml
output:
  feature:
    name: "router-refactor"
    module: "router"
    description: "Assess router simplification"

  decision:
    status: rejected
    reason: "The requested refactor would change the observable response contract."
    alternative: "Keep the current router contract and extract only internal helpers."

  code_changes:
    - file: "src/router/router.py"
      change_type: "none"
      summary: "No safe refactor path under the requested constraints"

  architecture_decision:
    description: "Preserve the current router boundary"
    rationale: "Behaviour preservation takes precedence over structural consolidation"

  architectural_impact:
    - affected_components: ["router"]
      pattern_usage: ["contract-first-architecture"]
      pattern_justification: "Avoids contract-breaking structural changes"

  risks:
    - description: "No refactor applied because the requested change is not behaviour-safe"

  validation_notes:
    - description: "Rejected before implementation because the change would alter the API"
```

## Example 3: Proposed

### Input

```yaml
input:
  target_path: "src/pipeline/selection.py"
  refactor_request: "Introduce a reusable selection strategy abstraction"
  constraints: "Keep current behaviour and make the abstraction reusable across modules"
```

### Output

```yaml
output:
  feature:
    name: "selection-strategy-abstraction"
    module: "pipeline"
    description: "Assess reusable selection strategy extraction"

  decision:
    status: proposed
    reason: "A reusable abstraction appears beneficial, but it requires a new pattern not present in the catalogue."
    alternative: "Keep the current implementation and extract only local helpers."

  code_changes:
    - file: "src/pipeline/selection.py"
      change_type: "modify"
      summary: "Outline abstraction boundaries only"

  architecture_decision:
    description: "Separate selection mechanics from callers"
    rationale: "Supports reuse without committing to a new architectural pattern yet"

  architectural_impact:
    - affected_components: ["pipeline"]
      pattern_usage: ["typed-execution-context"]
      pattern_justification: "Provides the closest existing boundary, but a new reusable strategy pattern would still be required"

  risks:
    - description: "A new shared abstraction may be over-generalised"

  validation_notes:
    - description: "Behaviour should be compared against the current selection path before adoption"
```

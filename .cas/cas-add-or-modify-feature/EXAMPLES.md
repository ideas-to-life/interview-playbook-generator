# Examples — cas-add-or-modify-feature

---

## Example 1: Audit Logging Feature (Accepted)

**Context:** User wants to add audit logging to track login attempts for compliance purposes.

### Input

```yaml
input:
  feature_request: "Add audit logging to user login process"
  target_module: "auth"
  existing_context: "System already has a logging module in src/cas_runner/logging/"
```

### Output

```yaml
output:
  feature:
    name: "audit-logging-login"
    module: "auth"
    description: "Adds structured audit logging to track login attempts for compliance"

  decision:
    status: "accepted"
    reason: "Reuses existing logging infrastructure and preserves deterministic core boundaries"
    alternative: "Inline unstructured print statements in login handlers (rejected due to lack of schema contract)"

  code_changes:
    - file: "src/cas_runner/skills/auth/login.py"
      change_type: "modify"
      summary: "Inject audit logger call after authentication outcome"
    - file: "src/cas_runner/skills/auth/audit_logger.py"
      change_type: "create"
      summary: "Centralized structured audit event emitter using existing logging module"

  architecture_decision:
    description: "Emit schema-validated audit events through a dedicated audit logger module injected into the login flow"
    rationale: "Keeps authentication logic decoupled from audit persistence while enforcing structured compliance records"

  architectural_impact:
    - affected_components: ["auth", "logging"]
      pattern_usage: ["build-time-governance", "deterministic-core-selective-augmentation"]
      pattern_justification: "Satisfies deterministic-core-selective-augmentation invariants by keeping authentication and audit emission purely deterministic without external provider coupling."

  risks:
    - description: "Synchronous logging latency if underlying sink blocks"

  validation_notes:
    - description: "Verified against .cas/rules/architecture_rules.md and pattern invariants/anti_patterns: reuses existing logging infrastructure with no cross-layer imports."
```

---

## Example 2: User Profile API (Accepted)

**Context:** User wants to expose user profile data via a REST API endpoint.

### Input

```yaml
input:
  feature_request: "Expose user profile via REST API"
  target_module: "api"
  existing_context: "API layer exists in src/cas_runner/api/ with authentication middleware"
```

### Output

```yaml
output:
  feature:
    name: "user-profile-api"
    module: "api"
    description: "Provides GET /users/:id endpoint returning schema-validated user profile data"

  decision:
    status: "accepted"
    reason: "Conforms to contract-first API boundary and reuses existing authentication middleware"
    alternative: "Expose raw database user entities directly without a response schema (rejected)"

  code_changes:
    - file: "src/cas_runner/api/user_profile.py"
      change_type: "create"
      summary: "Endpoint handler and response schema contract for user profile retrieval"
    - file: "src/cas_runner/api/routes.py"
      change_type: "modify"
      summary: "Register GET /users/:id route behind authentication middleware"

  architecture_decision:
    description: "Expose user profiles through a typed API response contract decoupled from internal storage models"
    rationale: "Prevents internal storage schema changes from breaking external API consumers"

  architectural_impact:
    - affected_components: ["api", "user-service"]
      pattern_usage: ["contract-first-architecture", "schema-enforced-domain-contracts"]
      pattern_justification: "Satisfies contract-first-architecture invariants by defining an explicit typed response schema between the API layer and domain service."

  risks:
    - description: "Potential PII exposure if authentication middleware is bypassed"

  validation_notes:
    - description: "Verified against contract-first-architecture invariants and anti_patterns: no untyped dicts or cross-layer private imports introduced."
```

---

## Example 3: Multi-Provider LLM Gateway Integration (Accepted)

**Context:** An onboarded project needs live LLM inference (supporting Gemini, Anthropic, OpenAI, and Ollama) behind its `ArchitectureReasoner` protocol while keeping unit tests 100% deterministic and offline.

### Input

```yaml
input:
  feature_request: "Add live LLM inference support alongside offline mock testing"
  target_module: "engagement_intake"
  existing_context: "Project defines ArchitectureReasoner protocol and MockArchitectureReasoner"
```

### Output

```yaml
output:
  feature:
    name: "unified-llm-gateway-integration"
    module: "engagement_intake"
    description: "Integrates a provider-agnostic LLM client gateway (LiteLLMClient + MockLLMClient) behind ArchitectureReasoner with declarative provider/model routing"

  decision:
    status: "accepted"
    reason: "Satisfies provider-agnostic-llm-client invariants by routing all live calls through a single unified multi-provider gateway configured via provider/model strings, paired with a deterministic offline mock client"
    alternative: "Create vendor-specific adapter classes per provider such as providers/gemini.py with google-genai SDK (rejected as a prohibited anti-pattern)"

  code_changes:
    - file: "src/ea4all/engagement_intake/llm/base.py"
      change_type: "create"
      summary: "Define abstract LLMClient interface, LLMResponse, and LLMUsage contracts"
    - file: "src/ea4all/engagement_intake/llm/litellm_client.py"
      change_type: "create"
      summary: "Implement unified LiteLLMClient routing provider/model strings across vendors with environment-based credential resolution"
    - file: "src/ea4all/engagement_intake/llm/mock_client.py"
      change_type: "create"
      summary: "Implement deterministic MockLLMClient for zero-cost offline testing"
    - file: "src/ea4all/engagement_intake/config.py"
      change_type: "modify"
      summary: "Add declarative ExecutionProfile (provider, model, temperature, max_tokens, api_base)"
    - file: "requirements.txt"
      change_type: "modify"
      summary: "Add litellm unified router dependency (no vendor-specific SDKs)"

  architecture_decision:
    description: "Route all live LLM invocations through a single unified LiteLLMClient conforming to LLMClient, parameterized by declarative provider/model configuration"
    rationale: "Eliminates vendor SDK lock-in and N-adapter proliferation; switching between Gemini, Claude, OpenAI, or Ollama requires only changing config.yaml or environment variables"

  architectural_impact:
    - affected_components: ["engagement_intake.llm", "engagement_intake.reasoning", "engagement_intake.config"]
      pattern_usage: ["provider-agnostic-llm-client", "provider-agnostic-llm-gateway", "deterministic-mock-evaluation-harness", "prompt-as-code-separation"]
      pattern_justification: "Strictly satisfies provider-agnostic-llm-client invariants: single multi-provider router adapter, deterministic mock test double, and zero vendor-specific SDK dependencies."

  risks:
    - description: "Transient rate limits or provider outages during live execution; mitigated by centralized gateway retry backoff and graceful fallback"

  validation_notes:
    - description: "Checked against provider-agnostic-llm-client invariants and anti_patterns: no vendor-specific adapter files (e.g., gemini.py) and no direct vendor SDKs in requirements.txt."
```

---

## Example 4: Single-Vendor LLM Adapter Coupling (Rejected)

**Context:** User or agent proposes wiring Google Gemini directly by creating `providers/gemini.py`, adding `google-genai` to `requirements.txt`, and hardcoding `--reasoner choices={mock,gemini}`.

### Input

```yaml
input:
  feature_request: "Add live Gemini LLM provider in providers/gemini.py using google-genai SDK and --reasoner gemini CLI flag"
  target_module: "engagement_intake"
  existing_context: "Project is governed by CAS rules and patterns-catalogue.yaml"
```

### Output

```yaml
output:
  feature:
    name: "gemini-specific-llm-adapter"
    module: "engagement_intake"
    description: "Proposed single-vendor Gemini adapter using google-genai SDK"

  decision:
    status: "rejected"
    reason: "Violates provider-agnostic-llm-client invariants and directly triggers its listed anti_patterns: creating a vendor-specific adapter module (providers/gemini.py), adding a direct vendor SDK (google-genai) to requirements.txt, and hardcoding vendor CLI choices ({mock, gemini})."
    alternative: "Implement a unified multi-provider gateway (LiteLLMClient + MockLLMClient) behind LLMClient where 'gemini/gemini-2.5-flash' or any other provider/model is selected declaratively via config.yaml and standard environment variables."

  code_changes: []

  architecture_decision:
    description: "Reject single-vendor LLM adapter proliferation in favor of a unified multi-provider LLM gateway"
    rationale: "Wrapping a single vendor SDK inside a local Port/Adapter still locks runtime dependencies to one vendor and forces N-adapter duplication for structured outputs, retries, and telemetry across additional providers."

  architectural_impact:
    - affected_components: ["engagement_intake.reasoning", "engagement_intake.config"]
      pattern_usage: ["provider-agnostic-llm-client", "build-time-governance"]
      pattern_justification: "Enforces provider-agnostic-llm-client anti_patterns at build time to block vendor SDK coupling before code is written."

  risks:
    - description: "Proceeding with a vendor-specific adapter would create immediate architectural drift and require rework to support additional LLM providers."

  validation_notes:
    - description: "Rejected during Step 3 validation against .cas/patterns/patterns-catalogue.yaml (provider-agnostic-llm-client anti_patterns)."
```

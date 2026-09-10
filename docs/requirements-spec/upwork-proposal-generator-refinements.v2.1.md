FEATURE: Human-Owned Opportunity Decision & Evidence-Gap Handling
PURPOSE
Extend the Upwork Proposal Generator so that it distinguishes between:
1. evidence integrity — which remains a hard machine-enforced boundary; and
2. application decision — which remains the human user's responsibility.
The system must never fabricate, infer, or silently strengthen career evidence. However, incomplete evidence MUST NOT by itself prevent the system from generating useful, evidence-safe opportunity analysis and proposal artefacts.
The system should therefore operate as an evidence-governed decision-support copilot rather than an autonomous application gatekeeper.
The user remains the ultimate decision maker on whether to apply.
This feature builds on the merged Evidence Integrity Contract V2.0 and MUST NOT weaken, bypass, or reinterpret any V2.0 evidence-integrity invariant.
CORE PRINCIPLE
The system owns truthfulness.
The human owns the application decision.
Evidence gaps must be surfaced, not filled.
Unsupported claims must be excluded or explicitly marked as unresolved.
The presence of an evidence gap must not automatically suppress useful artefact generation.
PROBLEM
The current V2.0 implementation correctly prevents an opportunity with an explicit production dealbreaker from reaching proposal generation when production evidence is unknown.
That behaviour successfully fixed the original false-APPLY defect, but it is too restrictive for the broader intended workflow.
Real career evidence is necessarily incomplete.
Examples include:
- an experience was performed but has not yet been captured in the canonical knowledge base;
- a technology was used but the source evidence does not currently contain it;
- production status is known by the user but has not yet been formally documented;
- an approximate scale or count is known by the user but has not yet been captured;
- a business outcome exists but has not yet been documented;
- an opportunity asks for a specific detail that the current evidence does not establish.
The system must not turn these gaps into fabricated claims.
However, it should still help the user evaluate and prepare the opportunity.
GOALS
G-01
Generate useful opportunity-analysis and proposal artefacts from existing canonical evidence even when some requirements are unsupported or unresolved.
G-02
Never fabricate or infer missing career evidence.
G-03
Make evidence gaps explicit and actionable.
G-04
Distinguish evidence-supported content from unresolved facts and user confirmation requirements.
G-05
Allow the user to make the final APPLY / DO NOT APPLY decision.
G-06
Preserve all Evidence Integrity Contract V2.0 protections.
G-07
Allow the user to improve canonical evidence after reviewing an opportunity and then regenerate deterministic artefacts.
G-08
Ensure that generated client-facing prose never presents an unresolved requirement as established fact.
NON-GOALS
NG-01
Do not automate Upwork submission.
NG-02
Do not automate clicking, Connects, marketplace interaction, or browser submission.
NG-03
Do not weaken production evidence requirements.
NG-04
Do not infer production status from employment, repository names, metrics, project names, technology names, or other contextual signals.
NG-05
Do not allow personal projects to satisfy real-company production requirements.
NG-06
Do not allow cross-organisation or cross-project evidence composition.
NG-07
Do not invent plausible answers merely to complete screening questions.
NG-08
Do not make the system the final authority on whether an opportunity should be pursued.
FUNCTIONAL REQUIREMENTS
FR-01 — Preserve Evidence Integrity V2.0
All V2.0 evidence-integrity requirements and architectural invariants remain authoritative.
This feature MUST NOT modify the meaning of:
- organisation identity;
- project identity;
- environment;
- production verification;
- implementation responsibility;
- provenance;
- evidence strength;
- cross-organisation isolation;
- cross-project isolation;
- personal-project isolation;
- explicit production verification;
- prohibited inference paths.
FR-02 — Evidence Completeness Classification
For each material opportunity requirement, the system MUST classify the current evidence independently from the final application decision.
Minimum classifications:
- SUPPORTED
- PARTIALLY_SUPPORTED
- UNKNOWN
- CONTRADICTED
Definitions:
SUPPORTED:
Canonical evidence directly supports the requirement sufficiently for client-facing use.
PARTIALLY_SUPPORTED:
Canonical evidence supports a meaningful portion of the requirement but does not establish all requested details.
UNKNOWN:
The canonical evidence does not establish whether the requirement is satisfied.
CONTRADICTED:
Canonical evidence explicitly indicates that the claimed requirement is not satisfied or conflicts with the requested condition.
The classification MUST NOT manufacture evidence.
FR-03 — Evidence Gap Identification
For every material requirement classified as PARTIALLY_SUPPORTED or UNKNOWN, the system MUST identify the specific missing fact where practical.
Examples:
- production deployment status;
- implementation role;
- agent count;
- workflow count;
- technology used;
- business outcome;
- scale;
- dates;
- client/project context;
- quantified result.
The system MUST NOT guess the missing value.
FR-04 — Human Confirmation Questions
Where a material evidence gap could reasonably be resolved by the user, the system SHOULD generate an explicit internal confirmation question.
Examples:
- "Was the WPP PCA/A2A system deployed to production?"
- "What was your personal implementation role?"
- "Approximately how many agents/workflows were involved?"
- "What measurable business outcome resulted?"
Questions MUST be based on the opportunity requirement and the actual evidence gap.
They MUST NOT assume that the missing fact is true.
FR-05 — Separation of Evidence and Decision
Evidence completeness MUST NOT be equivalent to application decision.
The system MUST maintain separate concepts for:
- evidence status;
- opportunity fit;
- application recommendation;
- proposal generation state;
- human application decision.
A requirement may be UNKNOWN without the system asserting that the user is unqualified.
FR-06 — Human-Owned Final Decision
The final decision to apply MUST remain with the user.
The system MAY provide a recommendation such as:
- STRONG_FIT
- POTENTIAL_FIT
- EVIDENCE_GAPS
- WEAK_FIT
- CLEAR_MISMATCH
but these recommendations MUST NOT represent an irreversible application decision.
The system MUST communicate that the user remains responsible for the final decision.
FR-07 — Evidence-Safe Proposal Generation
When proposal generation is permitted, the proposal MUST be generated exclusively from:
1. canonical evidence that supports the claim; and
2. opportunity-specific language that does not make unsupported career assertions.
The generator MUST NOT use UNKNOWN or PARTIALLY_SUPPORTED evidence as if it were SUPPORTED.
FR-08 — Explicit Handling of Unsupported Dealbreakers
An explicit client dealbreaker with UNKNOWN or PARTIALLY_SUPPORTED evidence MUST be surfaced prominently as an evidence gap.
The system MUST NOT state or imply that the candidate satisfies the dealbreaker.
However, the evidence gap MUST NOT automatically suppress all useful proposal artefacts solely because the evidence is incomplete.
The generated artefacts MUST make the unresolved condition visible to the human reviewer.
Example:
"Production multi-agent implementation: current canonical evidence does not establish production deployment."
NOT:
"I have production multi-agent implementation experience."
FR-09 — Contradicted Requirements
If canonical evidence explicitly contradicts a requirement, the system MUST NOT generate client-facing content claiming that the requirement is satisfied.
The system MAY still generate:
- opportunity analysis;
- evidence-gap analysis;
- a safe proposal draft based on other supported experience;
- internal human-review notes.
The contradiction MUST be surfaced clearly.
FR-10 — Screening Question Integrity
Screening questions MUST be answered only where supported by canonical evidence.
For an unresolved question, the system MUST NOT fabricate an answer.
It SHOULD generate one of:
- an evidence-safe answer that explicitly states the limitation;
- an internal `[OPEN CONDITION: ...]`;
- an internal "requires user confirmation" item.
The system MUST distinguish internal review markers from client-facing prose.
No invented yes/no answer is permitted.
FR-11 — Quantitative Claim Integrity
Quantitative claims MUST continue to satisfy V2.0 evidence requirements.
The system MUST NOT invent:
- agent counts;
- workflow counts;
- percentages;
- latency;
- cost savings;
- productivity improvements;
- throughput;
- headcount reduction;
- accuracy;
- business impact;
- scale.
Where a requested quantitative fact is unavailable, the system MUST surface the gap.
It MAY use qualitative evidence that is actually supported.
FR-12 — Proposal Content Modes
Proposal generation SHOULD support at least these conceptual content modes:
EVIDENCE_BACKED:
All material candidate claims are supported by canonical evidence.
EVIDENCE_GAPS:
The proposal can be generated, but one or more material requirements remain unresolved.
HUMAN_REVIEW_REQUIRED:
The artefact contains explicit unresolved conditions requiring user confirmation before submission.
These modes MUST NOT permit unsupported claims.
FR-13 — Evidence Gap Report
When material gaps exist, the generated package SHOULD include an evidence-gap section or companion artefact containing:
- requirement;
- evidence status;
- what is established;
- what is missing;
- relevant canonical evidence;
- user confirmation question, where applicable;
- impact on application suitability.
The purpose is decision support, not automatic rejection.
FR-14 — Proposal Safety Boundary
The proposal generator MUST distinguish between:
A. statements that can safely appear in client-facing prose; and
B. internal evidence-gap / human-confirmation information.
Internal provenance markers, evidence IDs, or implementation diagnostics MUST NOT leak into client-facing prose unless explicitly required by the target platform or user.
FR-15 — Work Sample Generation
Work samples MAY still be generated when evidence gaps exist, provided each work sample is independently evidence-backed.
A work sample MUST NOT be selected or described as satisfying an unresolved hard requirement.
Personal projects MUST remain clearly identified as personal projects.
Prototype/innovation work MUST remain clearly identified as prototype/innovation work.
FR-16 — Human Review Package
When evidence gaps exist, the system SHOULD produce a review package containing:
- opportunity fit summary;
- supported requirements;
- partial requirements;
- unknown requirements;
- contradicted requirements;
- evidence-backed proposal;
- screening answers or unresolved screening questions;
- recommended work samples;
- open questions for the user;
- material risks or caveats.
FR-17 — Regeneration After Evidence Update
If the user subsequently updates canonical evidence, the system MUST be able to regenerate the opportunity artefacts from the updated evidence.
The regeneration MUST be deterministic with respect to the same inputs and configuration.
The system MUST NOT require manual editing of generated proposal artefacts to incorporate newly captured evidence.
FR-18 — Evidence Improvement Loop
The workflow SHOULD support this lifecycle:
Opportunity
→ identify evidence gap
→ user confirms or supplies fact
→ canonical evidence updated
→ evidence validation
→ opportunity re-evaluated
→ proposal regenerated
→ human review.
The proposal generator MUST NOT itself silently promote user-confirmed facts into canonical evidence without the established knowledge-ingestion/governance process.
FR-19 — Recommendation Transparency
Any fit or application recommendation MUST expose the principal factors supporting it.
The recommendation SHOULD distinguish:
- evidence-supported strengths;
- evidence gaps;
- contradictions;
- material opportunity risks;
- assumptions requiring user confirmation.
The system MUST NOT represent an evidence-gap-driven recommendation as a factual statement about the user's career.
FR-20 — No Automatic Application Decision
The system MUST NOT treat:
DO NOT APPLY
as an irreversible machine decision unless required by an explicit safety/integrity rule.
Where V2.0 previously used a hard gate specifically to prevent unsupported claims, the new behaviour MUST preserve the integrity boundary while allowing evidence-safe decision-support artefacts.
The machine's responsibility is to prevent fabrication and clearly expose uncertainty.
The user's responsibility is to decide whether to apply.
FR-21 — Validation
Independent validation MUST verify that:
- every material candidate claim has supporting evidence or is explicitly qualified;
- no UNKNOWN evidence has been represented as fact;
- no PARTIALLY_SUPPORTED evidence has been represented as complete;
- no CONTRADICTED evidence has been represented as satisfied;
- production claims meet V2.0 production verification requirements;
- organisation/project boundaries remain intact;
- personal/prototype evidence is not upgraded;
- quantitative claims remain evidence-backed;
- screening answers do not fabricate;
- work samples remain evidence-backed;
- human-review/open-condition information is correctly separated from client-facing prose.
FR-22 — Validation Failure
If generated artefacts contain unsupported assertions, validation MUST fail them.
The system MUST require correction/regeneration before the artefact is considered submission-ready.
Validation failure MUST NOT be resolved by weakening evidence requirements.
FR-23 — Submission Readiness
An artefact MAY be labelled:
SUBMISSION_READY
only when all client-facing claims are evidence-safe and all material unresolved conditions are either:
- explicitly and safely disclosed; or
- resolved by canonical evidence.
An artefact containing unresolved material requirements MAY instead be labelled:
HUMAN_REVIEW_REQUIRED
It MUST NOT be labelled submission-ready merely because the prose sounds plausible.
FR-24 — User Decision State
The workflow SHOULD support a final human decision state distinct from qualification:
- APPLY
- DO_NOT_APPLY
- HOLD_FOR_EVIDENCE
This state represents the user's decision, not an inferred career fact.
The system MAY recommend a state but MUST NOT silently set the final human decision.
FR-25 — Auditability
The system MUST retain sufficient machine-readable information to explain:
- which evidence supported each material claim;
- which requirements were unresolved;
- why a requirement was classified as UNKNOWN/PARTIALLY_SUPPORTED/CONTRADICTED;
- which human confirmation questions were generated;
- which proposal content was generated from supported evidence;
- which validation checks passed or failed.
ARCHITECTURAL INVARIANTS
AI-generated prose MUST NEVER strengthen canonical evidence.
Evidence completeness and application decision are separate domains.
The qualification/evidence layer owns truthfulness.
The projection layer owns transformation of supported evidence into useful artefacts.
The human owns the final application decision.
Unknown is not equivalent to false.
Unknown is not equivalent to true.
Partial evidence is not complete evidence.
Contradicted evidence cannot be presented as satisfied.
Production status remains explicitly attested and MUST NOT be inferred.
Employment does not establish production implementation.
Repository names do not establish production implementation.
Metrics do not establish production deployment.
Personal projects do not establish real-company production experience.
Prototype/PoC/innovation work does not establish production experience unless explicit production evidence exists.
Cross-organisation evidence composition remains prohibited.
Cross-project evidence composition remains prohibited.
Validation remains independent and cross-cutting.
Human review remains the final boundary before submission.
PROPOSED ACCEPTANCE CRITERIA
AC-01
Given an opportunity with complete supporting evidence, the system generates an evidence-backed proposal package.
AC-02
Given an opportunity with an UNKNOWN material requirement, the system identifies the evidence gap and does not fabricate an answer.
AC-03
Given an explicit client production dealbreaker with UNKNOWN production evidence, the system does not claim production experience and does not fabricate a production answer.
AC-04
Given an explicit client production dealbreaker with UNKNOWN evidence, the system MAY generate an evidence-safe proposal and review package, provided the unresolved condition is clearly surfaced and no unsupported claim is made.
AC-05
Given an explicit client production dealbreaker with VERIFIED_NON_PRODUCTION evidence, the system does not represent the experience as production.
AC-06
Given an explicit client production dealbreaker with VERIFIED_PRODUCTION evidence and compatible implementation responsibility, the system may use that evidence in proposal generation.
AC-07
Given an opportunity requiring a specific agent count when the count is unknown, the system does not invent a count.
AC-08
Given an opportunity requiring a measurable outcome when no canonical metric exists, the system does not invent a metric and instead surfaces the evidence gap.
AC-09
Given an opportunity requiring a technology not present in canonical evidence, the system does not claim that the user used that technology.
AC-10
Given an UNKNOWN requirement, the system may generate an internal user-confirmation question without treating the answer as known.
AC-11
Given a screening question that cannot be answered from canonical evidence, the system does not generate a fabricated yes/no answer.
AC-12
Given evidence from a personal project and an employer project, the system does not combine them to create a stronger claim.
AC-13
Given evidence from different employer projects, the system does not combine them to satisfy a project-specific requirement.
AC-14
Given a contradicted requirement, the system does not generate a client-facing claim that the requirement is satisfied.
AC-15
Given evidence gaps, the system generates an explicit evidence-gap/review representation.
AC-16
Given a user updates canonical evidence to resolve a previously unknown requirement, regeneration incorporates the new evidence without manually editing generated artefacts.
AC-17
Independent validation rejects any client-facing claim that is not supported by canonical evidence or explicitly qualified.
AC-18
The system distinguishes the machine's evidence assessment from the user's final application decision.
AC-19
The system can generate a useful proposal draft even when one or more material requirements remain unresolved, provided the draft contains no unsupported assertions.
AC-20
The system does not automatically submit an application.
AC-21
For the previously failing Senior Agentic AI Architect opportunity, the system no longer generates a fabricated production claim. It may generate a human-review proposal package that accurately states the documented WPP experience and explicitly identifies production deployment as unresolved.
AC-22
The user can make the final decision to APPLY, DO_NOT_APPLY, or HOLD_FOR_EVIDENCE after reviewing the generated evidence and gaps.
REGRESSION REQUIREMENTS
The implementation MUST retain all V2.0 regression tests.
Additional regression scenarios SHOULD include:
R-01
Production requirement UNKNOWN → proposal contains no production claim, but evidence-gap package is generated.
R-02
Production requirement UNKNOWN → screening answer does not claim production.
R-03
Agent count UNKNOWN → no invented agent count.
R-04
Outcome UNKNOWN → no invented percentage or business result.
R-05
Technology UNKNOWN → no invented technology claim.
R-06
User confirmation supplied → canonical evidence update followed by regeneration produces newly supported claim.
R-07
User confirmation not supplied → proposal remains evidence-safe and explicitly identifies the unresolved condition.
R-08
Contradicted requirement → proposal cannot claim satisfaction.
R-09
Personal project + employer evidence → no evidence strengthening through composition.
R-10
Cross-project evidence → no evidence strengthening through composition.
R-11
Existing V2.0 false-APPLY scenario remains protected against fabricated production claims.
R-12
A fully supported APPLY scenario remains capable of producing a normal proposal package.
R-13
A non-dealbreaker evidence gap does not unnecessarily block proposal generation.
R-14
Human final decision state remains distinct from machine evidence classification.
SUCCESS CRITERIA
The feature is successful when the system can simultaneously demonstrate:
1. It never fabricates missing career evidence.
2. It identifies exactly what is known and unknown.
3. It produces useful artefacts despite incomplete evidence.
4. It explicitly surfaces material gaps requiring human confirmation.
5. It never represents an unresolved dealbreaker as satisfied.
6. It preserves all V2.0 evidence-integrity protections.
7. The user remains the final decision maker.
8. Updated canonical evidence can improve future opportunity projections.
9. Independent validation continues to prevent unsupported client-facing claims.
10. The system remains useful even when the user's canonical career knowledge is incomplete.
DESIRED END-TO-END BEHAVIOUR
The preferred workflow is:
Opportunity
→ Opportunity Analysis
→ Evidence Retrieval
→ Evidence Completeness Assessment
→ Evidence-Gap Analysis
→ Safe Projection
→ Independent Validation
→ Human Review
→ User Decision
Possible user decision:
APPLY
DO_NOT_APPLY
HOLD_FOR_EVIDENCE
The system's job is not to decide whether the user deserves to apply.
Its job is to produce the strongest defensible application package possible from the evidence available, make uncertainty visible, prevent fabrication, and give the user enough information to make the final decision.

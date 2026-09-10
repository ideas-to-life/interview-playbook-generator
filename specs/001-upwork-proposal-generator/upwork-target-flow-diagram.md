# Upwork Target Flow Architecture

This diagram visualizes the end-to-end processing pipeline for an Upwork opportunity across the platform's 4 architectural layers, qualification control boundary, validation gate, and human review boundary.

```mermaid
flowchart TD
    subgraph Inputs["INPUTS & CONFIGURATION"]
        JobDesc["Upwork Job Description\n(inputs/upwork-jd.md)"]
        TargetConfig["Target Configuration\n(target_type: upwork)"]
    end
    subgraph KnowledgeLayer["1. KNOWLEDGE LAYER (out/okf/)"]
        OKF["Canonical Career Evidence\n• Evidence Cards\n• Signature Achievements\n• Capabilities\n• Story Library\n• Executive Identity\n• Messaging / Narrative"]
    end
    subgraph RuntimeLayer["2. RUNTIME LAYER (out/<target-slug>/runtime/)"]
        OppAnalyzer["opportunity-analyzer\n(existing)"]
        OppAnalysisYaml["opportunity-analysis.yaml"]
        QualSkill["upwork-qualification\n(runtime capability)"]
        QualYaml["upwork-qualification.yaml\n• decision\n• proposal_generation\n• requirement assessment\n• evidence / claim traceability\n• production status\n• rationale"]
    end
    subgraph QualificationGate["QUALIFICATION CONTROL BOUNDARY"]
        Gate{"Qualification Decision"}
    end
    subgraph CoachingLayer["3. COACHING LAYER"]
        Coaching["Opportunity-Aware Strategy\n(existing capabilities where applicable)\n• Positioning\n• Emphasis Areas\n• Gap Awareness\n• Proposal Strategy (internal)"]
    end
    subgraph ProjectionLayer["4. PROJECTION LAYER (out/<target-slug>/)"]
        ProjRegistry["projection-registry\n(existing)"]
        ProposalSkill["upwork-proposal\n(projection capability)"]
        CleanProposal["upwork-qualification-report.md\nClean client-facing prose\n350–500 words target"]
        ScreeningAnswers["upwork-screening-answers.md\nDirect answers + evidence\nExplicit open conditions if conditional"]
        WorkSamples["upwork-work-samples.md\nMaximum 3 relevant samples\nEvidence-backed + externally suitable"]
        GateReport["upwork-qualification-report.md\n• Blocking Requirement\n• Evidence Gap\n• Decision Rationale\n• What Would Change Decision"]
    end
    subgraph ValidationGate["VALIDATION & QUALITY GATE"]
        Validator["projection-validator\n(existing, extended)"]
        ValReport["projection-validation-report.yaml\n• Qualification Gate Compliance\n• Evidence Integrity\n• Claim Traceability\n• Structure / Constraint Checks\n• Screening Coverage\n• Work-Sample Validation"]
        ValidationDecision{"Validation Passed?"}
    end
    subgraph HumanBoundary["HUMAN REVIEW BOUNDARY"]
        HumanReview["Human Candidate Review\n• Review Generated Artifacts\n• Verify Open Conditions\n• Assess Evidence / Positioning\n• Final Copy & Strategy Check"]
        HumanSubmit["Human Upwork Submission\nExternal Action\nManual — no automation in V1"]
    end
    %% Input and Knowledge Flow
    JobDesc --> OppAnalyzer
    TargetConfig --> OppAnalyzer
    OppAnalyzer --> OppAnalysisYaml
    OKF -->|Governed, relevant evidence| QualSkill
    OppAnalysisYaml --> QualSkill
    QualSkill --> QualYaml
    QualYaml --> Gate
    %% Qualification Decision Paths
    Gate -->|DO NOT APPLY| DoNotApply["DO NOT APPLY\nproposal_generation: blocked"]
    Gate -->|CONDITIONAL| Conditional["CONDITIONAL\nproposal_generation: allowed_with_conditions"]
    Gate -->|APPLY| Apply["APPLY\nproposal_generation: allowed"]
    %% Blocked Path
    DoNotApply --> GateReport
    GateReport --> HumanReview
    %% Qualified Paths
    Conditional --> ProjRegistry
    Apply --> ProjRegistry
    %% Coaching / Strategy
    QualYaml --> Coaching
    OppAnalysisYaml --> Coaching
    OKF --> Coaching
    Coaching --> ProposalSkill
    ProjRegistry --> ProposalSkill
    OKF -->|Approved evidence boundary| ProposalSkill
    QualYaml -->|Qualification boundary| ProposalSkill
    %% Projection Outputs
    ProposalSkill --> CleanProposal
    ProposalSkill --> ScreeningAnswers
    ProposalSkill --> WorkSamples
    %% All projection artifacts enter validation
    CleanProposal --> Validator
    ScreeningAnswers --> Validator
    WorkSamples --> Validator
    QualYaml --> Validator
    Validator --> ValReport
    ValReport --> ValidationDecision
    %% Validation Gate
    ValidationDecision -->|PASS| HumanReview
    ValidationDecision -->|FAIL| Correction["Correction / Regeneration\nWithin governed evidence boundary"]
    Correction --> ProposalSkill
    %% Human Boundary
    HumanReview --> HumanSubmit
    %% Styling
    classDef inputStyle fill:#e1f5fe,stroke:#0288d1,stroke-width:1px;
    classDef okfStyle fill:#fff3e0,stroke:#f57c00,stroke-width:1px;
    classDef runtimeStyle fill:#e8f5e9,stroke:#388e3c,stroke-width:1px;
    classDef gateStyle fill:#fffde7,stroke:#fbc02d,stroke-width:2px;
    classDef blockStyle fill:#ffebee,stroke:#d32f2f,stroke-width:2px;
    classDef applyStyle fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef conditionalStyle fill:#fff8e1,stroke:#f9a825,stroke-width:2px;
    classDef coachingStyle fill:#fff3e0,stroke:#ef6c00,stroke-width:1px;
    classDef projStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:1px;
    classDef evalStyle fill:#ede7f6,stroke:#512da8,stroke-width:1px;
    classDef validationGateStyle fill:#f5f0ff,stroke:#6a1b9a,stroke-width:2px;
    classDef humanStyle fill:#e0f2f1,stroke:#00796b,stroke-width:2px;
    classDef correctionStyle fill:#fff3e0,stroke:#e65100,stroke-width:1px;
    class JobDesc,TargetConfig inputStyle;
    class OKF okfStyle;
    class OppAnalyzer,OppAnalysisYaml,QualSkill,QualYaml runtimeStyle;
    class Gate gateStyle;
    class DoNotApply blockStyle;
    class Apply applyStyle;
    class Conditional conditionalStyle;
    class Coaching coachingStyle;
    class ProjRegistry,ProposalSkill,CleanProposal,ScreeningAnswers,WorkSamples,GateReport projStyle;
    class Validator,ValReport evalStyle;
    class ValidationDecision validationGateStyle;
    class HumanReview,HumanSubmit humanStyle;
    class Correction correctionStyle;
```

## Key Architectural Invariants

1. Four-Layer Architecture: Upwork processing conforms to the existing Knowledge, Runtime, Coaching, and Projection layers. Validation is a cross-cutting quality gate, not a fifth architectural layer.
2. Qualification Control Boundary: Qualification is a hard downstream control. Proposal projection cannot override the qualification result:
    * DO NOT APPLY → proposal_generation: blocked
    * CONDITIONAL → proposal_generation: allowed_with_conditions
    * APPLY → proposal_generation: allowed
3. Qualification Evidence vs Projection Evidence: Qualification determines whether the opportunity can legitimately be pursued. Projection selects persuasive evidence only within the evidence boundary established by qualification.
4. Production Evidence Integrity: Production experience, prototype/innovation experience, personal projects, and theoretical knowledge remain explicitly distinct. The system must never infer production status from technical similarity or sophistication.
5. Single Source of Career Evidence: Canonical career evidence remains in the OKF Knowledge Layer. The Upwork feature does not create a second career or evidence repository.
6. Clean Client Prose: upwork-qualification-report.md contains natural, professional client-facing prose. Internal provenance, evidence relationships, validation metadata, and qualification state remain in structured/runtime context rather than being exposed as machine-readable tags in the proposal.
7. DO NOT APPLY Is Not a Failure: A blocked opportunity produces a qualification/gate report, not a submission-ready proposal. The gate report is deliberately separate from upwork-qualification-report.md.
8. Validation Is a Quality Gate: All projection artifacts—including the proposal, screening answers, and work-sample recommendations—pass through projection-validator before reaching human review.
9. Validation Failure Does Not Bypass Governance: Failed outputs return for correction/regeneration within the same qualification and evidence boundaries. Validation cannot expand the evidence boundary or change the qualification decision.
10. Human Review Boundary: The system ends with human-reviewable artifacts. Final submission to Upwork remains a human action. No automated browser interaction, scraping, or proposal submission is performed in V1.
11. CAS / SLDC Governance: Processing is bounded, evidence-grounded, traceable, deterministic where applicable, and integrated with the existing repository lifecycle and validation mechanisms.

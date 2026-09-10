# Upwork Target Flow Architecture

This diagram visualizes the end-to-end processing pipeline for an Upwork opportunity across the platform's 4 architectural layers, control gate boundaries, and human review interface.

```mermaid
flowchart TD
    subgraph Inputs["1. INPUTS & CONFIGURATION"]
        JobDesc["Upwork Job Description\n(inputs/upwork-jd.md)"]
        TargetConfig["Target Configuration\n(target_type: upwork)"]
    end

    subgraph KnowledgeLayer["2. KNOWLEDGE LAYER (out/okf/)"]
        OKF["Canonical Career Evidence\n• Evidence Cards\n• Signature Achievements\n• Capabilities\n• Story Library"]
    end

    subgraph RuntimeLayer["3. RUNTIME LAYER (out/<target-slug>/runtime/)"]
        OppAnalyzer["opportunity-analyzer"]
        OppAnalysisYaml["opportunity-analysis.yaml"]
        
        QualSkill["upwork-qualification\n(skills/upwork-qualification/)"]
        QualYaml["upwork-qualification.yaml\n• decision: APPLY | CONDITIONAL | DO NOT APPLY\n• proposal_generation: allowed | allowed_with_conditions | blocked\n• claim_traceability: [...]"]
    end

    subgraph GateDecision["4. QUALIFICATION CONTROL GATE"]
        Gate{"Decision & Control State"}
    end

    subgraph GateOutcomes["Gate Outcomes"]
        DoNotApply["DO NOT APPLY\n(proposal_generation: blocked)"]
        Conditional["CONDITIONAL\n(proposal_generation: allowed_with_conditions)"]
        Apply["APPLY\n(proposal_generation: allowed)"]
    end

    subgraph ProjectionLayer["5. PROJECTION LAYER (out/<target-slug>/)"]
        GateReport["Gate Report\n(upwork-proposal.md)\n• Blocking Requirement\n• Evidence Gap\n• What Would Change Decision"]
        
        ProjRegistry["projection-registry\n(skills/projection-registry/)"]
        ProposalSkill["upwork-proposal\n(skills/upwork-proposal/)"]
        
        CleanProposal["upwork-proposal.md\n(Clean submission-ready prose,\n350-500 words)"]
        ScreeningAnswers["upwork-screening-answers.md\n(Direct answers + evidence;\n[OPEN CONDITION] tags if conditional)"]
        WorkSamples["upwork-work-samples.md\n(Max 3 evidence-backed samples)"]
    end

    subgraph EvaluationLayer["6. EVALUATION LAYER"]
        Validator["projection-validator\n(skills/projection-validator/)"]
        ValReport["projection-validation-report.yaml\n• Claim Traceability Check\n• Zero Fabrication Audit\n• Word Count Compliance"]
    end

    subgraph HumanBoundary["7. HUMAN APPROVAL BOUNDARY"]
        HumanReview["Human Candidate Review\n• Verify Open Conditions\n• Final Copywriting & Strategy Check"]
        HumanSubmit["Human Upwork Submission\n(External Action)"]
    end

    %% Data Flow Connections
    JobDesc --> OppAnalyzer
    TargetConfig --> OppAnalyzer
    OppAnalyzer --> OppAnalysisYaml
    
    OppAnalysisYaml --> QualSkill
    OKF --> QualSkill
    QualSkill --> QualYaml
    QualYaml --> Gate
    
    Gate -->|Blocked| DoNotApply
    Gate -->|Unverified Facts| Conditional
    Gate -->|Fully Supported| Apply
    
    DoNotApply --> GateReport
    Conditional --> ProjRegistry
    Apply --> ProjRegistry
    
    ProjRegistry --> ProposalSkill
    OKF --> ProposalSkill
    QualYaml --> ProposalSkill
    
    ProposalSkill --> CleanProposal
    ProposalSkill --> ScreeningAnswers
    ProposalSkill --> WorkSamples
    
    CleanProposal --> Validator
    ScreeningAnswers --> Validator
    QualYaml --> Validator
    Validator --> ValReport
    
    CleanProposal --> HumanReview
    ScreeningAnswers --> HumanReview
    WorkSamples --> HumanReview
    GateReport --> HumanReview
    
    HumanReview --> HumanSubmit

    %% Styling
    classDef inputStyle fill:#e1f5fe,stroke:#0288d1,stroke-width:1px;
    classDef okfStyle fill:#fff3e0,stroke:#f57c00,stroke-width:1px;
    classDef runtimeStyle fill:#e8f5e9,stroke:#388e3c,stroke-width:1px;
    classDef gateStyle fill:#fffde7,stroke:#fbc02d,stroke-width:2px;
    classDef blockStyle fill:#ffebee,stroke:#d32f2f,stroke-width:2px;
    classDef applyStyle fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef projStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:1px;
    classDef evalStyle fill:#ede7f6,stroke:#512da8,stroke-width:1px;
    classDef humanStyle fill:#e0f2f1,stroke:#00796b,stroke-width:2px;

    class JobDesc,TargetConfig inputStyle;
    class OKF okfStyle;
    class OppAnalyzer,OppAnalysisYaml,QualSkill,QualYaml runtimeStyle;
    class Gate gateStyle;
    class DoNotApply blockStyle;
    class Apply,Conditional applyStyle;
    class ProjRegistry,ProposalSkill,CleanProposal,ScreeningAnswers,WorkSamples,GateReport projStyle;
    class Validator,ValReport evalStyle;
    class HumanReview,HumanSubmit humanStyle;
```

## Key Architectural Invariants

1. **Qualification Control Gate**: Proposal generation CANNOT override qualification. If qualification evaluates to `DO NOT APPLY`, proposal generation is blocked and renders a Gate Report instead of a submission-ready application.
2. **Clean Client Prose**: `upwork-proposal.md` is rendered as clean professional prose ready for marketplace copy-pasting, while full claim-to-evidence provenance is preserved in `out/<target-slug>/runtime/upwork-qualification.yaml`.
3. **Automated Provenance Audit**: `projection-validator` verifies claim traceability internally by matching generated claims against the `claim_traceability` array in runtime context.
4. **Human Review Boundary**: The system ends at human-reviewable artifacts. No automated Upwork browser interaction or proposal submission is performed.

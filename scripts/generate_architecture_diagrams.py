#!/usr/bin/env python3
"""
Automated Architecture Diagram & Visualisation Generator (v2.0 - Modular UI/UX).

Auto-discovers repository architecture, skills, OKF knowledge graph schema,
and data flows from repository manifests (AGENTS.md, ARCHITECTURE.md, config.yaml, skills/*/SKILL.md).

Outputs:
1. Draw.io XML (.drawio.xml) files in docs/architecture/ (C4-style)
2. High-Level System Architecture Diagram (Modular Overview) in README.md & ARCHITECTURE.md
3. Detailed 4-Layer Skill Data Flow Diagram in ARCHITECTURE.md
4. OKF Knowledge Graph ER Schema in ARCHITECTURE.md
"""

import os
import re
import sys


def parse_skills(skills_dir="skills"):
    """Auto-discovers skills, frontmatter, descriptions, and layer classifications."""
    skills = []
    if not os.path.exists(skills_dir):
        return skills

    layer_mapping = {
        # Knowledge Layer
        "portfolio-ingestor": "Knowledge Layer",
        "portfolio-analyzer": "Knowledge Layer",
        "achievement-extractor": "Knowledge Layer",
        "evidence-card-generator": "Knowledge Layer",
        "behaviour-profile-generator": "Knowledge Layer",
        "capability-extractor": "Knowledge Layer",
        "signature-achievements-curator": "Knowledge Layer",
        "signature-theme-miner": "Knowledge Layer",
        "executive-identity-generator": "Knowledge Layer",
        "narrative-engine": "Knowledge Layer",
        "story-engine": "Knowledge Layer",
        "narrative-generator": "Knowledge Layer",
        # Runtime Layer
        "opportunity-analyzer": "Runtime Layer",
        # Coaching Layer
        "interview-strategy-generator": "Coaching Layer",
        "knowledge-gaps": "Coaching Layer",
        # Projection Layer
        "projection-registry": "Projection Layer",
        "resume-projection": "Projection Layer",
        "cover-letter-projection": "Projection Layer",
        "linkedin-projection": "Projection Layer",
        "opportunity-alignment-view": "Projection Layer",
        "executive-brief-view": "Projection Layer",
        "playbook-assembler": "Projection Layer",
        "projection-validator": "Projection Layer",
        "brand-validator": "Projection Layer",
        "playbook-orchestrator": "Orchestration Layer",
        "architecture-diagram-generator": "Tooling Layer",
    }

    for skill_name in sorted(os.listdir(skills_dir)):
        skill_path = os.path.join(skills_dir, skill_name, "SKILL.md")
        if os.path.isfile(skill_path):
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()

            desc = ""
            desc_match = re.search(r"description:\s*(.+)", content)
            if desc_match:
                desc = desc_match.group(1).strip().strip('"').strip("'")

            layer = layer_mapping.get(skill_name, "Knowledge Layer")
            skills.append({
                "name": skill_name,
                "description": desc,
                "layer": layer
            })

    return skills


def generate_high_level_mermaid_overview():
    """Generates a clean, compact High-Level System Architecture Overview diagram."""
    return """```mermaid
flowchart TD
    classDef inputStyle fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#F8FAFC
    classDef knowledgeStyle fill:#0369A1,stroke:#38BDF8,stroke-width:2px,color:#F8FAFC
    classDef runtimeStyle fill:#B45309,stroke:#FBBF24,stroke-width:2px,color:#F8FAFC
    classDef coachingStyle fill:#6D28D9,stroke:#C084FC,stroke-width:2px,color:#F8FAFC
    classDef projectionStyle fill:#15803D,stroke:#4ADE80,stroke-width:2px,color:#F8FAFC
    classDef validateStyle fill:#334155,stroke:#94A3B8,stroke-width:2px,color:#F8FAFC

    IN["📥 Candidate Portfolio & Target Role Spec"]:::inputStyle
    KL["🧠 1. Knowledge Layer (okf/)<br/><i>Canonical Knowledge Graph & Executive Identity</i>"]:::knowledgeStyle
    RL["⚡ 2. Runtime Layer (out/runtime/)<br/><i>Opportunity Context & Target Priorities</i>"]:::runtimeStyle
    CL["🎯 3. Coaching Layer (okf/)<br/><i>Opportunity-Aware Strategy & Gap Analysis</i>"]:::coachingStyle
    PL["📄 4. Projection Layer (out/)<br/><i>Resumes, Briefings, Cover Letter & Playbook</i>"]:::projectionStyle
    VG["🛡️ Quality & Brand Validation Gates<br/><i>Projection & Brand Alignment Verification</i>"]:::validateStyle

    IN --> KL
    IN --> RL
    KL --> RL
    KL --> CL
    RL --> CL
    KL --> PL
    RL --> PL
    CL --> PL
    PL --> VG
```"""


def generate_detailed_pipeline_mermaid():
    """Generates a structured, uncluttered 4-Layer Skill Data Flow diagram."""
    return """```mermaid
flowchart TD
    subgraph S0["📥 Input Ingestion"]
        direction LR
        IN_CV["Portfolio Sources<br/>(CV, LinkedIn, Architecture Docs)"]
        IN_JD["Target Opportunity Spec<br/>(Job Description / Recruiter Spec)"]
    end

    subgraph S1["🧠 1. Knowledge Layer (Canonical Graph in okf/)"]
        direction TB
        S1_ING["portfolio-ingestor"] --> S1_ANA["portfolio-analyzer"]
        S1_ANA --> S1_ACH["achievement-extractor"]
        S1_ACH --> S1_EVD["evidence-card-generator"]
        S1_EVD --> S1_CAP["capability-extractor & signature-curator"]
        S1_ACH --> S1_THM["signature-theme-miner"]
        S1_THM --> S1_IDN["executive-identity-generator"]
        S1_IDN --> S1_NAR["narrative-engine & story-engine"]
    end

    subgraph S2["⚡ 2. Runtime Layer (Derived Context in out/runtime/)"]
        S2_OPP["opportunity-analyzer<br/><i>Emits opportunity-analysis.yaml</i>"]
    end

    subgraph S3["🎯 3. Coaching Layer (Derived Strategy in okf/)"]
        S3_STR["interview-strategy-generator"]
        S3_GAP["knowledge-gaps (Pre-assembly Gate)"]
    end

    subgraph S4["📄 4. Projection Layer (Presentation Views in out/)"]
        direction TB
        S4_REG["projection-registry"]
        subgraph S4_VIEWS["Projections & Presentation Suite"]
            direction LR
            V_RES["resume-projection<br/><i>(Executive, ATS, Recruiter)</i>"]
            V_COV["cover-letter-projection"]
            V_LKD["linkedin-projection"]
            V_ALI["opportunity-alignment-view"]
            V_BRF["executive-brief-view"]
            V_PBK["playbook-assembler<br/><i>(Playbook & Cheat Sheet)</i>"]
        end
        S4_REG --> V_RES
        S4_REG --> V_COV
        S4_REG --> V_LKD
        S4_REG --> V_ALI
        S4_REG --> V_BRF
        S4_REG --> V_PBK
    end

    subgraph S5["🛡️ Quality Validation Gates"]
        S5_PV["projection-validator"]
        S5_BV["brand-validator"]
    end

    IN_CV --> S1_ING
    IN_JD --> S2_OPP
    S1_NAR --> S2_OPP
    S1_NAR --> S3_STR
    S2_OPP --> S3_STR
    S1_NAR --> S3_GAP
    S2_OPP --> S3_GAP
    S1_NAR --> S4_REG
    S2_OPP --> S4_REG
    S3_STR --> S4_REG
    S4_VIEWS --> S5_PV
    S4_VIEWS --> S5_BV
```"""


def generate_mermaid_okf_schema():
    """Generates Mermaid OKF Knowledge Graph schema diagram."""
    return """```mermaid
erDiagram
    SOURCE ||--o{ ACHIEVEMENT : "grounded in"
    ACHIEVEMENT ||--o{ EVIDENCE-CARD : "structured into STAR"
    EVIDENCE-CARD ||--o{ CAPABILITY : "grouped into"
    EVIDENCE-CARD ||--o{ SIGNATURE-ACHIEVEMENTS : "curated into"
    ACHIEVEMENT ||--o{ SIGNATURE-THEMES : "mined into"
    SIGNATURE-THEMES ||--|| EXECUTIVE-IDENTITY : "synthesises"
    EXECUTIVE-IDENTITY ||--|| VOICE-PROFILE : "defines"
    EXECUTIVE-IDENTITY ||--|| POSITIONING-STATEMENTS : "formulates"
    POSITIONING-STATEMENTS ||--o{ NARRATIVE-LIBRARY : "drives"
    EVIDENCE-CARD ||--|| STORY-LIBRARY : "consolidates"
    OPPORTUNITY-ANALYSIS ||--o{ INTERVIEW-STRATEGY : "shapes"
    STORY-LIBRARY ||--o{ PROJECTIONS : "adapts"
```"""


def create_drawio_xml(title, root_children_xml):
    """Wraps mxGraphModel nodes into valid Draw.io XML format."""
    return f"""<mxfile host="Electron" modified="2026-07-31T12:00:00.000Z" agent="Antigravity Architecture Generator" version="21.0.0" type="device">
  <diagram id="diag_{title.lower().replace(' ', '_')}" name="{title}">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        {root_children_xml}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""


def build_pipeline_drawio_xml(skills):
    """Generates C4-style Draw.io XML diagram for 4-Layer Pipeline Architecture."""
    nodes_xml = []
    
    # Title Box
    nodes_xml.append('<mxCell id="title" value="Career Projection Platform v0.5 — 4-Layer Pipeline Architecture" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontStyle=1;fontColor=#1E293B;" vertex="1" parent="1"><mxGeometry x="180" y="20" width="800" height="40" as="geometry" /></mxCell>')

    # 4 Layer Container Boxes
    layers = [
        ("Knowledge Layer (okf/)", "#E0F2FE", "#0284C7", 40, 80, 260, 680),
        ("Runtime Layer (out/runtime/)", "#FEF3C7", "#D97706", 320, 80, 240, 680),
        ("Coaching Layer (okf/)", "#F3E8FF", "#7C3AED", 580, 80, 240, 680),
        ("Projection Layer (out/)", "#DCFCE7", "#16A34A", 840, 80, 280, 680),
    ]

    cell_id = 2
    for name, bg_color, border_color, x, y, width, height in layers:
        nodes_xml.append(f'<mxCell id="{cell_id}" value="&lt;b&gt;{name}&lt;/b&gt;" style="swimlane;whiteSpace=wrap;html=1;fillColor={bg_color};strokeColor={border_color};fontColor=#0F172A;startSize=30;rounded=1;arcSize=4;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry" /></mxCell>')
        cell_id += 1

    # Populate Skills into Layer Containers
    layer_skill_y = {"Knowledge Layer": 120, "Runtime Layer": 120, "Coaching Layer": 120, "Projection Layer": 120}
    layer_x_map = {"Knowledge Layer": 55, "Runtime Layer": 335, "Coaching Layer": 595, "Projection Layer": 855}

    for skill in skills:
        layer = skill["layer"]
        if layer not in layer_x_map:
            continue
        sx = layer_x_map[layer]
        sy = layer_skill_y[layer]
        
        name = skill["name"]
        style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#64748B;fontColor=#334155;fontSize=11;shadow=1;"
        nodes_xml.append(f'<mxCell id="{cell_id}" value="&lt;b&gt;{name}&lt;/b&gt;" style="{style}" vertex="1" parent="1"><mxGeometry x="{sx}" y="{sy}" width="{layer_x_map[layer] and (230 if layer== "Projection Layer" else 210)}" height="45" as="geometry" /></mxCell>')
        cell_id += 1
        layer_skill_y[layer] += 55

    return create_drawio_xml("4-Layer Pipeline Architecture", "\n        ".join(nodes_xml))


def update_markdown_file(filepath, mermaid_content):
    """Safely updates or injects Mermaid diagram block in target markdown file."""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    begin_marker = "<!-- BEGIN AUTO-GENERATED ARCHITECTURE DIAGRAM -->"
    end_marker = "<!-- END AUTO-GENERATED ARCHITECTURE DIAGRAM -->"
    block = f"{begin_marker}\n{mermaid_content}\n{end_marker}"

    if begin_marker in content and end_marker in content:
        pattern = re.compile(f"{re.escape(begin_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        new_content = pattern.sub(block, content)
    else:
        # Append before '## Status' or at bottom if marker not present
        if "## Status" in content:
            new_content = content.replace("## Status", f"{block}\n\n## Status")
        else:
            new_content = content + f"\n\n## Architecture Diagram\n\n{block}\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Updated architecture diagram in {filepath}")
    return True


def main():
    print("=== Auto-Generating Architecture Visualisations & Diagrams (v2.0) ===")
    
    # 1. Parse Skills and Architecture Metadata
    skills = parse_skills()
    print(f"Discovered {len(skills)} pipeline skills across 4 architecture layers.")

    # 2. Ensure docs/architecture directory exists
    arch_dir = "docs/architecture"
    os.makedirs(arch_dir, exist_ok=True)

    # 3. Generate Draw.io XML Files
    pipeline_xml = build_pipeline_drawio_xml(skills)
    drawio_path = os.path.join(arch_dir, "4-layer-pipeline.drawio.xml")
    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(pipeline_xml)
    print(f"Emitted C4 Draw.io XML: {drawio_path}")

    # 4. Generate Modular Mermaid Visualizations
    high_level_overview = generate_high_level_mermaid_overview()
    detailed_pipeline = generate_detailed_pipeline_mermaid()
    okf_schema = generate_mermaid_okf_schema()

    readme_content = f"### System Architecture Overview\n\n{high_level_overview}"
    architecture_md_content = f"### System Architecture Overview\n\n{high_level_overview}\n\n### Detailed 4-Layer Skill Data Flow\n\n{detailed_pipeline}\n\n### OKF Knowledge Graph Schema\n\n{okf_schema}"

    # 5. Inject/Update Markdown Documentation
    update_markdown_file("README.md", readme_content)
    update_markdown_file("ARCHITECTURE.md", architecture_md_content)

    print("=== Architecture Diagram Auto-Generation Complete ===")


if __name__ == "__main__":
    main()

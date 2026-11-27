---
name: architecture-diagram-generator
description: Auto-discovers system architecture, skills, and data flows, emitting Draw.io XML diagrams and updating Mermaid diagrams in ARCHITECTURE.md and README.md.
---

# Architecture Diagram Generator

## Overview

`architecture-diagram-generator` is an automated tooling skill. It parses repository manifests (`AGENTS.md`, `ARCHITECTURE.md`, `config/config.yaml`, and `skills/*/SKILL.md`) to dynamically extract the 4-layer architecture, skill components, and OKF knowledge graph relationships.

## Outputs

- **Draw.io XML**: `docs/architecture/4-layer-pipeline.drawio.xml` (C4-style diagram)
- **Mermaid Diagrams**: Injected into `ARCHITECTURE.md` and `README.md` between `<!-- BEGIN AUTO-GENERATED ARCHITECTURE DIAGRAM -->` and `<!-- END AUTO-GENERATED ARCHITECTURE DIAGRAM -->` markers.

## Execution Instructions

1. Run the auto-discovery Python generator script:
   ```bash
   python3 scripts/generate_architecture_diagrams.py
   ```
2. Verify that output files in `docs/architecture/` and documentation files (`ARCHITECTURE.md`, `README.md`) are cleanly updated.

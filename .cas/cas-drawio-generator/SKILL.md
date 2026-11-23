---
name: cas-drawio-generator
description: Generates C4-style draw.io compatible XML diagrams (.drawio.xml) for system architecture, containers, components, and runtime flows. Use when the user needs to visualize architectural structures or flows based on codebase analysis or requirements.
---

# cas-drawio-generator

This skill enables the generation of valid, professional-grade architecture diagrams compatible with [draw.io](https://app.diagrams.net).

## Workflow

1.  **Analyze Context**: Identify the system boundaries, actors, containers, or components to be visualized.
2.  **Select Template**: Choose the appropriate C4 level or custom flow.
    - Level 1: System Context
    - Level 2: Container Architecture
    - Level 3: Component Architecture
    - Level 4: Runtime Flow
3.  **Plan Layout**: Map elements to a 10px grid. Use standard box sizes:
    - Small: 150x70 | Medium: 220x90 | Large: 260x140
    - Margins: x=40, y=20
4.  **Generate XML**: Construct the `<mxfile>` using the specifications in [drawio-specs.md](references/drawio-specs.md).
5.  **Save & Verify**: Save as `.drawio.xml` and run through the verification checklist in the reference file.

## Bundled Resources

- **Specifications**: [drawio-specs.md](references/drawio-specs.md) contains XML structures, style strings, and the C4 color palette.
- **Templates**: Reference the following assets for structural baseline:
    - `assets/system-context-template.drawio.xml`
    - `assets/container-architecture-template.drawio.xml`
    - `assets/component-architecture-template.drawio.xml`
    - `assets/runtime-flow-template.drawio.xml`

## Coordinate Planning Tips

- Start the title at `(40, 20)`.
- Use `dx="1280" dy="760"` for standard page models.
- Spacing between elements should be `40-80px`.
- For flows, use a row height of `100-120px`.

## Common Mistakes to Avoid

- DO NOT output pure SVG; it must be the `<mxfile>` XML format.
- DO NOT skip the root cells `id="0"` and `id="1"`.
- DO NOT forget `vertex="1"` or `edge="1"` on cell elements.

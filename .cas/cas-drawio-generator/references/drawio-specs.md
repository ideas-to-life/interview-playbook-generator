# draw.io XML Specifications

## Core XML Structure
All diagrams MUST follow this exact structure to be compatible with draw.io (app.diagrams.net).

```xml
<mxfile host="app.diagrams.net" agent="Claude Code" version="24.7.17">
  <diagram id="unique-id" name="Diagram Name">
    <mxGraphModel dx="WIDTH" dy="HEIGHT" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="WIDTH" pageHeight="HEIGHT" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Diagram elements go here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Element Definitions

### Vertex (Shapes)
```xml
<mxCell id="N" value="Label Text" style="STYLE_STRING" vertex="1" parent="1">
  <mxGeometry x="X" y="Y" width="W" height="H" as="geometry"/>
</mxCell>
```

### Edge (Connectors)
```xml
<mxCell id="N" value="" style="endArrow=block;html=1;rounded=0;" edge="1" parent="1" source="SOURCE_ID" target="TARGET_ID">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## Style Library

| Shape | Style String |
|-------|--------------|
| Rounded Box | `rounded=1;whiteSpace=wrap;html=1;fillColor=#COLOR;strokeColor=#COLOR;` |
| Text Label | `text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=SIZE;fontStyle=1` |
| Cylinder (DB) | `shape=cylinder;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#COLOR;strokeColor=#COLOR;` |
| Note | `shape=note;whiteSpace=wrap;html=1;fillColor=#COLOR;strokeColor=#COLOR;` |

## C4 Color Palette

| Purpose | Fill | Stroke |
|---------|------|--------|
| Person/External | `#dae8fc` | `#6c8ebf` |
| System/Container | `#fff2cc` | `#d6b656` |
| Component | `#ffe6cc` | `#d79b00` |
| Database | `#e1d5e7` | `#9673a6` |
| Service/API | `#f8cecc` | `#b85450` |
| Boundary Box | `#eef5ff` | `#6c8ebf` |
| Process/Flow | `#d5e8d4` | `#82b366` |
| Note | `#fff2cc` | `#d6b656` |

## Verification Checklist
- [ ] Root element is `<mxfile>` with correct attributes.
- [ ] Contains root cells `id="0"` and `id="1"`.
- [ ] All vertices have `vertex="1"` and a valid `mxGeometry`.
- [ ] All edges have `edge="1"`, `source`, and `target`.
- [ ] Coordinates are aligned to a 10px grid.

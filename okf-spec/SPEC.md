# Open Knowledge Format (OKF) v0.2 Specification (Vendored Summary)

## 1. Overview
OKF is a plain-markdown, file-system based knowledge graph standard designed for AI agents and human pair-programming. Every node in the graph is a Markdown file containing YAML frontmatter and a Markdown body.

## 2. Minimal Required Frontmatter
Every OKF concept file MUST contain valid YAML frontmatter with at least:
```yaml
---
type: <string>
---
```
Consumers MUST tolerate unknown `type` values and additional frontmatter keys.

## 3. Recommended Metadata Keys
- `title`: Human-readable title
- `description`: Single sentence overview
- `tags`: List of string tags
- `generated`: `{ by: <actor>, at: <ISO-8601> }`
- `verified`: List of `{ by: <actor>, at: <ISO-8601> }` (absent means unverified)
- `status`: `draft` | `stable` | `deprecated`
- `stale_after`: `YYYY-MM-DD`
- `sources`: List of source references `[{ id, resource, title, author, last_modified }]`

## 4. Statement Classification & Footnotes
OKF concepts classify body claims:
- `[evidence]` — Directly stated in a source. Accompanied by a `[^source-id]` footnote.
- `[inference]` — Derived from evidence.
- `[recommendation]` — Tactical recommendation grounded in evidence/inference.
- `[assumption]` — Explicit placeholder for unconfirmed or unstated values.

## 5. Reserved Filenames
- `index.md` — Root or directory index listing concepts. Bundle root `index.md` specifies `okf_version: "0.2"`.
- `log.md` — Append-only change history log (newest entry first).

---
name: cas-refactor-knowledge-links
description: Refactor CAS knowledge artefacts into an explicit navigable relationship graph without changing their semantic content. Use when asked to connect, link, trace, graph, or improve relationships between Architecture Work, Architecture Evolution Maps, Architecture Intent Documents, alignment reports, ADRs, patterns, or other CAS knowledge files, especially under knowledge/projects or knowledge/global. Always invoke before adding frontmatter relationship metadata or Obsidian-style markdown links to CAS knowledge artefacts.
---

# Skill: cas-refactor-knowledge-links

## Intent
Add explicit, verifiable links between existing CAS knowledge artefacts so architecture work, maps, intent, alignment, decisions, and patterns can be navigated as a connected knowledge graph.

## Inputs
- Read `INPUT.schema.yaml` first.
- Use `input.target_root` as the primary filesystem scope. Default to `knowledge/` only when the user gives no narrower scope.
- Use `input.relationship_request` to determine which artefacts and relationship types to add.
- Treat `input.constraints` as hard constraints unless they conflict with preserving existing artefact content.

## Decision Precedence
Apply rules in this order:
1. Preserve existing artefact meaning and body content.
2. Keep the search/edit scope to the user's target path.
3. Reuse existing artefact identifiers, filenames, and frontmatter fields.
4. Add only relationships that can be justified from current files.
5. Prefer the smallest additive change that makes traceability explicit.

If relationships cannot be inferred from current artefacts with confidence, mark the decision as `proposed` or `rejected` rather than inventing links.

## Relationship Model
Use this frontmatter block when missing:

```yaml
relationships:
  derives_from: []
  influences: []
  evaluates: []
  related_to: []
```

Use relationship keys consistently:
- `derives_from`: an artefact depends on or was generated from another artefact.
- `influences`: an artefact shapes or drives a later artefact.
- `evaluates`: an artefact reviews, checks, or scores another artefact.
- `related_to`: a non-directional relationship that is real but does not fit the other keys.

## Mapping Guidance
- Architecture Evolution Map (AEM): usually `derives_from` Architecture Work and `influences` Architecture Intent Documents or downstream decisions.
- Architecture Intent Document (AID): usually `derives_from` the relevant AEM and Architecture Work.
- Alignment report: usually `evaluates` the relevant AID, AEM, decision, diagram, or pattern.
- Architecture Work (AW): usually remains a source artefact; add `related_to` only when the file itself establishes the relationship.
- ADR: usually `derives_from` accepted Architecture Work, AEM, or alignment evidence and `influences` patterns.
- Pattern: usually `derives_from` accepted ADRs and may be `related_to` supporting maps or rules.

Prefer exact frontmatter references such as `id`, `pattern_id`, `related`, `decision.pattern_id`, or explicit body links. Use dates, version numbers, and project paths only as tie-breakers.

## Refactoring Steps

### 1. Discover Artefacts
- Inspect only the target scope and directly referenced files.
- Identify artefact type from frontmatter, path, filename prefix, and headings.
- Record each artefact identifier. Prefer frontmatter `id`; otherwise use the filename stem.

### 2. Infer Relationships
- Build candidate relationships from explicit references first.
- Use chronology and workflow conventions only when they are unambiguous.
- Do not link to files that do not exist.
- Do not duplicate an existing relationship.

### 3. Update Frontmatter
- Add the `relationships` block if missing.
- Preserve all existing fields and field ordering as much as practical.
- Merge missing values into existing relationship arrays.
- Do not overwrite valid existing relationship values.

### 4. Update Markdown Body
- Append or update a `## Relationships` section near the end of the file.
- Use Obsidian-style links in the form `[[target-id]]`.
- Keep labels human-readable:
  - `Derived from`
  - `Influences`
  - `Evaluates`
  - `Related to`
- Make markdown links match frontmatter relationship values.

### 5. Validate
- Confirm every new relationship target resolves to an artefact in scope or a directly referenced file.
- Confirm no duplicate values exist in relationship arrays.
- Confirm body links and frontmatter references are consistent.
- Run the smallest relevant validation command available for the repo or explain why no automated validation exists.

## Output Contract
Produce exactly one YAML output block conforming to `OUTPUT.schema.yaml`. Include no meta-commentary outside the YAML block when this skill is used as a decision contract.

## Anti-Patterns
- Inventing links because two artefacts have similar names.
- Rewriting body content unrelated to relationship links.
- Expanding scope beyond the user's target root.
- Adding graph metadata to generated output without checking current files.
- Replacing existing frontmatter wholesale when a minimal merge is enough.

## Examples
See `EXAMPLES.md` for accepted, proposed, and rejected examples.

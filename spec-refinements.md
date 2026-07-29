Mandatory refinements for v0.1

The current specification is approved as the baseline architecture.

Before implementation, make the following small refinements. Do not expand scope beyond these items.

1. Add portfolio-ingestor as Skill 0

Insert a new first Skill before portfolio-analyzer.

Responsibilities:

* Discover all portfolio artefacts.
* Classify artefacts (CV, LinkedIn, portfolio, presentations, architecture docs, publications, recruiter notes, etc.).
* Build a source index.
* Normalise metadata and provenance.

Output:

okf/sources/index.md

This keeps portfolio-analyzer focused on analysis rather than discovery.

⸻

2. Split role analysis from role overlay

Replace

role-overlay-builder

with two Skills:

role-analyzer
fit-mapper

Responsibilities:

role-analyzer

* Extract responsibilities.
* Required competencies.
* Leadership expectations.
* Technical expectations.
* Success measures.
* Unknowns.

Output:

okf/roles/current-role.md

fit-mapper

Maps role requirements to evidence cards.

Produces:

* strengths
* gaps
* differentiators
* recommended stories

Output:

okf/fit/current-role.md

The existing overlay becomes a presentation layer built from these outputs.

⸻

3. Add Interview Strategy output

Introduce a new Skill:

interview-strategy-generator

Produces a concise briefing:

* top differentiators
* recommended narrative
* strongest evidence cards
* likely objections
* mitigation
* interview priorities

Output:

okf/interview-strategy.md

This should be consumed by the final playbook assembler.

⸻

4. Add Knowledge Gap reporting

Before playbook generation, analyse whether sufficient evidence exists.

Output:

okf/knowledge-gaps.md

Missing information should never be fabricated.

Instead:

* identify missing evidence,
* mark affected outputs as draft,
* recommend portfolio improvements.

⸻

5. Preserve the thin slice

Do not expand the initial implementation.

The first runnable version remains:

1. portfolio-ingestor
2. portfolio-analyzer
3. achievement-extractor
4. evidence-card-generator
5. interview-strategy-generator
6. playbook-assembler

Everything else remains iterative.

⸻

Explicitly defer

The following ideas are valuable but not required for v0.1:

* Competency ontology/catalogue
* View generator
* Career narrative evolution
* Mock interviews
* Conversation simulator
* LLM-as-judge evaluation
* Company research
* Salary research
* Market intelligence
* Advanced OKF linting

These belong in future iterations after the end-to-end pipeline is proven.

⸻

Guiding principle

Optimise for a working end-to-end interview pipeline, not for a complete career intelligence platform.

Every new Skill introduced in v0.1 must directly improve the quality of the generated interview playbook for real interview preparation. Everything else should be deferred until the experiment has demonstrated value.

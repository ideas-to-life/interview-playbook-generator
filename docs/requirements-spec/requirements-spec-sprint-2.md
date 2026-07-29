Sprint 2 Requirement Specification

Interview Intelligence Refinement (v0.2)

Objective

The current pipeline successfully generates an evidence-grounded Interview Playbook.

However, the generated playbook is still largely a structured summary of the portfolio rather than an effective coaching tool.

The goal of Sprint 2 is not to improve extraction accuracy.

The goal is to transform extracted knowledge into interview guidance that can be used immediately during recruiter and hiring manager conversations.

The implementation should optimise for practical interview preparation rather than documentation completeness.

⸻

Success Criteria

After this sprint, a candidate should be able to read the generated playbook for ten minutes before an interview and feel prepared to answer:

* Tell me about yourself.
* Why this role?
* Why should we hire you?
* Tell me about your AI experience.
* What differentiates you?
* Why are you leaving?
* What questions should you ask us?

without needing to read the entire OKF bundle.

⸻

Refinement 1

Generate Signature Themes

Problem

The current playbook is organised around projects.

Interviewers remember professional themes rather than project chronology.

New Output

okf/signature-themes.md

Responsibilities

Analyse all extracted achievements.

Identify recurring professional patterns.

Each theme should:

* synthesise multiple achievements
* reference supporting evidence
* produce one executive-level message

Example

Theme
Operationalising Enterprise AI
Supporting evidence
BBC AI Capability Model
BBC AI Framework
WPP AI Platform
CAS
EA4ALL
Executive message
Transforms AI experimentation into governed organisational capability.

⸻

Refinement 2

Rewrite Interview Strategy

Problem

Current strategy summarises.

It does not coach.

Required Behaviour

The Interview Strategy should answer:

What should Alexandre lead with?
What should Alexandre avoid?
Which three stories should be remembered?
Which achievements differentiate him?
Which concerns might arise?
How should they be addressed?

Output

okf/interview-strategy.md

becomes a concise coaching document.

Maximum:

4 pages.

⸻

Refinement 3

Prioritise Evidence

Problem

The playbook currently presents every Evidence Card equally.

Real interviews rarely require more than a few flagship stories.

Required Behaviour

Rank every Evidence Card.

Classification:

Primary Story
Supporting Story
Optional Story
Do Not Use

Ranking should consider:

* target role
* interview stage
* relevance
* uniqueness
* evidence strength

The Playbook should render only:

* Primary
* Supporting

Optional stories remain available in OKF.

⸻

Refinement 4

Introduce Executive Narrative

Problem

Current narrative reads like an expanded CV.

Recruiters need a memorable story.

New Output

okf/executive-narrative.md

Generate:

* 30-second introduction
* 2-minute career journey
* 5-minute executive story

These should be conversational.

Avoid CV language.

Avoid listing job titles.

Focus on:

* evolution
* motivation
* differentiators

⸻

Refinement 5

Generate Interview Cheat Sheet

Problem

The playbook is too long to review immediately before an interview.

New Output

out/interview-cheatsheet.md

Maximum:

Two pages.

Contents:

Elevator Pitch

Top Five Messages

Three Stories to Remember

Likely Recruiter Questions

Suggested Answers

Questions to Ask

Red Flags

Things Not To Forget

This document becomes the primary interview preparation artefact.

⸻

Refinement 6

Improve Playbook Assembly

The current playbook is document-oriented.

Replace with coaching-oriented structure.

New order:

Executive Summary
30-second Pitch
2-minute Story
Why This Role
Top Differentiators
Top Three Stories
STAR Library
Likely Questions
Questions to Ask
Knowledge Gaps
Appendix

The STAR library should move into the appendix.

The interview narrative becomes the main content.

⸻

Refinement 7

Reduce CV Language

The Playbook Assembler should avoid reproducing CV wording.

Example:

Avoid

Senior Director – Systems Architect Agentic AI

Prefer

Enterprise Architect specialising in helping organisations operationalise AI through architecture, governance and transformation.

The goal is to produce language suitable for conversation rather than recruitment administration.

⸻

Acceptance Criteria

Sprint 2 is complete when the generated outputs include:

okf/signature-themes.md
okf/executive-narrative.md
okf/interview-strategy.md (coaching version)
out/playbook.md (coaching version)
out/interview-cheatsheet.md

and the Interview Cheat Sheet can realistically be reviewed in under ten minutes immediately before an interview.

⸻

Guiding Principle

Every generated artefact should help the candidate perform better in the interview, not simply document what the portfolio contains.

The pipeline has already demonstrated that it can extract, organise and govern knowledge. Sprint 2 should focus on transforming that knowledge into a concise, memorable narrative that enables confident, evidence-backed conversations with recruiters and hiring managers.

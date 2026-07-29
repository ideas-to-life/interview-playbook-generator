Requirement Specification

Master Interview Playbook Generator

Objective

Generate a high-quality interview preparation package from an individual’s portfolio and career knowledge.

The generated package must:

* remain grounded in evidence
* never invent achievements
* adapt to different role types
* reuse knowledge consistently
* preserve the candidate’s authentic voice
* optimise for executive conversations

⸻

Inputs

Mandatory

Candidate Knowledge Base

Examples

* Portfolio
* Career Timeline
* CV
* LinkedIn
* Project documentation
* Architecture artefacts
* Publications
* Presentations

⸻

Target Opportunity

Either

Job Description

or

Recruiter Message

or

Role Summary

⸻

Optional

Company information

Interviewer information

Industry

Salary expectations

Interview stage

Recruiter notes

⸻

Outputs

Generate a structured Interview Playbook.

⸻

Section 1

Executive Summary

One-page summary

Includes

* Role
* Candidate fit
* Top differentiators
* Risks
* Preparation priority

⸻

Section 2

Role Analysis

Extract

Mission

Business outcomes

Leadership expectations

Technical expectations

Soft skills

Success measures

Unknowns

Questions requiring clarification

⸻

Section 3

Fit Assessment

Produce

Overall fit score

Dimension-by-dimension alignment

Example

Enterprise Architecture

★★★★★

Leadership

★★★★☆

AI Transformation

★★★★★

Commercial

★★★★☆

Governance

★★★★★

Communication

★★★★★

⸻

Each score must reference evidence.

⸻

Section 4

Personal Narrative

Generate

30 second introduction

2 minute introduction

5 minute career journey

Executive version

Coffee-chat version

Recruiter version

⸻

Ground entirely on portfolio evidence.

⸻

Section 5

Signature Themes

Identify recurring themes across career.

Examples

Enterprise Transformation

Architecture Leadership

AI Operationalisation

Governance

Operating Models

Business Capability

Transformation

Architecture Communities

Innovation

Thought Leadership

⸻

These should be inferred rather than copied.

⸻

Section 6

Evidence Library

This becomes one of the most valuable outputs.

Create reusable evidence.

Example

Evidence Card

Title

Situation

Actions

Results

Lessons

Competencies demonstrated

Tags

Possible interview questions

Supporting artefacts

Confidence level

⸻

Think of these as reusable STAR objects.

⸻

Section 7

STAR Story Library

Generate

Short

Medium

Detailed

versions

of every STAR.

⸻

Section 8

Technical Preparation

Generate

Architecture questions

AI questions

Governance questions

Leadership questions

Trade-offs

System Design

Reference Architectures

Decision Frameworks

⸻

Again

Only from evidence.

Never fabricate.

⸻

Section 9

Executive Preparation

Generate

Executive concerns

Board-level questions

Operating Model

Transformation

Budget

Risk

People

Governance

Adoption

Culture

⸻

Section 10

Questions to Ask

Recruiter

Hiring Manager

CTO

Chief Architect

Engineering

HR

CEO

Board

⸻

Tailor by role.

⸻

Section 11

Salary Strategy

Prepare

Expected range

Negotiation approach

Market positioning

Fallback strategy

Non-financial considerations

⸻

Section 12

Role Overlay

This is the custom section.

Contains only

Role-specific preparation.

Everything else comes from reusable knowledge.

⸻

Quality Requirements

Every generated statement must be classified.

Evidence

Inference

Recommendation

Assumption

This prevents hallucination.

⸻

Every achievement must reference its evidence source.

Portfolio

CV

LinkedIn

Presentation

Architecture document

etc.

⸻

Never invent

Projects

Metrics

Team sizes

Budgets

Technologies

Responsibilities

⸻

Architecture

I wouldn’t build one giant prompt.

I’d build specialised Skills.

Example

Interview Playbook
├── Portfolio Analyzer
├── Career Timeline Builder
├── Achievement Extractor
├── Competency Mapper
├── STAR Generator
├── Leadership Story Generator
├── Architecture Story Generator
├── AI Story Generator
├── Executive Narrative Generator
├── Recruiter Narrative Generator
├── Technical Q&A Generator
├── Executive Q&A Generator
├── Question Generator
├── Salary Strategy Generator
├── Interview Pack Assembler

Each Skill has a single responsibility.

⸻

Future Extensions

Once the Master Interview Playbook exists, you can generate:

* Executive interview packs.
* Technical interview packs.
* Behavioural interview packs.
* Panel interview packs.
* Coffee-chat preparation.
* Recruiter preparation.
* Executive one-page briefing.
* “Tell me about yourself” variants.
* 30-60-90 day plans.
* Company-specific overlays.
* Mock interview questions.
* Gap analysis.
* Confidence assessment.
* Suggested portfolio artefacts to highlight.

⸻

One recommendation I’d add

Knowing how you’ve evolved CAS, I’d avoid making the Interview Playbook the primary artefact.

Instead, I’d make the Interview Knowledge Graph the primary artefact.

Think of it this way:

Portfolio
      │
      ▼
Knowledge Graph
      │
      ├── Achievements
      ├── Skills
      ├── Competencies
      ├── Leadership Stories
      ├── Architecture Stories
      ├── AI Stories
      ├── Evidence
      ├── Projects
      └── Lessons Learned
             │
             ▼
Interview Playbook Generator
             │
             ├── Recruiter Pack
             ├── CTO Pack
             ├── AI CoE Pack
             ├── Head of AI Pack
             ├── Executive Pack
             ├── Technical Pack
             └── Behavioural Pack

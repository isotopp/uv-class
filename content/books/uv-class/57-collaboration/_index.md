---
title: "Project hygiene and collaboration"
weight: 570
date: 2025-12-22T00:00:00Z
description: |
  Project hygiene and collaboration

---


This chapter focuses on maintainability.
It explains structure, documentation, automation boundaries, and collaboration norms.
The goal is to make projects legible to other humans and to machines.

## Topics

- Project structure
  - Source layout
  - Tests
- `.gitignore`
  - Minimal ignores
  - What not to ignore
- Documentation
    - How we learn
      - Recall and spaced retrieval drive durable learning
      - Explanations are still necessary to build mental models and reduce blind trial-and-error.
      - Reference is necessary to prevent folklore and drift.
    - What is [Diátaxis](https://diataxis.fr/)?
      - A framework for organizing docs by reader intent, preventing mixing fundamentally different doc modes.
    - Axes (Practical - Theoretical; Now - Future/Long Term),
    - Quadrants (Tutorials, How-To-Guides, References, Explanations)
      - Tutorials: guided learning, safe path, minimal branching
      - How-to guides: goal-driven procedures for known problems.
      - Reference: complete and exact, optimized for lookup.
      - Explanation: concepts, rationale, tradeoffs, context.
  - Bloom Categories: a taxonomy of cognitive operations, useful for designing tasks and assessments 
    - Remember - Understand (dt. "Reproduktion")
    - Apply (dt. "Anwendung")
    - Analyze - Evaluate - Create (dt. "Transfer")
  - Diátaxis chooses the document mode by reader intent, Bloom chooses the cognitive demand of the tasks you include
    - Tutorials: emphasize Remember - Understand - Apply with a tight scaffold.
    - How-to guides: emphasize Apply, sometimes Analyze when debugging or choosing options.
    - Reference: primarily Remember, sometimes Understand via definitions and constraints.
    - Explanation: emphasize Understand - Analyze - Evaluate, occasionally Create via design patterns.
    - "Use Diátaxis to decide what the page is; Use Bloom to decide what the reader is asked to do on that page"
- `README.md` as a user-interface, for large projects as a quick-start and pointer to the full docs. Sections:
  - What it is
  - Who it is for
  - Install
  - Quick start (minimal, runnable)
  - Common tasks (links to how-to guides)
  - Configuration (link to reference)
  - Concepts (link to explanation)
  - Support (link to github, troubleshooting, FAQ)
  - Versioning and compatibility  
  - What contributors need (link to `AGENTS.md`)
- `AGENTS.md` as an interface to contributors (human, and agents)
  - Automation policies (What may agents do unassisted, what must never be done automatically, data handling rules,
instrumentation and other guidelines)
  - Tooling boundaries (allowed toolchain, test policies, OS targets, formatting and linting sources of truth), dependency policy
  - Naming and consistency rules (Public API naming, file and module naming, doc style rules, error message logging conventions, backwards compat policy)
  - Other rules (Decision records location and format, Definition of done checklist, Standard PR template pointers, Test categories and how to run each.)

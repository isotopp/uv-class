---
title: "Dependencies, environments, and reproducibility"
weight: 50
date: 2025-12-22T00:00:00Z
description: |
  Dependencies, environments, and reproducibility

---

This chapter combines dependency management, environment syncing, and lockfiles into one coherent story.
Students learn how intent becomes reality, and why reproducibility is the core professional skill uv enforces.

## Topics

- Adding and removing dependencies
  - `uv add`
  - `uv remove`
- Runtime vs development dependencies
  - `uv add --dev`, `uv remove --dev`
- Dependency resolution
  - When?
  - What is considered?
  - Versions, Version ranges, what is chosen?
- Lockfiles
  - What `uv.lock` contains
  - Why it exists
- `uv sync` and `uv run`
  - What they read
  - Why lockfiles are authoritative
- Upgrading with `uv lock`
- Sharing projects and deterministic installs
- Why lockfiles belong in `git`

---
title: "Creating projects the uv way"
weight: 40
date: 2025-12-22T00:00:00Z
description: |
  Creating projects the uv way

---

This chapter introduces the **golden path**: projects as installable modules with entry points.
Students learn how uv init creates structure, why that structure matters, and how naming affects everything downstream.

This chapter sets expectations for maintainable, reusable projects.

## Topics

- `uv init`
  - Application vs package projects
- Project layout
  - `src` layout
  - Why flat layouts fail over time
- Naming conventions
  - Project names
  - Module names
  - Entry point names
- Script entry points
- Why entry points beat python `file.py`
- First run with `uv run`

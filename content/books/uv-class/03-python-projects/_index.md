---
title: "Python Projects and Configuration"
weight: 30
date: 2025-12-22T00:00:00Z
description: |
  Python Projects and Configuration

---

This chapter introduces the modern Python project model.
It explains `pyproject.toml` as the central contract for a project, what information lives there,
and what older mechanisms it replaces.

The goal is to give students a stable vocabulary for discussing projects, builds, dependencies, and tooling.

## Topics

- The Python project lifecycle
  - `pyproject.toml`
  - Purpose
  - Structure
  - Human intent vs machine state
- What `pyproject.toml` replaced
  - `setup.py`, `setup.cfg`
  - `requirements.txt`, `requirements-dev.txt`
  - `pip freeze`
- Dependency declaration vs resolution 
- Build metadata vs runtime metadata

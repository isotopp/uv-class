---
title: "What uv is and how it works"
weight: 20
date: 2025-12-22T00:00:00Z
description: |
  What uv is and how it works.

---

This chapter explains what **uv actually does**, beyond “it installs dependencies”.
Students learn uv’s mental model: environments are isolated, reproducible, disposable, and fast to create.
This chapter builds the conceptual foundation that makes later workflows intuitive.

This is where speed, caching, and isolation are explained once, so they don’t have to be re-explained everywhere else.

## Topics

- What problems uv solves
  - Scope of uv
    - Project management
    - Environment management
    - Tool execution
    - Packaging and publishing
  - Environments and isolation
    - Project environments  
    - Temporary isolated environments
    - Why isolation is the default 
  - Why uv is fast
    - Global cache
    - Shared wheels
    - Deterministic resolution
  - Cache management
  - What is cached
  - Where it lives
  - When to clear it and when not to

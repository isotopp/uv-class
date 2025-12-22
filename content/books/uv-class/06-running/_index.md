---
title: "Running code and tools consistently"
weight: 60
date: 2025-12-22T00:00:00Z
description: |
  Running code and tools consistently

---

This chapter establishes uv as the single execution interface.
Students learn that running code, tests, linters, and formatters are all the same category of action:
executing tools in a controlled environment.

This is where habits are formed.

## Topics

- `uv run`
  - Project commands
  - Tool commands
- Running modules vs files
- Entry points vs scripts
- Editable installs
  - Running the editable vs. running the installed (`uv tool install .`, more about that later)
- Tool execution
  - `pytest`
  - `ruff` (`ruff format`, `ruff check --fix`), replaces `black` and `pylint`
  - `mypy` (to be replaced with `ty` in the future)
- Why not call tools directly
  - How to `pytest` multiple versions of Python
- Reproducible execution across machines and CI

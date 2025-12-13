# Project structure and hygiene

## `src` layout vs. flat layout

Flat Layout

```
berlin-weather/
├── berlin_weather.py
├── pyproject.toml
└── tests/
```

Common structure for small scripts, and how most beginners start out.
Not recommended.
Looks simple, but is broken.

- Imports can succeed accidentally because the project root is on `sys.path`
- Code may work locally and fail when installed or packaged
- Tests may import the wrong module without noticing 

This is what `uv init new-dir` produces.
We don't want that.

`src` layout looks like this:

```
berlin-weather/
├── src/
│   └── berlin_weather/
│       ├── __init__.py
│       └── cli.py
├── pyproject.toml
└── tests/
```

Advantages:
- Imports behave exactly like installed packages
- Tests cannot accidentally import from the working directory
- Packaging issues surface early
- Refactoring is safer

Modern Python tooling strongly prefers the `src` layout for anything beyond a single file.

ALWAYS use `src` layout.
This is what `uv init --package new-dir` does.

## Tests are not in `src`

Tests are not part of the application runtime.
They have no place in `src`.

Recommended structure:

```
$ uv init --package berlin-weather
$ <edit edit>
$ tree berlin-weather
berlin-weather/
├── src/berlin_weather/
├── tests/
│   ├── test_cli.py
│   └── test_weather.py
```

- test-only imports do not leak into runtime.
- package contains only the actual source
- Users installing a wheel do not receive test code.
- `pytest` expects this, and works automatically.

## What to `.gitignore`

- the `.venv`
- all `__pycache__` and `*.pyc` files
- Tool caches and temporary files, including `dist`.

What should not be ignored and must be checked in:

- `pyproject.toml`
- `uv.lock`
- Source Code
- Tests

Example:

```
# Python files
/.venv
__pycache__
*.pyc
.pytest_cache

# IDE
/.idea

# Secrets
/.env

# Test runs and data
/downloaded_files
*.log
```


## README.md, AGENTS.md

README.md is for humans encountering the project for the first time.
Minimum recommended contents:

- One-sentence description of what the project does
- How to install or set up the project
- How to run it
- How to run tests
- Supported Python versions

AGENTS.md is a convention used to document automated actors interacting with the repository.
That is, it tells the LLM (codex, junie, copilot, and so on) how to behave.
It can also explain the same thing in the same language to human contributors.
It should tell what files can be modified and which must not be modified under which circumstances.
It should explain project policies, style guides, testing instructions and so on.

```
# AGENTS.md

## Purpose

This document defines the rules and expectations for automated agents,
tooling, and humans acting with automation assistance in this repository.

The goal is to keep the project reproducible, maintainable, and safe from accidental dependency or tooling drift.

---

## Dependency Management Policy

- Dependencies **must be added or removed using uv commands**:
  - `uv add`
  - `uv remove`

- `pyproject.toml` **must not be edited manually** for dependency changes unless there is no supported uv command to express the change.

- `uv.lock` **must never be edited by hand**.
  - If the lockfile needs to change, regenerate it using:
    ```
    uv lock
    ```
  - Any change to `uv.lock` must be intentional and reviewable.

---

## Execution Policy

- All project commands **must be executed via `uv run`**.
  - Examples:
    - `uv run pytest`
    - `uv run mypy`
    - `uv run ruff check`
  - Never call tools directly (e.g. `pytest`, `mypy`, `ruff`) without `uv run`.

This ensures correct Python version selection and reproducible environments.

---

## Testing Policy

- All tests **must be executed** after any code change.
  - Command:
    ```
    uv run pytest
    ```

- Tests are fast and must not be skipped.

- Failing tests **must not be disabled or marked as xfail**.
  - Broken code must be fixed instead.

---

## Formatting and Linting Policy

At the end of each edit cycle, the following commands must be run:

uv run pytest
uv run mypy
uv run ruff check --fix src tests
uv run ruff format src tests

Additional tooling may be run as appropriate (for example, type checking),
but these commands are the minimum required baseline.

---

## General Principles

- Reproducibility over convenience.
- Explicit commands over implicit behavior.
- Fix problems rather than silencing tools.
- Keep changes minimal, intentional, and reviewable.

This repository assumes modern Python tooling discipline.
```

This is only a starting point and can be adjusted to match project and AI needs.

# Naming

- Project names: lowercase, hyphenated: `berlin-weather`
- Packages, Module names: can't contain hyphens, so `berlin_weather`
- Test files start with `test_...` and mirror the source file name, `test_cli.py` for `cli.py`.
- Modules: Short, descriptive nouns.

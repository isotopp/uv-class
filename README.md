# Basic `uv`

1. What problem uv solves
2. Python environments and isolation
3. Installing and using uv
4. Creating a project
5. Dependency management
6. Running code and scripts
7. Lockfiles and reproducibility
8. Project structure and hygiene
9. Tooling integrations
10. Best practices and common mistakes 
11. Migration and comparison with older tools

# What Problem `uv` solves

## Topics

- Why Python projects break
- “Works on my machine” explained
- Dependencies, versions, conflicts
- Why pip alone is not enough

## Why first

Motivation and explanation of the problem space before starting.
We need to feel the pain first to justify the workflow `uv` solves.

## Side Topics

- very lighy intro of historioc tooling, `pip`, `venv`., `poetry` and `pipenv` plus `pyenv`.
- emphasize that `uv` replaces most of these tools, not adds more tooling on top.

# Python environments and isolation

## Topics

- Global Python vs project Python
- What a virtual environment is
- Why isolation matters
- One project, one environment

## Why

`uv` concepts make no sense without environments.
This section builds the mental model `uv` relies on.

## Side topics

`PATH`, `PYTHONPATH`, system python changes without notice,
packaging python dependencies also makes them old.
Multiple Python versions existing at once.

# Installing and using uv

## Topics

- Installing uv on macOS, Linux, Windows
- Verifying installation
- `uv --help`
- Philosophy of `uv` commands

## Why here

Get them started on a basic project.
Quick trial, "Hello Python".

## Side topics

- Why `uv` is fast: Rust plus local cache.
- Single binary concept

## Example Script

https://github.com/isotopp/uv-class/tree/main/berlin-weather

# Creating a project

## Topics

- uv init
- Project layout overview
- `pyproject.toml` purpose
- Naming a project

## Why

- With the example project, now go through things in detail

# Side topics

- What `pyproject.toml` replaced

# Dependency Management

## Topics

- `uv add`
- `uv remove`
- Runtime vs development dependencies
- Semantic versioning basics

## Why 
This is the core daily use of `uv`.
Students should learn safe dependency habits early.

## Side topics

- What dependency resolution means
- Why pinning matters

# Running code and scripts

## Topics

- `uv run`
- Running Python files
- Entry points
- Scripts vs modules

## Side topics

- Reproducible execution
- Brief mention of shebangs (if needed)

# Lockfiles and reproducibility

## Topics

- What a lockfile is (what does `uv.lock` look like exactly, and why is that there?)
- What is actually used when `uv sync` and `uv run` are used - `pyproject.toml` or `uv.lock` and why?
- Sharing projects and deterministic installs
- The `uv lock` command and upgrades.

## Side topics

- Why lockfiles belong in git

# Project structure and hygiene

## Topics

- `src` layout vs flat layout
- Keeping tests separate
- README basics
- Ignoring files correctly

## Side topics

- Minimal `.gitignore`
- Naming conventions

# Tooling integrations

## Topics

- Linters and formatters via `uv`
- Testing tools
- Running tools consistently

## Why
- 
- Shows `uv` as a hub, not just a dependency installer.
- Encourages automation thinking.

# Side topics

- `ruff` as an example
- `pytestz basics


# Best practices and common mistakes

## Topics

- Never editing lockfiles by hand
- Not mixing pip and uv
- One project per environment
- Keeping Python versions explicit

## Side topics

- When to delete and recreate environments
- Reading error messages calmly
- Asking the tool what it knows

# Migration and comparison with older tools

## Topics

- `uv` vs `pip` + `venv`
- `uv` vs `poetry`
- When `uv` is enough
- When something else might be needed

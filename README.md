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

## Side topics

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

- Shows `uv` as a hub, not just a dependency installer.
- Encourages automation thinking.

## Side topics

- `ruff` as an example
- `pytest` basics

# Migration and comparison with older tools

## Topics

- `uv` vs `pip` + `venv`
- `uv` vs `poetry`
- When `uv` is enough
- When something else might be needed

# Building Python projects

## What “building” means

Core idea:  Building a Python project means turning source code into a distributable artifact.

That artifact is usually:
- a wheel (.whl)
- sometimes a source distribution (.tar.gz)

Building does not mean:
- running the code
- installing dependencies
- compiling Python itself

Building is packaging code so someone else can install it without your source tree.

## Topics

- What a build artifact is
- When building is required
- What uv does and does not do
- Relationship between build and install

## When you do not need to build

Examples:
- internal tools
- applications run from source
- services deployed from a git checkout
- projects using `uv run`

Most application developers never need to build wheels.

## When you do need to build

Examples:
- publishing a library
- distributing a CLI to users
- shipping prebuilt artifacts
- CI/CD release workflows

## What uv’s role is

- uv understands build metadata
- uv installs build dependencies
- uv delegates building to a backend

uv is an orchestrator, not a compiler.

## Side topics

- Difference between “editable install” and built wheel
- Why wheels are preferred over source installs

# Wheels and distribution artifacts

## What a wheel is

Core idea: A wheel is a pre-packaged, installable Python package distribution.

Properties:
- fast to install
- no code execution during install
- deterministic contents
- platform-specific when needed

```
berlin_weather-0.1.0-py3-none-any.whl
```

## Topics

- Wheel naming
- Platform tags
- Pure Python vs platform wheels
- Why wheels exist

## Why

Most python people do not even know what a wheel is and why it matters.

## Wheel anatomy

- metadata
- packaged modules
- entry points

## Pure Python wheels

- py3-none-any
- easiest case
- common for teaching examples

## Platform wheels

- OS and architecture tags
- C extensions
- why building becomes harder

## Side topics

- why source distributions still exist
- why wheels are cached aggressively

# Build backends

Core idea: A build backend is the tool that actually performs the build of a wheel.

Examples:
- setuptools (strongly deprecated)
- hatchling (previously the default in `uv`)
- poetry-core
- uv_build (now default in `uv`)

Defined in `pyproject.toml`:

```toml
[build-system]
build-backend = "uv_build" # The default
```

## Topics

- PEP 517 and PEP 518
- Role of `[build-system]`
- Separation of frontend and backend
- Why backends exist

## Why

- `uv` does not build, it uses a backend
- the backend is pluggable
- tooling interoperability depends on this design

## Frontends vs backends

- Frontend: uv, pip, build
- Backend: hatchling, uv_build

The frontend asks for a build, the backend performs it.

## Why this replaced `setup.py`

- no arbitrary code execution
- reproducible builds
- isolated build environments

## Side topics

- Why most users never touch `[build-system]`
- When changing backends makes sense

# Publishing packages

Core idea: Publishing means uploading built artifacts to a package index ("index").

Common targets:
- PyPI
- internal company registries (actualy just an Apache dir, but many shops use JFrog Artifactory)
- private indexes or caches

Publishing always comes after building.

## Topics

- Build vs publish
- Versioning responsibility
- Authentication and trust
- Release automation

## When to publish

- libraries
- reusable tools
- shared components

In companies, teams usually publish to artifactory, so that production, CI and other teams pull from there.

## When not to publish

- internal scripts
- applications deployed from source
- coursework projects

## uv’s role in publishing

- uv prepares metadata
- uv installs build tools
- upload handled by dedicated tooling
- uv integrates, it does not monopolize.

## Side topics

- Why publishing is a social contract
- Why version numbers matter
- Why deletion is discouraged
- 

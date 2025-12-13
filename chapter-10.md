# Migration and comparison with older tools

This chapter is deliberately high level.
Students should not memorize tool differences, but understand why `uv` exists and when to reach for something else.

Where migration is involved, the authoritative source is Astral’s own documentation.
This chapter explains the reasoning, not the step-by-step mechanics.

## `uv` vs `pip` + `venv`

The classic Python setup looks like this:

- create a virtual environment with `python -m venv`
- activate it
- install dependencies with `pip install`
- freeze dependencies with `pip freeze`
- hope everyone did the same thing

Problems with this approach:

- Environment activation is manual and error-prone
- pip freeze captures (`pip freeze -r requirements.txt > requirements-frozen.txt` remedies that in part, but most projects don't do that)
- No first-class lockfile (even a frozen requirements file is only recording version numbers)
- Tooling versions drift silently (people do not treat a venv as disposable – recreate often!)
- CI setups diverge from local setups

`uv` replaces this stack with a single coherent system, and treats a venv as disposeable:

- automatic environment management
- dependency declaration in pyproject.toml with groups
- deterministic lockfile (uv.lock)
- fast, reliable resolution
- one command (`uv run`) to execute everything in the right environment

Key advantage:
- uv removes entire classes of mistakes, not just steps

-> works by default, enforces identical environments

## `uv` vs. `poetry`

Poetry did important work in setting standards:

- `pyproject.toml` as the source of truth
- dependency groups, lockfiles
- reproducible installs and 
- project centric workflows

`uv` rewrites this in a single rust binary for speed.
Faster (a lot!), single file, migration pathes, `pip` integration, full workflow end-to-end.

## When something else may be needed

- Projects that depend heavily on C, C++ integrations
- system libraries
- GPU toolchains

`uv` works to cover these as well, but may not be there in all cases.

- system package managers
- conda or conda-like environments
- container-based workflows

---

- Projects with code-generation from protobufs or OpenAPI
- language servers or SDK generators
- mixed-lang builds

These will require additional tools:

- build tools (`make` lookalikes)
- generatoes (`protobuf` et al)
- custom glue

`uv` can `uv run` these tools, not replace them.

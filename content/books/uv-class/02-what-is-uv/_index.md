---
title: "What uv is and how it works"
weight: 20
date: 2025-12-22T00:00:00Z
description: |
  What uv is and how it works.

---

{{% details title="**Summary**" open=true %}}
Everything in `uv` follows the same pattern: declare intent in `pyproject.toml`,
let `uv` resolve and lock dependencies in `uv.lock`, execute inside isolated environments that are recreated on the fly.
{{% /details %}}

## Topics

  - Environments and isolation
    - Project environments  
    - Temporary isolated environments

  - Cache management
  - What is cached
  - Where it lives
  - When to clear it and when not to

# What uv actually does

This chapter explains what `uv` actually does, beyond the shorthand “it installs dependencies”.

At its core, `uv` is a project-centric orchestration tool.
It coordinates Python versions, environments, dependencies, tools, builds, and publishing in a way that is fast,
reproducible, and difficult to misuse.

The key ideas to keep in mind throughout this chapter are:

- environments are isolated
- environments are reproducible
- environments are disposable
- creating and updating environments is cheap

Once these ideas are understood, most `uv` commands become self-explanatory.

# What an environment is

A Python environment is a concrete, runnable Python context made up of:

- A specific Python interpreter and stdlib, the standard library that comes with that interpreter
- A set of installed third-party packages
- Metadata describing how those packages were installed

`uv` manages all of these pieces together, instead of leaving them to separate tools and conventions.

## Python version

Every environment is built around one specific Python version, such as `3.11`, `3.12` or `3.14`.
The version determines language features, behavior of built-in modules, ABI compatibility, and
which third-party wheels can be installed.

`uv` can install and manage Python interpreters themselves, or use the operating system Python interpreter.

> [!CAUTION]
> Never use the system python.
> Always use a `--managed-python` with `uv`.

Using `uv` to manage python versions avoids the use of the system-managed system-python.
A Python provided by the operating system may contain modules on top of stdlib,
which may have been installed as OS packages to enable the system python to do system python things.
This makes it specific to your OS version and update level.

This Python is also managed and updated by the system,
which means it will change over time and outside your control.
This is generally ruining reproducibility, for example,
your system python and its environment will not match a CI environment – different bugs, different behavior.

Using `uv` with managed python versions gives you clean python environments with no preinstalled packages beyond stdlib,
allows you to have multiple versions (for example, for automated testing),
and makes sure the same python version is used everywhere (for example, on your machine and in CI).

> [!TIP]
> Using `uv` with `--managed-python` is the preferred way to use `uv` and Python.

When you request a Python version that is not present, `uv` can download and install it.
The interpreter comes with its matching standard library.
The Python version is fully isolated from system Python installations.
This is similar in spirit to tools like `pyenv`, but integrated directly into the project workflow.

`uv` does not install system libraries, compilers, operating system packages or non-Python runtimes.

For example, if a Python package requires a system library (such as OpenSSL or a C compiler),
that must be provided by the operating system or container, or you need to use something like `conda`.

## Virtual environments

A virtual environment is a directory that contains:

- a link to a Python interpreter (or a copy thereof)
- an isolated site-packages directory with the packages needed
- Python metadata pointing to those locations

It exists to ensure that packages installed for one project do not affect another.

`uv` creates and manages virtual environments automatically, implicitly and very quickly.
You do not run `python -m venv`.
You do not activate environments.
You do not manually install packages.

Instead:
- `uv sync` ensures the environment matches the lockfile
- `uv run` executes commands inside the environment

The environment is treated as a derived artifact, not something you curate by hand.
It is also completely disposable: You do not normally notice `uv` throwing away or rebuilding your virtual environment.
It is just there, always with exactly the tools, libraries and versions you configured. 

# Intent, Resolution, Lockfile

The environment contains Python packages.
The collection of Python packages on top of stdlib are called the project dependencies.
Each dependency has a version attached to it.

In the `pyproject.toml`, each dependency is declared with a range of acceptable versions for it.
Usually (and by default) that is "any version newer than the version we used when we started using the dependency".
This looks like

```toml
dependencies = [
    "httpx>=0.28.1",
]
```

This is declarative, and expresses our *intention*: We say what packages we need, and what versions are acceptable.
We do not say which *exact* version is to be used.

`uv` **resolves** dependencies by looking at the totality of all declared dependencies,
even those that are optional or separated out into other dependency groups.

It then tries to find versions that are compatible: For example, when one component depends on `httpx>=0.28.1`,
and another component we declared transitively depends on `httpx>=0.26.3`, `uv` will choose a version of
`httpx>=0.28.1`, because that is compatible with all packages that want `httpx`.

The outcome of the resolution is written to `uv.lock` and kept unchanged.
There, the exact version, file source and `sha` checksum are recorded.
The results from the `uv.lock` are used in a sync or run.

> [!TIP]
> The `uv.lock` file is a derived file, but it **must** be checked in,
> so that the exact same versions of packages are being used in every checkout by you, your colleages and the CI.

This guarantees that all users of our project will use the exact same versions of all dependencies at all times,
making runs identical and reproducible, across developer machines, CI/CD environments and installations.

This is also why *all* dependency groups are taken into account *all* of the time,
even those that are not relevant for this exact install:
We do **not** want the version of `httpx`
that is being used to change depending on the `dev` dependencies being installed or not.

A Python project can have many dependencies.
`uv` allows us to group them into separate groups, the default group being what is needed to run the project,
and additional groups typically being things such as `dev` (containing `ruff` and `mypy`) 
or `test` (containing `pytest`).

An `uv.lock` file will not change once it is created.
Upgrading versions is a conscious and reversible decision, and done with the `uv lock` command.

# What problem `uv` solves

Traditional Python workflows accumulate state over time:
- environments are created manually and forgotten
- environments are shared between projects
- dependencies are installed incrementally and drift
- tools are installed globally and differ per machine

Developers end up with a "works on my machine" situation, and fragile codebases:
Because virtual environments are not managed down to the checksum-level there may be subtle differences between different machines,
containers or other environments.
The development environment and the deployment environment can diverge, the process becomes fragile,
and instead of debugging code we debug environments.

`uv` prevents that by avoiding this situation structurally: each project is treated as the unit of truth,
not the machine.

It also makes the environment disposable,
recreated on the fly and completely dependent on the `pyproject.toml` and the resolved `uv.lock` file.
This creates freshly created,
up-to-date and statically resolved environments
that are upgraded to new versions in a controlled and reversible  process.

# From `setup.py` and `requirements.txt` to `pyproject.toml`

Python projects historically lack a single, authoritative definition:
metadata in `setup.py` embedded in executable Python code,
dependencies in `requirements.txt` and dev tools in `requirements-dev.txt`,
plus a number of scripts scattered across files in undefined locations.

This fragmentation makes it hard to understand what a project actually is,
much less parse this in a reliable way.

`uv` centers the project around `pyproject.toml`: project metadata lives in one place,
dependencies are declared explicitly,
scripts and entry points are defined once in a central place and  all tooling reads the same configuration.

`uv init` creates a project that already fits this model, instead of requiring manual cleanup later.

`uv` does not replace version control systems like `git` (but initializes a repo and creates a skeleton `.gitignore`),
documentation conventions (but creates an empty `README.md` as a starting point),
application-specific project structure decisions (but creates the necessary scaffolding).

Using `uv` habitually, you can't forget to activate the environment,
won't accidentally install dependencies into the global interpreter, won't have environment drift,
and don't have to wait for environment recreation.

For `uv`, environments are derived artifacts and not precious state.
They are created automatically, recreated if necessary, cheap to discard and rebuilt, and not "activated".

Using `uv`, projects are always isolated from each other.
Environments are never shared or re-used, state does not leak.
Multiple versions of environments, such as "the same environment with different Python versions" can be created and used.

Using dependency groups, `uv` also records tooling used, and tool versions.
Tools are (an optionally installable) part of the environment, they are dependencies.

This ensures identical tooling and tool versions across all developers (put your preferences into your own group!),
identical tooling in CI, reproducible results, and predictable behavior.

It collapses several categories into one:
- running the application
- running tests
- running linters
- running formatters

are all just commands executed inside a known environment.

`uv` does not replace `pytest`, `ruff` or `mypy`, but it makes sure they are installed in defined versions,
and run with the correct interpreter across machines.

# Beyond development and execution

Packaging is often misunderstood as something separate from development:
build tools feel opaque, 
publishing feels risky, 
metadata and build logic are scattered.
Many developers avoid packaging entirely because it seems complex,
they recommend running a git checkout.

`uv` integrates packaging into the same lifecycle:
project metadata is already present, 
build dependencies are declared explicitly, 
builds run in isolated environments, 
artifacts are reproducible.

Commands like `uv build`,
`uv publish` and `uv tool install .` use the same configuration and environment model as everything else.

`uv` does not replace build backends such as: setuptools, hatchling, scikit-build-core or meson-python.
Instead, it acts as a frontend, invoking these backends in a controlled, isolated way.

# Speed and caching

In `uv`, an environment is treated as disposable, and the environment is very frequently recreated.
This needs to be fast.

`uv` uses a global cache, and wheels are cached across projects, resolved dependencies are reused,
builds avoid unnecessary work.
This cache is, by default, a local directory.

```bash
$ uv cache dir
~/.cache/uv
$ uv cache size --human
warning: `uv cache size` is experimental and may change without warning. Pass `--preview-features cache-size` to disable this warning.
352.9MiB
```

The cache prevents multiple downloads of wheels and packages,
allowing recreation of a good-sized venv in a few hundred milliseconds "on the fly".

This is the foundation of `uv`'s speed and isolation.

# Exercises

## 1. Core Concepts (Reproduction)
What are the four key ideas about environments that `uv` promotes (as listed in the beginning of this chapter)?
Briefly explain what "environments are disposable" means in the context of `uv`.

## 2. The Role of the Lockfile (Reproduction)
Why is it mandatory to check the `uv.lock` file into version control?
What is the difference between "intent" (in `pyproject.toml`) and "resolution" (in `uv.lock`)?

## 3. Investigating the Cache (Application)
Run `uv cache dir` to find your local cache directory.
Then, run `uv cache size --human` (you might need to enable preview features as shown in the chapter).
How much space is your `uv` cache currently using?

## 4. Environment Isolation (Application)
Create two new projects in separate directories using `uv init`.
Add different dependencies to each (e.g., `uv add requests` in one and `uv add httpx` in the other).
Use `uv run python -c "import requests"` and `uv run python -c "import httpx"` in both directories.
What happens, and how does this demonstrate isolation?

## 5. The "Works on My Machine" Problem (Transfer)
A colleague says: "I don't need `uv.lock`, I just use `requirements.txt` with versions like `requests>=2.0.0`.
It works fine on my machine."
Based on what you learned about environment drift and reproducibility,
explain to them why this approach might lead to failures in CI/CD or on a teammate's machine.

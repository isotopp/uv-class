---
title: "Building, packaging, and publishing"
weight: 80
date: 2026-01-08T00:00:00Z
description: |
  Mastering `uv build` and `uv publish`: understanding wheels, source distributions, and the role of build backends in the Python lifecycle.
---

{{% details title="**Summary**" open=true %}}
**Building Packages:** `uv build` creates source distributions (sdists) and wheels, which are the standard formats for sharing Python code.

**Build Backends:** `uv` acts as a frontend that coordinates with backends like `hatchling`, `setuptools`, or `scikit-build-core` to perform the actual packaging.

**Native Extensions:** For performance-critical code, `uv` supports building native extensions written in C, Rust, or other languages via specialized backends.

**Publishing:** `uv publish` securely uploads built artifacts to PyPI or private registries, with built-in support for Trusted Publishing and duplicate check protection.

**Best Practices:** Always verify builds locally, use version control for tags, and prefer Trusted Publishing in CI/CD environments.
{{% /details %}}

# What "building" means

In the Python world, "building" a project refers to the process of turning your source code into a standardized,
distributable format that others can easily install.
This is the bridge between "code on your machine" and "a package on PyPI."

When you build a project, you typically produce two types of artifacts: **Source Distributions (sdists)** 
and **Binary Distributions (wheels)**.

## Wheels and Source Distributions

### Source Distributions (sdist)
An `sdist` is essentially a snapshot of your source code (usually a `.tar.gz` file) along with some metadata.
- **Pros:** It is universal; it contains the original code.
- **Cons:** It requires the installer to perform the build step. If the project contains C or Rust code, the user must have a compiler and the necessary system libraries installed.

### Wheels (wheel)
A wheel is a built, "ready-to-install" format (a `.whl` file). It is essentially a ZIP archive with a specific structure.
- **Pros:** Installation is nearly instantaneous (just unpacking). No compiler is needed on the user's machine.
- **Cons:** For projects with native code, you must build and provide different wheels for every platform (Linux, macOS,
Windows) and architecture (x86_64, ARM64) you want to support.

# Build Backends

Python uses a "frontend/backend" architecture for packaging, defined in [PEP 517](https://peps.python.org/pep-0517/).

### Frontend vs. Backend
- **The Frontend (`uv`):** This is the tool you interact with. `uv` handles the environment, downloads dependencies, 
and calls the backend.
- **The Backend:** This is the tool that actually knows how to pack your files into a wheel or sdist. 
Common backends include `hatchling`, `setuptools`, `maturin`, and `scikit_build`.

### Why backends exist
Backends exist because different projects have different needs. 
A pure Python project might use a simple backend like `hatchling`, 
while a high-performance project with C++ code might use `scikit-build-core` or `meson-python`.

By separating the frontend from the backend,
`uv` can support any build system without having to know the specifics of how every language or compiler works.

# Native Extensions Overview

Some Python packages aren't just Python.
They contain "native extensions" written in languages like C, C++,
or Rust to achieve performance that Python alone cannot provide.

When `uv` encounters a project with native extensions, its role remains the same:
it provides the isolated build environment and the necessary tools (like `cmake` or `cargo`),
then lets the specialized backend handle the compilation.

# `uv build`

`uv build` is the command that orchestrates the building process.

```bash
uv build
```

When you run this command:
1. `uv` reads your `pyproject.toml` to see which `build-backend` you have chosen.
2. It creates an isolated, temporary virtual environment.
3. It installs the required build dependencies (defined in `[build-system]`).
4. It calls the backend to produce an `sdist` in the `dist/` directory.
5. It then (usually) builds a `wheel` from that `sdist`.

### Useful Flags
- `--wheel`: Build only the wheel.
- `--sdist`: Build only the source distribution.
- `--out-dir <DIR>`: Change where the artifacts are placed (defaults to `dist/`).

# Publishing Packages

Once you have your files in `dist/`, you can share them with the world (on [PyPI](https://pypi.org)) or with your team (on a private registry).

### When and what to publish
- **Publish when:** You have a stable, tested version that you want others to use.
- **What to publish:** Both the `sdist` and the `wheel`. This ensures maximum compatibility for all users.

### When not to publish
- **Internal projects:** Do not publish private or proprietary code to the public PyPI! Use a private registry or install directly from Git.
- **Broken builds:** Always run your tests against the built wheel (using `uv run --no-editable`) before publishing.

# `uv publish`

`uv publish` is the command used to upload your artifacts to a registry.

```bash
uv publish
```

By default, it looks for files in the `dist/` directory and attempts to upload them to PyPI.

### Authentication and Best Practices

For security, you should avoid using your raw PyPI password. 
Instead, use:
1. **API Tokens:** Generate a scoped token on PyPI *per project* and use it with `--token`.
Using a different token per project allows you to scope things appropriately,
and also prevents you from mistakenly publishing code to the wrong project.
2. **Trusted Publishing:** If you are using GitHub Actions, `uv` supports "Trusted Publishing,"
which uses OIDC tokens to authenticate without needing any secrets stored in your repository.

### Preventing Duplicates
`uv publish` is "idempotent" if you use the `--check-url` flag (or the `--index` shorthand).
If a file with the exact same name and content already exists on the server, `uv` will skip it instead of erroring.
This is extremely useful for retrying failed CI jobs.

Example of a robust publish command:
```bash
uv publish --index pypi
```
(This assumes you have configured `pypi` in your `uv.toml` with the appropriate `publish-url`).

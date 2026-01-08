---
title: "Dependencies, environments, and reproducibility"
weight: 50
date: 2025-12-22T00:00:00Z
description: |
  Dependencies, environments, and reproducibility

---

{{% details title="**Summary**" open=true %}}
**Dependency Management:** Use `uv add` and `uv remove` to manage dependencies. `uv` updates `pyproject.toml` and `uv.lock` simultaneously.

**Lockfiles:** The `uv.lock` file ensures reproducible environments across all machines by recording exact versions and hashes.

**Syncing:** `uv sync` ensures the virtual environment matches the lockfile.

**Docker Optimization:** Use flags like `--no-install-project`, `--no-install-local`, and `--no-dev` to optimize Docker layers and reduce image size.
{{% /details %}}

## Topics

- Adding and removing dependencies
  - `uv add`
  - `uv remove`
- Runtime vs development dependencies
  - `uv add --dev`, `uv remove --dev`
  - `uv add --group <name>`, `uv remove --group <name>`
- Dependency resolution
  - When?
  - What is considered?
  - Versions, Version ranges, what is chosen?
- Lockfiles
  - What `uv.lock` contains
  - Why it exists
  - Why lockfiles belong in `git`
- `uv sync` and `uv run`
  - What they read
  - Why lockfiles are authoritative
- Upgrading with `uv lock`
- Sharing projects and deterministic installs
- Dependencies and Docker Installs
  - `--no-install-project`
  - `--no-install-local`
  - `--no-dev`
  - `--only-group <name>`
  - Layer caching strategies
- Installation
  - Installer options: `--link-mode`, `--reinstall`, `--compile-bytecode`
  - Cache options: `--no-cache`, `--refresh`
  - Python discovery and `--managed-python`

# Python Projects and Dependencies

After getting the basics out of the way,
let's dive deeper into how `uv` handles dependencies and why it does things the way it does,
using our `berlin-weather` project as a reference.

## Adding and removing dependencies

Managing dependencies in `uv` is primarily done through the `uv add` and `uv remove` commands.

### `uv add`

When we ran `uv add httpx` in the `berlin-weather` project, `uv` performed several actions:

1. It looked up `httpx` on PyPI.
2. It found the latest compatible version.
3. It updated the `dependencies` array in `pyproject.toml`.
4. It resolved the entire dependency tree (including `httpx`'s own dependencies like `anyio` and `httpcore`).
5. It updated the `uv.lock` file with the exact versions and checksums.
6. It synchronized the virtual environment in `.venv`.

**Why this way?**
By updating both `pyproject.toml` (your intent) and `uv.lock` (the resolution) immediately,
`uv` ensures that your development environment is always in sync with your declarations.

### Version constraints

You may also specify version constraints in `uv add`:

```
uv add "httpx>=0.23,<0.30"
```

`uv` puts exactly this version specifier with constraints into `pyproject.toml` and uses this to resolve.
This particular version constraint will allow `uv` to use `httpx` versions from `0.23` up to but not including `0.30`.


### `uv remove`

Similarly to `uv add`, `uv remove httpx` would:

1. Remove the entry from `pyproject.toml`.
2. Re-resolve the project (removing any transitive dependencies that are no longer needed).
3. Update `uv.lock`.
4. Clean up the `.venv`.

## Runtime vs development dependencies

Not all dependencies are needed to run the application. Some are only needed for development or testing.

A dependency is defined as "code that is required for the application or build process to function,
but that you did not write."
Dependencies are imported through your codebase through download, from PyPI or other package repositories,
Python also uses the term "index" for this.

All dependencies are declared in the `pyproject.toml`, and are assigned a dependency group.
The `uv` dependency resolution process decides what exact version of a dependency is being downloaded from an index, 
and this decision is recorded in the `uv.lock` file.

Types of dependencies are:

### Runtime Dependencies

These are required for the application to function.
In `berlin-weather`, `httpx` is a runtime dependency.
They are stored in the `[project.dependencies]` section of `pyproject.toml`.

### Development Dependencies (`--dev`)

Tools like `ruff` (for formatting) or `mypy` (for type checking) are not needed by the end-user of your weather app.
By running `uv add --dev ruff mypy`, you tell `uv` to put these in a special `dev` group.

- These are stored under `[dependency-groups]` in `pyproject.toml`.
- They are included in your local development environment by default.

### Dependency Groups (`--group <name>`)

You can create arbitrary groups for specific needs.
`--dev` is just shorthand for the longer `--group dev` option,
because about every projecy will need development dependencies.
But we can create arbitrarily named groups and add dependencies to them.

Another commonly used group is `test`.
We used `uv add --group test pytest` for our testing framework.

This allows a CI system to install *only* what it needs (e.g., `uv sync --group test` might be enough to run tests,
avoiding the overhead of `mypy` or `ruff` if those are not run as part of the testing cycle).

## Dependency resolution

Resolution is the process of finding a set of package versions that satisfy all constraints.

When does it happen?
: Every time you `add`, `remove`, or run `uv lock`.
  `uv` is designed to be so fast that it can re-resolve the entire project frequently.

What is considered?
: `uv` considers all dependency groups during resolution.

Versions and Ranges
: By default,
  `uv add` uses the newest version of a library
  that is compatible with all requirements from all packages and the `pyproject.toml`.
  Different resolver strategies exist (`--resolution <strategy>` switch), discussed elsewhere.

Why this way?
: Resolving all groups together prevents "dependency hell"
where adding a test tool later breaks your runtime environment.
If a conflict exists, `uv` finds it immediately rather than at deployment time.
Also, the same versions of everything are installed at all times, so the behavior (and the bugs)
of your project does not change when certain dependency groups are activated or deactivated.

## Result of Dependency Resolution

Resolution
: "Find a compatible set of versions"

That means:

- Take the declared dependencies
- Take their dependencies and their dependencies dependencies and so on -> transitive dependencies
- Look at all version constraints
- Look at the Python Version constraints

Find the newest set of dependencies that, taken together, fulfills all constraints.

- `berlin-weather` depends on `httpx`
- `httpx` depends on `httpcore` and many others.

- We also added `dev` and `test` dependencies.

```
$ uv pip tree
berlin-weather v0.1.0
└── httpx v0.28.1
    ├── anyio v4.12.1
    │   └── idna v3.11
    ├── certifi v2026.1.4
    ├── httpcore v1.0.9
    │   ├── certifi v2026.1.4
    │   └── h11 v0.16.0
    └── idna v3.11
mypy v1.19.1
├── librt v0.7.7
├── mypy-extensions v1.1.0
├── pathspec v1.0.2
└── typing-extensions v4.15.0
pytest v9.0.2
├── iniconfig v2.3.0
├── packaging v25.0
├── pluggy v1.6.0
└── pygments v2.19.2
ruff v0.14.10
```

The version numbers shown reflect the resolved environment, not the constraint set.

"Resolution" is a graph problem and becomes hard very quickly in larger projects.
It is not easy to solve for humans, which is why we write tools for it.

## Lockfiles

The `uv.lock` file is what powers reproducibility in `uv`.

What it contains
: Every single package in your environment (direct and transitive), its exact version, the source URL,
  and a cryptographic hash (SHA-256) of the file.
Why it exists
: To eliminate "works on my machine."
  It records exactly what was used during a successful resolution, no matter where it is being installed.
Why it belongs in Git
: By checking in `uv.lock`, you ensure that every developer, every CI runner,
  and every production deployment uses the *exact* same bytes for every dependency.

## `uv sync` and `uv run`

These commands are consumers of the lockfile.

Authority
: The `uv.lock` file is authoritative.
  When you run `uv sync`, `uv` doesn't look at PyPI to see if there's a newer version;
  it looks at the lockfile and makes your `.venv` match it exactly.
  You can tell `uv sync` to activate or deactivate dependency groups, though.

Automatic Sync
: `uv run` will automatically check if your `pyproject.toml` or `uv.lock` has changed 
  and perform a hidden `uv sync` if needed.

Why this way?
: This makes the virtual environment a "derived artifact."
You don't "manage" the `.venv`; you manage the `pyproject.toml` and `uv.lock`, and `uv` makes the `.venv` happen.

## Upgrading with `uv lock`

To update your dependencies to newer versions allowed by your `pyproject.toml` constraints, use:
- `uv lock --upgrade`: Upgrades all dependencies to the latest compatible versions.
- `uv lock --upgrade-package httpx`: Upgrades only `httpx` (and its dependencies if necessary).

This updates the `uv.lock` file, which you then test and commit.

## Sharing projects and deterministic installs

When a teammate clones the `berlin-weather` repo, they just run `uv sync`.

- `uv` reads `uv.lock`.
- `uv` downloads the exact wheels (verified by hashes).
- `uv` creates a `.venv` identical to yours.

This is a **deterministic install**.
The result is guaranteed to be the same regardless of when or where the command is run.

# Dependencies and Docker Installs

In a development environment, we usually want everything: the project, the runtime dependencies,
and the development tools.
But in a Docker container (especially for production), we want the opposite: as little as possible.

`uv sync` provides several options to control exactly what gets installed, which is crucial for building small,
efficient, and well-cached Docker images.

## Layer Caching and `--no-install-project`

Docker builds are faster when they can reuse previous layers.
The most expensive part of a Python build is usually installing dependencies.

If we copy our entire project and then run `uv sync`,
any small change to our source code will invalidate the Docker cache, forcing a full re-install of all dependencies.

To avoid this, we use the "dependency-first" pattern:

1. **Copy metadata only**: Copy `pyproject.toml` and `uv.lock` first.
2. **Install dependencies**: Run `uv sync --frozen --no-cache --no-install-project`.
   - `--frozen`: Ensures that `uv` does not update the `uv.lock` file. It will fail if the lockfile is out of sync with `pyproject.toml`. This is critical for reproducible builds.
   - `--no-cache`: Prevents `uv` from using the local cache.
     In Docker, avoiding the cache helps keep the image size down if we don't manage a persistent cache volume.
     Instead, your environments cache on the network is being used, that is,
     images are pulled from artifactory or whatever else is configured.
     But no `$HOME/.cache` is being used.
   - `--no-install-project`: Installs all dependencies into `.venv` but skips installing the project itself (the code in `src/`).
3. **Copy source code**: Copy the rest of your application code.
4. **Final Sync**: Run `uv sync --frozen --no-cache`. This will be nearly instant because the dependencies are already cached in a Docker layer.

```dockerfile
# Install dependencies first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --no-install-project

# Now copy the source code and install the project
COPY . .
RUN uv sync --frozen --no-cache
```

Dependencies change less often than the source code itself,
so Docker layer caching can kick in and our build speed will be higher
than if we did the install in the normal order (source code first,
dependencies second).

## Reducing Image Size with `--no-dev` and `--only-group`

Production images should not contain `pytest`, `ruff`, or `mypy`.
These tools take up space and increase the attack surface of your container.

- `--no-dev`: Excludes the `dev` dependency group.
- `--no-group <name>`: Excludes a specific group (e.g., `--no-group test`).
- `--only-group <name>`: Installs *only* the specified group.
  Note that this **excludes** the base `project.dependencies` and the project itself.
- `--no-install-local`: Skips the project and any local path dependencies. This is ideal for caching only heavy third-party packages from PyPI in an early Docker layer.

For a production web service, you might use:
```bash
uv sync --frozen --no-dev --no-group test
```

If you want an image that contains *only* the tools needed for testing, you might use:
```bash
uv sync --frozen --only-group test
```

and use this as a base layer for the "dependencies first install" outlines above.

## Summary of Exclusions

| Option                 | Effect                                                               |
|:-----------------------|:---------------------------------------------------------------------|
| `--no-install-project` | Skips installing the current project, but keeps its dependencies.    |
| `--no-install-local`   | Skips the project and all local/path dependencies. Best for caching. |
| `--no-dev`             | Omits the `dev` group.                                               |
| `--no-group <name>`    | Omits a specific named group.                                        |
| `--only-group <name>`  | Installs ONLY the named group (omits project and base deps).         |
| `--no-default-groups`  | Skips the default `dev` group.                                       |

By combining these flags, you can ensure that your CI environments get exactly the test tools they need,
while your production images remain lean and focused.

# Installation

While `uv sync` is the primary command to ensure your environment matches your lockfile,
several options control *how* that installation happens.
These options are crucial for optimizing performance, managing disk space,
and ensuring reliability in different environments.

## Installer Options

These flags control the mechanics of how packages are placed into your `.venv`.

### `--link-mode`

`uv` uses a global cache to avoid downloading the same packages repeatedly. The `--link-mode` option determines how packages are moved from this cache into your project's `site-packages`:

- `clone` (default on macOS): Uses "copy-on-write" clones.
  It's fast and doesn't take extra disk space, but allows the OS to separate files if they are modified.
  It requires that the cache directory is on the same filesystem as the `.venv`.
  That means it will not work with the user home on the internal disk, and the work directory on an external USB or network drive.
- `hardlink` (default on Linux/Windows): Creates hard links.
  Extremely fast and uses zero additional space, but files are shared across all environments.
  But the `.venv` and the cache must be on the same filesystem for this to work.
- `copy`: Physically copies the files.
  Slower and uses more disk space, but ensures the environment is completely independent of the cache.
- `symlink`: Creates symbolic links.
  Fast, but dangerous: if you clear the `uv` cache, your virtual environments will break because the target files are gone.
  Use of this mode is discouraged.

### `--reinstall` and `--reinstall-package`

- `--reinstall`: Forces `uv` to reinstall all packages even if they are already present. This is a "nuclear option" for fixing a corrupted environment.
- `--reinstall-package <name>`: Reinstalls only the specified package.

### `--compile-bytecode`

By default, Python compiles `.py` files to `.pyc` bytecode lazily (the first time they are imported).
Using `--compile-bytecode` during `uv sync` forces this compilation for all packages immediately.

- **Pros**: Faster application startup time.
- **Cons**: Longer installation time.
- **Usage**: Highly recommended for Docker images and CLI tools where startup latency matters.

## Cache Options

The `uv` cache is the heart of its speed.
See where it is located with `uv cache dir`.
By default, on MacOS and Linux, `$HOME/.cache/uv`.

- `--no-cache`: Tells `uv` to ignore the global cache entirely for the current operation. 
  - **In Docker**: Use this to keep your image small if you aren't using a persistent cache mount.
  - **Debugging**: Use this to rule out cache corruption issues.
- `--refresh`: Invalidates all cached data and re-downloads everything.
- `--refresh-package <name>`: Refreshes the cache for a specific package.

In a normal development workflow, you rarely need these.
But in a CI/CD pipeline,
`--refresh` ensures you are getting the absolute latest files if a package was re-published with the same version 
(which shouldn't happen, but sometimes does in private registries).

# Exercises

## 1. Python Projects and Dependencies
- **Reproduction:** What is the difference between `[project.dependencies]` and `[dependency-groups]` in `pyproject.toml`?
- **Reproduction:** How do you add a dependency to a specific group named `test`?
- **Application:** You want to add `requests` but only versions in the `2.x` range starting from `2.31.0`. Write the `uv add` command for this.

## 2. Dependency Resolution
- **Reproduction:** When does `uv` perform dependency resolution?
- **Reproduction:** Does `uv` resolve only the active dependency groups, or all of them? Why?
- **Application:** If package A requires `httpx>=0.20` and package B requires `httpx<0.28`, what version range will `uv` consider for `httpx`?

## 3. Lockfiles
- **Reproduction:** Name three things recorded in `uv.lock` for every package.
- **Reproduction:** Why should `uv.lock` be committed to version control?
- **Application:** You suspect a colleague is using a different version of a transitive dependency than you are. How can `uv.lock` help you prove this or resolve the discrepancy?

## 4. `uv sync` and `uv run`
- **Reproduction:** What is the relationship between `uv.lock` and `uv sync`?
- **Reproduction:** Why is it said that the `.venv` is a "derived artifact"?
- **Application:** You have just pulled changes from Git that include an updated `uv.lock`. What command should you run to ensure your local environment matches?

## 5. Dependencies and Docker Installs
- **Reproduction:** What is the purpose of the `--frozen` flag in a Docker `RUN` command?
- **Reproduction:** What does `--no-install-project` do, and how does it help with Docker layer caching?
- **Application:** Write a `uv sync` command for a CI job that only needs the `test` dependency group and must not include the `dev` group or the main project code.
- **Transfer:** Design a multi-stage Dockerfile strategy for a `uv`-managed project. Your strategy should:
    1. Maximize caching of third-party dependencies.
    2. Result in a production image that contains only the runtime dependencies (no `dev` or `test` tools).
    3. Include pre-compiled Python bytecode for faster startup.
    4. Ensure the final image is as small as possible.
    Explain each step of your strategy and the flags used.

## 6. Installation
- **Reproduction:** Explain the difference between `clone` and `copy` link modes. Which one is default on macOS?
- **Reproduction:** What is the benefit of using `--compile-bytecode` during installation?
- **Application:** You are working on a machine with very limited disk space and multiple `uv` projects. Which `--link-mode` would you choose to minimize disk usage, and what is the requirement for it to work?

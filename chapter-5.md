# Dependency Management

## What is a dependency?

- Code you didn't write, but rely on

In `berlin-weather`, `httpx` and of course Python itself, plus it's stdlib.
Python (at a certain version) and stdlib are implied,
`httpx` needed to be declared.

Dependencies are declared in the `pyproject.toml`:

```toml
requires-python = ">=3.14"
dependencies = [
    "httpx>=0.28.1",
]
```

`uv` resolves dependencies, and locks them (every time you `add`, `remove`, or `sync`).
It also installs them (you do not (and should not) need to run `pip`): `uv run ...` builds the environment from the lock file.

- You declare dependencies.
- `uv` installs them,

Resolving means to find a set of dependencies and transitive dependencies that do no contradict each other and fulfill the requirements.

## Adding dependencies

```
uv add httpx
```

- updates `pyproject.toml`
- resolves compatible versions
- updates `uv.lock`
- recreates the `.venv`

After running the command, the `pyproject.toml` contains

```toml
[project]
dependencies = [
    "httpx>=0.28.1",
]
```

- **Never** edit `uv.lock` manually.
- Do not run `pip install`.

`uv` builds the `uv.lock` lockfile, and rebuilds the `.venv`.

## Version constraints

```
uv add "httpx>=0.23,<0.30"
```

`uv` puts exactly this version specifier with constraints into `pyproject.toml` and uses this to resolve.
The newest compatible version is chosen and locked.

## Removing dependencies

``` 
uv remove httpx
```

- Removes the dependency from `pyproject.toml`
- Resolves the resulting remaining dependencies
- Updates `uv.lock`
- Recreates the `.venv`

Do not remove (or add) dependencies by hand (by editing `pyproject.toml` directly).
If you did, `uv sync`.

## Runtime and dev dependencies

**Runtime dependencies** are dependencies that your code needs to run.
In `berlin-weather`, `httpx` is a runtime dependency, because `cli.py` imports it and the program can't run without it.

Runtime dependencies live in `dependencies = ...` in `[project]

## Development dependencies

Development dependencies are tools used by developers to write, format, check or test the code.

Examples:

- `pytest` test frameowrk
- `ruff` linter and formatter
- `ty` or `mypy` type checkers
- `pre-commit` or other hooks and tools

They are not required to run `berlin-weather`, but we use them when building it.

`uv` supports "dependency groups", and one of them is `dev`:

```
uv add --group dev pytest
```

We get

```diff
$ diff -u p pyproject.toml
--- p	2025-12-13 20:06:12
+++ pyproject.toml	2025-12-13 20:06:55
@@ -17,3 +17,9 @@
 [build-system]
 requires = ["uv_build>=0.9.16,<0.10.0"]
 build-backend = "uv_build"
+
+[dependency-groups]
+dev = [
+    "mypy>=1.19.0",
+]
+
```

The `dev` dependency group is special, we can also `uv add --dev mypy` for the same result.
But we can have dependency groups of any name:

```
$ cp pyproject.toml q
$ uv add --group schnork ruff
$ diff -u q pyproject.toml
--- q	2025-12-13 20:08:09
+++ pyproject.toml	2025-12-13 20:08:23
@@ -22,4 +22,7 @@
 dev = [
     "mypy>=1.19.0",
 ]
+schnork = [
+    "ruff>=0.14.9",
+]
```

Reading `uv help sync` is recommended at some point.

```
uv sync --no-dev # dev dependencies are automatically installed, we can tell it not to.
uv sync --group schnork # the dependency group schnork is also installed.
```

**Important:** Resolution always includes **all** dependency groups.
This influences versions chosen.
Not selected dependency groups are not installed (some, like **dev** are autoselected).

```
kk:berlin-weather kris$ uv sync
Resolved 13 packages in 11ms
Uninstalled 1 package in 1ms
 - ruff==0.14.9
kk:berlin-weather kris$ uv sync --group schnork
Resolved 13 packages in 14ms
Installed 1 package in 4ms
 + ruff==0.14.9
```

## Semver (Semantic versioning)

Most Python packages use semver: `maj.min.patch`.

For example, `0.28.1`:

- Major `0` is incremented for breaking changes.
- Minor `28` is incremented for new, compatible features.
- Patch `1` is incremented for bug fixes.

Constraints tell `uv` what version you want:

- `httpx>=0.28.1` - version 0.28.1 or higher.
- `httpx>=0.28.1,<0.30` - a safe range avoiding the next major break (we know somehow that 0.30 will not work)

## Resolution

- Resolution = "Find a compatible set of versions"

That means:

- Take the declared dependencies
- Take their dependencies and their dependencies dependencies and so on -> transitive dependencies
- Look at all version constraints
- Look at the Python Version constraints

Find the newest set of dependencies, that together fulfills all constraints.

- `berlin-weather` depends on `httpx`
- `httpx` depends on `httpcore` and many others.

- We also added `dev` and `schnork` dependencies. 

```
$ uv pip tree
berlin-weather v0.1.0
└── httpx v0.28.1
    ├── anyio v4.12.0
    │   └── idna v3.11
    ├── certifi v2025.11.12
    ├── httpcore v1.0.9
    │   ├── certifi v2025.11.12
    │   └── h11 v0.16.0
    └── idna v3.11
mypy v1.19.0
├── librt v0.7.3
├── mypy-extensions v1.1.0
├── pathspec v0.12.1
└── typing-extensions v4.15.0
ruff v0.14.9
```

The version numbers shown reflect the resolved environment, not the constraint set.

"Resolution" is a graph problem and becomes hard very quickly in larger projects.
It is not easy to solve for humans, which is why we write tools for it.

## Pinning (`uv.lock`)

Pinning matters. The `pyproject.toml` expresses intent: What requirements we have.
A later resolution, or a resolution with different indexes (package sources) can lead to different results,
and reproduction problems.

The `uv.lock` file records our local solution to resolution, and checks it in. With exact version numbers, and with checksums.
That is, we will detect tampering even if the version numbers do not change.

This makes the build and test reproducible in other environments.
Together with CI/CD, we can be sure that what we tested is also running exactly as tested in production.

# Summary

- use `uv add` and `uv remove`.
- Keep runtime and dev dependencies separate.
- Do not pin exact version numbers in `pyproject.toml`.
- Build the lockfile, and check it in.

- `uv` does not use `pip`, but offers a partial `pip` cli in `uv pip`.
- `uv pip tree`, `uv pip tree --reverse`.

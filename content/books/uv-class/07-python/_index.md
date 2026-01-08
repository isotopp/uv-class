---
title: "Python Management"
weight: 70
date: 2026-01-08T00:00:00Z
description: |
  How uv manages Python versions, the benefits of managed Python, and the uv python toolset.
---

{{% details title="**Summary**" open=true %}}
**Python Management:** `uv` can automatically download and manage Python interpreters, ensuring consistent environments across machines.

**Managed Python:** Using `uv`-managed Python versions is preferred as it avoids the "it works on my machine" problem caused by system Python variations.

**Python Selection:** `uv` finds the correct Python version using `pyproject.toml`, `.python-version` files, and command-line flags.

**Tooling:** The `uv python` subcommand provides tools to install, list, upgrade, and pin Python versions globally or per project.
{{% /details %}}

# Where does `uv` get its Python version from?

By default, `uv` doesn't just look for what is installed on your system. It has the ability to download and manage its own Python interpreters. These interpreters are provided by the [python-build-standalone](https://github.com/astral-sh/python-build-standalone) project (maintained by Astral, the creators of `uv`).

These are highly portable, self-contained Python builds that are designed to be unpacked and run from any directory. They are:
- **Consistent:** Every user on every platform gets the exact same build of a specific Python version.
- **Isolated:** They do not interfere with your system Python or other versions.
- **Optimized:** They are built with modern compilers and optimizations (like LTO and PGO) for maximum performance.

When `uv` needs a Python version that it doesn't have, it fetches these pre-built binaries, unpacks them into its internal storage, and uses them to create your virtual environments.

# Why managed Python?

In previous chapters, we emphasized: **Never use the system Python.**

The "System Python" is the one that comes with your operating system (e.g., `/usr/bin/python3` on macOS or Linux). It is there for the OS to run its own scripts. It often has OS-specific patches, non-standard libraries, or pre-installed packages that can lead to subtle bugs in your application.

By using **Managed Python**, you ensure:
1. **Reproducibility:** Everyone on the team uses the exact same Python binary.
2. **Cleanliness:** The interpreter starts with a completely empty `site-packages` (only the standard library).
3. **Flexibility:** You can easily switch between Python 3.10, 3.12, 3.14, or even experimental "Free-threaded" (GIL-less) builds without any complex system setup.

Variants:
- Starting with 3.13 (3.14 in as the default), the free-threaded variants of Python become available. Selector: `+freethreaded`.
- If you want a variant with a global lock (gil), the selector is `+gil`.
- Debug builds of Python are slower and not useful for general use, but a non-optimized version of Python with Debug symbols can be requested as the `+debug` variant.

### Enforcing Managed Python

You can tell `uv` to *only* use its managed versions and ignore whatever is on your `PATH` by setting an environment variable or a config option:

```bash
export UV_PYTHON_PREFERENCE=only-managed
```

Or in your `uv.toml`:

```toml
[uv]
python-preference = "only-managed"
```

This is a great way to ensure that you never accidentally rely on a local system installation.

Valid values for this option are:

- only-managed: Only use managed Python installations; never use system Python installations.
- managed: the default, use managed Python installations, if already downloaded. Use System python versions, if matching the requested version. Only download new managed Python if the requested version cannot otherwise be matched.
- system: Prefer system Python installations over managed Python installations.
- only-system: Only use system Python installations; never use managed Python installations. Equivalent to --no-managed-python.

# Requesting a version

When you create an environment or run a script, you can specify exactly which Python version you want.

```bash
uv venv --python 3.13
uv run --python 3.11 my_script.py
```

Even if you request a specific version, `uv` will still respect the `requires-python` constraint in your `pyproject.toml`. If you ask for `3.10` but your project requires `>=3.12`, `uv` will report an error.

### Version Specifier Formats

The `--python` argument is very flexible:
- **Simple version:** `3.13` (Gets the latest patch of 3.13).
- **Exact version:** `3.13.1`.
- **Range:** `'>= 3.10,<3.13'` (Finds the best fit within the range).
- **Implementation:** `cpython@3.12` or `pypy@3.10`.
- **Variants:** `3.13+gil` (specifically requests a free-threaded build).
- **System Path:** If you *must* use a specific local Python, you can provide the absolute path: `--python /opt/homebrew/bin/python3.12`.

### Disabling Downloads

If you are in an environment where you don't want `uv` to download anything (e.g., for security or bandwidth reasons), you can disable automatic downloads:

```bash
uv sync --no-python-downloads
```

# The `.python-version` file

To avoid typing `--python` every time, you can "pin" a version for your project using a `.python-version` file.

If a `.python-version` file exists in your project root, `uv` will use that version by default for all commands in that directory.

### Global Pins

You can also set a default Python version for your entire user account:

```bash
uv python pin --global 3.12
```

This creates a `.python-version` file in `~/.config/uv/` (on Unix) or the equivalent configuration directory on your platform. Now, whenever you are *not* inside a project that specifies its own version, `uv` will default to 3.12.

# The `uv python` toolset

The `uv python` subcommand provides a set of tools for inspecting and managing your Python installations.

### `uv python list`
Lists all Python versions available to `uv`, including those already installed and those available for download.

```
$ uv python list
cpython-3.14.2-macos-aarch64-none   /opt/homebrew/bin/python3.14 -> ../Cellar/python@3.14/3.14.2/bin/python3.14
cpython-3.13.11-macos-aarch64-none  ~/.local/share/uv/python/cpython-3.13.11-macos-aarch64-none/bin/python3.13
cpython-3.11.14-macos-aarch64-none  <download available>
...
```

The options `--managed-python` and `--no-managed-python` select for managed and not managed Python versions, respectively.

### `uv python install`
Manually download and install specific versions.
```
$ uv python install cpython-3.8.20-macos-aarch64-none
Installed Python 3.8.20 in 929ms
 + cpython-3.8.20-macos-aarch64-none
```

### `uv python uninstall`
Remove a version to save disk space.

```
$ uv python uninstall cpython-3.8.20-macos-aarch64-none
Searching for Python versions matching: cpython-3.8.20-macos-aarch64-none
Uninstalled Python 3.8.20 in 109ms
 - cpython-3.8.20-macos-aarch64-none (python3.8)
```

`uv` will only uninstall `uv`-managed versions of Python.
Use the installer for the found Python to uninstall the Python version managed by other systems,
for example `brew uninstall python#3.8` to uninstall a Python version 3.8 managed by homebrew.

### `uv python find`
Show the path to the interpreter that `uv` would use for a given requirement.
```
$ pwd
~/Source/uv-class/berlin-weather
$ uv python find
~/Source/uv-class/berlin-weather/.venv/bin/python3
$ uv python find 3.8
error: No interpreter found for Python 3.8 in virtual environments, managed installations, or search path
$ uv python find 3.11
/opt/homebrew/opt/python@3.11/bin/python3.11
```

### `uv python dir`
Shows where `uv` stores its managed Python installations.
```
$ uv python dir
~/.local/share/uv/python
```

### `uv python upgrade`
Updates your managed Python installations to the latest available patch versions.
``` 
$ uv python upgrade
warning: `uv python upgrade` is experimental and may change without warning. Pass `--preview-features python-upgrade` to disable this warning
All versions already on latest supported patch release
```

### `uv python pin`

As seen before, this creates or updates a `.python-version` file in the current directory (or globally with `--global`).

# Exercises

## 1. Python Sources
- **Reproduction:** Where does `uv` obtain its pre-built Python binaries from by default?
- **Reproduction:** List three characteristics of these `python-build-standalone` interpreters that make them suitable for `uv`.
- **Application:** Run `uv python dir` on your machine. Explore the directory. What is the internal structure `uv` uses to store different Python versions?
- **Application:** If you are in a highly restricted network environment, what flag or environment variable would you use to prevent `uv` from trying to download a Python interpreter?

## 2. Why Managed Python?
- **Reproduction:** Why is it generally discouraged to use the "System Python" for development projects?
- **Reproduction:** What are the three main benefits of using **Managed Python** as described in this chapter?
- **Application:** Configure your environment (either via shell variable or `uv.toml`) to *only* allow managed Python versions. Verify this by trying to use a system Python path with `uv venv --python /usr/bin/python3`. What error does `uv` return?
- **Application:** Explain a scenario where using a `uv`-managed Python might be problematic, specifically regarding GUI libraries.

## 3. Requesting a Version
- **Reproduction:** What is the difference between requesting `--python 3.13` and `--python 3.13.1`?
- **Reproduction:** How does `uv` react if you request `--python 3.10` for a project that has `requires-python = ">=3.12"` in its `pyproject.toml`?
- **Application:** Write a command to create a virtual environment using a specific Python implementation (e.g., PyPy) at version 3.10.
- **Application:** Use `uv run` to execute a one-liner that prints the version of a free-threaded (GIL-less) Python build (e.g., `3.13+gil`).

## 4. The `.python-version` File
- **Reproduction:** What happens when you run a `uv` command in a directory that contains a `.python-version` file?
- **Reproduction:** How do you set a "Global Pin" for a Python version, and where is that setting stored?
- **Application:** Create a new directory and "pin" it to Python 3.11 using `uv python pin`. Verify the content of the created file.
- **Application:** You have a global pin of 3.12, but your project directory has a `.python-version` with 3.13. Which version will `uv` use when you run `uv run python --version` inside that project?

## 5. The `uv python` Toolset
- **Reproduction:** Which command allows you to see all Python versions `uv` knows about, including those not yet installed?
- **Reproduction:** What is the purpose of `uv python update-shell`?
- **Application:** Use `uv python find` to locate the interpreter `uv` would use for the current project. How does this output change if you are inside a project with a `.venv` versus outside any project?
- **Application:** You have several old Python patch versions installed (e.g., 3.12.1, 3.12.2) and want to update them to the latest available patches. Which command should you run, and what is its current status in `uv`?

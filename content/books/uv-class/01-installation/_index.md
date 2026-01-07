---
title: "Installing and Configuring uv"
weight: 10
date: 2025-12-22T00:00:00Z
description: |
  Installation and Configuration of uv

---

{{% details title="**Summary**" open=true %}}
**Choosing an installation method:** Use the native installer if you want the simplest, most direct setup.
Use Homebrew, Scoop, or Winget if you prefer centralized tool management.
Use Cargo only if you are a Rust developer or contributor.
All methods install the same uv binary. The difference is how updates and removal are handled.

**Shell integration** is optional but recommended. Completion improves discoverability and correctness.
{{% /details %}}

This chapter establishes `uv` as a system tool, not just a project tool.
Students learn how `uv` is installed, updated, and integrated into their shell, and where persistent configuration lives.
The goal is to make `uv` feel reliable, discoverable, and non-magical from the start.

Understanding installation and configuration early avoids later confusion about PATH issues, mismatched versions,
or “why does `uv` behave differently on this machine”.


# Installing `uv`

`uv` is distributed as a single, self-contained executable.
You do not need Python, `pip`, or an existing virtual environment to install it.
This makes installation fast, predictable, and easy to undo: `uv` is one single,
self-contained binary that goes into the system path.

There are several supported installation methods.
Which one you choose depends on your platform and how you manage system tools.

## Using the native installer (recommended)

The native installer is the recommended method on all platforms.
It installs a prebuilt `uv` binary and places it on your `PATH`.

### Linux and macOS

On Linux and macOS, use the official installer script:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

What this does:
- Downloads a precompiled `uv` and `uvx` binary for your platform
- Installs it without privileges into a user-local directory
  - On MacOS and Linux, it goes into `$HOME/.local/bin`.
- Updates your shell configuration so `uv` is on your `PATH`
  - On MacOS and Linux, using `bash`, you end up with
    ```bash
       # uv
       export PATH="$HOME/.local/bin:$PATH"
    ```
    at the end of `$HOME/.bash_profile`.

After installation, restart your shell (or in `bash`, run `hash -r`) or reload your profile, then verify:

```bash
which uv
uv --version # or 
uv self version
```

This method does not require administrator privileges and does not modify system Python installations,
nor does it require a preinstalled version of Python on your system at all.

### Windows

On Windows, the native installer is provided as a PowerShell script:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

This installs `uv` into a user-local directory and updates the `PATH` for your user account.

After installation, open a new terminal and verify:

```powershell
uv --version
```

### Updating using the native installer

Run the command

```bash
uv self update
```

> [!WARNING]
> This can only work if `uv` is installed locally (is writeable by you), and if the `uv` version is natively installed.
> If you try this on a version installed by Homebrew or another managed install, it will not work:
> 
> ```bash
> $ uv self update
> error: uv was installed through an external package manager and cannot update itself.
> 
> hint: You installed uv using Homebrew. To update uv, run `brew update && brew upgrade uv`
> ```

## Installing on MacOS with Homebrew

If you manage developer tools with Homebrew, you can install `uv` that way instead.

```bash
brew install uv
```

Later, upgrade with `brew upgrade uv`.

Use this method if
- You already manage most tools with Homebrew
- You prefer system-wide package management

## Installing on Windows with Scoop or Winget

On Windows, uv is also available through common package managers.

```powershell
scoop install uv
```

Scoop installs `uv` into your user profile and manages `PATH` automatically.

```powershell
winget install astral-sh.uv
```

Winget installs `uv` system-wide and integrates with Windows package management.

Choose Scoop or Winget if you already rely on them for other tools.

Updates are done using the native method for your package manager.

## Installing with Cargo (for Rust developers)

If you are a Rust developer or want to work on `uv` itself, you may prefer installing using Cargo.

```bash
cargo install uv
```

> [!CAUTION]
> This method is **not** recommended for general users, but it is appropriate if you:
> - contribute to uv
> - want to track development versions
> - are already managing Rust tools with Cargo

## Verifying the installation

Regardless of how you installed `uv`, always verify:

```bash
$ uv --version
uv 0.9.16 (Homebrew 2025-12-06)
```
or `uv self version --output-format json`:

```json
{
  "package_name": "uv",
  "version": "0.9.16",
  "commit_info": {
    "short_commit_hash": "Homebrew",
    "commit_hash": "Homebrew",
    "commit_date": "2025-12-06",
    "last_tag": null,
    "commits_since_last_tag": 0
  }
}

```

# Shell/Powershell Completion (optional step)

Once `uv` is installed, integrating it with your shell improves usability and discoverability.
This is not required to use `uv`, but it significantly reduces friction,
especially when learning the tool or exploring less frequently used commands.

## Linux and macOS shells

`uv` supports shell completion for: `bash`, `zsh`, `fish`.
To generate completion scripts, use:

```bash
uv generate-shell-completion bash
```

or replace "bash" with the name of your shell.
The command prints the completions to standard output.
You typically redirect this output into the appropriate completion directory for your shell.
After installing completions, restart your shell or reload its configuration.

## Windows Powershell

On Windows, `uv` can generate PowerShell completion scripts as well.

```powershell
uv generate-shell-completion powershell
```

This outputs a PowerShell script that enables tab completion for `uv`.
Typically, you append this output to your PowerShell profile file so it loads automatically:

```powershell
uv generate-shell-completion powershell >> $PROFILE
```

After restarting PowerShell, tab completion for `uv` commands becomes available.

# Configuration

`uv` can be configured in three different ways: command-line flags, configuration files, and environment variables.
All three exist to support different use cases, from one-off commands to persistent, shared configuration.

There is a hierarchy of configuration option sources:

- Command-line flags override everything
- Configuration files provide persistent defaults
- Environment variables act as a fallback and integration mechanism

Not every setting exists in all three forms, but many important ones do.
When multiple forms exist, they are designed to map cleanly to each other.

## Command-line flags

Command-line flags are the most explicit and visible way to configure uv.

Examples:

```bash
uv run --python 3.12
uv sync --frozen
uv add --group dev ruff
```

Flags
- apply to a single invocation
- are easy to discover via `uv help`
- always take precedence

## Configuration files

Configuration files allow you to set persistent defaults without repeating flags on every command.

`uv` supports configuration files at multiple levels:
- per-project configuration as a section in the `pyproject.toml` file of the project.
- per-user configuration via the `uv.toml` file.

Inside the `pyproject.toml`, `uv` uses the prefix `tool.uv`, so the configuration of PyPI indexes becomes

```toml
[[tool.uv.index]]
url = "https://test.pypi.org/simple"
default = true
```

In the `uv.toml`, the prefix is not used:

```toml
[[index]]
url = "https://test.pypi.org/simple"
default = true
```

`uv` will search for `pyproject.toml` or `uv.toml` files in the current directory and its parents.
`uv` will also discover `uv.toml` configuration files in the user- and system-level configuration directories, e.g.,
user-level configuration in `~/.config/uv/uv.toml`, and system-level configuration at `/etc/uv/
uv.toml` on macOS and Linux.

If multiple files are found, the options are merged in the expected way:
project-level configuration take precedence over the user-level configuration,
and user-level configuration takes precedence over the system-level configuration

Run `uv --no-config` to ignore any existing config-files.
Run `uv --config-file=...` to use a specific configuration file in `uv.toml` format,
there will be no search and all other config files will be ignored.

## Environment variables

Environment variables exist primarily for CI systems, automation and container environments.
They are also useful when configuration must be injected externally.

The `uv run` subcommand can read `.env` files, which are turned into environment variables inside the run,
which can be useful for own projects.

```bash
echo "MY_VAR='Hello, world!'" > .env
uv run --env-file .env -- python -c 'import os; print(os.getenv("MY_VAR"))'
Hello, world!
```

## Relationship between flags, config, and environment

There is no strict rule that every option has a command-line flag, a configuration file entry and an environment variable.
However, for core behavior, the mapping is usually consistent:
- a long-form flag, for example `--python`
- a configuration key with the same name, `python`
- an environment variable prefixed with `UV_`, `UV_PYTHON`.

So, `--python 3.12`, `[uv.tool]`-section `python = "3.12"` and environment variable `UV_PYTHON=3.12` correspond.

## Common options

There is a number of options that are common to all subcommands.
They are listed in the `uv help` output and in all help sections of all subcommands.

Among them are the `--managed-python` family of options, which will download and install a specific python version managed by `uv`, making an existing installation of Python optional, and forgoes using the system python.

There are `--quiet` and `--verbose` options, and there is a `--color` option controlling output colorization.

There is a `--directory` option, which does `cd` into a directory first thing the comman starts.

We already mentioned `--config-file ...` and `--no-config`.

There are TLS options and options to completely disable network access.

# Exercises

## 0. Installation (mandatory)
Install `uv` on your computer and prove that it works by displaying its version and the path to the executable.

## 1. Updating `uv` (easy)
How do you update `uv` if you installed it using the native installer?
How does this differ if you used a package manager like Homebrew or Scoop?

## 2. Configuration Hierarchy (easy)
List the three primary ways `uv` can be configured.
In what order of precedence are they applied if the same setting is defined in all three?

## 3. Shell Integration (medium)
Generate the shell completion script for your preferred shell (e.g., `bash`, `zsh`, or `powershell`).
Identify where this script needs to be placed or sourced on your system to make completions persistent across sessions.

## 4. Custom Configuration (medium)
Create a `uv.toml` file in a temporary directory that sets a specific Python version (e.g., `3.12`) as the default.
Use `uv --config-file <path>` or run `uv` from that directory to prove that it respects this configuration.

## 5. Transfer: Strategy Design (hard)
A development team wants to ensure all members use the same Python version and the same internal package index.
However, their CI/CD pipeline needs to use a different, faster mirror for the index.
Propose a configuration strategy using `pyproject.toml`, `uv.toml`,
and environment variables that satisfies these requirements while minimizing manual configuration for developers.

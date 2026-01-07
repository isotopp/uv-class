---
title: "General Options and TOML"
weight: 40
date: 2025-12-22T00:00:00Z
description: |
  What uv does, general options, and TOML for beginners.

---

# What uv can do

`uv` is a versatile tool designed to handle almost every aspect of Python development.
Below is an overview of its core capabilities.

- Manage Python `uv python ...`
- Run Scripts `uv run --script`, `uv add --script`, `uv remove --script`.
- Manage Projects `uv init`, `uv add`, `uv remove`, `uv sync`, `uv lock`, `uv run`, `uv tree`, `uv build` and `uv publish`
- Run tools: `uvx`, `uv tool run`, `uv tool install`, uv tool uninstall`, `uv tool list`, `uv tool update-shell`
- Cosplay as PIP: `uv pip ...`, and `uv pip compile`, `uv pip sync`.
- Manage a cache, `uv cache ...`, and other maintenance options `uv ... dir`, `uv self update`.

## Manage Python

`uv` can download, install, and manage multiple Python versions automatically.
Using `uv python ...` commands, you can list available versions, install specific ones,
and ensure your projects always run on the correct interpreter without relying on system-installed Python.

## Run Scripts

For standalone Python scripts, `uv` provides a seamless way to manage dependencies without a full project structure.
Commands like `uv run --script` allow you to execute scripts with inline dependency metadata,
while `uv add --script` and `uv remove --script` manage those dependencies directly within the script file.

## Manage Projects

`uv` simplifies project orchestration from initialization to publishing.
It handles scaffolding (`uv init`), dependency management (`uv add`, `uv remove`),
environment synchronization (`uv sync`), and locking (`uv lock`).
It also provides tools for inspecting dependency graphs (`uv tree`) and building or publishing packages (`uv build`,
`uv publish`).

## Run Tools

`uv` makes it easy to run and install Python-based CLI tools in isolated environments.
You can run tools instantly with `uvx` or `uv tool run`, and manage persistent installations with `uv tool install`,
`uv tool uninstall`, and `uv tool list`.
It also helps keep your environment integrated with `uv tool update-shell`.

## Cosplay as PIP

To maintain compatibility with existing workflows, `uv` can act as a drop-in replacement for `pip`.
The `uv pip` interface provides lightning-fast alternatives to common commands like `uv pip install`,
`uv pip compile` for requirements files, and `uv pip sync` for environment synchronization.

## Maintenance and Cache

`uv` includes built-in tools for self-maintenance and performance optimization.
You can manage the global package cache with `uv cache ...`, locate important directories using `uv ...
dir`, and keep the tool itself up to date with `uv self update`.

# Getting help

`uv` provides comprehensive built-in documentation through its help system.
You can access high-level help for the entire tool or detailed information for specific subcommands.

To see the main help text and a list of all available commands:

```bash
uv --help
```

For help on a specific subcommand, you can use either the `--help` flag after the command or the `help` subcommand:

```bash
uv init --help
# or
uv help init  # longer than --help
```

Because `uv` commands often have many options, the help output can be quite long.
You can pipe the output to a pager like `less` to make it easier to read:

```bash
uv run --help | less
```

# Verbose output

`uv` supports a `--verbose`/`-v` option to increase the verbosity of output.
This can be useful for debugging or understanding the steps `uv` is taking.

For example, to see detailed information about a command:

```bash
uv sync -v
```

The option can be repeated multiple times to get even more verbose output, for example `uv sync --vv`.
Usually, the verbose output also explains why `uv` is doing the things it does.

# Common options

Many options in `uv` are "global" or "common", meaning they work with almost every subcommand.
These options are always listed at the end of the help output for any command.
Because this list is long, using `| less` is particularly helpful to see all of them.

## Cache options

`uv` uses a global cache to speed up operations. You can control how `uv` interacts with this cache:

- `-n, --no-cache`: Avoids reading from or writing to the cache. `uv` will use a temporary directory for the duration of the command. This is useful for troubleshooting or ensuring a clean run.
- `--cache-dir <CACHE_DIR>`: Allows you to specify a custom path for the `uv` cache, overriding the default location.

## Python options

These options control how `uv` discovers and manages Python interpreters:

- `--managed-python` / `--no-managed-python`: Explicitly enable or disable the use of Python versions managed by `uv`.
- `--no-python-downloads`: Prevents `uv` from automatically downloading new Python versions (but the cached versions are still being used).

## Global options

These are general-purpose flags that affect `uv`'s behavior across the board:

- `-q, --quiet`: Minimizes output.
- `-v, --verbose`: Increases output detail (can be used multiple times, e.g., `-vv`).
- `--offline`: Disables all network access, forcing `uv` to rely only on cached data.
- `--directory <DIRECTORY>`: Changes the working directory before running the command.
- `--project <PROJECT>`: Forces `uv` to look for a project in a specific directory.
- `--config-file <CONFIG_FILE>`: Specifies a custom `uv.toml` file to use.
- `--no-config`: Prevents `uv` from discovering any configuration files (`pyproject.toml` or `uv.toml`).
- `--color <COLOR_CHOICE>`: Controls whether to use colored output (`auto`, `always`, or `never`).

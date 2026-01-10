---
title: "General Options and TOML"
weight: 40
date: 2025-12-22T00:00:00Z
description: |
  An overview of uv's capabilities, how to get help, common options, and the basics of TOML configuration.

---

{{% details title="**Summary**" open=true %}}
**uv's Capabilities:** uv handles Python versions, scripts, projects, tools, and provides a pip-compatible interface and cache management.

**Getting Help:** Use `uv --help`, `uv <command> --help`, or `uv help <command>` to access documentation.

**Common Options:** Global flags like `--no-cache`, `--managed-python`, `--offline`, and `--config-file` work across most subcommands.

**TOML Basics:** uv uses TOML for configuration. It supports basic types (strings, integers, booleans), tables for organization, and arrays of tables for lists of objects.
{{% /details %}}

## Topics

- What `uv` can do: A high-level overview of capabilities.
- Getting help: Navigating the built-in documentation and pagers.
- Verbose output: Using flags to see more detail.
- Common options: Global flags for cache, Python discovery, and configuration.
- TOML basics: Understanding the configuration format used by `uv`.

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
By default, `uv` detects if you are in a terminal and may automatically use a pager (like `less`) for the output.

If you want to read the help output without a pager (for example, to copy it or if you are scripting),
you can pipe the output to `cat`:

```bash
uv help init | cat
```

Conversely, if you want to explicitly use a pager,
or if you are in an environment where `uv` doesn't detect the terminal correctly, you can always pipe to `less`:

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

# TOML basics

`uv` uses TOML (Tom's Obvious, Minimal Language) for its configuration files (`pyproject.toml` and `uv.toml`).
TOML is designed to be easy to read and maps directly to a hash table (or JSON object).

## Basic types

TOML supports several basic data types:

- **Strings**: Always wrapped in double quotes. `"Hello, world!"`
- **Integers**: Plain numbers. `42`, `-10`
- **Floats**: Numbers with decimal points. `3.14`
- **Booleans**: `true` or `false` (lowercase).
- **Arrays**: Values in square brackets. `["a", "b", "c"]`

Equivalent JSON:
```json
{
  "name": "uv-project",
  "version": 1,
  "active": true,
  "tags": ["fast", "reliable"]
}
```

Equivalent TOML:
```toml
name = "uv-project"
version = 1
active = true
tags = ["fast", "reliable"]
```

## Tables

Tables (often called dictionaries or maps in other languages) are defined by a header in square brackets.
Everything following that header until the next header belongs to that table.

Equivalent JSON:
```json
{
  "project": {
    "name": "berlin-weather",
    "version": "0.1.0"
  }
}
```

Equivalent TOML:
```toml
[project]
name = "berlin-weather"
version = "0.1.0"
```

### Inline tables

For small sets of data, you can use inline tables, which look like JSON objects but use `=` instead of `:`.

```toml
authors = [{ name = "Alice", email = "alice@example.com" }]
```

## Arrays of tables

When you need a list of objects, TOML uses double square brackets `[[table]]`.
Each time you use the double bracket header, it appends a new entry to the array.

Equivalent JSON:
```json
{
  "index": [
    { "url": "https://pypi.org/simple", "default": true },
    { "url": "https://test.pypi.org/simple" }
  ]
}
```

Equivalent TOML:
```toml
[[index]]
url = "https://pypi.org/simple"
default = true

[[index]]
url = "https://test.pypi.org/simple"
```

This is how `uv` handles multiple package indexes or complex dependency groups.
Every `[[index]]` block adds another index to the list.

# Exercises

## 1. What uv can do
- **Reproduction:** Name three different categories of tasks that `uv` can manage besides project dependencies.
- **Reproduction:** What command would you use to see a tree of your project's dependencies?
- **Application:** You want to run a one-off tool that isn't in your project. Which `uv` command is specifically designed for this, and what happens to the environment after the tool finishes?
- **Application:** How would you use `uv` to check if a new version of the `uv` executable itself is available and install it?

## 2. Getting help
- **Reproduction:** What is the difference between `uv --help` and `uv help <command>`?
- **Reproduction:** How does `uv` decide whether to use a pager (like `less`) for its help output?
- **Application:** Write a command that displays the help for `uv sync` but forces the output to be displayed without a pager.
- **Application:** You are looking for a specific option in the help text of `uv run`. How can you paginate the output so you can search or scroll through it easily on a Unix-like system?

## 3. Verbose output
- **Reproduction:** Which flag is used to increase the verbosity of `uv`'s output?
- **Reproduction:** How do you get even more detailed information if the single verbose flag isn't enough?
- **Application:** Run a command like `uv python list -v`. What kind of additional information does `uv` provide that isn't in the standard output?
- **Application:** Explain a situation where using `-vv` might be helpful when `uv` is failing to resolve a dependency.

## 4. Common options
- **Reproduction:** Where in the help output are "Common options" typically listed?
- **Reproduction:** What does the `--offline` flag do, and what does it force `uv` to rely on?
- **Application:** You want to ensure `uv` uses a specific directory for its cache for a single command. Which flag would you use, and how would the command look?
- **Application:** Write a command that runs `uv sync` for a project located in `../other-project/` without first changing your current working directory in the shell.

## 5. TOML basics
- **Reproduction:** What are the basic data types supported by TOML mentioned in this chapter?
- **Reproduction:** In TOML, what is the difference between a single bracket `[table]` and double brackets `[[table]]`?
- **Application:** Convert the following JSON object into its TOML equivalent:
  ```json
  {
    "tool": {
      "uv": {
        "managed": true,
        "python": "3.12"
      }
    }
  }
  ```
- **Application:** You need to add multiple package indexes to your configuration. Show the TOML structure required to define an array of two index objects, each having a `url` and a `default` boolean.

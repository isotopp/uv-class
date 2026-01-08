---
title: "Running code and tools consistently"
weight: 60
date: 2025-12-22T00:00:00Z
description: |
  Mastering `uv run` and `uvx`: how `uv` manages environments for scripts, projects, and tools on the fly.

---

{{% details title="**Summary**" open=true %}}
**The `uv run` command** is the primary way to execute code. It ensures a consistent environment is available, creating or updating it as needed.

**Environment Discovery:** `uv` finds where it should run by looking for a `pyproject.toml`, or by creating an ephemeral environment for a single script.

**Editable Installs:** By default, `uv` installs your project in "editable" mode so changes to source code are reflected immediately.

**Tool Execution:** `uvx` (or `uv tool run`) allows running tools in isolated, temporary environments without affecting your project.

**Multiple Environments:** `uv` makes it trivial to test against multiple Python versions, either by switching the main environment or by maintaining side-by-side environments using `UV_PROJECT_ENVIRONMENT`.
{{% /details %}}

# Running Code with `uv run`

`uv run` is the Swiss Army knife of `uv`.
It is the primary way to execute Python code, scripts, or project entrypoints while ensuring they run in the correct,
isolated environment.

The most important thing to remember about `uv run` is that **it is not just a wrapper**.
It manages the environment *before* execution.
If your environment is out of sync with your `pyproject.toml` or `uv.lock`,
`uv run` will automatically perform a sync in the background before starting your program.

This will automatically, quickly and invisibly ensure that your code runs in a fresh environment.

So

- while `uv run` (and `uv sync`) create a virtual environment named `.venv` (by default)
- and you can still `.venv/bin/python your_script` or `.venv/bin/entrypoint_script`,

you should not do that.
Because if you do, you are losing the "check the environment and rebuild it" step that `uv run` executes.
Always run things with `uv run`, not directly from the virtual environment.

## Ways to use `uv run`

### `uv run <something>`

If you run a command that isn't a Python script,
`uv` looks for it in the virtual environment's `bin` (or `Scripts` on Windows) directory,
and only then in the rest of the system path.

``` 
$ uv run bash
bash-5.3$ echo $PATH
~/.local/bin:~/Source/uv-class/whoami/.venv/bin:...
```

In our `berlin-weather` project, we defined an entrypoint in `pyproject.toml`:
```toml
[project.scripts]
berlin-weather = "berlin_weather.cli:main"
```
This creates an (editable) entrypoint script `.venv/bin/berlin-weather`.

We can run this simply with:
```bash
uv run berlin-weather
```

`uv` ensures the `.venv` is up to date and then executes the `berlin-weather` script.

> [!WARNING]
> If you look closely at the `PATH` output above, you will see that `~/.local/bin` is before `.venv/bin`.
> That means production versions of tools that are named the same as project entrypoints will be found first.
> So if you installed `uv tool install .` inside the `berlin-weather` project,
> you now have a `~/.local/bin/berlin-weather` 
> that will be used even when you work with `uv run berlin-weather` inside the project.

### `uv run <script>.py`
If the argument ends in `.py`, `uv` treats it as a Python script. It is effectively a shorthand for `uv run python <script>.py`.

```bash
uv run whoami.py
```

> [!TIP] See below, the section on Scripts.
> `uv` checks if the script contains a PEP-723 inline dependency declaration for scripts.
> If it is found, `uv` will also handle the scripts dependencies.

### `uv run -m <module>`
Just like `python -m`, this runs an installed module as a script.
```bash
uv run -m json.tool blah.json
```

### `uv run -`
You can pipe Python code directly into `uv run -`. This executes the code using the project's Python interpreter and environment.
```bash
echo "import httpx; print(httpx.__version__)" | uv run -
```

## Where the environment comes from

One of the "magic" aspects of `uv run` is how it decides which environment to use.
It follows a specific discovery hierarchy:

Script Metadata
: If you run `uv run script.py` and that script contains [PEP 723](https://peps.python.org/pep-0723/) inline metadata,
`uv` creates a temporary, ephemeral environment just for that script.

Remote Scripts
: You can even run scripts directly from a URL:
```bash
uv run https://raw.githubusercontent.com/astral-sh/uv/main/scripts/uv-elapsed.py
```
`uv` will download the script, look for metadata, create an environment, and run it.

Project Discovery
: `uv` looks for a `pyproject.toml` in the current directory or any parent directory.
If found, it uses the environment associated with that project (the `.venv` directory).

> [!WARNING]
> If a virtual environment is already "active" in your shell (e.g., via `source .venv/bin/activate`),
> `uv run` will still prefer the environment it discovers via `pyproject.toml`.
> It is generally recommended **not** to activate environments when using `uv`.

## Argument Separation

When using `uv run`, you often need to pass parameters to the command you are running.
`uv` parameters must come after the `run` and before the command that `uv` is suppsed to run.

To make things clearer, you can expressly end the `uv` parameters list usingthe double-dash `--` separator:

```bash
# uv run <uv params> -- <command> <command params>
uv run --python 3.12 -- berlin-weather --verbose
```
In this example, `--python 3.12` is for `uv`, while `--verbose` is passed to the `berlin-weather` application.
Usually this is not needed, 

```bash
uv run --python 3.12 berlin-weather --verbose
```
will work just the same.

# Editable Installs

By default, when you work within a project,
`uv` installs your project into the virtual environment in **editable mode**.

### What is "Editable"?

In traditional Python, if you install a package, its files are copied into `site-packages`.
If you change your source code, you have to reinstall the package to see the changes.

An **editable install** (often called `pip install -e .`) creates a link (or a special `.pth` file)
in `site-packages` that points back to your source directory.

- **In `src` layout (`--package`):** `uv` handles the complexity of making the `src/berlin_weather` folder importable.
  It does that by adding the `src` directory to `sys.path` (in fact, it adds the directory named in the `.pth` file to the search path, and this happens to be the `src` directory).
- **In flat layout:** The current directory is made available.
  This is dangerous, because it can lead to unexpected behavior if you have files with the same name as modules in your project.
  That's one of multiple reasons why we discourage the use "flat" layout in Python and prefer the `src` layout created with `--package`. 

An editable install means you can edit your code in `src/berlin_weather/
cli.py` and immediately see the effect when you run `uv run berlin-weather`, without any re-installation step.

### `uv run --no-editable`

Sometimes you want to test your project as if it were a regular, non-editable installation (e.g.,
to ensure you haven't forgotten to include a file in your package).

```bash
uv run --no-editable berlin-weather
```

This forces `uv` to build a temporary wheel of your project and install it properly into the environment,
rather than linking to your source code.

# Tool Execution and `uvx`

Sometimes you want to run a tool (like `ruff` or `pytest`) that isn't necessarily a dependency of your project,
or you want to run it without setting up a project at all.

### What is `uvx`?

`uvx` is a convenient shorthand for `uv tool run`. It is designed for one-off tool execution.

```bash
uvx ruff format .
```

When you run this:
1.  `uv` creates an isolated, cached environment for `ruff`.
2.  It installs `ruff` into that environment.
3.  It executes the command.
4.  The environment is kept in the cache for future use, but it doesn't clutter your project's `.venv`.

### Common Tool Examples

Inside a project, you typically use `uv run` for tools declared in your `dev` group:

- **Testing:** `uv run pytest`
- **Linting & Formatting:** 
  - `uv run ruff format src` (Replaces `black`)
  - `uv run ruff check --fix src` (Replaces `pylint` and `isort`)
- **Type Checking:** `uv run mypy src`

### Automatic Parameter Supply

In many projects, you find yourself running the same long commands.
While `uv` doesn't have a built-in "task runner" like `npm run`,
it encourages the use of entrypoints or simple shell aliases.

# Multiple Environments

Because `uv` makes environment creation so cheap, you can easily test your code against multiple versions of Python.

### Example: Multi-version testing

If you want to ensure `berlin-weather` works on both Python 3.12 and 3.13:

```bash
uv run --managed-python --python 3.12 --group test pytest
uv run --managed-python --python 3.13 --group test pytest
```

`uv` will create matching `.venv` states or cached environments for these calls,
allowing you to switch back and forth instantly.
This is a powerful way to verify compatibility without the complexity of managing multiple manual installations.

### Side-by-side environments

Sometimes, you don't want `uv` to overwrite your main `.venv` every time you switch Python versions.
You might want to keep your development environment in `.venv` (e.g., using Python 3.13)
while having separate, persistent environments for testing against other versions.

You can achieve this by using the `UV_PROJECT_ENVIRONMENT` environment variable to point `uv` to a different directory:

```bash
# Create and sync the 3.12 environment
UV_PROJECT_ENVIRONMENT=.venv-3.12 uv sync --managed-python --python 3.12 --all-groups

# Create and sync the 3.13 environment
UV_PROJECT_ENVIRONMENT=.venv-3.13 uv sync --managed-python --python 3.13 --all-groups

# Run tests using the respective environments
UV_PROJECT_ENVIRONMENT=.venv-3.12 uv run --managed-python --python 3.12 --all-groups pytest
UV_PROJECT_ENVIRONMENT=.venv-3.13 uv run --managed-python --python 3.13 --all-groups pytest
```

By setting `UV_PROJECT_ENVIRONMENT`, you tell `uv` to use that specific directory instead of the default `.venv`.
This allows you to keep multiple virtual environments side-by-side in the same project directory,
and switching between them is as simple as changing the environment variable.
The default `uv run --all-groups pytest` (without the variable) will still use your main `.venv` directory.

### Simplifying multi-environment commands

Currently, `uv` does not have a built-in way to define these side-by-side environments in `pyproject.toml` or `uv.toml`.
If you find yourself frequently typing these long commands, the recommended approach is to use shell aliases,
a `Makefile`, or a task runner like `just`.

#### Option 1: Shell Aliases
Add these to your `.bashrc` or `.zshrc`:

```bash
alias uv-test-312='UV_PROJECT_ENVIRONMENT=.venv-3.12 uv run --managed-python --python 3.12 --all-groups'
alias uv-test-313='UV_PROJECT_ENVIRONMENT=.venv-3.13 uv run --managed-python --python 3.13 --all-groups'
```

Now you can simply run:
```bash
uv-test-312 pytest
```

#### Option 2: A simple `Makefile`
Create a `Makefile` in your project root:

```make
.PHONY: test-312 test-313 test-all

test-312:
	UV_PROJECT_ENVIRONMENT=.venv-3.12 uv run --managed-python --python 3.12 --all-groups pytest

test-313:
	UV_PROJECT_ENVIRONMENT=.venv-3.13 uv run --managed-python --python 3.13 --all-groups pytest

test-all: test-312 test-313
```

Then run `make test-all` to test against both versions.

# Scripts

Python has a way to specify dependencies inline in scripts, initially defined in 
[PEP-723](https://peps.python.org/pep-0723/) and now maintained in
[Inline Script Metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata).

`uv` can work with such inline script metadata.
Do make it do so, provide the option `--script`.

## Example script

```python
#!/usr/bin/env python3
# Script at /whoami/whoami.py in this repository, https://github.com/isotopp/uv-class
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.26",
# ]
# ///

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import httpx

def main() -> None:
    with httpx.Client(timeout=10.0) as client:
        r = client.get("https://httpbin.org/get")
        r.raise_for_status()

    print(f"Your apparent IP: {r.json().get('origin', 'unknown')}")

if __name__ == "__main__":
    main()
```

This short program calls `https://httpbin.org/get` to get the current IP.

## Running a script

Running this script without `uv` or without the `/// script` header results in an error due to `httpx` missing.

```
$ uv run whoami-no-dep.py
Traceback (most recent call last):
  File "~/Source/uv-class/whoami/whoami-no-dep.py", line 6, in <module>
    import httpx
ModuleNotFoundError: No module named 'httpx'
```

With the metadata block present, `uv` autodetects the metadata block (or we provide `--script`)
and creates an ephemeral virtual environment with `httpx` installed.

```
$ uv run --verbose whoami.py
DEBUG uv 0.9.21 (0dc9556ad 2025-12-30)
DEBUG Acquired shared lock for `~/.cache/uv`
DEBUG Reading inline script metadata from `whoami.py`
DEBUG Acquired exclusive lock for `~/Source/uv-class/whoami/whoami.py`
DEBUG No Python version file found in ancestors of working directory: ~/Source/uv-class/whoami
DEBUG Using Python request Python >=3.11 from `requires-python` metadata
DEBUG Checking for Python environment at: `~/.cache/uv/environments-v2/whoami-0492c73d0afa970a`
DEBUG The script environment's Python version satisfies the request: `Python >=3.11`
DEBUG Released lock at `/var/folders/dn/vtkw12w17qv7cqw5yj6lmgjh0000gn/T/uv-0492c73d0afa970a.lock`
DEBUG Acquired exclusive lock for `~/.cache/uv/environments-v2/whoami-0492c73d0afa970a`
DEBUG All requirements satisfied: anyio | certifi | h11>=0.16 | httpcore==1.* | httpx>=0.26 | idna | idna>=2.8
DEBUG Released lock at `~/.cache/uv/environments-v2/whoami-0492c73d0afa970a/.lock`
DEBUG Using Python 3.14.2 interpreter at: ~/.cache/uv/environments-v2/whoami-0492c73d0afa970a/bin/python3
DEBUG Running `python whoami.py`
DEBUG Spawned child 28443 in process group 28442
Your apparent IP: 5.166.154.224
DEBUG Command exited with code: 0
DEBUG Released lock at `~/.cache/uv/.lock`
```

The line `DEBUG Reading inline script metadata from whoami.py` shows us that the metadata block is autodetected.

The line `DEBUG Checking for Python environment at: ~/.cache/uv/environments-v2/whoami-0492c73d0afa970a` 
shows us that `uv` is looking for a Python environment in the cache directory.
This environment is kept stable and is re-used,
but is transient in the sense that `uv` can decide to trash and rebuilt it with a different name any time.

## Running a URL

We can even decide to run this script as a URL:

```
$ uv run -v 'https://raw.githubusercontent.com/isotopp/uv-class/refs/heads/main/whoami/whoami.py'
DEBUG uv 0.9.21 (0dc9556ad 2025-12-30)
DEBUG Acquired shared lock for `/Users/kris/.cache/uv`
DEBUG Reading inline script metadata from remote URL
DEBUG Acquired exclusive lock for `https://raw.githubusercontent.com/isotopp/uv-class/refs/heads/main/whoami/whoami.py`
DEBUG No Python version file found in ancestors of working directory: /Users/kris/Source/uv-class/whoami
DEBUG Using Python request Python >=3.11 from `requires-python` metadata
DEBUG Checking for Python environment at: `/Users/kris/.cache/uv/environments-v2/ed6cf9cb4d875881`
DEBUG The script environment's Python version satisfies the request: `Python >=3.11`
DEBUG Released lock at `/var/folders/dn/vtkw12w17qv7cqw5yj6lmgjh0000gn/T/uv-ed6cf9cb4d875881.lock`
DEBUG Acquired exclusive lock for `/Users/kris/.cache/uv/environments-v2/ed6cf9cb4d875881`
DEBUG All requirements satisfied: anyio | certifi | h11>=0.16 | httpcore==1.* | httpx>=0.28 | idna | idna>=2.8
DEBUG Released lock at `/Users/kris/.cache/uv/environments-v2/ed6cf9cb4d875881/.lock`
DEBUG Using Python 3.14.2 interpreter at: /Users/kris/.cache/uv/environments-v2/ed6cf9cb4d875881/bin/python3
DEBUG Running `python -c`
DEBUG Spawned child 28888 in process group 28886
Your apparent IP: 5.166.154.224
DEBUG Command exited with code: 0
DEBUG Released lock at `/Users/kris/.cache/uv/.lock`
```

This is very powerful, and also dangerous (in CI or production).
It will download arbitrary Python code from the network, install any dependencies requested
and then run that code.
There is no way to specifically disable this feature.
You can `uv run --offline ...` or `UV_OFFLINE=1 uv run ...` to disable any network access,
but there is no way to just disable uv-running a URL.

## Using `--with <dependency>`

As we saw above, if we try to run `whoami-no-dep.py`, this fails due to the missing `httpx` dependency.

Using the `--with <dependency>`, the dependency will be installed into a new, transient environment.
The dependency is allowed to violate version constraints.

```
$ uv run --with httpx whoami-no-dep.py
Your apparent IP: 5.166.154.224
```

## Editing inline dependencies

You can create a script with inline dependencies with the `--script` option:

```
$ uv init --script bla.py
Initialized script at `bla.py`

$ cat bla.py
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///


def main() -> None:
    print("Hello from bla.py!")


if __name__ == "__main__":
    main()
```

Dependencies are added and removed the same way:

``` 
$ uv add --script bla.py  httpx
Resolved 6 packages in 2ms

$ cat bla.py
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "httpx>=0.28.1",
# ]
# ///


def main() -> None:
    print("Hello from bla.py!")


if __name__ == "__main__":
    main()
```

and

``` 
$ uv remove --script bla.py httpx
Updated `bla.py`
```

## Running scripts automatically with `uv`

The magical sheband incantation to run a script through `uv` is

``` 
#!/usr/bin/env -S uv run --script
```

This will find `uv` in the path, and execute `uv` with the parameters listed `uv run --script` plus the name of the script
`uv` with automatically download a Python interpreter if needed,
detect any inline dependency declaration,
download the dependencies
and run the result.

This is rather powerful:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pyqt5>=5.15.11",
# ]
# ///

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout

app = QApplication(sys.argv)
widget = QWidget()
grid = QGridLayout()

text_label = QLabel()
text_label.setText("Hello World!")
grid.addWidget(text_label)

widget.setLayout(grid)
widget.setGeometry(100, 100, 200, 50)
widget.setWindowTitle("uv")
widget.show()
sys.exit(app.exec_())
```

and

``` 
$ ./q.py
```

will autodownload a full Qt5, and then show a small window:

![](q-py-screenshot.png)


## Making a persistent `.venv` for a script

```
uv venv
uv export --script whoami.py | uv pip sync -
```

The first command creates a `.venv` directory (optionally using options such as `--managed-python` and `--python 3.12`).
The second command takes the metadata from the script and generates a lockfile that is written to stdout.
The `uv pip` subcommand `sync` reads that and processes it, installing the dependencies into the `.venv`.

``` 
$ uv venv
Using CPython 3.14.2
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate

$ uv export --script whoami.py | uv pip sync -
Resolved 7 packages in 6ms
Resolved 6 packages in 1ms
Installed 6 packages in 5ms
 + anyio==4.12.1
 + certifi==2026.1.4
 + h11==0.16.0
 + httpcore==1.0.9
 + httpx==0.28.1
 + idna==3.11
$ ./.venv/bin/python whoami.py
Your apparent IP: 5.166.154.224
```

This is not a recommended way for handling an execution environment with `uv`,
but some tooling requires a local virtual environment with a fixed name, and this is a good way to create it.
Long term the tooling needs fixing, though.

# Exercises

## 1. Running Code with `uv run`
- **Reproduction:** Explain why `uv run` is preferred over executing `python` directly from the `.venv/bin` directory.
- **Reproduction:** What does the `--` (double-dash) separator do in a `uv run` command? 
- **Application:** You have a project with an entrypoint named `fetch-data`. Write the command to run this entrypoint using Python 3.12, ensuring that any parameters like `--limit 10` are passed to the application and not to `uv`. 

## 2. Editable Installs
- **Reproduction:** What is an "editable install," and what is the main benefit for a developer? 
- **Reproduction:** How does `uv` handle an editable install for a project using a `src` layout? 
- **Application:** You suspect that your project is missing a file that should be included in the final package, but the app works fine in your development environment. How can you use `uv run` to verify if the app works without the "link" to your source directory?

## 3. Tool Execution and `uvx`
- **Reproduction:** What is the difference between `uv run pytest` and `uvx pytest`? 
- **Reproduction:** Where does `uvx` store the environments it creates for one-off tool runs? 
- **Application:** You want to quickly format a single Python file named `utils.py` using `ruff`, but `ruff` is not a dependency in your current project. Write the command to do this without adding `ruff` to your `pyproject.toml`. 

## 4. Multiple Environments
- **Reproduction:** How can you test your project against Python 3.12 and 3.13 sequentially using only `uv run`? 
- **Reproduction:** What environment variable can you use to tell `uv` to use a non-default virtual environment directory (e.g., `.venv-test`)? 
- **Application:** Create a `Makefile` entry that runs `pytest` specifically using a virtual environment directory named `.venv-py312` and Python version 3.12. 
- **Transfer:** Your team is developing a library that must support Python 3.10 through 3.13. Explain how you would set up a local testing strategy that allows you to switch between these versions instantly without the overhead of `uv` recreating the main `.venv` every time, and how you would automate this for the team.

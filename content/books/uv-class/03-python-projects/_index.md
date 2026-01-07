---
title: "A sample project and a walkthrough"
weight: 30
date: 2026-01-04T00:00:00Z
description: |
  A walkthrough of simple `uv` usage with a primitive project to show what things look like
  during project creation, inside the dev project, and during build, install and version
  changes.

---

{{% details title="**Summary**" open=true %}}
A walkthrough of simple `uv` usage with a primitive project to show what things look like
during project creation, inside the dev project, and during build, install and version
changes.
{{% /details %}}

This walkthrough uses a tiny command line app as the learning vehicle.
The goal is not the weather-app.
Instead we use it as a vehicle to show how to set up a `uv` based project and how to run it.

# Create a project

```bash
mkdir berlin-weather
cd berlin-weather
uv init --no-managed-python --python 3.10  --package
```

For example:

```bash
$ mkdir berlin-weather
$ cd berlin-weather
$ uv init --no-managed-python --python 3.10  --package
Initialized project `berlin-weather`
$ tree
.
|-- README.md
|-- pyproject.toml
`-- src
    `-- berlin_weather
        `-- __init__.py

3 directories, 3 files
$ cat src/berlin_weather/__init__.py
def main() -> None:
    print("Hello from berlin-weather!")

$ ls -ld .??*
drwxr-xr-x  9 kris  wheel  288 Jan  4 17:25 .git
-rw-r--r--  1 kris  wheel  109 Jan  4 17:21 .gitignore
-rw-r--r--  1 kris  wheel    5 Jan  4 17:21 .python-version

$ cat .gitignore
# Python-generated files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info

# Virtual environments
.venv
$ cat .python-version
3.10

$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore
	.python-version
	README.md
	pyproject.toml
	src/

nothing added to commit but untracked files present (use "git add" to track)
```

We are running the command `uv init` with the option `--package` in an empty directory.
It creates a project named after the directory,
autoconverting `-` in the package-name to `_` to accommodate python naming rules.

We also specified
that we do not want `uv` to download a version of Python for us (we could also use `--managed-python` instead,
which is usually preferable).
And we specified a relatively old, custom version of Python, `3.10`.

Three files were created: 
- `README.md` (empty), 
- `pyproject.toml` (basic content) 
- and module: `src/berlin_weather/__init__.py` with a hello-world code-fragment.

The `uv init` also initialized an empty git repo for us, and a basic `.gitignore`.

The file `.python-version` describes the minimum python-version to be used.

## Testing the execution

We can run this with any allowed python version.
Since we said `3.10`, we could run this with `3.10` or newer.
Let's try `3.13` instead:

```bash
$ uv run --no-managed-python --python 3.13 python -c "from berlin_weather import main; main()"
Using CPython 3.13.11 interpreter at: /opt/homebrew/opt/python@3.13/bin/python3.13
Creating virtual environment at: .venv
      Built berlin-weather @ file:///private/tmp/berlin-weather
Installed 1 package in 2ms
Hello from berlin-weather!
```

We observe:

- `uv` casually created a `.venv` directory and installed all dependencies in it (one, the Python itself so far).
- We ran the code from the package.

## We use `uv init --package`

We could have simply used `uv init` to create a flat structure.

We prefer `--package`:
- It makes the project installable and buildable from day one.
- It defaults to a `src` layout, which avoids accidental imports from the working directory.
- It gives us modules and the opportunity to define entry points
  that can be called from loader scripts under `[project.scripts]` and
  that will become command line binaries in the `.venv` path.

So instead of "a folder of python files" we have a project with proper modules and dependencies.

Other `uv init` modes exist:
Flat layout ("folder of python files") and script mode (metadata in the header comments of a single python file),
but we don't go there.
Use `uv help init` for the details.

We get `src/berlin_weather/__init__.py`.
The directory name is the module name, and module names (identifiers) in Python can't contain minus-signs.
Instead the minus is converted to an underbar (`_`).
To make the directory an importable Python module, the file `__init__.py` must exist.
It may be empty.

In our case, it contains a callable `main()` function as a placeholder for testing.

## A basic `pyproject.toml`

We also get a basic `pyproject.toml`:

```toml
$ cat pyproject.toml
[project]
name = "berlin-weather"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Kristian Koehntopp", email = "kris-git@koehntopp.de" }
]
requires-python = ">=3.10"
dependencies = []

[project.scripts]
berlin-weather = "berlin_weather:main"

[build-system]
requires = ["uv_build>=0.9.21,<0.10.0"]
build-backend = "uv_build"
```

`uv init` filled in some basic metadata, a version number, a placeholder description and a pointer to the `README.md` file.
It lists the author metadata, finding it by reading the `git` configuration for the current user.

The list of project dependencies is empty.
The Python version requirement is from the `uv init` commandline, where we specified `--python 3.10`.

`uv init` also defined the default build-system (the built-in `uv` build system) to build packages.
Other build backends are possible, and we can change that.
For pure Python projects that is not necessary,
but if we want to build something that extends CPYthon in other languages such as Rust or C, we have to.

The dummy `main()` function in our package is listed as an entrypoint, which means that a build,
and install or an `uv run` will find a script `berlin-weather` in the path tha calls `main()
` in the berlin_weather` module.

## Running the application through the entrypoint script 

```
$ uv run berlin-weather
Using CPython 3.10.19
Creating virtual environment at: .venv
      Built berlin-weather @ file:///private/tmp/berlin-weather
Installed 1 package in 2ms
Hello from berlin-weather!

$ uv run --python 3.14 berlin-weather
Using CPython 3.14.2
Removed virtual environment at: .venv
Creating virtual environment at: .venv
Installed 1 package in 2ms
Hello from berlin-weather!
```

We have been calling the application through that entrypoint script:
`uv run berlin-weather`.

To make things more interesting we specify a Python version,
and observe how `uv` casually recreates the `.venv` as needed.
Our application is run twice, once with Python 3.10, the other time with 3.14.

# Adding some code

To turn this into a proper application with an external dependency,
we write a small piece of code
that loads the current weather for Berlin from BrightSky using the `httpx` module from PyPi.
`httpx` is a successor library to `request`, and can make REST calls or other HTTP requests.

The code looks like this:

```python
from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import date
from typing import Any

import httpx

BRIGHTSKY_WEATHER_URL = "https://api.brightsky.dev/weather"


@dataclass(frozen=True)
class WeatherNow:
    time: str
    temperature_c: float | None
    wind_speed_ms: float | None


def _pick_latest_weather(payload: dict[str, Any]) -> WeatherNow:
    weather = payload.get("weather") or []
    if not weather:
        raise RuntimeError("No weather data returned.")
    latest = weather[-1]
    return WeatherNow(
        time=str(latest.get("timestamp") or ""),
        temperature_c=latest.get("temperature"),
        wind_speed_ms=latest.get("wind_speed"),
    )


def _fetch_weather(lat: float, lon: float, day: date) -> WeatherNow:
    timeout = httpx.Timeout(10.0, connect=5.0)
    headers = {"User-Agent": "berlin-weather-training/1.0", "Accept": "application/json"}
    params = {"lat": lat, "lon": lon, "date": day.isoformat()}

    with httpx.Client(timeout=timeout, headers=headers, follow_redirects=True) as client:
        resp = client.get(BRIGHTSKY_WEATHER_URL, params=params)
        resp.raise_for_status()
        payload: dict[str, Any] = resp.json()
    return _pick_latest_weather(payload)


def main() -> int:
    berlin_lat = 52.52000
    berlin_lon = 13.40500
    today = date.today()

    try:
        now = _fetch_weather(berlin_lat, berlin_lon, today)
    except (httpx.HTTPError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    t = "?" if now.temperature_c is None else f"{now.temperature_c:.1f} C"
    w = "?" if now.wind_speed_ms is None else f"{now.wind_speed_ms:.1f} m/s"
    print(f"Berlin. {now.time}. {t}. Wind {w}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The module calls `main()` and returns any error, if there is one.

The `main()` function defines the geocoordinates for Berlin and the current date.
It then tries to call `_fetch_weather()` with these data.
If that succeeds, the location, time, temperature and wind speed are being printed.

`_fetch_weather() does a call to the `BRIGHTSKY_WEATHER_URL` with several request parameters,
and a defined timeout.
If there is a result, we parse it with `_pick_latest_weather()`.

`_pick_latest_weather()` takes the last field from the result,
which is the latest (current) weather.
It selects the data we want into a WeatherNow() dataclass and returns this.
This allows us to retrieve this information in an ordered and structured way.

## Adding a dependency with `uv add`

The important piece of this code it that it makes use of `httpx` to make the call,
which is not a library from stdlib.
It is an external, installable dependency.

We declare this dependency with `uv add httpx`.
This modifies `pyproject.toml` and then re-generates `uv.lock`.

```toml
$ cat pyproject.toml
[project]
name = "berlin-weather"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Kristian Koehntopp", email = "kris-git@koehntopp.de" }
]
requires-python = ">=3.10"
dependencies = [
    "httpx>=0.28.1",
]

[project.scripts]
berlin-weather = "berlin_weather.cli:main"

[build-system]
requires = ["uv_build>=0.9.21,<0.10.0"]
build-backend = "uv_build"
```

The `dependencies`-array is no longer empty.
It now contains a version spec of `httpx>=0.28.1`.
This is the current version of `httpx` at the moment we define this dependency.

We also manually changed the entrypoint to `berlin_weather.cli:main` (the function
`main()` in `src/berlin_weather/cli.py`).

## Running the script

We can run the script with different Python versions:

```
$ uv run --python 3.14 -- berlin-weather
Using CPython 3.14.2
Removed virtual environment at: .venv
Creating virtual environment at: .venv
Installed 7 packages in 4ms
Berlin. 2026-01-05T00:00:00+00:00. -1.3 C. Wind 13.0 m/s.

$ uv run --python 3.10 -- berlin-weather
Using CPython 3.10.19
Removed virtual environment at: .venv
Creating virtual environment at: .venv
Installed 9 packages in 5ms
Berlin. 2026-01-05T00:00:00+00:00. -1.3 C. Wind 13.0 m/s.
```

We observe how the `.venv` is recreated with different versions of Python.
We also observe how the number of packages installed is different.

## The `uv.lock` file

Whenever we change the dependencies of a script,
when we run `uv.lock` and in a few other situations the `uv.lock` file is recreated.
It contains the actual dependencies of our script – the ones we specified, and the transitive, implied dependencies,
taking different Python versions into account.

The precise source files, checksums and other details are recorded.

When an `uv.lock` file exists, exactly the versions in the `uv.lock` file are being installed,
guaranteeing the same versions of everything everywhere.

```toml
$ head uv.lock
version = 1
revision = 3
requires-python = ">=3.10"

[[package]]
name = "anyio"
version = "4.12.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
{ name = "exceptiongroup", marker = "python_full_version < '3.11'" },
{ name = "idna" },
{ name = "typing-extensions", marker = "python_full_version < '3.13'" },
]
sdist = { url = "https://files.pythonhosted.org/packages/16/ce/8a777047513153587
e5434fd752e89334ac33e379aa3497db860eeb60377/anyio-4.12.0.tar.gz", hash = "sha256
:73c693b567b0c55130c104d0b43a9baf3aa6a31fc6110116509f27bf75e21ec0", size = 22826
6, upload-time = "2025-11-28T23:37:38.911Z" }
wheels = [
{ url = "https://files.pythonhosted.org/packages/7f/9c/36c5c37947ebfb8c7f22e
0eb6e4d188ee2d53aa3880f3f2744fb894f0cb1/anyio-4.12.0-py3-none-any.whl", hash = "
sha256:dad2376a628f98eeca4881fc56cd06affd18f659b17a747d3ff0307ced94b1bb", size =
113362, upload-time = "2025-11-28T23:36:57.897Z" },
]

[[package]]
name = "berlin-weather"
...
```

The `uv.lock` file has a header that declares the `uv.lock` file version,
and the Python version requirement.

It then has a number of `[[package]]` entries (in toml, a `[]` is a table, an object,
and `[[]]` means to append to the table, here the table `package`).

We see the entry for the package `anyio`, which is required by `httpx`,
and the beginnning of the entry for the `berlin-weather` module itself.

We record the exact `version`, the `source` registry where we found the package,
the list of `dependencies` added by this module, the `sdist` url and checksum and other metadata,
and the `wheels` metadata, again with download url and checksum.
This nails down the version installed, and with the checksum ensures that it is really the exact same file.

The `anyio` dependency is interesting, because it has transitive dependencies, and two of them are conditional:
If we are below 3.11, we also need `exceptiongroup`, and if we are below 3.13, we need `typing-extensions` as well.
This explains the different number of packages, depending on Python version.

## Check in the `uv.lock` file

In order to ensure all environments are using the exact same packages, we put the `uv.lock` file under source control.

```bash
$ git add uv.lock
kris$ git commit -m 'dependency update'
[main (root-commit) 60e4d5e] dependency update
 1 file changed, 104 insertions(+)
 create mode 100644 uv.lock

```

# Building, Installing and Versioning

## Entrypoint

We changed the entrypoint to

```toml
[project.scripts]
berlin-weather = "berlin_weather.cli:main"
```

That is, the script `berlin-weather` is created and will now call `src/berlin_weather/cli.py`,
and specifically the `main()` function in there.

We can check:

```bash
$ ls -l .venv/bin/berlin-weather
-rwxr-xr-x  1 kris  wheel  328 Jan  4 22:38 .venv/bin/berlin-weather
$ cat .venv/bin/berlin-weather
#!/private/tmp/berlin-weather/.venv/bin/python
# -*- coding: utf-8 -*-
import sys
from berlin_weather.cli import main
if __name__ == "__main__":
    if sys.argv[0].endswith("-script.pyw"):
        sys.argv[0] = sys.argv[0][:-11]
    elif sys.argv[0].endswith(".exe"):
        sys.argv[0] = sys.argv[0][:-4]
    sys.exit(main())

```

The script is small Python script, running with the interpreter from the `.venv` created by `uv`.
It imports the entrypoint function from the entrypoint module,
and then calls it.

To be able to use entrypoint scripts we need to write our code as an importable module,
which is what the `--package` in `uv init --package` ensures.

## Build system and build

Our `pyproject.toml` also contains a build system:

```toml
[build-system]
requires = ["uv_build>=0.9.16,<0.10.0"]
build-backend = "uv_build"
```

This enables us to do

```
$ uv build
Building source distribution (uv build backend)...
Building wheel from source distribution (uv build backend)...
Successfully built dist/berlin_weather-0.1.0.tar.gz
Successfully built dist/berlin_weather-0.1.0-py3-none-any.whl
```

We get a `.whl`, a Python wheel (a built and installable "binary", specific to a Python Version, an ABI and a platform).
Our wheel is pure python, hence the ABI and playform are "none" and "any", respectively.
But for a CPython extension it may as well be "cp310-cp37-manylinux" (CPython 3.10,
a specific variant of the CPython 3.7 ABI and diverse Linux platforms).

The `.tar.gz` is a source distribution, enabling to build the wheel locally yourself.

## Installing

We can install the `berlin-weather` project with `uv install .` (install from the local directory).

```
$ uv tool install .
Resolved 7 packages in 27ms
Built berlin-weather @ file:///private/tmp/berlin-weather
Prepared 1 package in 4ms
Installed 7 packages in 4ms
+ anyio==4.12.0
+ berlin-weather==0.1.0 (from file:///private/tmp/berlin-weather)
+ certifi==2026.1.4
+ h11==0.16.0
+ httpcore==1.0.9
+ httpx==0.28.1
+ idna==3.11
  Installed 1 executable: berlin-weather

$ which berlin-weather
  /Users/kris/.local/bin/berlin-weather

$ uv tool uninstall berlin-weather
  Uninstalled 1 executable: berlin-weather
```

This installed the package with all dependencies in `~/.local`, including the entrypoint script,
which ends up in `~/.local/bin`, which should be in our `$PATH`.

We can uninstall all this with `uv tool uninstall berlin-weather`.

## Versioning

Our `pyproject.toml` mentions a version number:

```toml
$ cat pyproject.toml
[project]
name = "berlin-weather"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Kristian Koehntopp", email = "kris-git@koehntopp.de" }
]
requires-python = ">=3.10"
dependencies = [
    "httpx>=0.28.1",
]

[project.scripts]
berlin-weather = "berlin_weather.cli:main"

[build-system]
requires = ["uv_build>=0.9.21,<0.10.0"]
build-backend = "uv_build"
```

Here, the version is 0.1.0:

```toml
version = "0.1.0"
```

A new version of the tool `berlin-weather` will only be installed when the version number changes.

We can bump the version number of our project easily with `uv version`:

```bash
$ grep version pyproject.toml
version = "0.1.0"
$ uv version --bump minor
Resolved 9 packages in 26ms
      Built berlin-weather @ file:///private/tmp/berlin-weather
Prepared 1 package in 3ms
Uninstalled 1 package in 0.94ms
Installed 1 package in 2ms
 - berlin-weather==0.1.0 (from file:///private/tmp/berlin-weather)
 + berlin-weather==0.2.0 (from file:///private/tmp/berlin-weather)
berlin-weather 0.1.0 => 0.2.0
$ grep version pyproject.toml
version = "0.2.0"
```

And when we install this,
we can see how the isolated environment maintained by the `uv tool install` function gets changed:

```bash
$ uv tool install .
Resolved 7 packages in 2ms
      Built berlin-weather @ file:///private/tmp/berlin-weather
Prepared 1 package in 4ms
Uninstalled 1 package in 0.92ms
Installed 1 package in 2ms
 - berlin-weather==0.1.0 (from file:///private/tmp/berlin-weather)
 + berlin-weather==0.2.0 (from file:///private/tmp/berlin-weather)
Installed 1 executable: berlin-weather
```

and

```bash
$ ls -l ~/.local/share/uv/tools/berlin-weather/lib/python3.14/site-packages/
total 24
-rw-r--r--   1 kris  staff    18 Jan  4 23:03 _virtualenv.pth
-rw-r--r--   1 kris  staff  4342 Jan  4 23:03 _virtualenv.py
drwxr-xr-x  15 kris  staff   480 Jan  4 23:03 anyio
drwxr-xr-x  10 kris  staff   320 Jan  4 23:03 anyio-4.12.0.dist-info
drwxr-xr-x   4 kris  staff   128 Jan  4 23:06 berlin_weather
drwxr-xr-x  11 kris  staff   352 Jan  4 23:06 berlin_weather-0.2.0.dist-info
drwxr-xr-x   7 kris  staff   224 Jan  4 23:03 certifi
drwxr-xr-x   9 kris  staff   288 Jan  4 23:03 certifi-2026.1.4.dist-info
drwxr-xr-x  14 kris  staff   448 Jan  4 23:03 h11
drwxr-xr-x   9 kris  staff   288 Jan  4 23:03 h11-0.16.0.dist-info
drwxr-xr-x  14 kris  staff   448 Jan  4 23:03 httpcore
drwxr-xr-x   8 kris  staff   256 Jan  4 23:03 httpcore-1.0.9.dist-info
drwxr-xr-x  21 kris  staff   672 Jan  4 23:03 httpx
drwxr-xr-x   9 kris  staff   288 Jan  4 23:03 httpx-0.28.1.dist-info
drwxr-xr-x  11 kris  staff   352 Jan  4 23:03 idna
drwxr-xr-x   8 kris  staff   256 Jan  4 23:03 idna-3.11.dist-info
```

That is, for each installed tool, uv maintains an isolated venv for production in
`~/.local/share/uv/tools/berlin-weather`.
In this particular venv, the version of `berlin_weather` has now been changed to `0.2.0`.

# Adding dev and test dependencies

Our new code not only has a runtime dependency on `httpx`,
but we also want to use `ruff` for source code formatting (replacing `black`), and for linting (replacing `pylint`).
We still use `mypy` for type checking, because `ty` is not yet production quality.
These are `dev`-Dependencies, with `dev` being a dependency group.

We also want to use `pytest` for testing, and put that in either the `dev` dependency group,
or into a special `test` dependency group.
The latter allows the installation of only `pytest` in CI, while the full set of `dev` is not needed for CI.

We can add arbitrary dependency groups.

```bash
$ uv add --group test pytest
Resolved 16 packages in 63ms
      Built berlin-weather @ file:///private/tmp/berlin-weather
Prepared 2 packages in 16ms
Uninstalled 1 package in 0.94ms
Installed 7 packages in 13ms
 ~ berlin-weather==0.2.0 (from file:///private/tmp/berlin-weather)
 + iniconfig==2.3.0
 + packaging==25.0
 + pluggy==1.6.0
 + pygments==2.19.2
 + pytest==9.0.2
 + tomli==2.3.0

$ uv add --dev mypy ruff
Resolved 21 packages in 54ms
      Built berlin-weather @ file:///private/tmp/berlin-weather
Prepared 3 packages in 336ms
Uninstalled 1 package in 0.67ms
Installed 6 packages in 11ms
 ~ berlin-weather==0.2.0 (from file:///private/tmp/berlin-weather)
 + librt==0.7.7
 + mypy==1.19.1
 + mypy-extensions==1.1.0
 + pathspec==0.12.1
 + ruff==0.14.10
```

We add `pytest` to the group `test`.
We add `mypy` and `ruff` to the group `dev`.

A group is always specified as `--group <name>`.
The group `dev` is special, we can address it as `--group dev`, but also as `--dev`.

Our `pyproject.toml` now grew a new table `[dependency-groups]` with subtables for each group:

```toml
 cat pyproject.toml
[project]
name = "berlin-weather"
version = "0.2.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Kristian Koehntopp", email = "kris-git@koehntopp.de" }
]
requires-python = ">=3.10"
dependencies = [
    "httpx>=0.28.1",
]

[project.scripts]
berlin-weather = "berlin_weather.cli:main"

[build-system]
requires = ["uv_build>=0.9.21,<0.10.0"]
build-backend = "uv_build"

[dependency-groups]
dev = [
    "mypy>=1.19.1",
    "ruff>=0.14.10",
]
test = [
    "pytest>=9.0.2",
]
```

Resolution (the creation of the `uv.lock` file) will always take all dependencies in all groups into account,
even if we unselect certain dependency groups.
This is to ensure package versions stay stable and do not change just because we deselect testing or something.
If we didn't do that, we'd have code that may work, but only when `test` is installed,
because that selects a non-broken version of some package somewhere.

We can use `uv sync` to install no, some or all dependency groups:

```bash
$ uv sync --no-group test --no-dev
Resolved 21 packages in 7ms
Audited 9 packages in 0.53ms
```

We deselect the group `test`, and the group `dev`. We could have written `-no-group dev`, but for dev there is also special syntax.

```bash
$ uv sync --no-group test --dev
Resolved 21 packages in 6ms
Installed 6 packages in 17ms
 + librt==0.7.7
 + mypy==1.19.1
 + mypy-extensions==1.1.0
 + pathspec==0.12.1
 + ruff==0.14.10
 + tomli==2.3.0
```

We select the `dev` dependencies, but not the `test` dependencies.


```bash
$ uv sync --all-groups
Resolved 21 packages in 6ms
Installed 5 packages in 8ms
 + iniconfig==2.3.0
 + packaging==25.0
 + pluggy==1.6.0
 + pygments==2.19.2
 + pytest==9.0.2
```

We install all dependencies from all groups.

To run tools on our code, we need to run them **in** the environment,
so `uv run pytest`, `uv run mypy src` and `uv run ruff format src`, `uv run ruff checks --fix`.

```bash
$ uv run ruff format src
1 file reformatted, 1 file left unchanged
$ uv run ruff check --fix
All checks passed!
```

# What we get

In this walkthrough, we:
- Initialized a new Python project using `uv init --package`, establishing a robust `src` layout and an installable structure from the start.
- Developed a functional command-line application that fetches weather data from an external API (`BrightSky`) using `httpx`.
- Managed dependencies by adding `httpx` and observed how `uv` automatically handles transitive dependencies and environment markers in `uv.lock`.
- Demonstrated the flexibility of `uv` by running our application across multiple Python versions (3.10 and 3.14) with automatic virtual environment management.
- Built the project into a distributable wheel and source distribution using `uv build`.
- Installed and uninstalled the application as a standalone system tool using `uv tool install`.
- Automated version management with `uv version --bump`.
- Organized development and testing workflows by adding `dev` and `test` dependency groups for tools like `ruff`, `mypy`, and `pytest`.

Ultimately, we get a professional, reproducible, and easily distributable Python project, all managed through a single, unified tool: `uv`.

# Exercises

## 1. Project Scaffolding (Reproduction)
Why does this walkthrough recommend using `uv init --package` instead of a simple `uv init`?
List at least three benefits mentioned in the text.

## 2. Entrypoints and Scripts (Reproduction)
In `pyproject.toml`, what is the purpose of the `[project.scripts]` section? 
Explain what `berlin-weather = "berlin_weather.cli:main"` tells `uv` to do during installation.

## 3. Probing the Environment (Application)
Follow the walkthrough to create the `berlin-weather` project and add `httpx`.
Then, run the app with two different Python versions (e.g., 3.10 and 3.13) using `uv run --python <version>`. 
Observe the output of `uv` carefully. Why does `uv` say "Removed virtual environment" and "Creating virtual environment" when you switch versions?

## 4. Versioning and Tool Installation (Application)
Install your `berlin-weather` project as a tool using `uv tool install .`. 
Verify where the executable is placed using `which berlin-weather`.
Now, use `uv version --bump patch` to change the version, and run `uv tool install .` again.
Observe the output: how does `uv` handle the transition from the old version to the new one in the tool environment?
Go into the `.local` directory, find the `berlin-weather` application in the path – what does it look like?
The application runs from an isolated environment, a virtual environment in `.local/share/uv/tools/berlin-weather`.
Explore this environment.

## 5. Transitive Dependencies (Transfer)
Open the `uv.lock` file generated after adding `httpx`.
Find the `anyio` package entry.
Note the `dependencies` list for `anyio`.
Explain why a project running on Python 3.10 might have more packages installed in its `.venv`
than the same project running on Python 3.14,
based on the `marker` fields in `uv.lock`.

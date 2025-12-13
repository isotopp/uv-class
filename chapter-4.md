# Creating a project

## Our project was a `--package`

```bash
$ uv init --package berlin-weather
$ cd berlin-weather
$ uv sync
$ git init
```

We get a `pyproject.toml`,
an empty module `src/berlin_weather` (note the name change to match python naming requirements),
an empty `README.md`, and a hidden `.venv`.
Depending on the `uv` version, there is also already a starter script `.venv/bin/berlin-weather` (linking to keks:main).

``` 
berlin-weather/
    .python-version
    .venv/
        bin/
            python
            berlin-weather   # optional
    pyproject.toml
    README.md
    src/
        berlin_weather/
            __init__.py
    uv.lock
```

Each piece has a jobs:

- `.python-version`, a Python version requirement for `pyenv` or `uv`.
- `.venv` is the isolated environment, created and maintained by `uv sync`.
- `pyproject.toml` is the contract, with the description of what the intended environment should look like,
  open version ranges according to Python version specs.
- `README.md` is for humans.
- `src/berlin_weather` is a module, because it is a directory that contains an `__init__.py` 
  (that is what makes a dir a module).
- `uv.lock` is the actual installed files and versions, including transitive dependencies.
- We need to add a `cli.py`, and change the entrypoint in the `pyproject.toml`, then run `uv sync` to rebuild the `.venv`.

## `pyproject.toml`

- Project identity, contact, description
- Dependencies to run.
- Optional (later) dev dependencies.
- Entrypoint (forcing script creation)

It replaces `setup.py`, `setup.cfg`, `requirements.txt` and it's 1000 children.

`setup.py` and Setuptools is a way to write a Python program (the `setup.py`) to use a library (setuptools)
to install a program and drive a build.
It is hard to control and to maintain, and a security nightmare.

`setup.cfg` was a failed attempt to replace that.

Standard `pyproject.toml` as created (we edited the script section, and added the https dependency):

```
[project]
name = "berlin-weather"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Kristian Koehntopp", email = "kris-git@koehntopp.de" }
]
requires-python = ">=3.14"
dependencies = [
    "httpx>=0.28.1",
]

[project.scripts]
berlin-weather = "berlin_weather.cli:main"

[build-system]
requires = ["uv_build>=0.9.16,<0.10.0"]
build-backend = "uv_build"
```

We still need to edit the description, check the version and then we are good.

- `[project]`, core metadata block
- `dependencies = [ ]` or `[project.dependencies]`, install-time dependencies.
- `[project.scripts]`, starter script generation to call Python entrypoints.
- `[build-system]` declares the build system we use, explicitly.

## About `toml`

```toml
[project]
dependencies = [ "httpx>=0.28.1", ]
```
and
```toml
[project.dependencies]
  "httpx>=0.28.1"
```

are semantically the same.

TOML is a bit like YAML, but uses tables (arrays) with names (keys). These can be written as list form or table form.

The format for the full `pyproject.toml` was at first defined in [PEP-621](https://peps.python.org/pep-0621/),
and is now maintained at [`pyproject.toml` spec])https://packaging.python.org/en/latest/specifications/pyproject-toml/#pyproject-toml-spec).

- `[section]` defines a table,
- `key = value`,
- strings use quotes,
- lists use square brackets,
- trailing commas are legal, and encouraged,
- inline tables (dicts) use `{ }`.

```toml
authors = [
    { name = "Kristian Koehntopp", email = "kris-git@koehntopp.de" }
]
```

The key `authors` contains a list with a table (dict) of author names, each having the keys `name` and `email`.
We see an inline list and an inline table. 

## Project name

- lower-case, hyphenated name that speaks to the purpose.
- `uv` turns the module name automatically into underbarred version,
- avoid Python reserved words,

Main repo name (`berlin-weather`), CLI name (`berlin-weather`) and module name (`src/berlin_weather`) match.

## Old mess

Old style Python uses requirements files:

```bash
$ pip install -r requirements.txt
```

This also resolves transitive dependencies (not listed in the requirements).
You could freeze this as

```bash
$ pip freeze -r requirements.txt > requirements-frozen.txt
```

This would create a `requirements-frozen.txt` with sections for the intended requirements, and the transitive requirements,
and with explicit versions:

```
$ pip3 freeze -r requirements.txt > requirements-frozen.txt
$ cat requirements-frozen.txt
httpx==0.28.1
## The following requirements were added by pip freeze:
anyio==4.12.0
certifi==2025.11.12
h11==0.16.0
httpcore==1.0.9
idna==3.11
```

All of these are build dependencies, required to run the deliverable,
but not dev dependencies, require to run the programming cycle.

You'd often have a `requirements-dev.txt`, too, containing things such as `pyflake`, `pytest`, `mypy`, `black` and `pre-commit`.
`pyproject.toml` fixes that, and provides one file to specifify build and dev dependencies in a single file.

Tools such as `poetry` adopted `pyproject.toml`, and also write their own `poetry.lock` file, with checksums.

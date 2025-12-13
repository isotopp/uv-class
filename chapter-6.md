# Running code and scripts

## `uv run`

`uv run` executes a thing inside the projects managed environment.

For example

```
$ uv run berlin-weather
Bright Sky - Berlin - 2025-12-13
time: 2025-12-14T00:00:00+00:00
temperature: 5.7 C
precipitation: 0.0 mm
wind speed: 13.0 m/s
```

and

```
kk:berlin-weather kris$ uv run python3
Python 3.14.2 (main, Dec  5 2025, 16:49:16) [Clang 17.0.0 (clang-1700.4.4.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> sys.path
['', 
'/opt/homebrew/Cellar/python@3.14/3.14.2/Frameworks/Python.framework/Versions/3.14/lib/python314.zip', 
...
'/Users/kris/Source/uv-class/berlin-weather/.venv/lib/python3.14/site-packages', 
'/Users/kris/Source/uv-class/berlin-weather/src']
>>> sys.version
'3.14.2 (main, Dec  5 2025, 16:49:16) [Clang 17.0.0 (clang-1700.4.4.1)]'
```

Using `uv run` gives you

- the correct Python version
- all declared dependencies installed
- in the locked versions.
- The environment is created and updated as needed.

It still is a `venv`:

```
kk:berlin-weather kris$ .venv/bin/berlin-weather
Bright Sky - Berlin - 2025-12-13
time: 2025-12-14T00:00:00+00:00
temperature: 5.7 C
precipitation: 0.0 mm
wind speed: 13.0 m/s
```

but when working on the project, use `uv run` so that changes are being picked up and the environment is validated.
Do not run the `venv`, let `uv run` run the venv for you.

You can (and should) `uv run` 
- any console script from the `pyproject.toml`
- project `python`
- any executable installed into the `dev` or other environments

## Entry points

In `berlin-weather`, we defined an entrypoint in `pyproject.toml`:

```
[project.scripts]
berlin-weather = "berlin_weather.cli:main"
```

This will

- create an executable command `.venv/bin/berlin-weather` (left hand side)
- that calls `main()` in `src/berlin_weather/cli.py`

Note the `sys.path` from above, last component: `/Users/kris/Source/uv-class/berlin-weather/src`.
That means the `import berlin_weather.cli` will match the file `src/berlin_weather/cli.py`, and load that.

## Running Python files

You can also

```
uv run python main.py
uv run python src/berlin_weather/cli.py
```

That works, but has downsides:
- import paths depend on the working directory
- We leak project structure details
- Refactoring breaks things

Instead, we would rather update the RHS of the `berlin-weather` declaration and hide changes and paths.

You can use this to test things, or debug your env.
You must do that in user or production facing tools.
Declare scripts, `uv run the-script`.

## Scripts vs. Modules

Python supports running modules with `-m`:

```
uv run python -m berlin_weather.cli
```

This executes the module as part of the package, not a raw file.

- Imports resolve the same way as in production
- `sys.path` is set and used correctly.
- Package layout is respected
- Still leaks structure.

## Reproducible execution

Reproducible exection means:

- same command,
- same code,
- same dependency versions,
- same behavior

`uv run` enforces that by using `uv.lock`, creating environments, preventing drift.

## Shebangs

```
#! /usr/bin/env python
```

`#!` - This is a script, here is the interpreter: `#! /bin/bash`.

The `env` command searches the path and gives you the path for the command named as an arg.
`#! /usr/bin/env python` - the first Python in the path, "the python".

## Advanced `uv run`

`uv run` has a large number of parameters.
You can have more than one `uv run` environment.
This is useful for testing.

Read `uv help run`.
Read [Testing different Python versions with uv with-editable and uv-test](https://til.simonwillison.net/python/uv-tests).

- `uv run --python 3.14 ...` - run with a specific Python version.
- `uv run --managed-python --python 3.12 ...` - download that Python version and use it.

This is subject to version restrictions declared in the `pyproject.toml`.
If you force `>= 3.14`, it won't allow testing with 3.12.

`uv run --isolated berlin-weather` - run in a new temporary venv built just for this run.
The directory is somewhere in `uv`'s cache directory, i.e. `~/.cache/uv`, `~/Library/Caches/uv` or `%LOCALAPPDATA%\uv\cache\`.
The directory created will be set up from scratch, include only what was declared and no accidental extras,
and will be cleaned up.
This ensures that the execution environment is pristine.

`uv run --python 3.13 --isolated --with-editable '.[test]' pytest` - this will install something
into the isolated environment before using it.
Here what is installed is `.`, the current project, and the `test` dependency group (likely `pytest` and friends).
So we get the current project plus what `pytest` needs, and then run the command, `pytest`.
`-with-editable` will install the project in editable mode:

- code is imported from the working tree
- changes to source files are immediately visible
- no wheel is built (we did not explain wheels yet)

This is what we need for running tests, linters and type checkers.

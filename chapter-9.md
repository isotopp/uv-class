# Tooling Integrations

We already know `uv run`.
We now want to install tools as dev dependencies, and run them on our codebase in a consistent way.

## Installing dev dependencies

```
uv add --group dev ruff mypy
uv add --group test pytest
```

Use a group for every purpose.
Dependencies are always evaluated on the full set, even if only a partial subset of groups is installed.

The tools are part of the project, with locked versions.
They are not part of the machine.
This makes the environment transportable, even into CI containers.

## Ruff

`ruff` is a companion projec to `uv`, a linter and formatter.
It replaces `pylint` and `black`, and is much faster.

Running checks (linting):

```
uv run ruff check --fix src tests
```

The option `--fix` fixes fixable problems, and complains only about those that require human decisions.

Running formatting:

```
uv run ruff format src tests
```

This is the style we use.
You do not have to like it, the others also don't like it.
But we all use the same style, this one.

Type checking with `mypy`:

```
uv run mypy src
```

We do not type-check tests.
This is often too painful.

Run the test suite:

```
uv run pytest
```

Or also declare `pytest-xdist` as a test dependency and use `uv run pytest -n auto` for parallel testing.

Running the tools with `uv run` ensures the right versions are being used, the tools are present (and up to date),
and the environments are clean. Do not use `mypy src`, run `uv run mypy src`.

## Automation

Only this approach works reliably with automation,
for example in CI containers in your gitlab or github.

- CI runs the same commands in the same version.
- Pre-Commit Hooks all use the same commands.
- All devs use the same commands, IDEs use the same commands.

`uv` ensures through `pyproject.toml` and lockfile that these versions are also locked in for tooling.
The dev and test environment is part of the project, not part of your box.

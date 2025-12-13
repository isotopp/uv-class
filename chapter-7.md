# Lockfiles and reproducibility

## What a lockfile is

The lockfile records the exact dependency state of a project at a point in time.
For uv, that is the `uv.lock` file.

Never edit it.

## What the `uv.lock` file looks like

The file declares it's own internal version,
the python version and a sequence of `[[package]]` sections:

```
version = 1
revision = 3
requires-python = ">=3.14"

[[package]]
name = "anyio"
version = "4.12.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "idna" },
]
sdist = { url = ".../anyio-4.12.0.tar.gz", 
          hash = "sha256:73c...ec0", 
          size = 228266, 
          upload-time = "2025-11-28T23:37:38.911Z" }
wheels = [
    { url = ".../anyio-4.12.0-py3-none-any.whl", 
      hash = "sha256:da...1bb", 
      size = 113362, 
      upload-time = "2025-11-28T23:36:57.897Z" },
]
...
```

When we go through it, we find

- every direct and transitive dependency,
- exact versions, with checksums, and dates, and download locations,
- which means a fully pre-resolved dependency tree to exact file content (checksum),
- guarateeing reproducible install.

This is fundamentally more secure and specific than a `requirements.txt` (which is more like a simpler `pyproject.toml`),
and also better than a `requirements-frozen.txt` (`pip freeze -r requirements.txt > ...-frozen.txt`),
which contains exact versions, but no locations or checksums.

`uv sync` reads the `uv.lock` file, and creates a new environment that matches the `uv.lock` spec exactly.
`uv run` implies an `uv sync` for the target directory specified (`.venv` by default).

## Sharing

To share a project for installation, we hand over the git repo.
This should include both, the intended versions (`pyproject.toml`) and the actual versions (`uv.lock`).

With that, any developer (or a CI test matrix) can `uv sync` and `uv run berlin-weather`,
and get the same versions and the same behavior with th same bugs.

## Upgrading

`uv lock` recomputes the dependency graph and creates a new `uv.lock` file from `pyproject.toml`.
This upgrades versions of dependencies.

After running `uv.lock`, you must

- check in the new `uv.lock`
- run a full CI test to verify passing tests after dependency upgrades

Often you will want to adjust the version constraints in the `pyproject.toml`,
and then `uv lock` to regenerate the lockfile and re-run a full test suite.

## The lockfile must be checked in

"But it's machine generated!"
That is true, but it is the foundation for all other installs including the CI test install.
So despite the fact that this is a machine generated file, it's the foundation of all other installs,
to prevent "works on my machine" syndrome.

Always check in the `uv.lock` you have tested with.
It is the exact state of the codebase you ran (`--isolated`).

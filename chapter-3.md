
# Installation and Maintenance

## Installing `uv`

See the [installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

- Curlbash: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- PIP: `pip install uv`
- Homebrew: `brew install uv`
- Scoop: `scoop install main/uv`
- Winget: `winget install --id=astral-sh.uv -e`
- Cargo: `cargo install --locked uv`

## Updating

`uv self version`
`uv self update`

## Autocomplete

`.bashrc` line:

```bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
```

or whatever you need for your shell.

## Maintenance

`uv` maintains a download cache:

```bash
uv cache clean
```

Python Versions in `uv python dir`, other downloads in `uv tool dir`.

# Project

## A weather API call

`https://api.brightsky.dev/weather`, no API key

```bash
cd Source
uv init --package berlin-weather
cd berlin-weather
```

We run `init` with `--package`.
This will also create a `src/` module directory inside the project directory.

We also get a `.python-vversion`, a `pyproject.toml, and an empty `README.md`.

The `src` directory contains a basic module `berlin-weather`.
To make this directory a module, a file `__init__.py` must exist.

## Adding dependencies

```bash
$ cp pyproject.toml pyproject.toml-old # save a copy to compare
$ uv add httpx
$ diff -u pyproject.toml-old pyproject.toml
--- pyproject.toml-old  2025-12-12 13:16:02
+++ pyproject.toml      2025-12-12 13:16:19
@@ -7,7 +7,9 @@
     { name = "Kristian Koehntopp", email = "kris-git@koehntopp.de" }
 ]
 requires-python = ">=3.14"
-dependencies = []
+dependencies = [
+    "httpx>=0.28.1",
+]
 
 [project.scripts]
 berlin-weather = "berlin_weather:main"
$ rm pyproject.toml
```

## Setting up a start script

Edit the `pyproject.toml` or add the section for a starter script:

```toml
[project.scripts]
berlin-weather = "berlin_weather.cli:main"
```

This will make `src/berlin-weather/cli.py` the command line starter module,
and call `main()` in there.
It is best practice to put Python command line wrappers for modules into
`src/module-name/cli.py` and add all callable functions in there.
Then add a `main()` with command line parsing using Argparse or Click.

Run

```bash
$ uv sync
```

This will create `.venv` in your project, install all dependencies, and also create the start script.
Check `.venv/bin/berlin-weather`.

It does not work, yet: There is no `cli.py:main()`.

## Write the code

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
    precipitation_mm: float | None
    wind_speed_ms: float | None


def _pick_latest_weather(payload: dict[str, Any]) -> WeatherNow:
    weather = payload.get("weather")
    if not isinstance(weather, list) or not weather:
        raise ValueError("Bright Sky returned no weather records for this date.")

    last = weather[-1]
    if not isinstance(last, dict):
        raise ValueError("Bright Sky payload format was unexpected.")

    return WeatherNow(
        time=str(last.get("timestamp", "")),
        temperature_c=(last.get("temperature") if isinstance(last.get("temperature"), (int, float)) else None),
        precipitation_mm=(last.get("precipitation") if isinstance(last.get("precipitation"), (int, float)) else None),
        wind_speed_ms=(last.get("wind_speed") if isinstance(last.get("wind_speed"), (int, float)) else None),
    )


def fetch_weather_for(
    *,
    lat: float,
    lon: float,
    day: date,
    client: httpx.Client,
) -> WeatherNow:
    params = {
        "lat": f"{lat:.5f}",
        "lon": f"{lon:.5f}",
        "date": day.isoformat(),
    }

    r = client.get(BRIGHTSKY_WEATHER_URL, params=params)
    r.raise_for_status()
    payload = r.json()
    if not isinstance(payload, dict):
        raise ValueError("Bright Sky payload was not a JSON object.")
    return _pick_latest_weather(payload)


def main() -> int:
    berlin_lat = 52.52000
    berlin_lon = 13.40500
    today = date.today()

    timeout = httpx.Timeout(10.0, connect=5.0)
    headers = {
        "User-Agent": "berlin-weather-training/1.0",
        "Accept": "application/json",
    }

    try:
        with httpx.Client(timeout=timeout, headers=headers, follow_redirects=True) as client:
            w = fetch_weather_for(lat=berlin_lat, lon=berlin_lon, day=today, client=client)

        print(f"Bright Sky - Berlin - {today.isoformat()}")
        print(f"time: {w.time}")
        print(f"temperature: {w.temperature_c} C")
        print(f"precipitation: {w.precipitation_mm} mm")
        print(f"wind speed: {w.wind_speed_ms} m/s")
        return 0

    except httpx.HTTPError as e:
        print(f"Network error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
```

The script uses `https` to a public endpoint,
with proper timeouts, making a simple REST call.
On error, it will dump a traceback.
We take no parameters, coordinates are hardcoded for Berlin.

## Run the code

```bash
$ uv run --managed-python berlin-weather
Using CPython 3.14.2
Creating virtual environment at: .venv
      Built berlin-weather @ file:///Users/kris/Source/uv-class/berlin-weather
Installed 7 packages in 4ms
Bright Sky - Berlin - 2025-12-12
time: 2025-12-13T00:00:00+00:00
temperature: 2.0 C
precipitation: 0.0 mm
wind speed: 9.3 m/s
```

## What happens under the hood:

1. `uv` downloads a matching Python version (here: 3.14.2).
   See the downloads with `ls -l $(uv python dir)`.
2. `uv` creates a `.venv` directory from scratch using cached dependencies.
3. `uv` runs the Python with the binary.

You will find that there is now an `uv.lock` file that captures the exact versions of the exact modules you used.
This includes checksums.

The `uv.lock` should be checked in.
It is important for reproducible builds.

You can update the dependencies and re-build the `uv.lock` with the `uv lock` command,
and then check in the new `uv.lock` file.

So

1. `pyproject.toml` is the intent ("we depend on `httpx>=0.28.1` ").
2. `uv.lock`, we download this particular version plus all the implied dependencies, with checksums and urls.

Always run the program with `uv run ...`.

You can also run `.../berlin-weather/.venv/bin/berlin-weather`.

```bash
cat .venv/bin/berlin-weather
```
```python
#!/Users/kris/Source/uv-class/berlin-weather/.venv/bin/python
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

The hashbang will start the Python from the `.venv`, which activates the venv,
and then load code from the venv root, using the venv's `PYTHONPATH`.

This does use the existing environment for better or worse, not updating or rebuilding the environment. Using `uv run ...` is much cleaner, it will always ensure a clean environment.

We used `uv init --package` with a starter script, from the beginning, because that is always how we structure Python projects:
- re-usable modules that can be included from other python
- A `cli.py` for the arg parsing,
- a `main()` as the argparse entrypoint, branching out to all the other entrypoints as subcommands.

We then add a `project.scripts` scripts table to the toml, to have our tooling manage the entrypoint.

## Exercises

1. `rm uv.lock`, then `uv run` the project.
1. `rm -rf .venv`, then `uv run` the project.
2. `rm -rf .venv`, `uv cache clean --force`, then `uv run ...`
3. `rm -rf .venv`, `uv cache clean --force`, `rm -rf $(uv python dir)`, then `uv run ...`

5. Take an old project with an old `uv.lock` file, `cp uv.lock uv.lock-old`. Run `uv lock`. Diff.

# Junie Guidelines for berlin-weather

## Project Overview
`berlin-weather` is a pure Python example project used in the `uv-class` course. It demonstrates basic `uv` usage with a single external dependency.

## Technical Stack
- **Language**: Python (>= 3.14)
- **Dependency Manager**: `uv`
- **Main Dependencies**: `httpx`
- **Build System**: `uv_build`

## Project Structure
- `src/berlin_weather/`: Main package source code.
  - `cli.py`: Command-line interface entry point.
- `pyproject.toml`: Project metadata and dependencies.
- `uv.lock`: Locked dependency versions.

## Development Rules
- Use `uv` for all dependency management and execution.
- Maintain simplicity, as this is a teaching example.
- Follow PEP 8 coding standards.

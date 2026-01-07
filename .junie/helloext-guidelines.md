# Junie Guidelines for helloext

## Project Overview
`helloext` is a C-written "hello world" like extension for Python. It demonstrates a more complex project that integrates `uv` with `scikit-build-core` and CMake.

## Technical Stack
- **Language**: Python (>= 3.12) and C
- **Dependency Manager**: `uv`
- **Build System**: `scikit-build-core` with CMake
- **Testing**: `pytest`

## Project Structure
- `src/helloext/`:
  - `_hello.c`: The C source for the Python extension.
  - `__init__.py`: Python package initialization.
- `tests/`: Automated tests using `pytest`.
- `CMakeLists.txt`: CMake configuration for building the C extension.
- `pyproject.toml`: Project metadata and build system configuration.
- `uv.lock`: Locked dependency versions.

## Development Rules
- Use `uv` for dependency management.
- When modifying C code, ensure it remains compatible with CPython's C API.
- Maintain the `scikit-build-core` configuration in `pyproject.toml`.
- Run tests using `uv run pytest` to verify changes.

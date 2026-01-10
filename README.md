# uv-class: Modern Python Project Management

A comprehensive guide and tutorial for `uv`, the extremely fast Python package manager. This repository contains the source for the [uv-class book](https://isotopp.github.io/uv-class/) and several example projects used throughout the course.

---

## What it is
This is a teaching resource focused on `uv`. It covers everything from basic installation to advanced Docker multi-stage builds and C extension management.

The repository includes:
- **The Book**: A Hugo-based static site containing all chapters.
- **Example Projects**:
  - `examples/berlin-weather`: A pure Python project demonstrating standard `uv` workflows.
  - `examples/helloext`: A C-based Python extension using `scikit-build-core`.
  - `examples/whoami`: Demonstrations of PEP 723 inline script metadata.

## Who it is for
- **Students**: Learning how to manage Python projects effectively.
- **Instructors**: Looking for a structured curriculum to teach modern Python tooling.
- **Developers**: Migrating from `pip`, `venv`, or `Poetry` to `uv`.

## Installation

### 1. Clone the repository
This project uses Git submodules for the Hugo theme. You must clone recursively:

```bash
git clone --recurse-submodules https://github.com/isotopp/uv-class.git
cd uv-class
```

### 2. Requirements
- **uv**: [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
- **Hugo**: [Install Hugo](https://gohugo.io/installation/) (extended version required)

## Quick Start

### View the Book
To run the Hugo development server and view the book locally:

```bash
hugo server -D
```
The site will be available at `http://localhost:1313/`.

### Explore the Examples
Navigate to any example project in `/examples` and use `uv` to run it:

```bash
cd examples/berlin-weather
uv run berlin-weather
```

## Project Structure
- `content/books/uv-class/`: The source chapters for the book.
- `themes/hugo-book/`: The Hugo theme (git submodule).
- `examples/`: Standalone Python projects used for demonstrations.
- `AGENTS.md`: Policy for AI-assisted contributions.

## Contributing

Contributions are welcome! Please see [AGENTS.md](AGENTS.md) for guidelines on how to contribute, especially if you are using AI tools.

## Support
If you find a bug or have a suggestion, please [open a GitHub issue](https://github.com/isotopp/uv-class/issues).

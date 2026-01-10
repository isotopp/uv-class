# AGENTS.md

This document defines the guidelines and rules for contributing to the `uv-class` project.
It is intended for both human developers and AI agents.

## Shared Guidelines (Humans & Agents)

### Project Layout
- The site uses Hugo with the `hugo-book` theme (see `hugo.toml`).
- Theme docs: [hugo-book demo](https://hugo-book-demo.netlify.app/docs)
- Theme installation: `/themes/hugo-book` is a **git submodule**. Do not modify it.
- Book content: Located under `content/books/uv-class/`. Each chapter is a directory with an `_index.md`.
- Legacy content: Top-level `chapter-*.md` files are legacy. Do not update them unless specifically requested.
- Example projects: Located in `/examples/`. Use these for code snippets and exercises.

### Content Conventions
- **Front Matter**: Every chapter (`_index.md`) must have `title`, `weight`, `date`, and a concise `description`.
- **Chapter Structure**:
    - Start with a `{{% details title="**Summary**" open=true %}}` block.
    - Use `## Topics` for a high-level overview of the chapter.
    - Follow the Diátaxis framework (Tutorials, How-to, Reference, Explanation).
    - End with an `## Exercises` section.
- **Exercises**: Use Bloom's Taxonomy to categorize exercises (Reproduction, Application, Transfer).
- **Shortcodes**: Prefer existing Hugo Book shortcodes:
    - `hint`: `{{< hint info >}}...{{< /hint >}}` (info, warning, danger).
    - `details`: `{{% details title="..." %}}...{{% /details %}}` (collapsible section).
    - `steps`: `{{< steps >}}...{{< /steps >}}` (numbered procedures).
    - `tabs`: `{{< tabs >}}{{< tab "Name" >}}...{{< /tab >}}{{< /tabs >}}` (switchable panels).
    - `mermaid`: `{{< mermaid >}}...{{< /mermaid >}}` (diagrams).
    - `button`: `{{< button href="..." >}}...{{< /button >}}` (CTA).
    - `columns`: `{{< columns >}}...{{< /columns >}}` (layout).

### Validation
- Before submitting, always run `hugo -D -E -F`.
- The site must build without any errors or warnings.

---

## Agent-Specific Rules

This section contains rules and technical tips specifically for AI agents (like GitHub Copilot, Junie, etc.).

### Interacting with `uv`
- **Help Output**: `uv` uses a pager (like `less`) by default when run in a terminal.
To read the full help output in a non-interactive session, you **must** pipe it to `cat`:
  ```bash
  uv help <command> | cat
  # or
  uv <command> --help | cat
  ```
- **Lockfiles**: Always ensure that `uv.lock` is updated and committed if you change dependencies in `pyproject.toml`.
- **Python Discovery**: `uv` follows a discovery hierarchy. Check `.python-version` and `pyproject.toml` to understand the project's requirements.

### Content Generation
- **Consistency**: Match the tone and style of existing chapters.
- **References**: When referencing example projects, ensure the paths are correct (e.g., `examples/berlin-weather`).
- **Shortcode Escaping**: Be careful with Hugo shortcode syntax in markdown blocks; ensure they are rendered correctly or escaped if they are meant to be shown as code.

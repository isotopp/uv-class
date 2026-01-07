# Junie Guidelines for uv-class

## Project Overview
This is a Hugo-based project for the "uv-class" book, using the `hugo-book` theme. It also contains example Python projects used in the course.

## Project Structure
- **Hugo Site**: The main content and configuration for the book.
- **Example Projects**:
  - `/berlin-weather`: A pure Python project with a single dependency (`httpx`), used to demonstrate basic `uv` usage.
  - `/helloext`: A C-written "hello world" like extension to Python, demonstrating a more complex project that uses `uv` with `scikit-build-core`.

## Content Structure
- **Main Book Content**: Located in `content/books/uv-class/`. Each chapter is a directory containing an `_index.md` file.
- **Legacy Content**: `chapter-*.md` files in the root are legacy. **Do not update them** unless explicitly requested.
- **Theme**: The theme is located in `themes/hugo-book`. It is a git submodule and should not be modified.
- **Configuration**: Main Hugo config is `hugo.toml`.

## Content Conventions
- **Front Matter**: Use `title`, `weight`, `date`, and `description` in `_index.md` files.
- **Shortcodes**: Prefer using `hugo-book` shortcodes:
  - `{{< hint info >}}...{{< /hint >}}` for callouts (info, warning, danger).
  - `{{% details title="..." %}}...{{% /details %}}` for collapsible sections.
  - `{{< steps >}}...{{< /steps >}}` for procedures.
  - `{{< tabs >}}...{{< /tabs >}}` for multi-platform instructions.
  - `{{< button href="..." >}}...{{< /button >}}` for CTA.
  - `{{< columns >}}...{{< /columns >}}` for layout.
  - `{{< mermaid >}}...{{< /mermaid >}}` for diagrams.

## Validation
- Always run `hugo -D -E -F` to ensure the site builds without errors or warnings before submitting changes.

## Development Rules
- Follow existing patterns in `content/books/uv-class/` for new content.
- Ensure all links are relative or correctly point to the site structure.

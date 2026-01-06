# AGENTS.md

## Project layout

- The site uses Hugo with the `hugo-book` theme (see `hugo.toml`).
- Theme docs: https://hugo-book-demo.netlify.app/docs
- Theme installation: `/themes/hugo-book` (git submodule, do not change).
- The book section is configured with `BookSection = "books"`.
- Legacy content lives in top-level `chapter-*.md` files. Do not update those unless asked.
- New or updated content goes under `content/books/uv-class/`, with each chapter as a section folder containing `_index.md`.

## Content conventions

- Use front matter fields like `title`, `weight`, `date`, and `description` as in existing chapters.
- Prefer Hugo Book shortcodes already used in the content (for example, `{{% details %}}`).

## Validation

- Ensure `hugo -D -E -F` runs without errors or warnings.

## Addendum: hugo-book shortcodes (useful for technical docs)

- `button`: styled link button for strong calls-to-action like "Start here" or "Download".
  Example: `{{<button href="/books/uv-class/">}}Start reading{{</button>}}`
- `columns`: arrange short, parallel content in 2–3 columns for comparisons or short lists.
  Example: `{{< columns >}}- Column 1\n- Column 2{{< /columns >}}`
- `details`: collapsible section for summaries or optional deep dives (already used in chapters).
  Example: `{{% details title="Summary" open=true %}}...{{% /details %}}`
- `hints`: callout blocks for notes, tips, warnings, and cautions.
  Example: `{{< hint info >}}Remember to run `uv sync`.{{< /hint >}}`
- `steps`: numbered step list for procedures and lab instructions.
  Example: `{{< steps >}}1. Install uv\n2. Run `uv init`{{< /steps >}}`
- `tabs`: switchable panels for OS- or tool-specific instructions.
  Example: `{{< tabs >}}{{< tab "macOS" >}}...{{< /tab >}}{{< tab "Windows" >}}...{{< /tab >}}{{< /tabs >}}`
- `mermaid`: diagrams for workflows or architecture.
  Example: `{{< mermaid >}}flowchart TD\n  A-->B{{< /mermaid >}}`
- `katex`: math typesetting (only if needed for formulas).
  Example: `{{< katex >}}\pi(x){{< /katex >}}`

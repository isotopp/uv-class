from pathlib import Path
import argparse
import os
import re
import shutil


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text

    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text

    raw_meta = parts[0][4:]
    body = parts[1]
    meta: dict[str, str] = {}
    for line in raw_meta.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return meta, body


def rewrite_links(body: str, source_dir: Path, output_path: Path) -> str:
    def repl(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2)
        if target.startswith(("http://", "https://", "#", "mailto:")):
            return match.group(0)

        target_path = (source_dir / target).resolve()
        relpath = Path(os.path.relpath(target_path, output_path.parent))
        return f"![{label}]({relpath.as_posix()})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, body)


def chapter_files(book_dir: Path) -> list[Path]:
    chapters = sorted(book_dir.glob("*/_index.md"))
    return [book_dir / "_index.md", *chapters]


def copy_source_tree(source_dir: Path, build_dir: Path) -> None:
    if build_dir.exists():
        shutil.rmtree(build_dir)
    shutil.copytree(source_dir, build_dir)


def render_book(source_dir: Path, output_path: Path) -> None:
    sections: list[str] = []

    for index, path in enumerate(chapter_files(source_dir)):
        text = path.read_text(encoding="utf-8")
        meta, body = split_front_matter(text)
        body = body.replace(
            '{{% details title="**Summary**" open=true %}}', "## Summary"
        )
        body = body.replace("{{% /details %}}", "")
        body = re.sub(r"^\[//\]:\s+#\s+\(.*\)$", "", body, flags=re.MULTILINE)
        body = rewrite_links(body, path.parent, output_path)

        title = meta.get("title", path.parent.name.replace("-", " ").title())
        heading = f"# {title}"
        if index == 0:
            sections.append(f"{heading}\n\n{body.strip()}\n")
        else:
            sections.append(f"\n{heading}\n\n{body.strip()}\n")

    output_path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--build-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    source_dir = Path(args.source)
    build_dir = Path(args.build_dir)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    copy_source_tree(source_dir, build_dir)
    render_book(build_dir, output_path)


if __name__ == "__main__":
    main()

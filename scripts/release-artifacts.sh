#!/bin/sh

set -eu

TAG="${1:-}"
TITLE="${2:-$TAG}"

if [ -z "$TAG" ]; then
  printf 'Usage: %s <tag> [title]\n' "$0" >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  printf 'Error: gh is required.\n' >&2
  exit 1
fi

if ! command -v zip >/dev/null 2>&1; then
  printf 'Error: zip is required.\n' >&2
  exit 1
fi

make clean
make all

ZIP_PATH="out/uv-class-${TAG}.zip"
rm -f "$ZIP_PATH"
zip -j "$ZIP_PATH" \
  out/uv-class.epub \
  out/uv-class.docx \
  out/uv-class.odt \
  out/uv-class.html

gh release create "$TAG" \
  out/uv-class.epub \
  out/uv-class.docx \
  out/uv-class.odt \
  out/uv-class.html \
  "$ZIP_PATH" \
  --title "$TITLE" \
  --generate-notes

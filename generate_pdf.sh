#!/bin/bash
set -euo pipefail

# Thin wrapper: build_cv.py renders the Markdown files AND invokes Pandoc for
# every CV (academic EN/ES plus one industry CV per language for each profile
# in src/profiles/). To add a CV, drop a new file in src/profiles/ -- no script
# changes needed.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

command -v python3 >/dev/null 2>&1 || { echo "Missing required command: python3" >&2; exit 1; }
command -v pandoc  >/dev/null 2>&1 || { echo "Missing required command: pandoc"  >&2; exit 1; }

echo "Construyendo CVs (Markdown + PDF) desde cv_data.yaml y src/profiles/..."
python3 src/build_cv.py

echo "PDFs generados exitosamente en la carpeta 'output/'."

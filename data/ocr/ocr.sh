#!/usr/bin/env bash
#
# Applies OCR with ocrmypdf to every "raw_" PDF under data/regions/,
# writing the result to the same path without the "raw_" prefix.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CONFIG="${SCRIPT_DIR}/tesseract_config.cfg"
REGIONS_DIR="${SCRIPT_DIR}/../regions"

# ocrmypdf already parallelizes pages internally, so keep the default
# modest; override with e.g. JOBS=4 ./ocr.sh
JOBS="${JOBS:-2}"
FAIL_LOG="$(mktemp)"
trap 'rm -f "$FAIL_LOG"' EXIT

ocr_one() {
    local src="$1"
    local dest="${src/raw_/}"
    echo "OCR: $src -> $dest"
    if ! ocrmypdf -l spa --tesseract-pagesegmode 11 --output-type pdf --color-conversion-strategy Gray --continue-on-soft-render-error --tesseract-config "$CONFIG" "$src" "$dest"; then
        echo "ERROR: ocrmypdf failed for $src" >&2
        echo "$src" >> "$FAIL_LOG"
        return 1
    fi
}

shopt -s nullglob
for src in "$REGIONS_DIR"/*/*/raw_*.pdf; do
    # keep at most $JOBS ocrmypdf processes running at once
    while (( $(jobs -rp | wc -l) >= JOBS )); do
        wait -n || true
    done
    ocr_one "$src" &
done
wait || true

if (( $(wc -l < "$FAIL_LOG") > 0 )); then
    echo >&2
    echo "=== $(wc -l < "$FAIL_LOG") file(s) failed OCR ===" >&2
    while IFS= read -r f; do
        echo "  $f" >&2
    done < "$FAIL_LOG"
    exit 1
fi

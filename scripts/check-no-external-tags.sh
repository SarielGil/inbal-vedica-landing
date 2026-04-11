#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -f "assets/analytics-loader.js" ]]; then
  echo "ERROR: Missing required file assets/analytics-loader.js"
  exit 1
fi

ALL_HTML_FILES=()
while IFS= read -r file; do
  ALL_HTML_FILES+=("$file")
done < <(find . -type f -name "*.html" -not -path "./node_modules/*" -not -path "./.git/*" | sort)

ROOT_HTML_FILES=()
while IFS= read -r file; do
  ROOT_HTML_FILES+=("$file")
done < <(find . -maxdepth 1 -type f -name "*.html" | sort)

if ((${#ALL_HTML_FILES[@]} == 0)); then
  echo "ERROR: No HTML files found."
  exit 1
fi

declare -a BANNED_PATTERNS=(
  "fonts\\.googleapis\\.com"
  "fonts\\.gstatic\\.com"
  "googletagmanager\\.com/gtag/js"
  "googletagmanager\\.com/gtm\\.js"
  "googletagmanager\\.com/ns\\.html\\?id=GTM-"
  "google-analytics\\.com/g/collect"
)

FAILED=0

for pattern in "${BANNED_PATTERNS[@]}"; do
  MATCHES="$(grep -nE -- "$pattern" "${ALL_HTML_FILES[@]}" || true)"
  if [[ -n "$MATCHES" ]]; then
    echo "ERROR: Found banned external dependency pattern: $pattern"
    echo "$MATCHES"
    FAILED=1
  fi
done

for file in "${ROOT_HTML_FILES[@]}"; do
  if ! grep -q "assets/analytics-loader.js" "$file"; then
    echo "ERROR: Missing analytics loader include in $file"
    FAILED=1
  fi
done

if ((FAILED)); then
  echo "Guard failed."
  exit 1
fi

echo "Guard passed: no banned external tags found and analytics loader is included in all root HTML pages."

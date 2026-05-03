#!/usr/bin/env bash
set -euo pipefail

if [[ $# -eq 0 ]]; then
  mapfile -t files < <(find . -maxdepth 1 -name "*.html" | sort)
else
  files=("$@")
fi

if [[ ${#files[@]} -eq 0 ]]; then
  echo "No HTML files found."
  exit 0
fi

printf "UI audit for %d file(s)\n\n" "${#files[@]}"

for file in "${files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "[SKIP] $file (not found)"
    continue
  fi

  echo "=== $file ==="

  if rg -q '<meta[^>]+name="viewport"' "$file"; then
    echo "[OK] viewport meta"
  else
    echo "[WARN] missing viewport meta"
  fi

  if rg -q '<meta[^>]+name="description"' "$file"; then
    echo "[OK] meta description"
  else
    echo "[WARN] missing meta description"
  fi

  if rg -q '<link[^>]+rel="canonical"' "$file"; then
    echo "[OK] canonical"
  else
    echo "[WARN] missing canonical"
  fi

  h1_count=$( (rg -o '<h1\b' "$file" || true) | wc -l | tr -d ' ' )
  if [[ "$h1_count" == "1" ]]; then
    echo "[OK] exactly one h1"
  else
    echo "[WARN] h1 count is $h1_count"
  fi

  missing_alt_count=$( (rg -o '<img\b(?![^>]*\balt=)[^>]*>' -P "$file" || true) | wc -l | tr -d ' ' )
  if [[ "$missing_alt_count" == "0" ]]; then
    echo "[OK] no img tags missing alt"
  else
    echo "[WARN] $missing_alt_count img tag(s) missing alt"
  fi

  weak_blank_count=$( (rg -o '<img\b[^>]*\balt=""[^>]*>' -P "$file" || true) | wc -l | tr -d ' ' )
  if [[ "$weak_blank_count" != "0" ]]; then
    echo "[INFO] $weak_blank_count image(s) with empty alt (verify decorative use)"
  fi

  missing_rel_count=$( (rg -o '<a\b[^>]*target="_blank"(?![^>]*\brel=)[^>]*>' -P "$file" || true) | wc -l | tr -d ' ' )
  if [[ "$missing_rel_count" == "0" ]]; then
    echo "[OK] external target links include rel"
  else
    echo "[WARN] $missing_rel_count target=_blank link(s) missing rel"
  fi

  echo

done

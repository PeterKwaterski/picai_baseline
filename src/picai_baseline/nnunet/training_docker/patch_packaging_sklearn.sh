#!/usr/bin/env bash
# Replace deprecated PyPI package name "sklearn" with "scikit-learn" in packaging metadata only.
set -euo pipefail
ROOT="${1:?usage: patch_packaging_sklearn.sh /path/to/repo}"

find "$ROOT" -type f \( -name setup.py -o -name setup.cfg -o -name requirements.txt -o -name pyproject.toml \) -print0 |
  while IFS= read -r -d '' file; do
    sed -i.bak \
      -e 's/"sklearn"/"scikit-learn"/g' \
      -e "s/'sklearn'/'scikit-learn'/g" \
      -e 's/^sklearn$/scikit-learn/' \
      -e 's/^sklearn /scikit-learn /' \
      "$file"
    rm -f "${file}.bak"
  done

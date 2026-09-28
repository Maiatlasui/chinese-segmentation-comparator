#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="chinese-seg38"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v conda >/dev/null 2>&1; then
  echo "Conda was not found. Complete the setup steps in GITHUB_WORKBOOK.md first."
  exit 1
fi

cd "${PROJECT_DIR}"
exec conda run --no-capture-output --name "${ENV_NAME}" streamlit run app.py


#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="chinese-seg38"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v conda >/dev/null 2>&1; then
  echo "Conda was not found. Install Miniconda or Anaconda, reopen Terminal, and run this script again."
  exit 1
fi

if conda run --name "${ENV_NAME}" python --version >/dev/null 2>&1; then
  echo "Updating the existing ${ENV_NAME} environment..."
  conda env update --name "${ENV_NAME}" --file "${PROJECT_DIR}/environment.yml" --prune
else
  echo "Creating the ${ENV_NAME} environment..."
  conda env create --file "${PROJECT_DIR}/environment.yml"
fi

echo "Installing the main application packages..."
conda run --name "${ENV_NAME}" python -m pip install --upgrade pip
conda run --name "${ENV_NAME}" python -m pip install -r "${PROJECT_DIR}/requirements.txt"

echo "Installing pkuseg with its required legacy build process..."
conda run --name "${ENV_NAME}" python -m pip install Cython==0.29.37
conda run --name "${ENV_NAME}" python -m pip install --no-build-isolation -r "${PROJECT_DIR}/requirements-pkuseg.txt"

echo "Checking the installation..."
conda run --name "${ENV_NAME}" python "${PROJECT_DIR}/scripts/check_install.py"

echo
echo "Setup complete. Start the app with:"
echo "  bash \"${PROJECT_DIR}/scripts/run.sh\""

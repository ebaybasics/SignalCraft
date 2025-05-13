#!/usr/bin/env bash

set -e

PYTHON_VERSION="3.11.9"
VENV_DIR=".venv"

echo "🔍 Checking for pyenv..."
if ! command -v pyenv &> /dev/null; then
  echo "❌ pyenv is not installed."
  echo "👉 Install it from https://github.com/pyenv/pyenv#installation and rerun this script."
  exit 1
fi

echo "✅ pyenv found"

# Install Python if missing
if ! pyenv versions --bare | grep -q "^${PYTHON_VERSION}\$"; then
  echo "📦 Installing Python $PYTHON_VERSION via pyenv..."
  pyenv install $PYTHON_VERSION
else
  echo "✅ Python $PYTHON_VERSION already installed"
fi

# Set local pyenv version
echo "📌 Setting local Python version to $PYTHON_VERSION"
pyenv local $PYTHON_VERSION

# Create virtual environment
echo "🧪 Creating virtual environment in $VENV_DIR"
rm -rf $VENV_DIR
~/.pyenv/versions/$PYTHON_VERSION/bin/python -m venv $VENV_DIR

# Activate environment and install packages
echo "📦 Installing dependencies..."
source $VENV_DIR/bin/activate
pip install --upgrade pip setuptools wheel

# Install required packages
pip install numpy==1.24.4 scipy yfinance pandas_ta

echo "✅ Environment setup complete."

# Freeze requirements for reproducibility
pip freeze > requirements.txt
echo "📌 requirements.txt saved with pinned versions."

echo
echo "👉 To activate your environment:"
echo "   source $VENV_DIR/bin/activate"
echo
echo "🧠 Tip: pyenv will now auto-select Python $PYTHON_VERSION in this folder."

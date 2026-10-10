#!/bin/sh
# Build and upload to PyPI using the token in .pypirc (see .pypirc.example).
set -eu
cd "$(dirname "$0")/.."

uv run pytest -q
rm -rf build dist
uv build
uv tool run twine upload --config-file .pypirc dist/*

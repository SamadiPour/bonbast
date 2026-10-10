#!/bin/sh
# Build the package and install it as a global `bonbast` command with uv.
set -eu
cd "$(dirname "$0")/.."

rm -rf build dist
uv build
uv tool install --force --reinstall dist/bonbast-*.whl

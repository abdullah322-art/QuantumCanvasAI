#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

NAME="qca_bundle_$(date +%Y%m%d_%H%M%S).zip"

zip -r "$NAME" \
  qca \
  requirements.txt \
  README.md \
  .env.example \
  render.yaml \
  Procfile \
  runtime.txt \
  || true

echo "Created $NAME"


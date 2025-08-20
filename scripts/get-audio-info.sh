#!/bin/bash

set -euo pipefail

METADATA_PATH=./downloads/metadata/
METADATA_NAME="media"

yt-dlp --skip-download --quiet --no-warnings \
  --write-info-json --paths "$METADATA_PATH" --output "$METADATA_NAME" "$1"

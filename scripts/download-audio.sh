#!/bin/bash

set -euo pipefail

AUDIO_PATH=./downloads/audio
AUDIO_NAME="audio"
AUDIO_EXT="m4a"

METADATA_PATH=./downloads/metadata
METADATA_NAME="media"

THUMBNAIL_EXT="jpg"

yt-dlp --no-post-overwrites \
  --quiet --no-warnings \
  --paths "${AUDIO_PATH}" --output "${AUDIO_NAME}" \
  --embed-thumbnail --embed-metadata --add-metadata \
  -f "${AUDIO_EXT}/bestaudio/best" -o "${AUDIO_NAME}.${AUDIO_EXT}" "$1"

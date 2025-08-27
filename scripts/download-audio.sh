#!/bin/bash

set -euo pipefail

AUDIO_PATH=./downloads/audio
AUDIO_NAME="audio"
AUDIO_EXT="m4a"

yt-dlp --no-post-overwrites --quiet --no-warnings --paths "${AUDIO_PATH}" --output "${AUDIO_NAME}.${AUDIO_EXT}" --embed-thumbnail --embed-metadata --add-metadata -f "${AUDIO_EXT}/bestaudio/best" "$1"

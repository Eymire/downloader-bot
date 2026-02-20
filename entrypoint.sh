#!/usr/bin/env bash

echo "Clearing yt-dlp cache..."
uv run yt-dlp --rm-cache-dir
echo "Cache cleared!"

exec "$@"

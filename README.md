# Downloader Bot

Telegram bot for downloading short videos from:

- YouTube Shorts
- Instagram Reels
- TikTok

The bot accepts a URL and sends the downloaded video back in chat.

## Features

- `/start` command with usage help
- `/download <url>` command for supported links
- Automatic platform detection (YouTube / Instagram / TikTok)
- Max video duration: **120 seconds**
- Video post-processing with `ffmpeg` for Telegram-friendly playback
- Thumbnail download (with extra thumbnail cropping for Shorts)

## Requirements

- Python `3.13+`
- `uv` package manager
- `ffmpeg` installed in the system
- Telegram bot token from [@BotFather](https://t.me/BotFather)

## Environment Variables

Create a `.env` file in the project root:

```env
APP_TOKEN=your_telegram_bot_token_here
```

The app uses `APP_` prefix and reads `APP_TOKEN`.

## Run Locally

1. Install dependencies:

```bash
uv sync --locked
```

2. Start the bot:

```bash
uv run src/main.py
```

## Run with Docker Compose

Build and run:

```bash
docker compose up --build -d
```

View logs:

```bash
docker compose logs -f app
```

Stop:

```bash
docker compose down
```

## Bot Usage

In Telegram chat with your bot:

1. Send `/start`
2. Send command:

```text
/download https://example.com/video
```

## Supported URL Patterns

- TikTok: `*.tiktok.com`
- YouTube Shorts: `youtube.com/shorts/...` (and YouTube host links)
- Instagram Reels: `instagram.com/reel/...`

Unsupported links return an informative error message.

## Project Structure

```text
src/
	main.py               # Bot entrypoint
	settings.py           # Env-based configuration
	handlers/
		start.py            # /start command
		download.py         # /download command + URL routing
	downloader/
		tiktok.py           # TikTok downloader
		shorts.py           # YouTube Shorts downloader
		reels.py            # Instagram Reels downloader
```

## Notes

- Downloaded files are saved under `videos/`.
- Current cleanup after sending is disabled in code (file deletion lines are commented out).
- On container start, `yt-dlp` cache is cleared by `entrypoint.sh`.

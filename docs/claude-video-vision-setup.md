# Claude Video Vision setup

[Claude Video Vision](https://github.com/jordanrendric/claude-video-vision) is
a Claude Code plugin that lets Claude watch and understand videos. It extracts
frames with ffmpeg and transcribes audio through a backend you choose (Gemini
API, local Whisper, or OpenAI Whisper API). Claude receives the frames as
images plus a timestamped transcript, so it can review ad cuts, product videos,
Reels, TikToks, and YouTube links directly.

## Already configured for this repo

`.claude/settings.json` declares the `claude-video-vision` marketplace and
enables the plugin, so anyone opening this repo in Claude Code is prompted to
trust and install it. The MCP server is fetched from npm via `npx` on first
use, so there is no build step. After approving the prompt and restarting,
run the setup wizard once (see below) to pick an audio backend.

## Manual install (any other project)

1. Open Claude Code.
2. `/plugin marketplace add jordanrendric/claude-video-vision`
3. `/plugin install claude-video-vision@claude-video-vision`
4. Restart Claude Code so the plugin's skill, commands, and MCP server load.
5. Run `/claude-video-vision:setup-video-vision` to configure the backend.

The same steps work from a terminal without the interactive UI:

```sh
claude plugin marketplace add jordanrendric/claude-video-vision
claude plugin install claude-video-vision@claude-video-vision
claude plugin list
```

## Dependencies

The plugin runs a local MCP server and shells out to a few tools:

- **Node.js 20+** for the MCP server (`npx -y claude-video-vision@latest`).
- **ffmpeg** for frame and audio extraction. The setup wizard detects it and
  prints install instructions if it is missing (`brew install ffmpeg` on
  macOS).
- **yt-dlp** only if you want to pass YouTube URLs (`brew install yt-dlp`).
- **One audio backend:**
  - Gemini API: set `GEMINI_API_KEY` (free key from
    [ai.google.dev](https://ai.google.dev/gemini-api/docs/api-key)).
    Recommended; it also picks up non-speech audio events.
  - Local Whisper: `brew install whisper-cpp` (or Python `openai-whisper`).
    Fully offline, models auto-download to `~/.claude-video-vision/models/`.
  - OpenAI: set `OPENAI_API_KEY`. Paid per use.

Settings live in `~/.claude-video-vision/config.json`; the wizard writes them
for you.

## Verifying

`/claude-video-vision:setup-video-vision` should start an interactive wizard
asking which backend to use. Its final step checks ffmpeg, Node, and the
backend and reports anything missing.

Then try it on a real file or link:

```
/claude-video-vision:watch-video path/to/ad-cut.mp4 "does the plant stay consistent between shots?"
/claude-video-vision:watch-video https://www.youtube.com/shorts/... "summarize this"
```

If either command reports unknown, the plugin is installed but the session
predates it. Restart Claude Code and try again.

`claude plugin details claude-video-vision` shows the component inventory.

## What you get

- Commands: `/claude-video-vision:watch-video <path or URL> [question]` and
  `/claude-video-vision:setup-video-vision`.
- Skill: `video-perception`, which triggers automatically when you mention a
  video file (`.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`) or a YouTube URL in
  conversation.
- MCP tools: `video_info`, `video_analyze`, `video_watch`, `video_detail`,
  `video_configure`, and `video_setup`.
- Agent: `frame-describer`, used when `frame_mode` is `descriptions` to turn
  frames into text and save tokens on long videos.

For videos longer than about 30 seconds the skill runs `video_analyze` first
(scene changes, silence, motion) and then extracts frames only where they
matter. Short clips get full-coverage extraction.

## Privacy notes

- With the local Whisper backend nothing leaves the machine.
- With Gemini or OpenAI, extracted audio is sent to that provider under its own
  privacy terms. Video frames are never uploaded by the plugin; Claude sees
  them through the normal Claude Code session.
- The plugin has no telemetry. See its
  [PRIVACY.md](https://github.com/jordanrendric/claude-video-vision/blob/main/PRIVACY.md).

## Removing it

```sh
claude plugin uninstall claude-video-vision
claude plugin marketplace remove claude-video-vision
```

Delete the `claude-video-vision` entries from `.claude/settings.json` to stop
enabling it for this repo. Local config and downloaded Whisper models live in
`~/.claude-video-vision/` and can be deleted separately.

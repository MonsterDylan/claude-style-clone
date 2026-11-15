#!/bin/sh
# Installs the style-clone skill for Claude Code and checks the two tools it needs.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills/style-clone"
mkdir -p "$HOME/.claude/skills"
rm -rf "$DEST.new" && cp -R "$HERE/skills/style-clone" "$DEST.new"
[ -d "$DEST" ] && rm -rf "$DEST.old" && mv "$DEST" "$DEST.old"
mv "$DEST.new" "$DEST" && rm -rf "$DEST.old"
echo "Installed the skill to $DEST"
MISSING=""
for t in python3 ffmpeg ffprobe yt-dlp; do command -v "$t" >/dev/null 2>&1 || MISSING="$MISSING $t"; done
if [ -n "$MISSING" ]; then
  echo "Still needed:$MISSING"
  echo "  macOS:   brew install ffmpeg yt-dlp"
  echo "  Windows: winget install ffmpeg yt-dlp"
  echo "  Linux:   your package manager for ffmpeg, then: pip install yt-dlp"
else
  echo "ffmpeg, yt-dlp and python3 found. You're set."
fi
mkdir -p "$HOME/.config/style-clone"
[ -f "$HOME/.config/style-clone/.env" ] || cp "$HERE/.env.example" "$HOME/.config/style-clone/.env"
echo "Optional keys go in ~/.config/style-clone/.env (see the README). You can skip them."
echo "Now open Claude Code and say: clone the editing style of @somecreator on YouTube"

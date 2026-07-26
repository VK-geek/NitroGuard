#!/bin/bash
# NitroGuard Demo Screen Recorder
# Usage: ./record_demo.sh         — starts recording
#        Ctrl+C to stop

OUTPUT="$HOME/NitroGuard_Demo_$(date +%Y-%m-%d_%H-%M).mp4"

echo "🎬 Recording started → $OUTPUT"
echo "    Arrange your windows: MuJoCo (left) + Web Dashboard (right)"
echo "    Press Ctrl+C to stop recording"
echo ""

ffmpeg \
  -f x11grab \
  -framerate 30 \
  -video_size 2560x1600 \
  -i :0.0 \
  -vf "scale=1920:1200" \
  -c:v libx264 \
  -preset ultrafast \
  -crf 20 \
  -pix_fmt yuv420p \
  "$OUTPUT"

echo ""
echo "✅ Saved to: $OUTPUT"

#!/bin/bash
# Simple startup script for Chatterbox UI
# Just run: ./run.sh

cd "$(dirname "$0")" || exit 1

echo "Starting Chatterbox TTS Server..."
echo ""
echo "The server will start on: http://localhost:5001"
echo ""
echo "To stop the server, press Ctrl+C"
echo ""

uv run python app.py

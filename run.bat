@echo off
REM Simple startup script for Chatterbox UI on Windows
REM Just run: run.bat

echo Starting Chatterbox TTS Server...
echo.
echo The server will start on: http://localhost:5001
echo.
echo To stop the server, press Ctrl+C
echo.

uv run python app.py

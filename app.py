"""Flask backend for the Chatterbox ONNX UI.

Provides endpoints:
  GET  /               -> serve the static index.html
  GET  /source-files   -> JSON list of available .wav files in sourcefiles/
  GET  /scripts        -> current sourcscript.json mapping (debug)
  POST /generate       -> run generate_speech and return the generated file path
"""

import os
import json
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, abort

# Import the generation function and helpers from the UI copy
from chatterbox_turbo_onnx_ui import (
    generate_speech,
    list_source_wav_files,
)

app = Flask(__name__, static_folder=".")


@app.route('/')
def index():
    """Serve the static HTML UI."""
    return send_from_directory(os.path.dirname(__file__), "index.html")


@app.route('/source-files')
def source_files():
    """Return a JSON array of available source wav filenames (without extension)."""
    try:
        wavs = list_source_wav_files()
        print(f"DEBUG: Found WAV files: {wavs}")
        # Strip the .wav extension for UI convenience
        keys = [Path(f).stem for f in wavs]
        print(f"DEBUG: Returning keys: {keys}")
        return jsonify(keys)
    except Exception as e:
        print(f"ERROR in /source-files: {e}")
        return jsonify([]), 500




@app.route('/generate', methods=['POST'])
def generate():
    """Generate speech based on posted JSON parameters.

    Expected JSON payload:
    {
        "text": "...",
        "source_key": "B_MALE1",
        "output_name": "optional.wav",
        "emote": "laugh",
        "model_dtype": "q4",
        "max_new_tokens": 256,
        "repetition_penalty": 1.2,
        "exaggeration": 0.5,
        "cfg_weight": 0.5,
        "apply_watermark": false,
        "new_script": {"key": "NEW_KEY", "transcript": "..."}   # optional
    }
    """
    data = request.get_json(force=True)
    if not data:
        abort(400, description="Invalid JSON payload")

    # Debug: log the received data
    print(f"DEBUG: Received JSON data: {data}")

    # Required fields
    text = data.get("text")
    source_key = data.get("source_key")
    print(f"DEBUG: Extracted text='{text}'")
    print(f"DEBUG: Extracted source_key='{source_key}'")
    if not text or not source_key:
        abort(400, description="'text' and 'source_key' are required fields")

    # Optional fields with defaults
    output_name = data.get("output_name")
    emote = data.get("emote", "laugh")
    model_dtype = data.get("model_dtype", "q4")
    max_new_tokens = int(data.get("max_new_tokens", 256))
    repetition_penalty = float(data.get("repetition_penalty", 1.2))
    exaggeration = float(data.get("exaggeration", 0.5))
    cfg_weight = float(data.get("cfg_weight", 0.5))
    apply_watermark = bool(data.get("apply_watermark", False))

    try:
        out_path = generate_speech(
            text=text,
            source_key=source_key,
            output_name=output_name,
            emote=emote,
            model_dtype=model_dtype,
            max_new_tokens=max_new_tokens,
            repetition_penalty=repetition_penalty,
            exaggeration=exaggeration,
            cfg_weight=cfg_weight,
            apply_watermark=apply_watermark,
        )
    except Exception as exc:
        abort(500, description=str(exc))

    # Return the filename relative to the workspace so the UI can load it
    filename = os.path.basename(out_path)
    return jsonify({"output_file": filename})


# Serve generated wav files from the system temp directory
@app.route('/outputs/<path:filename>')
def serve_output(filename):
    temp_dir = tempfile.gettempdir()
    return send_from_directory(temp_dir, filename)

# ---------------------------------------------------------------------------
# Upload new audio file endpoint (moved above __main__ to ensure registration)
# ---------------------------------------------------------------------------
@app.route('/upload-audio', methods=['GET', 'POST'])
def upload_audio():
    """Handle audio file upload.

    Expected multipart/form-data with field:
        audio_file: the .wav file (minimum 10 seconds)
    Naming convention for the file (without extension) must be:
        <region>_<type>
    where <region> is "B" (British) or "A" (American) and <type> describes the voice
    (e.g., male, female, child, adultold, femaleChild, etc.).
    """
    if request.method == 'GET':
        return jsonify({'status': 'ready for upload'})
    if 'audio_file' not in request.files:
        abort(400, description='Missing audio_file in request')
    audio = request.files['audio_file']

    # Validate filename extension only
    filename = audio.filename
    if not filename.lower().endswith('.wav'):
        abort(400, description='Only .wav files are accepted')
    base_name = os.path.splitext(filename)[0]

    # Ensure file does not already exist
    dest_path = os.path.join(os.path.dirname(__file__), 'sourcefiles', f'{base_name}.wav')
    if os.path.exists(dest_path):
        abort(400, description='File with this name already exists')

    # Save the wav file
    audio.save(dest_path)

    return jsonify({'status': 'ok', 'key': base_name})


def cleanup_generated_files():
    """Delete all previously generated .wav files from the system temp directory on startup.
    
    Keeps source files in the sourcefiles/ directory untouched.
    """
    temp_dir = tempfile.gettempdir()
    
    # List all .wav files in temp directory and delete them
    try:
        for filename in os.listdir(temp_dir):
            if filename.endswith('.wav'):
                filepath = os.path.join(temp_dir, filename)
                # Only delete if it's a file
                if os.path.isfile(filepath):
                    try:
                        os.remove(filepath)
                        print(f"Cleaned up temp: {filename}")
                    except Exception as e:
                        print(f"Error deleting {filename}: {e}")
    except Exception as e:
        print(f"Error accessing temp directory: {e}")
    
    print("Cleanup complete. Temp directory ready.")


if __name__ == '__main__':
    # Clean up previously generated files on startup
    cleanup_generated_files()
    
    # Run on localhost:5001 to avoid port conflict
    app.run(host='0.0.0.0', port=5001, debug=True)

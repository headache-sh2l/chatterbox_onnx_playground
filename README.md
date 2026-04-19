# Chatterbox ONNX TTS UI

A web-based interface for generating speech using Chatterbox Turbo ONNX models.

---

## Quick Start (Easy Setup)

### Prerequisites
- **Python 3.9+** (check by opening Terminal and typing `python3 --version`)
- **uv** package manager (one-time setup)

### Installation (One Time Only)

#### macOS / Linux

1. **Install `uv`**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**:
   ```bash
   cd /path/to/chatterbox_onnx_playground
   uv sync
   ```

#### Windows

1. **Install `uv`**:
   - Download and run: https://astral.sh/uv/install.ps1
   - Or use `pip`:
     ```cmd
     pip install uv
     ```

2. **Install dependencies**:
   - Open Command Prompt or PowerShell
   - Navigate to the project folder:
     ```cmd
     cd C:\path\to\chatterbox_onnx_playground
     ```
   - Run:
     ```cmd
     uv sync
     ```

### Running the Server

#### macOS / Linux
**Option 1: Easy (Recommended)**
```bash
./run.sh
```

**Option 2: Manual**
```bash
uv run python app.py
```

#### Windows
**Option 1: Easy (Recommended)**
Double-click: **`run.bat`**

**Option 2: Manual**
Open Command Prompt and run:
```cmd
uv run python app.py
```

Then open your browser to: **http://localhost:5001**

---

## Testing the UI

1. **Select a voice** from the dropdown (e.g., "B_MALE1")
2. **Enter text** to generate speech for
3. **Choose parameters**:
   - Emotion (laugh, angry, whisper, etc.)
   - Model quality (q4, q8, fp16, fp32)
   - Adjust sliders as needed
4. **Click "Generate"** and wait for the audio file
5. **Upload new voices**: Click "Upload Audio" and select a `.wav` file to add to the voice collection

---

## Stopping the Server

Press **`Ctrl + C`** in the Terminal where the server is running.

---

## Troubleshooting

**"Port 5001 already in use"**
- Another program is using port 5001. Either:
  - Wait a minute and try again
  - Or kill the process: `pkill -f "python app.py"`

**"Module not found" errors**
- Run: `uv sync` to reinstall dependencies

**File upload not working**
- Ensure your `.wav` file is at least a few seconds long
- Check that the file is actually in WAV format

---

## For Non-Technical Users

**You only need to:**

1. Install `uv` once (follow the Installation step above for your OS)
2. Run `uv sync` once in the project folder
3. Then:
   - **Windows**: Double-click `run.bat`
   - **macOS/Linux**: Run `./run.sh`
4. Open your browser to `http://localhost:5001`
5. Press `Ctrl + C` in the terminal to stop the server

That's it! The script handles everything else.

---

## File Structure

```
.
├── run.sh                      # Easy startup script (macOS/Linux)
├── run.bat                     # Easy startup script (Windows)
├── app.py                      # Flask web server
├── index.html                  # Web interface
├── chatterbox_turbo_onnx_ui.py # Speech generation engine
├── sourcefiles/                # Voice files (add your own here)
└── README.md                   # This file
```

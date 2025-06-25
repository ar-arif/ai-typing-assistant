import os
import time
import httpx
import pyperclip
import argparse
from string import Template
from datetime import datetime
from dotenv import load_dotenv
from pynput import keyboard
from pynput.keyboard import Key, Controller

# Load .env
load_dotenv()
CURRENT_DIR = os.getcwd()
OPENROUTER_MODEL = "openai/gpt-4o-mini-2024-07-18"

# Argument parsing
parser = argparse.ArgumentParser(description="AI Typing Assistant using OpenRouter GPT-4o")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
args = parser.parse_args()

# Logger function
def log(msg):
    if args.verbose:
        ts = datetime.now().strftime("[%Y-%m-%d %I:%M:%S %p]")
        print(f"{ts} {msg}")

# Clipboard backend setup
try:
    original_clipboard = pyperclip.paste()
    pyperclip.copy("test")
    if pyperclip.paste() != "test":
        raise pyperclip.PyperclipException()
    pyperclip.copy(original_clipboard)
except pyperclip.PyperclipException:
    if os.system("which xclip > /dev/null") == 0:
        pyperclip.set_clipboard("xclip")
        log("Using clipboard backend: xclip")
    elif os.system("which xsel > /dev/null") == 0:
        pyperclip.set_clipboard("xsel")
        log("Using clipboard backend: xsel")
    else:
        raise SystemExit("Missing clipboard backend. Try: sudo pacman -S xclip")

# OpenRouter config
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise SystemExit("OPENROUTER_API_KEY not set in .env")

controller = Controller()
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

PROMPT_TEMPLATE = Template(
    """Fix all typos and casing and punctuation and grammar in this text, but preserve all new line characters:

$text

Return only the corrected text, don't include a preamble."""
)

def fix_text(text):
    prompt = PROMPT_TEMPLATE.substitute(text=text)
    log(f"Sending text to {OPENROUTER_MODEL}")
    os.system(f"notify-send -i {CURRENT_DIR}/icon.png -t 0 'Ai Typing Assistant' 'Sending text to {OPENROUTER_MODEL}'")
    try:
        start = time.time()
        response = httpx.post(
            OPENROUTER_API_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENROUTER_API_KEY}"
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=15
        )
        response.raise_for_status()
        elapsed = time.time() - start
        log(f"Response from {OPENROUTER_MODEL} in {elapsed:.2f} seconds")
        os.system(f"notify-send -i {CURRENT_DIR}/icon.png -t 0 'Ai Typing Assistant' 'Response from {OPENROUTER_MODEL} in {elapsed:.2f} seconds'")
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log(f"Error from {OPENROUTER_MODEL}: {e}")
        os.system(f"notify-send -i {CURRENT_DIR}/icon.png -t 0 'Ai Typing Assistant' 'Error from {OPENROUTER_MODEL}: {e}'")
        return None

def fix_selection():
    log("Copying selected text")
    with controller.pressed(Key.ctrl):
        controller.tap("c")
    time.sleep(0.1)

    text = pyperclip.paste()
    log(f"Original text: {repr(text)}")

    if not text.strip():
        log("Clipboard is empty or whitespace only")
        return

    fixed = fix_text(text)
    if not fixed:
        log("Failed to get correction")
        return

    pyperclip.copy(fixed)
    time.sleep(0.1)
    log(f"Corrected text: {repr(fixed)}")

    with controller.pressed(Key.ctrl):
        controller.tap("v")
    log("Pasted corrected text")

def on_hotkey():
    log("Hotkey Ctrl+Shift+Q pressed")
    fix_selection()

# Hotkey binding
hotkeys = {"<ctrl>+<shift>+q": on_hotkey}
log("Listening for hotkey: Ctrl+Shift+Q")
with keyboard.GlobalHotKeys(hotkeys) as h:
    h.join()


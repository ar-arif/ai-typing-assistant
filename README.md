# AI Typing Assistant

AI Typing Assistant is a Python tool that uses OpenRouter's GPT-4o (or compatible models) to automatically correct typos, casing, punctuation, and grammar in selected text. It works system-wide by listening for a hotkey (Ctrl+Shift+Q), copying the selected text, sending it to an AI model for correction, and pasting the improved text back.

## Features

- System-wide hotkey (Ctrl+Shift+Q) for instant correction
- Preserves all newlines and formatting
- Uses OpenRouter API for high-quality AI corrections
- Works on Linux (requires clipboard backend: xclip or xsel)

## Requirements

- Python 3.8+
- [OpenRouter API key](https://openrouter.ai/)
- Linux with `xclip` or `xsel` installed for clipboard support

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-typing-assistant.git
   cd ai-typing-assistant
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your OpenRouter API key:
   ```bash
   cp .env.example .env
   # Edit .env and set OPENROUTER_API_KEY
   ```
4. (Optional) Install `xclip` or `xsel` if not already present:
   ```bash
   sudo pacman -S xclip   # Arch Linux
   sudo apt install xclip # Debian/Ubuntu
   ```

## Usage

Run the assistant:

```bash
python main.py
```

- Select any text in any application.
- Press `Ctrl+Shift+Q`.
- The selected text will be corrected and replaced automatically.

### Verbose Logging

Add `-v` or `--verbose` for detailed logs:

```bash
python main.py -v
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

# speech-to-clipboard

A daemon to:

1. Record speech from your computer mic.
2. Send that speech to OpenAI Whisper for transcription.
3. Place that transcript in your clipboard.

Inspired by an iOS shortcut: https://x.com/basileSportif/status/1754262540639441329

## Installation

### Ubuntu

```bash
sudo apt install portaudio19-dev
pip3 install -r requirements.txt
```

### MacOS

```bash
brew install portaudio
pip3 install -r requirements.txt
```

## Usage

1. Add your API key to the file `my_api_key.txt`.
2. Run the script.
3. Hold down F6, in this window or another: key down -> recording start; key up -> send for transcription.
4. Paste transcription result from your clipboard.

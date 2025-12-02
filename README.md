---

# Audio Converter

A Python-based tool to **convert audio and MIDI files** to your preferred format using **FFmpeg** and **FluidSynth**.  
Supports standard audio formats (WAV, MP3, FLAC, etc.) and MIDI rendering to WAV/OGG.



## Features

- Converts audio files to your desired format (`ogg` by default, configurable).
- Renders standard MIDI files to audio using **FluidSynth**.
- Multiprocessing support for **faster batch conversion**.

---

## Requirements

### Software

- [**FFmpeg**](https://www.gyan.dev/ffmpeg/builds/)
* [**FluidSynth**](https://www.fluidsynth.org/)
  - Place the FluidSynth binary in the `bin/` folder.
- **SoundFont file (.sf2)**
    - Place your `.sf2` file in the `soundfont/` folder.
### Python

- Python 3.9+
- Install dependencies:
  
``pip install -r requirements.txt``

---

## Setup

1. Clone the repository:
`git clone https://github.com/ariest1021/audio-converter.git cd audio-converter`
2. Place your **FluidSynth binary** in `bin/` and **SoundFont file** in `soundfont/`.
3. Add your audio or MIDI files to the `audioInput/` folder.
4. Run the converter:
`python main.py`

5. Converted files will appear in the `audioOutput/` folder.
    

---

## Configuration

You can modify these settings in `main.py`:

``audioFormat = "ogg"`` Output audio format
``max_cores = 4`` Max CPU cores for parallel processing

Supported input formats:

- Audio: `.wav`, `.flac`, `.m4a`, `.aac`, `.mp3`, `.ogg`
- MIDI: `.mid`, `.midi`

---

## License
MIT License – see `LICENSE` file.

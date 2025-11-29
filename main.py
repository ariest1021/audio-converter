# Audio Converter Instructions
# 1. Install [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) and [FluidSynth](https://www.fluidsynth.org/).  
# 2. Place `soundfont.sf2` in `soundfont/` and FluidSynth binary in `bin/`.  
# 3. Install Python dependencies
import ffmpeg
from midi2audio import FluidSynth
import os
from tqdm import tqdm
from multiprocessing import Pool
import subprocess
import tempfile


# Config
inputAudio = "audioInput" # Input Folder
outputAudio = "audioOutput" # Output Folder
audioFormat = "ogg" # Change to whatever format you want the audio file to be converted to.
vext = (".wav", ".flac", ".m4a", ".aac", ".mp3", ".ogg") # Valid Formats
vext_midi = (".mid", ".midi") # Valid MIDI Formats
max_cores = 4 # Max CPU cores to use

# Paths
basedir = os.path.abspath(os.path.dirname(__file__))
soundfont_path = os.path.join(basedir, "soundfont", "soundfont.sf2") # Path to SoundFont file

# FluidSynth binary (use if available, otherwise fallback to Python renderer)
fs_bin = os.path.join(basedir, "bin", "fluidsynth.exe")  # Path to FluidSynth binary
fs_bin_exists = os.path.exists(fs_bin)
if fs_bin_exists:
    os.environ["PATH"] = os.path.dirname(fs_bin) + os.pathsep + os.environ.get("PATH", "")

else:
     if not os.path.exists(soundfont_path):
            raise FileNotFoundError("SoundFont file not found and FluidSynth binary is missing.")
     else:
          pass # SoundFont file exists but no binary, will use Python renderer
     
# Convert Audio File: Converts audio files to specified format
def convertAudio(filename):
    input_path = os.path.join(inputAudio, filename)
    output_path = os.path.join(outputAudio, os.path.splitext(filename)[0] + "." + audioFormat)

    if filename.lower().endswith("." + audioFormat):
        return True  # Skip already converted files
    def log_fail(msg):
        with open("failed_conversions.txt", "a", encoding="utf-8") as log:
            log.write(f"{filename} - {msg}\n")

    try:
        # Converts To MIDI
        if filename.lower().endswith(vext_midi):
            temp_wav_path = os.path.join(tempfile.gettempdir(), os.path.splitext(filename)[0] + "_tmp.wav")

            success = False
            if fs_bin_exists:
                # Try both argument orders for fluidsynth
                orders = [
                    [fs_bin, "-ni", "-F", temp_wav_path, soundfont_path, input_path],
                    [fs_bin, "-ni", "-F", temp_wav_path, input_path, soundfont_path],
                ]
                for cmd in orders:
                    try:
                        # Silence all output
                        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if os.path.exists(temp_wav_path) and os.path.getsize(temp_wav_path) > 100:
                            success = True
                            break
                    except subprocess.CalledProcessError:
                        log_fail("Fluidsynth binary failed")

            # Fallback to Python FluidSynth if binary fails or missing
            if not success:
                try:
                    fs = FluidSynth(soundfont_path)
                    fs.midi_to_audio(input_path, temp_wav_path)
                    if os.path.exists(temp_wav_path) and os.path.getsize(temp_wav_path) > 100:
                        success = True
                except Exception as e:
                    log_fail(f"Python FluidSynth failed: {e}")

            if not success:
                log_fail("MIDI render failed — no valid WAV created")
                return False

            # Transcode to output format
            try:
                ffmpeg.input(temp_wav_path).output(
                    output_path,
                    codec="libopus",
                    threads=1,
                    map="0:a"
                ).run(quiet=True, overwrite_output=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except ffmpeg.Error as e:
                log_fail("ffmpeg error during MIDI conversion")
                return False
            finally:
                if os.path.exists(temp_wav_path):
                    try:
                        os.remove(temp_wav_path)
                    except Exception:
                        pass

            return True

        # Converts To Other Audio Formats
        try:
            ffmpeg.input(input_path).output(
                output_path,
                codec="libopus",
                threads=1,
                map="0:a"
            ).run(quiet=True, overwrite_output=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except ffmpeg.Error:
            log_fail("ffmpeg error during audio conversion")
            return False

    except Exception as e:
        log_fail(f"Unexpected error: {e}")
        return False


# Main
if __name__ == "__main__":
    os.makedirs(outputAudio, exist_ok=True)
    supported_exts = vext + vext_midi
    files = [
        f for f in os.listdir(inputAudio)
        if f.lower().endswith(supported_exts) and not f.lower().endswith(audioFormat)
    ]

    # Multiprocessing Pool
    with Pool(processes=min(os.cpu_count(), max_cores)) as pool:
        chunksize = max(1, len(files) // (min(os.cpu_count(), max_cores) * 4))
        for result in tqdm(pool.imap_unordered(convertAudio, files, chunksize=chunksize),
                           total=len(files),
                           desc="Converting"):
            pass
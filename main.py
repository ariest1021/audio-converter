# install ffmpeg before running https://www.gyan.dev/ffmpeg/builds/
import ffmpeg
import os
from tqdm import tqdm
from multiprocessing import Pool

inputAudio = "audioInput" # Input Folder
outputAudio = "audioOutput" # Output Folder
audioFormat = "ogg" # Change to whatever format you want the audio file to be converted to.
vext = (".wav", ".flac", ".m4a", ".aac", ".mp3", ".ogg") # valid formats




def convertAudio(filename):
    if filename.lower().endswith("." + audioFormat):
        return
    try:
                (
                ffmpeg
                .input(os.path.join(inputAudio, filename))
                .output(os.path.join(outputAudio, os.path.splitext(filename)[0] + "." + audioFormat),
                codec='libopus', # Encoder
                audio_bitrate='128k', # Audio Bitrate 
                ac=2, # Audio channels
                ar=48000, # Audio sample rate
                threads=1 
                )
                .run(quiet=True, overwrite_output=True)
            )
    except ffmpeg.Error as e:
        return




if __name__ == "__main__":
    os.makedirs(outputAudio, exist_ok=True)
    files = [
    f for f in os.listdir(inputAudio)
    if f.lower().endswith(vext) and not f.lower().endswith("." + audioFormat)
]
    with Pool(processes=os.cpu_count()) as pool:
        for result in tqdm(pool.imap_unordered(convertAudio, files), total=len(files), desc="Converting"):
            if result:
                print(result)
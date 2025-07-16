# install ffmpeg before running https://www.gyan.dev/ffmpeg/builds/
import ffmpeg
import os
from tqdm import tqdm
from multiprocessing import Pool

inputAudio = "audioInput"
outputAudio = "audioOutput"
audioFormat = "ogg" # Change to whatever format you want the audio file to be converted to.


vext = (".wav", ".flac", ".m4a", ".aac", ".mp3", ".ogg") # valid formats
files = [f for f in os.listdir(inputAudio) if f.lower().endswith(vext)]
def convertAudio(filename):

    if filename.lower().endswith("." + audioFormat):
           return
    try:
                (
                ffmpeg
                .input(os.path.join(inputAudio, filename))
                .output(os.path.join(outputAudio, os.path.splitext(filename)[0] + "." + audioFormat),
                codec='libopus',
                audio_bitrate='128k',
                ac=2,
                ar=48000,
                threads=1
                )
                .run(quiet=True, overwrite_output=True)
            )
    except ffmpeg.Error as e:
                return

if __name__ == "__main__":
    os.makedirs(outputAudio, exist_ok=True)
    files = [f for f in os.listdir(inputAudio) if f.lower().endswith(vext)]

    with Pool(processes=os.cpu_count()) as pool:
        for result in tqdm(pool.imap_unordered(convertAudio, files), total=len(files), desc="Converting"):
            if result:
                print(result)
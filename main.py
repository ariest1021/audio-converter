# install ffmpeg before running https://www.gyan.dev/ffmpeg/builds/
import ffmpeg
import os
from multiprocessing import Pool

inputAudio = "audioInput"
outputAudio = "audioOutput"
audioFormat = "ogg" # Change to whatever format you want the audio file to be converted to.


vext = (".wav", ".flac", ".m4a", ".aac", ".mp3") # valid formats
files = [f for f in os.listdir(inputAudio) if f.lower().endswith(vext)]
def convertAudio(filename):

    if not filename.lower().endswith(vext):
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
                print(f"Success [✔]: {filename}")
    except ffmpeg.Error as e:
                print(f"Fail [✘]: {filename}\n{e.stderr.decode()}")

if __name__ == "__main__":
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(convertAudio, files)
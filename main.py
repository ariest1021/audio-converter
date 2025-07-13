# install ffmpeg before running https://www.gyan.dev/ffmpeg/builds/
import ffmpeg
import os

inputAudio = "audioInput"
outputAudio = "audioOutput"
audioFormat = "ogg" # Change to whatever format you want the audio file to be converted to.


vext = (".wav", ".flac", ".m4a", ".aac", ".mp3") # valid formats

for filename in os.listdir(inputAudio): # Loop that goes through each file and converts to whatever format
    if filename.endswith(vext):
        try:
            (
                ffmpeg
                .input(os.path.join(inputAudio, filename))
                .output(os.path.join(outputAudio, os.path.splitext(filename)[0] + "." + audioFormat),
                codec='libopus',
                audio_bitrate='128k',
                ac=2,
                ar=48000,
                threads=0
                )
                .run()
            )
        except ffmpeg.Error as e:
            print(f"Failed to convert {filename}:\n{e.stderr.decode()}")
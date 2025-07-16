Simple Python script that converts audio files to a chosen format.

**TODO**
* Optimization!!!!
* ~~Multithread support~~
* ~~Skip files already in target format~~
* Optional auto-delete after conversion


**How to use**
* Install dependencies <br>
``pip install -r requirements.txt`` <br>
``ffmpeg: https://www.gyan.dev/ffmpeg/builds/`` <br>
* Put supported files inside the ``audioInput/`` folder.

* Run from terminal/command prompt <br>
``python main.py`` <br>
This convers supported audio files from ``audioInput`` and saves them in ``audioOutput/``

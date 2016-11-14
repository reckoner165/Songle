# Songle
Contains server and client side code for Songle.


## To build: 

1. Clone repo into a local directory
2. Install dependencies. The code runs on Python 2.7.10.
`pip install pyaudio`

3. Open client.py and make sure HOST is set to 'localhost' (if you run server from another device, set it to that device IP)
4. Run server.py and then client.py. The later has commandline arguments with test keys. Try `python client.py 002` to play the song that is internaly stored as 002.wav. PyAudio is known to support only wav files. Trying to stream mp3 or other compressed formats will result in garbage output.

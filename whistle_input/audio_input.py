import pyaudio
import numpy as np

from chirp import Chirp
from utils import RATE

# Set up audio stream
# reduce chunk size and sampling rate for lower latency
CHUNK_SIZE = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
p = pyaudio.PyAudio()

# print info about audio devices
# let user select audio device
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

print('select audio device:')
input_device = int(input())

# open audio input stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE,
                input_device_index=input_device)


# Chirp object
chirp = Chirp()

# Get audio input and listen for chirps
def listen():
    # continuously capture audio singal
    while True:
        # Read audio data from stream
        data = stream.read(CHUNK_SIZE)

        # Convert audio data to numpy array
        data = np.frombuffer(data, dtype=np.int16)

        # Get chirp data
        result = chirp.check_chirp(data)
        return result
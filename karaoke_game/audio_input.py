import pyaudio
import numpy as np

# Set up audio stream
# reduce chunk size and sampling rate for lower latency
CHUNK_SIZE = 1024 * 2  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Audio sampling rate (Hz)
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


# Get the dominant frequency

def get_frequency(data):
    spectrum = np.abs(np.fft.fft(data))
    frequencies = np.fft.fftfreq(len(data), 1/RATE)
    mask = frequencies >= 0
    spectrum = spectrum[mask]
    frequencies = frequencies[mask]
    return frequencies[np.argmax(spectrum)]


def freq_generator():
    # continuously capture and plot audio singal
    while True:
        # Read audio data from stream
        data = stream.read(CHUNK_SIZE)

        # Convert audio data to numpy array
        data = np.frombuffer(data, dtype=np.int16)

        # Get the dominant frequency from the data
        yield get_frequency(data)

import numpy as np
import time

from utils import RATE

# Chirp class to handle whistling chirp detection

class Chirp:

    def __init__(self):
        self.listening = False
        self.noise_threshold = 3000
        self.freq_threshold = 800       # Frequencies need to be at least 800 Hz to be considered part of a whistling sound
        self.chirp_span = 500           # Minimum difference between first and last frequency to be considered a chirp
        self.detection_span = 0.5       # Time span for a chirp
        self.start_time = 0
        self.freqs = []


    # Check if input is whistling chirp

    def check_chirp(self, data):
        # If input is above the noise threshold, start listening for a chirp
        if not self.listening and max(data) > self.noise_threshold and min(data) < -self.noise_threshold:
            self.listening = True
            self.start_time = time.time()

        # Add frequencies to self.freq if they exceed self.freq_threshold
        if self.listening:
            freq = self.get_frequency(data)
            if freq > self.freq_threshold:
                self.freqs.append(freq)

            # Take [self.detection_span] seconds to save the frequencies
            if time.time() - self.start_time >= self.detection_span:
                self.listening = False

                # If self.freqs has data, check the span between the first and last entry to determine
                # whether or not it's a chirp
                if len(self.freqs) > 1:
                    if self.freqs[0] - self.freqs[len(self.freqs) - 1] < -self.chirp_span:
                        self.freqs.clear()
                        return "up"
                    elif self.freqs[0] - self.freqs[len(self.freqs) - 1] > self.chirp_span:
                        self.freqs.clear()
                        return "down"
                    else:
                        self.freqs.clear()
                        return None
        
    
    # Get the dominant frequency

    def get_frequency(self, data):
        spectrum = np.abs(np.fft.fft(data))
        frequencies = np.fft.fftfreq(len(data), 1/RATE)
        mask = frequencies >= 0
        spectrum = spectrum[mask]
        frequencies = frequencies[mask]
        return frequencies[np.argmax(spectrum)]
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks, butter, lfilter
from scipy.io import wavfile
import matplotlib.pyplot as plt
import soundfile as sf
import librosa
import numpy as np
import sounddevice as sd
from uuid import uuid4
import os

class AudioProcessor:

    def __init__(self):
        self.signal = None
        self.sr = None
        self.fft = None
        self.frecuency = None
        self.signal_transformed = None
        self.fft_transformed = None
        self.frecuency_transformed = None
        self.signal_noise = None
        self.fft_noise = None
        self.frecuency_noise = None
        

    def read_audio(self, filename):

        self.clear()

        if filename.endswith('.wav'):
            sr, signal = wavfile.read(filename)
        
        elif filename.endswith('.mp3'):
            signal, sr = librosa.load(filename)

        else:
            raise ValueError('File format not supported')
        
        self.signal = signal
        self.sr = sr
        self.apply_fft()
        self.add_noise()
        self.apply_fft_noise()
    
    def apply_fft(self):
        self.fft = fft(self.signal)
        self.frecuency = fftfreq(len(self.fft), 1/self.sr)
        self.fft = self.fft[:len(self.fft)//2]
        self.frecuency = self.frecuency[:len(self.frecuency)//2]

    def butter_filter(self, cutoff, type, order):
        nyq = 0.5*self.sr
        normal_cutoff = cutoff / nyq
        b,a = butter(order, normal_cutoff, btype=type, analog=False)
        return b,a
    
    def butter_filter_band(self, lowcut, highcut, type, order):
        nyq = 0.5*self.sr
        low = lowcut / nyq
        high = highcut / nyq
        b,a = butter(order, [low, high], btype=type, analog=False)
        return b,a
    
    def highpass_filter(self, cutoff, order=5):
        b, a = self.butter_filter(cutoff, type="high", order=order)
        self.signal_transformed = lfilter(b, a, self.signal_noise)

    def lowpass_filter(self, cutoff, order=5):
        b,a = self.butter_filter(cutoff, type="low", order=order)
        self.signal_transformed = lfilter(b, a, self.signal_noise)

    def bandstop_filter(self, lowcut, highcut, order=5):
        b,a = self.butter_filter_band(lowcut, highcut, type="bandstop", order=order)
        self.signal_transformed = lfilter(b, a, self.signal_noise)

    def bandpass_filter(self, lowcut, highcut, order=5):
        b,a = self.butter_filter_band(lowcut, highcut, type="band", order=order)
        self.signal_transformed = lfilter(b, a, self.signal_noise)

    
    
    def apply_fft_transformed(self):
        self.fft_transformed = fft(self.signal_transformed)
        self.frecuency_transformed = fftfreq(len(self.fft_transformed), 1/self.sr)
        self.fft_transformed = self.fft_transformed[:len(self.fft_transformed)//2]
        self.frecuency_transformed = self.frecuency_transformed[:len(self.frecuency_transformed)//2]


    def add_noise(self):
        noise = np.random.normal(0, 0.01, len(self.signal))
        self.signal_noise = self.signal + noise    

    def apply_fft_noise(self):
        self.fft_noise = fft(self.signal_noise)
        self.frecuency_noise = fftfreq(len(self.fft_noise), 1/self.sr)
        self.fft_noise = self.fft_noise[:len(self.fft_noise)//2]
        self.frecuency_noise = self.frecuency_noise[:len(self.frecuency_noise)//2]
    
    def reproduce_signal(self, signal):
        if signal is not None:
            sd.play(signal, self.sr)
            sd.wait()
        
        else:
            print("No hay señal")
    
    def clear(self):
        self.signal = None
        self.sr = None
        self.fft = None
        self.frecuency = None
        self.signal_transformed = None
        self.fft_transformed = None
        self.frecuency_transformed = None
        self.signal_noise = None
        self.fft_noise = None
        self.frecuency_noise = None

    def save_transformed_audio(self):
        uuid = uuid4()
        filename = f"audio_transformed_{uuid}.wav"
        
        folder = "filtrados"
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        filepath = os.path.join(folder, filename)
        sf.write(filepath, self.signal_transformed, self.sr)
        
        print(f"Archivo guardado como: {filepath}")






        

    
    


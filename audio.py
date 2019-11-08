import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
import struct
arduino = serial.Serial('/dev/cu.usbmodem14201', 115200, timeout=.1)

time.sleep(1)

np.set_printoptions(suppress=True) # don't use scientific notation

CHUNK = 4096 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

# create a numpy array holding a single read of audio data
while True: #to it a few times just to see
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    data = data * np.hanning(len(data)) # smooth the FFT by windowing data
    fft = abs(np.fft.fft(data).real)
    fft = fft[:int(len(fft)/2)] # keep only first half
    freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    freq = freq[:int(len(freq)/2)] # keep only first half
    freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
    print("peak frequency: %d Hz"%freqPeak)
    if (freqPeak > 300 and freqPeak <= 500):
        arduino.write(struct.pack('>B', 1))
    elif (freqPeak > 500 and freqPeak <= 800):
        arduino.write(struct.pack('>B', 2))
    elif (freqPeak > 800 and freqPeak <= 1000):
        arduino.write(struct.pack('>B', 3))
    elif (freqPeak > 1000 and freqPeak <= 1150):
        arduino.write(struct.pack('>B', 4))
    elif (freqPeak > 1150 and freqPeak <= 1200):
        arduino.write(struct.pack('>B', 5))
    elif (freqPeak > 1200 and freqPeak <= 1300):
        arduino.write(struct.pack('>B', 6))
    elif (freqPeak > 1300 and freqPeak <= 1400):
        arduino.write(struct.pack('>B', 7))
    elif (freqPeak > 1400 and freqPeak <= 1500):
        arduino.write(struct.pack('>B', 8))
    elif (freqPeak > 1500 ):
        arduino.write(struct.pack('>B', 9))
    else:
        arduino.write(struct.pack('>B', 0))

    # uncomment this if you want to see what the freq vs FFT looks like
    #plt.plot(freq,fft)
    #plt.axis([0,4000,None,None])
    #plt.show()
    #plt.close()

# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()

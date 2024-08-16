# ===================================================================================
# PROGRAM PURPOSE
# ===================================================================================
# The purpose of this program is to demonstrate how phase shifting generally does
# not affect what the perceived audio is. This program will generate sounds with
# multiple tones and phase shifts and differing tone amplitudes
# ===================================================================================

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.io.wavfile import write
import math, random, os

# ===================================================================================
# ADJUST THESE PARAMETERS ONLY
# ===================================================================================

# Sampling frequency in Hertz (Hz)
f_sampling = 44100

# Audio play time in seconds (sec)
t_playtime = 5

# Frequencies are in Hertz (Hz)
# Phase shifts are in Degrees
signal1_amplitudes = [(1.0/(2*i + 1)) for i in range(10)]
signal1_frequencies = [(2*i + 1)*300 for i in range(10)]
signal1_phases = [0 for i in range(10)]

# Frequencies are in Hertz (Hz)
# Phase shifts are in Degrees
signal2_amplitudes = [(1.0/(2*i + 1)) for i in range(10)]
signal2_frequencies = [(2*i + 1)*300 for i in range(10)]
signal2_phases = [random.randint(0, 90) for i in range(10)]

# Give user the option to display as log plot
log_plot = False

# Print Frequencies to Screen or Text File?
print_screen = False

# ===================================================================================
# PROGRAM MAIN
# ===================================================================================

# Include the datetime of the program run so you know if files are from a current run or a previous run
program_run_time = datetime.now()

# Raise an error if signal frequency, phase and amplitude arrays are not the same length
arr_error_condition = (not (len(signal1_amplitudes) == len(signal1_frequencies) == len(signal1_phases))) \
    or (not (len(signal2_amplitudes) == len(signal2_frequencies) == len(signal2_phases)))

if arr_error_condition:
    raise ValueError("Arrays for signals 1 and 2 must be consistent in length with amplitude, frequency and phase components")


# Print out actual frequencies, phases and amplitudes in the signal
# Look at the print screen or text file arguement to decide when to print the contents

if print_screen:
    print(program_run_time)
    print("-"*50)
    print("Signal 1 Contents")
    print("-"*50)
    for i in range(len(signal1_frequencies)):
        print("Frequency %d: %4.2f Hz, Phase %d: %4.2f degrees, Amplitude %d: %4.8f V" % \
            (i+1, signal1_frequencies[i], i+1, signal1_phases[i], i+1, signal1_amplitudes[i]))
    
    print("\n\n\n")

    print("-"*50)
    print("Signal 2 Contents")
    print("-"*50)
    for i in range(len(signal2_frequencies)):
        print("Frequency %d: %4.2f Hz, Phase %d: %4.2f degrees, Amplitude %d: %4.8f V" % \
            (i+1, signal2_frequencies[i], i+1, signal2_phases[i], i+1, signal2_amplitudes[i]))
else:
    file_path = os.path.dirname(os.path.realpath(__file__))
    file_name = 'SpectrumContents.txt'

    with open(file_path + '\\' + file_name, 'w') as f:
        print(program_run_time, file=f)
        print("-"*50, file=f)
        print("Signal 1 Contents", file=f)
        print("-"*50, file=f)
        for i in range(len(signal1_frequencies)):
            print("Frequency %d: %4.2f Hz, Phase %d: %4.2f degrees, Amplitude %d: %4.8f V" % \
                (i+1, signal1_frequencies[i], i+1, signal1_phases[i], i+1, signal1_amplitudes[i]), file=f)
        
        print("\n\n\n", file=f)

        print("-"*50, file=f)
        print("Signal 2 Contents", file=f)
        print("-"*50, file=f)
        for i in range(len(signal2_frequencies)):
            print("Frequency %d: %4.2f Hz, Phase %d: %4.2f degrees, Amplitude %d: %4.8f V" % \
                (i+1, signal2_frequencies[i], i+1, signal2_phases[i], i+1, signal2_amplitudes[i]), file=f)


t = np.linspace(0, t_playtime, math.ceil(t_playtime * f_sampling))
signal1 = np.linspace(0, 0, len(t))
signal2 = np.linspace(0, 0, len(t))

for i in range(len(signal1_frequencies)):
    signal1 = signal1 + np.multiply(signal1_amplitudes[i], np.sin(2*np.pi*signal1_frequencies[i]*t + (np.pi/180)*signal1_phases[i]))

for i in range(len(signal2_frequencies)):
    signal2 = signal2 + np.multiply(signal2_amplitudes[i], np.sin(2*np.pi*signal2_frequencies[i]*t + (np.pi/180)*signal2_phases[i]))

# Get plot parameters here
freq_min = min(signal1_frequencies + signal2_frequencies)
num_cycles = 10.0

plt.figure(1)
plt.plot(t, signal1)
plt.plot(t, signal2)
plt.legend(["Signal 1", "Signal 2"])
plt.title("Time Domain Plot of Signals")
plt.xlabel("Time [sec]")
plt.xlim([0, num_cycles/freq_min])
plt.ylabel("Amplitude [V]")
plt.minorticks_on()
plt.grid(visible=True)

# Get the frequency and phase content of both signals with the FFT
# First window both signals to reduce spectral leakage

signal1_windowed = np.multiply(np.kaiser(len(signal1), beta=2), signal1)
signal2_windowed = np.multiply(np.kaiser(len(signal2), beta=2), signal2)

signal1_fft = np.divide(2*np.fft.fftshift(np.fft.fft(signal1_windowed)), len(signal1_windowed))
signal2_fft = np.divide(2*np.fft.fftshift(np.fft.fft(signal2_windowed)), len(signal2_windowed))
f = (f_sampling/2)*np.linspace(-1, 1, len(signal1_fft))


# Figure out plot parameters for sizing the windows appropriately
f_min_signal1 = min(signal1_frequencies) * 0.8
f_max_signal1 = max(signal1_frequencies) * 1.2
f_min_signal2 = min(signal2_frequencies) * 0.8
f_max_signal2 = max(signal2_frequencies) * 1.2

plt.figure(2)
# Frequency Content of Signal 1
plt.subplot(2,1,1)
if log_plot:
    plt.loglog(f, np.abs(signal1_fft), color="C0")
    plt.minorticks_on()
    plt.grid(visible=True, which="both")
else:
    plt.plot(f, np.abs(signal1_fft), color="C0")
    plt.minorticks_on()
    plt.grid(visible=True)
plt.xlim([f_min_signal1, f_max_signal1])
plt.title("Spectrum of Signal 1")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitudes [V]")
# Phase Content of Signal 1
plt.subplot(2,1,2)
plt.plot(f, np.angle(signal1_fft, deg=True), color="C0")
plt.xlim([f_min_signal1, f_max_signal1])
plt.title("Phase Content of Signal 1")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Phase (degrees)")
plt.minorticks_on()
plt.grid(visible=True)


plt.figure(3)
# Frequency Content of Signal 2
plt.subplot(2,1,1)
if log_plot:
    plt.loglog(f, np.abs(signal2_fft), color="C1")
    plt.minorticks_on()
    plt.grid(visible=True, which="both")
else:
    plt.plot(f, np.abs(signal2_fft), color="C1")
    plt.minorticks_on()
    plt.grid(visible=True)
plt.xlim([f_min_signal2, f_max_signal2])
plt.title("Spectrum of Signal 2")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitudes [V]")
plt.minorticks_on()
plt.grid(visible=True)
# Phase Content of Signal 2
plt.subplot(2,1,2)
plt.plot(f, np.angle(signal2_fft, deg=True), color="C1")
plt.xlim([f_min_signal2, f_max_signal2])
plt.title("Phase Content of Signal 2")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Phase (Degrees)")
plt.minorticks_on()
plt.grid(visible=True)


plt.show()


# Export the waveforms now as .wav files so they can be played
file_path = os.path.dirname(os.path.realpath(__file__))
file_name_signal1 = 'Signal1.wav'
file_name_signal2 = 'Signal2.wav'

# Signals need to be scaled for a maximum value of 1 in order to play without clipping in the float32 format
signal1 = np.divide(signal1, np.max(np.abs(signal1)))
signal2 = np.divide(signal2, np.max(np.abs(signal2)))

write(file_path + "\\" + file_name_signal1, f_sampling, signal1.astype(np.float32))
write(file_path + "\\" + file_name_signal2, f_sampling, signal2.astype(np.float32))

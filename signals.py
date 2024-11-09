import numpy as np

def signalSpectrum(signalSamples, sampleRate):
  spectrum = np.fft.fftshift(np.fft.fft(signalSamples))
  freqs = np.fft.fftshift(np.fft.fftfreq(len(signalSamples), 1/sampleRate))
  return freqs, spectrum

def signalMeanPower(signalSamples):
  instantaneous_power = np.abs(signalSamples) ** 2
  # average_power = np.mean(instantaneous_power)
  return instantaneous_power
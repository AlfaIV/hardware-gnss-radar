import numpy as np
import datetime
import asyncio
import aiohttp
import requests
import time
from datetime import datetime, timezone, timedelta
import logging

from sdr import sdrConnect
from signals import signalSpectrum, signalMeanPower

url = 'http://85.198.109.43:1000/hardware'
token = '1234567890'
# sample_num = 256 * 1024
sample_num = 256
logging.basicConfig(level=logging.DEBUG)


def sendPower(sdr):
    startTime = datetime.now(timezone.utc).isoformat()
    timeStep = (datetime.now(timezone.utc) + timedelta(seconds=1/sdr.sample_rate)).isoformat()
    samples = sdr.read_samples(sample_num)
    print(f'Получено {len(samples)} выборок.')
    power = signalMeanPower(samples)
    print(f'Рассчитанная мощность: {power}')
    
    data = {
        'token': token,
        'description': {
            'startTime': startTime,
            'endTime': datetime.now(timezone.utc).isoformat(),
            'group': "GPS",
            'target': "G12",
            'signal': 'L1'
        },
        'data': {
            'power': power.tolist(),
            'startTime': startTime,
            'timeStep': timeStep,
        }
    }
    
    response = requests.post(f"{url}/power", json=data)
    if response.status_code == 200:
        print('Успешно отправлена мощность сигнала!')
        print('Ответ сервера:', response)
    else:
        print('Ошибка при отправке мощности сигнала:', response.status_code)
        print('Ответ сервера:', response)

def sendSpectrum(sdr):
    startTime = datetime.now(timezone.utc).isoformat()
    samples = sdr.read_samples(sample_num)
    freqs, spectrum = signalSpectrum(samples, sdr.sample_rate)
    print(f'Получено {len(samples)} выборок.')
    
    data = {
        'token': token,
        'description': {
            'startTime': startTime,
            'endTime': datetime.now(timezone.utc).isoformat(),
            'group': "GPS",
            'signal': 'L1',
            'target': "G12",
        },
        'data': {
            'spectrum': np.log10(np.abs(spectrum)).tolist(),
            'startFreq': freqs.tolist()[0],
            'freqStep': freqs.tolist()[1] - freqs.tolist()[0],
            'startTime': startTime,
        }
    }
    
    response = requests.post(f"{url}/spectrum", json=data)
    if response.status_code == 200:
        print('Успешно отправлен спектр сигнала!')
        print('Ответ сервера:', response)
    else:
        print('Ошибка при отправке спектра сигнала:', response.status_code)
        print('Ответ сервера:', response)

@sdrConnect
def main(sdr):
  while True:
    sendPower(sdr),
    time.sleep(5),
    sendSpectrum(sdr),
    time.sleep(5),


if __name__ == "__main__":
    main()

# @sdrConnect
# def plots(sdr):
#   samples = sdr.read_samples(256*1024)
#   print(f'Получено {len(samples)} выборок.')

#   freqs, spectrum = signalSpectrum(samples, sdr.sample_rate)

#   fig, ax = plt.subplots()
#   ax.set_title('Спектр сигнала')
#   ax.set_xlabel('Частота (Гц)')
#   ax.set_ylabel('Амплитуда (дБ)')
#   ax.set_xlim(-sdr.sample_rate/2, sdr.sample_rate/2)
#   ax.grid(True)

#   graph, = ax.plot(freqs, 20 * np.log10(np.abs(spectrum)))

#   def update(frame):
    
#     nonlocal graph
#     samples = sdr.read_samples(256*1024)
#     freqs, spectrum = signalSpectrum(samples, sdr.sample_rate)
#     graph.set_data(freqs, 20 * np.log10(np.abs(spectrum)))
#     return graph

#   ani = FuncAnimation(fig, update, frames=None)
#   plt.show()
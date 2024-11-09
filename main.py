import numpy as np
import datetime
import asyncio
import aiohttp
import requests
import time

from sdr import sdrConnect
from signals import signalSpectrum, signalMeanPower

url = 'http://85.198.109.43:1000/hardware/'
token = '1234567890'

# async def sendPower(sdr):
#     now = datetime.datetime.now()
#     samples = sdr.read_samples(256 * 1024)
#     print(f'Получено {len(samples)} выборок.')
#     power = signalMeanPower(samples)
#     print(f'Рассчитанная мощность: {power}')
    
#     data = {
#         'token': token,
#         'description': {
#             'time': now.time(),
#             'date': now.date(),
#             'satelliteGroup': "GPS",
#             'satelliteID': "G12",
#             'signalType': 'L1'
#         },
#         'data': {
#             'type': "power",
#             'power': power.tolist(),
#         }
#     }
    
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, json=data) as response:
#             if response.status == 200:
#                 print('Успешно отправлена мощность сигнала!')
#                 print('Ответ сервера:', await response.json())
#             else:
#                 print('Ошибка при отправке мощности сигнала:', response.status)
#     await asyncio.sleep(10)

# async def sendSpectrum(sdr):
#     now = datetime.datetime.now()
#     samples = sdr.read_samples(256 * 1024)
#     freqs, spectrum = signalSpectrum(samples, sdr.sample_rate)
#     print(f'Получено {len(samples)} выборок.')
    
#     data = {
#         'token': token,
#         'description': {
#             'time': now.time(),
#             'date': now.date(),
#             'satelliteGroup': "GPS",
#             'satelliteID': "G12",
#             'signalType': 'L1'
#         },
#         'data': {
#             'type': "spectrum",
#             'frequencies': freqs.tolist(),
#             'spectrum': np.log10(np.abs(spectrum)).tolist(),
#         }
#     }
    
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, json=data) as response:
#             if response.status == 200:
#                 print('Успешно отправлен спектр сигнала!')
#                 print('Ответ сервера:', await response.json())
#             else:
#                 print('Ошибка при отправке спектра сигнала:', response.status)
#     await asyncio.sleep(10) 

# @sdrConnect
# async def main(sdr):
#     await asyncio.gather(
#         sendPower(sdr),
#         sendSpectrum(sdr),
#     )

# if __name__ == "__main__":
#     main()


def sendPower(sdr):
    now = datetime.datetime.now()
    samples = sdr.read_samples(256 * 1024)
    print(f'Получено {len(samples)} выборок.')
    power = signalMeanPower(samples)
    print(f'Рассчитанная мощность: {power}')
    
    data = {
        'token': token,
        'description': {
            'time': now.time().strftime('%H:%M:%S'),
            'date': now.date().strftime('%Y-%m-%d'),
            'satelliteGroup': "GPS",
            'satelliteID': "G12",
            'signalType': 'L1'
        },
        'data': {
            'type': "power",
            'power': power.tolist(),
        }
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('Успешно отправлена мощность сигнала!')
        print('Ответ сервера:', response.json())
    else:
        print('Ошибка при отправке мощности сигнала:', response.status_code)

def sendSpectrum(sdr):
    now = datetime.datetime.now()
    samples = sdr.read_samples(256 * 1024)
    freqs, spectrum = signalSpectrum(samples, sdr.sample_rate)
    print(f'Получено {len(samples)} выборок.')
    
    data = {
        'token': token,
        'description': {
            'time': now.time().strftime('%H:%M:%S'),
            'date': now.date().strftime('%Y-%m-%d'),
            'satelliteGroup': "GPS",
            'satelliteID': "G12",
            'signalType': 'L1'
        },
        'data': {
            'type': "spectrum",
            'frequencies': freqs.tolist(),
            'spectrum': np.log10(np.abs(spectrum)).tolist(),
        }
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('Успешно отправлен спектр сигнала!')
        print('Ответ сервера:', response.json())
    else:
        print('Ошибка при отправке спектра сигнала:', response.status_code)

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
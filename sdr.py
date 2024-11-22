from rtlsdr import RtlSdr
import random

class SDRsim:
    def __init__(self):
        self.sdr = {
            'sample_rate': 0,
            'center_freq': 0,
            'gain': ''
        }
    
    def read_samples(self, count):
        complex_numbers = []
        for _ in range(count):
            real_part = random.random()
            imaginary_part = random.random()
            complex_number = complex(real_part, imaginary_part)
            complex_numbers.append(complex_number)
        return complex_numbers
    
    def close(self):
        return

def sdrConnect(func):
    def wrapper(*args, **kwargs):
        try:
            sdr = RtlSdr()
        except Exception as e:
            print("Ошибка подключения к RTL-SDR:", e)
            sdr = SDRsim()
            print("Подключение симулятора работы SDR")
            # return
        print("Успешное подключение к RTL-SDR.")
        sdr.sample_rate = 2.048e6  
        sdr.center_freq = 1227.60e6    
        sdr.gain = 'auto'          
        print("Успешная настройка параметров RTL-SDR.")
        result = func(*args, **kwargs, sdr=sdr)
        sdr.close()
        print("Успешное отключение от SDR")
        return result
    return wrapper

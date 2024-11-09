from rtlsdr import RtlSdr    

def sdrConnect(func):
    def wrapper(*args, **kwargs):
        sdr = RtlSdr()
        print("Успешное подключение к RTL-SDR.")
        sdr.sample_rate = 2.048e6  
        sdr.center_freq = 100e6    
        sdr.gain = 'auto'          
        print("Успешная настройка параметров RTL-SDR.")
        result = func(*args, **kwargs, sdr=sdr)
        sdr.close()
        print("Успешное отключение от SDR")
        return result
    return wrapper
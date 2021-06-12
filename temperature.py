from w1thermsensor import W1ThermSensor
import glob

onewire_dir = '/sys/bus/w1/devices/'

def get_temperature():
    sensor1 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20,str(glob.glob(onewire_dir + '28*')[0])[23:])
    
    temp = sensor1.get_temperature()
    return temp

# print(get_temperature())
import Adafruit_ADS1x15
GAIN = 1
adc1 = Adafruit_ADS1x15.ADS1115(address=0x48)
def get_light():
    temp_val = adc1.read_adc(3, gain=GAIN, data_rate=128)
    if temp_val > 4000:
        temp_val = 4000
    # 0 zui an , 100 zui liang
    return (100 - (temp_val / 40))
    # print(adc1.read_adc(3, gain=GAIN, data_rate=128))
    
# print(get_light())
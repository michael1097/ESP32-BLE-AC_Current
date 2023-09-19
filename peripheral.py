import bluetooth
import time
from simpleBLE import BLEPeripheral
from machine import Pin
from machine import ADC
from math import sqrt
from time import ticks_ms


# Bluetooth object
ble = bluetooth.BLE() 

# Environmental service
service=0x427d 

# Temperature characteristic
characteristic=0xace6 

# BLE peripheral object
power = BLEPeripheral(ble,"The best Sensor",service,characteristic) 

pin = Pin(34)
button = Pin(0)
adc=ADC(pin)
adc.atten(ADC.ATTN_11DB)

s = 0.066			#Sensibility

def getAverage():
    average = 0
    n = 0
    t = ticks_ms()

    while (ticks_ms() - t) <= 200:
        n += 1
        average += 3.3*adc.read()/4095
    
    return (average/n,n)
    
def getIrms(voff,N):
    v=0
    for j in range(N):
        v += ((3.3*adc.read()/4095)-voff)**2
    i = (1/s)*sqrt(v/N)
    return i

def getPapp(Irms):
    pot = Irms*120
    return pot
pot = 0
while True:
    if button.value() == 1:
        (average,n) = getAverage()
        #print("Average:",average)
        #print("Samples:",n)
        
        Irms = getIrms(average,n)
        #print("Irms:",Irms)

        pot += getPapp(Irms)/3600000
        print("Papp:",pot)
        
        power.set_values([int(pot*100)],notify=False,indicate=False)
        time.sleep_ms(1000)
        

    else:
        break
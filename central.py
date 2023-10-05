import bluetooth
import struct
import time
import sys
from simpleBLE import BLECentral
from machine import deepsleep

# Bluetooth object
ble = bluetooth.BLE()

# Environmental service
service=0x427d 

# Temperature characteristic
characteristic=0xace6 

# BLE Central object
central = BLECentral(ble,service,characteristic)

not_found = False

def on_scan(addr_type, addr, name):
    if addr_type is not None:
        print("Found sensor:", addr_type, addr, name)
        central.connect()
    else:
        global not_found
        not_found = True
        print("No sensor found.")

central.scan(callback=on_scan)

# Wait for connection...
while not central.is_connected():
    time.sleep_ms(100)
    if not_found:
        sys.exit()

print("Connected")

central.on_notify(callback= lambda data :print('Notified') )

# Explicitly issue reads, using "print" as the callback.
while central.is_connected():
    central.read(callback=lambda data: print(data[0]/100))
    deepsleep(1000)

# Alternative to the above, just show the most recently notified value.
# while central.is_connected():
#     print(central.value())
#     time.sleep_ms(1000)

print("Disconnected")

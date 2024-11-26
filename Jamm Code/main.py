import machine
from machine import Pin
import time
import ir_tx
from ir_tx.nec import NEC

tx_pin = Pin(4,Pin.OUT)
device_addr = 0x01
transmitter = NEC(tx_pin, freq=30_000)


while True:
    transmitter.transmit(device_addr,0x1)
    time.sleep(0.2)
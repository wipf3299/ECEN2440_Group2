#   Pico pin GP13   -> AIN2
#   Pico pin GP12   -> AIN1
#   any Pico GND    -> GND

import math, time
import machine

# load the MicroPython pulse-width-modulation module for driving hardware
from machine import PWM

from machine import Pin

time.sleep(1) # Wait for USB to become ready


pwm_rate = 2000
ain1_ph = Pin(12, Pin.OUT) # Initialize GP14 as an OUTPUT
ain2_en = PWM(13, freq = pwm_rate, duty_u16 = 0)

pwm = min(max(int(2**16 * abs(1)), 0), 65535)

while True:
#    for OFF
    # time.sleep(2)
    print("Motor ON") # Print to REPL
    ain1_ph.low()
    ain2_en.duty_u16(pwm)
   
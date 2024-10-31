import machine
from machine import Pin
from machine import PWM
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

pwm_rate = 2000
ain1_ph = Pin(12, Pin.OUT) # Initialize GP14 as an OUTPUT
ain2_en = PWM(13, freq = pwm_rate, duty_u16 = 0)

pwm = min(max(int(2**16 * abs(1)), 0), 65535)

# Callback function to execute when an IR code is received
def ir_callback(data, addr, _):
    if data == 0x01 or data == 0x02:
        print("Motor FORWARDS") # Print to REPL
        ain1_ph.low()
        ain2_en.duty_u16(pwm)
    elif data == 0x03:
        print("Motor BACKWARDS") # Print to REPL
        ain1_ph.high()
        ain2_en.duty_u16(pwm)
    elif data == 0x04: 
        print("Motor OFF") # Print to REPL
        ain1_ph.low()
        ain2_en.duty_u16(0) 

# Setup the IR receiver
ir_pin = Pin(17, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring
ir_receiver = NEC_8(ir_pin, callback=ir_callback)
# Optional: Use the print_error function for debugging
ir_receiver.error_function(print_error)

# Main loop to keep the script running
while True:
    pass

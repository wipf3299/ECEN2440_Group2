import machine
from machine import Pin
from machine import PWM
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

pwm_rate = 2000
m1_ain1_ph = Pin(12, Pin.OUT) 
m1_ain2_en = PWM(13, freq = pwm_rate, duty_u16 = 0)

m2_ain1_ph = Pin(8, Pin.OUT) 
m2_ain2_en = PWM(9, freq = pwm_rate, duty_u16 = 0)

pwm = min(max(int(2**16 * abs(1)), 0), 65535)

# Callback function to execute when an IR code is received
def ir_callback(data, addr, _):
    if data == 0x01:
        print("Motor FORWARDS") # Print to REPL
        m1_ain1_ph.low()
        m1_ain2_en.duty_u16(pwm)
        m2_ain1_ph.low()
        m2_ain2_en.duty_u16(pwm)
    elif data == 0x02:
        print("Motor BACKWARDS") # Print to REPL
        m1_ain1_ph.high()
        m1_ain2_en.duty_u16(pwm)
        m2_ain1_ph.high()
        m2_ain2_en.duty_u16(pwm)
    elif data == 0x03: 
        print("Motor LEFT") # Print to REPL
        m1_ain1_ph.low()
        m1_ain2_en.duty_u16(pwm)
        m2_ain1_ph.high()
        m2_ain2_en.duty_u16(pwm)
    elif data == 0x04: 
        print("Motor RIGHT") # Print to REPL
        m1_ain1_ph.high()
        m1_ain2_en.duty_u16(pwm)
        m2_ain1_ph.low()
        m2_ain2_en.duty_u16(pwm)
    elif data == 0x05: 
        print("Motor OFF") # Print to REPL
        m1_ain1_ph.low()
        m1_ain2_en.duty_u16(0) 
        m2_ain1_ph.low()
        m2_ain2_en.duty_u16(0) 

# Setup the IR receiver
ir_pin = Pin(17, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring
ir_receiver = NEC_8(ir_pin, callback=ir_callback)
# Optional: Use the print_error function for debugging
ir_receiver.error_function(print_error)

# Main loop to keep the script running
while True:
    pass

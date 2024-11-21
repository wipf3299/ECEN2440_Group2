import machine
from machine import Pin, PWM, Timer, mem32
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

def setPinDriveStrength(pin, mA):
    PADS_BANK0_BASE     = 0x4001C000
    PAD_GPIO            = PADS_BANK0_BASE + 0x04 # Add (pin * 4)
    PAD_GPIO_MPY        = 4
    PAD_DRIVE_BITS      = 4 # 0=2mA, 1=4mA, 2=8mA, 3=12mA   Default=1, 4mA drive
    adr = PAD_GPIO + PAD_GPIO_MPY * pin
    mem32[adr] &= 0xFFFFFFFF ^ ( 0b11 << PAD_DRIVE_BITS)
    if   mA <= 2 : mem32[adr] |= 0b00 << PAD_DRIVE_BITS
    elif mA <= 4 : mem32[adr] |= 0b01 << PAD_DRIVE_BITS
    elif mA <= 8 : mem32[adr] |= 0b10 << PAD_DRIVE_BITS
    else         : mem32[adr] |= 0b11 << PAD_DRIVE_BITS

global current_direction 
current_direction = -1

pwm_rate = 2000
pwm = min(max(int(2**16 * abs(1)), 0), 65535)

m1_ain1_ph = Pin(12, Pin.OUT) 
m1_ain2_en = PWM(13, freq = pwm_rate, duty_u16 = 0)

m2_ain1_ph = Pin(8, Pin.OUT) 
m2_ain2_en = PWM(9, freq = pwm_rate, duty_u16 = 0)

def ir_callback(data, addr, _):
    current_direction = data
    motorDirection(data)

def stopMotors():
    print("Motor OFF") # Print to REPL
    m1_ain1_ph.low()
    m1_ain2_en.duty_u16(0) 
    m2_ain1_ph.low()
    m2_ain2_en.duty_u16(0) 


def motorDirection(data):
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
    else:
        stopMotors()

def timer_callback(timer):
    global current_direction
    if current_direction == 0x05:
        stopMotors()

# Setup the IR receiver
ir_pin = Pin(17, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring
ir_receiver = NEC_8(ir_pin, callback=ir_callback)
# Optional: Use the print_error function for debugging
ir_receiver.error_function(print_error)
setPinDriveStrength(17, 12) # Set drive strenth to 12mA

# Setup the timer
timer = Timer(-1)
timer.init(period=1000, mode=Timer.PERIODIC, callback=timer_callback)

# Main loop 
while True:
    pass

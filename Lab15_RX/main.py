alse # Boolean to toggle between RF and IR

global current_direction # Used for IR control
current_direction = -1

pwm_rate = 2000
pwm = 65535//4 # 25% duty cycle

m1_ain1_ph = Pin(14, Pin.OUT) 
m1_ain2_en = PWM(15, freq = pwm_rate, duty_u16 = 0)

m2_ain1_ph = Pin(12, Pin.OUT) 
m2_ain2_en = PWM(13, freq = pwm_rate, duty_u16 = 0)

d0 = Pin(4, Pin.IN, Pin.PULL_DOWN)
d1 = Pin(5, Pin.IN, Pin.PULL_DOWN)
d2 = Pin(6, Pin.IN, Pin.PULL_DOWN)
d3 = Pin(7, Pin.IN, Pin.PULL_DOWN)

def stopMotors():
    print("Motor OFF") # Print to REPL
    m1_ain1_ph.low()
    m1_ain2_en.duty_u16(0) 
    m2_ain1_ph.low()
    m2_ain2_en.duty_u16(0) 

def motorForwards():
    print("Motor FORWARDS") # Print to REPL
    m1_ain1_ph.low()
    m1_ain2_en.duty_u16(pwm)
    m2_ain1_ph.low()
    m2_ain2_en.duty_u16(pwm)

def motorBackwards():
    print("Motor BACKWARDS") # Print to REPL
    m1_ain1_ph.high()
    m1_ain2_en.duty_u16(pwm)
    m2_ain1_ph.high()
    m2_ain2_en.duty_u16(pwm)

def motorLeft():
    print("Motor LEFT") # Print to REPL
    m1_ain1_ph.low()
    m1_ain2_en.duty_u16(pwm)
    m2_ain1_ph.high()
    m2_ain2_en.duty_u16(pwm)

def motorRight():
    print("Motor RIGHT") # Print to REPL
    m1_ain1_ph.high()
    m1_ain2_en.duty_u16(pwm)
    m2_ain1_ph.low()
    m2_ain2_en.duty_u16(pwm) 

def boostON():
    print("Boost ON")
    global pwm
    pwm = 65535//4

def boostOFF():
    print("Boost OFF")
    global pwm
    pwm = 65535

def motorDirection(dir):
    if dir == 0x01:
        motorForwards()
    elif dir == 0x02:
        motorBackwards()
    elif dir == 0x03: 
        motorLeft()
    elif dir == 0x04: 
        motorRight()
    elif dir == 0x05:
        stopMotors()
    elif dir == 0x06:
        boostON()
    elif dir == 0x07:
        boostOFF()
    
        
def handleSignal(signal):
    if signal == 0x1: # 0b0001        
        motorForwards()
    elif signal == 0x2: # 0b0010
        motorBackwards()
    elif signal == 0x4: # 0b0100
        motorRight()
    elif signal == 0x8: # 0b1000
        motorLeft()
    elif signal == 0x6: # 0b0110
        stopMotors()
    elif signal == 0x3: # 0b0011
        boostON()
    elif signal == 0x5: # 0b0101
        boostOFF()

def ir_callback(data, addr, _):
    global current_direction
    current_direction = data

def timer_callback(timer):
    if rf:
        signal = 0b0000
        signal = ((signal << 1) | d3.value())
        signal = ((signal << 1) | d2.value())
        signal = ((signal << 1) | d1.value())
        signal = ((signal << 1) | d0.value())
        handleSignal(signal)
    else:
        motorDirection(current_direction)

# Setup the IR receiver
ir_pin = Pin(18, Pin.IN, Pin.PULL_UP) 
ir_receiver = NEC_8(ir_pin, callback=ir_callback)

# Setup the timer
timer = Timer(-1)
timer.init(period=100, mode=Timer.PERIODIC, callback=timer_callback)

# Turn on on-board LED to ensure Pico is receiving power
led = Pin(25, Pin.OUT)
led.value(1)

# Main loop 
while True:
    pass

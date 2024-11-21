import machine
from machine import Pin
from machine import PWM

pwm_rate = 2000
m1_ain1_ph = Pin(12, Pin.OUT) 
m1_ain2_en = PWM(13, freq = pwm_rate, duty_u16 = 0)

m2_ain1_ph = Pin(8, Pin.OUT) 
m2_ain2_en = PWM(9, freq = pwm_rate, duty_u16 = 0)

pwm = min(max(int(2**16 * abs(1)), 0), 65535)

d0 = Pin(18, Pin.IN, Pin.PULL_DOWN)
d1 = Pin(19, Pin.IN, Pin.PULL_DOWN)
d2 = Pin(20, Pin.IN, Pin.PULL_DOWN)
d3 = Pin(21, Pin.IN, Pin.PULL_DOWN)

def d0_callback(data):
    print("Motor FORWARDS")
    m1_ain1_ph.low()
    m1_ain2_en.duty_u16(pwm)
    m2_ain1_ph.low()
    m2_ain2_en.duty_u16(pwm)
def d1_callback(data):
    print("Motor BACKWARDS") 
    m1_ain1_ph.high()
    m1_ain2_en.duty_u16(pwm)
    m2_ain1_ph.high()
    m2_ain2_en.duty_u16(pwm)
def d2_callback(data):
    print("Motor OFF") 
    m1_ain1_ph.low()
    m1_ain2_en.duty_u16(0) 
    m2_ain1_ph.low()
    m2_ain2_en.duty_u16(0) 
def d3_callback(data):
    print("Received data from D3")

d0.irq(trigger = Pin.IRQ_RISING, handler = d0_callback)
d1.irq(trigger = Pin.IRQ_RISING, handler = d1_callback)
d2.irq(trigger = Pin.IRQ_RISING, handler = d2_callback)
d3.irq(trigger = Pin.IRQ_RISING, handler = d3_callback)

while True:
    pass

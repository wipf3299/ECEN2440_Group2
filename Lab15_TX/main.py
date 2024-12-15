import machine
from machine import I2C, Pin
import seesaw
import time
import seesaw
import ir_tx
from ir_tx.nec import NEC

# Initialize I2C. Adjust pin numbers based on your Pico's configuration
i2c = I2C(0, scl=Pin(17), sda=Pin(16))

# RF Transmitter Pins
d0_pin = 18
d1_pin = 19
d2_pin = 20
d3_pin = 21

rf_pin0 = Pin(d0_pin, Pin.OUT)
rf_pin1 = Pin(d1_pin, Pin.OUT)
rf_pin2 = Pin(d2_pin, Pin.OUT)
rf_pin3 = Pin(d3_pin, Pin.OUT)

# Initialize the Seesaw driver with the I2C interface
# Use the Gamepad QT's I2C address from the Arduino code (0x50)
seesaw_device = seesaw.Seesaw(i2c, addr=0x50)

# Define button and joystick pin numbers as per the Arduino code
BUTTON_A = 5
BUTTON_B = 1
BUTTON_X = 6
BUTTON_Y = 2
BUTTON_START = 16
BUTTON_SELECT = 0
JOYSTICK_X_PIN = 14
JOYSTICK_Y_PIN = 15

# Button mask based on Arduino code
BUTTONS_MASK = (1 << BUTTON_X) | (1 << BUTTON_Y) | \
              (1 << BUTTON_A) | (1 << BUTTON_B) | \
              (1 << BUTTON_SELECT) | (1 << BUTTON_START)

tx_pin = Pin(4,Pin.OUT)
device_addr = 0x01
transmitter = NEC(tx_pin)

# Initialize LED states
button_states = {
   BUTTON_A: False,
   BUTTON_B: False,
   BUTTON_X: False,
   BUTTON_Y: False,
   BUTTON_START: False,
   BUTTON_SELECT: False
}

# Initialize last button states
last_buttons = 0

# Initialize joystick center position
joystick_center_x = 511
joystick_center_y = 497

def rf_transmit(option):
     if option == 1:   # Forward
          # ADDED BY CEARA
          rf_pin1.low()
          rf_pin2.low()
          rf_pin3.low()
          # END OF ADDED BY CEARA
          rf_pin0.high()
     elif option == 2: # Backward
          # ADDED BY CEARA
          rf_pin0.low()
          rf_pin2.low()
          rf_pin3.low()
          # END OF ADDED BY CEARA
          rf_pin1.high()
     elif option == 3: # Boost On
          rf_pin0.high()
          rf_pin1.high()
     elif option == 4: # Left
          rf_pin2.high()
     elif option == 5: # Boost Off
          rf_pin0.high()
          rf_pin2.high()
     elif option == 6:
          rf_pin1.high()
          rf_pin2.high()
     elif option == 7:
          rf_pin0.high()
          rf_pin1.high()
          rf_pin2.high()
     elif option == 8: # Right
          rf_pin3.high()
     elif option == 9:
          rf_pin0.high()
          rf_pin3.high()
     elif option == 10:
          rf_pin1.high()
          rf_pin3.high()
     elif option == 11:
          rf_pin0.high()
          rf_pin1.high()
          rf_pin3.high()
     elif option == 12: # Stop new
          # ADDED BY CEARA
          rf_pin0.low()
          rf_pin1.low()
          # END OF ADDED BY CEARA
          rf_pin2.high()
          rf_pin3.high()
          # print("Stop")
     elif option == 13:
          rf_pin0.high()
          rf_pin2.high()
          rf_pin3.high()
     elif option == 14:
          rf_pin1.high()
          rf_pin2.high()
          rf_pin3.high()
     elif option == 15: # Stop
          rf_pin0.high()
          rf_pin1.high()
          rf_pin2.high()
          rf_pin3.high()
     else:
          return "Invalid value"
     time.sleep(0.2)

def setup_buttons():
   """Configure the pin modes for buttons."""
   seesaw_device.pin_mode_bulk(BUTTONS_MASK, seesaw_device.INPUT_PULLUP)

def read_buttons():
   """Read and return the state of each button."""
   return seesaw_device.digital_read_bulk(BUTTONS_MASK)

def handle_button_press(button):
   """Toggle the corresponding LED state on button press."""
   button_states[button] = not button_states[button]
   if button == BUTTON_A:
        transmitter.transmit(device_addr,0x06) # Boost On
        rf_transmit(3)
   elif button == BUTTON_B:
        transmitter.transmit(device_addr,0x07) # Boost Off
        rf_transmit(5)
   elif button == BUTTON_X:
        transmitter.transmit(device_addr,0x05) # Motors OFF
        rf_transmit(6)
   elif button == BUTTON_Y:
        transmitter.transmit(device_addr,0x05) # Motors OFF
        rf_transmit(12)
   print("Button", button, "is pressed")

def main():
   """Main program loop."""
   global last_buttons  # Ensure last_buttons is recognized as a global variable

   setup_buttons()

   last_x, last_y = seesaw_device.analog_read(JOYSTICK_X_PIN), seesaw_device.analog_read(JOYSTICK_Y_PIN)
   joystick_threshold = 50  # Adjust threshold as needed

   while True:
      current_buttons = read_buttons()
      rf_pin0.low()
      rf_pin1.low()
      rf_pin2.low()
      rf_pin3.low()

      # Check if button state has changed
      for button in button_states:
         if current_buttons & (1 << button) and not last_buttons & (1 << button):
               handle_button_press(button)

       # Read joystick values
      current_x = seesaw_device.analog_read(JOYSTICK_X_PIN)
      current_y = seesaw_device.analog_read(JOYSTICK_Y_PIN)

      # Check if joystick position has changed significantly
      if ((current_x == 0 ) and (current_y == 0)):
          transmitter.transmit(device_addr,0x05)
      if abs(current_x - last_x) > joystick_threshold or abs(current_y - last_y) > joystick_threshold:
           print("Joystick moved - X:", current_x, ", Y:", current_y)
           last_x, last_y = current_x, current_y

           # Determine which direction to move based off joystick
           if current_y < joystick_center_y - joystick_threshold:    # Joystick moved up
                transmitter.transmit(device_addr,0x01)
                rf_transmit(1)
           elif current_y > joystick_center_y + joystick_threshold:  # Joystick moved down
                transmitter.transmit(device_addr,0x02)
                rf_transmit(2)
           elif current_x < joystick_center_x - joystick_threshold:  # Joystick moved left
                transmitter.transmit(device_addr,0x04)
                rf_transmit(4)
           elif current_x > joystick_center_x + joystick_threshold:  # Joystick moved right
                transmitter.transmit(device_addr,0x03)
                rf_transmit(8)
           else:
                transmitter.transmit(device_addr,0x05)
                rf_transmit(6)

      last_buttons = current_buttons
      time.sleep(0.1)  # Delay to prevent overwhelming the output

if __name__ == "__main__":
   main()
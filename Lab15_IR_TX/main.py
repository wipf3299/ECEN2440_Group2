import machine
from machine import I2C, Pin
import seesaw
import time
import seesaw
import ir_tx
from ir_tx.nec import NEC

# Initialize I2C. Adjust pin numbers based on your Pico's configuration
i2c = I2C(0, scl=Pin(17), sda=Pin(16))

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
        transmitter.transmit(device_addr,0x01) # Forward
   elif button == BUTTON_B:
        transmitter.transmit(device_addr,0x02) # Backwards
   elif button == BUTTON_X:
        transmitter.transmit(device_addr,0x05) # Motors OFF
   elif button == BUTTON_Y:
        transmitter.transmit(device_addr,0x05) # Motors OFF
   print("Button", button, "is pressed")

def main():
   """Main program loop."""
   global last_buttons  # Ensure last_buttons is recognized as a global variable

   setup_buttons()

   last_x, last_y = seesaw_device.analog_read(JOYSTICK_X_PIN), seesaw_device.analog_read(JOYSTICK_Y_PIN)
   joystick_threshold = 50  # Adjust threshold as needed

   while True:
      current_buttons = read_buttons()

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
           elif current_y > joystick_center_y + joystick_threshold:  # Joystick moved down
                transmitter.transmit(device_addr,0x02)
           elif current_x < joystick_center_x - joystick_threshold:  # Joystick moved left
                transmitter.transmit(device_addr,0x04)
           elif current_x > joystick_center_x + joystick_threshold:  # Joystick moved right
                transmitter.transmit(device_addr,0x03)
           else
                transmitter.transmit(device_addr,0x05)

      last_buttons = current_buttons
      time.sleep(0.1)  # Delay to prevent overwhelming the output

if __name__ == "__main__":
   main()

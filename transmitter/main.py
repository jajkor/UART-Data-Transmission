from machine import Pin, Timer
from huffman_coding import *
from nrf import *
import time
import utime

# Initialize pins
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
led = Pin("LED", Pin.OUT)  # Onboard LED
button = Pin(21, Pin.IN, Pin.PULL_DOWN)
send_button = Pin(13, Pin.IN, Pin.PULL_DOWN)
timer = Timer()

debounce_time = 300  # debounce time in milliseconds
last_press = 0
last_press_send = 0

# String to store readings
readings = ""

# Function to take a reading from the sensor
def ultra():
    # pull trigger low to make sure its not active then sleep for 2ms
    trigger.low()
    utime.sleep_us(2)
  
    #pull trigger pin high for 5 seconds then stop(sends a pulse)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
  
    # if no pulse recieved update signal off with time stamp
    while echo.value() == 0:
        #print("Waiting for echo start...")
        signaloff = utime.ticks_us()
      
    # if pulse is recieved update signalon with time stamp
    while echo.value() == 1:
        signalon = utime.ticks_us()
      
    # time for the pulse to be sent and received
    timepassed = signalon - signaloff
    # time multiplied by speed of sound in ms divided by two since time passed is both sending and receiving time
    distance = (timepassed * 0.0343) / 2
    return distance

# Function to collect data when the button is pressed
def collect_data():
    # makes sure the readings variable is global to update outside the function
    global readings
    start_time = utime.ticks_ms()
    
    if readings:
        readings += ','
    
    #loop to take readings for 5 seconds  **used chatGPT to get this to work correctly
    while utime.ticks_diff(utime.ticks_ms(), start_time) < 1000:
        distance = ultra()
        # Append distance only with f string rounded to 2 decimal places followed by comma
        readings += f"{distance:.2f},"
        # led blinks every 400 ms
        timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)
        # Take a reading every second
        utime.sleep(1)
    
    # stop the led blinking
    timer.deinit()
    led.value(0)
    
    # Remove the last comma
    readings = readings.rstrip(",")  
    print("Readings collected:", readings)
    led.value(1)

# Function that toggles the led for when sensor is taking readings
def blink(timer):
    led.toggle()
    
def handle_button_press(pin):
    global last_press
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_press) > debounce_time:
        last_press = current_time  # Update the last press time
        print('Collecting data...')
        collect_data()
        
def handle_button_press_send(pin):
    global last_press_send
    global readings
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_press_send) > debounce_time:
        last_press_send = current_time  # Update the last press time
        print("Sending data...")
        encoded_message = encode(readings)
        nrf.sendMessage(encoded_message)
        print("Sent Message")
        print(f"\tMessage = {readings}")
        print(f"\tEncoded = {encoded_message}")
        readings = ''
        led.value(0)

button.irq(trigger=Pin.IRQ_RISING, handler=handle_button_press)
send_button.irq(trigger=Pin.IRQ_RISING, handler=handle_button_press_send)

# Main loop
if __name__ == '__main__':
    print("Waiting for button press...")
    while True:
        time.sleep(0.1)
        
        
# sources
# chatGPT for readings loop
# https://projects.raspberrypi.org/en/projects/introduction-to-the-pico/10    for button
# https://www.tomshardware.com/how-to/raspberry-pi-pico-ultrasonic-sensor     for ultrasonic sensor code


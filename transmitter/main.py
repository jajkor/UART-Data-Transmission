from machine import Pin, Timer
import utime

# Initialize pins
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
led = Pin("LED", Pin.OUT)  # Onboard LED
button = Pin(18, Pin.IN, Pin.PULL_UP)  # Button with pull-up resistor
timer = Timer()

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
    # Clear previous readings
    readings = ""  
    start_time = utime.ticks_ms()
    
    #loop to take readings for 5 seconds  **used chatGPT to get this to work correctly
    while utime.ticks_diff(utime.ticks_ms(), start_time) < 5000:  
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

# Function that toggles the led for when sensor is taking readings
def blink(timer):
    led.toggle()

# Main loop
if __name__ == '__main__':
    print("Waiting for button press...")
    while True:
        # Button is pressed (active low)
        if button.value() == 0:  
            print("Button pressed, starting data collection...")
            collect_data()
            print("Data collection complete. Waiting for next button press.")

        
        
# sources
# chatGPT for readings loop
# https://projects.raspberrypi.org/en/projects/introduction-to-the-pico/10    for button
# https://www.tomshardware.com/how-to/raspberry-pi-pico-ultrasonic-sensor     for ultrasonic sensor code


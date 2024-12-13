from machine import UART, Pin, PWM
from lcd import LCD
from huffman_coding import *
import time

debounce_time = 300  # debounce time in milliseconds
last_press = 0

current_index = 0
prev_index = 1

# Initialize UART0 for communication
uart = UART(0)  # UART0 uses GPIO 0 (TX) and GPIO 1 (RX) by default
uart.init(baudrate=9600, bits=8, parity=None, stop=1)  # Configure UART parameters

lcd = LCD(28, 27, 26, 22, 21, 20, 19, 18, 17, 16)

# Handle button press in a functional way
def handle_left_button_press(pin):
    global last_press
    global current_index
    global prev_index
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_press) > debounce_time:
        last_press = current_time  # Update the last press time
        print("Left Button Pressed!")
        if current_index > 0:
            prev_index = current_index
            current_index = (current_index - 1)  # Move to the next number

# Handle button press in a functional way
def handle_right_button_press(pin):
    global last_press
    global current_index
    global prev_index
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_press) > debounce_time:
        last_press = current_time  # Update the last press time
        print("Right Button Pressed!")
        if prev_index < (len(numbers) - 1):
            current_index = prev_index
            prev_index = (prev_index + 1)  # Move to the next number

    
if __name__ == '__main__':
    # Set up the button with IRQ
    button_pin0 = Pin(12, Pin.IN, Pin.PULL_DOWN)
    button_pin2 = Pin(13, Pin.IN, Pin.PULL_DOWN)

    button_pin0.irq(trigger=Pin.IRQ_RISING, handler=handle_left_button_press)
    button_pin2.irq(trigger=Pin.IRQ_RISING, handler=handle_right_button_press)
    
    lcd = LCD(28, 27, 26, 22, 21, 20, 19, 18, 15, 16)
    
    numbers = []
    lcd.lcd_clear()
    lcd.lcd_print("Waiting for data", 0)
    while True:        
        if uart.any():  # Check if data is available
            message = uart.read().decode('utf-8').strip()  # Read and decode the message
            try:
                decompressed_message = decode(message)
                numbers = []
                numbers = decompressed_message.split(',')
                print(f"Received: {numbers}")
                lcd.lcd_clear()
            except:
                print("Decompression Error")
            
        if len(numbers) != 0:
            lcd.lcd_print(f"{numbers[current_index]}", 0)
            lcd.lcd_print(f"{numbers[prev_index]}", 1)


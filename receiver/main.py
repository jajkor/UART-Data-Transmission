from machine import Pin, PWM

from lcd import LCD
import time

debounce_time = 300  # debounce time in milliseconds
last_press = 0

# Handle button press in a functional way
def handle_button_press(pin):
    global last_press
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_press) > debounce_time:
        last_press = current_time  # Update the last press time
        print("Button Pressed!")

smiley = [
    0b00000,
    0b01010,
    0b01010,
    0b00000,
    0b10001,
    0b01010,
    0b00100,
    0b00000
    ]
    
if __name__ == '__main__':
    # Set up the button with IRQ
    button_pin0 = Pin(15, Pin.IN, Pin.PULL_DOWN)
    button_pin1 = Pin(13, Pin.IN, Pin.PULL_DOWN)
    button_pin2 = Pin(14, Pin.IN, Pin.PULL_DOWN)

    button_pin0.irq(trigger=Pin.IRQ_RISING, handler=handle_button_press)
    button_pin1.irq(trigger=Pin.IRQ_RISING, handler=handle_button_press)
    button_pin2.irq(trigger=Pin.IRQ_RISING, handler=handle_button_press)
    
    lcd = LCD(28, 27, 26, 22, 21, 20, 19, 18, 17, 16)
    
    lcd.create_custom_char(0, smiley)

    # Display the custom character
    lcd.lcd_set_cursor(0, 0)
    lcd.lcd_print_custom(0)  # Will print the smiley face on the LCD

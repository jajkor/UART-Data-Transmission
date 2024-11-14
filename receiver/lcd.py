from machine import Pin
import time

class LCD(object):
    def __init__(self, rs, e, d0, d1, d2, d3, d4, d5, d6, d7):
        self.RS = Pin(rs, Pin.OUT)
        self.E = Pin(e, Pin.OUT)
        self.D0 = Pin(d0, Pin.OUT)
        self.D1 = Pin(d1, Pin.OUT)
        self.D2 = Pin(d2, Pin.OUT)
        self.D3 = Pin(d3, Pin.OUT)
        self.D4 = Pin(d4, Pin.OUT)
        self.D5 = Pin(d5, Pin.OUT)
        self.D6 = Pin(d6, Pin.OUT)
        self.D7 = Pin(d7, Pin.OUT)
        self.initialize()
    
    def initialize(self):
        #self.RS.value(0)  # Write mode
        
        time.sleep(0.05)  # Wait for 50 ms after power on
        
        # Function Set: 8-bit, 2-line, 5x8 font
        self.lcd_command(0x38)
        time.sleep(0.0045)  # Wait for 4.5 ms
        
        # Display ON/OFF Control: Display ON, Cursor OFF, Blink OFF
        self.lcd_command(0x0C)
        
        # Clear Display
        self.lcd_command(0x01)
        time.sleep(0.002)  # Wait for 2 ms
        
        # Entry Mode Set: Increment cursor, no shift
        self.lcd_command(0x06)
        
    # Function to toggle the enable pin
    def lcd_toggle_enable(self):
        self.E.value(1)
        time.sleep(0.0005)  # Enable pulse must be > 450 ns
        self.E.value(0)
        time.sleep(0.0005)  # Commands need > 37 us to settle

    def lcd_send_byte_8bit(self, byte):
        self.D0.value(byte & 0x01)
        self.D1.value((byte >> 1) & 0x01)
        self.D2.value((byte >> 2) & 0x01)
        self.D3.value((byte >> 3) & 0x01)
        self.D4.value((byte >> 4) & 0x01)
        self.D5.value((byte >> 5) & 0x01)
        self.D6.value((byte >> 6) & 0x01)
        self.D7.value((byte >> 7))
        self.lcd_toggle_enable()

    # Send a command to the LCD
    def lcd_command(self, cmd):
        self.RS.value(0)  # RS = 0 -> Command mode
        self.lcd_send_byte_8bit(cmd)
        
    # Write data to the LCD
    def lcd_write(self, char):
        self.RS.value(1)
        self.lcd_send_byte_8bit(char)

    # Clear the LCD screen
    def lcd_clear(self):
        self.lcd_command(0x01)  # Clear display
        time.sleep(0.005)

    # Set cursor position
    def lcd_set_cursor(self, line, position):
        if line == 0:
            self.lcd_command(0x80 + position)
        elif line == 1:
            self.lcd_command(0xC0 + position)

    # Display a string on the LCD
    def lcd_print(self, text, line=0):
        self.lcd_set_cursor(line, 0)
        for char in text:
            self.lcd_write_char(char)

    # Define custom character in CGRAM
    def create_custom_char(self, location, char_map):
        location &= 0x07  # Ensure location is within 0-7
        self.lcd_command(0x40 | (location << 3))  # Set CGRAM address
        for i in range(8):
            self.lcd_write(char_map[i])  # Write the custom char row data

    # Display the custom character
    def lcd_print_custom(self, location):
        self.lcd_write(location)  # Send location code to print custom character


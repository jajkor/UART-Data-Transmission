from machine import Pin
import time

class LCD:
    def __init__(self, rs, e, d0, d1, d2, d3, d4, d5, d6, d7):
        # Initialize pins
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
        
        # Initialize LCD
        self.initialize()

    def initialize(self):
        """Initializes the LCD in 8-bit mode."""
        time.sleep(0.05)  # Wait for power-on reset
        self.command(0x38)  # Function Set: 8-bit, 2-line, 5x8 dots
        time.sleep(0.0045)
        self.command(0x0C)  # Display ON/OFF Control: Display ON, Cursor OFF
        self.command(0x01)  # Clear Display
        time.sleep(0.002)
        self.command(0x06)  # Entry Mode Set: Increment cursor, no shift

    def toggle_enable(self):
        """Toggles the enable pin to latch data."""
        self.E.value(1)
        time.sleep(0.0005)
        self.E.value(0)
        time.sleep(0.0005)

    def send_byte(self, data):
        """Sends a byte to the LCD in 8-bit mode."""
        self.D0.value(data & 0x01)
        self.D1.value((data >> 1) & 0x01)
        self.D2.value((data >> 2) & 0x01)
        self.D3.value((data >> 3) & 0x01)
        self.D4.value((data >> 4) & 0x01)
        self.D5.value((data >> 5) & 0x01)
        self.D6.value((data >> 6) & 0x01)
        self.D7.value((data >> 7) & 0x01)
        self.toggle_enable()

    def command(self, cmd):
        """Sends a command to the LCD."""
        self.RS.value(0)  # Command mode
        self.send_byte(cmd)

    def write(self, char):
        """Writes a single character to the LCD."""
        if isinstance(char, str):
            char = ord(char)  # Convert char to ASCII if it's a string
        self.RS.value(1)  # Data mode
        self.send_byte(char)

    def lcd_clear(self):
        """Clears the LCD screen."""
        self.command(0x01)  # Clear display
        time.sleep(0.002)

    def set_cursor(self, line, position):
        """Sets the cursor to a specific position on the LCD."""
        if line == 0:
            self.command(0x80 + position)  # Line 1 address
        elif line == 1:
            self.command(0xC0 + position)  # Line 2 address

    def lcd_print(self, text, line=0):
        """Prints a string to the LCD at a specific line."""
        self.set_cursor(line, 0)  # Start at the beginning of the line
        for char in text:
            self.write(char)


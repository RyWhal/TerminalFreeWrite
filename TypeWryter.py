import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2  # Adjust based on specific model
import datetime
from pynput import keyboard
import os
import time
from datetime import datetime
from threading import Thread, Event


# Global variables
last_keypress_time = None
refresh_display = True

class TypeWryting:
    def __init__(self, buffer_size):
        
        # initialize the eink Display
        self.init_display()

        # Typing & text buffer
        self.buffer = []
        self.buffer_size = buffer_size
        self.current_line = ""  # Current line being edited
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)
        self.max_lines = self.epd.width // 24  # Calculate max lines based on font size
        self.line_length = 30  # Adjust line length based on display size and font

        #initialize the drawn image
        self.image = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255: clear the frame
        self.draw = ImageDraw.Draw(self.image)

        #Threading
        self.refresh_event = Event()
        self.refresh_thread = Thread(target=self.refresh_display)
        self.refresh_thread.start()
        
        # File mgmt
        self.filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.txt")
        self.folder_name = "TypeWrytes"
        self.create_save_folder(self.folder_name)

    def init_display(self):
        self.epd = epd4in2_V2.EPD()
        self.epd.init()
        self.epd.Clear()
    
    def on_key_press(self, key):
        try:
            if key == keyboard.Key.enter:
                self.add_text(self.current_line)
                self.current_line = ""
                self.save_content()
            elif key == keyboard.Key.backspace:
                self.current_line = self.current_line[:-1]
            elif hasattr(key, 'char') and key.char:
                self.current_line += key.char
                if len(self.current_line) >= self.line_length:
                    self.add_text(self.current_line)
                    self.current_line = ""
        except AttributeError:
            pass  # Ignore special keys that don't represent characters

        self.last_keypress_time = time.time()  # Update the time of the last keypress
        self.refresh_event.set()  # Signal to resume refreshing

    def refresh_display(self):
        while True:
            if time.time() - self.last_keypress_time < 6:
                self.draw.rectangle((0, 0, self.epd.height, self.epd.width), fill=255)
                for i, line in enumerate(self.buffer[-self.max_lines:]):
                    self.draw.text((0, i * 24), line, font=self.font, fill=0)
                self.epd.display(self.epd.getbuffer(self.image))
            else:
                self.refresh_event.wait()  # Wait for the next keypress event
                self.refresh_event.clear()
            time.sleep(0.1)

    def start_refresh_check(self):
        self.refresh_thread.start()
        # Start key listener, and on each keypress, call self.on_key_press

    def start_key_listener(self):
        listener = keyboard.Listener(on_press=self.on_key_press)
        listener.start()

    def create_save_folder(self):
        if not os.path.exists(self.folder_name):
            # Create the folder
            os.makedirs(self.folder_name)
            print(f"Folder '{self.folder_name}' created.")
        else:
            print(f"Folder '{self.folder_name}' already exists.")

    def add_text(self, text):
        self.buffer.append(text)
        if len(self.buffer) > self.max_lines:
            self.buffer.pop(0)  # Remove the oldest line for scrolling
        self.refresh_display()

    def get_user_input(self):
        current_line = ""
        with keyboard.Listener(on_press=lambda key: self.on_key_press(key, current_line)) as listener:
            listener.join()

    def save_content(self):
        with open(self.filename, "w") as file:
            file.write('\n'.join(self.buffer))

    def main_app_loop(self):
        self.init_display()
        self.start_key_listener()
        self.start_refresh_check()

        try:
            while True:
                time.sleep(1)  # This sleep prevents the loop from consuming too much CPU.
        except KeyboardInterrupt:
            # Graceful shutdown on Ctrl+C
            print("Exiting program...")
            self.save_content()
            self.epd.sleep()
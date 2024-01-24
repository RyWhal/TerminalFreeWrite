from waveshare_epd import epd4in2_V2,epd2in9_V2
from PIL import Image, ImageDraw, ImageFont
import keyboard
import time

class display_menu:
    def __init__(self):
        self.epd = epd2in9_V2.EPD()
        self.epd.init()
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 11)
        self.menu_options = ["New Type Wrytes", "Continue Type Wryte", "Settings", "Manual"]
        self.selected_index = 0
        

        #Initialize display-related variables)
        self.image = Image.new('1', (self.epd.width, self.epd.height), 255)
        self.draw = ImageDraw.Draw(self.image)

    def update_buffer(self):
        #generate display buffer for display
        partial_buffer = self.epd.getbuffer(self.image)
        self.epd.display(partial_buffer)

    
    def draw_menu(self):
        self.draw.rectangle((0, 0, 400, 300), fill=255)
        self.draw.text((10, 30), "Does this work?", font=self.font, fill=0)
        self.update_buffer()
        '''
        # Create the image
        # Clear the main display area -- also clears input line (270-300)
        self.draw.rectangle((0, 0, 400, 300), fill=255)

        for i, option in enumerate(self.menu_options):
            prefix = "> " if i == self.selected_index else "  "
            self.draw.text((10, 10 + i * 30), prefix + option, font=self.font, fill=0)
        
        self.update_buffer()
        '''
    
    def navigate_menu(self):
        while True:
            self.draw_menu()
            if keyboard.is_pressed('up') or keyboard.is_pressed('w'):
                print("Up or W pressed")
                self.selected_index = max(self.selected_index - 1, 0)
            elif keyboard.is_pressed('down') or keyboard.is_pressed('s'):
                print("down or S pressed")
                self.selected_index = min(self.selected_index + 1, len(self.menu_options) - 1)
            elif keyboard.is_pressed('enter'):
                print("Enter")
                self.epd.sleep()
                break

    def cleanup(self):
        self.epd.sleep()
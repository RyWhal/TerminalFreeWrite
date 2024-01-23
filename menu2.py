from waveshare_epd import epd4in2_V2
from PIL import Image, ImageDraw, ImageFont
import keyboard

class display_menu:
    def __init__(self):
        self.epd = epd4in2_V2.EPD()
        self.epd.init()
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
        self.menu_options = ["New Type Wryte", "Continue Type Wryte", "Settings", "Manual"]
        self.selected_index = 0
        #self.epd.TurnOnDisplay_Fast()

    def draw_menu(self):
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        for i, option in enumerate(self.menu_options):
            prefix = "> " if i == self.selected_index else "  "
            draw.text((10, 10 + i * 30), prefix + option, font=self.font, fill=0)
        self.epd.display_Partial(self.epd.getbuffer(image))

    def navigate_menu(self):
        while True:
            self.draw_menu()
            if keyboard.is_pressed('up') or keyboard.is_pressed('w'):
                print("Up or W pressed")
                self.selected_index = max(self.selected_index - 1, 0)
            elif keyboard.is_pressed('down') or keyboard.is_pressed('s'):
                print("down or S pressed")
                self.selected_index = min(self.selected_index + 1, len(self.menu_options) - 1)
                print("Enter")
            elif keyboard.is_pressed('enter'):
                break

    def cleanup(self):
        self.epd.sleep()
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2  # Adjust based on your specific Waveshare model
import keyboard
import time
import logging


logging.basicConfig(level=logging.DEBUG)

class main_menu:
    def __init__(self):
        self.font20 = ImageFont.truetype('Courier Prime.ttf', 20)

        # Initialize vars
        self.title = "title"
        self.option = "option"
        self.selected_index = 0
        self.current_selection = 0
        self.previous_selection = 0
        self.prev_image = None

        self.main_menu_options = ["New freewrite", "Continue a freewrite", "Settings", "TypeWryter Manual"]
        self.menu_length = len(self.main_menu_options)

    def init_display(self):
        logging.info("init screen")
        #initialize and clear display
        self.epd = epd4in2_V2.EPD()
        self.epd.init_fast(self.epd.Seconds_1_5S)
        self.epd.Clear()
        return self.epd 

    def init_menu_image(self):
        self.draw_image = Image.new('1', (self.epd.width, self.epd.height), 255)  # 255: clear the frame
        self.draw = ImageDraw.Draw(self.draw_image)
        return self.draw,self.draw_image

    def get_keyboard_input(self,e):
        #global current_selection, main_menu_options
        if e.name == 'up': 
            self.current_selection = (self.current_selection - 1) % self.menu_length
        elif e.name == 'down':
            self.current_selection = (self.current_selection + 1) % self.menu_length
        elif e.name == 'enter':
            self.trigger_function_based_on_selection()
        elif e.name == 'esc':
            #cleanup(epd)
            pass

    def display_full_menu(self,epd,draw,draw_image):
        logging.info("Display initial menu")
        self.padding = 20  # Adjust padding as needed
        for i, self.option in enumerate(self.main_menu_options):
            self.draw.text((self.padding, 1 + 30 * i), self.option, font=self.font20, fill=0)
        self.epd.display(self.epd.getbuffer(self.draw_image))

    def update_menu(self, epd, draw, draw_image):
        logging.info("update menu")
        #global current_selection, previous_selection

        #current y-axis
        self.y_current = 1 + 30 * self.current_selection

        # Clear the area where the indicators are displayed
        self.draw.rectangle((1,1,20,300), fill=255)

        # Draw the indicator only for the current selection
        self.draw.text((1, self.y_current), ">", font=self.font20, fill=0)

        #partial update screen
        self.epd.display_Partial(self.epd.getbuffer(self.draw_image))

        self.previous_selection = self.current_selection

    # Function to be called based on the selection
    def trigger_function_based_on_selection(self):
        logging.info("choose function")
        #global current_selection
        if self.current_selection == 0:
            logging.info("trigger text display")
            #main_loop()
        elif self.current_selection == 1:
            # Trigger function for "Continue a freewrite"
            print ("option 2")
            pass
        # ... and so on for other options

    #cleanup e-ink screen and turn it to sleep
    def cleanup(self):
        # Cleanup and sleep
        self.epd.init()
        self.epd.Clear()
        self.epd.sleep()

    # Initialize and run the app
    def loop(self):
        #initialize e-ink screen
        self.epd = self.init_display()
        self.draw,self.draw_image = self.init_menu_image()

        #draw menu to e-ink screen
        self.display_full_menu(self.draw, self.draw_image)

        # start keyboard listener and callback to get_input_text method
        keyboard.on_press(self.get_keyboard_input, suppress=True) #handles keyboard input

        # Main app loop
        while True:
            time.sleep(.1)
            self.update_menu()

    def run_main_menu(self):
        try:
            self.loop()
        except IOError as e:
            logging.info(e)
        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd4in2_V2.epdconfig.module_exit()
            exit()
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2  # Adjust based on your specific Waveshare model
import keyboard
import time


class base_menu:
    def __init__(self, title, options):
        # Initialize the E-ink display
        self.epd = epd4in2_V2.EPD()
        self.epd.init()
        self.epd.Clear()

        self.font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 13)
        
        # Initialize vars
        self.title = title
        self.options = options
        self.selected_index = 0
        self.current_selection = 0
        self.previous_selection = 0
        self.prev_image = None

        # Declare image
        self.image = Image.new('1', (self.epd.width, self.epd.height), 255)
        self.draw = ImageDraw.Draw(self.image)

    def display_full_menu(self):
        # Drawing the complete menu
        for i, option in enumerate(self.options):
            if i == self.current_selection:
                self.draw.text((10, 10 + 30 * i), "> " + option, font=self.font, fill=0)
            else:
                self.draw.text((10, 10 + 30 * i), "  " + option, font=self.font, fill=0)

        #self.partial_update_buffer(self.image)
        #self.epd.display(self.epd.getbuffer(self.image))
        self.full_update_buffer(self.image)

        self.prev_image = self.image.copy()  # Store a copy of the image

    def update_selection(self):
        # Create a partial image for updating the selection
        self.new_image = Image.new('1', (self.epd.width, 30), 255)
        self.new_draw = ImageDraw.Draw(self.new_image)

        # Redraw only current and previous selections
        for i in [self.current_selection, self.previous_selection]:
            y_position = 10 + 30 * i  # Calculate the y position based on the selection
            if i == self.current_selection:
                self.new_draw.text((10, y_position), "> " + self.options[i], font=self.font, fill=0)
            else:
                self.new_draw.text((10, y_position), "  " + self.options[i], font=self.font, fill=0)

        # Update the e-paper display with the new partial image
        #self.epd.display(self.epd.getbuffer(new_image))

        self.prev_image = self.new_image
        self.previous_selection = self.current_selection

        self.partial_update_buffer(self.new_image)

    def partial_update_buffer(self, update_image):
        #generate display buffer for display
        self.draw.rectangle((0, 0, self.epd.height, self.epd.width), fill=255)
        partial_buffer = self.epd.getbuffer(update_image)
        self.epd.display_Partial(partial_buffer)

    def full_update_buffer(self, update_image):
        #generate display buffer for display
        self.draw.rectangle((0, 0, self.epd.height, self.epd.width), fill=255)
        partial_buffer = self.epd.getbuffer(update_image)
        self.epd.display(partial_buffer)

    '''
    def find_update_area(self, current_image, new_image):
        """
        Find the area that needs to be updated on the e-ink display.
        :param current_image: Image currently displayed.
        :param new_image: New image to display.
        :return: Tuple of (x, y, width, height) for the update area.
        """
        min_x, min_y = new_image.size
        max_x = max_y = 0

        for x in range(new_image.width):
            for y in range(new_image.height):
                if current_image.getpixel((x, y)) != new_image.getpixel((x, y)):
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

        # Check if there are any changes
        if min_x > max_x or min_y > max_y:
            return None  # No update needed

        update_width = max_x - min_x + 1
        update_height = max_y - min_y + 1

        return min_x, min_y, update_width, update_height
        '''

    # Function to get keyboard input for menu navigation
    def get_user_input(self):
        while True:
            time.sleep(0.3)
            if keyboard.is_pressed('up arrow') or keyboard.is_pressed('w'):
                print("up arrow")
                self.current_selection = (self.current_selection - 1 + len(self.options)) % len(self.options)
                self.update_selection()
            elif keyboard.is_pressed('down arrow') or keyboard.is_pressed('s'):
                print("down arrow")
                self.current_selection = (self.current_selection + 1) % len(self.options)
                self.update_selection()
            elif keyboard.is_pressed('enter'):
                print("enter")
                self.epd.sleep()
                #return self.options[self.current_selection]


class main_menu(base_menu):
    def __init__(self):
        super().__init__("Main Menu", ["New freewrite", "Continue a freewrite", "Settings", "TypeWryter Manual"])
    
    def handle_user_input(user_input):
        if user_choice == "New freewrite":
            #self.new_freewrite()
            pass
        elif user_choice == "Continue a freewrite":
            #self.continue_freewrite()
            pass
        elif user_choice == "Settings":
            #self.settings()
            pass
        elif user_choice == "TypeWryter Manual":
            #self.manual()
            pass


    # Define methods for each menu option
    def new_freewrite(self):
        # Logic for creating a new freewrite
        pass

    def continue_freewrite(self):
        # Logic for continuing an existing freewrite
        pass

    def settings(self):
        # Logic for adjusting settings
        pass

    def manual(self):
        # Logic for displaying the manual
        pass 

class MenuManager:
    def __init__(self):
        self.current_menu = main_menu()

    def run(self):
        while True:
            self.current_menu.display_menu()
            user_input = self.current_menu.get_user_input()
            self.current_menu = self.current_menu.handle_user_input(user_input)

# Initialize and run the app
app = main_menu()
app.display_full_menu()
while True:
    user_choice = app.get_user_input()
    app.handle_user_input(user_choice)

import time
import keyboard
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V3
import os

class base_menu:
    def __init__(self, title, options):
        
        # Initialize the e-Paper display
        # clear refreshes whole screen, should be done on slow init()
        self.epd = epd4in2_V3.EPD()
        self.epd.init()
        self.epd.Clear()

        #Initialize display-related variables)
        self.image = Image.new('1', (self.epd.width,self.epd.height), 255)
        self.display_draw = ImageDraw.Draw(self.image)

        #Display settings like font size, spacing, etc.
        self.display_start_line = 0
        self.font24 = ImageFont.truetype('Courier Prime.ttf', 16) #24
        self.last_display_update = time.time()

        # Initialize vars
        self.current_selection = 0
        self.previous_selection = 0
        self.title = title
        self.options = options

        #file directory setup: "/data/cache.txt"
        self.file_path = os.path.join(os.path.dirname(__file__), 'data', 'cache.txt')

    def update_partial_buffer(self):
        # Generate the display buffer from the current image
        partial_buffer = self.epd.getbuffer(self.image)

        # Update the e-Paper display with the new buffer
        self.epd.display(partial_buffer)


    def display_full_menu(self):
        # Declare forst image of menu
        image = Image.new('1', (400, 300), 255)
        self.draw = ImageDraw.Draw(image)
        self.font = self.font24

        self.draw.rectangle((0, 0, self.epd.width, self.epd.height), fill=255)  # Clear the display
        self.draw.text((10, 10), self.title, font=self.font, fill=0)

        # Drawing the complete menu
        for i, option in enumerate(self.options):
            y_position = 40 + 30 * i
            if i == self.current_selection:
                self.draw.text((10, y_position), "> " + option, font=self.font, fill=0)
            else:
                self.draw.text((10, y_position), "  " + option, font=self.font, fill=0)

        self.update_display()

    def update_selection(self):
        # Create a partial image for updating the selection
        new_image = Image.new('1', (400, 30), 255)
        new_draw = ImageDraw.Draw(new_image)
        font = self.font24

        # Redraw only current and previous selections
        for i in [self.current_selection, self.previous_selection]:
            y_position = 10 + 30 * i  # Calculate the y position based on the selection
            if i == self.current_selection:
                new_draw.text((10, y_position), "> " + self.options[i], font=font, fill=0)
            else:
                new_draw.text((10, y_position), "  " + self.options[i], font=font, fill=0)

        self.previous_selection = self.current_selection
        self.update_display()

    # Function to get keyboard input for menu navigation
    def get_user_input(self):
        while True:
            time.sleep(0.1)
            if keyboard.is_pressed('up arrow') or keyboard.is_pressed('w'):
                self.current_selection = (self.current_selection - 1 + len(self.options)) % len(self.options)
                self.update_selection()
            elif keyboard.is_pressed('down arrow') or keyboard.is_pressed('s'):
                self.current_selection = (self.current_selection + 1) % len(self.options)
                self.update_selection()
            elif keyboard.is_pressed('enter'):
                return self.options[self.current_selection]


    def update_display(self):
        # Clear the main display area -- also clears input line (270-300)
        self.display_draw.rectangle((0, 0, 400, 300), fill=255)
        
        #update the partial buffer
        self.update_partial_buffer()

class main_menu(base_menu):
    def __init__(self):
        #initialize menu items
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

# Initialize and run the app
app = main_menu()
app.display_full_menu()
while True:
    user_choice = app.get_user_input()
    app.handle_user_input()
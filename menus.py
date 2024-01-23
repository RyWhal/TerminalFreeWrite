import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2  # Adjust based on your specific Waveshare model
import keyboard


class base_menu:
    def __init__(self, title, options):
        # Initialize the E-ink display
        self.epd = epd4in2_V2.EPD()
        self.epd.init()
        
        # Initialize vars
        self.current_selection = 0
        self.previous_selection = 0
        self.title = title
        self.options = options
        self.selected_index = 0
        self.prev_image = None

    def display_menu(self):
        # Declare forst image of menu
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)

        # Drawing the complete menu
        for i, option in enumerate(self.options):
            if i == self.current_selection:
                draw.text((10, 10 + 30 * i), "> " + option, font=font, fill=0)
            else:
                draw.text((10, 10 + 30 * i), "  " + option, font=font, fill=0)

        self.epd.display(self.epd.getbuffer(image))
        self.prev_image = image
        self.first_run = False

    def update_selection(self):
        # Partial image for updating selection
        new_image = Image.new('1', (self.epd.width, 30), 255)
        new_draw = ImageDraw.Draw(new_image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)

        # re-draw only current and previous selections
        for i in [self.current_selection, self.previous_selection]:
            if i == self.current_selection:
                new_draw.text((10, 0), "> " + self.options[i], font=font, fill=0)
            else:
                new_draw.text((10, 0), "  " + self.options[i], font=font, fill=0)

        update_area = self.find_update_area(self.prev_image, new_image)

        if update_area is not None:
            self.epd.displayPartial(self.epd.getbuffer(new_image.crop(update_area)), x=10, y=10 + 30 * self.current_selection)
        else:
            self.epd.display(self.epd.getbuffer(new_image))

        self.prev_image = new_image

        # Update previous selection for next iteration
        self.previous_selection = self.current_selection

    def find_update_area(current_image, new_image):
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

    # Function to get keyboard input for menu navigation
    def get_user_input(self):
        while True:
            if keyboard.is_pressed('up arrow') or keyboard.is_pressed('w'):
                self.current_selection = (self.current_selection - 1) % len(self.options)
                self.display_menu()
            elif keyboard.is_pressed('down arrow') or keyboard.is_pressed('s'):
                self.current_selection = (self.current_selection + 1) % len(self.options)
                self.display_menu()
            elif keyboard.is_pressed('enter'):
                return self.options[self.current_selection]

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

class settings_menu(base_menu):
    def __init__(self):
        super().__init__("Settings", ["", ""])
        # Further initialization

class file_menu(base_menu):
    def __init__(self):
        super().__init__("File_Manager", ["", ""])
        # Further initialization    


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
app.display_menu()
while True:
    user_choice = app.get_user_input()
    app.handle_user_input(user_choice)
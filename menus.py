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
        self.title = title
        self.options = options
        self.selected_index = 0

    def display_menu(self):
        # Display the main menu on the E-ink screen
        
        image = Image.new('1', (self.epd.width, self.epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
        
        # Draw each option on the screen
        for i, option in enumerate(self.options):
            if i == self.current_selection:
                draw.text((10, 10 + 30 * i), "> " + option, font=font, fill=0)
            else:
                draw.text((10, 10 + 30 * i), "  " + option, font=font, fill=0)

        self.epd.display(self.epd.getbuffer(image))

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
            self.new_freewrite()
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

import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2  # Adjust based on your specific Waveshare model

class TypeWryterApp:
    def __init__(self):
        # Initialize the E-ink display
        self.epd = epd4in2_V2.EPD()
        self.epd.init()
        self.options = ["New freewrite", "Continue a freewrite", "Settings", "TypeWryter Manual"]

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

    def handle_user_input(self):
        user_choice = self.get_user_input()
        if user_choice == "New freewrite":
            self.new_freewrite()
        elif user_choice == "Continue a freewrite":
            self.continue_freewrite()
        elif user_choice == "Settings":
            self.settings()
        elif user_choice == "TypeWryter Manual":
            self.manual()

# Initialize and run the app
app = TypeWryterApp()
app.display_menu()
while True:
    app.handle_user_input()

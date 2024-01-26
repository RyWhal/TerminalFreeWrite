import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2  # Adjust based on your specific Waveshare model
#import keyboard
import threading

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

        # init keyboard listener in a thread 
        self.input_thread = threading.Thread(target=self.get_user_input)
        self.input_thread.start()

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
        self.epd.display(self.epd.getbuffer(self.image))

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
        self.epd.display(self.epd.getbuffer(self.new_image))

        self.prev_image = self.new_image
        self.previous_selection = self.current_selection

    def on_key_press(self, key):
        try:
            key_char = key.char
        except AttributeError:
            print("key inpout error")
            key_char = key

        if key_char == keyboard.Key.up or key_char == 'w':
            print("up arrow")
            self.current_selection = (self.current_selection - 1 + len(self.options)) % len(self.options)
            self.update_selection()
        elif key_char == keyboard.Key.down or key_char == 's':
            print("down arrow")
            self.current_selection = (self.current_selection + 1) % len(self.options)
            self.update_selection()
        elif key_char == keyboard.Key.enter:
            print("enter")
            self.listener.stop()
            return self.options[self.current_selection]
        
    # Function to get keyboard input for menu navigation
    def get_user_input(self):
        # Keep the main thread alive while the listener thread is running
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()  # Wait for the listener to complete

    '''
    def get_user_input(self):
        while True:
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
                return self.options[self.current_selection]
        '''

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
app.get_user_input()

'''
while True:
    user_choice = app.get_user_input()
    app.handle_user_input(user_choice)
    '''
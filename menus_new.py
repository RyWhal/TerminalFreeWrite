import time
import keyboard
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V3
import signal
import os

class base_menu:
    def __init__(self, title, options):
        
        # Initialize the e-Paper display
        # clear refreshes whole screen, should be done on slow init()
        epd = epd4in2_V3.EPD()
        epd.init()
        epd.Clear()
        
        #init_display routine
        epd.init()
        epd.Clear
        #previous_lines = app.load_previous_lines(file_path)#('previous_lines.txt')
        epd.init_Partial()
        epd.Clear

        #Initialize display-related variables)
        display_image = Image.new('1', (epd.width,epd.height), 255)
        self.display_draw = ImageDraw.Draw(display_image)

        #Display settings like font size, spacing, etc.
        self.display_start_line = 0
        self.font24 = ImageFont.truetype('Courier Prime.ttf', 16) #24
        self.textWidth=16
        self.linespacing = 22
        chars_per_line = 32 #28
        self.lines_on_screen = 12
        self.last_display_update = time.time()

        #display related
        self.needs_display_update = True
        self.needs_input_update = True
        self.updating_input_area = False
        self.input_catchup = False
        self.display_catchup = False
        self.display_updating = False
        self.shift_active = False
        self.control_active = False
        self.exit_cleanup = False
        self.console_message = ""
        self.scrollindex=1

        # Initialize cursor position
        self.cursor_position = 0

        # Initialize text matrix (size of text file)
        self.max_lines = 100  # Maximum number of lines, adjust as needed
        self.max_chars_per_line = chars_per_line  # Maximum characters per line, adjust as needed
        self.text_content=""
        self.temp_content=""
        self.input_content=""
        self.previous_lines = []
        self.typing_last_time = time.time()  # Timestamp of last key press
        
        # Initialize vars
        self.current_selection = 0
        self.previous_selection = 0
        self.title = title
        self.options = options
        self.selected_index = 0
        self.prev_image = None

        #file directory setup: "/data/cache.txt"
        self.file_path = os.path.join(os.path.dirname(__file__), 'data', 'cache.txt')

    def display_full_menu(self):
        # Declare forst image of menu
        image = Image.new('1', (400, 300), 255)
        draw = ImageDraw.Draw(image)
        font = self.font24

        # Drawing the complete menu
        for i, option in enumerate(self.options):
            if i == self.current_selection:
                draw.text((10, 10 + 30 * i), "> " + option, font=font, fill=0)
                self.update_display()
            else:
                draw.text((10, 10 + 30 * i), "  " + option, font=font, fill=0)
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
                self.update_display()
            else:
                new_draw.text((10, y_position), "  " + self.options[i], font=font, fill=0)
                self.update_display()

        self.previous_selection = self.current_selection

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
        
        '''
        # Display the previous lines
        y_position = 270 - self.linespacing  # leaves room for cursor input

        #Make a temp array from previous_lines. And then reverse it and display as usual.
        current_line=max(0,len(previous_lines)-self.lines_on_screen*self.scrollindex)
        temp=previous_lines[current_line:current_line+self.lines_on_screen]
        print(temp)# to debug if you change the font parameters (size, chars per line, etc)

        for line in reversed(temp[-self.lines_on_screen:]):
        self.display_draw.text((10, y_position), line[:self.max_chars_per_line], font=self.font24, fill=0)
        y_position -= self.linespacing
        '''

        #Display Console Message
        if console_message != "":
            self.display_draw.rectangle((300, 270, 400, 300), fill=255)
            self.display_draw.text((300, 270), console_message, font=self.font24, fill=0)
            console_message = ""
        
        #generate display buffer for display
        partial_buffer = self.epd.getbuffer(self.display_image)
        self.epd.display(partial_buffer)

        self.last_display_update = time.time()
        self.display_updating= False
        self.needs_display_update = False

    def handle_interrupt(self):
        keyboard.unhook_all()
        self.epd.init()
        self.epd.Clear()
        exit(0)

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

#Startup Stuff ---
#keyboard.on_press(handle_key_down, suppress=False) #handles modifiers and shortcuts
#keyboard.on_release(handle_key_press, suppress=True)
#signal.signal(signal.SIGINT, handle_interrupt)




# Initialize and run the app
app = main_menu()
app.display_full_menu()
while True:
    user_choice = app.get_user_input()
    app.handle_user_input(user_choice)


#mainloop
'''
try:
    while True:
        
        if exit_cleanup:
            break
                
        if needs_display_update and not display_updating:
            update_display()
            needs_diplay_update=False
            typing_last_time = time.time()
            
        elif (time.time()-typing_last_time)<(.5): #if not doing a full refresh, do partials
            #the screen enters a high refresh mode when there has been keyboard input
            if not updating_input_area and scrollindex==1:
                #update_input_area()
        time.sleep(0.05) #the sleep here seems to help the processor handle things, especially on 64-bit installs
'''
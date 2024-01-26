import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2  # Adjust based on your specific Waveshare model
#import keyboard
import threading



font20 = ImageFont.truetype('Courier Prime.ttf', 20)

# Initialize vars
title = "title"
option = "option"
selected_index = 0
current_selection = 0
previous_selection = 0
prev_image = None

main_menu_options = ["New freewrite", "Continue a freewrite", "Settings", "TypeWryter Manual"]

def init_display():
    #initialize and clear display
    epd = epd4in2_V2.EPD()
    epd.init()
    epd.Clear()
    return epd 

def init__menu_image(epd):
    draw_image = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(draw_image)
    return draw,draw_image

def display_full_menu(draw,draw_image):
    # Drawing the complete menu
    for i,option in enumerate(main_menu_options):
        if i == current_selection:
            draw.text((1, 1 + 30 * i), "> " + option, font=font20, fill=0)
        else:
            draw.text((1, 1 + 30 * i), "  " + option, font=font, fill=0)
    
    epd.display(epd.getbuffer(draw_image))

def partial_update_text(epd, draw, draw_image, text_lines):
    #logging.info("partial_update_start")
    draw.rectangle((0, 0, 400, 300), fill = 255)
    epd.display_Partial(epd.getbuffer(draw_image))

def full_update_text(draw, draw_image,text, epd):
    #logging.info("full update")
    draw.rectangle((0, 0, 400, 300), fill = 255)
    draw.text((0, 0), text, font = font16, fill=0)
    epd.display(epd.getbuffer(draw_image))

''' def update_selection(:
        # Create a partial image for updating the selection
        new_image = Image.new('1', (epd.width, 30), 255)
        new_draw = ImageDraw.Draw(new_image)

        # Redraw only current and previous selections
        for i in [current_selection, previous_selection]:
            y_position = 10 + 30 * i  # Calculate the y position based on the selection
            if i == current_selection:
                new_draw.text((10, y_position), "> " + options[i], font=font, fill=0)
            else:
                new_draw.text((10, y_position), "  " + options[i], font=font, fill=0)

        # Update the e-paper display with the new partial image
        epd.display(epd.getbuffer(new_image))

        prev_image = new_image
        previous_selection = current_selection
'''
'''    def on_key_press( key):
        try:
            key_char = key.char
        except AttributeError:
            print("key inpout error")
            key_char = key

        if key_char == keyboard.Key.up or key_char == 'w':
            print("up arrow")
            current_selection = (current_selection - 1 + len(options)) % len(options)
            update_selection()
        elif key_char == keyboard.Key.down or key_char == 's':
            print("down arrow")
            current_selection = (current_selection + 1) % len(options)
            update_selection()
        elif key_char == keyboard.Key.enter:
            print("enter")
            listener.stop()
            return options[current_selection]'''
        
'''class main_menu(base_menu):
    def __init__(:
        super().__init__("Main Menu", ["New freewrite", "Continue a freewrite", "Settings", "TypeWryter Manual"])
    
    def handle_user_input(user_input):
        if user_choice == "New freewrite":
            #new_freewrite()
            pass
        elif user_choice == "Continue a freewrite":
            #continue_freewrite()
            pass
        elif user_choice == "Settings":
            #settings()
            pass
        elif user_choice == "TypeWryter Manual":
            #manual()
            pass'''

'''class MenuManager:
    def __init__(:
        current_menu = main_menu()

    def run(:
        while True:
            current_menu.display_menu()
            user_input = current_menu.get_user_input()
            current_menu = current_menu.handle_user_input(user_input)'''

# Initialize and run the app

epd = init_display()
draw,draw_image = init__menu_image(epd)
display_full_menu(draw,draw_image)

'''
while True:
    user_choice = app.get_user_input()
    app.handle_user_input(user_choice)
    '''
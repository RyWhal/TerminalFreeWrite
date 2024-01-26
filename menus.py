import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2  # Adjust based on your specific Waveshare model
import keyboard
import time
import logging


logging.basicConfig(level=logging.INFO)
font20 = ImageFont.truetype('Courier Prime.ttf', 20)

# Initialize vars
title = "title"
option = "option"
selected_index = 0
current_selection = 0
previous_selection = 0
prev_image = None

main_menu_options = ["New freewrite", "Continue a freewrite", "Settings", "TypeWryter Manual"]
menu_length = len(main_menu_options)

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

def get_keyboard_input(e, epd):
    global current_selection, main_menu_options
    if e.name == 'up': 
        if current_selection >= 0 and current_selection < menu_length:
            current_selection += 1
    elif e.name == 'down':

        if current_selection <= menu_length and current_selection > 0:
            current_selection -= 1
    elif e.name == 'enter':
        trigger_function_based_on_selection()
    elif e.name == 'esc':
        cleanup(epd)

def display_full_menu(epd,draw,draw_image):
    # Drawing the complete menu
    for i,option in enumerate(main_menu_options):
        if i == current_selection:
            draw.text((1, 1 + 30 * i), "> " + option, font=font20, fill=0)
        else:
            draw.text((1, 1 + 30 * i), "  " + option, font=font20, fill=0)
    epd.display(epd.getbuffer(draw_image))

def partial_update_menu(epd, draw, draw_image):
    global current_selection, previous_selection
    #logging.info("partial_update_start")
    draw.rectangle((0, 0, 400, 300), fill = 255)

    # Redraw the menu options with the updated selection
    for i, option in enumerate(main_menu_options):
        if i == current_selection:
            draw.text((1, 1 + 30 * i), "> " + option, font=font20, fill=0)
        elif i == previous_selection:
            draw.text((1, 1 + 30 * i), "  " + option, font=font20, fill=0)
    
    epd.display_Fast(epd.getbuffer(draw_image))
    previous_selection = current_selection

# Function to be called based on the selection
def trigger_function_based_on_selection():
    global current_selection
    if current_selection == 0:
        print("option 1")
        # Trigger function for "New freewrite"
        pass
    elif current_selection == 1:
        # Trigger function for "Continue a freewrite"
        print ("option 2")
        pass
    # ... and so on for other options

def cleanup(epd):
    # Cleanup and sleep
    epd.init()
    epd.Clear()
    epd.sleep()

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

# start keyboard listener and callback to get_input_text method
def main():
    epd = init_display()
    draw,draw_image = init__menu_image(epd)
    display_full_menu(epd,draw,draw_image)
    keyboard.on_press(get_keyboard_input, suppress=True) #handles keyboard input

    while True:
        time.sleep(.1)
        partial_update_menu(epd, draw, draw_image)

if __name__ == '__main__':
    try:
        main()
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd4in2_V2.epdconfig.module_exit()
        exit()
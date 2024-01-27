import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2  # Adjust based on your specific Waveshare model
import keyboard
import time
import logging
from text_display import main_loop


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
    epd.init_fast(epd.Seconds_1_5S)
    epd.Clear()
    return epd 

def init__menu_image(epd):
    draw_image = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(draw_image)
    return draw,draw_image

def get_keyboard_input(e):
    global current_selection, main_menu_options
    if e.name == 'up': 
        current_selection = (current_selection - 1) % menu_length
    elif e.name == 'down':
        current_selection = (current_selection + 1) % menu_length
    elif e.name == 'enter':
        trigger_function_based_on_selection()
    elif e.name == 'esc':
        #cleanup(epd)
        pass

def display_full_menu(epd,draw,draw_image):
    padding = 20  # Adjust padding as needed
    for i, option in enumerate(main_menu_options):
        draw.text((padding, 1 + 30 * i), option, font=font20, fill=0)
    epd.display(epd.getbuffer(draw_image))

def update_menu(epd, draw, draw_image):
    global current_selection, previous_selection
    
    # Calculate the y-coordinates for the previous and current selections
    y_prev = 1 + 30 * previous_selection
    y_current = 1 + 30 * current_selection

    # Clear the area where the previous and current indicators are displayed
    indicator_width = 15  # Width of the area to clear for the indicator
    draw.rectangle((1,1,20,300), fill=255)
    #draw.rectangle((0, y_current, indicator_width, y_current + 30), fill=255)

    # Draw the indicator only for the current selection
    draw.text((1, y_current), ">", font=font20, fill=0)

    #partial update
    epd.display_Partial(epd.getbuffer(draw_image))

    previous_selection = current_selection

# Function to be called based on the selection
def trigger_function_based_on_selection():
    global current_selection
    if current_selection == 0:
        main_loop()
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

# Initialize and run the app


def main():
    #initialize e-ink screen
    epd = init_display()
    draw,draw_image = init__menu_image(epd)

    #draw menu to e-ink screen
    display_full_menu(epd,draw,draw_image)

    # start keyboard listener and callback to get_input_text method
    keyboard.on_press(get_keyboard_input, suppress=True) #handles keyboard input

    # Main app loop
    while True:
        time.sleep(.1)
        update_menu(epd, draw, draw_image)

if __name__ == '__main__':
    try:
        main()
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd4in2_V2.epdconfig.module_exit()
        exit()
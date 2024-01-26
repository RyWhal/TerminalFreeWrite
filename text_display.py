#!/usr/bin/python
import os
import logging
from waveshare_epd import epd4in2_V2
from PIL import Image,ImageDraw,ImageFont
import keyboard
import time
import keymaps
from datetime import datetime


#initialize some vars
logging.basicConfig(level=logging.INFO)
font16 = ImageFont.truetype('Courier Prime.ttf', 16)

text_lines = [""]  # List of text lines
chars_per_line = 40
max_lines_on_screen = 15
current_line = 0
filename = datetime.now().strftime("Text_%Y%m%d_%H%M%S.txt")

def init_display():
    #initialize and clear display
    epd = epd4in2_V2.EPD()
    epd.init()
    epd.Clear()
    return epd 

def init_image(epd):
    draw_image = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(draw_image)
    return draw,draw_image

def save_text_to_file(text_lines, filename):
    # Saves the text to a file
    with open(filename, 'w') as file:
        file.write('\n'.join(text_lines))

def handle_key_down(e, shift_active, control_active): #keys being held, ie modifier keys
    if e.name == 'shift': #if shift is released
        shift_active = True
    if e.name == 'ctrl': #if shift is released
        control_active = True
    return shift_active,control_active

def get_text(e):
    global text_lines, current_line, filename
    shift_active = False
    control_active = False
    shift_active,control_active = handle_key_down(e, shift_active, control_active)
    if e.name == 'backspace':
        handle_backspace()
    elif e.name == 'delete' and control_active:
        handle_delete_word()
    elif e.name == 'delete' and shift_active:
        handle_delete_line()
    elif e.name == 'tab':
        char= '   '
    elif e.name == 'enter':
        current_line += 1
        save_text_to_file(text_lines, filename)
        if current_line >= len(text_lines):
            text_lines.append("")
    elif e.name == 'space':
            char = ' '
            if len(text_lines[current_line]) < chars_per_line:
                text_lines[current_line] += char
    elif len(e.name) == 1 and control_active == False:  # Regular character
        char = e.name
        logging.info("if len(e.name) shift_active: " + str(shift_active))
        if shift_active:
            logging.info("getting shift keymaps")
            logging.info("if shift_active: " + str(shift_active))
            char = keymaps.shift_mapping.get(e.name) 
        if len(text_lines[current_line]) < chars_per_line:
            text_lines[current_line] += char
            
    # Check and wrap to the next line if the current line is full
    if len(text_lines[current_line]) >= chars_per_line:
        current_line += 1
        if current_line >= len(text_lines):
            text_lines.append("")
    
    shift_active = False
    control_active = False
        

def handle_backspace():
    logging.info("handle backspace")
    global text_lines, current_line
    if len(text_lines[current_line]) > 0:
        text_lines[current_line] = text_lines[current_line][:-1]
    elif current_line > 0:
        current_line -= 1

def handle_delete_word():
    logging.info("handle_delete_word")
    global text_lines, current_line
    words = text_lines[current_line].split()
    if words:
        text_lines[current_line] = ' '.join(words[:-1])
    elif current_line > 0:
        current_line -= 1
    
def handle_delete_line():
    logging.info("handle_delete_line")
    global text_lines, current_line
    if current_line > 0:
        text_lines.pop(current_line)
        current_line -= 1

def partial_update_text(epd, draw, draw_image, text_lines):
    #logging.info("partial_update_start")
    draw.rectangle((0, 0, 400, 300), fill = 255)
    #draw.text((0, 0), text, font = font16, fill=0)
    #epd.display_Partial(epd.getbuffer(draw_image))

    # Draw text lines on the image
    for i, line in enumerate(text_lines[-max_lines_on_screen:]):
        draw.text((1, 1 + i * 20), line, font=font16, fill=0)
    
    epd.display_Partial(epd.getbuffer(draw_image))
    #logging.info("partial_update_complete")

def full_update_text(draw, draw_image,text, epd):
    #logging.info("full update")
    draw.rectangle((0, 0, 400, 300), fill = 255)
    draw.text((0, 0), text, font = font16, fill=0)
    epd.display(epd.getbuffer(draw_image))

def cleanup(epd):
    # Cleanup and sleep
    epd.init()
    epd.Clear()
    epd.sleep()


# start keyboard listener and callback to get_input_text method
def main():
    epd = init_display() #initialize the display one time. 
    draw, draw_image = init_image(epd)
    keyboard.on_press(get_text, suppress=True) #handles keyboard input
    keyboard.on_press(handle_key_down, suppress=True) 
    #keyboard.on_press(handle_key_up, suppress=True)

    while True:
        time.sleep(.1)
        partial_update_text(epd, draw, draw_image, text_lines)


if __name__ == '__main__':
    try:
        main()
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd4in2_V2.epdconfig.module_exit()
        exit()
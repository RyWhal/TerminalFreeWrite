#!/usr/bin/python
import os
import logging
from waveshare_epd import epd4in2_V2
from PIL import Image,ImageDraw,ImageFont
import keyboard
import time
import signal
import keymaps

#initialize some vars
logging.basicConfig(level=logging.INFO)
font18 = ImageFont.truetype('Courier Prime.ttf', 18)
text = " "
chars_per_line = 45
lines_on_screen = 25
current_line = 0
shift_active = False
control_active = False

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

def handle_key_down(e, shift_active, control_active): #keys being held, ie modifier keys
    if e.name == 'shift': #if shift is released
        shift_active = True
    if e.name == 'ctrl': #if shift is released
        control_active = True
    return shift_active,control_active

# Not currently working. This method is displaying some of the CLI for some reason. 
def get_input_text(e):
    global text
    global shift_active
    global control_active

    shift_active,control_active = handle_key_down(e,shift_active,control_active)
    
    if e.name == 'enter':
        logging.info("\nKey Pressed:" + e.name)
        e.name += '\n'
    elif e.name == 'backspace':
        logging.info("\nKey Pressed:" + e.name)
        text = text[:-1]
    elif e.name == 'space':
        text += ' '
    elif len(e.name) == 1 and control_active == False: 
        if shift_active:
            char = keymaps.shift_mapping.get(e.name)
            text += char
            shift_active = False
        else:
            text += e.name
    time.sleep(.05)
    

def partial_update_text(draw, draw_image,text, epd):
    logging.info("draw text")
    draw.rectangle((0, 0, 400, 300), fill = 255)
    draw.text((0, 0), text, font = font18, fill=0)
    epd.display_Partial(epd.getbuffer(draw_image))

def full_update_text(draw, draw_image,text, epd):
    logging.info("full update")
    draw.rectangle((0, 0, 400, 300), fill = 255)
    draw.text((0, 0), text, font = font18, fill=0)
    epd.display(epd.getbuffer(draw_image))

def cleanup(epd):
    # Cleanup and sleep
    epd.init()
    epd.Clear()
    epd.sleep()

# start keyboard listener and callback to get_input_text method

epd = init_display() #initialize the display one time. 
draw, draw_image = init_image(epd)
keyboard.on_press(get_input_text, suppress=True) #handles keyboard input

try:
    while True:
        time.sleep(.1)
        partial_update_text(draw, draw_image, text, epd)
    

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in2_V2.epdconfig.module_exit(cleanup=True)
    cleanup(epd) 
    exit()
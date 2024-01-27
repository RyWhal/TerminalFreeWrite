#!/usr/bin/python
import os
import logging
from waveshare_epd import epd4in2_V2
from PIL import Image,ImageDraw,ImageFont
import keyboard
import time
import keymaps
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class text_display:
    def __init__(self):
        #initialize some vars
        self.font16 = ImageFont.truetype('Courier Prime.ttf', 16)
        self.text_lines = [""]  # List of text lines
        self.chars_per_line = 40
        self.max_lines_on_screen = 15
        self.current_line = 0
        self.shift_active = False
        self.control_active = False
        self.filename = datetime.now().strftime("Text_%Y%m%d_%H%M%S.txt")

    def init_display(self):
        #initialize and clear display
        self.epd = epd4in2_V2.EPD()
        self.epd.init()
        self.epd.Clear()
        #return epd 

    def init_image(self):
        self.draw_image = Image.new('1', (400, 300), 255)  # 255: clear the frame
        self.draw = ImageDraw.Draw(self.draw_image)
        #return self.draw,self.draw_image

    def save_text_to_file(self, text_lines, filename):
        # Saves the text to a file
        with open(filename, 'w') as file:
            file.write('\n'.join(self.text_lines))

    def handle_key_down(self, e, shift_active, control_active): #keys being held, ie modifier keys
        if e.name == 'shift': #if shift is released
            self.shift_active = True
        if e.name == 'ctrl': #if shift is released
            self.control_active = True
        #return shift_active,control_active

    def get_text(self,e):
        #global text_lines, current_line, filename, shift_active, control_active

        #check shift key
        self.shift_active,self.control_active = self.handle_key_down(e, shift_active, self.control_active)

        # Actions for differet key combos
        if e.name == 'backspace':
            self.handle_backspace()
        elif e.name == 'backspace' and self.control_active:
            self.handle_delete_word()
        elif e.name == 'backspace' and shift_active:
            self.handle_delete_line()
        elif e.name == 'tab':
            self.char= '   '
        elif e.name == 'enter':
            self.current_line += 1
            self.save_text_to_file(self.text_lines, self.filename)
            if self.current_line >= len(self.text_lines):
                self.text_lines.append("")
        elif e.name == 'space':
                char = ' '
                if len(self.text_lines[self.current_line]) < self.chars_per_line:
                    self.text_lines[self.current_line] += char
        elif len(e.name) == 1 and self.control_active == False:  # Regular character input
            self.char = e.name
            logging.info("if len(e.name) shift_active: " + str(self.shift_active))
            if self.shift_active:
                self.char = keymaps.shift_mapping.get(e.name) 
                shift_active = False
            if len(self.text_lines[self.current_line]) < self.chars_per_line:
                self.text_lines[self.current_line] += char
        
        # Check and wrap to the next line if the current line is full
        if len(self.text_lines[self.current_line]) >= self.chars_per_line:
            self.current_line += 1
            if self.current_line >= len(self.text_lines):
                self.text_lines.append("")

        # Debounce
        time.sleep(.05)
        #control_active = False    

    def handle_backspace(self):
        logging.info("handle backspace")
        #global text_lines, current_line
        if len(self.text_lines[self.current_line]) > 0:
            self.text_lines[self.current_line] = self.text_lines[self.current_line][:-1]
        elif self.current_line > 0:
            self.current_line -= 1

    def handle_delete_word(self):
        logging.info("handle_delete_word")
        #global text_lines, current_line
        self.words = self.text_lines[self.current_line].split()
        if self.words:
            self.text_lines[self.current_line] = ' '.join(self.words[:-1])
        elif self.current_line > 0:
            self.current_line -= 1
        
    def handle_delete_line(self):
        logging.info("handle_delete_line")
        #global text_lines, current_line
        if self.current_line > 0:
            self.text_lines.pop(self.current_line)
            self.current_line -= 1

    def partial_update_text(self, epd, draw, draw_image, text_lines):
        #logging.info("partial_update_start")
        self.draw.rectangle((0, 0, 400, 300), fill = 255)

        # Draw text lines on the image
        for i, line in enumerate(self.text_lines[-self.max_lines_on_screen:]):
            draw.text((1, 1 + i * 20), line, font=self.font16, fill=0)
        
        self.epd.display_Partial(self.epd.getbuffer(self.draw_image))

    def full_update_text(self, draw, draw_image,text, epd):
        #logging.info("full update")
        self.draw.rectangle((0, 0, 400, 300), fill = 255)
        self.draw.text((0, 0), text, font = self.font16, fill=0)
        self.epd.display(self.epd.getbuffer(self.draw_image))

    def cleanup(self):
        # Cleanup and sleep
        self.epd.init()
        self.epd.Clear()
        self.epd.sleep()


    # start keyboard listener and callback to get_input_text method
    def loop(self):
        self.epd = self.init_display() #initialize the display one time. 
        self.draw, self.draw_image = self.init_image()
        keyboard.on_press(self.get_text, suppress=True) #handles keyboard input

        while True:
            time.sleep(.1)
            self.partial_update_text(self.epd, self.draw, self.draw_image, self.text_lines)


    def run(self):
        try:
            self.loop()
        except IOError as e:
            logging.info(e)
        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd4in2_V2.epdconfig.module_exit()
            exit()
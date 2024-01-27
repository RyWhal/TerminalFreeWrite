import time
import keyboard
import keymaps
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2

from TypeWryter import ZeroWriter


# Instantiate ZeroWriter with the default configuration
zero_writer = ZeroWriter()

try:
  zero_writer.epd = epd4in2_V2.EPD()
  zero_writer.keyboard = keyboard
  zero_writer.initialize()
  zero_writer.run()

except KeyboardInterrupt:
    pass

finally:
    keyboard.unhook_all()
    zero_writer.epd.init()
    time.sleep(1)
    zero_writer.epd.Clear()
    zero_writer.epd.sleep()

#from text_display import text_display
'''from main_menu import main_menu

def main():
    #app = text_display()
    #app.run_text_display()
    app = main_menu()
    app.run_main_menu()

if __name__ == "__main__":
    main()'''


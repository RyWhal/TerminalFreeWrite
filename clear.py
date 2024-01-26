#!/usr/bin/python
import logging
from waveshare_epd import epd4in2_V2
from PIL import ImageFont

logging.basicConfig(level=logging.INFO)
logging.info("set font object")
font18 = ImageFont.truetype('Font.ttc', 18)

def init_display():
    epd = epd4in2_V2.EPD()
    epd.init()
    epd.Clear()
    return epd

def cleanup(epd):
    # Cleanup and sleep
    epd.init()
    epd.Clear()
    epd.sleep()

try:
    epd = init_display()
    cleanup(epd)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd4in2_V2.epdconfig.module_exit(cleanup=True)
    exit()
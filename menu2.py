from waveshare_epd import epd4in2_V2
from PIL import Image, ImageDraw, ImageFont

def main_menu():
    epd = epd4in2_V3.EPD()  # create an EPD instance
    epd.init()  # initialize the display

    # Create an empty image to draw on
    image = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)

    # Set font size and type
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)

    # Menu options
    menu_options = ["New Type Wryte", "Continue Type Wryte", "Settings", "Manual"]
    spacing = 30  # Vertical spacing between menu options

    # Draw each menu option on the image
    for i, option in enumerate(menu_options):
        draw.text((10, 10 + i * spacing), option, font=font, fill=0)

    # Display the image on the e-ink screen
    epd.display(epd.getbuffer(image))
    epd.sleep()  # Put the display to sleep to prevent damage
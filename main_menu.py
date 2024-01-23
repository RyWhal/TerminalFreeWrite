import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2  # Adjust based on your specific Waveshare model

# Constants for GPIO pins (adjust these based on your setup)
BUTTON_UP = 5
BUTTON_DOWN = 6
BUTTON_SELECT = 13

# Initialize the e-ink display
epd = epd2in13_V2.EPD()
epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)

# Menu items and current selection
menu_items = ["New Freewrite", "Continue Freewrite", "Settings", "Help"]
current_selection = 0

def display_menu():
    # Create a blank image for drawing
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    
    # Define font (adjust path as needed)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)

    # Draw each menu item
    for i, item in enumerate(menu_items):
        if i == current_selection:
            draw.rectangle([(0, i*20), (epd.height, (i+1)*20)], fill=0)
            draw.text((10, i*20), item, font=font, fill=255)
        else:
            draw.text((10, i*20), item, font=font, fill=0)

    # Update the display with the new image
    epd.display(epd.getbuffer(image))

def button_callback(channel):
    global current_selection
    if channel == BUTTON_UP:
        current_selection = (current_selection - 1) % len(menu_items)
    elif channel == BUTTON_DOWN:
        current_selection = (current_selection + 1) % len(menu_items)
    elif channel == BUTTON_SELECT:
        execute_selected_item()
    display_menu()

def execute_selected_item():
    selected_item = menu_items[current_selection]
    print(f"Selected: {selected_item}")
    # Add functionality for each menu item here

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup([BUTTON_UP, BUTTON_DOWN, BUTTON_SELECT], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON_UP, GPIO.FALLING, callback=button_callback, bouncetime=200)
GPIO.add_event_detect(BUTTON_DOWN, GPIO.FALLING, callback=button_callback, bouncetime=200)
GPIO.add_event_detect(BUTTON_SELECT, GPIO.FALLING, callback=button_callback, bouncetime=200)

# Initial display
display_menu()

try:
    while True:
        # Keep the script running
        pass
except KeyboardInterrupt:
    print("Exiting application")
    GPIO.cleanup()
    epd.sleep()
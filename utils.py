import os
from datetime import datetime
import curses
import requests

def generate_filename():
    """
    Generates a timestamped filename.
    Format: 'YYYYMMDD_HHMMSS.txt'
    """
    
    return datetime.now().strftime("%Y%m%d_%H%M%S.txt")

def shutdown_device():
    """
    Placeholder for shutdown functionality.
    Replace with actual shutdown command for deployment.
    """
    pass  # Safe placeholder to prevent accidental shutdown

def prompt_for_filename():
    """
    Prompts the user for a custom filename. Generates a timestamped filename if left blank.
    """
    filename = input("Enter a filename: ").strip()
    if not filename:
        return datetime.now().strftime("%Y%m%d_%H%M%S.txt")
    return filename + ".txt"  # Assuming text files; modify extension as needed

def connect_wifi():
    #TBD - connect device to a wifi network
    pass

def ensure_freewrites_directory():
    freewrites_dir = os.path.join(os.getcwd(), "TypeWrytes")
    if not os.path.exists(freewrites_dir):
        os.makedirs(freewrites_dir)
    return freewrites_dir

def display_manual(screen, filename):
    with open(filename, 'r') as file:
        content = file.readlines()

    max_height, max_width = screen.getmaxyx()
    top_line = 0  # Top line of the content being displayed

    while True:
        screen.clear()
        for i, line in enumerate(content[top_line:top_line + max_height]):
            screen.addstr(i, 0, line[:max_width].rstrip())

        key = screen.getch()

        # Scroll down
        if key == curses.KEY_DOWN and top_line < len(content) - max_height:
            top_line += 1

        # Scroll up
        elif key == curses.KEY_UP and top_line > 0:
            top_line -= 1

        # Exit on ESC or CTRL+E
        elif key in [27, 5]:
            break

        screen.refresh()

# Function to shorten URL using TinyURL
def shorten_url(long_url):
    api_url = f"http://tinyurl.com/api-create.php?url={long_url}"
    response = requests.get(api_url)
    return response.text
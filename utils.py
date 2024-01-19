import os
from datetime import datetime
import curses
import requests
import subprocess

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
    # First, verify that the URL contains the redirect_uri parameter
    if "redirect_uri=" not in long_url:
        print("Error: redirect_uri parameter is missing in the URL.")
        return None

    api_url = f"http://tinyurl.com/api-create.php?url={long_url}"
    response = requests.get(api_url)
    return response.text

def wait_for_escape(key):
    # Wait for user input
    while True:
        if key == 27:  # Escape key
            break

def generate_qr_code(url):
    try:
        # Shell out to bash to run qrencode
        command = ['bash', '-c', f'echo "{url}" | qrencode -t UTF8']

        # Execute the command and capture the output
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, text=True)
        return result.stdout.splitlines()  # Split the output into lines
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None

def show_qr_code(screen, qr_code_lines):
    #qr_code_lines = generate_qr_code(qr_code)
    if qr_code_lines:
        screen.clear()
        screen.addstr("Scan this QR Code to Authenticate to Google. Press 'esc' to close.\n")
        height, width = screen.getmaxyx()

        # Display each line of the QR code
        for i, line in enumerate(qr_code_lines):
            if i + 2 < height:  # Check if within the vertical limit of the window
                screen.addstr(i + 2, 0, line[:width])  # Add line, truncated to window width

        screen.refresh()
        wait_for_escape(screen.getch())
    else:
        screen.addstr("Failed to generate QR code.")
        screen.refresh()
        wait_for_escape(screen.getch())

import os
from datetime import datetime

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
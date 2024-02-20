import os
from datetime import date
import curses
import requests
import subprocess
import socket
import random

'''def generate_filename():
    """
    Generates a timestamped filename.
    Format: 'YYYYMMDD_HHMMSS.txt'
    """

    return datetime.now().strftime("%Y%m%d_%H%M%S.txt")'''

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
    freewrites_dir = os.path.join(os.getcwd(), "FreeWrites")
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
        if key == 27 or curses.ascii.ctrl('e'):  # Escape key
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
    if qr_code_lines:
        #screen.clear()
        height, width = screen.getmaxyx()
        # Display each line of the QR code
        for i, line in enumerate(qr_code_lines):
            if i + 2 < height:  # Check if within the vertical limit of the window
                screen.addstr(i + 4, 1, line[:width])  # Add line, truncated to window width
        
        screen.refresh()
        wait_for_escape(screen.getch())
    else:
        screen.addstr("Failed to generate QR code.")
        screen.refresh()
        wait_for_escape(screen.getch())

def get_local_ip_address():
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Connect to an external server (does not actually create a connection)
        s.connect(("8.8.8.8", 80))  # Google DNS as an example
        local_ip = s.getsockname()[0] # Get the local IP address
    return local_ip

def display_web_window(screen):
    # Get local IP address
    local_ip = get_local_ip_address()

    # Clear screen
    screen.clear()

    # Display the message
    message_lines = [
        "Use a web browser on the same wifi network as your TypeWryter to browse and download files.\n",
        "Visit the URL below:",
        f"http://{local_ip}:8080",
        "Press ESC or CTRL+E to end"
    ]

    # Display the help message
    start_y = 0
    for line in message_lines:
        screen.addstr(start_y, 0, line)
        start_y += 1  # Increment the line number for each message

    # Generate and display QR code
    url = f"http://{local_ip}:8080"
    qr_code_lines = generate_qr_code(url)
    show_qr_code(screen, qr_code_lines)

    wait_for_escape(screen.getch())

    # Clear and refresh screen before exit
    screen.clear()
    screen.refresh()

def get_random_name():
    adjectives = [
        "quick", "lazy", "sleepy", "noisy", "hungry", "bright", "brave", "calm", "dainty", "eager",
        "fancy", "gentle", "happy", "jolly", "kind", "lively", "merry", "nice", "proud", "silly",
        "tall", "short", "long", "small", "large", "tiny", "huge", "fat", "thin", "round",
        "flat", "sharp", "soft", "hard", "smooth", "rough", "cold", "hot", "warm", "cool",
        "wet", "dry", "heavy", "light", "dark", "bright", "loud", "quiet", "weak", "strong",
        "sad", "joyful", "angry", "peaceful", "excited", "bored", "busy", "lazy", "careful", "careless",
        "cheap", "expensive", "rich", "poor", "clean", "dirty", "deep", "shallow", "early", "late",
        "easy", "difficult", "empty", "full", "good", "bad", "hard", "soft", "high", "low",
        "important", "trivial", "interesting", "boring", "kind", "cruel", "loose", "tight", "major", "minor",
        "new", "old", "open", "closed", "public", "private", "quiet", "loud", "rare", "common",
        "safe", "dangerous", "shy", "outgoing", "single", "married", "slow", "fast", "small", "big",
        "smooth", "rough", "soft", "hard", "solid", "liquid", "sour", "sweet", "spicy", "bland",
        "spring", "autumn", "summer", "winter", "tall", "short", "thick", "thin", "tight", "loose",
        "warm", "cool", "wet", "dry", "young", "old", "happy", "sad", "beautiful", "ugly",
        "rich", "poor", "smart", "stupid", "funny", "serious", "healthy", "sick", "strong", "weak",
        "friendly", "hostile", "generous", "stingy", "honest", "deceitful", "loyal", "treacherous", "brave", "cowardly",
        "calm", "anxious", "content", "dissatisfied", "eager", "reluctant", "excited", "apathetic", "fearful", "bold",
        "grateful", "ungrateful", "hopeful", "pessimistic", "innocent", "guilty", "joyful", "mournful", "keen", "indifferent",
        "lively", "lethargic", "motivated", "unmotivated", "optimistic", "cynical", "passionate", "dispassionate", "quiet", "boisterous",
        "rational", "irrational", "sensible", "foolish", "thoughtful", "thoughtless", "understanding", "unreasonable", "vibrant", "dull",
        "spunky"
    ]

    animals = [
        "aardvark", "albatross", "alligator", "alpaca", "ant", "anteater", "antelope", "ape", "armadillo", "donkey",
        "baboon", "badger", "barracuda", "bat", "bear", "beaver", "bee", "bison", "boar", "buffalo",
        "butterfly", "camel", "capybara", "caribou", "cassowary", "cat", "caterpillar", "cattle", "chamois", "cheetah",
        "chicken", "chimpanzee", "chinchilla", "clam", "cobra", "cockroach", "cod", "coyote", "crab", "crane",
        "crocodile", "crow", "deer", "dinosaur", "dog", "dolphin", "dove", "dragonfly", "duck", "eagle",
        "echidna", "eel", "elephant", "elk", "emu", "falcon", "ferret", "finch", "fish", "flamingo",
        "fly", "fox", "frog", "gazelle", "gerbil", "giraffe", "gnat", "gnu", "goat", "goose",
        "goldfish", "gorilla", "grasshopper", "grouse", "guineapig", "gull", "hamster", "hare", "hawk", "hedgehog",
        "heron", "herring", "hippopotamus", "hornet", "horse", "hummingbird", "hyena", "ibex", "iguana", "jackal",
        "jaguar", "jay", "jellyfish", "kangaroo", "koala", "komododragon", "kookaburra", "lemur", "leopard", "lion",
        "llama", "lobster", "locust", "loris", "louse", "lyrebird", "magpie", "mallard", "manatee", "mandrill",
        "marmoset", "marten", "meerkat", "mink", "mole", "mongoose", "monkey", "moose", "mosquito", "mouse",
        "mule", "narwhal", "newt", "nightingale", "octopus", "okapi", "opossum", "oryx", "ostrich", "otter",
        "owl", "ox", "oyster", "panda", "panther", "parrot", "partridge", "peafowl", "pelican", "penguin",
        "pheasant", "pig", "pigeon", "platypus", "pony", "porcupine", "porpoise", "prairie dog", "quail", "quelea",
        "quokka", "quoll", "rabbit", "raccoon", "rat", "rattlesnake", "reindeer", "rhinoceros", "rook", "salamander",
        "salmon", "sand dollar", "sandpiper", "sardine", "scorpion", "seahorse", "seal", "shark", "sheep", "shrew",
        "skunk", "snail"
    ]
    animal = animals[random.randint(0, 171)]
    adjective = adjectives[random.randint(0, 199)]
    today = date.today().isoformat() # Today's date
    short_name = adjective + "_" + animal #concatenate an adjective and animal name
    filename_string = today + "_" + adjective + "_" + animal #add date to animal and adjective
    print(filename_string)
    return filename_string

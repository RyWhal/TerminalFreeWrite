import curses
import os
import threading
from datetime import datetime

class WritingInterface:
    def __init__(self, filename, directory, existing_content=""):
        self.filename = filename if filename else self.generate_filename()
        self.directory = directory
        self.text = existing_content
        self.auto_save_interval = 30  # Auto-save interval in seconds
        self.auto_save_thread = threading.Thread(target=self.auto_save)
        self.auto_save_thread.daemon = True  # Daemonize the thread

    def run(self, screen):
        self.auto_save_thread.start()  # Start the auto-save thread
        curses.noecho()  # Turn off automatic echoing of keys to the screen
        #curses.echo()  # Echo characters typed by the user
        screen.clear()

        screen.addstr("[CTRL+E] exit\n[CTRL+U] save\n[CTRL+N] Change Filename\n[CTRL+H] Show this help screen.\nHappy Writing!\n")
        screen.refresh()

        while True:
            screen.addstr(0, 0, self.text + ' ')  # Display the current text
            key = screen.getch()
            #screen.addstr(0, 0, f"Last key pressed: {key} ")
            #screen.refresh() 
            if key == curses.KEY_UP or key == curses.KEY_DOWN or key == curses.KEY_LEFT or key == curses.KEY_RIGHT:
                continue
            elif key == 5:  # Ctrl+E to exit
                break
            elif key == 14: # Ctrl+N to change filename
                self.change_filename(screen)
            elif key == 21:  # Ctrl+U to save
                self.save_file()
            elif key == 263:  # Ctrl+H for help
                self.show_help(screen)
            elif key == curses.KEY_BACKSPACE or key == 127:  # Handle backspace
                self.text = self.text[:-1]
            else:
                self.text += chr(key)

            screen.clear()
            screen.addstr(0, 0, self.text)  # Redraw text
            screen.refresh()

    def auto_save(self):
        while True:
            threading.Event().wait(self.auto_save_interval)
            self.save_file()

    def save_file(self):
        filepath = os.path.join(self.directory, self.filename)
        with open(filepath, "w") as file:
            file.write(self.text)
    
    def change_filename(self, screen):
        # Save the current filename in case the user enters a blank name
        current_filename = self.filename

        # Prompt for new filename
        screen.move(1, 0)  # Move cursor to the top of the screen
        screen.clrtoeol()  # Clear any existing text on the line
        screen.addstr(1, 0, "Enter new filename: ")
        screen.refresh()

        new_filename = ""
        while True:
            key = screen.getch()
            if key in [10, 13]:  # Enter key
                break
            elif key == curses.KEY_BACKSPACE or key == 127 or key == 263:  # Backspace
                new_filename = new_filename[:-1]
            elif key < 256 and (chr(key).isalnum() or chr(key) in '-_+='):
                new_filename += chr(key)

            # Update display
            screen.move(1, 20)  # Adjust as needed for your layout
            screen.clrtoeol()
            screen.addstr(1, 20, new_filename)  # Display current filename
            screen.refresh()

        # Get and decode user input
        #new_filename = screen.getstr().decode('utf-8').strip() 

        # Use the new filename if provided, otherwise fall back to the current one
        # Validate the filename for special characters
        if all(char.isalnum() or char in '-_+=' for char in new_filename):
            if new_filename:
                self.filename = new_filename + ".txt"
        else:
            screen.addstr(1, 0, "Error: Blank filename or invalid characters. Using default filename.")
            self.filename = current_filename
            screen.refresh()
            screen.getch()  # Wait for keypress before continuing
        

        # Clear the line after getting input and refresh the screen
        screen.move(0, 0)
        screen.clrtoeol()
        screen.refresh()

    def show_help(self, screen):
        # Clear the line for help text (assuming it's the first line)
        screen.move(0, 0)
        screen.clrtoeol()
        screen.addstr(0, 0, "[CTRL+E] exit\n[CTRL+U] save\n[CTRL+N] Change Filename\n[CTRL+H] Show this help screen.\nHappy Writing!\n")
        screen.refresh()
        # Wait for any keypress to continue
        screen.getch()
        screen.move(0, 0)
        screen.clrtoeol()
        screen.refresh()
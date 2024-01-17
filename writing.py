import curses
import os
import threading
from datetime import datetime

class WritingInterface:
    def __init__(self, filename, directory, existing_content=""):
        self.filename = filename if filename else self.generate_filename()
        self.directory = directory
        self.text = existing_content

        #Autosave every 30 seconds
        self.auto_save_interval = 30  # Auto-save interval in seconds
        self.auto_save_thread = threading.Thread(target=self.auto_save)
        self.auto_save_thread.daemon = True  # Daemonize the thread

        # Intializing text scrolling
        self.text = existing_content.split('\n') if isinstance(existing_content, str) else existing_content  # Split text into lines
        self.cursor_y = 0  # Vertical cursor position
        self.top_line = 0  # Top line of the text being displayed

    def run(self, screen):
        max_height, max_width = screen.getmaxyx() # Get Screen Size
        self.auto_save_thread.start()  # Start the auto-save thread
        curses.noecho()  # Turn off automatic echoing of keys to the screen
        screen.clear()

        # Display the help text on new Freewrite
        help_text = "[CTRL+E] exit\n[CTRL+U] save\n[CTRL+N] Change Filename\n[CTRL+H] Show this help screen.\nHappy Writing!\n"
        screen.addstr(0, 0, help_text)
        screen.refresh()

        while True:
            
            screen.clear() # Clear anything currently on the screen
            # Display text lines within the current view
            for i in range(self.top_line, min(self.top_line + max_height, len(self.text))):
                screen.addstr(i - self.top_line, 0, self.text[i][:max_width])

            #screen.addstr(0, 0, self.text + ' ')  # Display the current text. Old way before Scrolling implemented.
            key = screen.getch() # Get Key-presses

            if key == curses.KEY_UP or key == curses.KEY_DOWN or key == curses.KEY_LEFT or key == curses.KEY_RIGHT:
                continue
            elif key in range(32, 127):  # ASCII printable characters
                if len(self.text[-1]) >= max_width - 1:  # Check if the line is at max width
                    self.text.append("")  # Start a new line
                    self.cursor_y += 1
                self.text[-1] += chr(key)  # Add character to the current line
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.text.insert(self.cursor_y + 1, "")  # Start a new line
                self.cursor_y += 1
            elif key == 5 or key == 27:  # Ctrl+E to exit
                self.save_file()
                break
            elif key == 14: # Ctrl+N to change filename
                self.change_filename(screen)
            elif key == 21:  # Ctrl+U to save
                self.save_file()
            elif key == 263:  # Ctrl+H for help
                self.show_help(screen)
            elif key == curses.KEY_BACKSPACE or key == 127:
                if self.text[-1]:  # If there is text on the last line
                    self.text[-1] = self.text[-1][:-1]  # Remove last character
                elif len(self.text) > 1:  # If the last line is empty and there are previous lines
                    self.text.pop()  # Remove the last empty line
                    self.cursor_y -= 1

            #screen.clear()
            #screen.addstr(0, 0, self.text)  # Redraw text
            screen.refresh() # Refresh after redrawing text

            # Adjust scrolling
            if self.cursor_y >= self.top_line + max_height:
                self.top_line += 1  # Scroll down
            elif self.cursor_y < self.top_line:
                self.to
                p_line -= 1  # Scroll up
            screen.refresh() # Refresh after scrolling

    def auto_save(self):
        while True:
            threading.Event().wait(self.auto_save_interval)
            self.save_file()

    def save_file(self):
        text_to_save = '\n'.join(self.text) # join text into single string
        filepath = os.path.join(self.directory, self.filename)
        with open(filepath, "w") as file:
            file.write(text_to_save) #save all text
    
    def change_filename(self, screen):
        # Save the current filename in case the user enters a blank name
        current_filename = self.filename

        # Prompt for new filename
        screen.move(0, 0)  # Move cursor to the top of the screen
        screen.clrtoeol()  # Clear any existing text on the line
        screen.addstr(0, 0, "Enter new filename: ")
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
            screen.addstr(0, 20, new_filename)  # Display current filename
            screen.refresh()

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
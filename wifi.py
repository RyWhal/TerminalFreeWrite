import subprocess
import curses

class WifiManager:
    def __init__(self):
        pass

    def list_wifi_networks(self):
        result = subprocess.run(["nmcli", "-f", "SSID", "dev", "wifi"], capture_output=True, text=True)
        networks = result.stdout.split('\n')
        return [net.strip() for net in networks[1:] if net.strip()]  # Skip the header and empty lines

    def select_network(self, screen, networks):
        current_row = 0
        while True:
            screen.clear()
            for idx, net in enumerate(networks):
                if idx == current_row:
                    screen.attron(curses.color_pair(1))
                    screen.addstr(idx, 0, net)
                    screen.attroff(curses.color_pair(1))
                else:
                    screen.addstr(idx, 0, net)
            screen.refresh()

            key = screen.getch()
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(networks) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return networks[current_row]

        return None

    def connect_to_network(self, screen, ssid):
        screen.clear()
        screen.addstr(0, 0, f"Enter password for {ssid}: ")
        curses.echo()
        password = screen.getstr(1, 0, 20).decode('utf-8')
        curses.noecho()
        try:
            subprocess.run(["nmcli", "dev", "wifi", "connect", ssid, "password", password], check=True)
            screen.addstr(3, 0, "Connected successfully.")
        except subprocess.CalledProcessError:
            screen.addstr(3, 0, "Failed to connect.")
        screen.refresh()
        screen.getch()
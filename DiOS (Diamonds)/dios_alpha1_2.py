import os
import platform
import shlex
import time
import shutil
import random
import json
from datetime import datetime

# --- ANSI COLOR CODES ---
THEMES = {
    "standard": "\033[0m",
    "matrix": "\033[0;32m",
    "cyber": "\033[0;36m",
    "warning": "\033[0;31m"
}


class DiOS:
    def __init__(self):
        self.config_file = "dios_sys.json"
        self.current_dir = os.getcwd()
        self.user_data = {
            "name": "Guest",
            "country": "Unknown",
            "password": "",
            "installed_apps": [],
            "theme": "standard"
        }
        self.running = True
        self.version = "alpha 1.2"
        self.theme_prefix = THEMES["standard"]
        self.messenger_contacts = {"1": "Alex (Friend)", "2": "CodeMind AI"}

        self.help_text = f"""
DiOS {self.version} Help:
--- System ---
help      : show this help menu
clear     : refresh screen
theme     : change UI colors
store     : Diamond Store (Install Apps)
browser   : DiOS Web Browser
calc      : launch Calculator
antivirus : system security

--- Apps & Social ---
messages  : messenger
gallery   : media gallery
edit <f>  : text editor (like Nano)

--- Entertainment (Must install from Store) ---
games     : list installed games
construction : city builder
hide_seek : 3D Hide & Seek

--- File System ---
ls, cd, pwd, mkdir, rm, touch, cat, write
"""

    def _print(self, text, end="\n"):
        print(f"{self.theme_prefix}{text}\033[0m", end=end)

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # --- PERSISTENCE ---
    def save_system(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.user_data, f, indent=4)

    def load_system(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.user_data = json.load(f)
                self.theme_prefix = THEMES.get(self.user_data.get("theme", "standard"), THEMES["standard"])
                return True
            except:
                return False
        return False

    # --- INSTALLATION ---
    def first_time_setup(self):
        self._clear_screen()
        print("⚡ DiOS INSTALLATION WIZARD ⚡")
        print("-" * 30)
        time.sleep(1)
        print("Extracting system files...")
        for i in range(4):
            time.sleep(0.5)
            print(f"Progress: {(i + 1) * 25}%...")

        print("\n--- User Registration ---")
        self.user_data["name"] = input("Enter your name: ").strip()
        self.user_data["country"] = input("Enter your country: ").strip()

        print("\nFor better protection, use special characters.")
        while True:
            pwd = input("Set your password: ")
            conf = input("Confirm password: ")
            if pwd == conf:
                self.user_data["password"] = pwd
                break
            print("Passwords do not match!")

        self.save_system()
        print("\nInstallation successful! Restarting...")
        time.sleep(2)

    def login(self):
        self._clear_screen()
        print(f"--- DiOS {self.version} Login ---")
        while True:
            name = input("Username: ")
            pwd = input("Password: ")
            if name == self.user_data["name"] and pwd == self.user_data["password"]:
                self._print(f"Welcome back, {name}!")
                time.sleep(1)
                break
            self._print("Access Denied.", end="\n")

    # --- DIAMOND STORE ---
    def run_store(self):
        self._clear_screen()
        self._print("💎 DIAMOND STORE 💎")
        print("Available for download:")
        apps = {
            "1": ["Construction Simulator", "construction"],
            "2": ["Hide In Seek (3D Text)", "hide_seek"]
        }
        for k, v in apps.items():
            status = "[Installed]" if v[1] in self.user_data["installed_apps"] else "[Free]"
            print(f"[{k}] {v[0]} {status}")

        print("\n[Q] Exit Store")
        choice = input("\nSelect App ID to Install: ").strip()

        if choice in apps:
            app_id = apps[choice][1]
            if app_id in self.user_data["installed_apps"]:
                print("App already installed!")
            else:
                print(f"Downloading {apps[choice][0]}...")
                time.sleep(2)
                self.user_data["installed_apps"].append(app_id)
                self.save_system()
                print("Installation Complete!")

        print("\nNew features will be added to this Diamond Store soon, stay tuned for updates.")
        input("Press Enter...")

    # --- TEXT EDITOR (EDIT) ---
    def edit_file(self, filename):
        if not os.path.exists(filename):
            self._print("File does not exist.")
            return

        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        while True:
            self._clear_screen()
            self._print(f"--- DiOS EDITOR: {filename} ---")
            for idx, line in enumerate(lines):
                print(f"{idx + 1}: {line.strip()}")

            print("\nCommands: [Line #] edit line | [s] save | [q] cancel")
            cmd = input("Editor > ").strip().lower()

            if cmd == 'q':
                break
            elif cmd == 's':
                with open(filename, "w", encoding="utf-8") as f:
                    f.writelines(lines)
                self._print("File saved!")
                time.sleep(1)
                break
            elif cmd.isdigit():
                idx = int(cmd) - 1
                if 0 <= idx < len(lines):
                    new_text = input(f"New content for line {cmd}: ")
                    lines[idx] = new_text + "\n"
                else:
                    self._print("Invalid line number.")
                    time.sleep(1)

    # --- THEMES ---
    def change_theme(self):
        self._clear_screen()
        self._print("🎨 THEME CUSTOMIZATION")
        print("[1] Standard (White)")
        print("[2] Matrix (Green)")
        print("[3] Cyber (Cyan)")

        c = input("Choice: ")
        if c == "1":
            self.user_data["theme"] = "standard"
        elif c == "2":
            self.user_data["theme"] = "matrix"
        elif c == "3":
            self.user_data["theme"] = "cyber"

        self.theme_prefix = THEMES.get(self.user_data["theme"])
        self.save_system()
        self._print("Theme updated!")
        time.sleep(1)

    # --- BROWSER ---
    def run_browser(self):
        self._clear_screen()
        self._print("🌐 DiOS BROWSER v1.2")
        print("Try: dios.com, tgk.studio, diamond.net")
        url = input("URL > ").lower().strip()
        print("-" * 30)

        if "dios.com" in url:
            print("Welcome to DiOS Official! Current Version: Alpha 1.2.")
            print("Latest News: Diamond Store is now open for business.")
        elif "tgk.studio" in url:
            print("TGK DiamondCraft Studios: Building the future of urban simulators.")
            print("Project 'Construction' is now available in the Store.")
        elif "diamond.net" in url:
            print("Diamond Network: The fastest simulated data transfer.")
        else:
            print("404 Error: Page not found.")

        input("\n[Q] Exit Browser...")

    # --- CORE LOGIC ---
    def execute_command(self, cmd_str):
        parts = shlex.split(cmd_str)
        if not parts: return
        cmd = parts[0].lower()

        if cmd == "help":
            print(self.help_text)
        elif cmd in ["clear", "refresh"]:
            self._clear_screen()
        elif cmd == "theme":
            self.change_theme()
        elif cmd == "store":
            self.run_store()
        elif cmd == "browser":
            self.run_browser()
        elif cmd == "edit":
            if len(parts) > 1:
                self.edit_file(parts[1])
            else:
                print("Usage: edit <filename>")
        elif cmd == "construction":
            if "construction" in self.user_data["installed_apps"]:
                self._print("Running Construction Sim...")  # Simulation logic from 1.1.9 here
            else:
                self._print("Error: App not installed. Visit Diamond Store.")
        elif cmd == "hide_seek":
            if "hide_seek" in self.user_data["installed_apps"]:
                self._print("Running Hide In Seek...")  # Logic from 1.1.9 here
            else:
                self._print("Error: App not installed. Visit Diamond Store.")
        elif cmd == "3":
            self._print("Powering off...");
            time.sleep(1);
            self.running = False
        elif cmd == "2":
            self.run()
        elif cmd == "1":
            print(f"DiOS v{self.version} | User: {self.user_data['name']} | Locale: {self.user_data['country']}")
        # ... (rest of file system/calc/games from previous versions) ...
        else:
            print(f"Command not found: {cmd}")

    def run(self):
        if not self.load_system():
            self.first_time_setup()
        self.login()
        self._clear_screen()

        while self.running:
            now = datetime.now().strftime("%H:%M")
            print(f"\n[ 1:Sysinfo | 2:Restart | 3:Shutdown ] {'=' * 30} [ {now} ]")
            cmd = input(f"{self.user_data['name']} > ").strip()
            if cmd: self.execute_command(cmd)


if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except Exception as e:
        print(f"KERNEL ERROR: {e}")
    finally:
        input("\n[System Halted. Press Enter to Close]")
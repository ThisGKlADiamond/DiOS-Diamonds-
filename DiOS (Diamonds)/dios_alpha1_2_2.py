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

# Optional psutil for system metrics
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Optional pyperclip for AI code copying
try:
    import pyperclip

    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


class DiOS:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.user = "Guest"
        self.running = True
        self.version = "alpha 1.2.2"
        self.command_history = []
        self.config_file = "dios_sys.json"
        self.users_db = {}
        self.messenger_contacts = {"1": "Alex (Friend)", "2": "CodeMind AI"}

        # Base user data initialized
        self.user_data = {
            "name": "Guest",
            "country": "Unknown",
            "password": "",
            "theme": "standard",
            "installed_apps": []
        }
        self.theme_prefix = THEMES["standard"]

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

                # Ensure installed_apps exists in legacy saves
                if "installed_apps" not in self.user_data:
                    self.user_data["installed_apps"] = []

                self.theme_prefix = THEMES.get(self.user_data.get("theme", "standard"), THEMES["standard"])
                self.user = self.user_data.get("name", "Guest")
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

        self.user = self.user_data["name"]
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
        elif choice.lower() != 'q':
            print("Invalid choice.")

        print("\nNew features will be added to this Diamond Store soon, stay tuned for updates.")
        input("Press Enter...")

    # --- TEXT EDITOR (EDIT) ---
    def edit_file(self, filename):
        if not os.path.exists(filename):
            self._print("File does not exist. Creating new file...")
            with open(filename, "w", encoding="utf-8") as f:
                pass  # Create empty file

        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        while True:
            self._clear_screen()
            self._print(f"--- DiOS EDITOR: {filename} ---")
            for idx, line in enumerate(lines):
                print(f"{idx + 1}: {line.strip()}")

            print("\nCommands: [Line #] edit line | [a] add line | [s] save | [q] cancel")
            cmd = input("Editor > ").strip().lower()

            if cmd == 'q':
                break
            elif cmd == 's':
                with open(filename, "w", encoding="utf-8") as f:
                    f.writelines(lines)
                self._print("File saved!")
                time.sleep(1)
                break
            elif cmd == 'a':
                new_text = input("New line content: ")
                lines.append(new_text + "\n")
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

        self.theme_prefix = THEMES.get(self.user_data["theme"], THEMES["standard"])
        self.save_system()
        self._print("Theme updated!")
        time.sleep(1)

    # --- BROWSER ---
    def run_browser(self):
        self._clear_screen()
        self._print(f"🌐 DiOS BROWSER v{self.version}")
        print("Try: dios.com, tgk.studio, diamond.net")
        url = input("URL > ").lower().strip()
        print("-" * 30)

        if "dios.com" in url:
            print(f"Welcome to DiOS Official! Current Version: {self.version}.")
            print("Latest News: Diamond Store is now open for business.")
        elif "tgk.studio" in url:
            print("TGK DiamondCraft Studios: Building the future of urban simulators.")
            print("Project 'Construction' is now available in the Store.")
        elif "diamond.net" in url:
            print("Diamond Network: The fastest simulated data transfer.")
        else:
            print("404 Error: Page not found.")

        input("\n[Press Enter to Exit Browser...]")

    # --- ADVANCED CALCULATOR ---
    def run_calculator(self):
        self._clear_screen()
        print("🔢 DiOS Advanced Calculator")
        print("Modes: [1] Standard  [2] Programmer  [Q] Exit")
        mode = input("Select Mode: ").strip().lower()

        if mode == "1":
            print("\n-- Standard Mode (Type 'q' to go back) --")
            while True:
                expr = input("Calc > ").strip()
                if expr.lower() == 'q': break
                try:
                    allowed = "0123456789+-*/(). "
                    if all(c in allowed for c in expr):
                        print(f"Result: {eval(expr)}")
                    else:
                        print("Error: Invalid characters.")
                except:
                    print("Error: Invalid expression.")
        elif mode == "2":
            print("\n-- Programmer Mode (Dec/Hex/Bin) --")
            while True:
                val = input("Enter Decimal Number (or 'q'): ").strip()
                if val.lower() == 'q': break
                if val.isdigit():
                    n = int(val)
                    print(f"DEC: {n}")
                    print(f"HEX: {hex(n).upper()}")
                    print(f"BIN: {bin(n)}")
                else:
                    print("Error: Enter a whole number.")

    # --- HIDE IN SEEK (3D Simulation) ---
    def play_hide_seek(self):
        if "hide_seek" not in self.user_data.get("installed_apps", []):
            self._print("Error: App not installed. Visit Diamond Store.")
            return

        self._clear_screen()
        print("🙈 Hide In Seek: 3D Text Edition")
        print("Mode: [1] vs AI  [2] Local Multiplayer")
        mode = input("Choice: ")

        rooms = ["Kitchen", "Basement", "Attic", "Garden Shed", "Master Bedroom"]

        if mode == "1":
            print("\nAI is hiding...")
            time.sleep(1.5)
            ai_pos = random.choice(rooms)
            print("AI: 'I'm hidden! You have 2 tries to find me.'")
            for i in range(2):
                print(f"\nLocations: {', '.join(rooms)}")
                seek = input(f"Try {i + 1} - Where are you looking? ").title()
                if seek == ai_pos:
                    print(f"🎉 Found it! The AI was in the {ai_pos}!")
                    return
                else:
                    print("Nothing here...")
            print(f"Game Over! AI was in the {ai_pos}.")

        elif mode == "2":
            p1 = input("Player 1 Name: ")
            p2 = input("Player 2 Name: ")
            print(f"\n{p1}, close your eyes! {p2}, choose a location.")
            print(f"Rooms: {', '.join(rooms)}")
            p2_pos = input(f"{p2} > ").title()
            self._clear_screen()
            print(f"{p1}, it's time to search!")
            seek = input(f"Search location: ").title()
            if seek == p2_pos:
                print(f"Found you, {p2}!")
            else:
                print(f"Missed! {p2} was in the {p2_pos}.")
        input("\nPress Enter...")

    # --- CONSTRUCTION SIMULATOR ---
    def run_construction_sim(self):
        if "construction" not in self.user_data.get("installed_apps", []):
            self._print("Error: App not installed. Visit Diamond Store.")
            return

        self._clear_screen()
        print("⚡ TGK DiamondCraft Studios Presents:")
        print("🏗️  Construction of Villages and Towns")
        print("-" * 40)
        print("[1] New Game  [2] Information  [Q] Exit")

        choice = input("> ").lower()
        if choice == "2":
            print("\nIn the year 2026, TGK DiamondCraft Studios unveiled 'Construction of villages and towns'.")
            print("This pioneering urban planning simulator constitutes a significant advancement...")
            input("Press Enter...")
            self.run_construction_sim()
        elif choice == "1":
            self._clear_screen()
            print("Location: Sunny Valley (Natural Paradise)")
            print("Guide: 'This area is just a fire for development! Huge prospects!'")
            print("\nStep 1: Analyze the territory.")
            input("[Press Enter to Research Area...]")
            print("Analysis: Soil is stable. Water access is good. Perfect for a village.")

            pop = 0
            while pop < 20:
                print(f"\nCurrent Population: {pop} people")
                print("Options: [H] Place House (+5 pop)  [Q] Exit Game")
                act = input("Action: ").lower()
                if act == 'h':
                    print("🏗️  Building...")
                    time.sleep(1)
                    pop += 5
                    print(f"New residents moved in! Total: {pop}")
                elif act == 'q':
                    break

            if pop >= 20:
                print("\n🏆 Congratulations! Your village has become a small town!")
            input("Returning to menu...")

    # --- MESSENGER ---
    def run_messages(self):
        self._clear_screen()
        print(f"💬 DiOS Messenger v{self.version}")
        while True:
            print("\nContacts:")
            for k, v in self.messenger_contacts.items(): print(f"[{k}] {v}")
            print("[+] Add Contact  [Q] Exit")

            choice = input("\nSelect: ").strip().lower()
            if choice == 'q': break

            if choice == '+':
                name = input("Enter Name: ")
                self.messenger_contacts[str(len(self.messenger_contacts) + 1)] = name
                print("Contact Added!")
            elif choice == '2':
                print("\n[CodeMind]: Ask me for Python/C++ code!")
                req = input("You: ")
                print("AI: Generating...")
                time.sleep(1)
                print("```python\nprint('Simulation Complete')\n```")
            elif choice in self.messenger_contacts:
                print(f"\n[{self.messenger_contacts[choice]}]: Hello! I'm busy right now.")
                input("You: ")
            else:
                print("Invalid option.")

    def run_antivirus(self):
        self._clear_screen()
        print("🛡️  DiOS Antivirus System App")
        print("[1] Deep Scan [2] Delete Cache [Q] Exit")
        c = input("> ").lower()
        if c == "1":
            print("Scanning...")
            time.sleep(2)
            print("System is Clean!")
        elif c == "2":
            print("Cache deleted (50MB saved).")
        input("Press Enter...")

    def play_guess(self):
        self._clear_screen()
        print("🎮 Guess The Number")
        print("Not implemented in this build.")
        input("Press Enter...")

    def play_math(self):
        self._clear_screen()
        print("🎮 Math Challenge")
        print("Not implemented in this build.")
        input("Press Enter...")

    def boot_sequence(self):
        self._clear_screen()
        print("Initializing DiOS BIOS 2026...")
        time.sleep(0.5)
        print("Checking File System... OK")
        time.sleep(0.5)
        print("Mounting TGK_DiamondCraft_Drivers... Done.")
        time.sleep(0.5)

    def display_taskbar(self):
        now = datetime.now().strftime("%H:%M:%S")
        print(f"\n[ 1:Sysinfo | 2:Restart | 3:Shutdown ] {'=' * 30} [ {now} ]")

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
        elif cmd == "calc":
            self.run_calculator()
        elif cmd == "messages":
            self.run_messages()
        elif cmd == "antivirus":
            self.run_antivirus()
        elif cmd == "edit":
            if len(parts) > 1:
                self.edit_file(parts[1])
            else:
                print("Usage: edit <filename>")
        elif cmd == "hide_seek":
            self.play_hide_seek()
        elif cmd == "construction":
            self.run_construction_sim()
        elif cmd == "games":
            print("Games: 'guess', 'math', 'hide_seek', 'construction'")
        elif cmd == "guess":
            self.play_guess()
        elif cmd == "math":
            self.play_math()
        elif cmd == "1":
            print(
                f"DiOS v{self.version} | Host: {platform.node()} | Locale: {self.user_data.get('country', 'Unknown')}")
        elif cmd == "2":
            self._print("Restarting OS...")
            time.sleep(1)
            self.run()
        elif cmd == "3":
            print("Shutting down...")
            time.sleep(1)
            self.running = False
        else:
            print(f"Unknown command: {cmd}. Type 'help'.")

    def run(self):
        self.boot_sequence()

        if not self.load_system():
            self.first_time_setup()
        else:
            self.login()

        self._clear_screen()
        print(f"Welcome to DiOS {self.version}")
        print("If you don't know how to spell this command, then enter 'help' for a detailed list.")

        while self.running:
            self.display_taskbar()
            cmd = input(f"{self.user} > ").strip()
            if cmd:
                self.execute_command(cmd)


if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        print("\n[System successfully powered down]")
        input("[Press Enter to close the window...]")
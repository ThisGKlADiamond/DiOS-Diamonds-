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
        self.version = "alpha 1.2.2 medium edition"
        self.config_file = "dios_sys.json"
        self.running = True
        self.theme_prefix = THEMES["standard"]

        # Инициализация базовых данных пользователя
        self.user_data = {
            "name": "Guest",
            "country": "Unknown",
            "password": "",
            "theme": "standard",
            "installed_apps": []
        }

        self.messenger_contacts = {"1": "Alex (Friend)", "2": "CodeMind AI"}
        self.help_text = f"""
DiOS {self.version} Help Menu:
--- System ---
help      : show this menu
clear     : refresh screen
theme     : change UI colors
sysinfo   : show system information
store     : Diamond Store (Install Apps)
browser   : DiOS Web Browser
calc      : launch Calculator
antivirus : system security

--- Apps & Social ---
messages  : messenger
edit <f>  : text editor
games     : list installed games

--- Entertainment ---
construction : city builder (requires install)
hide_seek    : 3D Hide & Seek (requires install)

--- Controls ---
1: Info | 2: Restart | 3: Shutdown
"""

    # --- СИСТЕМНЫЕ МЕТОДЫ ---
    def _print(self, text, end="\n"):
        print(f"{self.theme_prefix}{text}\033[0m", end=end)

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def save_system(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self._print(f"Error saving system: {e}")

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

    def first_time_setup(self):
        self._clear_screen()
        print("⚡ DiOS INSTALLATION WIZARD ⚡")
        print("-" * 30)
        time.sleep(0.5)
        print("Extracting system files...")
        for i in range(4):
            time.sleep(0.3)
            print(f"Progress: {(i + 1) * 25}%...")

        print("\n--- User Registration ---")
        self.user_data["name"] = input("Enter your name: ").strip() or "User"
        self.user_data["country"] = input("Enter your country: ").strip() or "Unknown"

        while True:
            pwd = input("Set your password: ")
            conf = input("Confirm password: ")
            if pwd == conf:
                self.user_data["password"] = pwd
                break
            print("Passwords do not match!")

        self.save_system()
        print("\nInstallation successful! Restarting...")
        time.sleep(1.5)

    def login(self):
        self._clear_screen()
        print(f"--- DiOS {self.version} Login ---")
        attempts = 0
        while attempts < 3:
            name = input("Username: ")
            pwd = input("Password: ")
            if name == self.user_data["name"] and pwd == self.user_data["password"]:
                self._print(f"Welcome back, {name}!")
                time.sleep(1)
                return True
            else:
                self._print("Access Denied.")
                attempts += 1
        self._print("Too many failed attempts. Emergency shutdown.")
        return False

    # --- ПРИЛОЖЕНИЯ ---
    def run_store(self):
        self._clear_screen()
        self._print("💎 DIAMOND STORE 💎")
        apps = {
            "1": ["Construction Simulator", "construction"],
            "2": ["Hide In Seek (3D Text)", "hide_seek"]
        }
        for k, v in apps.items():
            status = "[Installed]" if v[1] in self.user_data.get("installed_apps", []) else "[Free]"
            print(f"[{k}] {v[0]} {status}")

        print("\n[Q] Exit Store")
        choice = input("\nSelect App ID: ").strip().lower()
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
        input("\nPress Enter...")

    def run_calculator(self):
        self._clear_screen()
        print("🔢 DiOS Advanced Calculator")
        mode = input("[1] Standard [2] Programmer [Q] Exit: ").strip().lower()
        if mode == "1":
            while True:
                expr = input("Calc > ").strip()
                if expr.lower() == 'q': break
                try:
                    allowed = "0123456789+-*/(). "
                    if all(c in allowed for c in expr) and expr:
                        print(f"Result: {eval(expr)}")
                    else:
                        print("Error: Invalid input.")
                except:
                    print("Error: Invalid expression.")
        elif mode == "2":
            while True:
                val = input("Enter Dec (or 'q'): ").strip()
                if val.lower() == 'q': break
                if val.isdigit():
                    n = int(val)
                    print(f"HEX: {hex(n).upper()} | BIN: {bin(n)}")
                else:
                    print("Error: Enter a number.")

    def change_theme(self):
        self._clear_screen()
        print("🎨 THEME CUSTOMIZATION\n[1] Standard [2] Matrix [3] Cyber")
        c = input("Choice: ")
        mapping = {"1": "standard", "2": "matrix", "3": "cyber"}
        if c in mapping:
            self.user_data["theme"] = mapping[c]
            self.theme_prefix = THEMES[mapping[c]]
            self.save_system()
            self._print("Theme updated!")
            time.sleep(1)

    def run_browser(self):
        self._clear_screen()
        self._print("🌐 DiOS BROWSER v1.2")
        print("Pages: dios.com, tgk.studio, diamond.net")
        url = input("URL > ").lower().strip()
        print("-" * 30)
        content = {
            "dios.com": "Welcome to DiOS Official! Diamond Store is now LIVE.",
            "tgk.studio": "TGK DiamondCraft Studios: Project 'Construction' is out now.",
            "diamond.net": "Diamond Network: High-speed data simulated."
        }
        print(content.get(url, "404 Error: Page not found."))
        input("\n[Q] Exit Browser...")

    # --- ОСНОВНАЯ ЛОГИКА ---
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
        elif cmd == "sysinfo" or cmd == "1":
            print(f"DiOS {self.version} | User: {self.user_data['name']} | Country: {self.user_data['country']}")
            print(f"Host: {platform.node()} | OS: {platform.system()}")
        elif cmd == "2":
            self._print("Restarting...")
            time.sleep(1)
            self.run()
        elif cmd == "3" or cmd == "shutdown":
            self._print("Powering off...")
            time.sleep(1.5)
            self.running = False
        elif cmd == "construction":
            if "construction" in self.user_data.get("installed_apps", []):
                self._print("Launching Construction Simulator...")
                # (Здесь должна быть логика симулятора)
            else:
                self._print("Error: Install this app from the Store first.")
        else:
            self._print(f"Command not found: {cmd}")

    def boot_sequence(self):
        self._clear_screen()
        print("Initializing DiOS BIOS 2026...")
        time.sleep(0.4)
        print("Checking File System... OK")
        print("Mounting TGK_DiamondCraft_Drivers... Done.")
        time.sleep(0.4)

    def run(self):
        if not self.load_system():
            self.first_time_setup()

        if not self.login():
            self.running = False
            return

        self.boot_sequence()
        self._clear_screen()
        self._print(f"Welcome to DiOS {self.version}")

        while self.running:
            now = datetime.now().strftime("%H:%M")
            print(f"\n[ 1:Sysinfo | 2:Restart | 3:Shutdown ] {'=' * 20} [ {now} ]")
            try:
                cmd = input(f"{self.user_data['name']}@dios > ").strip()
                if cmd: self.execute_command(cmd)
            except KeyboardInterrupt:
                print("\nUse command '3' to shutdown.")


if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
    finally:
        print("\n[System successfully powered down]")
        input("[Press Enter to close]")
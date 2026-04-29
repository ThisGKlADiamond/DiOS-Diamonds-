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
        self.version = "alpha 1.2.2 easy edition"
        self.config_file = "dios_sys.json"
        self.running = True

        # Инициализация базовых данных пользователя
        self.user_data = {
            "name": "Guest",
            "country": "Unknown",
            "password": "",
            "theme": "standard",
            "installed_apps": [],
            "balance": 100
        }

        self.theme_prefix = THEMES["standard"]
        self.messenger_contacts = {"1": "Alex (Friend)", "2": "CodeMind AI"}

        self.help_text = f"""
DiOS {self.version} Help:
--- System ---
help      : show this help menu
clear     : refresh screen
theme     : change UI colors
store     : Diamond Store (Install Apps)
antivirus : system security
sysinfo   : show system details (Command: 1)

--- Apps & Social ---
messages  : messenger
calc      : launch Calculator
browser   : DiOS Web Browser

--- Entertainment ---
games     : list installed games
construction : city builder (Store)
hide_seek    : 3D Hide & Seek (Store)

--- Navigation ---
2: Restart | 3: Shutdown
"""

    # --- СИСТЕМНЫЕ МЕТОДЫ ---
    def _print(self, text, end="\n"):
        print(f"{self.theme_prefix}{text}\033[0m", end=end)

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

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

    def first_time_setup(self):
        self._clear_screen()
        print("⚡ DiOS INSTALLATION WIZARD 1.2.2 ⚡")
        print("-" * 30)
        time.sleep(1)
        print("Extracting system files...")
        for i in range(1, 5):
            time.sleep(0.4)
            print(f"Progress: {i * 25}%...")

        self.user_data["name"] = input("\nEnter your name: ").strip() or "User"
        self.user_data["country"] = input("Enter your country: ").strip() or "Global"

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
        while True:
            name = input("Username: ")
            pwd = input("Password: ")
            if name == self.user_data["name"] and pwd == self.user_data["password"]:
                self._print(f"Welcome back, {name}!")
                time.sleep(1)
                break
            else:
                attempts += 1
                print(f"Access Denied. ({attempts}/3)")
                if attempts >= 3:
                    print("System Locked for 5 seconds.")
                    time.sleep(5)
                    attempts = 0

    # --- ПРИЛОЖЕНИЯ ---
    def run_store(self):
        self._clear_screen()
        self._print("💎 DIAMOND STORE 💎")
        apps = {
            "1": ["Construction Simulator", "construction"],
            "2": ["Hide In Seek (3D Text)", "hide_seek"]
        }
        for k, v in apps.items():
            status = "[Installed]" if v[1] in self.user_data["installed_apps"] else "[Free]"
            print(f"[{k}] {v[0]} {status}")

        choice = input("\nSelect App ID or [Q] to exit: ").strip().lower()
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
        print("Modes: [1] Standard  [2] Programmer  [Q] Exit")
        mode = input("> ").strip().lower()
        if mode == "1":
            while True:
                expr = input("Calc (or 'q'): ").strip()
                if expr.lower() == 'q': break
                try:
                    # Очистка ввода для безопасности
                    allowed = "0123456789+-*/(). "
                    if all(c in allowed for c in expr) and expr:
                        print(f"Result: {eval(expr)}")
                    else:
                        print("Error: Invalid characters.")
                except:
                    print("Error: Calculation error.")
        elif mode == "2":
            while True:
                val = input("Enter Dec (or 'q'): ").strip()
                if val.lower() == 'q': break
                if val.isdigit():
                    n = int(val)
                    print(f"HEX: {hex(n).upper()} | BIN: {bin(n)}")
                else:
                    print("Error: Enter a whole number.")

    def run_messages(self):
        self._clear_screen()
        print("💬 DiOS Messenger")
        while True:
            for k, v in self.messenger_contacts.items(): print(f"[{k}] {v}")
            choice = input("\nSelect ID or [Q]: ").strip().lower()
            if choice == 'q': break
            if choice == '2':
                print("\n[CodeMind]: I'm active. Need a Python script?")
                input("You: ")
                print("CodeMind: Interesting request. I'll process that in the next update.")
            elif choice in self.messenger_contacts:
                print(f"[{self.messenger_contacts[choice]}]: Hey! I'm away from keyboard.")
                input("You: ")

    def run_browser(self):
        self._clear_screen()
        self._print("🌐 DiOS BROWSER v1.2.2")
        url = input("URL > ").lower().strip()
        if "dios.com" in url:
            print("Official DiOS Site: Version 1.2.2 Stable is here.")
        elif "tgk.studio" in url:
            print("TGK Studios: 'Construction' sim updated with better AI.")
        else:
            print("404: Not Found.")
        input("\n[Enter] to close...")

    # --- ЯДРО И КОМАНДЫ ---
    def execute_command(self, cmd_str):
        parts = shlex.split(cmd_str)
        if not parts: return
        cmd = parts[0].lower()

        if cmd == "help":
            print(self.help_text)
        elif cmd in ["clear", "refresh"]:
            self._clear_screen()
        elif cmd == "theme":
            self._clear_screen()
            print("🎨 THEMES: [1] Standard [2] Matrix [3] Cyber")
            c = input("> ")
            t_map = {"1": "standard", "2": "matrix", "3": "cyber"}
            if c in t_map:
                self.user_data["theme"] = t_map[c]
                self.theme_prefix = THEMES[t_map[c]]
                self.save_system()
                print("Theme updated!")
        elif cmd == "store":
            self.run_store()
        elif cmd == "calc":
            self.run_calculator()
        elif cmd == "messages":
            self.run_messages()
        elif cmd == "browser":
            self.run_browser()
        elif cmd == "antivirus":
            print("🛡️ Scanning...")
            time.sleep(1.5)
            print("Status: System Secure. 0 threats found.")
        elif cmd == "construction":
            if "construction" in self.user_data["installed_apps"]:
                print("🏗️ (Simulating Construction...) Village population: 25. Level Up!")
            else:
                self._print("Error: Install this from 'store' first.")
        elif cmd == "1" or cmd == "sysinfo":
            print(f"--- SYSTEM INFO ---")
            print(f"OS: DiOS {self.version}\nUser: {self.user_data['name']}\nCountry: {self.user_data['country']}")
            print(f"Apps: {', '.join(self.user_data['installed_apps'])}")
        elif cmd == "2":
            self._print("Restarting...")
            time.sleep(1)
            self.run()
        elif cmd == "3":
            self._print("Powering off...")
            time.sleep(1)
            self.running = False
        else:
            print(f"Command '{cmd}' not recognized. Type 'help'.")

    def run(self):
        if not self.load_system():
            self.first_time_setup()
        self.login()
        self._clear_screen()
        self._print(f"Welcome to DiOS {self.version}")

        while self.running:
            now = datetime.now().strftime("%H:%M")
            # Панель управления
            print(f"\n\033[44m[ 1:Sys | 2:Reset | 3:Off ]{' ' * 15}[ {now} ]\033[0m")
            prompt = f"{self.user_data['name']}@dios ~> "
            cmd = input(prompt).strip()
            if cmd:
                self.execute_command(cmd)


if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except KeyboardInterrupt:
        print("\nEmergency Shutdown.")
    except Exception as e:
        print(f"\nKERNEL PANIC: {e}")
    finally:
        print("\n[System successfully powered down]")
import os
import platform
import shlex
import time
import shutil
import random
import json
import subprocess
from datetime import datetime

# --- ANSI COLOR CODES ---
THEMES = {
    "standard": "\033[0m",
    "matrix": "\033[0;32m",
    "cyber": "\033[0;36m",
    "warning": "\033[0;31m",
    "hacker": "\033[1;32m",
    "neon": "\033[1;35m"
}

BG_COLORS = {
    "black": "\033[40m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
    "white": "\033[47m"
}


class DiOS:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.user = "Guest"
        self.running = True
        self.version = "alpha 1.2.4"
        self.config_file = "dios_sys.json"
        self.messenger_contacts = {"1": "Alex (Friend)", "2": "CodeMind AI"}
        self.screen_buffer = []  # Для закрепления UI

        # Base user data initialized (старые данные не потеряются)
        self.user_data = {
            "name": "Guest",
            "country": "Unknown",
            "password": "",
            "theme": "standard",
            "bg_color": "black",
            "taskbar_color": "cyber",
            "installed_apps": []
        }
        self.theme_prefix = THEMES["standard"]

        self.help_text = f"""
DiOS {self.version} Help:
--- System ---
help      : show this help menu
clear     : refresh screen
settings  : OS personalization, theme, sysinfo
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
hide_seek : 3D Hide & Seek (Powered by Ursina)
"""

    def _print_buf(self, text):
        """Добавляет текст в буфер для отрисовки главного экрана"""
        self.screen_buffer.append(f"{self.theme_prefix}{text}\033[0m")

    def _print(self, text, end="\n"):
        """Прямой вывод для под-приложений"""
        print(f"{self.theme_prefix}{text}\033[0m", end=end)

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # --- PERSISTENCE (ИСПРАВЛЕНО В 1.2.4) ---
    def save_system(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, indent=4)
            return True
        except PermissionError:
            print(
                f"\n{THEMES['warning']}[ВНИМАНИЕ] Ошибка доступа (Errno 13)! Не удалось сохранить {self.config_file}.\033[0m")
            print("Возможно, файл открыт в другой программе или у DiOS нет прав на запись в этой папке.")
            print("Система продолжит работу, но данные могут не сохраниться после перезагрузки.")
            time.sleep(4)
            return False
        except Exception as e:
            print(f"\n{THEMES['warning']}[ВНИМАНИЕ] Непредвиденная ошибка при сохранении: {e}\033[0m")
            time.sleep(3)
            return False

    def load_system(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)
                    # Обновляем дефолтные ключи старых версий (чтобы не потерять данные)
                    for k, v in self.user_data.items():
                        if k not in saved_data:
                            saved_data[k] = v
                    self.user_data = saved_data

                self.theme_prefix = THEMES.get(self.user_data.get("theme", "standard"), THEMES["standard"])
                self.user = self.user_data.get("name", "Guest")
                return True
            except:
                return False
        return False

    # --- INSTALLATION & LOGIN ---
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
        self.save_system()  # Теперь ошибка доступа не "уронит" установку
        print("\nInstallation successful! Restarting...")
        time.sleep(2)

    def login(self):
        self._clear_screen()
        print(f"--- DiOS {self.version} Login ---")
        while True:
            name = input("Username: ")
            pwd = input("Password: ")
            if name == self.user_data["name"] and pwd == self.user_data["password"]:
                print(f"\nWelcome back, {name}!")
                time.sleep(1)
                break
            print("Access Denied.\n")

    # --- SETTINGS APP ---
    def run_settings(self):
        while True:
            self._clear_screen()
            self._print("⚙️ DiOS SETTINGS")
            print("[1] System Info")
            print("[2] Personalization (Themes & Colors)")
            print("[3] Wallpaper (Background Color)")
            print("[Q] Exit Settings")

            c = input("> ").strip().lower()
            if c == 'q': break

            if c == '1':
                self._clear_screen()
                print("--- SYSTEM INFO ---")
                print(f"OS Version: DiOS v{self.version}")
                print(f"User: {self.user_data['name']}")
                print(f"Location: {self.user_data['country']}")
                print(f"Host: {platform.node()}")
                print(f"System: {platform.system()} {platform.release()}")
                input("\nPress Enter...")

            elif c == '2':
                self._clear_screen()
                print("--- TEXT & TASKBAR THEME ---")
                print("[1] Standard [2] Matrix [3] Cyber [4] Hacker [5] Neon")
                tc = input("Choice: ")
                colors = {"1": "standard", "2": "matrix", "3": "cyber", "4": "hacker", "5": "neon"}
                if tc in colors:
                    self.user_data["theme"] = colors[tc]
                    self.user_data["taskbar_color"] = colors[tc]
                    self.theme_prefix = THEMES[self.user_data["theme"]]
                    self.save_system()
                    print("Theme applied!")
                    time.sleep(1)

            elif c == '3':
                self._clear_screen()
                print("--- OS WALLPAPER (BACKGROUND) ---")
                print("[1] Black (Default) [2] Blue [3] Magenta [4] Cyan [5] White")
                bg = input("Choice: ")
                bg_map = {"1": "black", "2": "blue", "3": "magenta", "4": "cyan", "5": "white"}
                if bg in bg_map:
                    self.user_data["bg_color"] = bg_map[bg]
                    self.save_system()
                    print("Wallpaper applied!")
                    time.sleep(1)

    # --- URSINA 3D GAME (HIDE IN SEEK) ---
    def play_hide_seek(self):
        if "hide_seek" not in self.user_data.get("installed_apps", []):
            self._print_buf("Error: App not installed. Visit Diamond Store.")
            return

        self._clear_screen()
        print("🚀 Launching Hide In Seek 3D Engine...")
        print("Make sure you have Ursina installed (pip install ursina)")
        time.sleep(1.5)

        game_code = """
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Графика и окружение
ground = Entity(model='plane', scale=(50, 1, 50), color=color.green, texture='white_cube', texture_scale=(50, 50), collider='box')
Sky()

# Стены лабиринта (укрытия)
for i in range(15):
    Entity(model='cube', color=color.gray, scale=(random.randint(2, 6), random.randint(3, 6), 1),
           position=(random.randint(-20, 20), 2, random.randint(-20, 20)), collider='box')

# AI (Кого мы ищем)
target = Entity(model='cube', color=color.red, scale=(1, 2, 1),
                position=(random.randint(-20, 20), 1, random.randint(-20, 20)), collider='box')

player = FirstPersonController()

text = Text(text="FIND THE RED CUBE! [Press ESC to Exit]", position=(0, 0.4), origin=(0,0), scale=2, color=color.yellow)

def update():
    if distance(player.position, target.position) < 2.5:
        text.text = "YOU FOUND THEM! YOU WIN!"
        text.color = color.green

app.run()
"""
        try:
            with open("dios_hideseek_3d.py", "w", encoding="utf-8") as f:
                f.write(game_code)
            subprocess.run(["python", "dios_hideseek_3d.py"])
        except Exception as e:
            print(f"Failed to launch 3D engine: {e}")
            input("Press Enter to continue...")

    # --- Остальные приложения ---
    def run_store(self):
        self._clear_screen()
        self._print("💎 DIAMOND STORE 💎")
        print("Available for download:")
        apps = {
            "1": ["Construction Simulator", "construction"],
            "2": ["Hide In Seek 3D (Ursina Engine)", "hide_seek"]
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
        time.sleep(1)

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

    def run_construction_sim(self):
        if "construction" not in self.user_data.get("installed_apps", []):
            self._print_buf("Error: App not installed. Visit Diamond Store.")
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

    def edit_file(self, filename):
        if not os.path.exists(filename):
            self._print("File does not exist. Creating new file...")
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    pass
            except Exception as e:
                self._print(f"Error creating file: {e}")
                time.sleep(2)
                return

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
                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.writelines(lines)
                    self._print("File saved!")
                except Exception as e:
                    self._print(f"Error saving file: {e}")
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

    # --- CORE UI RENDERER (ФИКСИРОВАННАЯ ПАНЕЛЬ ЗАДАЧ) ---
    def render_desktop(self):
        self._clear_screen()
        cols, lines = shutil.get_terminal_size((80, 24))

        # Применяем фон
        bg_col = BG_COLORS.get(self.user_data.get("bg_color", "black"), "")
        reset_col = "\033[0m"

        # Заголовок (Обои / Лого)
        header = f"{bg_col}{THEMES[self.user_data['theme']]}"
        header += "═" * cols + "\n"
        header += f" DiOS {self.version} Desktop ".center(cols, " ") + "\n"
        header += "═" * cols + reset_col
        print(header)

        # Вычисляем доступное место для буфера команд
        available_lines = lines - 6  # Header(3) + Taskbar(2) + Input(1)

        # Сохраняем только последние N строк буфера
        if len(self.screen_buffer) > available_lines:
            self.screen_buffer = self.screen_buffer[-available_lines:]

        # Печатаем буфер с учетом фона
        for line in self.screen_buffer:
            print(f"{bg_col}{line}{reset_col}")

        # Заполняем пустое пространство, чтобы прибить панель задач к низу
        empty_lines = available_lines - len(self.screen_buffer)
        for _ in range(empty_lines):
            print(f"{bg_col}{' ' * cols}{reset_col}")

        # ПАНЕЛЬ ЗАДАЧ
        taskbar_theme = THEMES.get(self.user_data.get("taskbar_color", "cyber"), "")
        now = datetime.now().strftime("%H:%M")
        tb_text = f" [1: Sysinfo] | [settings] | [store] | [messages] ".ljust(cols - 10) + f"[{now}] "

        print(f"{taskbar_theme}█{'▀' * (cols - 2)}█{reset_col}")
        print(f"{taskbar_theme}█{tb_text}█{reset_col}")

    # --- CORE LOGIC ---
    def execute_command(self, cmd_str):
        parts = shlex.split(cmd_str)
        if not parts: return
        cmd = parts[0].lower()

        self._print_buf(f"{self.user} > {cmd_str}")

        if cmd == "help":
            for line in self.help_text.split('\n'):
                if line.strip(): self._print_buf(line)
        elif cmd in ["clear", "refresh"]:
            self.screen_buffer.clear()
        elif cmd == "settings":
            self.run_settings()
        elif cmd == "store":
            self.run_store()
        elif cmd == "hide_seek":
            self.play_hide_seek()
        elif cmd == "browser":
            self.run_browser()
        elif cmd == "calc":
            self.run_calculator()
        elif cmd == "messages":
            self.run_messages()
        elif cmd == "antivirus":
            self.run_antivirus()
        elif cmd == "construction":
            self.run_construction_sim()
        elif cmd == "edit":
            if len(parts) > 1:
                self.edit_file(parts[1])
            else:
                self._print_buf("Usage: edit <filename>")
        elif cmd == "3":
            self._print_buf("Shutting down...")
            self.running = False
        else:
            self._print_buf(f"Command executed: {cmd} (или открой help)")

    def run(self):
        if not self.load_system():
            self.first_time_setup()
        else:
            self.login()

        self.screen_buffer.append(f"Welcome to DiOS {self.version}")
        self.screen_buffer.append("Type 'help' for a detailed list.")

        # Main Desktop Loop
        while self.running:
            self.render_desktop()
            cmd = input(f"{self.theme_prefix}Type command > \033[0m").strip()
            if cmd:
                self.execute_command(cmd)


if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
    finally:
        print("\n[System successfully powered down]")
        input("[Press Enter to close the window...]")
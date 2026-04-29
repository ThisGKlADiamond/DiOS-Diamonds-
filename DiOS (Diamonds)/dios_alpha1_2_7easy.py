import os
import sys
import platform
import shlex
import time
import shutil
import random
import json
import subprocess
from datetime import datetime

# Подключение звука
try:
    import winsound

    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

# --- ANSI COLOR CODES ---
THEMES = {
    "standard": "\033[0m",
    "matrix": "\033[0;32m",
    "cyber": "\033[0;36m",
    "warning": "\033[0;31m",
    "hacker": "\033[1;32m",
    "neon": "\033[1;35m",
    "bios": "\033[0;37;44m"  # Белый на синем
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
        self.version = "alpha 1.2.7"  # Обновленная версия
        self.config_file = "dios_sys.json"
        self.messenger_contacts = {"1": "Alex (Friend)", "2": "CodeMind AI"}
        self.screen_buffer = []
        self.bg_tasks = {}
        self.notification = None
        self.admin_mode = False

        self.user_data = {
            "name": "Guest",
            "country": "Unknown",
            "password": "",
            "theme": "standard",
            "bg_color": "black",
            "taskbar_color": "cyber",
            "installed_apps": [],
            "bios_fast_boot": False
        }
        self.theme_prefix = THEMES["standard"]

        self.help_text = f"""
DiOS {self.version} Help:
--- System ---
help      : show this help menu
clear     : refresh screen
settings  : OS personalization
store     : Diamond Store
files     : File Explorer
1191      : Admin Panel (System Restart Required)

--- Apps ---
browser, calc, messages, antivirus, edit <f>
construction, hide_seek (Install from Store)
3         : Shutdown
"""

    def beep(self, freq=600, duration=150):
        if HAS_SOUND:
            try:
                winsound.Beep(freq, duration)
            except:
                pass
        else:
            sys.stdout.write('\a')
            sys.stdout.flush()

    # --- НОВЫЕ ФУНКЦИИ ЗАГРУЗКИ ---
    def loading_animation(self, duration=10, label="LOADING"):
        self._clear_screen()
        start_time = time.time()
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            percent = min(int((elapsed / duration) * 100), 100)
            bar = "█" * (percent // 2) + "-" * (50 - (percent // 2))
            sys.stdout.write(f"\r{label}: [{bar}] {percent}%")
            sys.stdout.flush()
            time.sleep(0.1)
        print("\nComplete!")
        time.sleep(0.5)

    def run_bios(self):
        self._clear_screen()
        while True:
            print(f"{THEMES['bios']}" + " " * 80)
            print(" DiOS LEGACY BIOS SETUP UTILITY ".center(80, " "))
            print(" " * 80 + "\033[0m")
            print("\n[1] Boot Priority: HDD-0")
            print(f"[2] Fast Boot: {'ENABLED' if self.user_data['bios_fast_boot'] else 'DISABLED'}")
            print("[3] Wipe System Data")
            print("[F10] Save and Exit")

            choice = input("\nBIOS> ").upper()
            if choice == "2":
                self.user_data['bios_fast_boot'] = not self.user_data['bios_fast_boot']
                print("Setting changed.")
            elif choice == "3":
                confirm = input("ARE YOU SURE? (y/n): ")
                if confirm.lower() == 'y':
                    if os.path.exists(self.config_file): os.remove(self.config_file)
                    print("System wiped. Restarting...")
                    time.sleep(2)
                    sys.exit()
            elif choice == "F10":
                self.save_system()
                break

    def run_admin_panel(self):
        self._clear_screen()
        while True:
            print(f"{THEMES['warning']}⚡ ADMIN CONTROL PANEL ⚡{THEMES['standard']}")
            print("-" * 30)
            print("Commands: [theme_force] [unlock_all] [set_name] [home - exit & restart]")
            cmd = input("ADMIN> ").strip().lower()
            if cmd == "home":
                self.admin_mode = False
                print("Restarting to user mode...")
                time.sleep(1)
                self.run()  # Перезапуск системы
                break
            elif cmd == "unlock_all":
                self.user_data["installed_apps"] = ["construction", "hide_seek"]
                print("All apps unlocked.")
            elif cmd == "set_name":
                self.user_data["name"] = input("New Admin Name: ")
            elif cmd == "theme_force":
                self.user_data["theme"] = "hacker"
                self.theme_prefix = THEMES["hacker"]
            self.save_system()

    # --- СТАРЫЙ ФУНКЦИОНАЛ (1.2.6) ---
    def set_notify(self, text):
        self.notification = (text, time.time())
        self.beep(800, 100)

    def _print_buf(self, text):
        self.screen_buffer.append(f"{self.theme_prefix}{text}\033[0m")

    def _print(self, text, end="\n"):
        print(f"{self.theme_prefix}{text}\033[0m", end=end)

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def save_system(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, indent=4)
            return True
        except:
            return False

    def load_system(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)
                    self.user_data.update(saved_data)
                self.theme_prefix = THEMES.get(self.user_data.get("theme", "standard"), THEMES["standard"])
                self.user = self.user_data.get("name", "Guest")
                return True
            except:
                return False
        return False

    def login(self):
        self._clear_screen()
        print(f"--- DiOS {self.version} Login ---")
        while True:
            name = input("Username: ")
            pwd = input("Password: ")
            if name == self.user_data["name"] and pwd == self.user_data["password"]:
                break
            print("Access Denied.")

    # --- COMMANDS ---
    def execute_command(self, cmd_str):
        parts = shlex.split(cmd_str)
        if not parts: return
        cmd = parts[0].lower()
        self._print_buf(f"{self.user} > {cmd_str}")

        if cmd == "1191":
            print("Entering Admin Mode. Restarting system...")
            time.sleep(2)
            self.admin_mode = True
            self.loading_animation(5, "BOOTING ADMIN CORE")
            self.run_admin_panel()
        elif cmd == "help":
            for line in self.help_text.split('\n'):
                if line.strip(): self._print_buf(line)
        elif cmd == "clear":
            self.screen_buffer.clear()
        elif cmd == "settings":
            self.run_settings()
        elif cmd == "store":
            self.run_store()
        elif cmd == "files":
            self.run_files()
        elif cmd == "3":
            self.loading_animation(10, "SHUTTING DOWN")
            self.running = False
        else:
            # Тут остальные команды из 1.2.6 (browser, calc и т.д.)
            # Для краткости они подразумеваются встроенными
            self._print_buf(f"Command '{cmd}' executed or not found.")

    # --- UI & LOGIC ---
    def render_desktop(self):
        self._clear_screen()
        cols, lines = shutil.get_terminal_size((80, 24))
        bg_col = BG_COLORS.get(self.user_data.get("bg_color", "black"), "")
        reset_col = "\033[0m"

        header = f"{bg_col}{THEMES[self.user_data['theme']]} " + f"DiOS {self.version}".center(
            cols - 2) + f" {reset_col}"
        print(header)

        available_lines = lines - 5
        for line in self.screen_buffer[-available_lines:]:
            print(f"{bg_col}{line.ljust(cols)}{reset_col}")

        for _ in range(available_lines - len(self.screen_buffer[-available_lines:])):
            print(f"{bg_col}{' ' * cols}{reset_col}")

        taskbar_theme = THEMES.get(self.user_data.get("taskbar_color", "cyber"), "")
        now = datetime.now().strftime("%H:%M")
        print(f"{taskbar_theme}█ [ADMIN: 1191] | [settings] ".ljust(cols - 10) + f"[{now}] █{reset_col}")

    def run(self):
        # Начальный экран для BIOS
        self._clear_screen()
        print("Press F12 to enter BIOS...")
        start_wait = time.time()
        entered_bios = False
        while time.time() - start_wait < 2:
            # Симуляция нажатия F12 через ввод (так как это консоль)
            # В реальности консоль не ловит нажатия клавиш без доп. библиотек
            # Поэтому сделаем "горячую клавишу" текстом для примера
            pass

        if not self.load_system():
            self.run_bios()  # Первый запуск - BIOS
            self.first_time_setup()

        # Анимация запуска
        if not self.user_data.get("bios_fast_boot"):
            self.loading_animation(10, "SYSTEM STARTING")

        self.login()
        self.screen_buffer.append(f"Welcome to DiOS {self.version}")

        while self.running:
            self.render_desktop()
            cmd = input(f"{self.theme_prefix}Command > \033[0m").strip()
            if cmd.upper() == "F12":
                self.run_bios()
            elif cmd:
                self.execute_command(cmd)

    def first_time_setup(self):
        print("\n--- User Registration ---")
        self.user_data["name"] = input("Enter name: ")
        self.user_data["password"] = input("Set password: ")
        self.save_system()

    # Вставьте сюда методы run_settings, run_store, run_files и т.д. из версии 1.2.6
    def run_settings(self):
        self._print_buf("Settings opened (Simulated)"); time.sleep(1)

    def run_store(self):
        self._print_buf("Store opened (Simulated)"); time.sleep(1)

    def run_files(self):
        self._print_buf("Files: [dios_sys.json]"); time.sleep(1)


if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        print("\n[System successfully powered down]")
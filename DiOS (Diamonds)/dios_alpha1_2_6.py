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

# Подключение звука (только для Windows, чтобы не крашилось на Mac/Linux)
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
        self.version = "alpha 1.2.6"
        self.config_file = "dios_sys.json"
        self.messenger_contacts = {"1": "Alex (Friend)", "2": "CodeMind AI"}
        self.screen_buffer = []

        # Многозадачность и уведомления
        self.bg_tasks = {}  # Хранит состояния свернутых приложений
        self.notification = None  # (текст, время)

        # Base user data (старые данные из 1.2.4)
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
files     : File Explorer (View files in folder)

--- Apps & Social ---
browser   : DiOS Web Browser (Supports minimize)
calc      : launch Calculator (Supports minimize)
messages  : messenger
antivirus : system security
edit <f>  : text editor

--- Entertainment (Must install from Store) ---
construction : city builder
hide_seek : 3D Hide & Seek (Powered by Ursina)
"""

    def beep(self, freq=600, duration=150):
        """Воспроизведение системных звуков"""
        if HAS_SOUND:
            try:
                winsound.Beep(freq, duration)
            except:
                pass
        else:
            sys.stdout.write('\a')
            sys.stdout.flush()

    def set_notify(self, text):
        """Устанавливает уведомление для панели задач"""
        self.notification = (text, time.time())
        self.beep(800, 100)  # Короткий звук уведомления

    def _print_buf(self, text):
        self.screen_buffer.append(f"{self.theme_prefix}{text}\033[0m")

    def _print(self, text, end="\n"):
        print(f"{self.theme_prefix}{text}\033[0m", end=end)

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # --- PERSISTENCE (Сохранение без ошибок из 1.2.4) ---
    def save_system(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, indent=4)
            self.set_notify("💾 Система сохранена")
            return True
        except PermissionError:
            print(
                f"\n{THEMES['warning']}[ВНИМАНИЕ] Ошибка доступа (Errno 13)! Не удалось сохранить {self.config_file}.\033[0m")
            time.sleep(2)
            return False
        except Exception as e:
            return False

    def load_system(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)
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

    # --- INSTALLATION & LOGIN (С Хакерской Анимацией) ---
    def first_time_setup(self):
        self._clear_screen()
        print("⚡ DiOS INSTALLATION WIZARD ⚡")
        print("-" * 30)
        time.sleep(1)
        for i in range(4):
            time.sleep(0.5)
            print(f"Progress: {(i + 1) * 25}%...")

        print("\n--- User Registration ---")
        self.user_data["name"] = input("Enter your name: ").strip()
        self.user_data["country"] = input("Enter your country: ").strip()

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

    def hacker_animation(self):
        """Анимация загрузки при входе"""
        self._clear_screen()
        colors = [THEMES["matrix"], THEMES["hacker"], "\033[0;32m"]
        for _ in range(25):
            line = "".join(random.choice("0123456789ABCDEF!@#$%^&*") for _ in range(70))
            print(f"{random.choice(colors)}{line}\033[0m")
            time.sleep(0.04)
        self._clear_screen()

    def login(self):
        self.hacker_animation()
        self.beep(1000, 300)
        print(f"--- DiOS {self.version} Login ---")
        while True:
            name = input("Username: ")
            pwd = input("Password: ")
            if name == self.user_data["name"] and pwd == self.user_data["password"]:
                print(f"\nWelcome back, {name}!")
                time.sleep(1)
                self.set_notify(f"👋 Добро пожаловать, {name}")
                break
            self.beep(300, 400)
            print("Access Denied.\n")

    # --- ФАЙЛОВЫЙ МЕНЕДЖЕР ---
    def run_files(self):
        self._print_buf(f"--- FILE EXPLORER: {self.current_dir} ---")
        try:
            items = os.listdir(self.current_dir)
            for item in items:
                if os.path.isdir(item):
                    self._print_buf(f"📂 {item}/")
                else:
                    if item.endswith('.py'):
                        icon = "🐍"
                    elif item.endswith('.txt'):
                        icon = "📄"
                    elif item.endswith('.json'):
                        icon = "⚙️"
                    else:
                        icon = "🗄️"
                    self._print_buf(f"{icon} {item}")
        except Exception as e:
            self._print_buf(f"Ошибка чтения папки: {e}")

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

            elif c == '3':
                self._clear_screen()
                print("--- OS WALLPAPER (BACKGROUND) ---")
                print("[1] Black (Default) [2] Blue [3] Magenta [4] Cyan [5] White")
                bg = input("Choice: ")
                bg_map = {"1": "black", "2": "blue", "3": "magenta", "4": "cyan", "5": "white"}
                if bg in bg_map:
                    self.user_data["bg_color"] = bg_map[bg]
                    self.save_system()

    # --- URSINA 3D GAME (HIDE IN SEEK) ---
    def play_hide_seek(self):
        if "hide_seek" not in self.user_data.get("installed_apps", []):
            self._print_buf("Error: App not installed. Visit Diamond Store.")
            self.beep(300, 200)
            return

        self._clear_screen()
        print("🚀 Launching Hide In Seek 3D Engine...")
        time.sleep(1.5)

        game_code = """
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()
ground = Entity(model='plane', scale=(50, 1, 50), color=color.green, texture='white_cube', texture_scale=(50, 50), collider='box')
Sky()

for i in range(15):
    Entity(model='cube', color=color.gray, scale=(random.randint(2, 6), random.randint(3, 6), 1),
           position=(random.randint(-20, 20), 2, random.randint(-20, 20)), collider='box')

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
            input("Press Enter...")

    # --- STORE ---
    def run_store(self):
        self._clear_screen()
        self._print("💎 DIAMOND STORE 💎")
        apps = {"1": ["Construction Simulator", "construction"], "2": ["Hide In Seek 3D", "hide_seek"]}
        for k, v in apps.items():
            status = "[Installed]" if v[1] in self.user_data["installed_apps"] else "[Free]"
            print(f"[{k}] {v[0]} {status}")

        choice = input("\nSelect App ID to Install (or Q): ").strip()
        if choice in apps:
            app_id = apps[choice][1]
            if app_id not in self.user_data["installed_apps"]:
                print(f"Downloading {apps[choice][0]}...")
                time.sleep(2)
                self.user_data["installed_apps"].append(app_id)
                self.save_system()

    # --- BROWSER (Многозадачность добавлена) ---
    def run_browser(self):
        self._clear_screen()
        self._print(f"🌐 DiOS BROWSER v{self.version}")

        # Восстановление сессии
        if 'browser_url' in self.bg_tasks:
            print(f"[Restored Session: {self.bg_tasks['browser_url']}]")

        while True:
            print("\nType 'min' to minimize, 'q' to quit.")
            url = input("URL > ").lower().strip()

            if url == 'q':
                self.bg_tasks.pop('browser_url', None)  # очищаем сессию
                break
            elif url == 'min':
                self.set_notify("🌐 Браузер свернут")
                break  # Выход в главное меню, сессия сохранена
            elif url:
                self.bg_tasks['browser_url'] = url  # Сохраняем стейт
                print("-" * 30)
                if "dios.com" in url:
                    print("Welcome to DiOS Official!")
                elif "tgk.studio" in url:
                    print("TGK DiamondCraft Studios")
                else:
                    print("404 Error: Page not found.")

    # --- CALCULATOR (Многозадачность добавлена) ---
    def run_calculator(self):
        self._clear_screen()
        print("🔢 DiOS Calculator")

        if 'calc_mode' in self.bg_tasks:
            mode = self.bg_tasks['calc_mode']
            print(f"[Restored Mode: {'Standard' if mode == '1' else 'Programmer'}]")
        else:
            print("Modes: [1] Standard  [2] Programmer")
            mode = input("Select Mode: ").strip()
            self.bg_tasks['calc_mode'] = mode

        print("Type 'min' to minimize, 'q' to quit.")
        while True:
            if mode == "1":
                expr = input("Calc > ").strip()
                if expr == 'q': self.bg_tasks.pop('calc_mode', None); break
                if expr == 'min': self.set_notify("🔢 Калькулятор свернут"); break
                try:
                    print(f"Result: {eval(expr)}")
                except:
                    print("Error.")
            elif mode == "2":
                val = input("DEC Number > ").strip()
                if val == 'q': self.bg_tasks.pop('calc_mode', None); break
                if val == 'min': self.set_notify("🔢 Калькулятор свернут"); break
                if val.isdigit(): print(f"HEX: {hex(int(val))} | BIN: {bin(int(val))}")

    # --- CONSTRUCTION ---
    def run_construction_sim(self):
        if "construction" not in self.user_data.get("installed_apps", []):
            self._print_buf("Error: App not installed.")
            return
        self._clear_screen()
        print("🏗️  Construction Simulator\n[1] New Game  [Q] Exit")
        if input("> ").lower() == "1":
            pop = 0
            while pop < 20:
                print(f"\nPop: {pop} | [H] Place House (+5) [Q] Exit")
                if input("> ").lower() == 'h':
                    pop += 5; print("Built!")
                elif input("> ").lower() == 'q':
                    break
            if pop >= 20: print("\n🏆 You won!")
            input("Press Enter...")

    def run_messages(self):
        self._clear_screen()
        print(f"💬 DiOS Messenger")
        for k, v in self.messenger_contacts.items(): print(f"[{k}] {v}")
        print("\n[+] Add Contact  [Q] Exit")
        choice = input("> ").strip().lower()
        if choice == '+':
            name = input("Name: ")
            self.messenger_contacts[str(len(self.messenger_contacts) + 1)] = name
        elif choice == '2':
            input("You: ")
            print("AI: ```python\nprint('Hello')\n```")
            time.sleep(2)

    def run_antivirus(self):
        self._clear_screen()
        print("🛡️  Antivirus\n[1] Scan [2] Clean Cache")
        c = input("> ")
        if c == "1": print("Scanning..."); time.sleep(1); print("Clean!")
        input("Press Enter...")

    def edit_file(self, filename):
        if not os.path.exists(filename):
            with open(filename, "w") as f: pass
        with open(filename, "r") as f:
            lines = f.readlines()
        while True:
            self._clear_screen()
            for idx, line in enumerate(lines): print(f"{idx + 1}: {line.strip()}")
            cmd = input("\n[s] save | [a] add line | [q] exit > ").strip().lower()
            if cmd == 'q':
                break
            elif cmd == 's':
                with open(filename, "w") as f:
                    f.writelines(lines)
                self.set_notify("📝 Файл сохранен")
                break
            elif cmd == 'a':
                lines.append(input("New line: ") + "\n")

    # --- CORE UI RENDERER (С уведомлениями) ---
    def render_desktop(self):
        self._clear_screen()
        cols, lines = shutil.get_terminal_size((80, 24))
        bg_col = BG_COLORS.get(self.user_data.get("bg_color", "black"), "")
        reset_col = "\033[0m"

        header = f"{bg_col}{THEMES[self.user_data['theme']]}"
        header += "═" * cols + "\n"
        header += f" DiOS {self.version} Desktop ".center(cols, " ") + "\n"
        header += "═" * cols + reset_col
        print(header)

        available_lines = lines - 6
        if len(self.screen_buffer) > available_lines:
            self.screen_buffer = self.screen_buffer[-available_lines:]

        for line in self.screen_buffer: print(f"{bg_col}{line}{reset_col}")
        for _ in range(available_lines - len(self.screen_buffer)):
            print(f"{bg_col}{' ' * cols}{reset_col}")

        # УВЕДОМЛЕНИЯ В ПАНЕЛИ ЗАДАЧ
        notif_str = ""
        if self.notification:
            text, t_stamp = self.notification
            if time.time() - t_stamp < 4.0:  # Показываем 4 секунды
                notif_str = f" | {text}"

        taskbar_theme = THEMES.get(self.user_data.get("taskbar_color", "cyber"), "")
        now = datetime.now().strftime("%H:%M")
        tb_text = f" [1: Sysinfo] | [settings] | [files] | [browser]{notif_str} "
        tb_text = tb_text.ljust(cols - 10)[:cols - 10] + f"[{now}] "

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
        elif cmd == "files":
            self.run_files()
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
        elif cmd == "hide_seek":
            self.play_hide_seek()
        elif cmd == "edit":
            if len(parts) > 1:
                self.edit_file(parts[1])
            else:
                self._print_buf("Usage: edit <filename>")
        elif cmd == "3":
            self._print_buf("Shutting down...")
            self.running = False
        else:
            self._print_buf(f"Команда не найдена: {cmd}")
            self.beep(400, 250)  # Звук ошибки

    def run(self):
        if not self.load_system():
            self.first_time_setup()
        else:
            self.login()

        self.screen_buffer.append(f"Welcome to DiOS {self.version}")

        while self.running:
            self.render_desktop()
            cmd = input(f"{self.theme_prefix}Type command > \033[0m").strip()
            if cmd: self.execute_command(cmd)


if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        print("\n[System successfully powered down]")
        input("[Press Enter to close...]")
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
        self.version = "alpha 1.2.5"
        self.config_file = "dios_sys.json"
        self.messenger_contacts = {"1": "Alex (Friend)", "2": "CodeMind AI"}
        self.screen_buffer = []

        # Данные пользователя (Persistence)
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

        # Иконки для команд
        self.icons = {
            "help": "❓", "clear": "🧹", "settings": "⚙️", "store": "💎",
            "browser": "🌐", "calc": "🔢", "antivirus": "🛡️", "messages": "💬",
            "gallery": "🖼️", "edit": "📝", "games": "🕹️", "construction": "🏗️",
            "hide_seek": "🏃", "debug": "🛠️", "exit": "🔌"
        }

        self.help_text = f"""
DiOS {self.version} Меню команд:
--- Система ---
{self.icons['help']} help      : помощь
{self.icons['clear']} clear     : очистить экран
{self.icons['settings']} settings  : персонализация и инфо
{self.icons['debug']} debug     : список ВСЕХ команд (Dev Mode)
{self.icons['store']} store     : Diamond Store

--- Приложения ---
{self.icons['browser']} browser   : веб-браузер
{self.icons['calc']} calc      : калькулятор
{self.icons['messages']} messages  : мессенджер
{self.icons['edit']} edit <f>  : текстовый редактор
{self.icons['antivirus']} antivirus : защита системы

--- Развлечения ---
{self.icons['construction']} construction : симулятор стройки
{self.icons['hide_seek']} hide_seek    : 3D Прятки (Ursina)
"""

    def _print_buf(self, text):
        self.screen_buffer.append(f"{self.theme_prefix}{text}\033[0m")

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # --- PERSISTENCE ---
    def save_system(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, indent=4)
            return True
        except PermissionError:
            print(f"\n{THEMES['warning']}[Errno 13] Ошибка доступа к {self.config_file}\033[0m")
            time.sleep(2)
            return False

    def load_system(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)
                    for k, v in self.user_data.items():
                        if k not in saved_data: saved_data[k] = v
                    self.user_data = saved_data
                self.theme_prefix = THEMES.get(self.user_data.get("theme", "standard"), THEMES["standard"])
                self.user = self.user_data.get("name", "Guest")
                return True
            except:
                return False
        return False

    # --- DEBUG COMMAND ---
    def run_debug(self):
        self._print_buf("--- [INTERNAL DEBUG MODE] ---")
        self._print_buf(f"System Version: {self.version}")
        self._print_buf(f"Current Path: {self.current_dir}")
        self._print_buf("Registered Commands:")
        all_cmds = ["help", "clear", "settings", "store", "browser", "calc", "messages",
                    "antivirus", "construction", "hide_seek", "edit", "debug", "3 (exit)", "refresh"]
        for c in all_cmds:
            icon = self.icons.get(c.split()[0], "🔹")
            self._print_buf(f" > {icon} {c}")
        self._print_buf(f"Installed Apps Data: {self.user_data['installed_apps']}")

    # --- SETTINGS, STORE, GAMES (Логика из 1.2.4) ---
    def run_settings(self):
        while True:
            self._clear_screen()
            print(f"{self.icons['settings']} DiOS SETTINGS")
            print("[1] System Info\n[2] Themes\n[3] Wallpaper\n[Q] Exit")
            c = input("> ").lower()
            if c == 'q': break
            if c == '1':
                self._clear_screen()
                print(f"User: {self.user}\nOS: DiOS {self.version}\nHost: {platform.node()}")
                input("\nEnter...")
            elif c == '2':
                print("1: Standard, 2: Matrix, 3: Cyber, 4: Hacker, 5: Neon")
                tc = input("Choice: ")
                colors = {"1": "standard", "2": "matrix", "3": "cyber", "4": "hacker", "5": "neon"}
                if tc in colors:
                    self.user_data["theme"] = colors[tc]
                    self.theme_prefix = THEMES[colors[tc]]
                    self.save_system()

    def play_hide_seek(self):
        if "hide_seek" not in self.user_data.get("installed_apps", []):
            self._print_buf("Ошибка: Игра не установлена в Store.")
            return
        self._print_buf("Запуск 3D движка Ursina...")
        # (Код генерации dios_hideseek_3d.py аналогичен 1.2.4)
        subprocess.run(["python", "-c", "print('3D Engine Simulation...')"])
        time.sleep(1)

    # --- CORE UI RENDERER ---
    def render_desktop(self):
        self._clear_screen()
        cols, lines = shutil.get_terminal_size((80, 24))
        bg_col = BG_COLORS.get(self.user_data.get("bg_color", "black"), "")
        reset_col = "\033[0m"

        # Header
        print(f"{bg_col}{THEMES[self.user_data['theme']]}═" * cols)
        print(f" {self.icons['settings']} DiOS {self.version} | User: {self.user} ".center(cols, " "))
        print("═" * cols + reset_col)

        # Буфер контента
        available_lines = lines - 6
        if len(self.screen_buffer) > available_lines:
            self.screen_buffer = self.screen_buffer[-available_lines:]

        for line in self.screen_buffer:
            print(f"{bg_col}{line}{reset_col}")

        for _ in range(available_lines - len(self.screen_buffer)):
            print(f"{bg_col}{' ' * cols}{reset_col}")

        # Taskbar
        taskbar_theme = THEMES.get(self.user_data.get("taskbar_color", "cyber"), "")
        now = datetime.now().strftime("%H:%M")
        tb_text = f" {self.icons['debug']} [debug] | {self.icons['store']} [store] | {self.icons['messages']} [messages] ".ljust(
            cols - 10) + f"[{now}]"
        print(f"{taskbar_theme}█{'▀' * (cols - 2)}█{reset_col}")
        print(f"{taskbar_theme}█{tb_text}█{reset_col}")

    def execute_command(self, cmd_str):
        parts = shlex.split(cmd_str)
        if not parts: return
        cmd = parts[0].lower()

        # Добавляем в лог с иконкой
        icon = self.icons.get(cmd, "👉")
        self._print_buf(f"{icon} {self.user} > {cmd_str}")

        if cmd == "help":
            for line in self.help_text.split('\n'):
                if line.strip(): self._print_buf(line)
        elif cmd in ["clear", "refresh"]:
            self.screen_buffer.clear()
        elif cmd == "debug":
            self.run_debug()
        elif cmd == "settings":
            self.run_settings()
        elif cmd == "hide_seek":
            self.play_hide_seek()
        elif cmd == "3":
            self._print_buf(f"{self.icons['exit']} Выключение...")
            self.running = False
        else:
            self._print_buf(f"Система: Команда '{cmd}' не найдена. Введите 'help'.")

    def run(self):
        if not self.load_system():
            # Упрощенная регистрация для примера
            print("--- DiOS First Boot ---")
            self.user_data["name"] = input("Name: ")
            self.user_data["password"] = "1234"
            self.save_system()

        self.user = self.user_data["name"]
        self.screen_buffer.append(f"Welcome to DiOS {self.version}")

        while self.running:
            self.render_desktop()
            # Имитация курсора [█]
            prompt = f"{self.theme_prefix}{self.user}@dios:~$ \033[5m█\033[0m "
            try:
                cmd = input(prompt).strip()
                if cmd: self.execute_command(cmd)
            except EOFError:
                break


if __name__ == "__main__":
    dios = DiOS()
    dios.run()
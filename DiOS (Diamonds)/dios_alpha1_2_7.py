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

# Подключение звука и системных клавиш (для Windows)
try:
    import winsound
    import msvcrt

    HAS_WINDOWS_API = True
except ImportError:
    HAS_WINDOWS_API = False

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
        self.version = "alpha 1.2.7"
        self.config_file = "dios_sys.json"
        self.messenger_contacts = {"1": "Alex (Friend)", "2": "CodeMind AI"}
        self.screen_buffer = []

        # Системные состояния
        self.power_on = True
        self.current_state = "boot"  # Состояния: boot, bios, os, admin, shutdown

        # Многозадачность и уведомления
        self.bg_tasks = {}
        self.notification = None

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
files     : File Explorer (View files)

--- Apps & Social ---
browser   : DiOS Web Browser (Supports minimize)
calc      : launch Calculator (Supports minimize)
messages  : messenger
antivirus : system security
edit <f>  : text editor

--- Entertainment ---
construction : city builder
hide_seek : 3D Hide & Seek (Ursina)
"""

    def beep(self, freq=600, duration=150):
        if HAS_WINDOWS_API:
            try:
                winsound.Beep(freq, duration)
            except:
                pass
        else:
            sys.stdout.write('\a')
            sys.stdout.flush()

    def set_notify(self, text):
        self.notification = (text, time.time())
        self.beep(800, 100)

    def _print_buf(self, text):
        self.screen_buffer.append(f"{self.theme_prefix}{text}\033[0m")

    def _print(self, text, end="\n"):
        print(f"{self.theme_prefix}{text}\033[0m", end=end)

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # --- PERSISTENCE ---
    def save_system(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, indent=4)
            self.set_notify("💾 Система сохранена")
            return True
        except PermissionError:
            print(f"\n{THEMES['warning']}[Errno 13] Ошибка доступа к {self.config_file}\033[0m")
            time.sleep(2)
            return False
        except Exception:
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

    # --- BIOS & BOOT ANIMATION (10 Seconds) ---
    def check_f12(self):
        """Проверка нажатия F12 на Windows"""
        if HAS_WINDOWS_API and msvcrt.kbhit():
            key = msvcrt.getch()
            if key in (b'\x00', b'\xe0'):
                if msvcrt.kbhit():
                    keycode = msvcrt.getch()
                    if keycode == b'\x86':  # Код клавиши F12
                        return True
        return False

    def boot_sequence(self, target_state="os"):
        self._clear_screen()
        print(f"{THEMES['cyber']}--- TGK BIOS v1.0.4 ---{THEMES['standard']}")
        print("Initializing Hardware...")
        self.beep(1200, 200)

        boot_time = 10.0  # 10 секунд загрузки
        start_time = time.time()
        modules = ["CPU Logs", "RAM Check", "Mounting Storage", "Loading Kernel", "Loading UI", "Mounting FS",
                   "Init Drivers"]

        entered_bios = False

        while time.time() - start_time < boot_time:
            elapsed = time.time() - start_time
            progress = int((elapsed / boot_time) * 100)
            bar = "█" * (progress // 2) + "-" * (50 - (progress // 2))

            # Рандомный вывод логов для красоты
            if random.random() > 0.8:
                mod = random.choice(modules)
                sys.stdout.write(f"\r[OK] {mod} loaded at {hex(random.randint(0x1000, 0xFFFF))}\n")

            sys.stdout.write(f"\r{THEMES['matrix']}[{bar}] {progress}% | Press F12 for BIOS...{THEMES['standard']}")
            sys.stdout.flush()

            # Проверка F12
            if not entered_bios and self.check_f12():
                entered_bios = True
                break

            time.sleep(0.1)

        print("\n\nBoot sequence complete.")
        time.sleep(0.5)

        if entered_bios:
            self.current_state = "bios"
        else:
            self.current_state = target_state

    def shutdown_sequence(self, target_state="power_off"):
        self._clear_screen()
        self.beep(400, 300)
        print(f"{THEMES['warning']}Initiating System Shutdown...{THEMES['standard']}")

        shutdown_time = 10.0
        start_time = time.time()
        tasks = ["Stopping processes", "Saving user data", "Unmounting disk", "Powering off CPU"]

        while time.time() - start_time < shutdown_time:
            elapsed = time.time() - start_time
            progress = int((elapsed / shutdown_time) * 100)
            bar = "█" * (progress // 2) + "-" * (50 - (progress // 2))

            if random.random() > 0.85:
                task = random.choice(tasks)
                sys.stdout.write(f"\r[INFO] {task}... OK\n")

            sys.stdout.write(f"\r{THEMES['warning']}[{bar}] {progress}% {THEMES['standard']}")
            sys.stdout.flush()
            time.sleep(0.1)

        print("\nSystem Halted. Safe to power off.")
        time.sleep(1)
        self.current_state = target_state

    def run_bios(self):
        while True:
            self._clear_screen()
            print(f"{THEMES['blue']}======================================")
            print("        TGK DiOS BIOS UTILITY         ")
            print("======================================")
            print("1. System Information")
            print("2. Boot Priority")
            print("3. Hardware Monitor (Temperatures)")
            print("4. Exit & Reboot into OS")
            print("======================================\033[0m")

            c = input("Select > ")
            if c == '1':
                print(f"OS Version: DiOS {self.version}")
                print(f"CPU Arch: {platform.machine()}")
                input("Press Enter...")
            elif c == '2':
                print("[1] DiOS Virtual Drive (Primary)")
                print("[2] Network Boot (PXE)")
                input("Press Enter...")
            elif c == '3':
                print(f"CPU Temp: {random.randint(35, 45)}°C")
                print("Fan Speed: 1200 RPM")
                input("Press Enter...")
            elif c == '4':
                self.current_state = "boot"  # Перезагрузка
                break

    # --- ADMIN PANEL ---
    def run_admin_panel(self):
        self._clear_screen()
        self.beep(1000, 500)
        while True:
            print(f"{THEMES['warning']}--- DiOS ROOT ADMIN PANEL ---")
            print("Warning: Direct system modification active.")
            print("[users] View user database | [logs] System Logs")
            print("[reset] Factory reset OS   | [home] Reboot to OS")

            cmd = input("root@dios:~# ").strip().lower()
            if cmd == "home":
                self.current_state = "shutdown_to_os"
                break
            elif cmd == "users":
                print(f"Registered User: {self.user_data['name']}")
                print(f"Password Hash: {'*' * len(self.user_data['password'])}")
            elif cmd == "logs":
                print("Loading logs...")
                for i in range(5): print(f"kernel: memory block {hex(i * 2048)} clear")
            elif cmd == "reset":
                confirm = input("Type 'YES' to delete all data: ")
                if confirm == "YES":
                    if os.path.exists(self.config_file): os.remove(self.config_file)
                    print("System reset. Rebooting...")
                    self.current_state = "boot"
                    break
            else:
                print("Unknown command.")
            print("\033[0m")

    # --- INSTALLATION & LOGIN ---
    def first_time_setup(self):
        self._clear_screen()
        print("⚡ DiOS INSTALLATION WIZARD ⚡")
        print("-" * 30)
        time.sleep(1)
        self.user_data["name"] = input("Enter your name: ").strip()
        self.user_data["country"] = input("Enter your country: ").strip()

        while True:
            pwd = input("Set password: ")
            conf = input("Confirm password: ")
            if pwd == conf:
                self.user_data["password"] = pwd
                break
        self.user = self.user_data["name"]
        self.save_system()
        print("Installation successful! Restarting...")
        time.sleep(2)

    def hacker_animation(self):
        self._clear_screen()
        colors = [THEMES["matrix"], THEMES["hacker"], "\033[0;32m"]
        for _ in range(15):
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
                self.set_notify(f"👋 Добро пожаловать, {name}")
                break
            self.beep(300, 400)
            print("Access Denied.\n")

    # --- APPS & FUNCTIONS (From 1.2.6) ---
    def run_files(self):
        self._print_buf(f"--- FILE EXPLORER: {self.current_dir} ---")
        try:
            for item in os.listdir(self.current_dir):
                icon = "📂" if os.path.isdir(item) else "🐍" if item.endswith('.py') else "⚙️" if item.endswith(
                    '.json') else "📄"
                self._print_buf(f"{icon} {item}")
        except Exception as e:
            self._print_buf(f"Ошибка: {e}")

    def run_settings(self):
        while True:
            self._clear_screen()
            self._print("⚙️ DiOS SETTINGS\n[1] SysInfo [2] Theme [3] Wallpaper [Q] Exit")
            c = input("> ").strip().lower()
            if c == 'q':
                break
            elif c == '1':
                print(f"OS: DiOS v{self.version}\nUser: {self.user_data['name']}")
                input("Press Enter...")
            elif c == '2':
                print("1: Standard, 2: Matrix, 3: Cyber, 4: Hacker, 5: Neon")
                tc = input("Choice: ")
                colors = {"1": "standard", "2": "matrix", "3": "cyber", "4": "hacker", "5": "neon"}
                if tc in colors:
                    self.user_data["theme"] = self.user_data["taskbar_color"] = colors[tc]
                    self.theme_prefix = THEMES[colors[tc]]
                    self.save_system()
            elif c == '3':
                print("1: Black 2: Blue 3: Magenta 4: Cyan 5: White")
                bg = input("Choice: ")
                bg_map = {"1": "black", "2": "blue", "3": "magenta", "4": "cyan", "5": "white"}
                if bg in bg_map:
                    self.user_data["bg_color"] = bg_map[bg]
                    self.save_system()

    def play_hide_seek(self):
        if "hide_seek" not in self.user_data.get("installed_apps", []):
            self._print_buf("Error: Install from Store.")
            return
        game_code = """from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
app = Ursina()
ground = Entity(model='plane', scale=(50, 1, 50), color=color.green, texture='white_cube', texture_scale=(50, 50), collider='box')
Sky()
for i in range(15): Entity(model='cube', color=color.gray, scale=(random.randint(2,6), random.randint(3,6), 1), position=(random.randint(-20,20), 2, random.randint(-20,20)), collider='box')
target = Entity(model='cube', color=color.red, scale=(1,2,1), position=(random.randint(-20,20), 1, random.randint(-20,20)), collider='box')
player = FirstPersonController()
text = Text(text="FIND RED CUBE! [ESC to Exit]", position=(0, 0.4), scale=2, color=color.yellow)
def update():
    if distance(player.position, target.position) < 2.5: text.text = "YOU WIN!"; text.color = color.green
app.run()"""
        try:
            with open("dios_hideseek_3d.py", "w", encoding="utf-8") as f:
                f.write(game_code)
            subprocess.run(["python", "dios_hideseek_3d.py"])
        except Exception as e:
            print(f"Launch failed: {e}"); input("Enter...")

    def run_store(self):
        self._clear_screen()
        print("💎 DIAMOND STORE")
        apps = {"1": ["Construction Sim", "construction"], "2": ["Hide In Seek 3D", "hide_seek"]}
        for k, v in apps.items():
            print(f"[{k}] {v[0]} {'[Installed]' if v[1] in self.user_data['installed_apps'] else '[Free]'}")
        choice = input("\nSelect App ID (or Q): ").strip()
        if choice in apps and apps[choice][1] not in self.user_data["installed_apps"]:
            self.user_data["installed_apps"].append(apps[choice][1])
            self.save_system()

    def run_browser(self):
        self._clear_screen()
        print(f"🌐 DiOS BROWSER v{self.version}")
        if 'browser_url' in self.bg_tasks: print(f"[Restored: {self.bg_tasks['browser_url']}]")
        while True:
            url = input("URL (min/q) > ").lower().strip()
            if url == 'q':
                self.bg_tasks.pop('browser_url', None); break
            elif url == 'min':
                self.set_notify("Браузер свернут"); break
            elif url:
                self.bg_tasks['browser_url'] = url
                if "dios.com" in url:
                    print("DiOS Official")
                else:
                    print("404 Error")

    def run_calculator(self):
        self._clear_screen()
        print("🔢 DiOS Calculator")
        mode = self.bg_tasks.get('calc_mode', input("Mode [1] Standard [2] Programmer: ").strip())
        self.bg_tasks['calc_mode'] = mode
        while True:
            expr = input("Calc (min/q) > ").strip()
            if expr == 'q':
                self.bg_tasks.pop('calc_mode', None); break
            elif expr == 'min':
                self.set_notify("Калькулятор свернут"); break
            try:
                print(f"Result: {eval(expr)}")
            except:
                print("Error.")

    def run_construction_sim(self):
        if "construction" not in self.user_data.get("installed_apps", []): return
        pop = 0
        while pop < 20:
            if input(f"Pop: {pop} | [H] Build (+5) [Q] Exit > ").lower() == 'h':
                pop += 5
            elif input == 'q':
                break
        if pop >= 20: print("\n🏆 You won!")
        input("Enter...")

    def run_messages(self):
        for k, v in self.messenger_contacts.items(): print(f"[{k}] {v}")
        if input("[+] Add  [Q] Exit > ") == '+': self.messenger_contacts[str(len(self.messenger_contacts) + 1)] = input(
            "Name: ")

    def run_antivirus(self):
        if input("🛡️ [1] Scan [2] Clean > ") == "1": print("Clean!")
        input("Enter...")

    def edit_file(self, filename):
        if not os.path.exists(filename): open(filename, "w").close()
        with open(filename, "r") as f:
            lines = f.readlines()
        while True:
            for i, l in enumerate(lines): print(f"{i + 1}: {l.strip()}")
            cmd = input("[s] save | [a] add | [q] exit > ").strip().lower()
            if cmd == 'q':
                break
            elif cmd == 's':
                with open(filename, "w") as f:
                    f.writelines(lines)
                break
            elif cmd == 'a':
                lines.append(input("New line: ") + "\n")

    # --- OS MAIN LOOP ---
    def render_desktop(self):
        self._clear_screen()
        cols, lines = shutil.get_terminal_size((80, 24))
        bg_col = BG_COLORS.get(self.user_data.get("bg_color", "black"), "")
        reset_col = "\033[0m"

        print(f"{bg_col}{THEMES[self.user_data['theme']]}═" * cols)
        print(f" DiOS {self.version} ".center(cols, " "))
        print("═" * cols + reset_col)

        avail = lines - 6
        if len(self.screen_buffer) > avail: self.screen_buffer = self.screen_buffer[-avail:]
        for line in self.screen_buffer: print(f"{bg_col}{line}{reset_col}")
        for _ in range(avail - len(self.screen_buffer)): print(f"{bg_col}{' ' * cols}{reset_col}")

        notif = f" | {self.notification[0]}" if self.notification and time.time() - self.notification[1] < 4 else ""
        tb = f" [settings] | [files] | [browser]{notif} ".ljust(cols - 10)[
                 :cols - 10] + f"[{datetime.now().strftime('%H:%M')}] "
        tt = THEMES.get(self.user_data.get("taskbar_color", "cyber"), "")

        print(f"{tt}█{'▀' * (cols - 2)}█{reset_col}\n{tt}█{tb}█{reset_col}")

    def run_os_loop(self):
        self.screen_buffer.append(f"Welcome to DiOS {self.version}")
        while self.current_state == "os":
            self.render_desktop()
            cmd_str = input(f"{self.theme_prefix}Command > \033[0m").strip()
            if not cmd_str: continue

            parts = shlex.split(cmd_str)
            cmd = parts[0].lower()
            self._print_buf(f"{self.user} > {cmd_str}")

            if cmd == "1191":
                self.current_state = "shutdown_to_admin"
                break
            elif cmd == "3":
                self.current_state = "power_off"
                break
            elif cmd == "help":
                [self._print_buf(l) for l in self.help_text.split('\n') if l.strip()]
            elif cmd == "clear":
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
                self.edit_file(parts[1]) if len(parts) > 1 else self._print_buf("Usage: edit <file>")
            else:
                self._print_buf(f"Unknown command: {cmd}")
                self.beep(400, 250)

    # --- MAIN SYSTEM CONTROLLER ---
    def run(self):
        while self.power_on:
            if self.current_state == "boot":
                self.boot_sequence(target_state="os_login")
            elif self.current_state == "bios":
                self.run_bios()
            elif self.current_state == "os_login":
                if not self.load_system():
                    self.first_time_setup()
                else:
                    self.login()
                self.current_state = "os"
            elif self.current_state == "os":
                self.run_os_loop()
            elif self.current_state == "shutdown_to_admin":
                self.shutdown_sequence(target_state="boot_to_admin")
            elif self.current_state == "boot_to_admin":
                self.boot_sequence(target_state="admin")
            elif self.current_state == "admin":
                self.run_admin_panel()
            elif self.current_state == "shutdown_to_os":
                self.shutdown_sequence(target_state="boot")
            elif self.current_state == "power_off":
                self.shutdown_sequence(target_state="halt")
                self.power_on = False


if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        print("\n[System successfully powered down]")
        input("[Press Enter to close...]")
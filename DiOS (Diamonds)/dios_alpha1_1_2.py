import os
import platform
import shlex
import getpass
import time
import shutil
import random
import json
from datetime import datetime

# Опциональная загрузка psutil
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class DiOS:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.user = "Guest"
        self.hostname = platform.node() or "DiOS"
        self.running = True
        self.version = "alpha 1.1.2"
        self.command_history = []
        self.config_file = "dios_sys.json"
        self.users_db = {}

        self.help_text = f"""
DiOS {self.version} Help:
--- System ---
help      : show this help menu
clear     : clear screen completely
refresh   : refresh the console screen instantly
date      : show current date and time
whoami    : show current user
history   : show command history
calc <exp>: calculate a mathematical expression (e.g. calc 2 + 2)

--- Games ---
games     : list available games
guess     : play 'Guess the Number'
math      : play 'Math Quiz'

--- File System ---
pwd       : show current directory
ls        : list files in current directory
cd <dir>  : change directory
mkdir <dir>: create a new directory
rmdir <dir>: remove an empty directory
touch <file>: create an empty file
rm <file> : remove a file
cp <src> <dst>: copy a file or directory
mv <src> <dst>: move or rename a file/directory
cat/read <file>: read and print file contents
write <file> <txt>: append text to a file
echo <txt>: print text to console
"""

    def _clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def load_system_data(self):
        """Загружает базу пользователей, если система уже была установлена"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.users_db = data.get("users", {})
                return True
            except Exception:
                return False
        return False

    def save_system_data(self):
        """Сохраняет данные пользователей"""
        data = {"users": self.users_db}
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def first_time_setup(self):
        """Процесс первой установки ОС и регистрации пользователя"""
        self._clear_screen()
        print(f"=== Welcome to DiOS {self.version} Setup ===")
        print("Starting first-time installation...")
        time.sleep(1)

        # Имитация распаковки файлов
        files_to_extract = ["kernel.sys", "drivers.cab", "filesystem.bin", "ui_module.dll", "games_pack.zip"]
        for file in files_to_extract:
            print(f"Extracting {file}...", end="", flush=True)
            time.sleep(random.uniform(0.2, 0.7))
            print(" Done.")

        print("\nSystem installed successfully!\n")
        print("--- User Registration ---")
        print("Let's set up your primary account.")

        while True:
            new_user = input("Enter a new username: ").strip()
            if not new_user:
                print("Username cannot be empty.")
                continue
            if new_user.lower() in [u.lower() for u in self.users_db.keys()]:
                print("User already exists. Try another name.")
                continue
            break

        country = input("Which country do you live in? ").strip()

        while True:
            password = getpass.getpass("Create a password: ")
            confirm_pwd = getpass.getpass("Confirm password: ")
            if password == confirm_pwd:
                break
            else:
                print("Passwords do not match. Try again.")

        self.users_db[new_user] = {
            "password": password,
            "country": country,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_system_data()

        print("\nAccount created successfully! Rebooting system...\n")
        time.sleep(1.5)

    def login_screen(self):
        """Экран входа в систему"""
        self._clear_screen()
        print(f"--- DiOS {self.version} Login ---")

        while True:
            req_user = input("Username: ").strip()
            if req_user in self.users_db:
                req_pwd = getpass.getpass("Password: ")
                if req_pwd == self.users_db[req_user]["password"]:
                    self.user = req_user
                    country = self.users_db[req_user].get("country", "Unknown")
                    print(f"\nWelcome back to DiOS, {self.user} from {country}!")
                    break
                else:
                    print("Incorrect password. Try again.\n")
            else:
                print("User not found. Try again.\n")
        time.sleep(1)

    def boot_sequence(self):
        self._clear_screen()
        print("Initializing DiOS BIOS...")
        time.sleep(0.3)
        print("Memory check: OK")
        time.sleep(0.2)
        print(f"Loading kernel for {platform.system()}...")
        time.sleep(0.5)
        print("Mounting virtual file systems... Done.")
        time.sleep(0.3)
        print("Starting user session...")
        time.sleep(0.4)

    def trigger_bsod(self):
        if os.name == 'nt':
            self._clear_screen()
            os.system('color 1F')
        else:
            self._clear_screen()
            print('\033[44;37m', end='')

        print("\n\n  :( \n")
        print("  Your DiOS ran into a critical problem and stopped working.")
        print("  We're just collecting some error info, and then you can recover.")
        print("\n  Error code: CRITICAL_PROCESS_DIED\n")
        print("  Options:")
        print("    [recover] - Restore system to a working state")
        print("    [exit]    - Shutdown the system completely\n")

        while True:
            action = input("  > ").strip().lower()
            if action == "recover":
                self._reset_colors()
                self.recover_system()
                break
            elif action == "exit":
                self._reset_colors()
                self.running = False
                break
            else:
                print("  [!] Invalid command. Type 'recover' or 'exit'.")

    def _reset_colors(self):
        if os.name == 'nt':
            os.system('color 07')
        else:
            print('\033[0m', end='')

    def recover_system(self):
        print("\nInitiating system recovery...")
        time.sleep(1)
        print("Checking file system integrity...")
        time.sleep(1)
        print("Clearing corrupted memory caches...")
        self.command_history.clear()
        self.current_dir = os.getcwd()
        time.sleep(1)
        self.boot_sequence()
        print(f"\n[System Recovered] Welcome back to DiOS, {self.user}!")

    def display_taskbar(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        bar_length = 70
        menu_str = "[ Menu: 1=Sysinfo | 2=Restart | 3=Shutdown ]"
        time_str = f"[ Time: {current_time} ]"

        spaces_needed = bar_length - len(menu_str) - len(time_str)
        if spaces_needed < 0: spaces_needed = 0

        taskbar = menu_str + ("=" * spaces_needed) + time_str
        print("\n" + taskbar)

    def prompt(self):
        return f"{self.user} > "

    def run(self):
        # 1. Проверяем, установлена ли ОС (есть ли конфиг)
        if not self.load_system_data():
            self.first_time_setup()
            self.load_system_data()  # Загружаем только что созданные данные

        # 2. Обычная загрузка и вход
        self.boot_sequence()
        self.login_screen()

        print("Type 'help' for available commands.")
        if not PSUTIL_AVAILABLE:
            print("\n[Warning] 'psutil' module is not installed.")
            print("Some 'sysinfo' features will be disabled.")

        self.main_loop()

    def main_loop(self):
        while self.running:
            try:
                self.display_taskbar()
                command = input(self.prompt()).strip()
                if command:
                    self.command_history.append(command)
                    self.execute_command(command)
            except (KeyboardInterrupt, EOFError):
                print("\nUse 'shutdown' or '3' to safely turn off DiOS.")

    def execute_command(self, command):
        try:
            parts = shlex.split(command)
        except ValueError as e:
            print(f"Syntax error: {e}")
            return

        if not parts:
            return

        cmd = parts[0].lower()

        if cmd == "help":
            print(self.help_text)

        elif cmd in ["3", "shutdown"]:
            print("Shutting down DiOS... Goodbye!")
            time.sleep(0.5)
            self.running = False

        elif cmd in ["2", "restart"]:
            print("Rebooting DiOS...")
            time.sleep(1)
            self.command_history.clear()
            # При перезагрузке снова требуем логин
            self.boot_sequence()
            self.login_screen()

        elif cmd in ["1", "sysinfo"]:
            self.show_system_info()

        # Команда refresh работает аналогично clear, создавая эффект моментального обновления экрана
        elif cmd in ["clear", "refresh"]:
            self._clear_screen()

        elif cmd == "date":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        elif cmd == "whoami":
            print(self.user)

        elif cmd == "history":
            for i, c in enumerate(self.command_history):
                print(f"{i + 1:3}  {c}")

        elif cmd == "echo":
            print(" ".join(parts[1:]))

        elif cmd == "calc":
            if len(parts) > 1:
                expression = " ".join(parts[1:])
                allowed_chars = "0123456789+-*/(). "
                if all(c in allowed_chars for c in expression):
                    try:
                        result = eval(expression)
                        print(f"Result: {result}")
                    except Exception as e:
                        print(f"calc: error calculating expression: {e}")
                else:
                    print("calc: invalid characters. Use only numbers and + - * / ( )")
            else:
                print("calc: missing expression. Usage: calc 2 + 2")

        elif cmd == "crash":
            self.trigger_bsod()

        elif cmd == "games":
            print("--- Available Games ---")
            print("  guess - Number guessing game")
            print("  math  - Quick math quiz")
            print("Type the name of the game to start playing!")

        elif cmd == "guess":
            target = random.randint(1, 100)
            print("--- Guess the Number (1-100) ---")
            print("Type 'q' to quit.")
            while True:
                ans = input("Your guess: ").strip()
                if ans.lower() == 'q':
                    print("Game aborted.")
                    break
                if not ans.isdigit():
                    print("Please enter a valid number.")
                    continue
                ans = int(ans)
                if ans < target:
                    print("Higher!")
                elif ans > target:
                    print("Lower!")
                else:
                    print(f"Correct! The number was {target}. You win!")
                    break

        elif cmd == "math":
            a = random.randint(1, 50)
            b = random.randint(1, 50)
            print(f"--- Math Quiz ---")
            ans = input(f"What is {a} + {b}? ").strip()
            if ans.isdigit() and int(ans) == (a + b):
                print("Correct! Good job.")
            else:
                print(f"Wrong! The correct answer is {a + b}.")

        elif cmd == "pwd":
            print(self.current_dir)

        elif cmd == "ls":
            try:
                files = os.listdir(self.current_dir)
                for f in sorted(files):
                    if os.path.isdir(os.path.join(self.current_dir, f)):
                        print(f"[DIR]  {f}")
                    else:
                        print(f"       {f}")
            except Exception as e:
                print(f"ls: error: {e}")

        elif cmd == "cd":
            target_dir = parts[1] if len(parts) > 1 else "~"
            try:
                if target_dir.startswith("~"):
                    target_path = os.path.expanduser(target_dir)
                else:
                    target_path = os.path.join(self.current_dir, target_dir)

                target_path = os.path.abspath(target_path)
                os.chdir(target_path)
                self.current_dir = os.getcwd()
            except Exception as e:
                print(f"cd: error: {e}")

        elif cmd in ["mkdir", "rmdir", "touch", "rm"]:
            if len(parts) > 1:
                target = parts[1]
                try:
                    if cmd == "mkdir":
                        os.mkdir(target); print(f"Directory created: {target}")
                    elif cmd == "rmdir":
                        os.rmdir(target); print(f"Directory removed: {target}")
                    elif cmd == "touch":
                        open(target, 'a').close(); os.utime(target, None)
                    elif cmd == "rm":
                        os.remove(target); print(f"File removed: {target}")
                except Exception as e:
                    print(f"{cmd}: error: {e}")
            else:
                print(f"{cmd}: missing operand")

        elif cmd in ["cp", "mv"]:
            if len(parts) > 2:
                try:
                    if cmd == "cp":
                        shutil.copy2(parts[1], parts[2]); print(f"Copied '{parts[1]}' to '{parts[2]}'")
                    elif cmd == "mv":
                        shutil.move(parts[1], parts[2]); print(f"Moved '{parts[1]}' to '{parts[2]}'")
                except Exception as e:
                    print(f"{cmd}: error: {e}")
            else:
                print(f"{cmd}: missing operand. Usage: {cmd} <src> <dst>")

        elif cmd == "write":
            if len(parts) > 2:
                try:
                    with open(parts[1], 'a', encoding='utf-8') as f:
                        f.write(" ".join(parts[2:]) + "\n")
                    print(f"Appended text to '{parts[1]}'")
                except Exception as e:
                    print(f"write: error: {e}")
            else:
                print("write: missing operand.")

        elif cmd in ["cat", "read"]:
            if len(parts) > 1:
                try:
                    with open(parts[1], 'r', encoding='utf-8') as f:
                        print(f.read())
                except Exception as e:
                    print(f"{cmd}: error: {e}")
            else:
                print(f"{cmd}: missing operand")

        else:
            print(f"Command not found: {cmd}. Type 'help' for available commands.")

    def show_system_info(self):
        print("=" * 50)
        print("SYSTEM INFORMATION")
        print("=" * 50)
        print(f"OS: {platform.system()} {platform.release()} ({platform.version()})")
        print(f"Machine: {platform.machine()}")
        print(f"Processor: {platform.processor()}")

        if PSUTIL_AVAILABLE:
            if hasattr(psutil, 'virtual_memory'):
                memory = psutil.virtual_memory()
                print(
                    f"Memory: {memory.available / (1024 ** 3):.2f} GB available of {memory.total / (1024 ** 3):.2f} GB")
        else:
            print("\n[!] Advanced info (Memory, Disk) is unavailable.")

        print(f"\nCurrent Session User: {self.user}")
        user_info = self.users_db.get(self.user, {})
        if user_info:
            print(f"Registered Location: {user_info.get('country', 'Unknown')}")
            print(f"Account Created: {user_info.get('created_at', 'Unknown')}")

        print(f"DiOS version: {self.version}")
        print("=" * 50)


if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
    finally:
        if os.name == 'nt':
            os.system('color 07')
        else:
            print('\033[0m', end='')
import os
import platform
import shlex
import getpass
import time
import shutil
import random
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
        self.user = getpass.getuser()  # Дефолтное имя
        self.hostname = platform.node() or "DiOS"
        self.running = True
        self.version = "alpha 1.1"
        self.command_history = []
        self.help_text = f"""
DiOS {self.version} Help:
--- System ---
help      : show this help menu
clear     : clear screen completely
date      : show current date and time
whoami    : show current user
history   : show command history
calc <exp>: calculate a mathematical expression (e.g. calc 2 + 2)
crash     : [DANGER] trigger a critical system failure (BSOD)

--- Games ---
games     : list available games
guess     : play 'Guess the Number'
math      : play 'Math Quiz'

--- Quick Menu (Bottom) ---
[1] sysinfo   : display system information
[2] restart   : reboot DiOS
[3] shutdown  : shutdown DiOS

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

    def boot_sequence(self):
        """Имитация процесса загрузки операционной системы"""
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

        self._clear_screen()

    def _clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def trigger_bsod(self):
        """Симулирует Синий Экран Смерти (BSOD)"""
        if os.name == 'nt':
            self._clear_screen()
            os.system('color 1F')  # Синий фон, белый текст для Windows
        else:
            self._clear_screen()
            print('\033[44;37m', end='')  # ANSI-коды для синего фона (Linux/Mac)

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
            os.system('color 07')  # Возврат к черному фону и белому тексту
        else:
            print('\033[0m', end='')

    def recover_system(self):
        """Восстановление системы после краша"""
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

    def display_bottom_menu(self):
        """Отображает нижнее меню перед строкой ввода"""
        print("\n" + "-" * 55)
        print(" Menu: [1] Sysinfo  |  [2] Restart  |  [3] Shutdown ")
        print("-" * 55)

    def prompt(self):
        return f"{self.user} > "

    def run(self):
        self.boot_sequence()

        # Экран входа
        print(f"--- DiOS {self.version} Login ---")
        requested_user = input("Enter your username: ").strip()
        if requested_user:
            self.user = requested_user
        else:
            self.user = "Guest"

        print(f"\nWelcome to DiOS, {self.user}! Type 'help' for available commands.")

        if not PSUTIL_AVAILABLE:
            print("\n[Warning] 'psutil' module is not installed.")
            print("Some 'sysinfo' features will be disabled.\n")

        self.main_loop()

    def main_loop(self):
        while self.running:
            try:
                self.display_bottom_menu()
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

        # --- System & Menu Commands ---
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
            self.run()

        elif cmd in ["1", "sysinfo"]:
            self.show_system_info()

        elif cmd == "clear":
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

        # --- Games ---
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

        # --- File System Commands ---
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

        print(f"\nUser: {self.user}")
        print(f"DiOS version: {self.version}")
        print("=" * 50)


if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
    finally:
        # Убеждаемся, что цвета сброшены при выходе из скрипта
        if os.name == 'nt':
            os.system('color 07')
        else:
            print('\033[0m', end='')
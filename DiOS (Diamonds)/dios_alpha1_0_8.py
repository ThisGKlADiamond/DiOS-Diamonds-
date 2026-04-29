import os
import platform
import shlex
import getpass
import time
import shutil
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
        self.user = getpass.getuser()  # Дефолтное имя, будет перезаписано при входе
        self.hostname = platform.node() or "DiOS"
        self.running = True
        self.version = "alpha 1.0.8"
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
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

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

        # Очищаем экран перед экраном входа
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def display_bottom_menu(self):
        """Отображает нижнее меню перед строкой ввода"""
        print("\n" + "-" * 55)
        print(" Меню: [1] Sysinfo  |  [2] Restart  |  [3] Shutdown ")
        print("-" * 55)

    def prompt(self):
        # Обновленный формат строки ввода
        return f"{self.user} > "

    def run(self):
        self.boot_sequence()

        # --- НОВОВВЕДЕНИЕ: Экран входа ---
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
            self.run()  # Перезапуск логики (включая boot и запрос имени)

        elif cmd in ["1", "sysinfo"]:
            self.show_system_info()

        elif cmd == "clear":
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')

        elif cmd == "date":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        elif cmd == "whoami":
            print(self.user)

        elif cmd == "history":
            for i, c in enumerate(self.command_history):
                print(f"{i + 1:3}  {c}")

        elif cmd == "echo":
            print(" ".join(parts[1:]))

        # --- НОВОВВЕДЕНИЕ: Калькулятор ---
        elif cmd == "calc":
            if len(parts) > 1:
                expression = " ".join(parts[1:])
                # Допускаем только безопасные символы для вычислений
                allowed_chars = "0123456789+-*/(). "
                if all(c in allowed_chars for c in expression):
                    try:
                        result = eval(expression)
                        print(f"Result: {result}")
                    except Exception as e:
                        print(f"calc: error calculating expression: {e}")
                else:
                    print("calc: invalid characters in expression. Use only numbers and + - * / ( )")
            else:
                print("calc: missing expression. Usage: calc 2 + 2")

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
            except PermissionError:
                print("ls: Permission denied")
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
            except FileNotFoundError:
                print(f"cd: no such directory: {target_dir}")
            except NotADirectoryError:
                print(f"cd: not a directory: {target_dir}")
            except PermissionError:
                print(f"cd: permission denied: {target_dir}")

        elif cmd == "mkdir":
            if len(parts) > 1:
                try:
                    os.mkdir(parts[1])
                    print(f"Directory created: {parts[1]}")
                except FileExistsError:
                    print(f"mkdir: cannot create directory '{parts[1]}': File exists")
                except PermissionError:
                    print(f"mkdir: permission denied: '{parts[1]}'")
                except Exception as e:
                    print(f"mkdir: error: {e}")
            else:
                print("mkdir: missing operand")

        elif cmd == "rmdir":
            if len(parts) > 1:
                try:
                    os.rmdir(parts[1])
                    print(f"Directory removed: {parts[1]}")
                except FileNotFoundError:
                    print(f"rmdir: failed to remove '{parts[1]}': No such directory")
                except OSError:
                    print(f"rmdir: failed to remove '{parts[1]}': Directory not empty")
                except Exception as e:
                    print(f"rmdir: error: {e}")
            else:
                print("rmdir: missing operand")

        elif cmd == "touch":
            if len(parts) > 1:
                try:
                    with open(parts[1], 'a'):
                        os.utime(parts[1], None)
                except Exception as e:
                    print(f"touch: error: {e}")
            else:
                print("touch: missing operand")

        elif cmd == "rm":
            if len(parts) > 1:
                try:
                    os.remove(parts[1])
                    print(f"File removed: {parts[1]}")
                except FileNotFoundError:
                    print(f"rm: cannot remove '{parts[1]}': No such file")
                except IsADirectoryError:
                    print(f"rm: cannot remove '{parts[1]}': Is a directory (use rmdir)")
                except Exception as e:
                    print(f"rm: error: {e}")
            else:
                print("rm: missing operand")

        elif cmd == "cp":
            if len(parts) > 2:
                try:
                    shutil.copy2(parts[1], parts[2])
                    print(f"Copied '{parts[1]}' to '{parts[2]}'")
                except FileNotFoundError:
                    print(f"cp: cannot stat '{parts[1]}': No such file or directory")
                except IsADirectoryError:
                    print(f"cp: '{parts[1]}' is a directory (not supported yet)")
                except Exception as e:
                    print(f"cp: error: {e}")
            else:
                print("cp: missing file operand. Usage: cp <src> <dst>")

        elif cmd == "mv":
            if len(parts) > 2:
                try:
                    shutil.move(parts[1], parts[2])
                    print(f"Moved/Renamed '{parts[1]}' to '{parts[2]}'")
                except FileNotFoundError:
                    print(f"mv: cannot stat '{parts[1]}': No such file or directory")
                except Exception as e:
                    print(f"mv: error: {e}")
            else:
                print("mv: missing file operand. Usage: mv <src> <dst>")

        # --- НОВОВВЕДЕНИЕ: Запись в файл ---
        elif cmd == "write":
            if len(parts) > 2:
                filename = parts[1]
                content = " ".join(parts[2:])
                try:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(content + "\n")
                    print(f"Appended text to '{filename}'")
                except Exception as e:
                    print(f"write: error: {e}")
            else:
                print("write: missing operand. Usage: write <file> <text to append>")

        elif cmd in ["cat", "read"]:
            if len(parts) > 1:
                try:
                    with open(parts[1], 'r', encoding='utf-8') as f:
                        print(f.read())
                except FileNotFoundError:
                    print(f"{cmd}: {parts[1]}: No such file")
                except IsADirectoryError:
                    print(f"{cmd}: {parts[1]}: Is a directory")
                except UnicodeDecodeError:
                    print(f"{cmd}: {parts[1]}: Cannot read binary or non-UTF-8 file")
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
        print(f"Architecture: {platform.architecture()[0]}")

        if PSUTIL_AVAILABLE:
            if hasattr(psutil, 'virtual_memory'):
                memory = psutil.virtual_memory()
                total_memory_gb = memory.total / (1024 ** 3)
                available_memory_gb = memory.available / (1024 ** 3)
                used_memory_percent = memory.percent
                print(
                    f"Memory: {available_memory_gb:.2f} GB available of {total_memory_gb:.2f} GB ({used_memory_percent}% used)")

            try:
                root_path = os.path.abspath(os.sep)
                disk = psutil.disk_usage(root_path)
                total_disk_gb = disk.total / (1024 ** 3)
                used_disk_gb = disk.used / (1024 ** 3)
                free_disk_gb = disk.free / (1024 ** 3)
                print(f"Disk (Root): {used_disk_gb:.2f} GB used, {free_disk_gb:.2f} GB free of {total_disk_gb:.2f} GB")
            except Exception as e:
                print(f"Disk: Unable to retrieve disk information ({e})")

            if hasattr(psutil, 'boot_time'):
                boot_time = datetime.fromtimestamp(psutil.boot_time())
                uptime = datetime.now() - boot_time
                days = uptime.days
                hours, remainder = divmod(uptime.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                print(f"Uptime: {days}d {hours}h {minutes}m {seconds}s")
        else:
            print("\n[!] Advanced info (Memory, Disk, Uptime) is unavailable.")

        print(f"\nUser: {self.user}")
        print(f"Hostname: {self.hostname}")
        print(f"Current directory: {self.current_dir}")
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
            input("\nPress Enter to exit...")
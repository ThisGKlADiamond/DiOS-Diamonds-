import os
import platform
import shlex
import getpass
import time
import sys
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
        self.user = getpass.getuser()
        self.hostname = platform.node() or "DiOS"
        self.running = True
        self.version = "alpha 1.0.6 easy edition"
        self.help_text = f"""
DiOS {self.version} Help:
--- System ---
help      : show this help menu
sysinfo   : display system information
clear     : clear screen completely
date      : show current date and time
whoami    : show current user
shutdown  : close DiOS session
restart   : reboot DiOS system

--- File System ---
pwd        : show current directory
ls         : list files in current directory
cd <dir>   : change directory
mkdir <dir>: create a new directory
rmdir <dir>: remove an empty directory
touch <file>: create an empty file
rm <file>  : remove a file
cat <file> : read and print file contents
echo <txt> : print text to console
"""

    def boot_sequence(self):
        """Имитация процесса загрузки операционной системы"""
        self.clear_screen()
        print("Initializing DiOS BIOS...")
        time.sleep(0.3)
        print(f"Memory check: {self._get_total_mem() if PSUTIL_AVAILABLE else 'OK'}")
        time.sleep(0.2)
        print(f"Loading kernel for {platform.system()}...")
        time.sleep(0.5)
        print("Mounting virtual file systems... Done.")
        time.sleep(0.3)
        print("Starting user session...")
        time.sleep(0.4)
        self.clear_screen()
        print(f"Welcome to DiOS {self.version}! Type 'help' for available commands.")
        if not PSUTIL_AVAILABLE:
            print("\n[Warning] 'psutil' not found. Advanced sysinfo disabled.\n")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _get_total_mem(self):
        return f"{psutil.virtual_memory().total / (1024 ** 3):.1f} GB"

    def prompt(self):
        return f"{self.user}@{self.hostname}:{self.current_dir}$ "

    def run(self):
        self.boot_sequence()

        while self.running:
            try:
                command = input(self.prompt()).strip()
                if command:
                    self.execute_command(command)
            except (KeyboardInterrupt, EOFError):
                print("\nUse 'shutdown' to exit.")

    def execute_command(self, command):
        try:
            parts = shlex.split(command)
        except ValueError as e:
            print(f"Syntax error: {e}")
            return

        if not parts: return
        cmd = parts[0].lower()

        # --- System Commands ---
        if cmd == "help":
            print(self.help_text)

        elif cmd == "shutdown":
            print("Shutting down DiOS... Saving buffers...")
            time.sleep(0.7)
            print("Goodbye!")
            self.running = False

        elif cmd == "restart":
            print("Rebooting DiOS system...")
            time.sleep(1)
            self.boot_sequence()

        elif cmd == "clear":
            self.clear_screen()

        elif cmd == "date":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        elif cmd == "whoami":
            print(self.user)

        elif cmd == "sysinfo":
            self.show_system_info()

        elif cmd == "echo":
            print(" ".join(parts[1:]))

        # --- File System Commands ---
        elif cmd == "pwd":
            print(self.current_dir)

        elif cmd == "ls":
            try:
                files = os.listdir(self.current_dir)
                for f in sorted(files):
                    prefix = "[DIR] " if os.path.isdir(os.path.join(self.current_dir, f)) else "      "
                    print(f"{prefix} {f}")
            except PermissionError:
                print("ls: Permission denied")

        elif cmd == "cd":
            target_dir = parts[1] if len(parts) > 1 else "~"
            try:
                target_path = os.path.abspath(
                    os.path.expanduser(target_dir) if target_dir.startswith("~") else os.path.join(self.current_dir,
                                                                                                   target_dir))
                os.chdir(target_path)
                self.current_dir = os.getcwd()
            except Exception as e:
                print(f"cd: {e}")

        elif cmd in ["mkdir", "rmdir", "touch", "rm", "cat"]:
            if len(parts) > 1:
                self.handle_fs_ops(cmd, parts[1])
            else:
                print(f"{cmd}: missing operand")

        else:
            print(f"Command not found: {cmd}. Type 'help' for commands.")

    def handle_fs_ops(self, cmd, path):
        try:
            if cmd == "mkdir":
                os.mkdir(path); print(f"Created directory: {path}")
            elif cmd == "rmdir":
                os.rmdir(path); print(f"Removed directory: {path}")
            elif cmd == "touch":
                with open(path, 'a'):
                    os.utime(path, None)
            elif cmd == "rm":
                os.remove(path); print(f"Removed file: {path}")
            elif cmd == "cat":
                with open(path, 'r', encoding='utf-8') as f:
                    print(f.read())
        except Exception as e:
            print(f"{cmd}: {e}")

    def show_system_info(self):
        print("=" * 50)
        print(f"SYSTEM INFORMATION - DiOS {self.version}")
        print("=" * 50)
        print(f"OS/Kernel: {platform.system()} {platform.release()}")
        print(f"CPU: {platform.processor()}")

        if PSUTIL_AVAILABLE:
            mem = psutil.virtual_memory()
            print(f"Memory: {mem.percent}% used ({mem.available // 1024 ** 2}MB free)")
            uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
            print(f"Uptime: {uptime}")

        print(f"User: {self.user}@{self.hostname}")
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
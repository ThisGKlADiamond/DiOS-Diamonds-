import os
import platform
import psutil
from datetime import datetime

class DiOS:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.user = "user"
        self.hostname = "DiOS"
        self.running = True
        self.version = "alpha 1.0.2"
        self.help_text = f"""
DiOS {self.version} Help:
- help    : show this help
- ls      : list files in current directory
- pwd     : show current directory
- cd <dir>: change directory (supports relative paths)
- echo <text>: print text to console
- date    : show current date and time
- whoami  : show current user
- clear   : clear screen completely
- sysinfo : display system information
- exit    : shutdown DiOS
"""

    def prompt(self):
        return f"{self.user}@{self.hostname}:{self.current_dir}$ "

    def run(self):
        print(f"Welcome to DiOS {self.version}! Type 'help' for available commands.")
        while self.running:
            try:
                command = input(self.prompt()).strip()
                self.execute_command(command)
            except (KeyboardInterrupt, EOFError):
                print("\nUse 'exit' to shutdown DiOS.")

    def execute_command(self, command):
        parts = command.split()
        if not parts:
            return

        cmd = parts[0].lower()

        if cmd == "help":
            print(self.help_text)

        elif cmd == "ls":
            try:
                files = os.listdir(self.current_dir)
                print("\n".join(sorted(files)))
            except PermissionError:
                print("ls: Permission denied")
            except Exception as e:
                print(f"ls: {e}")

        elif cmd == "pwd":
            print(self.current_dir)

        elif cmd == "cd":
            if len(parts) > 1:
                target_dir = parts[1]
                try:
                    # Разрешаем относительные пути
                    target_path = os.path.join(self.current_dir, target_dir)
                    os.chdir(target_path)
                    self.current_dir = os.getcwd()  # Всегда обновляем
                except FileNotFoundError:
                    print(f"cd: no such directory: {target_dir}")
                except NotADirectoryError:
                    print(f"cd: not a directory: {target_dir}")
                except PermissionError:
                    print(f"cd: permission denied: {target_dir}")
            else:
                print("cd: missing argument. Usage: cd <directory>")

        elif cmd == "echo":
            print(" ".join(parts[1:]))

        elif cmd == "date":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        elif cmd == "whoami":
            print(self.user)

        elif cmd == "clear":
            # Кросс‑платформенная очистка экрана без вывода текста
            if os.name == 'nt':  # Windows
                os.system('cls')
            else:  # Unix/Linux/Mac
                os.system('clear')

        elif cmd == "sysinfo":
            self.show_system_info()

        elif cmd == "exit":
            print("Shutting down DiOS... Goodbye!")
            self.running = False

        else:
            print(f"Command not found: {cmd}. Type 'help' for available commands.")

    def show_system_info(self):
        """Отображает подробную системную информацию"""
        print("=" * 50)
        print("SYSTEM INFORMATION")
        print("=" * 50)

        # Основная информация
        print(f"OS: {platform.system()} {platform.release()} ({platform.version()})")
        print(f"Machine: {platform.machine()}")
        print(f"Processor: {platform.processor()}")
        print(f"Architecture: {platform.architecture()[0]}")

        # Информация о памяти
        if hasattr(psutil, 'virtual_memory'):
            memory = psutil.virtual_memory()
            total_memory_gb = memory.total / (1024**3)
            available_memory_gb = memory.available / (1024**3)
            used_memory_percent = memory.percent
            print(f"Memory: {available_memory_gb:.2f} GB available of {total_memory_gb:.2f} GB ({used_memory_percent}% used)")

        # Информация о диске
        try:
            disk = psutil.disk_usage('/')
            total_disk_gb = disk.total / (1024**3)
            used_disk_gb = disk.used / (1024**3)
            free_disk_gb = disk.free / (1024**3)
            print(f"Disk: {used_disk_gb:.2f} GB used, {free_disk_gb:.2f} GB free of {total_disk_gb:.2f} GB")
        except:
            print("Disk: Unable to retrieve disk information")

        # Время работы системы
        if hasattr(psutil, 'boot_time'):
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"Uptime: {days}d {hours}h {minutes}m {seconds}s")

        # Сеть
        try:
            net_interfaces = psutil.net_if_addrs()
            print(f"Network interfaces: {len(net_interfaces)}")
        except:
            print("Network: Unable to retrieve network information")

        # Пользователь и хост
        print(f"User: {self.user}")
        print(f"Hostname: {self.hostname}")
        print(f"Current directory: {self.current_dir}")
        print(f"DiOS version: {self.version}")
        print("=" * 50)

if __name__ == "__main__":
    dios = DiOS()
    dios.run()

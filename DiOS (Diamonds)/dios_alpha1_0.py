import os
from datetime import datetime

class DiOS:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.user = "user"
        self.hostname = "DiOS"
        self.running = True
        self.help_text = """
DiOS Help:
- help    : show this help
- ls      : list files in current directory
- pwd     : show current directory
- cd <dir>: change directory (supports relative paths)
- echo <text>: print text to console
- date    : show current date and time
- whoami  : show current user
- clear   : clear screen
- exit    : shutdown DiOS
"""

    def prompt(self):
        return f"{self.user}@{self.hostname}:{self.current_dir}$ "

    def run(self):
        print("Welcome to DiOS! Type 'help' for available commands.")
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
            # ANSI escape code for clearing screen
            print("\033[H\033[J", end="")

        elif cmd == "exit":
            print("Shutting down DiOS... Goodbye!")
            self.running = False

        else:
            print(f"Command not found: {cmd}. Type 'help' for available commands.")

if __name__ == "__main__":
    dios = DiOS()
    dios.run()

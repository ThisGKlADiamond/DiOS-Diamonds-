import sys

class SimpleOS:
    def __init__(self):
        self.running = True
        self.commands = {
            'help': self.cmd_help,
            'echo': self.cmd_echo,
            'exit': self.cmd_exit,
            'calc': self.cmd_calc
        }

    def start(self):
        print("EXP OS alpha 0.0.0.1 started. Press 'help' for the list of commands.")
        while self.running:
            try:
                user_input = input("\n> ").strip()
                if user_input:
                    self.execute_command(user_input)
            except (KeyboardInterrupt, EOFError):
                print("\nShutting down...")
                break

    def execute_command(self, command_line):
        parts = command_line.split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''

        if cmd in self.commands:
            self.commands[cmd](args)
        else:
            print(f"Error: command '{cmd}' not found. Press 'help'.")

    def cmd_help(self, args):
        print("Available Commands:")
        for cmd in self.commands:
            print(f"  {cmd}")

    def cmd_echo(self, args):
        print(args)

    def cmd_calc(self, args):
        try:
            result = eval(args)
            print(result)
        except Exception as e:
            print(f"Error in expression: {e}")

    def cmd_exit(self, args):
        print("Shutting down EXP OS...")
        self.running = False

# Запуск
if __name__ == "__main__":
    os = SimpleOS()
    os.start()
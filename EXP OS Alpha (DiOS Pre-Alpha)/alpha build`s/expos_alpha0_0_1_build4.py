import sys
import operator
import ast
import datetime
import os as py_os
import platform
import random  # Добавлен модуль для игры


class SimpleOS:
    def __init__(self):
        self.running = True
        self.version = "alpha 0.0.1 Build 4"  # Обновлена версия
        self.history = []

        self.commands = {
            'help': self.cmd_help,
            'echo': self.cmd_echo,
            'shutdown': self.cmd_shutdown,  # Команда exit заменена на shutdown
            'calc': self.cmd_calc,
            'clear': self.cmd_clear,
            'time': self.cmd_time,
            'history': self.cmd_history,
            'ls': self.cmd_ls,
            'sysinfo': self.cmd_sysinfo,
            'game': self.cmd_game  # Добавлена новая команда для игры
        }

        self.help_text = {
            'help': 'Show this help or help on a specific command',
            'echo': 'Print the given text',
            'shutdown': 'Shut down the OS',  # Обновлено описание
            'calc': 'Calculate a simple arithmetic expression (+, -, *, /, //, %, **)',
            'clear': 'Clear the screen',
            'time': 'Show current date and time',
            'history': 'Show the history of entered commands',
            'ls': 'List files and directories in the current folder',
            'sysinfo': 'Show system information',
            'game': 'Play a number guessing game'  # Описание игры
        }

    def start(self):
        print(f"EXP OS {self.version} started. Press 'help' for the list of commands.")
        while self.running:
            try:
                user_input = input("\n> ").strip()
                if not user_input:
                    continue

                self.history.append(user_input)
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
        if args:
            if args in self.help_text:
                print(f"{args}: {self.help_text[args]}")
            else:
                print(f"No help available for command '{args}'.")
        else:
            print("Available Commands:")
            for cmd, desc in self.help_text.items():
                print(f"  {cmd:<8} - {desc}")

    def cmd_echo(self, args):
        print(args)

    def cmd_time(self, args):
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))

    def cmd_history(self, args):
        if not self.history:
            print("History is empty.")
        else:
            for i, cmd in enumerate(self.history, 1):
                print(f"{i:3}: {cmd}")

    def cmd_ls(self, args):
        try:
            files = py_os.listdir('.')
            if not files:
                print("Directory is empty.")
            else:
                for f in sorted(files):
                    if py_os.path.isdir(f):
                        print(f"[DIR]  {f}")
                    else:
                        print(f"[FILE] {f}")
        except Exception as e:
            print(f"Error reading directory: {e}")

    def cmd_sysinfo(self, args):
        print(f"EXP OS Version : {self.version}")
        print(f"Host OS        : {platform.system()} {platform.release()}")
        print(f"Python Version : {platform.python_version()}")
        print(f"Architecture   : {platform.machine()}")

    def cmd_calc(self, args):
        if not args:
            print("Usage: calc <expression>. Example: calc 2 + 2")
            return
        try:
            result = self.safe_eval(args)
            print(result)
        except ValueError as e:
            print(f"Error in expression: {e}")
        except Exception:
            print("Error: invalid expression. Use only numbers and +, -, *, /, //, %, **.")

    def safe_eval(self, expression):
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
        }

        def _eval(node):
            if isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
                left = _eval(node.left)
                right = _eval(node.right)
                op_type = type(node.op)
                if op_type in allowed_operators:
                    return allowed_operators[op_type](left, right)
                else:
                    raise ValueError(f"Unsupported operator: {op_type}")
            else:
                raise ValueError("Invalid expression")

        try:
            tree = ast.parse(expression, mode='eval')
            return _eval(tree.body)
        except SyntaxError:
            raise ValueError("Invalid syntax")
        except Exception as e:
            raise ValueError(str(e))

    def cmd_clear(self, args):
        if platform.system() == "Windows":
            py_os.system('cls')
        else:
            print("\033[H\033[J", end="")

    def cmd_shutdown(self, args):
        print("Shutting down EXP OS...")
        self.running = False

    def cmd_game(self, args):
        """Мини-игра 'Угадай число'"""
        number = random.randint(1, 100)
        print("Welcome to the Guessing Game!")
        print("I am thinking of a number between 1 and 100.")
        print("Type 'quit' or 'exit' to leave the game.")

        attempts = 0
        while True:
            guess_str = input("Game > ").strip().lower()

            if guess_str in ['quit', 'exit']:
                print("Exiting game. Returning to EXP OS.")
                break

            if not guess_str.isdigit():
                print("Please enter a valid number.")
                continue

            guess = int(guess_str)
            attempts += 1

            if guess < number:
                print("Too low!")
            elif guess > number:
                print("Too high!")
            else:
                print(f"Congratulations! You guessed the number {number} in {attempts} attempts!")
                break


# Запуск
if __name__ == "__main__":
    my_os = SimpleOS()
    my_os.start()
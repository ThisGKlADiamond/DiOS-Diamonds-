import sys
import operator

class SimpleOS:
    def __init__(self):
        self.running = True
        self.version = "alpha 0.0.0.2"
        self.commands = {
            'help': self.cmd_help,
            'echo': self.cmd_echo,
            'exit': self.cmd_exit,
            'calc': self.cmd_calc,
            'clear': self.cmd_clear
        }
        # Описание команд для справки
        self.help_text = {
            'help': 'Show this help or help on a specific command',
            'echo': 'Print the given text',
            'exit': 'Shut down the OS',
            'calc': 'Calculate a simple arithmetic expression (+, -, *, /, //, %, **)',
            'clear': 'Clear the screen'
        }

    def start(self):
        print(f"EXP OS {self.version} started. Press 'help' for the list of commands.")
        while self.running:
            try:
                user_input = input("\n> ").strip()
                if not user_input:
                    continue  # Пропускаем пустые строки
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
        if args:  # Если указана конкретная команда
            if args in self.help_text:
                print(f"{args}: {self.help_text[args]}")
            else:
                print(f"No help available for command '{args}'.")
        else:  # Общий список команд
            print("Available Commands:")
            for cmd, desc in self.help_text.items():
                print(f"  {cmd:<8} - {desc}")

    def cmd_echo(self, args):
        print(args)

    def cmd_calc(self, args):
        if not args:
            print("Usage: calc <expression>. Example: calc 2 + 2")
            return
        try:
            # Безопасный калькулятор: разрешены только арифметические операции
            result = self.safe_eval(args)
            print(result)
        except ValueError as e:
            print(f"Error in expression: {e}")
        except Exception:
            print("Error: invalid expression. Use only numbers and +, -, *, /, //, %, **.")

    def safe_eval(self, expression):
        """Безопасное вычисление арифметических выражений"""
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
            if isinstance(node, ast.Constant):  # Число
                return node.value
            elif isinstance(node, ast.BinOp):  # Бинарная операция
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
        except:
            raise ValueError("Invalid syntax")

    def cmd_clear(self, args):
        print("\033[H\033[J", end="")  # ANSI-код для очистки экрана

    def cmd_exit(self, args):
        print("Shutting down EXP OS...")
        self.running = False

# Запуск
if __name__ == "__main__":
    import ast  # Импорт здесь, чтобы не засорять глобальную область
    os = SimpleOS()
    os.start()

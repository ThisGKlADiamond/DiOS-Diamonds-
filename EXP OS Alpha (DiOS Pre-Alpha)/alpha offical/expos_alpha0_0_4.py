import os
import sys
import time
import random
import logging
import json
import shlex

# Настройка логирования
logging.basicConfig(filename='.expos_log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ExpOS:
    def __init__(self, safe_mode=False):
        self.version = "alpha 0.0.4"
        self.safe_mode = safe_mode
        self.is_running = True
        self.current_user = "guest"
        self.ps1 = f"[{self.current_user}@expos]/>"
        self.history = []
        self.aliases = {}
        self.theme_colors = {"dark": "\033[0m", "light": "\033[1;30m\033[47m", "reset": "\033[0m"}
        self.current_theme = "dark"

        # Виртуальная файловая система
        self.vfs = {
            "README.exp": {
                "content": "Добро пожаловать в EXP OS!\nДоступные команды: help, menu, ping, wget, ps, df, view.",
                "perms": "644"},
            "test.txt": {"content": "Строка 1\nСтрока 2\nОШИБКА: тест\nУспех", "perms": "644"}
        }
        self.config = {"password": "root", "require_auth": True}

    def boot(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        logos = [
            "  _____  __  __  ____    ___   ____  \n | ____| \\ \\/ / |  _ \\  / _ \\ / ___| \n |  _|    \\  /  | |_) || | | |\\___ \\ \n | |___   /  \\  |  __/ | |_| | ___) |\n |_____| /_/\\_\\ |_|     \\___/ |____/ \n",
            " [ E X P   O S   v.0.0.4 ] \n    /// ALIVE AND KICKING ///"
        ]
        print(self.theme_colors[self.current_theme])
        print(random.choice(logos))
        print(f"Загрузка EXP OS {self.version}...")

        # Анимация загрузки
        for i in range(101):
            sys.stdout.write(
                f"\r[CPU: {random.randint(5, 30)}% | BAT: 98%] Загрузка модулей: [{'#' * (i // 10)}{'.' * (10 - i // 10)}] {i}%")
            sys.stdout.flush()
            time.sleep(0.01)
        print("\nСистема готова.\n")
        logging.info("Система успешно загружена.")

        if self.config["require_auth"] and not self.safe_mode:
            attempts = 3
            while attempts > 0:
                pwd = input("Введите пароль (по умолчанию 'root'): ")
                if pwd == self.config["password"]:
                    self.current_user = "admin"
                    self.ps1 = f"[{self.current_user}@expos]/>"
                    print("Доступ разрешен.")
                    break
                else:
                    attempts -= 1
                    print(f"Неверный пароль. Осталось попыток: {attempts}")
            if attempts == 0:
                print("Система заблокирована.")
                sys.exit()

    def run(self):
        self.boot()
        while self.is_running:
            try:
                cmd_line = input(f"{self.theme_colors[self.current_theme]}{self.ps1} {self.theme_colors['reset']}")
                if not cmd_line.strip():
                    continue

                self.history.append(cmd_line)
                self.save_history()

                # Обработка конвейера (|)
                if "|" in cmd_line:
                    cmds = [c.strip() for c in cmd_line.split("|")]
                    output = self.execute_command(cmds[0], return_output=True)
                    if len(cmds) > 1 and cmds[1].startswith("grep"):
                        search_term = cmds[1].split(" ", 1)[1] if " " in cmds[1] else ""
                        output = "\n".join([line for line in output.split("\n") if search_term in line])
                    print(output)
                else:
                    output = self.execute_command(cmd_line)
                    if output:
                        print(output)

            except KeyboardInterrupt:
                print("\nИспользуйте команду 'menu' -> 'shutdown' для выхода.")
            except Exception as e:
                logging.error(f"Сбой: {e}")
                print(f"Критическая ошибка: {e}. Детали в .expos_log")

    def execute_command(self, cmd_line, return_output=False):
        parts = shlex.split(cmd_line)
        cmd = parts[0]
        args = parts[1:]

        # Замена алиасов
        if cmd in self.aliases:
            parts = shlex.split(self.aliases[cmd]) + args
            cmd = parts[0]
            args = parts[1:]

        # Ограничения главного экрана
        if cmd in ["exit", "shutdown", "sysinfo", "quit"]:
            msg = "Команда недоступна в консоли. Используйте 'menu'."
            return msg if return_output else print(msg)

        # Диспетчер команд
        try:
            if cmd == "help":
                return self.cmd_help(args)
            elif cmd == "menu":
                return self.cmd_menu()
            elif cmd == "man":
                return self.cmd_man(args)
            elif cmd == "ping":
                return self.cmd_ping(args)
            elif cmd == "wget":
                return self.cmd_wget(args)
            elif cmd == "ps":
                return self.cmd_ps()
            elif cmd == "df":
                return self.cmd_df()
            elif cmd == "alias":
                return self.cmd_alias(args)
            elif cmd == "view":
                return self.cmd_view(args)
            elif cmd == "color":
                return self.cmd_color(args)
            elif cmd == "tictactoe":
                return self.cmd_tictactoe()
            elif cmd == "chmod":
                return self.cmd_chmod(args)
            elif cmd == "ls":
                return "\n".join([f"{k} [{v['perms']}]" for k, v in self.vfs.items()])
            else:
                return f"Команда не найдена: {cmd}. Введите 'help' для списка."
        except Exception as e:
            logging.error(f"Ошибка команды {cmd}: {e}")
            return f"Ошибка выполнения {cmd}: {e}"

    # --- РЕАЛИЗАЦИЯ КОМАНД ---

    def cmd_help(self, args):
        if args:
            return self.cmd_man(args)
        return ("Доступные команды:\n"
                "  help, man, menu, ls, view, chmod\n"
                "  ping, wget, ps, df, alias, color\n"
                "  tictactoe\n"
                "Подсказка: команды exit и sysinfo находятся в menu!")

    def cmd_man(self, args):
        docs = {
            "ping": "ping [-c count] [-s size] <host> - Симуляция сетевого пинга.",
            "wget": "wget <url> - Симуляция скачивания файла.",
            "view": "view <file> - Просмотр текстового файла (например view README.exp)",
            "menu": "menu - Открывает графическое меню системы."
        }
        if not args: return "Укажите команду: man <command>"
        return docs.get(args[0], f"Нет руководства для {args[0]}")

    def cmd_menu(self):
        while True:
            print("\n" + "=" * 20)
            print(" ГЛАВНОЕ МЕНЮ")
            print("=" * 20)
            print(" 1. Системная информация (sysinfo)")
            print(" 2. Настройки промпта (PS1)")
            print(" 3. Игры")
            print(" 4. Выключение (shutdown)")
            print(" 0. Назад в терминал")

            choice = input("Выбор: ")
            if choice == "1":
                print(
                    f"\nОС: EXP OS {self.version}\nПользователь: {self.current_user}\nТема: {self.current_theme}\nАлиасов: {len(self.aliases)}")
            elif choice == "2":
                self.ps1 = input("Введите новый формат промпта: ")
            elif choice == "3":
                print("Запуск игрового хаба... Введите 'tictactoe' в консоли.")
            elif choice == "4":
                print("Завершение работы...")
                self.is_running = False
                break
            elif choice == "0":
                break
        return ""

    def cmd_ping(self, args):
        count = 4
        if "-c" in args:
            idx = args.index("-c")
            count = int(args[idx + 1])
            args.pop(idx + 1)
            args.pop(idx)

        host = args[0] if args else "127.0.0.1"
        res = f"PING {host} 56(84) bytes of data.\n"
        print(res, end="")
        for i in range(count):
            ms = random.uniform(1.0, 50.0)
            print(f"64 bytes from {host}: icmp_seq={i + 1} ttl=64 time={ms:.2f} ms")
            time.sleep(0.5)
        return ""

    def cmd_wget(self, args):
        if not args: return "Укажите URL"
        url = args[0]
        filename = url.split("/")[-1] or "downloaded_file"
        print(f"Подключение к {url}...")
        time.sleep(1)
        for i in range(10, 101, 10):
            sys.stdout.write(f"\rСкачивание {filename}: [{'#' * (i // 10)}{'.' * (10 - i // 10)}] {i}%")
            sys.stdout.flush()
            time.sleep(0.2)
        print()
        self.vfs[filename] = {"content": f"Файл скачан с {url}", "perms": "644"}
        return f"Файл {filename} сохранен."

    def cmd_ps(self):
        return ("PID   USER     TIME  COMMAND\n"
                "1     root     0:02  init\n"
                f"42    {self.current_user[:7]:<8} 0:01  exp_shell\n"
                "99    system   0:00  cron_sim")

    def cmd_df(self):
        return ("Filesystem     1K-blocks    Used Available Use%\n"
                "vfs_root            1024      12      1012   1%\n"
                "trash_dir            512       0       512   0%")

    def cmd_view(self, args):
        if not args: return "Укажите файл."
        file = args[0]
        if file in self.vfs:
            print(f"--- Просмотр: {file} ---")
            lines = self.vfs[file]["content"].split("\n")
            for i, line in enumerate(lines):
                print(line)
                if (i + 1) % 5 == 0 and len(lines) > i + 1:
                    if input("-- Нажмите Enter для продолжения (q для выхода) --").lower() == 'q':
                        break
            return ""
        return "Файл не найден."

    def cmd_alias(self, args):
        if not args:
            return "\n".join([f"{k}='{v}'" for k, v in self.aliases.items()])
        if "=" in args[0]:
            k, v = args[0].split("=", 1)
            self.aliases[k] = v.strip("'\"")
            return f"Алиас добавлен: {k}"
        return "Формат: alias name='command'"

    def cmd_color(self, args):
        if not args or args[0] not in ["dark", "light"]:
            return "Использование: color dark | light"
        self.current_theme = args[0]
        return "Тема изменена."

    def cmd_chmod(self, args):
        if len(args) < 2: return "Формат: chmod <права> <файл>"
        perms, file = args[0], args[1]
        if file in self.vfs:
            self.vfs[file]["perms"] = perms
            return f"Права файла {file} изменены на {perms}"
        return "Файл не найден."

    def cmd_tictactoe(self):
        board = [' '] * 9

        def print_board():
            print(
                f"\n {board[0]} | {board[1]} | {board[2]} \n---+---+---\n {board[3]} | {board[4]} | {board[5]} \n---+---+---\n {board[6]} | {board[7]} | {board[8]} \n")

        while ' ' in board:
            print_board()
            try:
                move = int(input("Ваш ход (1-9): ")) - 1
                if board[move] == ' ':
                    board[move] = 'X'
                else:
                    print("Клетка занята!"); continue
            except:
                continue

            # Ход ИИ
            empty = [i for i, x in enumerate(board) if x == ' ']
            if empty: board[random.choice(empty)] = 'O'

            # Базовая проверка на конец
            if ' ' not in board: break

        print_board()
        return "Игра окончена!"

    def save_history(self):
        try:
            with open("exp_history.txt", "a") as f:
                f.write(self.history[-1] + "\n")
        except:
            pass


if __name__ == "__main__":
    is_safe = "--safe" in sys.argv
    os_sim = ExpOS(safe_mode=is_safe)
    os_sim.run()
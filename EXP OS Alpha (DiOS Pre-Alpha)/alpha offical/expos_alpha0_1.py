import os
import sys
import time
import random
import logging
import shlex
import traceback

# Настройка логирования
logging.basicConfig(filename='.expos_log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ExpOS:
    def __init__(self, safe_mode=False):
        self.version = "alpha 0.1.0"
        self.safe_mode = safe_mode
        self.is_running = True
        self.current_user = "guest"
        self.ps1 = f"[{self.current_user}@expos]/>"
        self.history = []
        self.aliases = {}
        self.theme_colors = {"dark": "\033[0m", "light": "\033[1;30m\033[47m", "reset": "\033[0m"}
        self.current_theme = "dark"

        # Переменные состояния системы
        self.crash_count = 0
        self.is_corrupted = False

        self.config = {"password": "root", "require_auth": True}
        self.init_vfs()

    def init_vfs(self):
        """Инициализация или восстановление виртуальной файловой системы"""
        self.vfs = {
            "README.exp": {
                "content": "Добро пожаловать в EXP OS!\nДоступные команды: help, menu, ping, wget, ps, df, view.",
                "perms": "644"},
            "test.txt": {"content": "Строка 1\nСтрока 2\nОШИБКА: тест\nУспех", "perms": "644"}
        }

    def boot(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        logos = [
            "  _____  __  __  ____    ___   ____  \n | ____| \\ \\/ / |  _ \\  / _ \\ / ___| \n |  _|    \\  /  | |_) || | | |\\___ \\ \n | |___   /  \\  |  __/ | |_| | ___) |\n |_____| /_/\\_\\ |_|     \\___/ |____/ \n",
            " [ E X P   O S   v.0.1.0 ] \n    /// СИСТЕМА АКТИВНА ///"
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
            # Проверка на повреждение ОС
            if self.is_corrupted:
                print(
                    "\nОС не может нормально работать, так как все её файлы повреждены, запустите восстановление системы или выйти.")
                recovery_cmd = input("Введите 'recovery' (восстановление) или 'exit' (выход): ").strip().lower()
                if recovery_cmd == "recovery":
                    self.cmd_recovery()
                elif recovery_cmd == "exit":
                    self.is_running = False
                    break
                continue

            try:
                cmd_line = input(f"{self.theme_colors[self.current_theme]}{self.ps1} {self.theme_colors['reset']}")
                if not cmd_line.strip():
                    continue

                self.history.append(cmd_line)
                self.save_history()

                # Обработка конвейеров (|)
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

                # Сброс счетчика ошибок при успешном выполнении команды
                self.crash_count = 0

            except KeyboardInterrupt:
                print("\nИспользуйте 'menu' -> 'shutdown' для выхода из системы.")
            except Exception as e:
                self.crash_count += 1
                logging.error(f"Сбой [{self.crash_count}]: {e}")
                print(f"Критическая ошибка: {e}. Детали в .expos_log")
                if self.crash_count >= 3:
                    self.is_corrupted = True

    def execute_command(self, cmd_line, return_output=False):
        try:
            parts = shlex.split(cmd_line)
        except ValueError as e:
            return f"Синтаксическая ошибка: {e}"

        if not parts:
            return ""

        cmd = parts[0]
        args = parts[1:]

        # Замена алиасов
        if cmd in self.aliases:
            try:
                parts = shlex.split(self.aliases[cmd]) + args
                cmd = parts[0]
                args = parts[1:]
            except ValueError:
                return "Ошибка синтаксиса в алиасе."

        # Ограничения главного экрана
        if cmd in ["exit", "shutdown", "sysinfo", "quit"]:
            msg = "Команда недоступна в консоли. Используйте команду 'menu'."
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
                return "\n".join([f"{k} [{v['perms']}]" for k, v in self.vfs.items()]) if self.vfs else "Папка пуста."
            elif cmd == "crash":
                raise RuntimeError("Принудительный сбой системы.")  # Скрытая команда для теста
            else:
                return f"Команда не найдена: {cmd}. Введите 'help' для списка команд."
        except Exception as e:
            # Перебрасываем ошибку выше для счетчика крашей
            raise RuntimeError(f"Ошибка выполнения {cmd}: {e}")

    # --- РЕАЛИЗАЦИЯ КОМАНД ---

    def cmd_recovery(self):
        print("\nЗапуск системы восстановления (Recovery)...")
        time.sleep(1)
        print("Сканирование поврежденных секторов...")
        for i in range(1, 101, 20):
            sys.stdout.write(f"\rПрогресс: [{i}%]")
            sys.stdout.flush()
            time.sleep(0.5)
        print("\nВосстановление файлов виртуальной системы до заводских...")
        self.init_vfs()
        self.is_corrupted = False
        self.crash_count = 0
        print("Система успешно восстановлена. Перезагрузка...\n")
        time.sleep(1)
        self.boot()
        return ""

    def cmd_help(self, args):
        if args:
            return self.cmd_man(args)
        return ("Доступные команды:\n"
                "  help, man, menu, ls, view, chmod\n"
                "  ping, wget, ps, df, alias, color\n"
                "  tictactoe\n"
                "Подсказка: команды 'exit' и 'sysinfo' находятся в menu!")

    def cmd_man(self, args):
        docs = {
            "ping": "ping [-c количество] <хост> - Симуляция сетевого пинга.",
            "wget": "wget <url> - Симуляция скачивания файла из сети.",
            "view": "view <файл> - Просмотр текстового файла (например, view README.exp).",
            "menu": "menu - Открывает графическое меню системы."
        }
        if not args: return "Укажите команду: man <команда>"
        return docs.get(args[0], f"Нет руководства для {args[0]}")

    def cmd_menu(self):
        while True:
            print("\n" + "=" * 20)
            print(" ГЛАВНОЕ МЕНЮ")
            print("=" * 20)
            print(" 1. Системная информация (sysinfo)")
            print(" 2. Настройки промпта (PS1)")
            print(" 3. Игровой хаб")
            print(" 4. Выключение (shutdown)")
            print(" 0. Назад в терминал")

            choice = input("Ваш выбор: ")
            if choice == "1":
                print(
                    f"\nОС: EXP OS {self.version}\nПользователь: {self.current_user}\nТема: {self.current_theme}\nКоличество алиасов: {len(self.aliases)}")
            elif choice == "2":
                self.ps1 = input("Введите новый формат строки ввода: ")
            elif choice == "3":
                print("Запуск игрового хаба... Введите 'tictactoe' в консоли для игры.")
            elif choice == "4":
                print("Завершение работы системы...")
                self.is_running = False
                break
            elif choice == "0":
                break
            else:
                print("Неверный выбор.")
        return ""

    def cmd_ping(self, args):
        count = 4
        if "-c" in args:
            try:
                idx = args.index("-c")
                count = int(args[idx + 1])
                args.pop(idx + 1)
                args.pop(idx)
            except:
                return "Неверный синтаксис команды ping."

        host = args[0] if args else "127.0.0.1"
        print(f"Обмен пакетами с {host} по 56(84) байт данных.")
        for i in range(count):
            ms = random.uniform(1.0, 50.0)
            print(f"Ответ от {host}: число байт=64 время={ms:.2f}мс TTL=64")
            time.sleep(0.5)
        return ""

    def cmd_wget(self, args):
        if not args: return "Укажите URL адрес."
        url = args[0]
        filename = url.split("/")[-1] or "скачанный_файл"
        print(f"Подключение к {url}...")
        time.sleep(1)
        for i in range(10, 101, 10):
            sys.stdout.write(f"\rСкачивание {filename}: [{'#' * (i // 10)}{'.' * (10 - i // 10)}] {i}%")
            sys.stdout.flush()
            time.sleep(0.2)
        print()
        self.vfs[filename] = {"content": f"Файл успешно скачан с {url}", "perms": "644"}
        return f"Файл {filename} сохранен."

    def cmd_ps(self):
        return ("PID   USER     TIME  COMMAND\n"
                "1     root     0:02  init\n"
                f"42    {self.current_user[:7]:<8} 0:01  exp_shell\n"
                "99    system   0:00  cron_sim")

    def cmd_df(self):
        return ("Файловая система   1K-блоков Использовано Доступно Испол.%\n"
                "vfs_root            1024      12           1012     1%\n"
                "trash_dir            512       0            512     0%")

    def cmd_view(self, args):
        if not args: return "Укажите файл для просмотра."
        file = args[0]
        if file in self.vfs:
            print(f"--- Просмотр файла: {file} ---")
            lines = self.vfs[file]["content"].split("\n")
            for i, line in enumerate(lines):
                print(line)
                if (i + 1) % 5 == 0 and len(lines) > i + 1:
                    if input("-- Нажмите Enter для продолжения (q для выхода) --").strip().lower() == 'q':
                        break
            return ""
        return "Файл не найден."

    def cmd_alias(self, args):
        if not args:
            return "\n".join([f"{k}='{v}'" for k, v in self.aliases.items()]) if self.aliases else "Алиасы не заданы."
        if "=" in args[0]:
            k, v = args[0].split("=", 1)
            self.aliases[k] = v.strip("'\"")
            return f"Алиас '{k}' успешно добавлен."
        return "Формат: alias имя='команда'"

    def cmd_color(self, args):
        if not args or args[0] not in ["dark", "light"]:
            return "Использование: color dark | light"
        self.current_theme = args[0]
        return "Тема оформления изменена."

    def cmd_chmod(self, args):
        if len(args) < 2: return "Формат: chmod <права> <файл>"
        perms, file = args[0], args[1]
        if file in self.vfs:
            self.vfs[file]["perms"] = perms
            return f"Права доступа для файла {file} изменены на {perms}"
        return "Файл не найден."

    def cmd_tictactoe(self):
        board = [' '] * 9

        def print_board():
            print(
                f"\n {board[0]} | {board[1]} | {board[2]} \n---+---+---\n {board[3]} | {board[4]} | {board[5]} \n---+---+---\n {board[6]} | {board[7]} | {board[8]} \n")

        while ' ' in board:
            print_board()
            try:
                move_input = input("Ваш ход (выберите клетку 1-9): ")
                if not move_input.isdigit(): continue
                move = int(move_input) - 1
                if 0 <= move <= 8 and board[move] == ' ':
                    board[move] = 'X'
                else:
                    print("Клетка занята или указан неверный номер!"); continue
            except:
                continue

            # Ход компьютера
            empty = [i for i, x in enumerate(board) if x == ' ']
            if empty: board[random.choice(empty)] = 'O'

            if ' ' not in board: break

        print_board()
        return "Игра окончена!"

    def save_history(self):
        try:
            with open("exp_history.txt", "a", encoding="utf-8") as f:
                f.write(self.history[-1] + "\n")
        except:
            pass


if __name__ == "__main__":
    # Включаем поддержку ANSI-цветов для консоли Windows
    os.system('')

    try:
        is_safe = "--safe" in sys.argv
        os_sim = ExpOS(safe_mode=is_safe)
        os_sim.run()
    except Exception as e:
        # Теперь, если возникнет ошибка Python, окно не закроется мгновенно!
        print("\n" + "=" * 50)
        print(" ПРОИЗОШЛА КРИТИЧЕСКАЯ ОШИБКА PYTHON:")
        print("=" * 50)
        print(traceback.format_exc())
        print("=" * 50)
    finally:
        # Эта строчка не даст командной строке закрыться, пока ты не нажмешь Enter
        input("\nНажмите Enter для закрытия окна...")
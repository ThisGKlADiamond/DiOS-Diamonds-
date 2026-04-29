import os
import sys
import time
import random
import logging
import shlex
import traceback
import json

# Настройка логирования
logging.basicConfig(filename='.expos_log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ExpOS:
    def __init__(self, safe_mode=False):
        self.version = "alpha 0.1.1"
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

        # Многоязычность
        self.language = 'ru'
        self.translations = {
            'ru': {
                'system_ready': 'Система готова.',
                'password_prompt': 'Введите пароль (по умолчанию \'root\'): ',
                'access_granted': 'Доступ разрешён.',
                'invalid_password': 'Неверный пароль. Осталось попыток: ',
                'system_locked': 'Система заблокирована.',
                'corrupted_system': 'ОС не может нормально работать, так как все её файлы повреждены, запустите восстановление системы или выйдите.',
                'recovery_prompt': 'Введите \'recovery\' (восстановление) или \'exit\' (выход): ',
                'shutdown_prompt': 'Завершение работы системы...',
                'help_title': 'Доступные команды:',
                'menu_title': 'ГЛАВНОЕ МЕНЮ',
                'lang_change': 'Язык изменён.',
                'lang_prompt': 'Выберите язык: 1 - Русский, 2 - English',
                'lang_invalid': 'Неверный выбор.',
                'save_state_error': 'Ошибка сохранения состояния: ',
                'load_state_error': 'Ошибка загрузки состояния: ',
                'history_saved': 'История команд сохранена.',
                'history_save_error': 'Ошибка сохранения истории: ',
            },
            'en': {
                'system_ready': 'System ready.',
                'password_prompt': 'Enter password (default \'root\'): ',
                'access_granted': 'Access granted.',
                'invalid_password': 'Invalid password. Attempts left: ',
                'system_locked': 'System locked.',
                'corrupted_system': 'The OS cannot function properly as all its files are corrupted. Run system recovery or exit.',
                'recovery_prompt': 'Enter \'recovery\' (recovery) or \'exit\' (exit): ',
                'shutdown_prompt': 'Shutting down the system...',
                'help_title': 'Available commands:',
                'menu_title': 'MAIN MENU',
                'lang_change': 'Language changed.',
                'lang_prompt': 'Select language: 1 - Russian, 2 - English',
                'lang_invalid': 'Invalid choice.',
                'save_state_error': 'Error saving state: ',
                'load_state_error': 'Error loading state: ',
                'history_saved': 'Command history saved.',
                'history_save_error': 'Error saving history: ',
            }
        }

        self.config = {"password": "root", "require_auth": True}
        self.load_state()  # Загрузка сохранённого состояния
        self.init_vfs()

    def _(self, key):
        """Получить перевод для ключа."""
        return self.translations[self.language].get(key, key)

    def load_state(self):
        """Загрузить сохранённое состояние системы."""
        try:
            with open('exp_state.json', 'r', encoding='utf-8') as f:
                state = json.load(f)
                self.aliases = state.get('aliases', {})
                self.history = state.get('history', [])
                self.current_theme = state.get('current_theme', 'dark')
                self.language = state.get('language', 'ru')
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.error(f"{self._('load_state_error')}{e}")

    def save_state(self):
        """Сохранить текущее состояние системы."""
        state = {
            'aliases': self.aliases,
            'history': self.history,
            'current_theme': self.current_theme,
            'language': self.language
        }
        try:
            with open('exp_state.json', 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"{self._('save_state_error')}{e}")

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
            " [ E X P   O S   v.0.1.1 ] \n    /// СИСТЕМА АКТИВНА ///"
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
        print("\n" + self._('system_ready'))
        logging.info("Система успешно загружена.")

        if self.config["require_auth"] and not self.safe_mode:
            attempts = 3
            while attempts > 0:
                pwd = input(self._('password_prompt'))
                if pwd == self.config["password"]:
                    self.current_user = "admin"
                    self.ps1 = f"[{self.current_user}@expos]/>"
                    print(self._('access_granted'))
                    break
                else:
                    attempts -= 1
                    print(f"{self._('invalid_password')}{attempts}")
            if attempts == 0:
                print(self._('system_locked'))
                sys.exit()

    def run(self):
        self.boot()
        while self.is_running:
            # Проверка на повреждение ОС
            if self.is_corrupted:
                print("\n" + self._('corrupted_system'))
                recovery_cmd = input(self._('recovery_prompt')).strip().lower()
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
                    output = self.handle_pipeline(cmd_line)
                    if output:
                        print(output)
                else:
                    output = self.execute_command(cmd_line)
                    if output:
                        print(output)

                # Сброс счётчика ошибок при успешном выполнении команды
                self.crash_count = 0

            except KeyboardInterrupt:
                print("\nИспользуйте 'menu' -> 'shutdown' для выхода из системы.")
            except Exception as e:
                self.crash_count += 1
                logging.error(f"Сбой [{self.crash_count}]: {e}")
                print(f"Критическая ошибка: {e}. Детали в .expos_log")
                if self.crash_count >= 3:
                    self.is_corrupted = True

        def handle_pipeline(self, cmd_line):
            """Обработка конвейеров команд (например, ls | grep exp)"""
            try:
                cmds = [c.strip() for c in cmd_line.split("|")]
                current_output = ""

                for i, cmd in enumerate(cmds):
                    if i == 0:
                        current_output = self.execute_command(cmd, return_output=True)
                    else:
                        if cmd.startswith("grep"):
                            search_term = cmd.split(" ", 1)[1] if " " in cmd else ""
                            current_output = "\n".join(
                                [line for line in current_output.split("\n") if search_term in line])
                        # Здесь можно добавить поддержку других команд
                return current_output
            except Exception as e:
                return f"Ошибка конвейера: {e}"

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
                    return "\n".join(
                        [f"{k} [{v['perms']}]" for k, v in self.vfs.items()]) if self.vfs else "Папка пуста."
                elif cmd == "crash":
                    raise RuntimeError("Принудительный сбой системы.")  # Скрытая команда для теста
                elif cmd == "lang":
                    return self.cmd_lang()
                else:
                    return f"Команда не найдена: {cmd}. Введите 'help' для списка команд."
            except Exception as e:
                # Перебрасываем ошибку выше для счётчика крашей
                raise RuntimeError(f"Ошибка выполнения {cmd}: {e}")

        # --- РЕАЛИЗАЦИЯ КОМАНД ---

        def cmd_recovery(self):
            print("\nЗапуск системы восстановления (Recovery)...")
            time.sleep(1)
            print("Сканирование повреждённых секторов...")
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
            return (self._('help_title') + "\n"
                                           "  help, man, menu, ls, view, chmod\n"
                                           "  ping, wget, ps, df, alias, color\n"
                                           "  tictactoe, lang\n"
                                           "Подсказка: команды 'exit' и 'sysinfo' находятся в menu!")

        def cmd_man(self, args):
            docs = {
                "ping": "ping [-c количество] <хост> - Симуляция сетевого пинга.",
                "wget": "wget <url> - Симуляция скачивания файла из сети.",
                "view": "view <файл> - Просмотр текстового файла (например, view README.exp).",
                "menu": "menu - Открывает графическое меню системы.",
                "lang": "lang - Смена языка интерфейса (русский/английский)."
            }
            if not args: return "Укажите команду: man <команда>"
            return docs.get(args[0], f"Нет руководства для {args[0]}")

        def cmd_menu(self):
            while True:
                print("\n" + "=" * 20)
                print(self._('menu_title'))
                print("=" * 20)
                print(" 1. Системная информация (sysinfo)")
                print(" 2. Настройки промпта (PS1)")
                print(" 3. Игровой хаб")
                print(" 4. Выключение (shutdown)")
                print(" 5. Смена языка (lang)")
                print(" 0. Назад в терминал")

                choice = input("Ваш выбор: ")
                if choice == "1":
                    print(
                        f"\nОС: EXP OS {self.version}\nПользователь: {self.current_user}\nТема: {self.current_theme}\nЯзык: {self.language}\nКоличество алиасов: {len(self.aliases)}")
                elif choice == "2":
                    self.ps1 = input("Введите новый формат строки ввода: ")
                elif choice == "3":
                    print("Запуск игрового хаба... Введите 'tictactoe' в консоли для игры.")
                elif choice == "4":
                    print(self._('shutdown_prompt'))
                    self.is_running = False
                    break
                elif choice == "5":
                    print(self._('lang_prompt'))
                    lang_choice = input("Ваш выбор: ")
                    if lang_choice == "1":
                        self.language = 'ru'
                        print(self._('lang_change'))
                    elif lang_choice == "2":
                        self.language = 'en'
                        print(self._('lang_change'))
                    else:
                        print(self._('lang_invalid'))
                elif choice == "0":
                    break
                else:
                    print("Неверный выбор.")
            return ""

        def cmd_lang(self):
            print(self._('lang_prompt'))
            lang_choice = input("Ваш выбор: ")
            if lang_choice == "1":
                self.language = 'ru'
                print(self._('lang_change'))
            elif lang_choice == "2":
                self.language = 'en'

                def cmd_ping(self, args):
                    host = "localhost"
                    count = 4

                    if "-c" in args:
                        try:
                            idx = args.index("-c")
                            count = int(args[idx + 1])
                            args.pop(idx + 1)
                            args.pop(idx)
                        except (ValueError, IndexError):
                            return "Ошибка: укажите корректное число пакетов после -c"

                    if args:
                        host = args[0]

                    print(
                        f"PING {host} ({random.randint(192, 193)}.{random.randint(168, 169)}.{random.randint(0, 255)}.{random.randint(1, 254)}): 56(84) bytes of data.")

                    for i in range(count):
                        time.sleep(0.5)
                        print(
                            f"{random.randint(56, 64)} bytes from {host}: icmp_seq={i + 1} ttl={random.randint(48, 58)} time={random.uniform(10, 100):.1f} ms")

                    return f"\n--- {host} ping statistics ---\n{count} packets transmitted, {count} received, 0% packet loss"

                def cmd_wget(self, args):
                    if not args:
                        return "Использование: wget <url>"

                    url = args[0]
                    filename = url.split("/")[-1] or "download"

                    print(f"--{time.strftime('%Y-%m-%d %H:%M:%S')}--  {url}")
                    print(
                        f"Resolving {url.split('/')[2]}... {random.randint(192, 193)}.{random.randint(168, 169)}.{random.randint(0, 255)}.{random.randint(1, 254)}")

                    total_size = random.randint(10000, 50000)
                    downloaded = 0

                    while downloaded < total_size:
                        chunk = random.randint(1000, 5000)
                        downloaded += chunk
                        if downloaded > total_size:
                            downloaded = total_size

                        percent = (downloaded / total_size) * 100
                        sys.stdout.write(f"\r{downloaded}/{total_size} bytes ({percent:.1f}%)")
                        sys.stdout.flush()
                        time.sleep(0.1)

                    print(f"\n'{filename}' saved [{total_size}/{total_size}]")
                    self.vfs[filename] = {"content": f"Содержимое файла {filename}", "perms": "644"}
                    return ""

                def cmd_ps(self):
                    processes = [
                        "1 root    0:01 [init]",
                        "2 root    0:00 [kthreadd]",
                        "3 root    0:00 [rcu_gp]",
                        f"{random.randint(100, 999)} {self.current_user}    {random.randint(0, 10)}:{random.randint(0, 59):02d} python exp_os.py"
                    ]
                    return "\n".join(processes)

                def cmd_df(self):
                    total = random.randint(20, 100) * 1024
                    used = random.randint(5, total // 2)
                    free = total - used
                    percent = (used / total) * 100

                    output = [
                        "Filesystem     Size   Used  Avail Use% Mounted on",
                        f"/dev/vda1     {total}K  {used}K  {free}K {percent:.0f}% /"
                    ]
                    return "\n".join(output)

                def cmd_alias(self, args):
                    if not args:
                        if not self.aliases:
                            return "Алиасы не определены."
                        return "\n".join([f"{k}='{v}'" for k, v in self.aliases.items()])

                    try:
                        alias_name, alias_value = args[0].split("=", 1)
                        self.aliases[alias_name] = alias_value
                        self.save_state()
                        return f"Алиас '{alias_name}' создан."
                    except ValueError:
                        return "Использование: alias имя=команда"

                def cmd_view(self, args):
                    if not args:
                        return "Использование: view <файл>"

                    filename = args[0]
                    if filename not in self.vfs:
                        return f"Файл не найден: {filename}"

                    content = self.vfs[filename]["content"]
                    return f"=== Содержимое {filename} ===\n{content}"

                def cmd_color(self, args):
                    if not args:
                        return f"Текущая тема: {self.current_theme}. Доступные: dark, light"

                    theme = args[0]
                    if theme in self.theme_colors:
                        self.current_theme = theme
                        self.save_state()
                        return f"Тема изменена на {theme}."
                    else:
                        return f"Неизвестная тема. Доступные: {', '.join(self.theme_colors.keys())}"

                def cmd_tictactoe(self):
                    # Простая реализация игры в крестики-нолики
                    board = [" " for _ in range(9)]

                    def print_board():
                        for i in range(0, 9, 3):
                            print(" | ".join(board[i:i + 3]))
                            if i < 6:
                                print("---------")

                    def check_winner():
                        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
                        for a, b, c in lines:
                            if board[a] == board[b] == board[c] != " ":
                                return board[a]
                        return None

                    current_player = "X"
                    print("Игра в крестики-нолики. Введите номер клетки (1-9):")

                    for _ in range(9):
                        print_board()
                        try:
                            move = int(input(f"Ход {current_player}: ")) - 1
                            if move < 0 or move > 8 or board[move] != " ":
                                print("Неверный ход!")
                                continue
                            board[move] = current_player
                            winner = check_winner()
                            if winner:
                                print_board()
                                print(f"Победил {winner}!")
                                return ""
                            current_player = "O" if current_player == "X" else "X"
                        except ValueError:
                            print("Введите число от 1 до 9.")
                            continue

                    print_board()
                    return "Ничья!"

                def cmd_chmod(self, args):
                    if len(args) != 2:
                        return "Использование: chmod <права> <файл>"

                    perms, filename = args
                    if filename not in self.vfs:
                        return f"Файл не найден: {filename}"

                    self.vfs[filename]["perms"] = perms
                    return f"Права для {filename} изменены на {perms}"

                def save_history(self):
                    """Сохранить историю команд"""
                    try:
                        with open('.expos_history', 'w', encoding='utf-8') as f:
                            f.write('\n'.join(self.history[-100:]))  # Сохраняем последние 100 команд
                        logging.info(self._('history_saved'))
                    except Exception as e:
                        logging.error(f"{self._('history_save_error')}{e}")

            # --- ЗАПУСК СИСТЕМЫ ---

            if __name__ == '__main__':
                os = ExpOS()
                os.run()

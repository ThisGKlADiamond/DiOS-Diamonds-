import sys
import operator
import ast
import datetime
import os as py_os
import platform
import random
import time
import shutil
import json

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# --- ASCII Pictures (Standard Images) ---
PICS = {
    'logo': """
      ███████╗██╗  ██╗██████╗     ██████╗ ███████╗
      ██╔════╝╚██╗██╔╝██╔══██╗   ██╔═══██╗██╔════╝
      █████╗   ╚███╔╝ ██████╔╝   ██║   ██║███████╗
      ██╔══╝   ██╔██╗ ██╔═══╝    ██║   ██║╚════██║
      ███████╗██╔╝ ██╗██║        ╚██████╔╝███████║
      ╚══════╝╚═╝  ╚═╝╚═╝         ╚═════╝ ╚══════╝
    """,
    'cat': """
       /\_/\ 
      ( o.o )
       > ^ <
    """,
    'computer': """
       .---------------.
      | .------------. |
      | | EXP OS     | |
      | | 2026 (c)   | |
      | '------------' |
       '---------------'
            |  |
         _.-'  '-._
        '----------'
    """
}

# --- Translation Dictionary ---
LANGUAGES = {
    'en': {
        'welcome': "Welcome back, {name}! Press 'help' for the list of commands.",
        'started': "EXP OS {version} started.",
        'shutdown': "Shutting down EXP OS...",
        'restarting': "Restarting EXP OS...",
        'not_found': "Error: command '{cmd}' not found.",
        'avail_cmd': "Available Commands:",
        'no_help': "No help available for command '{cmd}'.",
        'hist_empty': "History is empty.",
        'dir_empty': "Directory is empty.",
        'boot_init': "Initializing hardware interface...",
        'boot_kernel': "Loading system kernel...",
        'boot_fs': "Mounting virtual file system...",
        'boot_session': "Starting user session...",
        'boot_ready': "System ready!                   ",
        'menu_title': "--- Main Menu ---",
        'menu_prompt': "Menu > ",
        'menu_help': "Options: 'settings', 'restart', 'shutdown', 'back'",
        'desc_menu': "Open main menu (settings, power options)",
        'set_title': "--- Settings Menu ---",
        'set_prompt': "Settings > ",
        'set_help': "Options: 'sysinfo', 'lang', 'datetime', 'back'",
        'lang_choose': "Available: en, fr, nl, ru.\nChoose language: ",
        'lang_set': "Language successfully set.",
        'desc_help': "Show this help",
        'desc_echo': "Print the given text",
        'desc_calc': "Calculate math (e.g., calc 2+2)",
        'desc_clear': "Clear the screen",
        'desc_time': "Show current date and time",
        'desc_history': "Show command history",
        'desc_ls': "List files in current folder",
        'desc_game': "Play a number guessing game",
        'desc_touch': "Create an empty file",
        'desc_cat': "Read file content",
        'desc_mkdir': "Create a new directory",
        'desc_rm': "Remove a file or directory",
        'desc_whoami': "Display current user name",
        'desc_gallery': "View standard system pictures",
        'desc_fmenu': "Open File Mini-Menu (copy, paste, undo, import)",
        'sys_info_title': "--- System Information ---",
        'sys_storage': "--- Storage & Memory ---",
        'sys_unavailable': "Unavailable",
        'sys_ram_req': "Requires 'psutil' module",
        'file_err': "Please specify a name/path.",
        'file_not_found': "Error: '{file}' not found.",
        'file_created': "Item '{file}' created.",
        'file_deleted': "Item '{file}' deleted.",
        'file_read_err': "Error: {error}"
    },
    'ru': {
        'welcome': "С возвращением, {name}! Введите 'help' для списка команд.",
        'started': "EXP OS {version} запущена.",
        'shutdown': "Завершение работы EXP OS...",
        'restarting': "Перезагрузка EXP OS...",
        'not_found': "Ошибка: команда '{cmd}' не найдена.",
        'avail_cmd': "Доступные команды:",
        'no_help': "Нет справки для '{cmd}'.",
        'hist_empty': "История пуста.",
        'dir_empty': "Папка пуста.",
        'boot_init': "Инициализация оборудования...",
        'boot_kernel': "Загрузка ядра системы...",
        'boot_fs': "Монтирование файловой системы...",
        'boot_session': "Запуск пользовательской сессии...",
        'boot_ready': "Система готова!                   ",
        'menu_title': "--- Главное Меню ---",
        'menu_prompt': "Меню > ",
        'menu_help': "Опции: 'settings', 'restart', 'shutdown', 'back'",
        'desc_menu': "Открыть главное меню",
        'set_title': "--- Настройки ---",
        'set_prompt': "Настройки > ",
        'set_help': "Опции: 'sysinfo', 'lang', 'datetime', 'back'",
        'lang_choose': "Доступно: en, fr, nl, ru.\nВыберите язык: ",
        'lang_set': "Язык успешно изменен.",
        'desc_help': "Показать эту справку",
        'desc_echo': "Вывести текст на экран",
        'desc_calc': "Калькулятор (напр., calc 2+2)",
        'desc_clear': "Очистить экран",
        'desc_time': "Показать дату и время",
        'desc_history': "Показать историю команд",
        'desc_ls': "Список файлов и папок",
        'desc_game': "Игра 'Угадай число'",
        'desc_touch': "Создать пустой файл",
        'desc_cat': "Прочитать файл",
        'desc_mkdir': "Создать новую папку",
        'desc_rm': "Удалить файл или папку",
        'desc_whoami': "Показать имя пользователя",
        'desc_gallery': "Просмотр стандартных картинок",
        'desc_fmenu': "Мини-меню файлов (копировать, вставить, импорт, отмена)",
        'sys_info_title': "--- Информация о системе ---",
        'sys_storage': "--- Память и Накопители ---",
        'sys_unavailable': "Недоступно",
        'sys_ram_req': "Требуется модуль 'psutil'",
        'file_err': "Укажите имя или путь.",
        'file_not_found': "Ошибка: '{file}' не найдено.",
        'file_created': "Объект '{file}' создан.",
        'file_deleted': "Объект '{file}' удален.",
        'file_read_err': "Ошибка: {error}"
    },
    'fr': {  # (Краткая версия для экономии места, использует ключи EN по умолчанию если не найдено)
        'welcome': "Bon retour, {name}! Tapez 'help' pour l'aide.",
        'desc_help': "Afficher l'aide",
        'desc_fmenu': "Ouvrir le mini-menu des fichiers"
    },
    'nl': {
        'welcome': "Welkom terug, {name}! Typ 'help' voor hulp.",
        'desc_help': "Toon hulp",
        'desc_fmenu': "Open Bestandsmenu"
    }
}


class EXPOS:
    def __init__(self):
        self.running = True
        self.is_restarting = False
        self.version = "alpha 0.0.2 Build 13"
        self.history = []
        self.username = "User"
        self.lang = "ru"  # По умолчанию ставим русский
        self.config_file = ".expos_config"
        self.trash_dir = ".expos_trash"

        # Настройки времени
        self.tz_offset_hours = 0
        self.time_offset_seconds = 0

        # Буфер обмена и история файлов
        self.clipboard = None  # ('copy'|'cut', 'source_path')
        self.undo_stack = []
        self.redo_stack = []

        self.commands = {
            'help': self.cmd_help,
            'menu': self.cmd_menu,
            'echo': self.cmd_echo,
            'calc': self.cmd_calc,
            'clear': self.cmd_clear,
            'time': self.cmd_time,
            'history': self.cmd_history,
            'ls': self.cmd_ls,
            'game': self.cmd_game,
            'touch': self.cmd_touch,
            'cat': self.cmd_cat,
            'mkdir': self.cmd_mkdir,
            'rm': self.cmd_rm,
            'whoami': self.cmd_whoami,
            'gallery': self.cmd_gallery,
            'fmenu': self.cmd_fmenu
        }

    @property
    def help_text(self):
        return {k: self.t(f'desc_{k}') for k in self.commands.keys()}

    def t(self, key, **kwargs):
        text = LANGUAGES.get(self.lang, LANGUAGES['en']).get(key, LANGUAGES['en'].get(key, key))
        return text.format(**kwargs) if kwargs else text

    def get_current_time(self):
        # Автоматическое системное время + смещения настроек
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours=self.tz_offset_hours,
                                                             seconds=self.time_offset_seconds)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def load_config(self):
        py_os.makedirs(self.trash_dir, exist_ok=True)
        if py_os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.loads(f.read().strip())
                    self.username = config.get('username', 'User')
                    self.lang = config.get('lang', 'ru')
                    self.tz_offset_hours = config.get('tz_hours', 0)
                    self.time_offset_seconds = config.get('t_secs', 0)
            except:
                pass
        else:
            self.run_installation()

    def save_config(self):
        config = {
            'username': self.username, 'lang': self.lang,
            'tz_hours': self.tz_offset_hours, 't_secs': self.time_offset_seconds
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except:
            pass

    def run_installation(self):
        self.cmd_clear("")
        print(">>> EXP OS Deployment System <<<")
        time.sleep(0.5)
        while True:
            name = input("Enter System Username (Введите имя): ").strip()
            if name:
                self.username = name
                break
        self.lang = "ru"
        self.save_config()
        self.cmd_clear("")

    def boot_sequence(self):
        self.cmd_clear("")
        print(f"EXP OS Core v.{self.version}")
        print("EXP OS 2026 © All Rights Reserved\n")

        for i in range(1, 101):
            blocks = int((i / 100) * 30)
            bar = '█' * blocks + '░' * (30 - blocks)

            if i < 30:
                status = self.t('boot_init')
            elif i < 60:
                status = self.t('boot_kernel')
            elif i < 85:
                status = self.t('boot_fs')
            else:
                status = self.t('boot_session')

            sys.stdout.write(f"\rLoading: [{bar}] {i}% | {status}")
            sys.stdout.flush()
            time.sleep(random.uniform(0.005, 0.02))

        print(f"\n\n{self.t('boot_ready')}")
        time.sleep(0.5)
        self.cmd_clear("")

    def print_taskbar(self):
        width = 70
        print("=" * width)
        tz_str = f"UTC{'+' + str(self.tz_offset_hours) if self.tz_offset_hours >= 0 else self.tz_offset_hours}"
        info = f" {self.get_current_time()} | {self.username} | {tz_str} "
        print(f"| EXP OS 2026 {info:>{width - 15}}|")
        print("=" * width)

    def start(self):
        self.load_config()
        self.boot_sequence()
        self.print_taskbar()
        print(self.t('started', version=self.version))
        print(self.t('welcome', name=self.username))

        while self.running:
            try:
                user_input = input(f"[{self.username}@expos ~]$ ").strip()
                if not user_input: continue
                self.history.append(user_input)
                self.execute_command(user_input)
            except (KeyboardInterrupt, EOFError):
                self.cmd_shutdown("")

    def execute_command(self, command_line):
        parts = command_line.split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''
        if cmd in self.commands:
            self.commands[cmd](args)
        else:
            print(self.t('not_found', cmd=cmd))

    # --- Core Commands ---
    def cmd_help(self, args):
        print("\nEXP OS 2026 © All Rights Reserved")
        print(f"{self.t('avail_cmd')}")
        for cmd, desc in self.help_text.items():
            print(f"  {cmd:<10} : {desc}")

    def cmd_echo(self, args):
        print(args)

    def cmd_time(self, args):
        print(self.get_current_time())

    def cmd_history(self, args):
        if not self.history:
            print(self.t('hist_empty'))
        else:
            for i, cmd in enumerate(self.history, 1): print(f"{i:3}: {cmd}")

    def cmd_whoami(self, args):
        print(self.username)

    def cmd_gallery(self, args):
        print("--- Standard Pictures Gallery ---")
        for name in PICS.keys():
            print(f"- {name}")
        choice = input("Enter picture name to view (or 'exit'): ").strip().lower()
        if choice in PICS:
            print(PICS[choice])
        elif choice != 'exit':
            print("Picture not found.")

    # --- FS Commands ---
    def cmd_ls(self, args):
        try:
            files = [f for f in py_os.listdir('.') if f != self.trash_dir and not f.startswith('.expos')]
            if not files:
                print(self.t('dir_empty'))
            else:
                for f in sorted(files):
                    tag = "[DIR] " if py_os.path.isdir(f) else "[FILE]"
                    print(f"{tag} {f}")
        except Exception as e:
            print(f"FS Error: {e}")

    def cmd_mkdir(self, args):
        if not args: print(self.t('file_err')); return
        try:
            py_os.makedirs(args, exist_ok=True); print(self.t('file_created', file=args))
        except Exception as e:
            print(self.t('file_read_err', error=e))

    def cmd_rm(self, args):
        if not args: print(self.t('file_err')); return
        if not py_os.path.exists(args): print(self.t('file_not_found', file=args)); return
        try:
            # Move to virtual trash for UNDO functionality
            trash_path = py_os.path.join(self.trash_dir, f"{int(time.time())}_{py_os.path.basename(args)}")
            shutil.move(args, trash_path)
            self.undo_stack.append({'action': 'delete', 'orig': args, 'trash': trash_path})
            self.redo_stack.clear()
            print(self.t('file_deleted', file=args))
        except Exception as e:
            print(self.t('file_read_err', error=e))

    def cmd_touch(self, args):
        if not args: print(self.t('file_err')); return
        try:
            with open(args, 'a'):
                pass
            print(self.t('file_created', file=args))
        except Exception as e:
            print(self.t('file_read_err', error=e))

    def cmd_cat(self, args):
        if not args: print(self.t('file_err')); return
        if not py_os.path.exists(args): print(self.t('file_not_found', file=args)); return
        if py_os.path.isdir(args): print(self.t('file_read_err', error="Is a directory")); return
        try:
            with open(args, 'r', encoding='utf-8') as f:
                print(f.read())
        except Exception as e:
            print(self.t('file_read_err', error=e))

    # --- File Mini-Menu (Context Menu Simulator) ---
    def cmd_fmenu(self, args):
        while True:
            print("\n--- File Mini-Menu ---")
            print("1. Create File/Folder")
            print("2. Delete")
            print("3. Copy")
            print("4. Cut")
            print("5. Paste")
            print(f"6. Undo (Available: {len(self.undo_stack)})")
            print(f"7. Redo (Available: {len(self.redo_stack)})")
            print("8. Import from Host OS")
            print("9. Refresh Screen")
            print("0. Exit")

            choice = input("fmenu > ").strip()

            if choice == '1':
                t = input("Type (file/dir): ").strip().lower()
                n = input("Name: ").strip()
                if t == 'dir':
                    self.cmd_mkdir(n)
                else:
                    self.cmd_touch(n)

            elif choice == '2':
                self.cmd_rm(input("Target to delete: ").strip())

            elif choice == '3':
                src = input("Target to copy: ").strip()
                if py_os.path.exists(src):
                    self.clipboard = ('copy', src)
                    print("Copied to clipboard.")
                else:
                    print("File not found.")

            elif choice == '4':
                src = input("Target to cut: ").strip()
                if py_os.path.exists(src):
                    self.clipboard = ('cut', src)
                    print("Cut to clipboard.")
                else:
                    print("File not found.")

            elif choice == '5':
                if not self.clipboard:
                    print("Clipboard is empty.")
                else:
                    mode, src = self.clipboard
                    dest = input(f"Destination name for '{src}': ").strip()
                    try:
                        if mode == 'copy':
                            if py_os.path.isdir(src):
                                shutil.copytree(src, dest)
                            else:
                                shutil.copy2(src, dest)
                            self.undo_stack.append({'action': 'paste_copy', 'dest': dest})
                        elif mode == 'cut':
                            shutil.move(src, dest)
                            self.undo_stack.append({'action': 'paste_cut', 'src': src, 'dest': dest})
                            self.clipboard = None  # Clear after cut
                        self.redo_stack.clear()
                        print(f"Pasted as '{dest}'.")
                    except Exception as e:
                        print(f"Paste Error: {e}")

            elif choice == '6':  # UNDO
                if not self.undo_stack:
                    print("Nothing to undo.")
                else:
                    act = self.undo_stack.pop()
                    try:
                        if act['action'] == 'delete':
                            shutil.move(act['trash'], act['orig'])
                            self.redo_stack.append(act)
                            print(f"Undo: Restored '{act['orig']}'")
                        elif act['action'] == 'paste_copy':
                            if py_os.path.isdir(act['dest']):
                                shutil.rmtree(act['dest'])
                            else:
                                py_os.remove(act['dest'])
                            self.redo_stack.append(act)
                            print(f"Undo: Removed pasted item '{act['dest']}'")
                        elif act['action'] == 'paste_cut':
                            shutil.move(act['dest'], act['src'])
                            self.redo_stack.append(act)
                            print(f"Undo: Moved '{act['dest']}' back to '{act['src']}'")
                    except Exception as e:
                        print(f"Undo Failed: {e}")

            elif choice == '7':  # REDO
                if not self.redo_stack:
                    print("Nothing to redo.")
                else:
                    act = self.redo_stack.pop()
                    try:
                        if act['action'] == 'delete':
                            shutil.move(act['orig'], act['trash'])
                            self.undo_stack.append(act)
                            print(f"Redo: Deleted '{act['orig']}'")
                        elif act['action'] == 'paste_copy':
                            print(
                                "Redo for copy-paste requires original file context. (Not fully supported in simple OS)")
                        elif act['action'] == 'paste_cut':
                            shutil.move(act['src'], act['dest'])
                            self.undo_stack.append(act)
                            print(f"Redo: Moved '{act['src']}' to '{act['dest']}'")
                    except Exception as e:
                        print(f"Redo Failed: {e}")

            elif choice == '8':  # IMPORT
                print("WARNING: Use absolute path from your real computer (e.g. C:\\Users\\...\\file.txt)")
                host_path = input("Host Path: ").strip()
                if py_os.path.exists(host_path):
                    try:
                        basename = py_os.path.basename(host_path)
                        if py_os.path.isdir(host_path):
                            shutil.copytree(host_path, basename)
                        else:
                            shutil.copy2(host_path, basename)
                        print(f"Successfully imported '{basename}'.")
                    except Exception as e:
                        print(f"Import Error: {e}")
                else:
                    print("Host path not found.")

            elif choice == '9':
                self.cmd_clear("")
                self.print_taskbar()
            elif choice == '0' or choice == 'exit':
                break
            else:
                print("Invalid choice.")

    # --- System & Menus ---
    def cmd_menu(self, args):
        print(f"\n{self.t('menu_title')}\n{self.t('menu_help')}")
        while self.running:
            cmd = input(self.t('menu_prompt')).strip().lower()
            if cmd in ['back', 'exit']:
                break
            elif cmd == 'settings':
                self.cmd_settings("")
            elif cmd == 'restart':
                self.cmd_restart("")
            elif cmd == 'shutdown':
                self.cmd_shutdown("")

    def cmd_settings(self, args):
        print(f"\n{self.t('set_title')}\n{self.t('set_help')}")
        while self.running:
            cmd = input(self.t('set_prompt')).strip().lower()
            if cmd in ['back', 'exit']:
                break
            elif cmd == 'sysinfo':
                self.run_sysinfo()
            elif cmd == 'lang':
                self.run_lang()
            elif cmd == 'datetime':
                self.run_datetime_settings()

    def run_datetime_settings(self):
        print("\n--- Date & Time Settings ---")
        print(f"Current System Time : {self.get_current_time()}")
        print(
            f"Current Timezone    : UTC{'+' + str(self.tz_offset_hours) if self.tz_offset_hours >= 0 else self.tz_offset_hours}")
        print("1. Change Timezone")
        print("2. Shift Time (Add/Remove Hours)")
        print("3. Reset to Default")
        print("0. Back")

        c = input("Choice: ").strip()
        if c == '1':
            try:
                self.tz_offset_hours = int(input("Enter timezone offset (-12 to +14): ").strip())
                self.save_config()
                print("Timezone updated.")
            except:
                print("Invalid input.")
        elif c == '2':
            try:
                h = int(input("Add hours (negative to subtract): ").strip())
                self.time_offset_seconds += h * 3600
                self.save_config()
                print("Time shifted.")
            except:
                print("Invalid input.")
        elif c == '3':
            self.tz_offset_hours = 0
            self.time_offset_seconds = 0
            self.save_config()
            print("Time settings reset.")

    def run_sysinfo(self):
        print(f"\n{self.t('sys_info_title')}")
        print(f"Build Version  : {self.version}")
        print(f"User           : {self.username}")
        print(f"OS Platform    : {platform.system()} {platform.release()}")
        print(self.t('sys_storage'))
        try:
            total, used, free = shutil.disk_usage(py_os.path.abspath(py_os.sep))
            print(f"Disk Total     : {total // (2 ** 30)} GB")
            print(f"Disk Free      : {free // (2 ** 30)} GB")
        except:
            print(f"Disk           : {self.t('sys_unavailable')}")

        if HAS_PSUTIL:
            mem = psutil.virtual_memory()
            print(f"RAM Total      : {mem.total // (2 ** 20)} MB")
        else:
            print(f"RAM            : {self.t('sys_ram_req')}")

    def run_lang(self):
        new_lang = input(self.t('lang_choose')).strip().lower()
        if new_lang in LANGUAGES:
            self.lang = new_lang
            self.save_config()
            print(self.t('lang_set'))
        else:
            print("Invalid Code.")

    def cmd_shutdown(self, args):
        print(self.t('shutdown'))
        time.sleep(1)
        self.running = False

    def cmd_restart(self, args):
        print(self.t('restarting'))
        time.sleep(1)
        self.running = False
        self.is_restarting = True

    def cmd_calc(self, args):
        if not args: print("Usage: calc <expr>"); return
        try:
            print(self.safe_eval(args))
        except Exception as e:
            print(f"Math Error: {e}")

    def safe_eval(self, expression):
        operators = {
            ast.Add: operator.add, ast.Sub: operator.sub,
            ast.Mult: operator.mul, ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
            ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos
        }

        def _eval(node):
            if isinstance(node, ast.Constant): return node.value
            if isinstance(node, ast.BinOp):
                return operators[type(node.op)](_eval(node.left), _eval(node.right))
            if isinstance(node, ast.UnaryOp):
                return operators[type(node.op)](_eval(node.operand))
            raise ValueError("Unsupported Operation")

        tree = ast.parse(expression, mode='eval')
        return _eval(tree.body)

    def cmd_clear(self, args):
        py_os.system('cls' if platform.system() == "Windows" else 'clear')

    def cmd_game(self, args):
        number = random.randint(1, 100)
        print("Guess Number (1-100). Type 'exit' to quit.")
        while True:
            inp = input("Guess > ").strip().lower()
            if inp == 'exit': break
            if not inp.isdigit(): continue
            guess = int(inp)
            if guess < number:
                print("Higher ↑")
            elif guess > number:
                print("Lower ↓")
            else:
                print("Correct!"); break


if __name__ == "__main__":
    while True:
        os_instance = EXPOS()
        os_instance.start()
        if not os_instance.is_restarting:
            break
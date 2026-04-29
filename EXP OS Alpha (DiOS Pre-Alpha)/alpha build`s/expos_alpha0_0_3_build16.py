"""
EXP OS / ЕХП ОС
Version: alpha 0.0.3 Build 16
Description: Advanced terminal-based operating system simulation.
Features: Virtual FS (nested, clipboard, undo/redo), Network Simulation, Media Viewer, Scripting, Games.
"""

import sys
import ast
import operator
import datetime
import os as py_os
import platform
import random
import time
import shutil
import json
import subprocess

# --- Опциональные зависимости ---
try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    if platform.system() != 'Windows':
        import readline

        HAS_READLINE = True
    else:
        import pyreadline3 as readline

        HAS_READLINE = True
except ImportError:
    HAS_READLINE = False

# =============================================================================
# РЕСУРСЫ: ЦВЕТА И ASCII-ГРАФИКА
# =============================================================================

COLORS = {
    'reset': '\033[0m', 'red': '\033[91m', 'green': '\033[92m',
    'yellow': '\033[93m', 'blue': '\033[94m', 'magenta': '\033[95m',
    'cyan': '\033[96m', 'white': '\033[97m'
}

LOGOS = {
    'en': """
       .-----------------------.
     .'                         '.
    /           EXP OS            \\
   |     ( a0.0.3 Build 16 )       |
    \\                             /
     '.                         .'
       '-----------------------'
    """,
    'ru': """
       .-----------------------.
     .'                         '.
    /           ЕХП ОС            \\
   |     ( a0.0.3 Build 16 )       |
    \\                             /
     '.                         .'
       '-----------------------'
    """
}

PICS = {
    'cat': """
       /\_/\ 
      ( o.o )
       > ^ <
    """,
    'computer': """
       .---------------.
      | .------------. |
      | | OS 2026    | |
      | | SYSTEM     | |
      | '------------' |
       '---------------'
            |  |
         _.-'  '-._
        '----------'
    """
}

# =============================================================================
# ЛОКАЛИЗАЦИЯ
# =============================================================================

LANGUAGES = {
    'ru': {
        'os_name': "ЕХП ОС",
        'welcome': "С возвращением, {name}! Введите 'help' для списка команд.",
        'started': "{os_name} {version} запущена.",
        'shutdown': "Завершение работы {os_name}...",
        'restarting': "Перезагрузка {os_name}...",
        'not_found': "Ошибка: команда '{cmd}' не найдена.",
        'avail_cmd': "Доступные команды:",
        'boot_init': "Инициализация оборудования...",
        'boot_kernel': "Загрузка ядра системы...",
        'boot_fs': "Монтирование файловой системы...",
        'boot_session': "Запуск пользовательской сессии...",
        'boot_ready': "Система готова!                   ",
        'menu_title': "--- Главное Меню ---",
        'menu_prompt': "Меню > ",
        'menu_help': "Опции: 'settings', 'restart', 'shutdown', 'back'",
        'set_title': "--- Настройки ---",
        'set_prompt': "Настройки > ",
        'set_help': "Опции: 'sysinfo', 'lang', 'datetime', 'color', 'back'",
        'lang_choose': "Доступно: en, ru.\nВыберите язык: ",
        'lang_set': "Язык успешно изменен.",
        'sys_info_title': "--- Информация о системе ---",
        'sys_storage': "--- Память и Накопители ---",
        'sys_unavailable': "Недоступно",
        'sys_ram_req': "Требуется модуль 'psutil'",
        'file_err': "Укажите имя или путь.",
        'file_not_found': "Ошибка: '{file}' не найдено.",
        'file_created': "Объект '{file}' создан.",
        'file_deleted': "Объект '{file}' удален.",
        'deploy_sys': ">>> Система Развертывания {os_name} <<<",
        'enter_user': "Введите имя пользователя: ",
        'boot_title': "{os_name} Ядро v.{version}",
        'copyright': "{os_name} 2026 © Все права защищены",
        'loading': "Загрузка: [{bar}] {pct}% | {status}",
        'gallery_title': "--- Галерея ---",
        'gallery_prompt': "Имя картинки (или 'exit'): ",
        'fmenu_title': "--- Мини-Меню Файлов ---",
        'fmenu_opts': "1.Создать 2.Удалить 3.Копировать 4.Вырезать 5.Вставить 6.Отмена 7.Возврат 8.Импорт 0.Выход",
        'fmenu_prompt': "файл-меню > ",
        'dt_title': "--- Дата и Время ---",
        'sys_build': "Версия Сборки : {version}",
        'sys_user': "Пользователь  : {user}",
        'sys_plat': "Платформа ОС  : {platform}",
        'sys_disk_tot': "Диск Всего    : {total} GB",
        'sys_disk_free': "Диск Свободно : {free} GB",
        'sys_ram_tot': "ОЗУ Всего     : {total} MB",
        'game_welcome': "Угадай число (1-100). 'exit' для выхода.",
        'game_high': "Выше ↑", 'game_low': "Ниже ↓", 'game_win': "Угадано!",
        'err_disk': "Ошибка доступа к диску/файлу: {err}",
        'ping_sim': "Обмен пакетами с {ip} по 32 байт:",
        'ping_reply': "Ответ от {ip}: число байт=32 время={time}мс TTL=117",
        'ping_timeout': "Превышен интервал ожидания.",
        'color_set': "Цветовая схема изменена на {color}",
        'script_err': "Ошибка скрипта: {err}",
        'media_open': "Открытие медиафайла {file}...",
        'media_err': "Формат не поддерживается или файл не найден.",
        'refresh_msg': "Рабочий стол обновлен."
    },
    'en': {
        'os_name': "EXP OS",
        'welcome': "Welcome back, {name}! Type 'help' for commands.",
        'started': "{os_name} {version} started.",
        'shutdown': "Shutting down {os_name}...",
        'restarting': "Restarting {os_name}...",
        'not_found': "Error: command '{cmd}' not found.",
        'avail_cmd': "Available Commands:",
        'boot_init': "Initializing hardware...",
        'boot_kernel': "Loading kernel...",
        'boot_fs': "Mounting FS...",
        'boot_session': "Starting session...",
        'boot_ready': "System ready!                   ",
        'menu_title': "--- Main Menu ---",
        'menu_prompt': "Menu > ",
        'menu_help': "Options: 'settings', 'restart', 'shutdown', 'back'",
        'set_title': "--- Settings ---",
        'set_prompt': "Settings > ",
        'set_help': "Options: 'sysinfo', 'lang', 'datetime', 'color', 'back'",
        'lang_choose': "en, ru.\nChoose: ",
        'lang_set': "Language set.",
        'sys_info_title': "--- System Info ---",
        'sys_storage': "--- Storage & RAM ---",
        'sys_unavailable': "N/A",
        'sys_ram_req': "Needs 'psutil'",
        'file_err': "Specify name.",
        'file_not_found': "Not found: '{file}'",
        'file_created': "Created '{file}'",
        'file_deleted': "Deleted '{file}'",
        'deploy_sys': ">>> {os_name} Deployment <<<",
        'enter_user': "Username: ",
        'boot_title': "{os_name} Core v.{version}",
        'copyright': "{os_name} 2026 © All Rights Reserved",
        'loading': "Loading: [{bar}] {pct}% | {status}",
        'gallery_title': "--- Gallery ---",
        'gallery_prompt': "Picture (or 'exit'): ",
        'fmenu_title': "--- File Menu ---",
        'fmenu_opts': "1.Create 2.Delete 3.Copy 4.Cut 5.Paste 6.Undo 7.Redo 8.Import 0.Exit",
        'fmenu_prompt': "fmenu > ",
        'dt_title': "--- Date/Time ---",
        'sys_build': "Build  : {version}",
        'sys_user': "User   : {user}",
        'sys_plat': "Platform: {platform}",
        'sys_disk_tot': "Disk Total: {total} GB",
        'sys_disk_free': "Disk Free : {free} GB",
        'sys_ram_tot': "RAM Total : {total} MB",
        'game_welcome': "Guess (1-100). 'exit' to quit.",
        'game_high': "Higher ↑", 'game_low': "Lower ↓", 'game_win': "Correct!",
        'err_disk': "Access error: {err}",
        'ping_sim': "Pinging {ip} with 32 bytes of data:",
        'ping_reply': "Reply from {ip}: bytes=32 time={time}ms TTL=117",
        'ping_timeout': "Request timed out.",
        'color_set': "Color scheme set to {color}",
        'script_err': "Script error: {err}",
        'media_open': "Opening media file {file}...",
        'media_err': "Unsupported format or file not found.",
        'refresh_msg': "Desktop refreshed."
    }
}


# =============================================================================
# ЯДРО И СИСТЕМА
# =============================================================================

class EXPOS:
    def __init__(self):
        # Базовые параметры
        self.running = True
        self.is_restarting = False
        self.version = "alpha 0.0.3 Build 16"
        self.username = "User"
        self.lang = "ru"
        self.ui_color = "white"

        # Системные директории и файлы
        self.config_file = ".expos_config"
        self.history_file = ".expos_history"
        self.trash_dir = ".expos_trash"
        self.start_dir = py_os.getcwd()

        # Переменные сессии
        self.history = []
        self.tz_offset_hours = 0
        self.time_offset_seconds = 0
        self.clipboard = None
        self.undo_stack = []
        self.redo_stack = []

        # Реестр команд
        self.commands = {
            'help': self.cmd_help, 'menu': self.cmd_menu, 'echo': self.cmd_echo,
            'calc': self.cmd_calc, 'clear': self.cmd_clear, 'time': self.cmd_time,
            'history': self.cmd_history, 'whoami': self.cmd_whoami,

            # Файловая система
            'ls': self.cmd_ls, 'cd': self.cmd_cd, 'pwd': self.cmd_pwd,
            'mkdir': self.cmd_mkdir, 'touch': self.cmd_touch, 'cat': self.cmd_cat,
            'rm': self.cmd_rm, 'fmenu': self.cmd_fmenu,

            # Сеть и Скрипты
            'ping': self.cmd_ping, 'ipconfig': self.cmd_ipconfig, 'run': self.cmd_run,

            # Медиа и Графика
            'view': self.cmd_view, 'refresh': self.cmd_refresh, 'color': self.cmd_color,
            'gallery': self.cmd_gallery, 'sysinfo': self.run_sysinfo,

            # Игры и Утилиты
            'game': self.cmd_game, 'tictactoe': self.cmd_tictactoe, 'stopwatch': self.cmd_stopwatch
        }

    def t(self, key, **kwargs):
        """Функция локализации текста"""
        base = LANGUAGES.get(self.lang, LANGUAGES['en'])
        text = base.get(key, LANGUAGES['en'].get(key, key))
        return text.format(**kwargs) if kwargs else text

    def get_logo(self):
        return LOGOS.get(self.lang if self.lang == 'ru' else 'en')

    def get_current_time(self):
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours=self.tz_offset_hours,
                                                             seconds=self.time_offset_seconds)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # --- Конфигурация и Инициализация ---
    def load_config(self):
        try:
            py_os.makedirs(self.trash_dir, exist_ok=True)
        except:
            pass

        if py_os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.username = config.get('username', 'User')
                    self.lang = config.get('lang', 'ru')
                    self.tz_offset_hours = config.get('tz_hours', 0)
                    self.time_offset_seconds = config.get('t_secs', 0)
                    self.ui_color = config.get('color', 'white')
            except:
                pass
        else:
            self.run_installation()

        if py_os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = [line.strip() for line in f.readlines()]
            except:
                pass

    def save_config(self):
        config = {
            'username': self.username, 'lang': self.lang,
            'tz_hours': self.tz_offset_hours, 't_secs': self.time_offset_seconds,
            'color': self.ui_color
        }
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                for item in self.history[-100:]: f.write(f"{item}\n")
        except:
            pass

    def run_installation(self):
        self.cmd_clear("")
        print(self.t('deploy_sys', os_name="EXP/ЕХП"))
        while True:
            name = input(self.t('enter_user')).strip()
            if name:
                self.username = name
                break
        self.lang = "ru"
        self.save_config()

    def boot_sequence(self):
        self.cmd_clear("")
        print(self.get_logo())
        print(self.t('boot_title', os_name=self.t('os_name'), version=self.version))
        print(self.t('copyright', os_name=self.t('os_name')) + "\n")

        for i in range(1, 101, 2):
            blocks = int((i / 100) * 30)
            bar = '#' * blocks + '-' * (30 - blocks)
            if i < 30:
                status = self.t('boot_init')
            elif i < 60:
                status = self.t('boot_kernel')
            elif i < 85:
                status = self.t('boot_fs')
            else:
                status = self.t('boot_session')
            sys.stdout.write(f"\r" + self.t('loading', bar=bar, pct=i, status=status))
            sys.stdout.flush()
            time.sleep(random.uniform(0.01, 0.04))
        print(f"\n\n{self.t('boot_ready')}")
        time.sleep(0.5)
        self.cmd_refresh("")

    def print_taskbar(self):
        width = 70
        print("=" * width)
        info = f" {self.get_current_time()} | {self.username} "
        os_n = self.t('os_name')
        print(f"| {os_n} {self.version} {info:>{width - len(os_n) - len(self.version) - 4}}|")
        print("=" * width)

    # --- Базовые Команды ---
    def cmd_help(self, args):
        print("\n" + self.t('avail_cmd'))
        cmds = list(self.commands.keys()) + ['exit']
        # Разбиваем на колонки для красоты
        cmds.sort()
        for i in range(0, len(cmds), 4):
            print("  ".join([f"{cmd:<12}" for cmd in cmds[i:i + 4]]))

    def cmd_echo(self, args):
        print(args)

    def cmd_time(self, args):
        print(self.get_current_time())

    def cmd_whoami(self, args):
        print(self.username)

    def cmd_clear(self, args):
        py_os.system('cls' if platform.system() == "Windows" else 'clear')

    def cmd_history(self, args):
        for i, cmd in enumerate(self.history[-20:], 1): print(f"{i:3}: {cmd}")

    def cmd_color(self, args):
        if args in COLORS:
            self.ui_color = args
            self.save_config()
            print(self.t('color_set', color=args))
        else:
            print(f"Цвета: {', '.join(COLORS.keys())}")

    def cmd_refresh(self, args):
        self.cmd_clear("")
        self.print_taskbar()
        print(f"\n[{self.username} Окружение - {py_os.getcwd()}]")
        self.cmd_ls("")
        print("\n" + self.t('refresh_msg'))

    # --- Файловая Система ---
    def cmd_pwd(self, args):
        print(py_os.getcwd())

    def cmd_cd(self, args):
        if not args: args = self.start_dir
        try:
            py_os.chdir(args)
        except Exception as e:
            print(self.t('err_disk', err=e))

    def cmd_ls(self, args):
        try:
            target = args if args else '.'
            items = py_os.listdir(target)
            filtered = [i for i in items if not i.startswith('.expos')]
            if not filtered: print("Пусто.")
            for item in sorted(filtered):
                path = py_os.path.join(target, item)
                print(f"{'[DIR] ' if py_os.path.isdir(path) else '[FILE]'} {item}")
        except Exception as e:
            print(self.t('err_disk', err=e))

    def cmd_mkdir(self, args):
        if args:
            try:
                py_os.makedirs(args, exist_ok=True); print(self.t('file_created', file=args))
            except Exception as e:
                print(self.t('err_disk', err=e))

    def cmd_touch(self, args):
        if args:
            try:
                open(args, 'a').close(); print(self.t('file_created', file=args))
            except Exception as e:
                print(self.t('err_disk', err=e))

    def cmd_cat(self, args):
        if args:
            try:
                with open(args, 'r', encoding='utf-8') as f:
                    print(f.read())
            except Exception as e:
                print(self.t('err_disk', err=e))

    def cmd_rm(self, args):
        if not args: return
        try:
            # Перемещаем в корзину вместо полного удаления
            shutil.move(args, py_os.path.join(self.trash_dir, f"{int(time.time())}_{args}"))
            print(self.t('file_deleted', file=args))
            self.undo_stack.append(('rm', args, py_os.path.join(self.trash_dir, f"{int(time.time())}_{args}")))
        except Exception as e:
            print(self.t('err_disk', err=e))

    # --- Мини-меню файлов (fmenu) с поддержкой буфера обмена ---
    def cmd_fmenu(self, args):
        while True:
            print(f"\n{self.t('fmenu_title')}")
            print(self.t('fmenu_opts'))
            c = input(self.t('fmenu_prompt')).strip()

            if c == '0':
                break
            elif c == '1':
                self.cmd_touch(input("Имя нового файла: "))
            elif c == '2':
                self.cmd_rm(input("Имя файла для удаления: "))
            elif c == '3':
                src = input("Что копировать: ")
                if py_os.path.exists(src):
                    self.clipboard = ('copy', src); print("Скопировано.")
                else:
                    print("Не найдено.")
            elif c == '4':
                src = input("Что вырезать: ")
                if py_os.path.exists(src):
                    self.clipboard = ('cut', src); print("Вырезано.")
                else:
                    print("Не найдено.")
            elif c == '5':
                if not self.clipboard:
                    print("Буфер пуст.")
                else:
                    action, src = self.clipboard
                    dest = input(f"Новое имя для '{src}': ")
                    try:
                        if action == 'copy':
                            shutil.copy(src, dest)
                        elif action == 'cut':
                            shutil.move(src, dest); self.clipboard = None
                        print(f"Вставлено как '{dest}'")
                    except Exception as e:
                        print(f"Ошибка: {e}")
            elif c == '8':
                path = input("Абсолютный путь с хост-системы: ")
                try:
                    shutil.copy(path, '.')
                    print("Успешно импортировано.")
                except Exception as e:
                    print(f"Ошибка: {e}")
            elif c == '6' or c == '7':
                print("Функция Undo/Redo в доработке (Доступно базовое удаление корзины).")

    # --- Мультимедиа ---
    def cmd_view(self, args):
        """Открывает фото (.png, .jpeg, .webp) и видео (.mp4) через хост-систему"""
        if not args: return print(self.t('media_err'))
        ext = args.lower().split('.')[-1]
        valid_exts = ['png', 'jpg', 'jpeg', 'webp', 'mp4', 'gif', 'avi']

        if ext in valid_exts and py_os.path.exists(args):
            print(self.t('media_open', file=args))
            try:
                if platform.system() == 'Windows':
                    py_os.startfile(args)
                elif platform.system() == 'Darwin':
                    subprocess.call(('open', args))
                else:
                    subprocess.call(('xdg-open', args))
            except Exception as e:
                print(self.t('err_disk', err=e))
        else:
            print(self.t('media_err'))

    def cmd_gallery(self, args):
        print(f"\n{self.t('gallery_title')}")
        for name in PICS: print(f"- {name}")
        c = input(self.t('gallery_prompt')).strip()
        if c in PICS: print(PICS[c])

    # --- Сеть и Скрипты ---
    def cmd_run(self, args):
        if not args: return print("Укажите файл скрипта (напр. run script.txt)")
        try:
            with open(args, 'r', encoding='utf-8') as f:
                for line in f:
                    cmd = line.strip()
                    if cmd and not cmd.startswith('#'):
                        print(f"{COLORS['yellow']}> {cmd}{COLORS[self.ui_color]}")
                        self.execute_command(cmd)
                        time.sleep(0.5)
        except Exception as e:
            print(self.t('script_err', err=e))

    def cmd_ping(self, args):
        ip = args if args else "127.0.0.1"
        print(self.t('ping_sim', ip=ip))
        for _ in range(4):
            time.sleep(0.8)
            if random.random() > 0.1:
                print(self.t('ping_reply', ip=ip, time=random.randint(10, 80)))
            else:
                print(self.t('ping_timeout'))

    def cmd_ipconfig(self, args):
        print("\nКонфигурация IP для EXP OS")
        print(f"IPv4-адрес. . . . . . . . . . . : 192.168.0.{random.randint(2, 254)}")
        print("Маска подсети . . . . . . . . . : 255.255.255.0")
        print("Основной шлюз . . . . . . . . . : 192.168.0.1\n")

    # --- Системные Меню и Настройки ---
    def run_sysinfo(self, args=""):
        print(self.get_logo())
        print(f"\n{self.t('sys_info_title')}")
        print(self.t('sys_build', version=self.version))
        print(self.t('sys_user', user=self.username))
        print(self.t('sys_plat', platform=platform.system()))
        print(f"Текущая директория: {py_os.getcwd()}")
        try:
            t, u, f = shutil.disk_usage(".")
            print(f"Диск Всего: {t // (2 ** 30)} GB | Свободно: {f // (2 ** 30)} GB")
        except:
            pass
        if HAS_PSUTIL:
            try:
                print(f"ОЗУ Всего : {psutil.virtual_memory().total // (1024 * 1024)} MB")
            except:
                pass

    def cmd_menu(self, args):
        while True:
            print(f"\n{self.t('menu_title')}\n{self.t('menu_help')}")
            c = input(self.t('menu_prompt')).lower()
            if c in ['back', 'exit']:
                break
            elif c == 'settings':
                self.cmd_settings()
            elif c == 'restart':
                self.is_restarting = True; self.running = False; break
            elif c == 'shutdown':
                self.running = False; break

    def cmd_settings(self):
        while True:
            print(f"\n{self.t('set_title')}\n{self.t('set_help')}")
            c = input(self.t('set_prompt')).lower()
            if c in ['back', 'exit']:
                break
            elif c == 'sysinfo':
                self.run_sysinfo()
            elif c == 'lang':
                nl = input(self.t('lang_choose')).strip().lower()
                if nl in LANGUAGES:
                    self.lang = nl;
                    self.save_config();
                    print(self.t('lang_set'))
            elif c == 'color':
                cl = input(f"Цвет ({', '.join(COLORS.keys())}): ").strip().lower()
                self.cmd_color(cl)
            elif c == 'datetime':
                try:
                    shift = int(input("Сдвиг часового пояса (-12 до 14): "))
                    self.tz_offset_hours = shift
                    self.save_config()
                    print("Время обновлено.")
                except:
                    print("Ошибка ввода.")

    # --- Утилиты и Игры ---
    def cmd_calc(self, args):
        if not args: return print("Использование: calc 2+2")
        try:
            print(eval(args, {"__builtins__": None}, {}))
        except Exception as e:
            print(f"Ошибка: {e}")

    def cmd_stopwatch(self, args):
        print("Секундомер. Нажмите Enter для старта, еще раз для остановки.")
        input()
        start = time.time()
        print("Идет отсчет...")
        input()
        print(f"Прошло: {round(time.time() - start, 2)} сек.")

    def cmd_game(self, args):
        n = random.randint(1, 100);
        print(self.t('game_welcome'))
        while True:
            i = input("> ");
            if i == 'exit': break
            if not i.isdigit(): continue
            g = int(i)
            if g < n:
                print(self.t('game_high'))
            elif g > n:
                print(self.t('game_low'))
            else:
                print(self.t('game_win')); break

    def cmd_tictactoe(self, args):
        print("Крестики-Нолики (Локальный мультиплеер)")
        board = [' '] * 9

        def draw():
            print(
                f"\n {board[0]} | {board[1]} | {board[2]} \n---+---+---\n {board[3]} | {board[4]} | {board[5]} \n---+---+---\n {board[6]} | {board[7]} | {board[8]} \n")

        turn = 'X'
        for _ in range(9):
            draw()
            try:
                move = int(input(f"Ход {turn} (1-9): ")) - 1
                if 0 <= move <= 8 and board[move] == ' ':
                    board[move] = turn
                    turn = 'O' if turn == 'X' else 'X'
                else:
                    print("Недопустимый ход!")
            except:
                print("Введите число от 1 до 9.")
        draw()
        print("Игра окончена!")

    # --- Обработка Команд и Жизненный Цикл ---
    def execute_command(self, cmd_line):
        parts = cmd_line.split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''

        if cmd == 'exit': self.running = False; return
        if cmd in self.commands:
            self.commands[cmd](args)
        else:
            print(self.t('not_found', cmd=cmd))

    def start(self):
        self.load_config()
        self.boot_sequence()
        print(self.t('welcome', name=self.username))

        # Автодополнение Tab
        if HAS_READLINE:
            def completer(text, state):
                options = [cmd for cmd in self.commands.keys() if cmd.startswith(text)]
                return options[state] if state < len(options) else None

            readline.set_completer(completer)
            readline.parse_and_bind("tab: complete")

        # Основной цикл
        while self.running:
            try:
                color_code = COLORS.get(self.ui_color, COLORS['white'])
                current_folder = py_os.path.basename(py_os.getcwd()) or "/"
                prompt = f"{color_code}[{self.username}@expos {current_folder}]$ {COLORS['reset']}"

                user_input = input(prompt).strip()
                if not user_input: continue

                self.history.append(user_input)
                print(color_code, end="")
                self.execute_command(user_input)
                print(COLORS['reset'], end="")

            except (KeyboardInterrupt, EOFError):
                self.running = False
            except Exception as e:
                print(f"\nКритическая ошибка оболочки: {e}")

        print(self.t('shutdown', os_name=self.t('os_name')))
        self.save_config()


if __name__ == "__main__":
    while True:
        os_inst = EXPOS()
        os_inst.start()
        if not os_inst.is_restarting: break
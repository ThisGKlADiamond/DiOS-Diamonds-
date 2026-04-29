"""
EXP OS / ЕХП ОС
Version: alpha 0.0.3 Build 19
Description: Advanced terminal-based OS simulation with Multi-language support (RU_RU, RU_BY, EN, FR, NL).
Features: Instant Desktop Refresh, Dynamic Logo, Virtual FS, Network Sim, Scripting, Games.
"""

import sys
import datetime
import os as py_os
import platform
import random
import time
import shutil
import json
import subprocess

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

PICS = {
    'cat': "\n       /\\_/\\ \n      ( o.o )\n       > ^ <\n",
    'computer': "\n       .---------------.\n      | .------------. |\n      | | OS 2026    | |\n      | | SYSTEM     | |\n      | '------------' |\n       '---------------'\n            |  |\n         _.-'  '-._\n        '----------'\n"
}

# =============================================================================
# БАЗА ЛОКАЛИЗАЦИИ
# =============================================================================

base_ru = {
    'welcome': "С возвращением, {name}!",
    'shutdown': "Завершение работы {os_name}...",
    'restarting': "Перезагрузка {os_name}...",
    'not_found': "Ошибка: команда '{cmd}' не найдена.",
    'avail_cmd': "Справочник команд:",
    'boot_init': "Инициализация оборудования...",
    'boot_kernel': "Загрузка ядра системы...",
    'boot_fs': "Монтирование файловой системы...",
    'boot_session': "Запуск пользовательской сессии...",
    'boot_ready': "Система готова!                   ",
    'menu_title': "--- Главное Меню ---",
    'menu_prompt': "Меню > ",
    'menu_help': "Опции: 'settings' (настройки), 'restart' (перезагрузка), 'shutdown' (выключение), 'back' (назад)",
    'set_title': "--- Настройки ---",
    'set_prompt': "Настройки > ",
    'set_help': "Опции: 'sysinfo', 'lang', 'datetime', 'color', 'back'",
    'lang_choose': "Доступно: ru_ru, ru_by, en, fr, nl.\nВыберите язык: ",
    'lang_set': "Язык успешно изменен.",
    'sys_info_title': "--- Информация о системе ---",
    'file_created': "Объект '{file}' создан.",
    'file_deleted': "Объект '{file}' удален в корзину.",
    'deploy_sys': ">>> Развертывание Системы <<<",
    'enter_user': "Введите имя пользователя: ",
    'boot_title': "{os_name} Ядро v.{version}",
    'loading': "Загрузка: [{bar}] {pct}% | {status}",
    'gallery_title': "--- Галерея ---",
    'gallery_prompt': "Имя картинки (или 'exit'): ",
    'fmenu_title': "--- Мини-Меню Файлов ---",
    'fmenu_opts': "1.Создать 2.Удалить 3.Копировать 4.Вырезать 5.Вставить 8.Импорт 0.Выход",
    'fmenu_prompt': "файл-меню > ",
    'dt_title': "--- Настройки Даты и Времени ---",
    'dt_menu': "1. Сдвиг часового пояса\n2. Сдвиг секунд\n3. Назад",
    'dt_prompt': "Выбор > ",
    'sys_build': "Версия Сборки : {version}",
    'sys_user': "Пользователь  : {user}",
    'sys_plat': "Платформа ОС  : {platform}",
    'game_welcome': "Угадай число (1-100). 'exit' для выхода.",
    'game_high': "Выше ↑", 'game_low': "Ниже ↓", 'game_win': "Угадано!",
    'err_disk': "Ошибка доступа: {err}",
    'ping_sim': "Обмен пакетами с {ip}:",
    'ping_reply': "Ответ от {ip}: время={time}мс",
    'ping_timeout': "Превышен интервал ожидания.",
    'color_set': "Цветовая схема изменена на {color}",
    'script_err': "Ошибка скрипта: {err}",
    'media_open': "Открытие медиафайла {file}...",
    'media_err': "Формат не поддерживается или файл не найден.",
    'refresh_msg': "Рабочий стол обновлен.",
    'help_notice': "Если вы не знаете, что означает данная команда, то введите 'help' чтобы поподробнее разобраться с командами.",

    # Подсказки
    'hint_help': "Справка по командам", 'hint_menu': "Главное системное меню",
    'hint_echo': "Вывод текста на экран", 'hint_calc': "Калькулятор",
    'hint_clear': "Очистка экрана", 'hint_time': "Текущее время",
    'hint_history': "История введенных команд", 'hint_whoami': "Имя текущего пользователя",
    'hint_ls': "Список файлов и папок", 'hint_cd': "Переход в другую папку",
    'hint_pwd': "Путь текущей папки", 'hint_mkdir': "Создать новую папку",
    'hint_touch': "Создать пустой файл", 'hint_cat': "Просмотр содержимого файла",
    'hint_rm': "Удаление файла/папки", 'hint_fmenu': "Графическое файловое меню",
    'hint_ping': "Проверка сетевого соединения", 'hint_ipconfig': "Сетевые настройки",
    'hint_run': "Выполнение файла скрипта", 'hint_view': "Просмотр фото и видео",
    'hint_refresh': "Обновление интерфейса (Рабочий стол)", 'hint_color': "Смена цвета терминала",
    'hint_gallery': "Просмотр ASCII-картинок", 'hint_game': "Игра 'Угадай число'",
    'hint_tictactoe': "Игра 'Крестики-Нолики'", 'hint_stopwatch': "Утилита секундомера"
}

LANGUAGES = {
    'ru_ru': {**base_ru, 'os_name': "ЕХП"},
    'ru_by': {**base_ru, 'os_name': "EXP"},
    'en': {
        'os_name': "EXP",
        'welcome': "Welcome back, {name}!",
        'shutdown': "Shutting down {os_name}...",
        'restarting': "Restarting {os_name}...",
        'not_found': "Error: command '{cmd}' not found.",
        'avail_cmd': "Command Reference:",
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
        'lang_choose': "Available: ru_ru, ru_by, en, fr, nl.\nChoose: ",
        'lang_set': "Language successfully changed.",
        'sys_info_title': "--- System Info ---",
        'file_created': "Created '{file}'.",
        'file_deleted': "Deleted '{file}' to trash.",
        'deploy_sys': ">>> System Deployment <<<",
        'enter_user': "Enter username: ",
        'boot_title': "{os_name} Core v.{version}",
        'loading': "Loading: [{bar}] {pct}% | {status}",
        'gallery_title': "--- Gallery ---",
        'gallery_prompt': "Picture name (or 'exit'): ",
        'fmenu_title': "--- File Menu ---",
        'fmenu_opts': "1.Create 2.Delete 3.Copy 4.Cut 5.Paste 8.Import 0.Exit",
        'fmenu_prompt': "fmenu > ",
        'dt_title': "--- Date & Time Settings ---",
        'dt_menu': "1. Timezone offset\n2. Seconds offset\n3. Back",
        'dt_prompt': "Select > ",
        'sys_build': "Build  : {version}",
        'sys_user': "User   : {user}",
        'sys_plat': "Platform: {platform}",
        'game_welcome': "Guess (1-100). 'exit' to quit.",
        'game_high': "Higher ↑", 'game_low': "Lower ↓", 'game_win': "Correct!",
        'err_disk': "Access error: {err}",
        'ping_sim': "Pinging {ip}:",
        'ping_reply': "Reply from {ip}: time={time}ms",
        'ping_timeout': "Request timed out.",
        'color_set': "Color scheme set to {color}",
        'script_err': "Script error: {err}",
        'media_open': "Opening media file {file}...",
        'media_err': "Unsupported format or file not found.",
        'refresh_msg': "Desktop refreshed.",
        'help_notice': "If you don't know what a command means, type 'help' to learn more about the commands.",

        'hint_help': "Command reference", 'hint_menu': "Main system menu",
        'hint_echo': "Print text to screen", 'hint_calc': "Calculator",
        'hint_clear': "Clear terminal screen", 'hint_time': "Current time",
        'hint_history': "Command history", 'hint_whoami': "Current username",
        'hint_ls': "List directory contents", 'hint_cd': "Change directory",
        'hint_pwd': "Print working directory", 'hint_mkdir': "Make directory",
        'hint_touch': "Create empty file", 'hint_cat': "Read file contents",
        'hint_rm': "Remove file/folder", 'hint_fmenu': "Graphical file menu",
        'hint_ping': "Test network connection", 'hint_ipconfig': "Network configuration",
        'hint_run': "Execute script file", 'hint_view': "View photo/video",
        'hint_refresh': "Refresh desktop interface", 'hint_color': "Change terminal color",
        'hint_gallery': "ASCII art gallery", 'hint_game': "Number guessing game",
        'hint_tictactoe': "Tic-Tac-Toe game", 'hint_stopwatch': "Stopwatch utility"
    },
    'fr': {
        'os_name': "EXP",
        'welcome': "Bon retour, {name}!",
        'shutdown': "Arrêt de {os_name}...",
        'restarting': "Redémarrage de {os_name}...",
        'not_found': "Erreur: commande '{cmd}' introuvable.",
        'avail_cmd': "Référence des commandes:",
        'boot_init': "Initialisation du matériel...",
        'boot_kernel': "Chargement du noyau...",
        'boot_fs': "Montage du système de fichiers...",
        'boot_session': "Démarrage de la session...",
        'boot_ready': "Système prêt!                   ",
        'menu_title': "--- Menu Principal ---",
        'menu_prompt': "Menu > ",
        'menu_help': "Options: 'settings', 'restart', 'shutdown', 'back'",
        'set_title': "--- Paramètres ---",
        'set_prompt': "Paramètres > ",
        'set_help': "Options: 'sysinfo', 'lang', 'datetime', 'color', 'back'",
        'lang_choose': "Disponible: ru_ru, ru_by, en, fr, nl.\nChoisissez: ",
        'lang_set': "Langue modifiée avec succès.",
        'sys_info_title': "--- Info Système ---",
        'file_created': "Créé '{file}'.",
        'file_deleted': "Supprimé '{file}'.",
        'deploy_sys': ">>> Déploiement du Système <<<",
        'enter_user': "Nom d'utilisateur: ",
        'boot_title': "{os_name} Noyau v.{version}",
        'loading': "Chargement: [{bar}] {pct}% | {status}",
        'gallery_title': "--- Galerie ---",
        'gallery_prompt': "Nom de l'image (ou 'exit'): ",
        'fmenu_title': "--- Menu Fichier ---",
        'fmenu_opts': "1.Créer 2.Supprimer 3.Copier 4.Couper 5.Coller 8.Importer 0.Quitter",
        'fmenu_prompt': "fmenu > ",
        'dt_title': "--- Date et Heure ---",
        'dt_menu': "1. Décalage horaire\n2. Décalage en secondes\n3. Retour",
        'dt_prompt': "Sélection > ",
        'sys_build': "Build  : {version}",
        'sys_user': "Utilisateur : {user}",
        'sys_plat': "Plateforme  : {platform}",
        'game_welcome': "Devinez (1-100). 'exit' pour quitter.",
        'game_high': "Plus haut ↑", 'game_low': "Plus bas ↓", 'game_win': "Correct!",
        'err_disk': "Erreur d'accès: {err}",
        'ping_sim': "Ping vers {ip}:",
        'ping_reply': "Réponse de {ip}: temps={time}ms",
        'ping_timeout': "Délai d'attente dépassé.",
        'color_set': "Couleur changée en {color}",
        'script_err': "Erreur de script: {err}",
        'media_open': "Ouverture du fichier {file}...",
        'media_err': "Format non supporté ou fichier introuvable.",
        'refresh_msg': "Bureau rafraîchi.",
        'help_notice': "Si vous ne savez pas ce que signifie une commande, tapez 'help' pour en savoir plus sur les commandes.",

        'hint_help': "Aide des commandes", 'hint_menu': "Menu principal",
        'hint_echo': "Afficher du texte", 'hint_calc': "Calculatrice",
        'hint_clear': "Effacer l'écran", 'hint_time': "Heure actuelle",
        'hint_history': "Historique des commandes", 'hint_whoami': "Utilisateur actuel",
        'hint_ls': "Lister les fichiers", 'hint_cd': "Changer de dossier",
        'hint_pwd': "Dossier actuel", 'hint_mkdir': "Créer un dossier",
        'hint_touch': "Créer un fichier vide", 'hint_cat': "Lire un fichier",
        'hint_rm': "Supprimer un fichier", 'hint_fmenu': "Menu fichier graphique",
        'hint_ping': "Test réseau", 'hint_ipconfig': "Configuration réseau",
        'hint_run': "Exécuter un script", 'hint_view': "Voir photo/vidéo",
        'hint_refresh': "Rafraîchir l'interface", 'hint_color': "Changer la couleur",
        'hint_gallery': "Galerie ASCII", 'hint_game': "Jeu de devinette",
        'hint_tictactoe': "Jeu Morpion", 'hint_stopwatch': "Chronomètre"
    },
    'nl': {
        'os_name': "EXP",
        'welcome': "Welkom terug, {name}!",
        'shutdown': "{os_name} afsluiten...",
        'restarting': "{os_name} herstarten...",
        'not_found': "Fout: commando '{cmd}' niet gevonden.",
        'avail_cmd': "Commando Referentie:",
        'boot_init': "Hardware initialiseren...",
        'boot_kernel': "Kernel laden...",
        'boot_fs': "Bestandssysteem koppelen...",
        'boot_session': "Sessie starten...",
        'boot_ready': "Systeem klaar!                  ",
        'menu_title': "--- Hoofdmenu ---",
        'menu_prompt': "Menu > ",
        'menu_help': "Opties: 'settings', 'restart', 'shutdown', 'back'",
        'set_title': "--- Instellingen ---",
        'set_prompt': "Instellingen > ",
        'set_help': "Opties: 'sysinfo', 'lang', 'datetime', 'color', 'back'",
        'lang_choose': "Beschikbaar: ru_ru, ru_by, en, fr, nl.\nKies: ",
        'lang_set': "Taal succesvol gewijzigd.",
        'sys_info_title': "--- Systeeminfo ---",
        'file_created': "'{file}' aangemaakt.",
        'file_deleted': "'{file}' verwijderd.",
        'deploy_sys': ">>> Systeem Implementatie <<<",
        'enter_user': "Gebruikersnaam: ",
        'boot_title': "{os_name} Kernel v.{version}",
        'loading': "Laden: [{bar}] {pct}% | {status}",
        'gallery_title': "--- Galerij ---",
        'gallery_prompt': "Afbeeldingsnaam (of 'exit'): ",
        'fmenu_title': "--- Bestandsmenu ---",
        'fmenu_opts': "1.Maken 2.Verwijderen 3.Kopiëren 4.Knippen 5.Plakken 8.Importeren 0.Afsluiten",
        'fmenu_prompt': "fmenu > ",
        'dt_title': "--- Datum en Tijd ---",
        'dt_menu': "1. Tijdzone aanpassen\n2. Seconden aanpassen\n3. Terug",
        'dt_prompt': "Selecteer > ",
        'sys_build': "Build  : {version}",
        'sys_user': "Gebruiker: {user}",
        'sys_plat': "Platform : {platform}",
        'game_welcome': "Raad (1-100). 'exit' om te stoppen.",
        'game_high': "Hoger ↑", 'game_low': "Lager ↓", 'game_win': "Correct!",
        'err_disk': "Toegangsfout: {err}",
        'ping_sim': "Pingen naar {ip}:",
        'ping_reply': "Antwoord van {ip}: tijd={time}ms",
        'ping_timeout': "Time-out van verzoek.",
        'color_set': "Kleurschema ingesteld op {color}",
        'script_err': "Scriptfout: {err}",
        'media_open': "Mediabestand {file} openen...",
        'media_err': "Niet-ondersteund formaat of bestand niet gevonden.",
        'refresh_msg': "Bureaublad vernieuwd.",
        'help_notice': "Als u niet weet wat een commando betekent, typ dan 'help' om meer te leren over de commando's.",

        'hint_help': "Commando referentie", 'hint_menu': "Hoofdsysteemmenu",
        'hint_echo': "Tekst afdrukken", 'hint_calc': "Rekenmachine",
        'hint_clear': "Scherm wissen", 'hint_time': "Huidige tijd",
        'hint_history': "Commando geschiedenis", 'hint_whoami': "Huidige gebruiker",
        'hint_ls': "Bestanden weergeven", 'hint_cd': "Map wijzigen",
        'hint_pwd': "Huidige map", 'hint_mkdir': "Map maken",
        'hint_touch': "Leeg bestand maken", 'hint_cat': "Bestand lezen",
        'hint_rm': "Bestand/map verwijderen", 'hint_fmenu': "Grafisch bestandsmenu",
        'hint_ping': "Netwerk testen", 'hint_ipconfig': "Netwerkconfiguratie",
        'hint_run': "Script uitvoeren", 'hint_view': "Foto/video bekijken",
        'hint_refresh': "Interface vernieuwen", 'hint_color': "Kleur wijzigen",
        'hint_gallery': "ASCII galerij", 'hint_game': "Raadspel",
        'hint_tictactoe': "Boter-kaas-en-eieren", 'hint_stopwatch': "Stopwatch"
    }
}


# =============================================================================
# ЯДРО И СИСТЕМА
# =============================================================================

class EXPOS:
    def __init__(self):
        self.running = True
        self.is_restarting = False
        self.version = "alpha 0.0.3 Build 19"
        self.username = "User"
        self.lang = "ru_ru"
        self.ui_color = "white"

        self.config_file = ".expos_config"
        self.history_file = ".expos_history"
        self.trash_dir = ".expos_trash"
        self.start_dir = py_os.getcwd()

        self.history = []
        self.tz_offset_hours = 0
        self.time_offset_seconds = 0
        self.clipboard = None

        self.commands = {
            'help': (self.cmd_help, 'hint_help'), 'menu': (self.cmd_menu, 'hint_menu'),
            'echo': (self.cmd_echo, 'hint_echo'), 'calc': (self.cmd_calc, 'hint_calc'),
            'clear': (self.cmd_clear, 'hint_clear'), 'time': (self.cmd_time, 'hint_time'),
            'history': (self.cmd_history, 'hint_history'), 'whoami': (self.cmd_whoami, 'hint_whoami'),

            'ls': (self.cmd_ls, 'hint_ls'), 'cd': (self.cmd_cd, 'hint_cd'),
            'pwd': (self.cmd_pwd, 'hint_pwd'), 'mkdir': (self.cmd_mkdir, 'hint_mkdir'),
            'touch': (self.cmd_touch, 'hint_touch'), 'cat': (self.cmd_cat, 'hint_cat'),
            'rm': (self.cmd_rm, 'hint_rm'), 'fmenu': (self.cmd_fmenu, 'hint_fmenu'),

            'ping': (self.cmd_ping, 'hint_ping'), 'ipconfig': (self.cmd_ipconfig, 'hint_ipconfig'),
            'run': (self.cmd_run, 'hint_run'),

            'view': (self.cmd_view, 'hint_view'), 'refresh': (self.cmd_refresh, 'hint_refresh'),
            'color': (self.cmd_color, 'hint_color'), 'gallery': (self.cmd_gallery, 'hint_gallery'),

            'game': (self.cmd_game, 'hint_game'), 'tictactoe': (self.cmd_tictactoe, 'hint_tictactoe'),
            'stopwatch': (self.cmd_stopwatch, 'hint_stopwatch')
        }

    def t(self, key, **kwargs):
        base = LANGUAGES.get(self.lang, LANGUAGES['en'])
        text = base.get(key, LANGUAGES['en'].get(key, key))
        return text.format(**kwargs) if kwargs else text

    def get_os_name(self):
        return self.t('os_name')

    def get_dynamic_logo(self):
        name = self.get_os_name()
        return f"""
       .-----------------------.
     .'                         '.
    /        {name:^11}          \\
   |      ( a0.0.3 Build 19 )      |
    \\                             /
     '.                         .'
       '-----------------------'
"""

    def get_current_time(self):
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours=self.tz_offset_hours,
                                                             seconds=self.time_offset_seconds)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

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
                    self.lang = config.get('lang', 'ru_ru')
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
        print(self.t('deploy_sys'))
        while True:
            name = input(self.t('enter_user')).strip()
            if name:
                self.username = name
                break
        self.lang = "ru_ru"
        self.save_config()

    def boot_sequence(self):
        self.cmd_clear("")
        print(COLORS.get(self.ui_color, ''))
        print(self.get_dynamic_logo())
        print(self.t('boot_title', os_name=self.get_os_name(), version=self.version) + "\n")

        for i in range(1, 101, 4):
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
            time.sleep(random.uniform(0.01, 0.03))
        print(f"\n\n{self.t('boot_ready')}")
        time.sleep(0.5)
        self.cmd_refresh("")

    def print_taskbar(self):
        width = 75
        print("=" * width)
        info = f" {self.get_current_time()} | {self.username} "
        os_n = self.get_os_name()
        print(f"| {os_n} {self.version} {info:>{width - len(os_n) - len(self.version) - 4}}|")
        print("=" * width)

    def print_desktop_grid(self):
        cmds = [c for c in sorted(self.commands.keys()) if c != 'menu']
        cols = 5
        print("\n" + "=" * 75)
        for i in range(0, len(cmds), cols):
            row = cmds[i:i + cols]
            print("  ".join([f"{cmd:<12}" for cmd in row]))

        # Меню в самом низу
        print(f"\n{'[' + 'menu' + ']':^75}")
        print("=" * 75)
        # Уведомление про help
        print(COLORS['cyan'] + self.t('help_notice') + COLORS.get(self.ui_color, COLORS['reset']))

    # --- Базовые Команды ---
    def cmd_help(self, args):
        print(COLORS['cyan'] + "\n" + self.t('help_notice') + COLORS.get(self.ui_color, COLORS['reset']))
        print(f"\n{self.t('avail_cmd')}")
        print("-" * 55)
        for cmd_name in sorted(self.commands.keys()):
            hint_key = self.commands[cmd_name][1]
            print(f"  {cmd_name:<12} | {self.t(hint_key)}")
        print("-" * 55)

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
            self.cmd_refresh("")  # Мгновенное обновление
        else:
            print(f"Colors: {', '.join(COLORS.keys())}")

    def cmd_refresh(self, args=""):
        self.cmd_clear("")
        self.print_taskbar()
        print(f"\n[{self.username} Dir: {py_os.getcwd()}]")
        self.cmd_ls("")
        self.print_desktop_grid()

    # --- Файловая Система ---
    def cmd_pwd(self, args):
        print(py_os.getcwd())

    def cmd_cd(self, args):
        if not args: args = self.start_dir
        try:
            py_os.chdir(args)
            self.cmd_refresh("")  # Обновляем "рабочий стол" при смене папки
        except Exception as e:
            print(self.t('err_disk', err=e))

    def cmd_ls(self, args):
        try:
            target = args if args else '.'
            items = py_os.listdir(target)
            filtered = [i for i in items if not i.startswith('.expos')]
            if not filtered: print("--- Пусто ---")
            for item in sorted(filtered):
                path = py_os.path.join(target, item)
                print(f"{'[DIR]' if py_os.path.isdir(path) else '[FILE]'} {item}")
        except Exception as e:
            print(self.t('err_disk', err=e))

    def cmd_mkdir(self, args):
        if args:
            try:
                py_os.makedirs(args, exist_ok=True)
                self.cmd_refresh("")  # Мгновенное обновление экрана
            except Exception as e:
                print(self.t('err_disk', err=e))

    def cmd_touch(self, args):
        if args:
            try:
                open(args, 'a').close()
                self.cmd_refresh("")  # Мгновенное обновление
            except Exception as e:
                print(self.t('err_disk', err=e))

    def cmd_cat(self, args):
        if args:
            try:
                with open(args, 'r', encoding='utf-8') as f:
                    print(f"\n{f.read()}\n")
            except Exception as e:
                print(self.t('err_disk', err=e))

    def cmd_rm(self, args):
        if not args: return
        try:
            shutil.move(args, py_os.path.join(self.trash_dir, f"{int(time.time())}_{args}"))
            self.cmd_refresh("")  # Мгновенное обновление
        except Exception as e:
            print(self.t('err_disk', err=e))

    def cmd_fmenu(self, args):
        changed = False
        while True:
            print(f"\n{self.t('fmenu_title')}\n{self.t('fmenu_opts')}")
            c = input(self.t('fmenu_prompt')).strip()
            if c == '0':
                break
            elif c == '1':
                self.cmd_touch(input("Name: "));
                changed = True
            elif c == '2':
                self.cmd_rm(input("Delete target: "));
                changed = True
            elif c == '3':
                src = input("Copy target: ")
                if py_os.path.exists(src): self.clipboard = ('copy', src); print("Copied.")
            elif c == '4':
                src = input("Cut target: ")
                if py_os.path.exists(src): self.clipboard = ('cut', src); print("Cut.")
            elif c == '5':
                if not self.clipboard:
                    print("Clipboard empty.")
                else:
                    action, src = self.clipboard
                    dest = input(f"Paste as (name): ")
                    try:
                        if action == 'copy':
                            shutil.copy(src, dest)
                        elif action == 'cut':
                            shutil.move(src, dest); self.clipboard = None
                        changed = True
                    except Exception as e:
                        print(f"Error: {e}")
            elif c == '8':
                path = input("Host system absolute path: ")
                try:
                    shutil.copy(path, '.')
                    changed = True
                except Exception as e:
                    print(f"Error: {e}")

        # Обновляем "рабочий стол" при выходе, если были изменения
        if changed: self.cmd_refresh("")

    # --- Мультимедиа ---
    def cmd_view(self, args):
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
        if not args: return
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
        print("\nIP Configuration")
        print(f"IPv4........ : 192.168.1.{random.randint(2, 254)}")
        print("Subnet Mask. : 255.255.255.0")
        print("Gateway..... : 192.168.1.1\n")

    # --- Меню и Настройки ---
    def run_sysinfo(self):
        self.cmd_clear("")
        print(COLORS.get(self.ui_color, ''))
        print(self.get_dynamic_logo())
        print(f"\n{self.t('sys_info_title')}")
        print(self.t('sys_build', version=self.version))
        print(self.t('sys_user', user=self.username))
        print(self.t('sys_plat', platform=platform.system()))
        print(f"Dir: {py_os.getcwd()}")
        try:
            t, u, f = shutil.disk_usage(".")
            print(f"Disk Total: {t // (2 ** 30)} GB | Free: {f // (2 ** 30)} GB")
        except:
            pass
        print("\n")

    def cmd_menu(self, args):
        while True:
            print(f"\n{self.t('menu_title')}\n{self.t('menu_help')}")
            c = input(self.t('menu_prompt')).lower().strip()
            if c in ['back']:
                self.cmd_refresh("")
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
            c = input(self.t('set_prompt')).lower().strip()
            if c in ['back']:
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
                cl = input(f"Color ({', '.join(COLORS.keys())}): ").strip().lower()
                self.cmd_color(cl)
            elif c == 'datetime':
                self.cmd_datetime_config()

    def cmd_datetime_config(self):
        while True:
            print(f"\n{self.t('dt_title')}")
            print(f"Current System Time: {self.get_current_time()}")
            print(self.t('dt_menu'))
            c = input(self.t('dt_prompt')).strip()
            if c == '3':
                break
            elif c == '1':
                try:
                    self.tz_offset_hours = int(input("Hours offset (e.g. -3, 2): "))
                    self.save_config()
                except:
                    pass
            elif c == '2':
                try:
                    self.time_offset_seconds = int(input("Seconds offset (e.g. 3600): "))
                    self.save_config()
                except:
                    pass

    # --- Утилиты и Игры ---
    def cmd_calc(self, args):
        if not args: return
        try:
            print(eval(args, {"__builtins__": None}, {}))
        except Exception as e:
            print(f"Error: {e}")

    def cmd_stopwatch(self, args):
        print("Stopwatch. Press Enter to start/stop.")
        input();
        start = time.time();
        print("Running...")
        input();
        print(f"Time: {round(time.time() - start, 2)}s")

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
        print("Tic-Tac-Toe")
        board = [' '] * 9

        def draw():
            print(
                f"\n {board[0]} | {board[1]} | {board[2]} \n---+---+---\n {board[3]} | {board[4]} | {board[5]} \n---+---+---\n {board[6]} | {board[7]} | {board[8]} \n")

        turn = 'X'
        for _ in range(9):
            draw()
            try:
                move = int(input(f"Move {turn} (1-9): ")) - 1
                if 0 <= move <= 8 and board[move] == ' ':
                    board[move] = turn
                    turn = 'O' if turn == 'X' else 'X'
            except:
                pass
        draw();
        print("Game Over!")

    # --- Жизненный цикл ---
    def execute_command(self, cmd_line):
        parts = cmd_line.split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''

        if cmd in self.commands:
            func = self.commands[cmd][0]
            func(args)
        else:
            print(self.t('not_found', cmd=cmd))

    def start(self):
        self.load_config()
        self.boot_sequence()
        print(self.t('welcome', name=self.username))

        if HAS_READLINE:
            def completer(text, state):
                options = [c for c in self.commands.keys() if c.startswith(text)]
                return options[state] if state < len(options) else None

            readline.set_completer(completer)
            readline.parse_and_bind("tab: complete")

        while self.running:
            try:
                color_code = COLORS.get(self.ui_color, COLORS['white'])
                prompt = f"\n{color_code}[{self.username}@{self.get_os_name().lower()}]$ {COLORS['reset']}"

                user_input = input(prompt).strip()
                if not user_input: continue

                self.history.append(user_input)
                print(color_code, end="")
                self.execute_command(user_input)
                print(COLORS['reset'], end="")

            except (KeyboardInterrupt, EOFError):
                self.running = False
            except Exception as e:
                print(f"\nTerminal Error: {e}")

        print(self.t('shutdown', os_name=self.get_os_name()))
        self.save_config()


if __name__ == "__main__":
    while True:
        os_inst = EXPOS()
        os_inst.start()
        if not os_inst.is_restarting: break
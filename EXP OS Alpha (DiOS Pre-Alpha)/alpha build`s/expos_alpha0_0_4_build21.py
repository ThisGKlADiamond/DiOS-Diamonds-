"""
EXP OS / ЕХП ОС
Version: alpha 0.0.4 Build 21
Description: Advanced terminal-based OS simulation with Multi-language support (RU_RU, RU_BY, EN, FR, NL).
Features: Virtual FS, Network Sim, Scripting, Games, Pipes, Aliases, Logging, Auth.
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
import shlex
import logging
import io

# --- Инициализация Логирования ---
logging.basicConfig(filename='.expos_log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
    'cyan': '\033[96m', 'white': '\033[97m',
    'dark': '\033[90m', 'light': '\033[97m'
}

PICS = {
    'cat': "\n       /\\_/\\ \n      ( o.o )\n       > ^ <\n",
    'computer': "\n       .---------------.\n      | .------------. |\n      | | OS 2026    | |\n      | | SYSTEM     | |\n      | '------------' |\n       '---------------'\n            |  |\n         _.-'  '-._\n        '----------'\n",
    'robot': "\n        [o_o]\n       /|___|\\\n        /   \\\n"
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
    'menu_help': "Опции: 'settings', 'update', 'restart', 'shutdown', 'back'",
    'set_title': "--- Настройки ---",
    'set_prompt': "Настройки > ",
    'set_help': "Опции: 'sysinfo', 'lang', 'datetime', 'color', 'password', 'back'",
    'lang_choose': "Доступно: ru_ru, ru_by, en, fr, nl.\nВыберите язык: ",
    'lang_set': "Язык успешно изменен.",
    'sys_info_title': "--- Информация о системе ---",
    'file_created': "Объект '{file}' создан.",
    'file_deleted': "Объект '{file}' удален.",
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
    'ping_sim': "Обмен пакетами с {ip} (size={size}):",
    'ping_reply': "Ответ от {ip}: время={time}мс",
    'ping_timeout': "Превышен интервал ожидания.",
    'color_set': "Цветовая схема изменена на {color}",
    'script_err': "Ошибка скрипта: {err}",
    'media_open': "Открытие файла {file}...",
    'media_err': "Формат не поддерживается или файл не найден.",
    'refresh_msg': "Рабочий стол обновлен.",
    'help_notice': "Если вы не знаете, что означает данная команда, то введите 'help <команда>' или 'man <команда>'.",
    'update_msg': "Проверка обновлений...\nУ вас установлена последняя версия ({version}). Обновлений пока нет.",
    'pass_ask': "Введите пароль для входа: ",
    'pass_set': "Новый пароль установлен. (Оставьте пустым для отключения)",

    # Подсказки
    'hint_help': "Справка по командам", 'hint_menu': "Главное системное меню",
    'hint_echo': "Вывод текста на экран", 'hint_calc': "Калькулятор",
    'hint_clear': "Очистка экрана", 'hint_time': "Текущее время",
    'hint_history': "История введенных команд", 'hint_whoami': "Имя текущего пользователя",
    'hint_ls': "Список файлов и папок", 'hint_cd': "Переход в другую папку",
    'hint_pwd': "Путь текущей папки", 'hint_mkdir': "Создать новую папку",
    'hint_touch': "Создать пустой файл", 'hint_cat': "Просмотр содержимого файла",
    'hint_rm': "Удаление (опции: -r, -i)", 'hint_fmenu': "Графическое файловое меню",
    'hint_ping': "Ping (опции: -c, -s)", 'hint_ipconfig': "Сетевые настройки",
    'hint_run': "Выполнение скрипта", 'hint_view': "Просмотр фото/видео/текста",
    'hint_refresh': "Обновление интерфейса", 'hint_color': "Смена цвета (dark/light)",
    'hint_gallery': "Галерея ASCII", 'hint_game': "Игра 'Угадай число'",
    'hint_tictactoe': "Игра 'Крестики-Нолики'", 'hint_stopwatch': "Утилита секундомера",
    'hint_mv': "Перемещение/Переименование", 'hint_cp': "Копирование файлов",
    'hint_find': "Поиск файлов", 'hint_chmod': "Изменение прав доступа",
    'hint_traceroute': "Трассировка маршрута", 'hint_wget': "Скачивание файлов",
    'hint_play': "Воспроизведение аудио", 'hint_top': "Список процессов",
    'hint_df': "Информация о дисках", 'hint_alias': "Создание псевдонимов",
    'hint_man': "Руководство по команде", 'hint_minesweeper': "Игра Сапер (Текст)"
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
        'hint_tictactoe': "Tic-Tac-Toe game", 'hint_stopwatch': "Stopwatch utility",
        'update_msg': "Checking for updates...\nYou are on the latest version ({version}). No updates yet.",
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
        'hint_tictactoe': "Jeu Morpion", 'hint_stopwatch': "Chronomètre",
        'update_msg': "Recherche de mises à jour...\nVersion à jour ({version}).",
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
        'hint_tictactoe': "Boter-kaas-en-eieren", 'hint_stopwatch': "Stopwatch",
        'update_msg': "Controleren op updates...\nJe hebt de nieuwste versie ({version}).",
    }
}


# =============================================================================
# ЯДРО И СИСТЕМА
# =============================================================================

class EXPOS:
    def __init__(self):
        self.running = True
        self.is_restarting = False
        self.version = "alpha 0.0.4 Build 22"
        self.username = "User"
        self.password = ""
        self.lang = "ru_ru"
        self.ui_color = "white"
        self.ps1 = "[{user}@{os}]$ "

        self.config_file = ".expos_config"
        self.history_file = ".expos_history"
        self.aliases_file = ".expos_aliases"
        self.trash_dir = ".expos_trash"
        self.start_dir = py_os.getcwd()

        self.history = []
        self.aliases = {}
        self.scores = {}
        self.tz_offset_hours = 0
        self.time_offset_seconds = 0
        self.clipboard = None

        # Перехват вывода для pipe
        self.pipe_buffer = None

        self.commands = {
            'help': (self.cmd_help, 'hint_help'), 'menu': (self.cmd_menu, 'hint_menu'),
            'echo': (self.cmd_echo, 'hint_echo'), 'calc': (self.cmd_calc, 'hint_calc'),
            'clear': (self.cmd_clear, 'hint_clear'), 'time': (self.cmd_time, 'hint_time'),
            'history': (self.cmd_history, 'hint_history'), 'whoami': (self.cmd_whoami, 'hint_whoami'),

            'ls': (self.cmd_ls, 'hint_ls'), 'cd': (self.cmd_cd, 'hint_cd'),
            'pwd': (self.cmd_pwd, 'hint_pwd'), 'mkdir': (self.cmd_mkdir, 'hint_mkdir'),
            'touch': (self.cmd_touch, 'hint_touch'), 'cat': (self.cmd_cat, 'hint_cat'),
            'rm': (self.cmd_rm, 'hint_rm'), 'fmenu': (self.cmd_fmenu, 'hint_fmenu'),
            'mv': (self.cmd_mv, 'hint_mv'), 'cp': (self.cmd_cp, 'hint_cp'),
            'find': (self.cmd_find, 'hint_find'), 'chmod': (self.cmd_chmod, 'hint_chmod'),

            'ping': (self.cmd_ping, 'hint_ping'), 'ipconfig': (self.cmd_ipconfig, 'hint_ipconfig'),
            'traceroute': (self.cmd_traceroute, 'hint_traceroute'), 'wget': (self.cmd_wget, 'hint_wget'),
            'run': (self.cmd_run, 'hint_run'),

            'view': (self.cmd_view, 'hint_view'), 'play': (self.cmd_play, 'hint_play'),
            'refresh': (self.cmd_refresh, 'hint_refresh'), 'color': (self.cmd_color, 'hint_color'),
            'gallery': (self.cmd_gallery, 'hint_gallery'),

            'game': (self.cmd_game, 'hint_game'), 'tictactoe': (self.cmd_tictactoe, 'hint_tictactoe'),
            'minesweeper': (self.cmd_minesweeper, 'hint_minesweeper'),

            'stopwatch': (self.cmd_stopwatch, 'hint_stopwatch'), 'top': (self.cmd_top, 'hint_top'),
            'df': (self.cmd_df, 'hint_df'), 'alias': (self.cmd_alias, 'hint_alias'),
            'man': (self.cmd_help, 'hint_man')  # man - синоним help
        }

    def t(self, key, **kwargs):
        base = LANGUAGES.get(self.lang, LANGUAGES['en'])
        text = base.get(key, LANGUAGES['en'].get(key, key))
        return text.format(**kwargs) if kwargs else text

    def get_os_name(self):
        return self.t('os_name')

    def out(self, text, end="\n"):
        """Кастомный вывод для поддержки конвейеров (pipes)"""
        if self.pipe_buffer is not None:
            self.pipe_buffer.write(str(text) + end)
        else:
            print(text, end=end)

    def parse_args(self, args_str):
        try:
            return shlex.split(args_str)
        except:
            return args_str.split()

    def get_dynamic_logo(self):
        name = self.get_os_name()
        logo_art = random.choice(list(PICS.values()))
        return f"\n{name} Kernel [a0.0.4 B21]\n" + logo_art

    def get_current_time(self):
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours=self.tz_offset_hours,
                                                             seconds=self.time_offset_seconds)
        return dt.strftime("%H:%M")

    def load_config(self):
        try:
            py_os.makedirs(self.trash_dir, exist_ok=True)
        except:
            pass
        if py_os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    c = json.load(f)
                    self.username = c.get('username', 'User')
                    self.lang = c.get('lang', 'ru_ru')
                    self.tz_offset_hours = c.get('tz_hours', 0)
                    self.time_offset_seconds = c.get('t_secs', 0)
                    self.ui_color = c.get('color', 'white')
                    self.password = c.get('password', '')
                    self.ps1 = c.get('ps1', '[{user}@{os}]$ ')
            except Exception as e:
                logging.error(f"Config load error: {e}")
        else:
            self.run_installation()

        if py_os.path.exists(self.aliases_file):
            try:
                with open(self.aliases_file, 'r') as f:
                    self.aliases = json.load(f)
            except:
                pass

        if py_os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = [line.strip() for line in f.readlines()]
            except:
                pass

    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'username': self.username, 'lang': self.lang, 'tz_hours': self.tz_offset_hours,
                           't_secs': self.time_offset_seconds, 'color': self.ui_color,
                           'password': self.password, 'ps1': self.ps1}, f)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                for item in self.history[-100:]: f.write(f"{item}\n")
            with open(self.aliases_file, 'w') as f:
                json.dump(self.aliases, f)
        except Exception as e:
            logging.error(f"Save error: {e}")

    def run_installation(self):
        self.cmd_clear("")
        print(self.t('deploy_sys'))
        while True:
            name = input(self.t('enter_user')).strip()
            if name:
                self.username = name;
                break
        self.save_config()

    def boot_sequence(self):
        self.cmd_clear("")
        print(COLORS.get(self.ui_color, ''))
        print(self.get_dynamic_logo())

        # Safe mode check
        if '--safe' in sys.argv:
            print("[!] SAFE MODE ACTIVE")
        else:
            for i in range(1, 101, 7):
                blocks = int((i / 100) * 30)
                bar = '#' * blocks + '-' * (30 - blocks)
                status = self.t('boot_session') if i > 70 else self.t('boot_kernel')
                sys.stdout.write(f"\r" + self.t('loading', bar=bar, pct=i, status=status))
                sys.stdout.flush()
                time.sleep(random.uniform(0.01, 0.04))
            print(f"\n\n{self.t('boot_ready')}")
            time.sleep(0.5)

        if self.password:
            attempts = 3
            while attempts > 0:
                p = input(self.t('pass_ask'))
                if p == self.password: break
                attempts -= 1
                print("Access Denied.")
            if attempts == 0: sys.exit()

        self.cmd_refresh("")

    def print_taskbar(self):
        width = 75
        print("=" * width)
        # Имитация батареи и CPU
        cpu = random.randint(2, 45)
        bat = random.randint(10, 100)
        info = f" {self.get_current_time()} | CPU: {cpu}% | BAT: {bat}% | {self.username} "
        os_n = self.get_os_name()
        print(f"| {os_n} {self.version} {info:>{width - len(os_n) - len(self.version) - 4}}|")
        print("=" * width)

    def print_desktop_grid(self):
        cmds = [c for c in sorted(self.commands.keys()) if c not in ('menu', 'man')]
        cols = 5
        print("\n" + "=" * 75)
        for i in range(0, len(cmds), cols):
            row = cmds[i:i + cols]
            print("  ".join([f"{cmd:<13}" for cmd in row]))

        print(f"\n{'[' + 'menu' + ']':^75}")
        print("=" * 75)
        print(COLORS['cyan'] + self.t('help_notice') + COLORS.get(self.ui_color, COLORS['reset']))

    # --- Базовые Команды ---
    def cmd_help(self, args):
        parsed = self.parse_args(args)
        if parsed and parsed[0] in self.commands:
            cmd = parsed[0]
            print(f"\n[MANUAL] {cmd} - {self.t(self.commands[cmd][1])}")
            return

        print(COLORS['cyan'] + "\n" + self.t('help_notice') + COLORS.get(self.ui_color, COLORS['reset']))
        print(f"\n{self.t('avail_cmd')}")
        print("-" * 55)
        for cmd_name in sorted(self.commands.keys()):
            self.out(f"  {cmd_name:<13} | {self.t(self.commands[cmd_name][1])}")
        print("-" * 55)

    def cmd_echo(self, args):
        self.out(args)

    def cmd_time(self, args):
        self.out(self.get_current_time())

    def cmd_whoami(self, args):
        self.out(self.username)

    def cmd_clear(self, args):
        py_os.system('cls' if platform.system() == "Windows" else 'clear')

    def cmd_history(self, args):
        for i, cmd in enumerate(self.history[-20:], 1): self.out(f"{i:3}: {cmd}")

    def cmd_color(self, args):
        a = args.strip().lower()
        if a in COLORS:
            self.ui_color = a;
            self.save_config();
            self.cmd_refresh("")
        else:
            self.out(f"Colors: {', '.join(COLORS.keys())}")

    def cmd_refresh(self, args=""):
        self.cmd_clear("")
        self.print_taskbar()
        print(f"\n[{self.username} Dir: {py_os.getcwd()}]")
        self.cmd_ls("")
        self.print_desktop_grid()

    # --- Файловая Система ---
    def clean_trash(self):
        # Автоочистка корзины если > 50MB
        try:
            size = sum(py_os.path.getsize(py_os.path.join(self.trash_dir, f)) for f in py_os.listdir(self.trash_dir) if
                       py_os.path.isfile(py_os.path.join(self.trash_dir, f)))
            if size > 50 * 1024 * 1024:
                shutil.rmtree(self.trash_dir)
                py_os.makedirs(self.trash_dir)
        except Exception as e:
            logging.error(e)

    def cmd_pwd(self, args):
        self.out(py_os.getcwd())

    def cmd_cd(self, args):
        p = self.parse_args(args)
        path = p[0] if p else self.start_dir
        try:
            py_os.chdir(path); self.cmd_refresh("")
        except Exception as e:
            self.out(self.t('err_disk', err=e))

    def cmd_ls(self, args):
        p = self.parse_args(args)
        target = p[0] if p else '.'
        try:
            items = py_os.listdir(target)
            filtered = [i for i in items if not i.startswith('.expos')]
            if not filtered: self.out("--- Пусто ---")
            for item in sorted(filtered):
                path = py_os.path.join(target, item)
                self.out(f"{'[DIR]' if py_os.path.isdir(path) else '[FILE]'} {item}")
        except Exception as e:
            self.out(self.t('err_disk', err=e))

    def cmd_mkdir(self, args):
        p = self.parse_args(args)
        if p:
            try:
                py_os.makedirs(p[0], exist_ok=True); self.cmd_refresh("")
            except Exception as e:
                self.out(self.t('err_disk', err=e))

    def cmd_touch(self, args):
        p = self.parse_args(args)
        if p:
            try:
                open(p[0], 'a').close(); self.cmd_refresh("")
            except Exception as e:
                self.out(self.t('err_disk', err=e))

    def cmd_cat(self, args):
        p = self.parse_args(args)
        if p:
            try:
                with open(p[0], 'r', encoding='utf-8') as f:
                    self.out(f"\n{f.read()}\n")
            except Exception as e:
                self.out(self.t('err_disk', err=e))

    def cmd_rm(self, args):
        p = self.parse_args(args)
        if not p: return
        interactive = '-i' in p
        recursive = '-r' in p
        target = p[-1]  # Предполагаем путь в конце

        if interactive:
            if input(f"Remove {target}? (y/n): ").lower() != 'y': return

        try:
            dest = py_os.path.join(self.trash_dir, f"{int(time.time())}_{py_os.path.basename(target)}")
            if recursive and py_os.path.isdir(target):
                shutil.move(target, dest)
            else:
                shutil.move(target, dest)
            self.clean_trash()
            self.cmd_refresh("")
        except Exception as e:
            self.out(self.t('err_disk', err=e))

    def cmd_cp(self, args):
        p = self.parse_args(args)
        if len(p) >= 2:
            try:
                shutil.copy(p[0], p[1]); self.cmd_refresh("")
            except Exception as e:
                self.out(self.t('err_disk', err=e))

    def cmd_mv(self, args):
        p = self.parse_args(args)
        if len(p) >= 2:
            try:
                shutil.move(p[0], p[1]); self.cmd_refresh("")
            except Exception as e:
                self.out(self.t('err_disk', err=e))

    def cmd_find(self, args):
        p = self.parse_args(args)
        if not p: return
        q = p[0]
        for root, dirs, files in py_os.walk('.'):
            for name in files:
                if q in name: self.out(py_os.path.join(root, name))

    def cmd_chmod(self, args):
        self.out("Permissions updated (Simulation only).")

    def cmd_fmenu(self, args):
        changed = False
        while True:
            print(f"\n{self.t('fmenu_title')}\n{self.t('fmenu_opts')}")
            c = input(self.t('fmenu_prompt')).strip()
            if c == '0':
                break
            elif c == '1':
                self.cmd_touch(input("Name: ")); changed = True
            elif c == '2':
                self.cmd_rm(input("Delete target: ")); changed = True
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
        if changed: self.cmd_refresh("")

    # --- Мультимедиа ---
    def cmd_view(self, args):
        p = self.parse_args(args)
        if not p: return self.out(self.t('media_err'))
        args = p[0]
        ext = args.lower().split('.')[-1]
        if ext in ['txt', 'log', 'exp'] and py_os.path.exists(args):
            with open(args, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i in range(0, len(lines), 20):
                    self.out("".join(lines[i:i + 20]))
                    if i + 20 < len(lines): input("-- Press Enter for more --")
        elif ext in ['png', 'jpg', 'mp4'] and py_os.path.exists(args):
            try:
                if platform.system() == 'Windows':
                    py_os.startfile(args)
                elif platform.system() == 'Darwin':
                    subprocess.call(('open', args))
                else:
                    subprocess.call(('xdg-open', args))
            except Exception as e:
                self.out(self.t('err_disk', err=e))
        else:
            self.out(self.t('media_err'))

    def cmd_gallery(self, args):
        print(f"\n{self.t('gallery_title')}")
        arts = list(PICS.keys())
        if py_os.path.exists('gallery'):
            arts += [f for f in py_os.listdir('gallery') if f.endswith('.txt')]
        for name in arts: print(f"- {name}")

        c = input(self.t('gallery_prompt')).strip()
        if c in PICS:
            print(PICS[c])
        elif py_os.path.exists(f"gallery/{c}"):
            with open(f"gallery/{c}", 'r') as f:
                print(f.read())

    def cmd_play(self, args):
        p = self.parse_args(args)
        if not p: return
        self.out(f"Playing {p[0]}...")
        for _ in range(15):
            bars = " ".join("|" * random.randint(1, 8) for _ in range(10))
            sys.stdout.write(f"\r[AUDIO] {bars:<80}")
            sys.stdout.flush()
            time.sleep(0.1)
        print("\nPlayback finished.")

    # --- Сеть и Скрипты ---
    def cmd_run(self, args):
        p = self.parse_args(args)
        if not p: return
        script = p[0]
        script_args = p[1:]
        try:
            with open(script, 'r', encoding='utf-8') as f:
                for line in f:
                    cmd = line.strip()
                    if cmd and not cmd.startswith('#'):
                        # Замена аргументов $1, $2
                        for i, a in enumerate(script_args, 1): cmd = cmd.replace(f"${i}", a)
                        print(f"{COLORS['yellow']}> {cmd}{COLORS[self.ui_color]}")
                        self.execute_command(cmd)
                        time.sleep(0.2)
        except Exception as e:
            self.out(self.t('script_err', err=e))

    def cmd_ping(self, args):
        p = self.parse_args(args)
        ip = "127.0.0.1"
        count = 4
        size = 32

        if '-c' in p: count = int(p[p.index('-c') + 1])
        if '-s' in p: size = int(p[p.index('-s') + 1])
        for arg in p:
            if not arg.startswith('-') and arg not in str(count) and arg not in str(size): ip = arg

        self.out(self.t('ping_sim', ip=ip, size=size))
        for _ in range(count):
            time.sleep(0.5)
            if random.random() > 0.05:
                self.out(self.t('ping_reply', ip=ip, time=random.randint(10, 80)))
            else:
                self.out(self.t('ping_timeout'))

    def cmd_traceroute(self, args):
        ip = args if args else "1.1.1.1"
        self.out(f"Tracing route to {ip} over a maximum of 30 hops:\n")
        for i in range(1, random.randint(4, 9)):
            time.sleep(0.4)
            self.out(f" {i:2d}    {random.randint(10, 50)} ms   10.1.{i}.{random.randint(1, 254)}")
        self.out(f" Trace complete.")

    def cmd_wget(self, args):
        p = self.parse_args(args)
        if not p: return
        url = p[0]
        fname = url.split('/')[-1] or "downloaded_file"
        self.out(f"Resolving {url}... done.")
        self.out(f"Connecting to {url}... connected.")
        for i in range(1, 101, 10):
            sys.stdout.write(f"\r[{'#' * (i // 5):<20}] {i}%")
            sys.stdout.flush()
            time.sleep(0.1)
        print()
        open(fname, 'a').close()
        self.out(f"Saved '{fname}'.")

    def cmd_ipconfig(self, args):
        self.out("\nIP Configuration")
        self.out(f"IPv4........ : 192.168.1.{random.randint(2, 254)}")
        self.out("Subnet Mask. : 255.255.255.0")
        self.out("Gateway..... : 192.168.1.1\n")

    # --- Утилиты ---
    def cmd_top(self, args):
        self.out("PID   USER     PR  NI    VIRT    RES  %CPU %MEM  COMMAND")
        self.out(f"1     root     20   0    200M    50M   0.5  0.1  kernel_init")
        self.out(f"42    {self.username:<8} 20   0    150M    40M  12.0  2.5  ui_shell")
        self.out(f"89    {self.username:<8} 20   0     50M    10M   0.0  0.1  cron_sim")

    def cmd_df(self, args):
        try:
            t, u, f = shutil.disk_usage(".")
            gb = 2 ** 30
            self.out("Filesystem      Size  Used Avail Use% Mounted on")
            self.out(f"/dev/vda1       {t / gb:.1f}G  {u / gb:.1f}G  {f / gb:.1f}G  {int(u / t * 100)}% /")
        except:
            self.out("Disk info unavailable.")

    def cmd_alias(self, args):
        if not args:
            for k, v in self.aliases.items(): self.out(f"alias {k}='{v}'")
        else:
            if '=' in args:
                k, v = args.split('=', 1)
                self.aliases[k.strip()] = v.strip().strip("'\"")
                self.save_config()

    # --- Меню и Настройки ---
    def cmd_menu(self, args):
        while True:
            print(f"\n{self.t('menu_title')}\n{self.t('menu_help')}")
            c = input(self.t('menu_prompt')).lower().strip()
            if c in ['back']:
                self.cmd_refresh(""); break
            elif c == 'settings':
                self.cmd_settings()
            elif c == 'update':
                print(self.t('update_msg', version=self.version))
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
            elif c == 'password':
                self.password = input("New password: ")
                self.save_config();
                print(self.t('pass_set'))

    def run_sysinfo(self):
        self.cmd_clear("")
        print(COLORS.get(self.ui_color, ''))
        print(self.get_dynamic_logo())
        print(f"\n{self.t('sys_info_title')}")
        print(self.t('sys_build', version=self.version))
        print(self.t('sys_user', user=self.username))
        print(self.t('sys_plat', platform=platform.system()))
        print("\n")

    def cmd_datetime_config(self):
        while True:
            print(f"\n{self.t('dt_title')}")
            print(f"Time: {self.get_current_time()}")
            print(self.t('dt_menu'))
            c = input(self.t('dt_prompt')).strip()
            if c == '3':
                break
            elif c == '1':
                try:
                    self.tz_offset_hours = int(input("Hours offset: ")); self.save_config()
                except:
                    pass
            elif c == '2':
                try:
                    self.time_offset_seconds = int(input("Seconds offset: ")); self.save_config()
                except:
                    pass

    # --- Игры ---
    def cmd_calc(self, args):
        if not args: return
        try:
            self.out(eval(args, {"__builtins__": None}, {}))
        except Exception as e:
            self.out(f"Error: {e}")

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
        tries = 0
        while True:
            i = input("> ");
            if i == 'exit': break
            if not i.isdigit(): continue
            g = int(i);
            tries += 1
            if g < n:
                print(self.t('game_high'))
            elif g > n:
                print(self.t('game_low'))
            else:
                print(self.t('game_win'))
                print(f"Tries: {tries}")
                break

    def cmd_tictactoe(self, args):
        print("Tic-Tac-Toe (You vs AI)")
        board = [' '] * 9

        def draw():
            print(
                f"\n {board[0]} | {board[1]} | {board[2]} \n---+---+---\n {board[3]} | {board[4]} | {board[5]} \n---+---+---\n {board[6]} | {board[7]} | {board[8]} \n")

        def check_win(b, mark):
            wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
            return any(b[i] == b[j] == b[k] == mark for i, j, k in wins)

        for step in range(9):
            draw()
            if step % 2 == 0:
                try:
                    move = int(input(f"Move X (1-9): ")) - 1
                    if 0 <= move <= 8 and board[move] == ' ':
                        board[move] = 'X'
                    else:
                        continue
                except:
                    continue
            else:
                empty = [i for i, v in enumerate(board) if v == ' ']
                board[random.choice(empty)] = 'O'
                print("AI plays 'O'")

            if check_win(board, 'X'): draw(); print("You Win!"); return
            if check_win(board, 'O'): draw(); print("AI Wins!"); return

        draw();
        print("Draw!")

    def cmd_minesweeper(self, args):
        # Очень базовая симуляция
        print("Minesweeper (Lite CLI Version)")
        field = ['?'] * 10
        bomb = random.randint(0, 9)
        while True:
            print(" ".join(field))
            try:
                c = int(input("Dig (1-10) or 0 to exit: ")) - 1
                if c == -1: break
                if c == bomb:
                    print("BOOM! Game Over."); break
                else:
                    field[c] = '_'
                if field.count('?') == 1: print("You win!"); break
            except:
                pass

    # --- Жизненный цикл ---
    def execute_command(self, cmd_line):
        if not cmd_line: return

        # Поддержка простого пайпа: cmd | grep word
        pipe_cmd = None
        if '|' in cmd_line:
            parts = cmd_line.split('|', 1)
            cmd_line = parts[0].strip()
            pipe_cmd = parts[1].strip()
            self.pipe_buffer = io.StringIO()

        parts = self.parse_args(cmd_line)
        cmd = parts[0].lower()

        # Раскрытие alias
        if cmd in self.aliases:
            full_alias = self.aliases[cmd] + " " + " ".join(parts[1:])
            parts = self.parse_args(full_alias)
            cmd = parts[0].lower()

        args = cmd_line[len(parts[0]):].strip()  # Оригинальная строка аргументов для сложных команд

        try:
            if cmd in self.commands:
                func = self.commands[cmd][0]
                func(args)
            else:
                self.out(self.t('not_found', cmd=cmd))
        except Exception as e:
            logging.error(f"Cmd error '{cmd}': {e}")
            self.out(f"Internal Error: {e}")

        # Обработка пайпа (grep симуляция)
        if pipe_cmd and self.pipe_buffer:
            output = self.pipe_buffer.getvalue()
            self.pipe_buffer.close()
            self.pipe_buffer = None

            p_parts = self.parse_args(pipe_cmd)
            if p_parts[0] == 'grep' and len(p_parts) > 1:
                keyword = p_parts[1]
                for line in output.split('\n'):
                    if keyword in line: print(line)
            else:
                print(output)

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
                prompt_str = self.ps1.format(user=self.username, os=self.get_os_name().lower())
                prompt = f"\n{color_code}{prompt_str}{COLORS['reset']}"

                user_input = input(prompt).strip()
                if not user_input: continue

                self.history.append(user_input)
                self.save_config()  # Автосохранение

                print(color_code, end="")
                self.execute_command(user_input)
                print(COLORS['reset'], end="")

            except (KeyboardInterrupt, EOFError):
                self.running = False
            except Exception as e:
                logging.error(f"Terminal crash: {e}")
                print(f"\nTerminal Error: {e}")

        print(self.t('shutdown', os_name=self.get_os_name()))
        self.save_config()


if __name__ == "__main__":
    while True:
        os_inst = EXPOS()
        os_inst.start()
        if not os_inst.is_restarting: break
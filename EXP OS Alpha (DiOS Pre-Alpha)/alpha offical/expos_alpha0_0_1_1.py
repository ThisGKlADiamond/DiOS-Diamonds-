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

# Словарь переводов системы
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

        # Загрузочные сообщения
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
        'set_help': "Available options: 'sysinfo' (System Info), 'lang' (Change Language), 'back' (Exit settings)",

        'lang_choose': "Available languages: en (English), fr (Français), nl (Nederlands).\nChoose language: ",
        'lang_set': "Language successfully set to English.",

        'desc_help': "Show this help",
        'desc_echo': "Print the given text",
        'desc_calc': "Calculate a simple expression (+, -, *, /, //, %, **)",
        'desc_clear': "Clear the screen",
        'desc_time': "Show current date and time",
        'desc_history': "Show the history of entered commands",
        'desc_ls': "List files and directories in the current folder",
        'desc_game': "Play a number guessing game",
        'desc_touch': "Create a new empty file (e.g., touch file.txt)",
        'desc_cat': "Read and print file content (e.g., cat file.txt)",

        'sys_info_title': "--- System Information ---",
        'sys_storage': "--- Storage & Memory ---",
        'sys_unavailable': "Unavailable",
        'sys_ram_req': "Not available (Requires 'psutil')",
        'file_err': "Please specify a file name.",
        'file_not_found': "Error: File '{file}' not found or is a directory.",
        'file_created': "File '{file}' created successfully.",
        'file_read_err': "Error processing file: {error}"
    },
    'fr': {
        'welcome': "Bon retour, {name}! Tapez 'help' pour la liste des commandes.",
        'started': "EXP OS {version} a démarré.",
        'shutdown': "Fermeture de EXP OS...",
        'restarting': "Redémarrage de EXP OS...",
        'not_found': "Erreur: commande '{cmd}' introuvable.",
        'avail_cmd': "Commandes disponibles:",
        'no_help': "Aucune aide disponible pour la commande '{cmd}'.",
        'hist_empty': "L'historique est vide.",
        'dir_empty': "Le répertoire est vide.",

        'boot_init': "Initialisation de l'interface matérielle...",
        'boot_kernel': "Chargement du noyau du système...",
        'boot_fs': "Montage du système de fichiers virtuel...",
        'boot_session': "Démarrage de la session utilisateur...",
        'boot_ready': "Système prêt!                   ",

        'menu_title': "--- Menu Principal ---",
        'menu_prompt': "Menu > ",
        'menu_help': "Options: 'settings', 'restart', 'shutdown', 'back'",
        'desc_menu': "Ouvrir le menu principal (paramètres, alimentation)",

        'set_title': "--- Menu des Paramètres ---",
        'set_prompt': "Paramètres > ",
        'set_help': "Options: 'sysinfo' (Info système), 'lang' (Changer de langue), 'back' (Quitter)",

        'lang_choose': "Langues disponibles: en (Anglais), fr (Français), nl (Néerlandais).\nChoisissez la langue: ",
        'lang_set': "La langue a été définie sur Français.",

        'desc_help': "Afficher cette aide",
        'desc_echo': "Imprimer le texte donné",
        'desc_calc': "Calculer une expression simple (+, -, *, /, //, %, **)",
        'desc_clear': "Effacer l'écran",
        'desc_time': "Afficher la date et l'heure",
        'desc_history': "Afficher l'historique des commandes",
        'desc_ls': "Lister les fichiers et dossiers du répertoire",
        'desc_game': "Jouer au jeu de devinettes de nombres",
        'desc_touch': "Créer un nouveau fichier texte (ex: touch fichier.txt)",
        'desc_cat': "Lire et afficher le contenu du fichier (ex: cat fichier.txt)",

        'sys_info_title': "--- Informations Système ---",
        'sys_storage': "--- Stockage & Mémoire ---",
        'sys_unavailable': "Indisponible",
        'sys_ram_req': "Indisponible (Nécessite 'psutil')",
        'file_err': "Veuillez spécifier un nom de fichier.",
        'file_not_found': "Erreur: Fichier '{file}' introuvable ou est un dossier.",
        'file_created': "Fichier '{file}' créé avec succès.",
        'file_read_err': "Erreur de traitement du fichier: {error}"
    },
    'nl': {
        'welcome': "Welkom terug, {name}! Typ 'help' voor de lijst met opdrachten.",
        'started': "EXP OS {version} is gestart.",
        'shutdown': "EXP OS wordt afgesloten...",
        'restarting': "EXP OS wordt opnieuw gestart...",
        'not_found': "Fout: commando '{cmd}' niet gevonden.",
        'avail_cmd': "Beschikbare commando's:",
        'no_help': "Geen hulp beschikbaar voor commando '{cmd}'.",
        'hist_empty': "Geschiedenis is leeg.",
        'dir_empty': "Map is leeg.",

        'boot_init': "Hardware-interface initialiseren...",
        'boot_kernel': "Systeemkernel laden...",
        'boot_fs': "Virtueel bestandssysteem koppelen...",
        'boot_session': "Gebruikerssessie starten...",
        'boot_ready': "Systeem gereed!                   ",

        'menu_title': "--- Hoofdmenu ---",
        'menu_prompt': "Menu > ",
        'menu_help': "Opties: 'settings', 'restart', 'shutdown', 'back'",
        'desc_menu': "Open hoofdmenu (instellingen, afsluiten/herstarten)",

        'set_title': "--- Instellingen Menu ---",
        'set_prompt': "Instellingen > ",
        'set_help': "Opties: 'sysinfo' (Systeeminfo), 'lang' (Taal wijzigen), 'back' (Sluiten)",

        'lang_choose': "Beschikbare talen: en (Engels), fr (Frans), nl (Nederlands).\nKies een taal: ",
        'lang_set': "Taal succesvol ingesteld op Nederlands.",

        'desc_help': "Toon deze hulp",
        'desc_echo': "Druk de gegeven tekst af",
        'desc_calc': "Bereken een eenvoudige expressie (+, -, *, /, //, %, **)",
        'desc_clear': "Wis het scherm",
        'desc_time': "Toon huidige datum en tijd",
        'desc_history': "Toon commandogeschiedenis",
        'desc_ls': "Toon bestanden en mappen in de huidige map",
        'desc_game': "Speel een getallenraadspel",
        'desc_touch': "Maak een nieuw tekstbestand (bijv. touch bestand.txt)",
        'desc_cat': "Lees en toon de bestandsinhoud (bijv. cat bestand.txt)",

        'sys_info_title': "--- Systeeminformatie ---",
        'sys_storage': "--- Opslag & Geheugen ---",
        'sys_unavailable': "Niet beschikbaar",
        'sys_ram_req': "Niet beschikbaar (Vereist 'psutil')",
        'file_err': "Geef een bestandsnaam op.",
        'file_not_found': "Fout: Bestand '{file}' niet gevonden of is een map.",
        'file_created': "Bestand '{file}' succesvol aangemaakt.",
        'file_read_err': "Fout bij verwerken bestand: {error}"
    }
}


class EXPOS:
    def __init__(self):
        self.running = True
        self.is_restarting = False
        self.version = "alpha 0.0.1.1"  # Версия обновлена
        self.history = []
        self.username = "User"
        self.lang = "en"
        self.config_file = ".expos_config"

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
            'cat': self.cmd_cat
        }

    @property
    def help_text(self):
        return {
            'help': self.t('desc_help'),
            'menu': self.t('desc_menu'),
            'echo': self.t('desc_echo'),
            'calc': self.t('desc_calc'),
            'clear': self.t('desc_clear'),
            'time': self.t('desc_time'),
            'history': self.t('desc_history'),
            'ls': self.t('desc_ls'),
            'game': self.t('desc_game'),
            'touch': self.t('desc_touch'),
            'cat': self.t('desc_cat')
        }

    def t(self, key, **kwargs):
        text = LANGUAGES.get(self.lang, LANGUAGES['en']).get(key, LANGUAGES['en'].get(key, key))
        if kwargs:
            return text.format(**kwargs)
        return text

    def load_config(self):
        if py_os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    content = f.read().strip()
                    if content.startswith('{'):
                        config = json.loads(content)
                        self.username = config.get('username', 'User')
                        self.lang = config.get('lang', 'en')
                    else:
                        self.username = content
                        self.lang = "en"
                        self.save_config()
            except:
                self.username = "User"
                self.lang = "en"
        else:
            self.run_installation()

    def save_config(self):
        config = {'username': self.username, 'lang': self.lang}
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Config save error: {e}")

    def run_installation(self):
        self.cmd_clear("")
        print("Starting EXP OS Installation Process...")
        time.sleep(1)
        print("Checking hardware compatibility...")
        time.sleep(1)
        print("\nInstallation successful!")

        while True:
            name = input("Please create a username for this system: ").strip()
            if name:
                self.username = name
                break
            else:
                print("Username cannot be empty.")

        self.lang = "en"
        self.save_config()
        print(f"\nConfiguring user profile for '{self.username}'...")
        time.sleep(1)
        self.cmd_clear("")

    # ===== ПРОЦЕСС ЗАГРУЗКИ ОТ 1 ДО 100% =====
    def boot_sequence(self):
        self.cmd_clear("")
        print(f"EXP OS {self.version} Booting...\n")

        total_steps = 100
        for i in range(1, total_steps + 1):
            # Вычисляем длину полоски загрузки (40 символов)
            blocks = int((i / 100) * 40)
            bar = '█' * blocks + '-' * (40 - blocks)

            # Динамические сообщения в зависимости от процента
            if i < 25:
                status = self.t('boot_init')
            elif i < 50:
                status = self.t('boot_kernel')
            elif i < 85:
                status = self.t('boot_fs')
            elif i < 100:
                status = self.t('boot_session')
            else:
                status = self.t('boot_ready')

            # Использование sys.stdout для перерисовки строки без перехода на новую
            sys.stdout.write(f"\r[{bar}] {i}% | {status}")
            sys.stdout.flush()

            # Задержки для реалистичности (иногда система "задумывается")
            if i in [24, 49, 84]:
                time.sleep(0.3)
            else:
                time.sleep(random.uniform(0.01, 0.05))

        print("\n")
        time.sleep(0.5)
        self.cmd_clear("")

    # =========================================

    def start(self):
        self.load_config()
        self.boot_sequence()  # Запуск анимации загрузки
        print(self.t('started', version=self.version))
        print(self.t('welcome', name=self.username))

        while self.running:
            try:
                user_input = input(f"\n{self.username}@expos > ").strip()
                if not user_input:
                    continue

                self.history.append(user_input)
                self.execute_command(user_input)
            except (KeyboardInterrupt, EOFError):
                print(f"\n{self.t('shutdown')}")
                break

    def execute_command(self, command_line):
        parts = command_line.split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''

        if cmd in self.commands:
            self.commands[cmd](args)
        else:
            print(self.t('not_found', cmd=cmd))

    def cmd_help(self, args):
        if args:
            if args in self.help_text:
                print(f"{args}: {self.help_text[args]}")
            else:
                print(self.t('no_help', cmd=args))
        else:
            print(self.t('avail_cmd'))
            for cmd, desc in self.help_text.items():
                print(f"  {cmd:<8} - {desc}")

    def cmd_echo(self, args):
        print(args)

    def cmd_time(self, args):
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))

    def cmd_history(self, args):
        if not self.history:
            print(self.t('hist_empty'))
        else:
            for i, cmd in enumerate(self.history, 1):
                print(f"{i:3}: {cmd}")

    def cmd_ls(self, args):
        try:
            files = py_os.listdir('.')
            if not files:
                print(self.t('dir_empty'))
            else:
                for f in sorted(files):
                    if py_os.path.isdir(f):
                        print(f"[DIR]  {f}")
                    else:
                        print(f"[FILE] {f}")
        except Exception as e:
            print(f"Error: {e}")

    def cmd_menu(self, args):
        print(self.t('menu_title'))
        print(self.t('menu_help'))

        while self.running:
            cmd = input(self.t('menu_prompt')).strip().lower()
            if cmd in ['back', 'exit', 'quit']:
                break
            elif cmd == 'settings':
                self.cmd_settings("")
            elif cmd == 'restart':
                self.cmd_restart("")
            elif cmd == 'shutdown':
                self.cmd_shutdown("")
            else:
                print(self.t('menu_help'))

    def cmd_settings(self, args):
        print(self.t('set_title'))
        print(self.t('set_help'))

        while self.running:
            cmd = input(self.t('set_prompt')).strip().lower()
            if cmd in ['back', 'exit', 'quit']:
                break
            elif cmd == 'sysinfo':
                self.run_sysinfo()
            elif cmd == 'lang':
                self.run_lang()
            else:
                print(self.t('set_help'))

    def run_sysinfo(self):
        print(self.t('sys_info_title'))
        print(f"EXP OS Version : {self.version} Build 11")
        print(f"Current User   : {self.username}")
        print(f"Host System    : {platform.system()} {platform.release()}")
        print(f"Architecture   : {platform.machine()}")
        print(self.t('sys_storage'))

        try:
            total, used, free = shutil.disk_usage(py_os.path.abspath(py_os.sep))
            print(f"Disk Total     : {total // (2 ** 30)} GB")
            print(f"Disk Free      : {free // (2 ** 30)} GB")
        except Exception:
            print(f"Disk Space     : {self.t('sys_unavailable')}")

        if HAS_PSUTIL:
            mem = psutil.virtual_memory()
            print(f"RAM Total      : {mem.total // (2 ** 20)} MB")
            print(f"RAM Available  : {mem.available // (2 ** 20)} MB")
        else:
            print(f"RAM Info       : {self.t('sys_ram_req')}")

    def run_lang(self):
        new_lang = input(self.t('lang_choose')).strip().lower()
        if new_lang in LANGUAGES:
            self.lang = new_lang
            self.save_config()
            print(self.t('lang_set'))
        else:
            print("Invalid language code. Keeping current language.")

    def cmd_shutdown(self, args):
        print(self.t('shutdown'))
        time.sleep(1)
        self.running = False

    def cmd_restart(self, args):
        # Теперь перезагрузка просто прерывает текущую сессию
        # Загрузочный экран появится автоматически благодаря boot_sequence()
        print(self.t('restarting'))
        time.sleep(1)
        self.running = False
        self.is_restarting = True

    def cmd_touch(self, args):
        if not args:
            print(self.t('file_err'))
            return
        try:
            with open(args, 'a') as f:
                pass
            print(self.t('file_created', file=args))
        except Exception as e:
            print(self.t('file_read_err', error=str(e)))

    def cmd_cat(self, args):
        if not args:
            print(self.t('file_err'))
            return
        if not py_os.path.exists(args) or py_os.path.isdir(args):
            print(self.t('file_not_found', file=args))
            return
        try:
            with open(args, 'r', encoding='utf-8') as f:
                print(f.read())
        except Exception as e:
            print(self.t('file_read_err', error=str(e)))

    def cmd_calc(self, args):
        if not args:
            print("Usage: calc <expression>")
            return
        try:
            result = self.safe_eval(args)
            print(result)
        except Exception as e:
            print(f"Error in expression: {e}")

    def safe_eval(self, expression):
        allowed_operators = {
            ast.Add: operator.add, ast.Sub: operator.sub,
            ast.Mult: operator.mul, ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
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
                raise ValueError(f"Unsupported operator: {op_type}")
            raise ValueError("Invalid expression")

        try:
            tree = ast.parse(expression, mode='eval')
            return _eval(tree.body)
        except Exception as e:
            raise ValueError("Invalid syntax")

    def cmd_clear(self, args):
        if platform.system() == "Windows":
            py_os.system('cls')
        else:
            print("\033[H\033[J", end="")

    def cmd_game(self, args):
        number = random.randint(1, 100)
        print("Welcome to the Guessing Game! (1 - 100)")
        attempts = 0
        while True:
            guess_str = input("Game > ").strip().lower()
            if guess_str in ['quit', 'exit', 'back']:
                break
            if not guess_str.isdigit():
                continue
            guess = int(guess_str)
            attempts += 1
            if guess < number:
                print("Too low!")
            elif guess > number:
                print("Too high!")
            else:
                print(f"Congratulations! You guessed {number} in {attempts} attempts!")
                break


if __name__ == "__main__":
    while True:
        my_os = EXPOS()
        my_os.start()

        if not my_os.is_restarting:
            break
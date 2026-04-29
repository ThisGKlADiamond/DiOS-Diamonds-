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

# Translation Dictionary
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

        # Boot Messages
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
        'set_help': "Available options: 'sysinfo', 'lang', 'back'",

        'lang_choose': "Available: en, fr, nl.\nChoose language: ",
        'lang_set': "Language successfully set to English.",

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

        'sys_info_title': "--- System Information ---",
        'sys_storage': "--- Storage & Memory ---",
        'sys_unavailable': "Unavailable",
        'sys_ram_req': "Requires 'psutil' module",
        'file_err': "Please specify a name/path.",
        'file_not_found': "Error: '{file}' not found.",
        'file_created': "Item '{file}' created.",
        'file_deleted': "Item '{file}' deleted.",
        'file_read_err': "Error processing item: {error}"
    },
    'fr': {
        'welcome': "Bon retour, {name}! Tapez 'help' pour l'aide.",
        'started': "EXP OS {version} démarré.",
        'shutdown': "Fermeture de EXP OS...",
        'restarting': "Redémarrage de EXP OS...",
        'not_found': "Erreur: commande '{cmd}' introuvable.",
        'avail_cmd': "Commandes disponibles:",
        'no_help': "Aucune aide pour '{cmd}'.",
        'hist_empty': "L'historique est vide.",
        'dir_empty': "Le répertoire est vide.",

        'boot_init': "Initialisation du matériel...",
        'boot_kernel': "Chargement du noyau...",
        'boot_fs': "Montage du système de fichiers...",
        'boot_session': "Démarrage de la session...",
        'boot_ready': "Système prêt!                   ",

        'menu_title': "--- Menu Principal ---",
        'menu_prompt': "Menu > ",
        'menu_help': "Options: 'settings', 'restart', 'shutdown', 'back'",
        'desc_menu': "Menu principal",

        'set_title': "--- Paramètres ---",
        'set_prompt': "Paramètres > ",
        'set_help': "Options: 'sysinfo', 'lang', 'back'",

        'lang_choose': "Disponibles: en, fr, nl.\nLangue: ",
        'lang_set': "Langue définie sur Français.",

        'desc_help': "Afficher l'aide",
        'desc_echo': "Afficher un texte",
        'desc_calc': "Calculatrice mathématique",
        'desc_clear': "Effacer l'écran",
        'desc_time': "Afficher l'heure",
        'desc_history': "Historique des commandes",
        'desc_ls': "Lister les fichiers",
        'desc_game': "Jeu de devinettes",
        'desc_touch': "Créer un fichier",
        'desc_cat': "Lire un fichier",
        'desc_mkdir': "Créer un nouveau dossier",
        'desc_rm': "Supprimer un fichier/dossier",
        'desc_whoami': "Afficher l'utilisateur actuel",

        'sys_info_title': "--- Informations Système ---",
        'sys_storage': "--- Stockage & Mémoire ---",
        'sys_unavailable': "Indisponible",
        'sys_ram_req': "Nécessite 'psutil'",
        'file_err': "Spécifiez un nom/chemin.",
        'file_not_found': "Erreur: '{file}' introuvable.",
        'file_created': "Élément '{file}' créé.",
        'file_deleted': "Élément '{file}' supprimé.",
        'file_read_err': "Erreur: {error}"
    },
    'nl': {
        'welcome': "Welkom terug, {name}! Typ 'help' voor hulp.",
        'started': "EXP OS {version} gestart.",
        'shutdown': "EXP OS wordt afgesloten...",
        'restarting': "EXP OS wordt opnieuw gestart...",
        'not_found': "Fout: commando '{cmd}' niet gevonden.",
        'avail_cmd': "Beschikbare commando's:",
        'no_help': "Geen hulp voor '{cmd}'.",
        'hist_empty': "Geschiedenis is leeg.",
        'dir_empty': "Map is leeg.",

        'boot_init': "Hardware initialiseren...",
        'boot_kernel': "Kernel laden...",
        'boot_fs': "Bestandssysteem koppelen...",
        'boot_session': "Sessie starten...",
        'boot_ready': "Systeem gereed!                   ",

        'menu_title': "--- Hoofdmenu ---",
        'menu_prompt': "Menu > ",
        'menu_help': "Opties: 'settings', 'restart', 'shutdown', 'back'",
        'desc_menu': "Open hoofdmenu",

        'set_title': "--- Instellingen ---",
        'set_prompt': "Instellingen > ",
        'set_help': "Opties: 'sysinfo', 'lang', 'back'",

        'lang_choose': "Beschikbaar: en, fr, nl.\nKies taal: ",
        'lang_set': "Taal ingesteld op Nederlands.",

        'desc_help': "Toon hulp",
        'desc_echo': "Tekst afdrukken",
        'desc_calc': "Bereken wiskunde",
        'desc_clear': "Scherm wissen",
        'desc_time': "Huidige tijd",
        'desc_history': "Commandogeschiedenis",
        'desc_ls': "Bestanden weergeven",
        'desc_game': "Getallenspel",
        'desc_touch': "Maak bestand",
        'desc_cat': "Bestand lezen",
        'desc_mkdir': "Maak een nieuwe map",
        'desc_rm': "Verwijder een bestand/map",
        'desc_whoami': "Toon huidige gebruiker",

        'sys_info_title': "--- Systeeminformatie ---",
        'sys_storage': "--- Opslag & Geheugen ---",
        'sys_unavailable': "Niet beschikbaar",
        'sys_ram_req': "Vereist 'psutil'",
        'file_err': "Geef een naam/pad op.",
        'file_not_found': "Fout: '{file}' niet gevonden.",
        'file_created': "Item '{file}' aangemaakt.",
        'file_deleted': "Item '{file}' verwijderd.",
        'file_read_err': "Fout: {error}"
    }
}


class EXPOS:
    def __init__(self):
        self.running = True
        self.is_restarting = False
        self.version = "alpha 0.0.2 Build 12"
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
            'cat': self.cmd_cat,
            'mkdir': self.cmd_mkdir,
            'rm': self.cmd_rm,
            'whoami': self.cmd_whoami
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
            'cat': self.t('desc_cat'),
            'mkdir': self.t('desc_mkdir'),
            'rm': self.t('desc_rm'),
            'whoami': self.t('desc_whoami')
        }

    def t(self, key, **kwargs):
        text = LANGUAGES.get(self.lang, LANGUAGES['en']).get(key, LANGUAGES['en'].get(key, key))
        return text.format(**kwargs) if kwargs else text

    def load_config(self):
        if py_os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    content = f.read().strip()
                    config = json.loads(content)
                    self.username = config.get('username', 'User')
                    self.lang = config.get('lang', 'en')
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
        print(">>> EXP OS Deployment System <<<")
        time.sleep(0.5)
        while True:
            name = input("Enter System Username: ").strip()
            if name:
                self.username = name
                break
            print("Username required.")
        self.save_config()
        self.cmd_clear("")

    def boot_sequence(self):
        self.cmd_clear("")
        print(f"EXP OS Core v.{self.version}")
        print("EXP OS 2026 © All Rights Reserved\n")  # Добавлен копирайт

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
            time.sleep(random.uniform(0.01, 0.04))

        print(f"\n\n{self.t('boot_ready')}")
        time.sleep(0.8)
        self.cmd_clear("")

    def start(self):
        self.load_config()
        self.boot_sequence()
        print(self.t('started', version=self.version))
        print(self.t('welcome', name=self.username))

        while self.running:
            try:
                user_input = input(f"{self.username} EXP OS > ").strip()
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

    def cmd_help(self, args):
        print("\nEXP OS 2026 © All Rights Reserved")  # Добавлен копирайт
        print(f"{self.t('avail_cmd')}")
        for cmd, desc in self.help_text.items():
            print(f"  {cmd:<10} : {desc}")

    def cmd_echo(self, args):
        print(args)

    def cmd_time(self, args):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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
                    tag = "[DIR] " if py_os.path.isdir(f) else "[FILE]"
                    print(f"{tag} {f}")
        except Exception as e:
            print(f"FS Error: {e}")

    def cmd_whoami(self, args):
        print(self.username)

    def cmd_mkdir(self, args):
        if not args: print(self.t('file_err')); return
        try:
            py_os.makedirs(args, exist_ok=True)
            print(self.t('file_created', file=args))
        except Exception as e:
            print(self.t('file_read_err', error=e))

    def cmd_rm(self, args):
        if not args: print(self.t('file_err')); return
        if not py_os.path.exists(args): print(self.t('file_not_found', file=args)); return
        try:
            if py_os.path.isdir(args):
                shutil.rmtree(args)
            else:
                py_os.remove(args)
            print(self.t('file_deleted', file=args))
        except Exception as e:
            print(self.t('file_read_err', error=e))

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

    def run_sysinfo(self):
        print(f"\n{self.t('sys_info_title')}")
        print(f"Build Version  : {self.version}")
        print(f"User           : {self.username}")
        print(f"OS Platform    : {platform.system()} {platform.release()}")
        print(self.t('sys_storage'))
        try:
            # Исправлено на кроссплатформенный вариант для Windows/Linux/Mac
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
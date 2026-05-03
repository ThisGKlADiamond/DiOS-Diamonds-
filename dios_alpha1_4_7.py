import os
import sys
import platform
import shlex
import time
import shutil
import random
import json
import subprocess
import math
import calendar
from datetime import datetime

# Autocompletion and history (Unix/Linux and supported consoles)
try:
    import readline

    COMMANDS = ['menu', 'help', 'clear', 'settings', 'store', 'files', 'browser', 'calc', 'messages',
                'antivirus', 'edit', 'notepad', 'cat', 'construction', 'hide_seek', 'number_guess', 'shutdown',
                'restart', 'exit', 'new_user', 'update', 'backup', 'restore', 'cd', 'mkdir', 'rm', 'sysmon', 'history',
                'charge', 'lock', 'time', 'ping', 'wget', 'ps', 'kill', 'coins', 'whoami', 'su', 'sudo', 'mail', 'sh',
                'ssh', 'moryak.exe', 'run', 'zip', 'unzip', 'paint', 'bank', 'alias', 'autostart', 'notifications',
                'profile', 'weather', 'calendar']


    def completer(text, state):
        options = [cmd for cmd in COMMANDS if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None


    readline.set_completer(completer)
    if readline.__doc__ and 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
except ImportError:
    pass

# Sound and system keys (Windows)
try:
    import winsound
    import msvcrt

    HAS_WINDOWS_API = True
except ImportError:
    HAS_WINDOWS_API = False

# --- ANSI COLOR CODES ---
THEMES = {
    "standard": "\033[37m",
    "matrix": "\033[32m",
    "cyber": "\033[36m",
    "warning": "\033[31m",
    "hacker": "\033[1;32m",
    "neon": "\033[1;35m",
    "med_cyan": "\033[1;36m",
    "med_white": "\033[1;37m",
    "med_red": "\033[1;31m",
    "dark": "\033[30m",
    "edu_gold": "\033[33m",
    "gold": "\033[1;33m",
    "retro": "\033[1;34m"
}

# Image-based Wallpapers mapped to ANSI Backgrounds
WALLPAPERS = {
    "black": "\033[40m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "purple": "\033[45m",
    "cyan": "\033[46m",
    "white": "\033[47m",
    "green": "\033[42m",
    "flowers": "\033[42m",
    "rain": "\033[44m",
    "gold_grid": "\033[43m",
    "retro_grid": "\033[44m"
}


class DiOS:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.user = "Guest"
        self.current_user = "Guest"
        self.version = "alpha 1.4.7"  # UPDATED VERSION
        self.config_file = "dios_sys.json"
        self.backup_file = "dios_sys_backup.json"
        self.messenger_contacts = {"1": "Alex (Friend)", "2": "CodeMind AI"}
        self.screen_buffer = []
        self.command_history = []
        self.battery = 100
        self.root_password = "root"

        # Process Management
        self.processes = {
            1: "dios_kernel",
            102: "vfs_daemon",
            105: "net_listener",
            214: "sysmon_bg"
        }

        # Fake servers for SSH
        self.fake_servers = {
            "admin@192.168.0.100": {
                "password": "admin",
                "files": {
                    "logs.asc": "   \\_/\n  (o.o)\n   > ^ <\nASCII Server Cat!",
                    "secret.txt": "Project Moryak was abandoned. Reward code for 100 coins: 777"
                }
            }
        }

        # System states
        self.power_on = True
        self.current_state = "boot"
        self.active_app = None

        self.bg_tasks = {}
        self.notification = None

        # User Database
        self.users_db = {}
        self.user_data = {}

        self.theme_prefix = THEMES["cyber"]

        self.help_text = f"""
DiOS {self.version} Help:
--- System & Environment ---
menu          : open main system menu
help          : show this help menu
clear         : refresh screen
settings      : OS personalization, theme, sysinfo
store         : Diamond Store (Install Apps & Themes)
update        : Check for OS updates
sysmon        : System Resource Monitor
backup        : Backup system config
restore       : Restore system config
history       : Show command history
charge        : Plug in charger
lock          : Lock system
time          : Show system time
calendar      : Show current month calendar
weather       : Show local weather simulation
notifications : Notification Center
alias         : Create command shortcuts
autostart     : Set app on login

--- Permissions & Scripting ---
whoami    : Show current logged in user
su <user> : Switch user
sudo <cmd>: Execute command with admin privileges
sh <file> : Execute a .dsh script file
run <file>: Run .dsh scripts easily
new_user  : Create new account
profile   : View your User Profile & Level

--- Network & Files ---
files       : File Explorer
cd <dir>    : Change directory
mkdir <dir> : Create directory
rm <target> : Remove file/directory
cat <file>  : Read text/ASCII file content
zip <dir>   : Archive folder
unzip <file>: Extract archive
ping <host> : Send ICMP echo requests
wget <url>  : Download file
ssh <u@ip>  : Connect to servers

--- Processes ---
ps          : List running background processes
kill <pid>  : Terminate process

--- Economy & Social ---
coins          : Check Diamond Coins balance
bank <usr> <#>: Transfer coins
mail           : Open Mail Client

--- Apps & Entertainment ---
browser      : Web Browser
calc         : Extended Calculator
messages     : Messenger
antivirus    : System security
notepad      : Open Text Editor
paint        : DiOS Paint ASCII
edit <f>     : Quick Edit Text file
construction : City Builder
hide_seek    : 3D Hide & Seek
number_guess : Number Guesser Game
moryak.exe   : [CLASSIFIED]
"""

    def set_4_3_resolution(self):
        sys.stdout.write('\x1b[8;60;80t')
        sys.stdout.flush()

    def beep(self, freq=600, duration=150):
        if HAS_WINDOWS_API:
            try:
                winsound.Beep(freq, duration)
            except:
                pass
        else:
            sys.stdout.write('\a')
            sys.stdout.flush()

    def set_notify(self, text):
        self.notification = (text, time.time())
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.user_data.setdefault("notifications", []).insert(0, f"[{timestamp}] {text}")
        if len(self.user_data["notifications"]) > 50:
            self.user_data["notifications"].pop()
        self.beep(800, 100)

    def add_xp(self, amount):
        if self.user_data.get("xp_boost", False):
            amount *= 2

        self.user_data.setdefault("xp", 0)
        self.user_data.setdefault("level", 1)

        self.user_data["xp"] += amount
        xp_needed = self.user_data["level"] * 100

        self._print_buf(f"{THEMES['edu_gold']}✨ +{amount} XP!{THEMES['standard']}")

        if self.user_data["xp"] >= xp_needed:
            self.user_data["xp"] -= xp_needed
            self.user_data["level"] += 1
            self.update_title()
            self.set_notify(f"🎉 LEVEL UP! You are now Level {self.user_data['level']}")
            self.beep(1200, 300)

    def update_title(self):
        lvl = self.user_data.setdefault("level", 1)
        if lvl >= 20:
            title = "Academic Genius"
        elif lvl >= 15:
            title = "Master Scholar"
        elif lvl >= 10:
            title = "Senior Student"
        elif lvl >= 5:
            title = "Dedicated Learner"
        else:
            title = "Novice"
        self.user_data["title"] = title

    def _print_buf(self, text):
        self.screen_buffer.append(f"{self.theme_prefix}{text}")

    def _print_unknown(self, cmd=""):
        if cmd:
            self._print_buf(f"Unknown command: {cmd}")
        self._print_buf("If you don't know this command, write 'help' to parse all the commands.")
        self.beep(400, 250)

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # --- PERSISTENCE & BACKUPS ---
    def save_system(self):
        try:
            if self.current_user in self.users_db:
                self.users_db[self.current_user] = self.user_data

            save_payload = {
                "version": self.version,
                "users_db": self.users_db
            }
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(save_payload, f, indent=4)
            return True
        except Exception:
            return False

    def load_system(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)

                    if "users_db" not in saved_data:
                        name = saved_data.get("name", "Guest")
                        self.users_db = {name: saved_data}
                    else:
                        self.users_db = saved_data["users_db"]
                return True
            except:
                return False
        return False

    def backup_system(self):
        if os.path.exists(self.config_file):
            shutil.copy(self.config_file, self.backup_file)
            self.set_notify("💾 Backup successfully created")
            self._print_buf("System configuration backed up to " + self.backup_file)
        else:
            self._print_buf("Error: No config file to backup.")

    def restore_system(self):
        if os.path.exists(self.backup_file):
            shutil.copy(self.backup_file, self.config_file)
            self.load_system()
            self.set_notify("🔄 System restored")
            self._print_buf("System restored from backup. Please reboot to apply.")
        else:
            self._print_buf("Error: No backup file found.")

    def run_update(self):
        self._print_buf(f"Checking for updates... Current version: {self.version}")
        time.sleep(1)
        server_version = "alpha 1.4.7"
        if self.version == server_version:
            self._print_buf("✅ You are on the latest version.")
        else:
            self._print_buf(f"📥 Update found: {server_version}!")
            self._print_buf("Applying update... please restart OS.")
            self.version = server_version
            self.save_system()

    # --- BIOS & BOOT ANIMATION ---
    def check_f12(self):
        if HAS_WINDOWS_API and msvcrt.kbhit():
            key = msvcrt.getch()
            if key in (b'\x00', b'\xe0'):
                if msvcrt.kbhit():
                    keycode = msvcrt.getch()
                    if keycode == b'\x86': return True
        return False

    def boot_sequence(self, target_state="os", skip_bios=False):
        self.set_4_3_resolution()
        self._clear_screen()
        print(f"{THEMES['neon']}          ❖          {THEMES['standard']}")
        print(f"{THEMES['cyber']}      DiOS Core      {THEMES['standard']}")
        print(f"{THEMES['cyber']}--- TGK BIOS v1.0.6 ---{THEMES['standard']}")
        print("Initializing Hardware (4:3 Display Native)...")
        self.beep(1200, 200)

        boot_time = 3.0 if skip_bios else 10.0
        start_time = time.time()
        modules = ["CPU Logs", "RAM Check", "Mounting Storage", "Loading Kernel", "Loading UI", "Mounting FS"]
        entered_bios = False

        while time.time() - start_time < boot_time:
            elapsed = time.time() - start_time
            progress = int((elapsed / boot_time) * 100)
            bar = "█" * (progress // 2) + "-" * (50 - (progress // 2))

            if random.random() > 0.8:
                sys.stdout.write(f"\r[OK] {random.choice(modules)} loaded at {hex(random.randint(0x1000, 0xFFFF))}\n")

            sys.stdout.write(f"\r{THEMES['matrix']}[{bar}] {progress}% | Press F12 for BIOS...{THEMES['standard']}")
            sys.stdout.flush()

            if not skip_bios and not entered_bios and self.check_f12():
                entered_bios = True
                break
            time.sleep(0.1)

        print("\n\nBoot sequence complete.")
        time.sleep(0.5)
        self.current_state = "bios" if entered_bios else target_state

    def shutdown_sequence(self, target_state="power_off"):
        self._clear_screen()
        self.beep(400, 300)
        print(f"{THEMES['warning']}Initiating System Shutdown...{THEMES['standard']}")
        shutdown_time = 5.0
        start_time = time.time()
        while time.time() - start_time < shutdown_time:
            progress = int(((time.time() - start_time) / shutdown_time) * 100)
            bar = "█" * (progress // 2) + "-" * (50 - (progress // 2))
            sys.stdout.write(f"\r{THEMES['warning']}[{bar}] {progress}% {THEMES['standard']}")
            sys.stdout.flush()
            time.sleep(0.1)
        print("\nSystem Halted.")
        time.sleep(1)
        self.current_state = target_state

    def run_bios(self):
        while True:
            self._clear_screen()
            print(f"{THEMES['blue']}======================================")
            print("        TGK DiOS BIOS UTILITY         ")
            print("======================================")
            print("1. System Information\n2. Boot Priority\n3. Hardware Monitor\n4. Exit & Reboot")
            print("======================================\033[0m")
            c = input("Select > ")
            if c == '1':
                print(f"OS: DiOS {self.version}");
                input("Enter...")
            elif c == '2':
                print("[1] DiOS Virtual Drive");
                input("Enter...")
            elif c == '3':
                print(f"CPU Temp: {random.randint(35, 45)}°C");
                input("Enter...")
            elif c == '4':
                self.current_state = "boot";
                break

    # --- INSTALLATION CHAIN & MULTI-USER ---
    def run_install_step_1(self):
        self._clear_screen()
        print(f"{THEMES['neon']}❖ DiOS INSTALLATION WIZARD ❖{THEMES['standard']}")
        print("Step 1: Information Gathering...")
        time.sleep(2.5)
        print("Gathering system parameters and preparing disk partitions...")
        time.sleep(2.5)
        print("Step 2: Preparation for installation...")
        time.sleep(2.5)
        print("\nRebooting computer to initialize installer environment...")
        time.sleep(3)
        self.current_state = "install_reboot_1"

    def run_install_step_3(self):
        self._clear_screen()
        print(f"{THEMES['neon']}❖ DiOS INSTALLATION WIZARD ❖{THEMES['standard']}")
        print("Step 3: System Installation...")
        for i in range(1, 101, 7):
            bar = "█" * (i // 5) + "-" * (20 - (i // 5))
            sys.stdout.write(f"\rInstalling Core Components... [{bar}] {i}%")
            sys.stdout.flush()
            time.sleep(0.4)
        sys.stdout.write(f"\rInstalling Core Components... [{'█' * 20}] 100%\n")
        print("Installation of core files complete.\nRebooting computer to apply system changes...")
        time.sleep(3)
        self.current_state = "install_reboot_2"

    def run_install_step_4(self):
        self._clear_screen()
        print(f"{THEMES['neon']}❖ DiOS INSTALLATION WIZARD ❖{THEMES['standard']}")
        print("Step 4: Finishing installation...")
        time.sleep(2)
        print("Configuring hardware profiles...")
        time.sleep(2)
        print("Setting up virtual file systems...")
        time.sleep(2)
        print("\nFinalizing setup... Rebooting computer one last time...")
        time.sleep(3)
        self.current_state = "install_reboot_3"

    def run_install_register(self):
        self._clear_screen()
        print(f"{THEMES['neon']}❖ DiOS REGISTRATION ❖{THEMES['standard']}")
        print("Welcome to your new operating system. Let's create your first account.")
        time.sleep(1)
        name = input("Enter your username: ").strip()
        country = input("Enter your country: ").strip()
        while True:
            pwd = input("Set password: ")
            if pwd == input("Confirm password: "):
                break
            else:
                print("Passwords do not match. Try again.")

        self.users_db = {}
        self.users_db[name] = {
            "name": name,
            "country": country,
            "password": pwd,
            "theme": "cyber",
            "wallpaper": "magenta",
            "taskbar_color": "neon",
            "installed_apps": [],
            "coins": 62,  # UPDATED IN 1.4.6 (50 initial + 12 gift)
            "level": 1,
            "xp": 0,
            "title": "Novice",
            "xp_boost": False,
            "magic_door_bought": False,
            "aliases": {},
            "autostart": "",
            "themes_owned": ["cyber", "neon", "matrix", "hacker", "standard", "dark"],
            "inbox": [{"id": 1, "from": "DiOS Team", "subject": f"Welcome to {self.version}!",
                       "body": "Welcome to DiOS! Check out your new Profile and the updated Education OS features.",
                       "read": False}]
        }
        self.current_user = name
        self.user_data = self.users_db[name]
        self.save_system()
        print("Registration complete! Loading desktop...")
        print(
            f"{THEMES['edu_gold']}🎁 SYSTEM GIFT: You received 12 Diamond Coins for installing DiOS!{THEMES['standard']}")
        time.sleep(3)
        self.current_state = "os"

    def create_new_user(self):
        print(f"\n{THEMES['neon']}--- CREATE NEW ACCOUNT ---{THEMES['standard']}")
        name = input("Enter new username: ").strip()
        if name in self.users_db or name == "root" or name.lower() == "new":
            print("User already exists or name invalid!")
            time.sleep(1.5)
            return
        pwd = input("Set password: ")
        country = input("Country: ")
        self.users_db[name] = {
            "name": name,
            "country": country,
            "password": pwd,
            "theme": "cyber",
            "wallpaper": "magenta",
            "taskbar_color": "neon",
            "installed_apps": [],
            "coins": 0,
            "level": 1,
            "xp": 0,
            "title": "Novice",
            "xp_boost": False,
            "magic_door_bought": False,
            "aliases": {},
            "autostart": "",
            "themes_owned": ["cyber", "neon", "matrix", "hacker", "standard", "dark"],
            "inbox": [{"id": 1, "from": "DiOS Team", "subject": "Welcome!",
                       "body": "Welcome! You can switch accounts using the 'exit' command.",
                       "read": False}]
        }
        self.save_system()
        print(f"Account '{name}' created successfully!")
        time.sleep(1.5)

    def login(self):
        while True:
            self._clear_screen()
            print(f"{THEMES['cyber']}❖ DiOS {self.version} Login ❖{THEMES['standard']}")
            print("Available accounts:")
            for u in self.users_db:
                print(f" - {u}")
            print("\nType 'new' to create a new account.")

            name = input("\nUsername: ")
            if name.lower() == "new":
                self.create_new_user()
                continue

            pwd = input("Password: ")
            if name in self.users_db and pwd == self.users_db[name]["password"]:
                self.current_user = name
                self.user_data = self.users_db[name]

                # Migrations for older accounts
                self.user_data.setdefault("aliases", {})
                self.user_data.setdefault("autostart", "")
                self.user_data.setdefault("notifications", [])
                self.user_data.setdefault("themes_owned", ["cyber", "neon", "matrix", "hacker", "standard", "dark"])
                self.user_data.setdefault("level", 1)
                self.user_data.setdefault("xp", 0)
                self.user_data.setdefault("title", "Novice")
                self.user_data.setdefault("xp_boost", False)
                self.user_data.setdefault("magic_door_bought", False)
                self.update_title()

                self.theme_prefix = THEMES.get(self.user_data.get("theme", "cyber"), THEMES["cyber"])
                self.set_notify(f"👋 Welcome back, {self.user_data.get('title', 'Novice')} {name}")

                autostart_cmd = self.user_data.get("autostart")
                if autostart_cmd:
                    self.set_notify(f"Autostarting: {autostart_cmd}")
                    self.execute_command(autostart_cmd)
                break
            elif name == "root" and pwd == self.root_password:
                self.current_user = "root"
                self.user_data = {"name": "root", "coins": 0, "level": 99, "title": "SYSTEM GOD", "installed_apps": [],
                                  "wallpaper": "black", "aliases": {}, "autostart": ""}
                self.theme_prefix = THEMES["warning"]
                self.set_notify("🛡️ Logged in as ROOT")
                break
            print("Access Denied or User Not Found.\n")
            time.sleep(1.5)

    def lock_screen(self):
        self._clear_screen()
        print(f"{THEMES['warning']}🔒 SYSTEM LOCKED 🔒{THEMES['standard']}")
        print(f"User: {self.current_user}")
        while True:
            pwd = input("Enter password to unlock: ")
            if (self.current_user in self.users_db and pwd == self.users_db[self.current_user]["password"]) or \
                    (self.current_user == "root" and pwd == self.root_password):
                self.set_notify("System unlocked")
                break
            else:
                self.beep(400, 200)
                print("Access Denied.\n")

    # --- ADMIN PANEL ---
    def run_admin_panel(self):
        self._clear_screen()
        self.beep(1000, 500)
        while True:
            print(f"{THEMES['warning']}--- DiOS ROOT ADMIN PANEL ---")
            print("[users] View DB | [logs] Sys Logs | [reset] Factory Reset | [home] Reboot to OS")
            print("[mutant.exe] Execute Biometric Override Protocol")

            cmd = input("root@dios:~# ").strip().lower()
            if cmd == "home":
                self.current_state = "shutdown_to_os"
                break
            elif cmd == "users":
                print(f"Total Users: {len(self.users_db)}")
                for u in self.users_db: print(f"- {u}")
            elif cmd == "logs":
                for i in range(3): print(f"kernel: memory block {hex(i * 2048)} clear")
            elif cmd == "reset":
                if input("Type 'YES' to reset: ") == "YES":
                    if os.path.exists(self.config_file): os.remove(self.config_file)
                    self.current_state = "boot"
                    break
            elif cmd == "mutant.exe":
                print(f"\n{THEMES['neon']}>>> EXECUTING MUTANT.EXE OVERRIDE <<<")
                print(">>> INJECTING BIO-KERNEL MODULES...")
                print(f">>> PLEASE STAND BY FOR 9 SECONDS...{THEMES['standard']}")
                for i in range(9):
                    self.beep(1500, 50)
                    time.sleep(1)
                self.current_state = "boot_med_os"
                break
            else:
                self._print_unknown(cmd)
            print("\033[0m")

    # --- MEDICINE OS ---
    def boot_med_os_sequence(self):
        self._clear_screen()
        print(f"{THEMES['med_cyan']}========================================")
        print("  DIAMONDS MEDICINE OS - KERNEL BOOT")
        print("========================================\033[0m")
        self.beep(800, 400)

        boot_time = 11.0
        start_time = time.time()
        tasks = ["Loading Bio-Database", "Syncing MRI Drivers", "Initializing Blood Analyzer",
                 "Connecting to Global Health Net", "Booting DNA Sequencer"]

        while time.time() - start_time < boot_time:
            elapsed = time.time() - start_time
            progress = int((elapsed / boot_time) * 100)
            bar = "▓" * (progress // 2) + "░" * (50 - (progress // 2))

            if random.random() > 0.85:
                sys.stdout.write(f"\r{THEMES['med_cyan']}[MEDICAL] {random.choice(tasks)}... OK\n")

            sys.stdout.write(f"\r{THEMES['med_white']}[{bar}] {progress}% {THEMES['standard']}")
            sys.stdout.flush()
            time.sleep(0.1)

        print(f"\n\n{THEMES['med_cyan']}Welcome to Diamonds Medicine OS.{THEMES['standard']}")
        time.sleep(1)
        self.current_state = "med_os"

    def run_med_os_loop(self):
        self._clear_screen()
        print(f"{THEMES['med_cyan']}⚕️ DIAMONDS MEDICINE OS (D-MED) ⚕️")
        print(f"User: Dr. {self.user} | Status: Online")
        print("Type 'help' for medical tools or '1345' to return to DiOS.")
        print("-" * 50 + "\033[0m")

        self.user_data.setdefault("pharmacy_inventory", {"Paracetamol": 5, "Antibiotics": 2})

        while self.current_state == "med_os":
            cmd = input(f"{THEMES['med_cyan']}D-MED> \033[0m").strip().lower()

            if cmd == "1345":
                print("Disconnecting from Medical Net...")
                time.sleep(1)
                self.current_state = "shutdown_to_os"
                break
            elif cmd == "help":
                print("database       - View registered patients")
                print("blood_test     - Run simulated hematology scan")
                print("mri_scan       - Run simulated neural/body scan")
                print("dna_sequence   - Analyze DNA sequences")
                print("vitals_monitor - Real-time patient telemetry")
                print("prescribe      - Generate patient prescription")
                print("notes          - Open Medical Notepad")
                print("diagnose       - Diagnose patient symptoms")
                print("pharmacy       - Buy medical supplies for clinic")
                print("1345           - Exit Med OS")
            elif cmd == "diagnose":
                symptoms = {
                    "High fever, cough, loss of taste": "covid",
                    "Headache, stiff neck, light sensitivity": "meningitis",
                    "Chest pain, shortness of breath, left arm pain": "heart attack",
                    "Frequent urination, excessive thirst, fatigue": "diabetes"
                }
                case = random.choice(list(symptoms.keys()))
                print(f"\n[URGENT] Patient reports: {case}")
                ans = input("Enter your diagnosis: ").strip().lower()
                if ans == symptoms[case]:
                    print("Correct diagnosis! Treatment administered.")
                    print("💰 You earned 30 Diamond Coins!")
                    self.user_data["coins"] += 30
                    self.add_xp(25)
                else:
                    print(f"Incorrect diagnosis. The correct answer was: {symptoms[case]}")
                input("Press Enter...")
            elif cmd == "pharmacy":
                print(f"\n--- D-MED PHARMACY --- | Coins: {self.user_data.get('coins', 0)}")
                print("Your Inventory:", self.user_data.get("pharmacy_inventory", {}))
                catalog = {"1": ("Paracetamol (Pain/Fever)", 10, "Paracetamol"),
                           "2": ("Antibiotics (Infection)", 25, "Antibiotics"),
                           "3": ("Adrenaline (Emergency)", 50, "Adrenaline")}
                for k, v in catalog.items():
                    print(f"[{k}] {v[0]} - {v[1]} Coins")
                buy_cmd = input("Select item ID to buy (or Q to exit): ").strip()
                if buy_cmd in catalog:
                    cost = catalog[buy_cmd][1]
                    item_name = catalog[buy_cmd][2]
                    if self.user_data.get("coins", 0) >= cost:
                        self.user_data["coins"] -= cost
                        inv = self.user_data["pharmacy_inventory"]
                        inv[item_name] = inv.get(item_name, 0) + 1
                        print(f"Purchased {item_name}!")
                    else:
                        print("Not enough Diamond Coins.")
                input("Press Enter...")
            elif cmd == "database":
                print("1. John Doe (ID: 8812) - Stable\n2. Jane Smith (ID: 9921) - Needs Review")
            elif cmd == "blood_test":
                print("Running simulated blood panel...")
                time.sleep(1.5)
                wbc = random.uniform(3.5, 12.0)
                hgb = random.uniform(10.0, 18.0)
                plt = random.randint(100, 450)
                print(f"WBC (Leukocytes): {wbc:.1f} x10^9/L " + ("(HIGH)" if wbc > 10.5 else "(Normal)"))
                print(f"HGB (Hemoglobin): {hgb:.1f} g/dL " + ("(LOW)" if hgb < 12.0 else "(Normal)"))
                print(f"PLT (Platelets) : {plt} x10^9/L (Normal)")
            elif cmd == "mri_scan":
                print("Initializing MRI Simulation...")
                for i in range(5):
                    print(f"Scanning layer {i + 1}...")
                    time.sleep(0.5)
                print(f"{THEMES['med_cyan']}Scan Complete. No anomalies detected.\033[0m")
            elif cmd == "dna_sequence":
                print("Initializing DNA Sequencer...")
                bases = ["A", "T", "C", "G"]
                for i in range(3):
                    seq = "".join(random.choices(bases, k=20))
                    print(f"Sequence block {i + 1}: {seq}")
                    time.sleep(0.5)
                print(f"{THEMES['med_cyan']}Analysis Complete: No genetic mutations detected.\033[0m")
            elif cmd == "vitals_monitor":
                print("Connecting to Patient Telemetry... (Press Ctrl+C to exit)")
                try:
                    for _ in range(7):
                        hr = random.randint(65, 90)
                        spo2 = random.randint(96, 100)
                        sys.stdout.write(f"\rHeart Rate: {hr} BPM | SpO2: {spo2}%   ")
                        sys.stdout.flush()
                        time.sleep(1)
                    print("\nDisconnecting telemetry...")
                except KeyboardInterrupt:
                    print("\nTelemetry interrupted.")
            elif cmd == "prescribe":
                patient = input("Enter patient name: ")
                meds = input("Enter medication details: ")
                print(f"\n{THEMES['med_white']}--- PRESCRIPTION ---")
                print(f"Attending: Dr. {self.current_user}")
                print(f"Patient: {patient}")
                print(f"Rx: {meds}")
                print(f"Signature: Validated by D-MED OS{THEMES['standard']}")
                input("\nPress Enter to file prescription...")
            elif cmd == "notes":
                print("Opening medical notepad...")
                time.sleep(0.5)
                self.edit_file("medical_notes.txt")
            elif not cmd:
                continue
            else:
                self._print_unknown(cmd)

    # --- EDUCATION OS ---
    def boot_edu_os_sequence(self):
        self._clear_screen()
        print(f"{THEMES['edu_gold']}========================================")
        print("  DIAMONDS EDUCATION OS - STARTING")
        print("========================================\033[0m")
        self.beep(900, 300)
        time.sleep(0.5)
        self.beep(1200, 400)

        boot_time = 8.0
        start_time = time.time()
        tasks = ["Loading Curriculum", "Syncing Textbooks", "Preparing Virtual Labs", "Setting up Linguistics",
                 "Loading Gamification Core"]

        while time.time() - start_time < boot_time:
            elapsed = time.time() - start_time
            progress = int((elapsed / boot_time) * 100)
            bar = "▓" * (progress // 2) + "░" * (50 - (progress // 2))

            if random.random() > 0.85:
                sys.stdout.write(f"\r{THEMES['edu_gold']}[EDU] {random.choice(tasks)}... OK\n")

            sys.stdout.write(f"\r{THEMES['med_white']}[{bar}] {progress}% {THEMES['standard']}")
            sys.stdout.flush()
            time.sleep(0.1)

        print(f"\n\n{THEMES['edu_gold']}Welcome to Diamonds Education OS.{THEMES['standard']}")
        time.sleep(1)
        self.current_state = "edu_os"

    def run_edu_os_loop(self):
        foreign_languages = {
            "Russian": {"Привет": "Hello", "Яблоко": "Apple", "Школа": "School", "Кошка": "Cat"},
            "French": {"Привет": "Bonjour", "Школа": "École", "Собака": "Chien", "Спасибо": "Merci"},
            "Italian": {"Привет": "Ciao", "Школа": "Scuola", "Кошка": "Gatto", "Книга": "Libro"}
        }

        english_tasks = [
            ("Correct the grammar: 'He don't like apples.'", ["he doesn't like apples", "he does not like apples"]),
            ("What is the past tense of 'Go'?", ["went"])
        ]

        physics_tasks = [("What is the formula for force? (F = ?)", ["m*a", "ma", "m a"])]
        chemistry_tasks = [("What is the chemical symbol for Gold?", ["au"])]
        history_tasks = [("In what year did World War II end?", ["1945"])]
        biology_tasks = [("What is the powerhouse of the cell?", ["mitochondria", "mitochondrion"])]
        geography_tasks = [("What is the capital of Australia?", ["canberra"])]
        social_nature_tasks = [("What is the basic unit of society?", ["family"])]
        informatics_tasks = [("What does RAM stand for?", ["random access memory"])]

        logic_tasks = [
            ("Что выведет этот код: print(2 + 2 * 2)?", ["6"]),
            ("Исправь ошибку: whil True: print('A')", ["while true: print('a')", "while true:"]),
            ("Логика: Если А больше Б, а Б больше В, то А больше В? (да/нет)", ["да", "yes"]),
            ("Какой тип данных у числа 3.14 в Python?", ["float"])
        ]

        while self.current_state == "edu_os":
            self._clear_screen()
            print(f"{THEMES['edu_gold']}🎓 DIAMONDS EDUCATION OS 🎓")
            lvl = self.user_data.setdefault('level', 1)
            title = self.user_data.setdefault('title', 'Novice')
            print(f"Student: [{lvl}] {title} {self.user} | Coins: {self.user_data.get('coins', 0)}")
            print("Select Subject or Game:")
            print("[1] English (Native)      [2] Foreign Languages (Audio)")
            print("[3] Physics               [4] Chemistry")
            print("[5] History               [6] Biology")
            print("[7] Geography             [8] Social Studies / Nature")
            print("[9] Informatics           [10] Mathematics")
            print("[11] Logic & Algorithms   [12] Mini-Games (Fun Learning!)")
            print(f"{THEMES['neon']}[13] Knowledge Shop{THEMES['standard']}")
            print(f"{THEMES['med_cyan']}[14] Virtual Chemistry Lab{THEMES['standard']}")
            print("[0] Exit to DiOS")
            print("-" * 50 + "\033[0m")

            cmd = input("EDU> ").strip()

            def ask_random_question(task_list, reward=10):
                q, answers = random.choice(task_list)
                ans = input(f"Question: {q}\nAnswer: ").strip().lower()
                if ans in [a.lower() for a in answers]:
                    print(f"Correct! +{reward} Coins");
                    self.user_data["coins"] += reward
                    self.add_xp(reward * 2)
                else:
                    print(f"Incorrect. Acceptable answers: {', '.join(answers)}")
                input("Press Enter...")

            if cmd == "0":
                print("Closing textbook...")
                time.sleep(1)
                self.current_state = "shutdown_to_os"
                break
            elif cmd == "1":
                ask_random_question(english_tasks)
            elif cmd == "2":
                print("--- Foreign Languages ---")
                langs = list(foreign_languages.keys())
                for i, l in enumerate(langs): print(f"[{i + 1}] {l}")
                l_cmd = input("Select language (or 0 to cancel): ")
                if l_cmd.isdigit() and 1 <= int(l_cmd) <= len(langs):
                    lang = langs[int(l_cmd) - 1]
                    word_ru, word_en = random.choice(list(foreign_languages[lang].items()))

                    print(f"\n[AUDIO SIMULATION] Listen closely to '{word_en}'...")
                    if HAS_WINDOWS_API:
                        for char in word_en:
                            winsound.Beep(400 + (ord(char) * 5), 150)
                            sys.stdout.write(f"{char} ")
                            sys.stdout.flush()
                            time.sleep(0.05)
                        print("")

                    ans = input(f"\nTranslate '{word_ru}' to {lang}: ").strip().lower()
                    clean_en = word_en.lower().replace("?", "").replace(".", "").replace("!", "")
                    clean_ans = ans.replace("?", "").replace(".", "").replace("!", "")
                    if clean_ans == clean_en:
                        print("Correct! +15 Coins");
                        self.user_data["coins"] += 15
                        self.add_xp(30)
                    else:
                        print(f"Incorrect. The correct translation is '{word_en}'.")
                input("Press Enter...")
            elif cmd == "3":
                ask_random_question(physics_tasks)
            elif cmd == "4":
                ask_random_question(chemistry_tasks)
            elif cmd == "5":
                ask_random_question(history_tasks)
            elif cmd == "6":
                ask_random_question(biology_tasks)
            elif cmd == "7":
                ask_random_question(geography_tasks)
            elif cmd == "8":
                ask_random_question(social_nature_tasks)
            elif cmd == "9":
                ask_random_question(informatics_tasks)
            elif cmd == "10":
                a = random.randint(1, 50)
                b = random.randint(1, 50)
                op = random.choice(['+', '-', '*'])
                if op == '*': a, b = random.randint(2, 12), random.randint(2, 12)
                correct_ans = eval(f"{a} {op} {b}")
                ans = input(f"Solve: {a} {op} {b} = ?\nAnswer: ").strip()
                if ans == str(correct_ans):
                    print("Correct! +10 Coins");
                    self.user_data["coins"] += 10
                    self.add_xp(20)
                else:
                    print(f"Incorrect. The answer is {correct_ans}.")
                input("Press Enter...")
            elif cmd == "11":
                print("--- Logic & Algorithms ---")
                ask_random_question(logic_tasks, reward=20)
            elif cmd == "12":
                self._clear_screen()
                print(f"{THEMES['neon']}🎮 EDU MINI-GAMES 🎮{THEMES['standard']}")
                print("[1] Math Sprint (Solve 5 fast math problems)")
                print("[2] Word Scramble (English Vocabulary)")
                g_cmd = input("Select Game (or 0 to exit): ").strip()

                if g_cmd == "1":
                    print("MATH SPRINT: 5 Questions. Ready? Go!")
                    score = 0
                    for _ in range(5):
                        a, b = random.randint(1, 20), random.randint(1, 20)
                        if input(f"{a} + {b} = ? ").strip() == str(a + b): score += 1
                    self.user_data["coins"] += score * 5
                    self.add_xp(score * 10)
                    print(f"Sprint over! You got {score}/5 correct. Earned {score * 5} Coins.")
                    input("Press Enter...")
                elif g_cmd == "2":
                    word = random.choice(["algorithm", "biology", "terminal", "computer"])
                    scrambled = "".join(random.sample(word, len(word)))
                    print(f"Unscramble this word: {scrambled}")
                    if input("Your answer: ").strip().lower() == word:
                        print("Correct! +15 Coins");
                        self.user_data["coins"] += 15
                        self.add_xp(30)
                    else:
                        print(f"Incorrect! The word was: {word}")
                    input("Press Enter...")

            elif cmd == "13":
                self._clear_screen()
                print(f"{THEMES['edu_gold']}🛒 KNOWLEDGE SHOP 🛒{THEMES['standard']}")
                print(f"Your Balance: {self.user_data.get('coins', 0)} Diamond Coins")
                print("Boost your learning experience!")
                print("-" * 30)
                print("[1] XP Boost (x2 XP for all tasks) - 100 Coins")
                print("[2] Random Hint Ticket (Guarantees 1 easy question) - 50 Coins")
                print("[0] Return")

                shop_cmd = input("Select item to buy: ").strip()
                if shop_cmd == "1":
                    if self.user_data.get("coins", 0) >= 100:
                        if not self.user_data.get("xp_boost", False):
                            self.user_data["coins"] -= 100
                            self.user_data["xp_boost"] = True
                            self.save_system()
                            print("🎉 XP Boost Activated! You now earn double XP.")
                        else:
                            print("You already have an active XP Boost!")
                    else:
                        print("Not enough coins.")
                elif shop_cmd == "2":
                    print("Hint tickets are coming in version 1.4.7! Keep your coins.")
                input("Press Enter...")

            elif cmd == "14":
                self._clear_screen()
                print(f"{THEMES['med_cyan']}🧪 VIRTUAL CHEMISTRY LAB 🧪{THEMES['standard']}")
                print("Combine elements to discover new substances and earn rewards!")
                print("Available base elements: H (Hydrogen), O (Oxygen), Na (Sodium), Cl (Chlorine), C (Carbon)")

                recipes = {
                    ("H", "H", "O"): ("Water (H2O)", 20),
                    ("Na", "Cl"): ("Salt (NaCl)", 15),
                    ("C", "O", "O"): ("Carbon Dioxide (CO2)", 25),
                }

                print("\nType elements separated by space (e.g. 'H H O'). Type '0' to exit.")
                mix = input("Mix > ").strip().split()
                if mix and mix[0] != '0':
                    attempt = tuple(sorted(mix))
                    found = False
                    for recipe_key, (result_name, reward) in recipes.items():
                        if tuple(sorted(list(recipe_key))) == attempt:
                            print(f"✨ SUCCESS! You created {result_name}!")
                            print(f"Reward: +{reward} Coins, +{reward * 2} XP")
                            self.user_data["coins"] += reward
                            self.add_xp(reward * 2)
                            found = True
                            break
                    if not found:
                        print("💥 BOOM! Invalid reaction. The mixture exploded safely in the virtual lab.")
                input("Press Enter...")

    # --- APPS & FUNCTIONS ---
    def show_menu(self):
        self._print_buf("=" * 30)
        self._print_buf(f"❖ DiOS MAIN MENU | User: {self.current_user}")
        self._print_buf("=" * 30)
        self._print_buf("📌 TASKBAR APPS:")
        self._print_buf("   - settings")
        self._print_buf("   - files")
        self._print_buf("   - browser")
        self._print_buf("   - store")
        self._print_buf("   - mail")
        self._print_buf("   - notepad")
        self._print_buf("   - paint     (ASCII Art)")
        self._print_buf("-" * 30)
        self._print_buf("⚙️ SYSTEM COMMANDS:")
        self._print_buf("   - lock      (Lock Screen)")
        self._print_buf("   - exit      (Log Out)")
        self._print_buf("   - new_user  (Create Account)")
        self._print_buf("   - notifications")
        self._print_buf("   - profile   (View Stats)")
        self._print_buf("=" * 30)

    def run_profile(self):
        self.active_app = "Profile"
        self._clear_screen()
        lvl = self.user_data.get('level', 1)
        xp = self.user_data.get('xp', 0)
        title = self.user_data.get('title', 'Novice')
        coins = self.user_data.get('coins', 0)
        xp_needed = lvl * 100

        print(f"{THEMES['cyber']}╔══════════════════════════════════════╗")
        print(f"║ ❖ STUDENT PROFILE: {self.current_user.ljust(17)} ║")
        print(f"╠══════════════════════════════════════╣")
        print(f"║ Title: {title.ljust(29)} ║")
        print(f"║ Level: {str(lvl).ljust(29)} ║")
        print(f"║ Coins: {str(coins).ljust(29)} ║")
        print(f"║ XP:    {str(xp)} / {str(xp_needed).ljust(22)} ║")

        # XP Bar
        progress = int((xp / xp_needed) * 20)
        bar = "█" * progress + "-" * (20 - progress)
        print(f"║ Prog:  [{bar}]       ║")

        boost_status = "ACTIVE" if self.user_data.get("xp_boost", False) else "INACTIVE"
        print(f"║ XP Boost: {boost_status.ljust(26)} ║")
        print(f"╚══════════════════════════════════════╝{THEMES['standard']}")
        input("Press Enter to close profile...")
        self.active_app = None

    def run_calendar(self):
        self.active_app = "Calendar"
        now = datetime.now()
        cal = calendar.TextCalendar(calendar.MONDAY)
        str_cal = cal.formatmonth(now.year, now.month)

        self._print_buf(f"{THEMES['neon']}--- SYSTEM CALENDAR ---{THEMES['standard']}")
        for line in str_cal.split('\n'):
            if line.strip():
                self._print_buf(line)
        self.active_app = None

    def run_weather(self):
        self.active_app = "Weather"
        conditions = [
            ("☀️  Sunny", 20, 35),
            ("🌧️  Raining", 10, 22),
            ("🌩️  Thunderstorm", 15, 25),
            ("☁️  Cloudy", 12, 28),
            ("❄️  Snowing", -10, 2)
        ]
        cond = random.choice(conditions)
        temp = random.randint(cond[1], cond[2])

        self._print_buf(f"{THEMES['cyber']}--- LOCAL WEATHER ---{THEMES['standard']}")
        self._print_buf(f"Condition: {cond[0]}")
        self._print_buf(f"Temperature: {temp}°C")
        self._print_buf("Data sourced from DiOS Geo-Satellite.")
        self.active_app = None

    def run_sysmon(self):
        self.active_app = "SysMon"
        self._clear_screen()
        print(f"{THEMES['matrix']}📊 SYSTEM MONITOR (Visual Mode){THEMES['standard']}")
        print("Press Ctrl+C to exit monitor")
        try:
            for _ in range(5):
                cpu = random.randint(5, 100)
                ram = random.randint(30, 100)
                cpu_bar = "█" * (cpu // 5) + "-" * (20 - (cpu // 5))
                ram_bar = "█" * (ram // 5) + "-" * (20 - (ram // 5))
                sys.stdout.write(f"\rCPU: [{cpu_bar}] {cpu}% | RAM: [{ram_bar}] {ram}%  ")
                sys.stdout.flush()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        print("\nMonitor closed.")
        self.active_app = None
        time.sleep(0.5)

    def run_ssh(self, target):
        self.active_app = "Terminal"
        if target not in self.fake_servers:
            self._print_buf(f"ssh: Could not resolve hostname {target}")
            self.active_app = None
            return
        server = self.fake_servers[target]
        self._clear_screen()
        pwd = input(f"{target}'s password: ")

        if pwd == server["password"]:
            print(f"Access granted.\nWelcome to {target} Terminal.")
            while True:
                cmd = input(f"{THEMES['neon']}admin@{target.split('@')[1]}:~$ {THEMES['standard']}").strip()
                if cmd == "exit":
                    break
                elif cmd == "ls":
                    print("  ".join(server["files"].keys()))
                elif cmd.startswith("cat "):
                    fname = cmd.split(" ")[1]
                    print(server["files"].get(fname, "File not found."))
                else:
                    print(f"{cmd}: command not found")
        else:
            print("Access denied.")
        self.active_app = None

    def run_ping(self, target):
        self._print_buf(f"Pinging {target} with 32 bytes of data:")
        for i in range(4):
            time.sleep(0.5)
            self._print_buf(f"Reply from {target}: bytes=32 time={random.randint(12, 105)}ms TTL=54")

    def run_wget(self, url):
        self._print_buf(f"Connecting to {url}...")
        time.sleep(1)
        filename = url.split("/")[-1] if "/" in url else "downloaded.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Source: {url}\nWelcome to the DiOS Network!")
        self._print_buf(f"100% [===================>] Saved '{filename}'")

    def run_ps(self):
        self._print_buf("PID   TTY      TIME     CMD")
        for pid, cmd in self.processes.items(): self._print_buf(f"{pid:<5} pts/0    00:00:01 {cmd}")

    def run_kill(self, pid_str, is_sudo=False):
        try:
            pid = int(pid_str)
            if pid == 1:
                self._print_buf("kill: Cannot kill kernel process")
            elif pid in self.processes:
                if pid < 200 and not is_sudo and self.current_user != "root":
                    self._print_buf("kill: Permission denied. Use sudo.")
                else:
                    self._print_buf(f"Process {pid} ({self.processes.pop(pid)}) terminated.")
            else:
                self._print_buf(f"kill: ({pid}) - No such process")
        except ValueError:
            self._print_buf("Usage: kill <pid>")

    def run_files(self):
        self._print_buf(f"--- FILE EXPLORER: {self.current_dir} ---")
        try:
            for item in os.listdir(self.current_dir):
                icon = "📂" if os.path.isdir(os.path.join(self.current_dir, item)) else \
                    "🐍" if item.endswith('.py') else \
                        "📜" if item.endswith('.dsh') else \
                            "📦" if item.endswith('.zip') else "📄"
                self._print_buf(f"{icon} {item}")
        except Exception as e:
            self._print_buf(f"Error: {e}")

    def run_settings(self):
        self.active_app = "Settings"
        while True:
            self._clear_screen()
            print("⚙️ SETTINGS\n[1] SysInfo [2] Theme [3] Wallpaper\n[Q] Exit")
            c = input("> ").strip().lower()
            if c == 'q':
                break
            elif c == '1':
                print(f"❖ OS: DiOS {self.version}")
                print(f"❖ User: {self.current_user}")
                print(f"❖ Level: {self.user_data.get('level', 1)} | Title: {self.user_data.get('title', 'Novice')}")
                print(f"❖ Diamond Coins: {self.user_data.get('coins', 0)}")
                input("Press Enter...")
            elif c == '2':
                owned = self.user_data.get("themes_owned", [])
                print("Owned themes:", ", ".join(owned))
                tc = input("Enter theme name (standard/matrix/cyber/hacker/neon/dark/gold/retro) > ").strip().lower()
                if tc in THEMES and tc in owned:
                    self.user_data["theme"] = tc
                    self.theme_prefix = THEMES[tc]
                    self.save_system()
                    self.set_notify("Theme updated")
                else:
                    print("Theme not found or not purchased! Check Store.")
                    input("...")
            elif c == '3':
                bg_map = {"1": "black", "2": "flowers", "3": "rain", "4": "magenta", "5": "purple", "6": "gold_grid",
                          "7": "retro_grid"}
                for k, v in bg_map.items(): print(f"{k}: {v}")
                bg = input("Select Image > ")
                if bg in bg_map:
                    self.user_data["wallpaper"] = bg_map[bg]
                    self.save_system()
                    self.set_notify("Wallpaper updated")
        self.active_app = None

    def run_mail(self):
        self.active_app = "Mail"
        while True:
            self._clear_screen()
            print(f"📧 DiOS MAIL CLIENT | Inbox: {len(self.user_data.get('inbox', []))} messages")
            print("-" * 50)
            for mail in self.user_data.get("inbox", []):
                status = "[*]" if not mail.get("read") else "[ ]"
                print(f"ID: {mail['id']} {status} From: {mail['from']} | Subj: {mail['subject']}")

            print("-" * 50)
            cmd = input("Commands: [read <id>] | [del <id>] | [q] Exit > ").strip().lower()
            if cmd == 'q': break
            parts = cmd.split()
            if len(parts) == 2 and parts[1].isdigit():
                m_id = int(parts[1])
                mail_item = next((m for m in self.user_data["inbox"] if m["id"] == m_id), None)
                if not mail_item: continue

                if parts[0] == "read":
                    mail_item["read"] = True
                    self._clear_screen()
                    print(f"--- Message {m_id} ---\nFrom: {mail_item['from']}\nSubject: {mail_item['subject']}\n")
                    print(mail_item['body'] + "\n" + "-" * 20)
                    input("Press Enter to return...")

                    if "reward" in mail_item and not mail_item.get("claimed"):
                        self.user_data["coins"] += mail_item["reward"]
                        mail_item["claimed"] = True
                        self.set_notify(f"💰 +{mail_item['reward']} Coins!")
                        print(
                            f"You claimed {mail_item['reward']} Diamond Coins! New Balance: {self.user_data['coins']}")
                        input("Press Enter...")

                elif parts[0] == "del":
                    self.user_data["inbox"].remove(mail_item)
                    print("Message deleted.")
                    time.sleep(0.5)
        self.active_app = None

    def run_notepad(self):
        self.active_app = "Notepad"
        self._clear_screen()
        print(f"{THEMES['cyber']}❖ DiOS NOTEPAD ❖{THEMES['standard']}")
        fname = input("Enter filename to open/create (e.g. notes.txt): ").strip()
        if fname: self.edit_file(fname)
        self.active_app = None

    def run_paint(self):
        self.active_app = "Paint"
        self._clear_screen()
        print(f"{THEMES['neon']}🎨 DiOS Paint (ASCII Edition) 🎨{THEMES['standard']}")
        fname = input("Enter filename to save drawing (e.g. art.asc): ").strip()
        if not fname:
            self.active_app = None
            return
        print("Draw using ASCII characters (#, *, @). Type 'EOF' on a new line to save and exit.")
        art = []
        while True:
            line = input("| ")
            if line.strip() == "EOF": break
            art.append(line + "\n")

        with open(fname, "w", encoding="utf-8") as f:
            f.writelines(art)
        self.set_notify(f"Artwork saved as {fname}")
        self.active_app = None

    def play_hide_seek(self):
        self.active_app = "Game3D"
        if "hide_seek" not in self.user_data.get("installed_apps", []): return self._print_buf("Install from Store.")
        try:
            self._clear_screen()
            print(f"{THEMES['neon']}🌲 HIDE IN SEEK 3D 🌲{THEMES['standard']}")
            print("Choose an object to transform into:")
            print("[1] Bench")
            print("[2] Trash Can")
            print("[3] Wishing Well")
            choice = input("Select > ").strip()

            if choice == '1':
                print("\nYou transformed into a Bench. Nobody noticed you!")
                time.sleep(1)
                self.user_data["coins"] += 20
                print("You earned 20 Diamond Coins from Hide & Seek!")
                input("Press Enter...")
            elif choice == '2':
                print("\nYou transformed into a Trash Can. Smelly, but effective!")
                time.sleep(1)
                self.user_data["coins"] += 20
                print("You earned 20 Diamond Coins from Hide & Seek!")
                input("Press Enter...")
            elif choice == '3':
                print("\nWaiting...")
                time.sleep(6)
                for _ in range(100):
                    print("Well fix the well")
                    time.sleep(0.01)

                print("\n✨ You transformed into a Wishing Well!")
                time.sleep(2)
                print("Villagers approach and start taking water from the well...")
                time.sleep(2)
                print("Well (You): Glub glub... here is your water.")
                time.sleep(2)
                print("Villagers: Wait a minute... this well is talking?!")
                time.sleep(2)
                print("Villagers start tickling the well!")
                time.sleep(1)

                for i in range(9):
                    print("HAHAHA! STOP IT! HAHAHA!")
                    self.beep(800 + (i * 100), 200)
                    time.sleep(1)

                print(f"{THEMES['warning']}")
                print("██████╗  ██████╗  ██████╗ ███╗   ███╗")
                print("██╔══██╗██╔═══██╗██╔═══██╗████╗ ████║")
                print("██████╔╝██║   ██║██║   ██║██╔████╔██║")
                print("██╔══██╗██║   ██║██║   ██║██║╚██╔╝██║")
                print("██████╔╝╚██████╔╝╚██████╔╝██║ ╚═╝ ██║")
                print("╚═════╝  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝\033[0m")
                print("GAME OVER")
                input("Press Enter to exit...")
            else:
                print("Invalid choice! The seekers found you instantly!")
                input("Press Enter...")

        except Exception as e:
            print(f"Launch failed: {e}")
            input("Enter...")
        self.active_app = None

    def play_number_guess(self):
        self.active_app = "Game"
        if "number_guess" not in self.user_data.get("installed_apps", []): return self._print_buf("Install from Store.")
        self._clear_screen()
        print("🎲 NUMBER GUESSER 🎲")
        target = random.randint(1, 100)
        attempts = 0
        while True:
            guess = input("Guess a number between 1 and 100 (or Q to quit) > ").strip().lower()
            if guess == 'q': break
            if not guess.isdigit(): continue
            attempts += 1
            val = int(guess)
            if val < target:
                print("Too low!")
            elif val > target:
                print("Too high!")
            else:
                coins_earned = max(10, 50 - (attempts * 5))
                self.user_data["coins"] += coins_earned
                print(f"Correct! In {attempts} attempts. Earned {coins_earned} Coins!")
                input("Press Enter...")
                break
        self.active_app = None

    # --- UPDATED STORE FOR 1.4.7 ---
    def run_store(self):
        self.active_app = "Store"
        in_secret_store = False

        while True:
            self._clear_screen()
            print(f"💎 DIAM STORE | Balance: {self.user_data.get('coins', 0)} Coins")

            apps = {}
            if not in_secret_store:
                apps["1"] = ["Construction Sim", "construction", 0, "app"]
                apps["2"] = ["Hide In Seek 3D", "hide_seek", 0, "app"]
                apps["3"] = ["Number Guesser", "number_guess", 0, "app"]
                apps["4"] = ["Golden Theme (Premium)", "gold", 200, "theme"]
                apps["5"] = ["Retro 80s Theme", "retro", 150, "theme"]

                # Rainbow Doors
                if not self.user_data.get("magic_door_bought", False):
                    apps["6"] = ["Red Door (Magic)", "magic_door", 10, "item"]
                apps["7"] = ["Orange Door", "orange_door", 12, "item"]
                apps["8"] = ["Yellow Door", "yellow_door", 14, "item"]
                apps["9"] = ["Green Door", "green_door", 16, "item"]
                apps["10"] = ["Light Blue Door", "blue_door", 18, "item"]
                apps["11"] = ["Dark Blue Door", "indigo_door", 20, "item"]
                apps["12"] = ["Violet Door (Expensive)", "violet_door", 36, "item"]
            else:
                # Secret Menu
                apps["1"] = ["Villager hero", "villager_hero", 50, "item"]
                apps["2"] = ["Wishing Well", "wishing_well", 0, "item"]
                apps["3"] = ["Heart Emoji", "heart_emoji", 15, "item"]

            owned_themes = self.user_data.get("themes_owned", [])

            for k, v in apps.items():
                if v[3] == "app":
                    status = "[Installed]" if v[1] in self.user_data.get('installed_apps', []) else (
                        f"[{v[2]} Coins]" if v[2] > 0 else "[Free]")
                elif v[3] == "theme":
                    status = "[Owned]" if v[1] in owned_themes else f"[{v[2]} Coins]"
                else:  # item
                    status = f"[{v[2]} Coins]" if v[2] > 0 else "[Free]"
                print(f"[{k}] {v[0]} {status}")

            choice = input("\nSelect ID to install/buy (or Q to exit): ").strip().lower()
            if choice == 'q':
                break

            if choice in apps:
                item = apps[choice]

                if self.user_data.get("coins", 0) < item[2]:
                    print("Not enough Coins!");
                    input("...")
                    continue

                if item[3] == "app" and item[1] not in self.user_data.get("installed_apps", []):
                    self.user_data["coins"] -= item[2]
                    self.user_data["installed_apps"].append(item[1])
                    self.save_system()
                    self.set_notify(f"Installed: {item[0]}")
                elif item[3] == "theme" and item[1] not in owned_themes:
                    self.user_data["coins"] -= item[2]
                    self.user_data["themes_owned"].append(item[1])
                    self.save_system()
                    self.set_notify(f"Unlocked Theme: {item[0]}")
                elif item[3] == "item":
                    if item[1] == "magic_door":
                        self.user_data["coins"] -= item[2]
                        self.user_data["magic_door_bought"] = True
                        self.save_system()
                        print("\nProcessing purchase... Please wait.")
                        time.sleep(4)

                        rainbow = ["\033[31m", "\033[33m", "\033[93m", "\033[32m", "\033[36m", "\033[34m", "\033[35m"]

                        # Virus phase 1
                        for _ in range(4):
                            for color in rainbow:
                                print(f"{color}item\033[0m")
                                time.sleep(0.05)

                        # Virus phase 2
                        start_t = time.time()
                        while time.time() - start_t < 10:
                            print(f"{random.choice(rainbow)}teleportation\033[0m")
                            time.sleep(0.1)

                        # Virus phase 3
                        for _ in range(4):
                            for color in rainbow:
                                print(f"{color}item\033[0m")
                                time.sleep(0.05)

                        in_secret_store = True  # Switch to the secret menu

                    elif item[1] == "wishing_well":
                        print(f"\n{THEMES['warning']}")
                        print("██████╗  ██████╗  ██████╗ ███╗   ███╗")
                        print("██╔══██╗██╔═══██╗██╔═══██╗████╗ ████║")
                        print("██████╔╝██║   ██║██║   ██║██╔████╔██║")
                        print("██╔══██╗██║   ██║██║   ██║██║╚██╔╝██║")
                        print("██████╔╝╚██████╔╝╚██████╔╝██║ ╚═╝ ██║")
                        print("╚═════╝  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝\033[0m")
                        print("\nyou lost")
                        input("[Press Enter to close...]")
                        sys.exit(0)  # Terminate completely

                    elif item[1] in ["villager_hero", "heart_emoji"]:
                        self.user_data["coins"] -= item[2]
                        print(f"Purchased {item[0]}!")
                        input("Press Enter...")
                        in_secret_store = False  # Revert to normal store

                    else:
                        # Standard doors
                        self.user_data["coins"] -= item[2]
                        print(f"Purchased {item[0]}!")
                        input("Press Enter...")
        self.active_app = None

    def run_browser(self):
        self.active_app = "Browser"
        self._clear_screen()
        print(f"🌐 DiOS BROWSER {self.version}")
        while True:
            url = input("URL (min/q) > ").lower().strip()
            if url == 'q':
                break
            elif url == 'min':
                self.set_notify("Browser minimized");
                break
            elif url:
                print("Loading...")
        self.active_app = None

    def run_calculator(self):
        self.active_app = "Calc"
        self._clear_screen()
        print("🔢 DiOS Extended Calculator")
        safe_dict = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        while True:
            expr = input("Calc (min/q) > ").strip()
            if expr == 'q':
                break
            elif expr == 'min':
                self.set_notify("Calculator minimized");
                break
            try:
                print(f"Result: {eval(expr, {'__builtins__': None}, safe_dict)}")
            except Exception as e:
                print(f"Error: {e}")
        self.active_app = None

    def run_construction_sim(self):
        self.active_app = "SimCity"
        if "construction" not in self.user_data.get("installed_apps", []): return self._print_buf("Install from Store.")
        pop = 0
        while pop < 20:
            cmd = input(f"Pop: {pop} | [H] Build (+5) [Q] Exit > ").lower()
            if cmd == 'h':
                pop += 5
            elif cmd == 'q':
                break
        self.active_app = None

    def run_messages(self):
        self.active_app = "Messenger"
        for k, v in self.messenger_contacts.items(): print(f"[{k}] {v}")
        cmd = input("[+] Add  [Q] Exit > ")
        if cmd == '+': self.messenger_contacts[str(len(self.messenger_contacts) + 1)] = input("Name: ")
        self.active_app = None

    def run_antivirus(self):
        self.active_app = "AntiVirus"
        if input("🛡️ [1] Scan [2] Clean > ") == "1": print("Clean!")
        self.active_app = None

    def edit_file(self, filename, is_sudo=False):
        if filename in ["dios_sys.json", "dios_sys_backup.json"] and not is_sudo and self.current_user != "root":
            return self._print_buf("Permission denied. System file requires root/sudo access.")

        if not os.path.exists(filename): open(filename, "w").close()
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        while True:
            self._clear_screen()
            print(f"--- EDITING: {filename} ---")
            for i, l in enumerate(lines): print(f"{i + 1}: {l.strip()}")
            cmd = input("[s] save | [a] add | [q] exit > ").strip().lower()
            if cmd == 'q':
                break
            elif cmd == 's':
                with open(filename, "w", encoding="utf-8") as f:
                    f.writelines(lines)
                self.set_notify("File saved")
                break
            elif cmd == 'a':
                lines.append(input("New line: ") + "\n")

    # --- COMMAND PROCESSOR ---
    def execute_command(self, cmd_str, is_sudo=False):
        parts = shlex.split(cmd_str)
        if not parts: return
        cmd_raw = parts[0]

        aliases = self.user_data.get("aliases", {})
        if cmd_raw in aliases:
            cmd_str = aliases[cmd_raw] + " " + " ".join(parts[1:])
            parts = shlex.split(cmd_str)

        cmd = parts[0].lower()

        if cmd == "1191":
            self.current_state = "shutdown_to_admin"
        elif cmd == "shutdown":
            self.current_state = "power_off"
        elif cmd == "restart":
            self.current_state = "shutdown_to_os"
        elif cmd == "lock":
            self.lock_screen()
        elif cmd == "exit":
            self.current_state = "os_login"
        elif cmd == "new_user":
            self.create_new_user()
        elif cmd == "notepad":
            self.run_notepad()
        elif cmd == "paint":
            self.run_paint()
        elif cmd == "profile":
            self.run_profile()
        elif cmd == "weather":
            self.run_weather()
        elif cmd == "calendar":
            self.run_calendar()
        elif cmd == "moryak.exe":
            self._print_buf(f"{THEMES['warning']}>>> INITIATING PROJECT MORYAK...")
            self.render_desktop()
            for i in range(6, 0, -1):
                print(f"Rebooting to Education OS in {i} seconds...")
                self.beep(600, 100)
                time.sleep(1)
            self.current_state = "boot_edu_os"

        elif cmd == "sudo":
            if len(parts) < 2: return self._print_buf("Usage: sudo <command>")
            if self.current_user == "root":
                self.execute_command(" ".join(parts[1:]), is_sudo=True)
            else:
                pwd = input(f"[sudo] password for {self.current_user}: ")
                if (self.current_user in self.users_db and pwd == self.users_db[self.current_user].get("password",
                                                                                                       "")) or pwd == self.root_password:
                    self.execute_command(" ".join(parts[1:]), is_sudo=True)
                else:
                    self._print_buf("Sorry, try again.")
        elif cmd == "su":
            target_user = parts[1] if len(parts) > 1 else "root"
            if target_user == "root":
                if input("Password: ") == self.root_password:
                    self.current_user = "root"
                    self._print_buf("Switched to root.")
            elif target_user in self.users_db:
                if input("Password: ") == self.users_db[target_user].get("password", ""):
                    self.current_user = target_user
                    self.user_data = self.users_db[target_user]
                    self._print_buf(f"Switched to {self.current_user}.")
            else:
                self._print_buf(f"su: user {target_user} does not exist")
        elif cmd == "whoami":
            self._print_buf(self.current_user)

        elif cmd in ["sh", "run"]:
            if len(parts) > 1:
                filepath = parts[1]
                if not filepath.endswith('.dsh') and cmd == "run": filepath += ".dsh"
                if os.path.exists(filepath):
                    self.active_app = "Runner"
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            self._print_buf(f"> {line}")
                            self.execute_command(line, is_sudo=is_sudo)
                            self.render_desktop()
                            time.sleep(0.4)
                    self.active_app = None
                else:
                    self._print_buf(f"File not found: {filepath}")
            else:
                self._print_buf("Usage: run <script.dsh>")

        elif cmd == "zip":
            if len(parts) > 1:
                target = parts[1]
                if os.path.exists(target):
                    self._print_buf(f"Compressing {target}...")
                    time.sleep(1)
                    with open(f"{target}.zip", "w") as f:
                        f.write(f"VIRTUAL_ARCHIVE_OF:{target}")
                    self._print_buf(f"Created archive: {target}.zip")
                else:
                    self._print_buf(f"Target not found: {target}")
            else:
                self._print_buf("Usage: zip <file_or_folder>")

        elif cmd == "unzip":
            if len(parts) > 1:
                target = parts[1]
                if target.endswith('.zip') and os.path.exists(target):
                    self._print_buf(f"Extracting {target}...")
                    time.sleep(1)
                    self._print_buf(f"Extraction complete (Virtual).")
                else:
                    self._print_buf(f"Archive not found.")
            else:
                self._print_buf("Usage: unzip <file.zip>")

        elif cmd == "bank":
            if len(parts) == 3:
                target_user = parts[1]
                try:
                    amount = int(parts[2])
                    if amount <= 0:
                        self._print_buf("Amount must be positive.")
                    elif self.user_data.get("coins", 0) < amount:
                        self._print_buf("Insufficient Diamond Coins.")
                    elif target_user not in self.users_db:
                        self._print_buf("Target user not found.")
                    else:
                        self.user_data["coins"] -= amount
                        self.users_db[target_user]["coins"] += amount
                        self.save_system()
                        self._print_buf(f"Successfully transferred {amount} coins to {target_user}.")
                except ValueError:
                    self._print_buf("Amount must be a number.")
            else:
                self._print_buf("Usage: bank <username> <amount>")

        elif cmd == "alias":
            if len(parts) == 2 and "=" in parts[1]:
                alias_name, target_cmd = parts[1].split("=", 1)
                self.user_data.setdefault("aliases", {})[alias_name] = target_cmd
                self.save_system()
                self._print_buf(f"Alias set: {alias_name} -> {target_cmd}")
            else:
                self._print_buf("Current Aliases:")
                for k, v in self.user_data.get("aliases", {}).items():
                    self._print_buf(f"  {k} = {v}")
                self._print_buf("Usage: alias name=command")

        elif cmd == "autostart":
            if len(parts) > 1:
                prog = " ".join(parts[1:])
                self.user_data["autostart"] = prog
                self.save_system()
                self._print_buf(f"Autostart set to: {prog}")
            else:
                self._print_buf(f"Current autostart: {self.user_data.get('autostart', 'None')}")
                self._print_buf("Usage: autostart <command> (or use 'autostart clear' to remove)")

        elif cmd == "notifications":
            self._clear_screen()
            print(f"📬 NOTIFICATION CENTER | {self.current_user}")
            print("=" * 40)
            notifs = self.user_data.get("notifications", [])
            if notifs == []:
                print("No recent notifications.")
            else:
                for n in notifs[:15]: print(n)
            print("=" * 40)
            input("Press Enter to return...")

        elif cmd == "menu":
            self.show_menu()
        elif cmd == "help":
            [self._print_buf(l) for l in self.help_text.split('\n') if l.strip()]
        elif cmd == "clear":
            self.screen_buffer.clear()
        elif cmd == "history":
            self._print_buf("--- Command History ---")
            for idx, h_cmd in enumerate(self.command_history[-10:], 1): self._print_buf(f"{idx}: {h_cmd}")
        elif cmd == "charge":
            self.battery = 100;
            self.set_notify("Battery fully charged ⚡")
        elif cmd == "time":
            self._print_buf(f"🕒 System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        elif cmd == "coins":
            self._print_buf(f"Diamond Coins: {self.user_data.get('coins', 0)}")
        elif cmd == "ping":
            self.run_ping(parts[1] if len(parts) > 1 else "127.0.0.1")
        elif cmd == "wget":
            if len(parts) > 1:
                self.run_wget(parts[1])
            else:
                self._print_buf("Usage: wget <url>")
        elif cmd == "ssh":
            if len(parts) > 1:
                self.run_ssh(parts[1])
            else:
                self._print_buf("Usage: ssh <user@ip>")
        elif cmd == "ps":
            self.run_ps()
        elif cmd == "kill":
            if len(parts) > 1:
                self.run_kill(parts[1], is_sudo)
            else:
                self._print_buf("Usage: kill <pid>")
        elif cmd == "settings":
            self.run_settings()
        elif cmd == "store":
            self.run_store()
        elif cmd == "files":
            self.run_files()
        elif cmd == "mail":
            self.run_mail()

        elif cmd == "cd":
            if len(parts) > 1:
                try:
                    os.chdir(parts[1]);
                    self.current_dir = os.getcwd();
                    self._print_buf(
                        f"Changed directory to {self.current_dir}")
                except Exception as e:
                    self._print_buf(f"Error: {e}")
            else:
                self._print_buf("Usage: cd <directory_name>")
        elif cmd == "mkdir":
            if len(parts) > 1:
                try:
                    os.mkdir(parts[1]);
                    self._print_buf(f"Directory '{parts[1]}' created.")
                except Exception as e:
                    self._print_buf(f"Error: {e}")
            else:
                self._print_buf("Usage: mkdir <directory_name>")
        elif cmd == "rm":
            if len(parts) > 1:
                target = parts[1]
                if target in ["dios_sys.json", "dios_sys_backup.json"] and not is_sudo and self.current_user != "root":
                    self._print_buf("rm: Permission denied.")
                else:
                    try:
                        shutil.rmtree(target) if os.path.isdir(target) else os.remove(target);
                        self._print_buf(
                            f"Deleted: {target}")
                    except Exception as e:
                        self._print_buf(f"Error: {e}")
            else:
                self._print_buf("Usage: rm <file_or_directory>")
        elif cmd == "cat":
            if len(parts) > 1:
                filepath = parts[1]
                if os.path.exists(filepath) and os.path.isfile(filepath):
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            self._print_buf(f"--- {filepath} ---")
                            for line in f.readlines(): self._print_buf(line.rstrip('\n'))
                            self._print_buf("-" * (len(filepath) + 8))
                    except Exception as e:
                        self._print_buf(f"Error reading file: {e}")
                else:
                    self._print_buf("File not found.")
            else:
                self._print_buf("Usage: cat <file>")

        elif cmd == "sysmon":
            self.run_sysmon()
        elif cmd == "update":
            self.run_update()
        elif cmd == "backup":
            self.backup_system()
        elif cmd == "restore":
            self.restore_system()
        elif cmd == "browser":
            self.run_browser()
        elif cmd == "calc":
            self.run_calculator()
        elif cmd == "messages":
            self.run_messages()
        elif cmd == "antivirus":
            self.run_antivirus()
        elif cmd == "construction":
            self.run_construction_sim()
        elif cmd == "hide_seek":
            self.play_hide_seek()
        elif cmd == "number_guess":
            self.play_number_guess()
        elif cmd == "edit":
            if len(parts) > 1:
                self.edit_file(parts[1], is_sudo)
            else:
                self._print_buf("Usage: edit <file>")
        else:
            if cmd_raw == "autostart" and len(parts) > 1 and parts[1] == "clear":
                self.user_data["autostart"] = ""
                self._print_buf("Autostart cleared.")
            else:
                self._print_unknown(cmd)

    # --- OS MAIN LOOP ---
    def render_desktop(self):
        self._clear_screen()
        cols, lines = 80, 60
        bg_col = WALLPAPERS.get(self.user_data.get("wallpaper", "magenta"), "\033[45m")
        reset_col = "\033[0m"

        print(f"{bg_col}{self.theme_prefix}═" * cols)
        print(f"{bg_col}{self.theme_prefix}" + f" ❖ DiOS {self.version} ❖ ".center(cols, " "))
        print(f"{bg_col}{self.theme_prefix}═" * cols)

        avail = lines - 8
        if len(self.screen_buffer) > avail: self.screen_buffer = self.screen_buffer[-avail:]

        for line in self.screen_buffer: print(f"{bg_col}{line}\033[K")
        for _ in range(avail - len(self.screen_buffer)): print(f"{bg_col}{' ' * cols}\033[K")

        notif = f" | {self.notification[0]}" if self.notification and time.time() - self.notification[1] < 4 else ""

        active = f" [{self.active_app}] " if self.active_app else ""
        tb_apps = f" ❖ [menu] | [settings] | [files] | [mail]{active}{notif} "
        sys_status = f"[{datetime.now().strftime('%H:%M')}] "

        tb = tb_apps.ljust(cols - len(sys_status))[:cols - len(sys_status)] + sys_status
        tt = THEMES.get(self.user_data.get("taskbar_color", "neon"), "")

        print(f"{bg_col}{tt}█{'▀' * (cols - 2)}█")
        print(f"{bg_col}{tt}█{tb}█{reset_col}")

    def run_os_loop(self):
        self.screen_buffer.append(f"Welcome to DiOS {self.version}. Type 'help' or 'menu'.")
        self.save_system()

        while self.current_state == "os":
            self.render_desktop()
            bg_col = WALLPAPERS.get(self.user_data.get("wallpaper", "magenta"), "\033[45m")

            user_display = f"{THEMES['warning']}root" if self.current_user == "root" else f"{THEMES['cyber']}{self.current_user}"
            prompt_symbol = "#" if self.current_user == "root" else ">"

            cmd_str = input(f"{bg_col}{user_display}@dios {prompt_symbol} {reset_col}{bg_col}").strip()

            if self.battery > 0 and random.random() < 0.25: self.battery -= 1

            if random.random() < 0.05:
                inbox = self.user_data.get("inbox", [{"id": 0}])
                new_id = max([m["id"] for m in inbox]) + 1 if inbox else 1
                if random.random() < 0.3:
                    self.user_data.setdefault("inbox", []).append(
                        {"id": new_id, "from": "System", "subject": "Daily Bonus!",
                         "body": "Here is your daily bonus of 15 Diamond Coins.",
                         "reward": 15, "read": False, "claimed": False})
                    self.set_notify("📧 New Mail: Daily Bonus!")
                else:
                    self.user_data.setdefault("inbox", []).append(
                        {"id": new_id, "from": "Unknown", "subject": "Buy cheap RAM!",
                         "body": "Download more RAM for free!\n(Fake spam message. Please delete.)",
                         "read": False})
                    self.set_notify("📧 New Mail received")

            if not cmd_str: continue

            if not self.command_history or self.command_history[-1] != cmd_str:
                self.command_history.append(cmd_str)

            self._print_buf(f"{self.current_user} {prompt_symbol} {cmd_str}")

            self.execute_command(cmd_str)
            self.save_system()

            if self.battery == 0:
                self._clear_screen()
                print("\n[!] BATTERY DEPLETED. SYSTEM SHUTTING DOWN...")
                time.sleep(2)
                self.current_state = "power_off"
                break

    # --- MAIN SYSTEM CONTROLLER ---
    def run(self):
        while self.power_on:
            if self.current_state == "boot":
                self.boot_sequence(target_state="os_login")
            elif self.current_state == "bios":
                self.run_bios()
            elif self.current_state == "os_login":
                if not self.load_system():
                    self.current_state = "install_step_1"
                else:
                    self.login()
                    if self.current_state != "os": continue
            elif self.current_state == "install_step_1":
                self.run_install_step_1()
            elif self.current_state == "install_reboot_1":
                self.boot_sequence(target_state="install_step_3", skip_bios=True)
            elif self.current_state == "install_step_3":
                self.run_install_step_3()
            elif self.current_state == "install_reboot_2":
                self.boot_sequence(target_state="install_step_4", skip_bios=True)
            elif self.current_state == "install_step_4":
                self.run_install_step_4()
            elif self.current_state == "install_reboot_3":
                self.boot_sequence(target_state="install_register", skip_bios=True)
            elif self.current_state == "install_register":
                self.run_install_register()
            elif self.current_state == "os":
                self.run_os_loop()
            elif self.current_state == "shutdown_to_admin":
                self.shutdown_sequence(target_state="boot_to_admin")
            elif self.current_state == "boot_to_admin":
                self.boot_sequence(target_state="admin")
            elif self.current_state == "admin":
                self.run_admin_panel()
            elif self.current_state == "boot_med_os":
                self.boot_med_os_sequence()
            elif self.current_state == "med_os":
                self.run_med_os_loop()
            elif self.current_state == "boot_edu_os":
                self.boot_edu_os_sequence()
            elif self.current_state == "edu_os":
                self.run_edu_os_loop()
            elif self.current_state == "shutdown_to_os":
                self.shutdown_sequence(target_state="boot")
            elif self.current_state == "power_off":
                self.shutdown_sequence(target_state="halt")
                self.power_on = False


reset_col = "\033[0m"

if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        print("\n[System safely powered down]")
        input("[Press Enter to close...]")
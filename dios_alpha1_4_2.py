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
from datetime import datetime

# Autocompletion and history (Unix/Linux and supported consoles)
try:
    import readline

    COMMANDS = ['menu', 'help', 'clear', 'settings', 'store', 'files', 'browser', 'calc', 'messages',
                'antivirus', 'edit', 'cat', 'construction', 'hide_seek', 'number_guess', 'shutdown', 'restart', 'exit',
                'update', 'backup', 'restore', 'cd', 'mkdir', 'rm', 'sysmon', 'history',
                'charge', 'lock', 'time', 'ping', 'wget', 'ps', 'kill', 'coins', 'whoami', 'su', 'sudo', 'mail', 'sh',
                'ssh', 'moryak.exe']


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
    "edu_gold": "\033[33m"
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
    "33f02bb445a11f1aeae9e34197fb5d1_1.jpg": "\033[42m",
    "23ae770445a11f1a16896dc08cef86a_2.jpg": "\033[44m",
    "ОСнова.png": "\033[45m"
}


class DiOS:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.user = "Guest"
        self.current_user = "Guest"
        self.version = "alpha 1.4.2"
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

        self.bg_tasks = {}
        self.notification = None

        self.user_data = {
            "name": "Guest",
            "country": "Unknown",
            "password": "",
            "theme": "cyber",
            "wallpaper": "magenta",
            "taskbar_color": "neon",
            "installed_apps": [],
            "coins": 0,
            "inbox": [{"id": 1, "from": "DiOS Team", "subject": "Welcome to 1.4.2!",
                       "body": "Welcome to DiOS alpha 1.4.2.\nEnjoy the new colorful UI, logos, and advanced installer!",
                       "read": False}]
        }
        self.theme_prefix = THEMES["cyber"]

        self.help_text = f"""
DiOS {self.version} Help:
--- System ---
menu      : open main system menu
help      : show this help menu
clear     : refresh screen
settings  : OS personalization, theme, sysinfo
store     : Diamond Store (Install Apps)
update    : Check for OS updates
sysmon    : System Resource Monitor (with ASCII graphs)
backup    : Backup system config
restore   : Restore system config
history   : Show command history
charge    : Plug in charger (Restore Battery)
lock      : Lock the system screen
time      : Show current system time/date
coins     : Check Diamond Coins balance

--- Permissions & Scripting ---
whoami    : Show current logged in user
su <user> : Switch user (e.g. su root)
sudo <cmd>: Execute command with admin privileges
sh <file> : Execute a .dsh script file
mail      : Open Mail Client

--- Network & Files ---
files       : File Explorer
cd <dir>    : Change directory
mkdir <dir> : Create directory
rm <target> : Remove file/directory
cat <file>  : Read text/ASCII file content
ping <host> : Send ICMP echo requests
wget <url>  : Download file
ssh <u@ip>  : Connect to external terminal servers

--- Processes ---
ps          : List running background processes
kill <pid>  : Terminate a specific process

--- Apps & Entertainment ---
browser      : DiOS Web Browser
calc         : Extended Calculator
messages     : Messenger
antivirus    : System security
edit <f>     : Text editor
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
        self.beep(800, 100)

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
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, indent=4)
            return True
        except Exception:
            return False

    def load_system(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)
                    for k, v in self.user_data.items():
                        if k not in saved_data: saved_data[k] = v
                    self.user_data = saved_data
                self.theme_prefix = THEMES.get(self.user_data.get("theme", "cyber"), THEMES["cyber"])
                self.user = self.user_data.get("name", "Guest")
                self.current_user = self.user
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
            self._print_buf("System restored from backup. Theme and settings applied.")
        else:
            self._print_buf("Error: No backup file found.")

    def run_update(self):
        self._print_buf(f"Checking for updates... Current version: {self.version}")
        time.sleep(1)
        server_version = "alpha 1.4.2"
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

    # --- INSTALLATION CHAIN ---
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
        print("Welcome to your new operating system. Let's create your account.")
        time.sleep(1)
        self.user_data["name"] = input("Enter your username: ").strip()
        self.user_data["country"] = input("Enter your country: ").strip()
        while True:
            pwd = input("Set password: ")
            if pwd == input("Confirm password: "):
                self.user_data["password"] = pwd
                break
            else:
                print("Passwords do not match. Try again.")
        self.user = self.user_data["name"]
        self.current_user = self.user
        self.save_system()
        print("Registration complete! Loading desktop...")
        time.sleep(2)
        self.current_state = "os"

    def login(self):
        self._clear_screen()
        print(f"{THEMES['cyber']}❖ DiOS {self.version} Login ❖{THEMES['standard']}")
        while True:
            name = input("Username: ")
            pwd = input("Password: ")
            if name == self.user_data["name"] and pwd == self.user_data["password"]:
                self.current_user = name
                self.set_notify(f"👋 Welcome, {name}")
                break
            elif name == "root" and pwd == self.root_password:
                self.current_user = "root"
                self.set_notify("🛡️ Logged in as ROOT")
                break
            print("Access Denied.\n")

    def lock_screen(self):
        self._clear_screen()
        print(f"{THEMES['warning']}🔒 SYSTEM LOCKED 🔒{THEMES['standard']}")
        print(f"User: {self.current_user}")
        while True:
            pwd = input("Enter password to unlock: ")
            if (self.current_user == self.user_data["name"] and pwd == self.user_data.get("password", "")) or \
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
                print(f"User: {self.user_data['name']}")
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
                print("1345           - Exit Med OS")
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
        tasks = ["Loading Curriculum", "Syncing Textbooks", "Preparing Virtual Labs", "Setting up Linguistics"]

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
            "Russian": {
                "Привет": "Hello",
                "Яблоко": "Apple",
                "Школа": "School",
                "Собака": "Dog",
                "Кошка": "Cat",
                "Книга": "Book",
                "Машина": "Car",
                "Дерево": "Tree",
                "Учитель": "Teacher",
                "Студент": "Student",
                "Время": "Time",
                "Друг": "Friend",
                "Город": "City",
                "Солнце": "Sun",
                "Я люблю программировать": "I love to program",
                "Как дела?": "How are you?",
                "Где находится библиотека?": "Where is the library?",
                "Мой любимый цвет - синий": "My favorite color is blue",
                "Доброе утро": "Good morning",
                "Спасибо за помощь": "Thank you for the help",
                "Я учусь в школе": "I study at school",
                "Какой сегодня день?": "What day is it today?"
            }
        }

        english_tasks = [
            ("Correct the grammar: 'He don't like apples.'", ["he doesn't like apples", "he does not like apples"]),
            ("What is the plural form of the word 'child'?", ["children"]),
            ("Fill in the blank: 'I have been waiting ___ 2 hours.' (for/since)", ["for"]),
            ("Correct the spelling: 'Acomodation'", ["accommodation"]),
            ("Which word is an adjective? (Run, Beautiful, Quickly)", ["beautiful"]),
            ("Translate to English: 'Всегда'", ["always"]),
            ("What is the past tense of 'Go'?", ["went"])
        ]

        physics_tasks = [
            ("What is the formula for force? (F = ?)", ["m*a", "ma", "m a"]),
            ("What is the speed of light in a vacuum? (approx, in km/s)", ["300000", "299792"]),
            ("What force pulls objects toward the Earth?", ["gravity"]),
            ("What unit is used to measure electrical resistance?", ["ohm", "ohms"])
        ]

        chemistry_tasks = [
            ("What is the chemical symbol for Gold?", ["au"]),
            ("What is the chemical formula for water?", ["h2o"]),
            ("What gas do plants absorb from the atmosphere?", ["co2", "carbon dioxide"]),
            ("What is the lightest element on the periodic table?", ["hydrogen"])
        ]

        history_tasks = [
            ("In what year did World War II end?", ["1945"]),
            ("Who was the first human in space? (Last name)", ["gagarin"]),
            ("What year was Rome supposedly founded? (BCE)", ["753"]),
            ("Who discovered America in 1492? (Last name)", ["columbus"])
        ]

        biology_tasks = [
            ("What is the powerhouse of the cell?", ["mitochondria", "mitochondrion"]),
            ("How many chromosomes are in a normal human cell?", ["46"]),
            ("What molecule carries genetic information?", ["dna", "deoxyribonucleic acid"]),
            ("What organ pumps blood through the human body?", ["heart"])
        ]

        geography_tasks = [
            ("What is the capital of Australia?", ["canberra"]),
            ("Which is the largest ocean on Earth?", ["pacific", "pacific ocean"]),
            ("On which continent is the Sahara Desert located?", ["africa"]),
            ("What is the longest river in the world?", ["nile", "amazon"])
        ]

        social_nature_tasks = [
            ("What is the basic unit of society?", ["family"]),
            ("What is the process by which water vapor turns into liquid? (Nature)", ["condensation"]),
            ("What type of economy is based on supply and demand?", ["market", "market economy"]),
            ("What do we call the envelope of gases surrounding the earth?", ["atmosphere"])
        ]

        informatics_tasks = [
            ("What does RAM stand for?", ["random access memory"]),
            ("What is 10 in binary? (Translate to decimal)", ["2"]),
            ("What Python function prints text to the console?", ["print", "print()"]),
            ("What does 'HTTP' stand for? (First word)", ["hypertext"])
        ]

        while self.current_state == "edu_os":
            self._clear_screen()
            print(f"{THEMES['edu_gold']}🎓 DIAMONDS EDUCATION OS 🎓")
            print(f"Student: {self.user} | Coins: {self.user_data['coins']}")
            print("Select Subject or Game:")
            print("[1] English (Native)      [2] Foreign Language (RU)")
            print("[3] Physics               [4] Chemistry")
            print("[5] History               [6] Biology")
            print("[7] Geography             [8] Social Studies / Nature")
            print("[9] Informatics           [10] Mathematics")
            print(f"{THEMES['neon']}[11] Mini-Games (Fun Learning!){THEMES['standard']}")
            print("[0] Exit to DiOS")
            print("-" * 50 + "\033[0m")

            cmd = input("EDU> ").strip()

            def ask_random_question(task_list, reward=10):
                q, answers = random.choice(task_list)
                ans = input(f"Question: {q}\nAnswer: ").strip().lower()
                if ans in [a.lower() for a in answers]:
                    print(f"Correct! +{reward} Coins");
                    self.user_data["coins"] += reward
                else:
                    print(f"Incorrect. Acceptable answers: {', '.join(answers)}")
                input("Press Enter...")

            if cmd == "0":
                print("Closing textbook...")
                time.sleep(1)
                self.current_state = "shutdown_to_os"
                break
            elif cmd == "1":
                print("--- English (Native) ---")
                ask_random_question(english_tasks)
            elif cmd == "2":
                print("--- Foreign Languages ---")
                langs = list(foreign_languages.keys())
                for i, l in enumerate(langs): print(f"[{i + 1}] {l}")
                l_cmd = input("Select language (or 0 to cancel): ")
                if l_cmd.isdigit() and 1 <= int(l_cmd) <= len(langs):
                    lang = langs[int(l_cmd) - 1]
                    word_ru, word_en = random.choice(list(foreign_languages[lang].items()))
                    ans = input(f"Translate '{word_ru}' to English: ").strip().lower()
                    clean_en = word_en.lower().replace("?", "").replace(".", "").replace("!", "")
                    clean_ans = ans.replace("?", "").replace(".", "").replace("!", "")
                    if clean_ans == clean_en:
                        print("Correct! +10 Coins");
                        self.user_data["coins"] += 10
                    else:
                        print(f"Incorrect. The correct translation is '{word_en}'.")
                input("Press Enter...")
            elif cmd == "3":
                print("--- Physics ---")
                ask_random_question(physics_tasks)
            elif cmd == "4":
                print("--- Chemistry ---")
                ask_random_question(chemistry_tasks)
            elif cmd == "5":
                print("--- History ---")
                ask_random_question(history_tasks)
            elif cmd == "6":
                print("--- Biology ---")
                ask_random_question(biology_tasks)
            elif cmd == "7":
                print("--- Geography ---")
                ask_random_question(geography_tasks)
            elif cmd == "8":
                print("--- Social Studies / Nature ---")
                ask_random_question(social_nature_tasks)
            elif cmd == "9":
                print("--- Informatics ---")
                ask_random_question(informatics_tasks)
            elif cmd == "10":
                print("--- Mathematics ---")
                a = random.randint(1, 50)
                b = random.randint(1, 50)
                op = random.choice(['+', '-', '*'])
                if op == '*':
                    a = random.randint(2, 12)
                    b = random.randint(2, 12)
                correct_ans = eval(f"{a} {op} {b}")
                ans = input(f"Solve: {a} {op} {b} = ?\nAnswer: ").strip()
                if ans == str(correct_ans):
                    print("Correct! +10 Coins");
                    self.user_data["coins"] += 10
                else:
                    print(f"Incorrect. The answer is {correct_ans}.")
                input("Press Enter...")
            elif cmd == "11":
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
                        ans = input(f"{a} + {b} = ? ").strip()
                        if ans == str(a + b):
                            score += 1
                    reward = score * 5
                    self.user_data["coins"] += reward
                    print(f"Sprint over! You got {score}/5 correct. Earned {reward} Coins.")
                    input("Press Enter...")
                elif g_cmd == "2":
                    words = ["algorithm", "biology", "geography", "history", "education", "terminal", "computer"]
                    word = random.choice(words)
                    scrambled = "".join(random.sample(word, len(word)))
                    print(f"Unscramble this word: {scrambled}")
                    ans = input("Your answer: ").strip().lower()
                    if ans == word:
                        print("Correct! +15 Coins");
                        self.user_data["coins"] += 15
                    else:
                        print(f"Incorrect! The word was: {word}")
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
        self._print_buf("-" * 30)
        self._print_buf("⚙️ SYSTEM COMMANDS:")
        self._print_buf("   - lock     (Lock Screen)")
        self._print_buf("   - exit     (Log Out)")
        self._print_buf("   - restart  (Reboot OS)")
        self._print_buf("   - shutdown (Power Off)")
        self._print_buf("=" * 30)

    def run_sysmon(self):
        self._clear_screen()
        print(f"{THEMES['matrix']}📊 SYSTEM MONITOR (Visual Mode){THEMES['standard']}")
        print("Press Ctrl+C to exit monitor")
        try:
            for _ in range(5):
                cpu = random.randint(5, 100)
                ram = random.randint(30, 100)
                disk = random.randint(1, 100)

                cpu_bar = "█" * (cpu // 5) + "-" * (20 - (cpu // 5))
                ram_bar = "█" * (ram // 5) + "-" * (20 - (ram // 5))

                sys.stdout.write(f"\rCPU: [{cpu_bar}] {cpu}% | RAM: [{ram_bar}] {ram}%  ")
                sys.stdout.flush()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        print("\nMonitor closed.")
        time.sleep(0.5)

    def run_ssh(self, target):
        if target not in self.fake_servers:
            self._print_buf(f"ssh: Could not resolve hostname {target}")
            self._print_unknown()
            return

        server = self.fake_servers[target]
        self._clear_screen()
        print(f"Connecting to {target}...")
        time.sleep(1)
        pwd = input(f"{target}'s password: ")

        if pwd == server["password"]:
            print(f"Access granted.\nWelcome to {target} Terminal.")
            while True:
                cmd = input(f"{THEMES['neon']}admin@{target.split('@')[1]}:~$ {THEMES['standard']}").strip()
                if cmd == "exit":
                    print("Connection closed.")
                    break
                elif cmd == "ls":
                    print("  ".join(server["files"].keys()))
                elif cmd.startswith("cat "):
                    filename = cmd.split(" ")[1]
                    if filename in server["files"]:
                        print(server["files"][filename])
                    else:
                        print("File not found.")
                else:
                    print(f"{cmd}: command not found")
        else:
            print("Access denied.")

    def run_ping(self, target):
        self._print_buf(f"Pinging {target} with 32 bytes of data:")
        for i in range(4):
            time.sleep(0.5)
            ms = random.randint(12, 105)
            self._print_buf(f"Reply from {target}: bytes=32 time={ms}ms TTL=54")
        self._print_buf(f"Ping statistics for {target}: Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)")

    def run_wget(self, url):
        self._print_buf(f"Resolving {url}...")
        time.sleep(0.5)
        self._print_buf(f"Connecting to {url}...")
        time.sleep(1)
        filename = url.split("/")[-1] if "/" in url else "downloaded_file.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(
                f"--- Downloaded Content ---\nSource: {url}\nWelcome to the DiOS Network!\nData successfully fetched.")
        self._print_buf(f"100% [===================>] Saved '{filename}'")

    def run_ps(self):
        self._print_buf("PID   TTY      TIME     CMD")
        for pid, cmd in self.processes.items():
            self._print_buf(f"{pid:<5} pts/0    00:00:01 {cmd}")

    def run_kill(self, pid_str, is_sudo=False):
        try:
            pid = int(pid_str)
            if pid == 1:
                self._print_buf("kill: Cannot kill kernel process (PID 1)")
            elif pid in self.processes:
                if pid < 200 and not is_sudo and self.current_user != "root":
                    self._print_buf("kill: Permission denied. Use sudo to kill system daemons.")
                else:
                    p_name = self.processes.pop(pid)
                    self._print_buf(f"Process {pid} ({p_name}) terminated.")
            else:
                self._print_buf(f"kill: ({pid}) - No such process")
        except ValueError:
            self._print_buf("Usage: kill <pid>")
            self._print_unknown()

    def run_files(self):
        self._print_buf(f"--- FILE EXPLORER: {self.current_dir} ---")
        try:
            for item in os.listdir(self.current_dir):
                icon = "📂" if os.path.isdir(os.path.join(self.current_dir, item)) else \
                    "🐍" if item.endswith('.py') else \
                        "📜" if item.endswith('.dsh') else \
                            "🎨" if item.endswith('.asc') else \
                                "⚙️" if item.endswith('.json') else "📄"
                self._print_buf(f"{icon} {item}")
        except Exception as e:
            self._print_buf(f"Error reading directory: {e}")

    def run_settings(self):
        while True:
            self._clear_screen()
            print("⚙️ SETTINGS\n[1] SysInfo [2] Theme [3] Wallpaper (Images)\n[Q] Exit")
            c = input("> ").strip().lower()
            if c == 'q':
                break
            elif c == '1':
                print(f"❖ OS: DiOS {self.version}")
                print(f"❖ User: {self.current_user}")
                print(f"❖ Battery Level: {self.battery}%")
                print(f"❖ Diamond Coins Balance: {self.user_data.get('coins', 0)}")
                input("Press Enter...")
            elif c == '2':
                tc = input("1:Standard 2:Matrix 3:Cyber 4:Hacker 5:Neon 6:Dark > ")
                colors = {"1": "standard", "2": "matrix", "3": "cyber", "4": "hacker", "5": "neon", "6": "dark"}
                if tc in colors:
                    self.user_data["theme"] = colors[tc]
                    self.theme_prefix = THEMES[colors[tc]]
                    self.save_system()
                    self.set_notify("Theme updated")
            elif c == '3':
                print("Available Backgrounds/Images:")
                print("1: Solid Black")
                print("2: Flowers (Meadow)")
                print("3: City Rain")
                print("4: Magenta")
                print("5: Purple")
                bg = input("Select Image > ")
                bg_map = {"1": "black", "2": "flowers", "3": "rain", "4": "magenta", "5": "purple"}
                if bg in bg_map:
                    self.user_data["wallpaper"] = bg_map[bg]
                    self.save_system()
                    self.set_notify("Wallpaper updated")

    def run_mail(self):
        while True:
            self._clear_screen()
            print(f"📧 DiOS MAIL CLIENT | Inbox: {len(self.user_data['inbox'])} messages")
            print("-" * 50)
            for mail in self.user_data["inbox"]:
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
                    print(f"--- Message {m_id} ---")
                    print(f"From: {mail_item['from']}\nSubject: {mail_item['subject']}\n")
                    print(mail_item['body'])
                    print("-" * 20)
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

    def play_hide_seek(self):
        if "hide_seek" not in self.user_data.get("installed_apps", []): return self._print_buf("Install from Store.")
        game_code = """from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
app = Ursina()
ground = Entity(model='plane', scale=(50, 1, 50), color=color.green, texture='white_cube', texture_scale=(50, 50), collider='box')
Sky()
for i in range(15): Entity(model='cube', color=color.gray, scale=(random.randint(2,6), random.randint(3,6), 1), position=(random.randint(-20,20), 2, random.randint(-20,20)), collider='box')
target = Entity(model='cube', color=color.red, scale=(1,2,1), position=(random.randint(-20,20), 1, random.randint(-20,20)), collider='box')
player = FirstPersonController()
text = Text(text="FIND RED CUBE! [ESC to Exit]", position=(0, 0.4), scale=2, color=color.yellow)
def update():
    if distance(player.position, target.position) < 2.5: text.text = "YOU WIN!"; text.color = color.green
app.run()"""
        try:
            with open("dios_hideseek_3d.py", "w", encoding="utf-8") as f:
                f.write(game_code)
            subprocess.run(["python", "dios_hideseek_3d.py"])
            self.user_data["coins"] += 20
            self._print_buf("You earned 20 Diamond Coins from Hide & Seek!")
        except Exception as e:
            print(f"Launch failed: {e}");
            input("Enter...")

    def play_number_guess(self):
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
                print(f"Correct! You guessed it in {attempts} attempts.")
                coins_earned = max(10, 50 - (attempts * 5))
                self.user_data["coins"] += coins_earned
                print(f"You earned {coins_earned} Diamond Coins! Total: {self.user_data['coins']}")
                input("Press Enter...")
                break

    def run_store(self):
        self._clear_screen()
        print(f"💎 DIAM STORE | Balance: {self.user_data['coins']} Coins")
        apps = {
            "1": ["Construction Sim", "construction", 0],
            "2": ["Hide In Seek 3D", "hide_seek", 0],
            "3": ["Number Guesser", "number_guess", 0],
            "4": ["Pro Network Tools", "net_tools", 50],
            "5": ["AI Assistant Core", "ai_core", 100]
        }
        for k, v in apps.items():
            status = "[Installed]" if v[1] in self.user_data['installed_apps'] else (
                f"[{v[2]} Coins]" if v[2] > 0 else "[Free]")
            print(f"[{k}] {v[0]} {status}")

        choice = input("\nSelect App ID to install/buy (or Q): ").strip()
        if choice in apps and apps[choice][1] not in self.user_data["installed_apps"]:
            app_cost = apps[choice][2]
            if self.user_data["coins"] >= app_cost:
                self.user_data["coins"] -= app_cost
                self.user_data["installed_apps"].append(apps[choice][1])
                self.save_system()
                self.set_notify(f"Installed: {apps[choice][0]}")
            else:
                print("Not enough Diamond Coins!")
                input("Press Enter...")

    def run_browser(self):
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

    def run_calculator(self):
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
                result = eval(expr, {"__builtins__": None}, safe_dict)
                print(f"Result: {result}")
            except Exception as e:
                print(f"Error: {e}")

    def run_construction_sim(self):
        if "construction" not in self.user_data.get("installed_apps", []): return self._print_buf("Install from Store.")
        pop = 0
        while pop < 20:
            cmd = input(f"Pop: {pop} | [H] Build (+5) [Q] Exit > ").lower()
            if cmd == 'h':
                pop += 5
            elif cmd == 'q':
                break

    def run_messages(self):
        for k, v in self.messenger_contacts.items(): print(f"[{k}] {v}")
        cmd = input("[+] Add  [Q] Exit > ")
        if cmd == '+': self.messenger_contacts[str(len(self.messenger_contacts) + 1)] = input("Name: ")

    def run_antivirus(self):
        if input("🛡️ [1] Scan [2] Clean > ") == "1": print("Clean!")

    def edit_file(self, filename, is_sudo=False):
        if filename in ["dios_sys.json", "dios_sys_backup.json"] and not is_sudo and self.current_user != "root":
            return self._print_buf("Permission denied. System file requires root/sudo access.")

        if not os.path.exists(filename): open(filename, "w").close()
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        while True:
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
        elif cmd == "moryak.exe":
            self._print_buf(f"{THEMES['warning']}>>> INITIATING PROJECT MORYAK...")
            self.render_desktop()
            for i in range(6, 0, -1):
                print(f"Rebooting to Education OS in {i} seconds...")
                self.beep(600, 100)
                time.sleep(1)
            self.current_state = "boot_edu_os"

        elif cmd == "sudo":
            if len(parts) < 2:
                self._print_buf("Usage: sudo <command>")
                return self._print_unknown()
            if self.current_user == "root":
                self.execute_command(" ".join(parts[1:]), is_sudo=True)
            else:
                pwd = input(f"[sudo] password for {self.current_user}: ")
                if pwd == self.user_data.get("password", "") or pwd == self.root_password:
                    self.execute_command(" ".join(parts[1:]), is_sudo=True)
                else:
                    self._print_buf("Sorry, try again.")
        elif cmd == "su":
            target_user = parts[1] if len(parts) > 1 else "root"
            if target_user == "root":
                pwd = input("Password: ")
                if pwd == self.root_password:
                    self.current_user = "root"
                    self._print_buf("Switched to root.")
                else:
                    self._print_buf("Authentication failure.")
            elif target_user == self.user_data["name"]:
                pwd = input("Password: ")
                if pwd == self.user_data.get("password", ""):
                    self.current_user = self.user_data["name"]
                    self._print_buf(f"Switched to {self.current_user}.")
                else:
                    self._print_buf("Authentication failure.")
            elif target_user == "Guest":
                self.current_user = "Guest"
                self._print_buf("Switched to Guest.")
            else:
                self._print_buf(f"su: user {target_user} does not exist")
        elif cmd == "whoami":
            self._print_buf(self.current_user)

        elif cmd == "sh":
            if len(parts) > 1:
                filepath = parts[1]
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            self._print_buf(f"> {line}")
                            self.execute_command(line, is_sudo=is_sudo)
                            self.render_desktop()
                            time.sleep(0.4)
                else:
                    self._print_buf(f"File not found: {filepath}")
            else:
                self._print_buf("Usage: sh <file.dsh>")
                self._print_unknown()

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
            self.battery = 100
            self.set_notify("Battery fully charged ⚡")
        elif cmd == "time":
            self._print_buf(f"🕒 System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        elif cmd == "coins":
            self._print_buf(f"Diamond Coins: {self.user_data['coins']}")
        elif cmd == "ping":
            self.run_ping(parts[1] if len(parts) > 1 else "127.0.0.1")
        elif cmd == "wget":
            if len(parts) > 1:
                self.run_wget(parts[1])
            else:
                self._print_buf("Usage: wget <url>")
                self._print_unknown()
        elif cmd == "ssh":
            if len(parts) > 1:
                self.run_ssh(parts[1])
            else:
                self._print_buf("Usage: ssh <user@ip>")
                self._print_unknown()
        elif cmd == "ps":
            self.run_ps()
        elif cmd == "kill":
            if len(parts) > 1:
                self.run_kill(parts[1], is_sudo)
            else:
                self._print_buf("Usage: kill <pid>")
                self._print_unknown()
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
                    os.chdir(parts[1])
                    self.current_dir = os.getcwd()
                    self._print_buf(f"Changed directory to {self.current_dir}")
                except Exception as e:
                    self._print_buf(f"Error: {e}")
            else:
                self._print_buf("Usage: cd <directory_name>")
                self._print_unknown()
        elif cmd == "mkdir":
            if len(parts) > 1:
                try:
                    os.mkdir(parts[1]);
                    self._print_buf(f"Directory '{parts[1]}' created.")
                except Exception as e:
                    self._print_buf(f"Error: {e}")
            else:
                self._print_buf("Usage: mkdir <directory_name>")
                self._print_unknown()
        elif cmd == "rm":
            if len(parts) > 1:
                target = parts[1]
                if target in ["dios_sys.json", "dios_sys_backup.json"] and not is_sudo and self.current_user != "root":
                    self._print_buf("rm: Permission denied.")
                else:
                    try:
                        shutil.rmtree(target) if os.path.isdir(target) else os.remove(target)
                        self._print_buf(f"Deleted: {target}")
                    except Exception as e:
                        self._print_buf(f"Error: {e}")
            else:
                self._print_buf("Usage: rm <file_or_directory>")
                self._print_unknown()
        elif cmd == "cat":
            if len(parts) > 1:
                filepath = parts[1]
                if os.path.exists(filepath) and os.path.isfile(filepath):
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            self._print_buf(f"--- {filepath} ---")
                            for line in f.readlines():
                                self._print_buf(line.rstrip('\n'))
                            self._print_buf("-" * (len(filepath) + 8))
                    except Exception as e:
                        self._print_buf(f"Error reading file: {e}")
                else:
                    self._print_buf("File not found.")
            else:
                self._print_buf("Usage: cat <file>")
                self._print_unknown()

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
                self._print_unknown()
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

        for line in self.screen_buffer:
            print(f"{bg_col}{line}\033[K")

        for _ in range(avail - len(self.screen_buffer)):
            print(f"{bg_col}{' ' * cols}\033[K")

        notif = f" | {self.notification[0]}" if self.notification and time.time() - self.notification[1] < 4 else ""

        # Cleaned up taskbar, stats moved to SysInfo settings
        tb_apps = f" ❖ [menu] | [settings] | [files] | [mail]{notif} "
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

            if self.battery > 0 and random.random() < 0.25:
                self.battery -= 1

            if random.random() < 0.05:
                new_id = max([m["id"] for m in self.user_data.get("inbox", [{"id": 0}])]) + 1
                if random.random() < 0.3:
                    self.user_data["inbox"].append({"id": new_id, "from": "System", "subject": "Daily Bonus!",
                                                    "body": "Here is your daily bonus of 15 Diamond Coins.",
                                                    "reward": 15, "read": False, "claimed": False})
                    self.set_notify("📧 New Mail: Daily Bonus!")
                else:
                    self.user_data["inbox"].append({"id": new_id, "from": "Unknown", "subject": "Buy cheap RAM!",
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
                    self.current_state = "os"

            # --- Install Chain ---
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
            # ---------------------

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
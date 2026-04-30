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
                'charge', 'lock', 'time', 'ping']


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
    "standard": "\033[0m",
    "matrix": "\033[0;32m",
    "cyber": "\033[0;36m",
    "warning": "\033[0;31m",
    "hacker": "\033[1;32m",
    "neon": "\033[1;35m",
    "med_cyan": "\033[1;36m",
    "med_white": "\033[1;37m",
    "med_red": "\033[1;31m"
}

BG_COLORS = {
    "black": "\033[40m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
    "white": "\033[47m"
}


class DiOS:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.user = "Guest"
        self.version = "alpha 1.3.4"
        self.config_file = "dios_sys.json"
        self.backup_file = "dios_sys_backup.json"
        self.messenger_contacts = {"1": "Alex (Friend)", "2": "CodeMind AI"}
        self.screen_buffer = []
        self.command_history = []
        self.battery = 100

        # System states
        self.power_on = True
        self.current_state = "boot"

        self.bg_tasks = {}
        self.notification = None

        self.user_data = {
            "name": "Guest",
            "country": "Unknown",
            "password": "",
            "theme": "standard",
            "bg_color": "black",
            "taskbar_color": "cyber",
            "installed_apps": []
        }
        self.theme_prefix = THEMES["standard"]

        self.help_text = f"""
DiOS {self.version} Help:
--- System ---
menu      : open main system menu
help      : show this help menu
clear     : refresh screen
settings  : OS personalization, theme, sysinfo
store     : Diamond Store (Install Apps)
update    : Check for OS updates
sysmon    : System Resource Monitor
backup    : Backup system config
restore   : Restore system config
history   : Show command history
charge    : Plug in charger (Restore Battery)
lock      : Lock the system screen
time      : Show current system time/date

--- Network & Files ---
files       : File Explorer (View files)
cd <dir>    : Change directory
mkdir <dir> : Create directory
rm <target> : Remove file/directory
cat <file>  : Read text file content (NEW)
ping <host> : Send ICMP echo requests

--- Apps & Social ---
browser   : DiOS Web Browser (Supports minimize)
calc      : Extended Calculator (Supports math logic)
messages  : Messenger
antivirus : System security
edit <f>  : Text editor

--- Entertainment ---
construction : City Builder
hide_seek    : 3D Hide & Seek (Ursina)
number_guess : Number Guesser Game (NEW)
"""

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
        self.screen_buffer.append(f"{self.theme_prefix}{text}\033[0m")

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
                self.theme_prefix = THEMES.get(self.user_data.get("theme", "standard"), THEMES["standard"])
                self.user = self.user_data.get("name", "Guest")
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
        server_version = "alpha 1.3.4"
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

    def boot_sequence(self, target_state="os"):
        self._clear_screen()
        print(f"{THEMES['cyber']}--- TGK BIOS v1.0.4 ---{THEMES['standard']}")
        print("Initializing Hardware...")
        self.beep(1200, 200)

        boot_time = 10.0
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

            if not entered_bios and self.check_f12():
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
                print("Unknown command.")
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
                print("dna_sequence   - Analyze DNA sequences (NEW)")
                print("vitals_monitor - Real-time patient telemetry (NEW)")
                print("1345           - Exit Med OS")
            elif cmd == "database":
                print("1. John Doe (ID: 8812) - Stable")
                print("2. Jane Smith (ID: 9921) - Needs Review")
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
                print(f"{THEMES['med_cyan']}Scan Complete. No anomalies detected in frontal lobe.\033[0m")
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
                print("Unknown medical command.")

    # --- INSTALLATION, LOGIN & LOCK ---
    def first_time_setup(self):
        self._clear_screen()
        print("⚡ DiOS INSTALLATION WIZARD ⚡")
        time.sleep(1)
        self.user_data["name"] = input("Enter your name: ").strip()
        self.user_data["country"] = input("Enter your country: ").strip()
        while True:
            pwd = input("Set password: ")
            if pwd == input("Confirm password: "):
                self.user_data["password"] = pwd
                break
        self.user = self.user_data["name"]
        self.save_system()
        time.sleep(1)

    def login(self):
        self._clear_screen()
        print(f"--- DiOS {self.version} Login ---")
        while True:
            name = input("Username: ")
            pwd = input("Password: ")
            if name == self.user_data["name"] and pwd == self.user_data["password"]:
                self.set_notify(f"👋 Welcome, {name}")
                break
            print("Access Denied.\n")

    def lock_screen(self):
        self._clear_screen()
        print(f"{THEMES['warning']}🔒 SYSTEM LOCKED 🔒{THEMES['standard']}")
        print(f"User: {self.user}")
        while True:
            pwd = input("Enter password to unlock: ")
            if pwd == self.user_data.get("password", ""):
                self.set_notify("System unlocked")
                break
            else:
                self.beep(400, 200)
                print("Access Denied.\n")

    # --- APPS & FUNCTIONS ---
    def show_menu(self):
        self._print_buf("=" * 30)
        self._print_buf(f"💠 DiOS MAIN MENU | User: {self.user}")
        self._print_buf("=" * 30)
        self._print_buf("📌 TASKBAR APPS:")
        self._print_buf("   - settings")
        self._print_buf("   - files")
        self._print_buf("   - browser")
        self._print_buf("   - store")
        self._print_buf("-" * 30)
        self._print_buf("⚙️ SYSTEM COMMANDS:")
        self._print_buf("   - lock     (Lock Screen)")
        self._print_buf("   - exit     (Log Out)")
        self._print_buf("   - restart  (Reboot OS)")
        self._print_buf("   - shutdown (Power Off)")
        self._print_buf("=" * 30)

    def run_sysmon(self):
        self._clear_screen()
        print(f"{THEMES['matrix']}📊 SYSTEM MONITOR (Simulated){THEMES['standard']}")
        print("Press Ctrl+C to exit monitor (or wait 5 cycles)")
        try:
            for _ in range(5):
                cpu = random.randint(5, 45)
                ram = random.randint(30, 80)
                disk = random.randint(1, 15)
                sys.stdout.write(f"\rCPU Usage: {cpu}% | RAM Usage: {ram}% | Disk I/O: {disk} MB/s   ")
                sys.stdout.flush()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        print("\nMonitor closed.")
        time.sleep(0.5)

    def run_ping(self, target):
        self._print_buf(f"Pinging {target} with 32 bytes of data:")
        for i in range(4):
            time.sleep(0.5)
            ms = random.randint(12, 105)
            self._print_buf(f"Reply from {target}: bytes=32 time={ms}ms TTL=54")
        self._print_buf(f"Ping statistics for {target}: Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)")

    def run_files(self):
        self._print_buf(f"--- FILE EXPLORER: {self.current_dir} ---")
        try:
            for item in os.listdir(self.current_dir):
                icon = "📂" if os.path.isdir(os.path.join(self.current_dir, item)) else "🐍" if item.endswith(
                    '.py') else "⚙️" if item.endswith('.json') else "📄"
                self._print_buf(f"{icon} {item}")
        except Exception as e:
            self._print_buf(f"Error reading directory: {e}")

    def run_settings(self):
        while True:
            self._clear_screen()
            print("⚙️ SETTINGS\n[1] SysInfo [2] Theme [3] Wallpaper [Q] Exit")
            c = input("> ").strip().lower()
            if c == 'q':
                break
            elif c == '1':
                print(f"OS: DiOS {self.version}");
                input("Enter...")
            elif c == '2':
                tc = input("1:Standard 2:Matrix 3:Cyber 4:Hacker 5:Neon > ")
                colors = {"1": "standard", "2": "matrix", "3": "cyber", "4": "hacker", "5": "neon"}
                if tc in colors:
                    self.user_data["theme"] = self.user_data["taskbar_color"] = colors[tc]
                    self.theme_prefix = THEMES[colors[tc]]
                    self.save_system()
                    self.set_notify("Theme updated")
            elif c == '3':
                bg = input("1:Black 2:Blue 3:Magenta 4:Cyan 5:White > ")
                bg_map = {"1": "black", "2": "blue", "3": "magenta", "4": "cyan", "5": "white"}
                if bg in bg_map:
                    self.user_data["bg_color"] = bg_map[bg]
                    self.save_system()
                    self.set_notify("Background updated")

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
                input("Press Enter...")
                break

    def run_store(self):
        self._clear_screen()
        print("💎 DIAMOND STORE")
        apps = {
            "1": ["Construction Sim", "construction"],
            "2": ["Hide In Seek 3D", "hide_seek"],
            "3": ["Number Guesser", "number_guess"]
        }
        for k, v in apps.items():
            print(f"[{k}] {v[0]} {'[Installed]' if v[1] in self.user_data['installed_apps'] else '[Free]'}")
        choice = input("\nSelect App ID (or Q): ").strip()
        if choice in apps and apps[choice][1] not in self.user_data["installed_apps"]:
            self.user_data["installed_apps"].append(apps[choice][1])
            self.save_system()
            self.set_notify(f"Installed: {apps[choice][0]}")

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
        print("Tips: use math functions like sin(0), pi, sqrt(16), log(10)")

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
            if input(f"Pop: {pop} | [H] Build (+5) [Q] Exit > ").lower() == 'h':
                pop += 5
            elif input == 'q':
                break

    def run_messages(self):
        for k, v in self.messenger_contacts.items(): print(f"[{k}] {v}")
        if input("[+] Add  [Q] Exit > ") == '+': self.messenger_contacts[str(len(self.messenger_contacts) + 1)] = input(
            "Name: ")

    def run_antivirus(self):
        if input("🛡️ [1] Scan [2] Clean > ") == "1": print("Clean!")

    def edit_file(self, filename):
        if not os.path.exists(filename): open(filename, "w").close()
        with open(filename, "r") as f:
            lines = f.readlines()
        while True:
            for i, l in enumerate(lines): print(f"{i + 1}: {l.strip()}")
            cmd = input("[s] save | [a] add | [q] exit > ").strip().lower()
            if cmd == 'q':
                break
            elif cmd == 's':
                with open(filename, "w") as f:
                    f.writelines(lines)
                self.set_notify("File saved")
                break
            elif cmd == 'a':
                lines.append(input("New line: ") + "\n")

    # --- OS MAIN LOOP ---
    def render_desktop(self):
        self._clear_screen()
        cols, lines = shutil.get_terminal_size((80, 24))
        bg_col = BG_COLORS.get(self.user_data.get("bg_color", "black"), "")
        reset_col = "\033[0m"

        print(f"{bg_col}{THEMES[self.user_data['theme']]}═" * cols)
        print(f" DiOS {self.version} ".center(cols, " "))
        print("═" * cols + reset_col)

        avail = lines - 6
        if len(self.screen_buffer) > avail: self.screen_buffer = self.screen_buffer[-avail:]
        for line in self.screen_buffer: print(f"{bg_col}{line}{reset_col}")
        for _ in range(avail - len(self.screen_buffer)): print(f"{bg_col}{' ' * cols}{reset_col}")

        # Taskbar Generation
        notif = f" | {self.notification[0]}" if self.notification and time.time() - self.notification[1] < 4 else ""

        tb_apps = f" [menu] | [settings] | [files] | [browser]{notif} "
        sys_status = f"[Bat: {self.battery}%] [{datetime.now().strftime('%H:%M')}] "

        tb = tb_apps.ljust(cols - len(sys_status))[:cols - len(sys_status)] + sys_status
        tt = THEMES.get(self.user_data.get("taskbar_color", "cyber"), "")

        print(f"{tt}█{'▀' * (cols - 2)}█{reset_col}\n{tt}█{tb}█{reset_col}")

    def run_os_loop(self):
        self.screen_buffer.append(f"Welcome to DiOS {self.version}. Type 'help' or 'menu'.")
        self.save_system()

        while self.current_state == "os":
            self.render_desktop()
            cmd_str = input(f"{self.theme_prefix}Command > \033[0m").strip()

            if self.battery > 0 and random.random() < 0.25:
                self.battery -= 1

            if not cmd_str: continue

            if not self.command_history or self.command_history[-1] != cmd_str:
                self.command_history.append(cmd_str)

            parts = shlex.split(cmd_str)
            cmd = parts[0].lower()
            self._print_buf(f"{self.user} > {cmd_str}")

            if cmd == "1191":
                self.current_state = "shutdown_to_admin"
                break
            elif cmd == "shutdown":
                self.current_state = "power_off"
                break
            elif cmd == "restart":
                self.current_state = "shutdown_to_os"
                break
            elif cmd == "lock":
                self.lock_screen()
            elif cmd == "exit":
                self.current_state = "os_login"
                break
            elif cmd == "menu":
                self.show_menu()
            elif cmd == "help":
                [self._print_buf(l) for l in self.help_text.split('\n') if l.strip()]
            elif cmd == "clear":
                self.screen_buffer.clear()
            elif cmd == "history":
                self._print_buf("--- Command History ---")
                for idx, h_cmd in enumerate(self.command_history[-10:], 1):
                    self._print_buf(f"{idx}: {h_cmd}")
            elif cmd == "charge":
                self.battery = 100
                self.set_notify("Battery fully charged ⚡")
            elif cmd == "time":
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self._print_buf(f"🕒 System Time: {current_time}")
            elif cmd == "ping":
                target = parts[1] if len(parts) > 1 else "127.0.0.1"
                self.run_ping(target)
            elif cmd == "settings":
                self.run_settings()
            elif cmd == "store":
                self.run_store()
            elif cmd == "files":
                self.run_files()
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
            elif cmd == "mkdir":
                if len(parts) > 1:
                    try:
                        os.mkdir(parts[1])
                        self._print_buf(f"Directory '{parts[1]}' created successfully.")
                    except Exception as e:
                        self._print_buf(f"Error: {e}")
                else:
                    self._print_buf("Usage: mkdir <directory_name>")
            elif cmd == "rm":
                if len(parts) > 1:
                    try:
                        target = parts[1]
                        if os.path.isdir(target):
                            shutil.rmtree(target)
                        else:
                            os.remove(target)
                        self._print_buf(f"Deleted: {target}")
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
                                for line in f.readlines():
                                    self._print_buf(line.strip())
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
                self.edit_file(parts[1]) if len(parts) > 1 else self._print_buf("Usage: edit <file>")
            else:
                self._print_buf(f"Unknown command: {cmd}")
                self.beep(400, 250)

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
                    self.first_time_setup()
                else:
                    self.login()
                self.current_state = "os"
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
            elif self.current_state == "shutdown_to_os":
                self.shutdown_sequence(target_state="boot")
            elif self.current_state == "power_off":
                self.shutdown_sequence(target_state="halt")
                self.power_on = False


if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        print("\n[System safely powered down]")
        input("[Press Enter to close...]")
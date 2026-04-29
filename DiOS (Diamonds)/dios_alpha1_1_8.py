import os
import platform
import shlex
import time
import shutil
import random
import json
from datetime import datetime

# Опциональная загрузка psutil
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Опциональная загрузка pyperclip для копирования кода
try:
    import pyperclip

    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


class DiOS:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.user = "Guest"
        self.running = True
        self.version = "alpha 1.1.8"
        self.command_history = []
        self.config_file = "dios_sys.json"
        self.users_db = {}

        # Динамический список контактов для мессенджера (сохраняется в рамках сессии)
        self.messenger_contacts = {
            "1": "Alex (Friend)",
            "2": "CodeMind AI (Developer Bot)"
        }

        self.help_text = f"""
DiOS {self.version} Help:
--- System ---
help      : show this help menu
clear     : clear screen
refresh   : refresh the console screen
date      : show current date and time
antivirus : launch DiOS Antivirus

--- Social & AI ---
messages  : DiOS Messenger (Chat with Friends or AI)
gallery   : View media files (Photos, Videos, Audio)

--- Games ---
games     : list available games
guess     : play 'Guess the Number'
math      : play 'Math Quiz'

--- File System ---
ls, cd, pwd, mkdir, rm, touch, cat, write
"""

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_system_data(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.users_db = data.get("users", {})
                return True
            except:
                return False
        return False

    def save_system_data(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({"users": self.users_db}, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def first_time_setup(self):
        self._clear_screen()
        print(f"=== Welcome to DiOS {self.version} Setup ===")
        print("Installing system core...")
        time.sleep(1)
        print("Setting up AI Modules and Media Drivers...")
        time.sleep(1)

        new_user = input("Enter username: ").strip()
        country = input("Your country: ").strip()
        print("\nFor better protection, use special characters.")
        password = input("Create password: ")

        self.users_db[new_user] = {
            "password": password,
            "country": country,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_system_data()
        print("\nInstallation complete. Rebooting...")
        time.sleep(1.5)

    def login_screen(self):
        self._clear_screen()
        print(f"--- DiOS {self.version} Login ---")
        while True:
            req_user = input("Username: ").strip()
            if req_user in self.users_db:
                req_pwd = input("Password: ")
                if req_pwd == self.users_db[req_user]["password"]:
                    self.user = req_user
                    break
                else:
                    print("Wrong password.")
            else:
                print("User not found.")

    def run_messages(self):
        self._clear_screen()
        print("💬 DiOS Messenger")
        print("-----------------")

        while True:
            print("\nContacts:")
            for k, v in self.messenger_contacts.items():
                print(f"[{k}] {v}")
            print("[+] Add new contact")
            print("[Q] Exit Messenger")

            choice = input("\nSelect action or contact: ").strip().lower()
            if choice == "q": break

            if choice == "+":
                new_name = input("Enter contact name: ").strip()
                if new_name:
                    new_id = str(len(self.messenger_contacts) + 1)
                    self.messenger_contacts[new_id] = new_name
                    print(f"✅ Contact '{new_name}' added successfully!")
                continue

            if choice == "1":
                print("\n[Alex]: Привет! Как тебе новая версия DiOS? ИИ реально тащит!")
                input(f"[{self.user}]: ")
                print("[Alex]: Согласен! Ладно, я погнал кодить.")
                input(f"[{self.user}]: ")
                print("[Alex]: Ну давай пока, sorry what the Russian, I`m Alexey.")

            elif choice == "2":
                print("\n--- CodeMind AI Online ---")
                print("Ask me to write a code (e.g., 'write python hello world')")
                prompt = input("Prompt: ").lower()
                print("\n[CodeMind AI]: Analyzing request...")
                time.sleep(1.5)

            elif choice == "3":
                print("\n[Artemiy KlADiamond Developer]: Hello, what can I do for you?")
                input(f"[{self.user}]: ")
                time.sleep(5)
                print("[Artemiy KlADiamond Developer]: We can do anything, wait for the update and you'll find out, goodbye")


                generated_code = ""
                file_ext = ""

                if "python" in prompt:
                    generated_code = "print('Hello from DiOS AI!')\n# Generated by CodeMind"
                    file_ext = ".py"
                    print(f"```python\n{generated_code}\n```")
                elif "c++" in prompt:
                    generated_code = "#include <iostream>\nint main() { std::cout << \"DiOS Power\"; return 0; }"
                    file_ext = ".cpp"
                    print(f"```cpp\n{generated_code}\n```")
                else:
                    print("I can help you with Python or C++. Just ask!")
                    continue

                print("\n[CodeMind AI]: What would you like to do with this code?")
                print("1. Save to file")
                if CLIPBOARD_AVAILABLE: print("2. Copy to clipboard")
                print("3. Nothing")

                action = input("Choice: ").strip()
                if action == "1":
                    filename = f"ai_script{file_ext}"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(generated_code)
                    print(f"✅ Code saved to {filename} in your current directory.")
                elif action == "2" and CLIPBOARD_AVAILABLE:
                    pyperclip.copy(generated_code)
                    print("✅ Code copied to clipboard!")

            elif choice in self.messenger_contacts:
                print(f"\n[{self.messenger_contacts[choice]}]: Hi there! Currently away from keyboard.")
                input(f"[{self.user}]: ")
            else:
                print("Unknown contact.")

    def run_gallery(self):
        self._clear_screen()
        print("🖼️  DiOS Media Gallery")
        files = {
            "1": "cat_photo.jpg",
            "2": "flower_garden.png",
            "3": "wild_bears_clip.mp4",
            "4": "system_startup.wav"
        }

        while True:
            print("\nFiles in /home/media:")
            for k, v in files.items(): print(f"[{k}] {v}")
            print("[Q] Close Gallery")

            choice = input("\nOpen file: ").strip().lower()
            if choice == "q": break

            if choice == "1":
                print("\n[Displaying cat_photo.jpg]")
                print("  ^._.^  \n (  > < ) \n  v___v ")
                print("Description: A cute ASCII cat looking at you.")
            elif choice == "2":
                print("\n[Displaying flower_garden.png]")
                print("  _(_)_  \n (_)@(_) \n   (_)   ")
                print("Description: A beautiful digital flower.")
            elif choice == "3":
                print("\n[Playing wild_bears_clip.mp4]")
                for i in range(3):
                    print(f"Frame {i + 1}: Bear is eating honey...")
                    time.sleep(0.7)
                print("Video finished.")
            elif choice == "4":
                print("\n[Playing system_startup.wav]")
                print("♪ Beep-Boop-Bip! ♪")
            else:
                print("File not found.")

    def run_antivirus(self):
        self._clear_screen()
        print("🛡️  DiOS Antivirus")
        print("[1] Scan  [2] Clean Cache  [3] Exit")
        c = input("> ")
        if c == "1":
            print("Scanning...");
            time.sleep(2);
            print("Clean!")
        elif c == "2":
            print("Cache cleared.");
            time.sleep(1)

    def trigger_bsod(self):
        self._clear_screen()
        print("\n:( SYSTEM CRASH\nError: CRITICAL_PROCESS_DIED")
        input("Press Enter to try recovery...")
        self.run()

    def play_guess(self):
        target = random.randint(1, 100)
        print("--- Guess the Number (1-100) ---")
        print("Type 'q' to quit.")
        while True:
            ans = input("Your guess: ").strip()
            if ans.lower() == 'q':
                print("Game aborted.")
                break
            if not ans.isdigit():
                print("Please enter a valid number.")
                continue
            ans = int(ans)
            if ans < target:
                print("Higher!")
            elif ans > target:
                print("Lower!")
            else:
                print(f"Correct! The number was {target}. You win!")
                break

    def play_math(self):
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        print(f"--- Math Quiz ---")
        ans = input(f"What is {a} + {b}? ").strip()
        if ans.isdigit() and int(ans) == (a + b):
            print("Correct! Good job.")
        else:
            print(f"Wrong! The correct answer is {a + b}.")

    def shutdown_sequence(self):
        print("\nInitiating shutdown sequence...")
        time.sleep(0.5)
        print("Saving user session data...")
        self.save_system_data()
        time.sleep(0.5)
        print("Stopping DiOS Kernel...")
        time.sleep(0.5)
        print("Powering off...")
        time.sleep(0.8)
        self._clear_screen()

    def display_taskbar(self):
        now = datetime.now().strftime("%H:%M:%S")
        print(f"\n[ 1:Sysinfo | 2:Restart | 3:Shutdown ] {'=' * 30} [ Time: {now} ]")

    def run(self):
        if not self.load_system_data(): self.first_time_setup()
        self.login_screen()
        self._clear_screen()

        print(f"Welcome to DiOS {self.version}, {self.user}!")
        # Подсказка для пользователя при входе
        print("If you don't know how to spell this command, then enter help for a detailed list of commands.")

        while self.running:
            self.display_taskbar()
            cmd = input(f"{self.user} > ").strip().lower()
            if not cmd: continue
            self.command_history.append(cmd)

            if cmd == "help":
                print(self.help_text)
            elif cmd in ["clear", "refresh"]:
                self._clear_screen()
            elif cmd == "messages":
                self.run_messages()
            elif cmd == "gallery":
                self.run_gallery()
            elif cmd == "antivirus":
                self.run_antivirus()

            # Игры из версии 1.1.4
            elif cmd == "games":
                print("Available Games: 'guess', 'math'")
            elif cmd == "guess":
                self.play_guess()
            elif cmd == "math":
                self.play_math()

            elif cmd == "1":
                print(f"DiOS v{self.version} on {platform.system()}")
            elif cmd == "2":
                print("Restarting...");
                time.sleep(1);
                self.run()
            elif cmd in ["3", "shutdown", "exit"]:
                self.shutdown_sequence()
                self.running = False
            elif cmd == "crash":
                self.trigger_bsod()
            elif cmd == "ls":
                print("messages/  gallery/  games/  dios_sys.json")
            else:
                print(f"Unknown command: {cmd}")
                print("If you don't know how to spell this command, then enter help for a detailed list of commands.")


if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        if CLIPBOARD_AVAILABLE is False:
            pass  # pyperclip is just optional
        print("\n[System successfully powered down]")
        input("[Program has finished its work. Press Enter to close the window...]")
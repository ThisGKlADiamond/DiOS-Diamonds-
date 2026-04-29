import os
import platform
import shlex
import time
import shutil
import random
import json
from datetime import datetime

# Optional psutil for system metrics
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Optional pyperclip for AI code copying
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
        self.version = "alpha 1.1.9"
        self.command_history = []
        self.config_file = "dios_sys.json"
        self.users_db = {}
        self.messenger_contacts = {"1": "Alex (Friend)", "2": "CodeMind AI"}

        self.help_text = f"""
DiOS {self.version} Help:
--- System ---
help      : show this help menu
clear     : clear screen / refresh
calc      : launch Advanced Calculator (Standard/Programmer)
antivirus : launch DiOS Antivirus

--- Social & AI ---
messages  : DiOS Messenger (Fixed Exit Bug)
gallery   : Media Gallery (Photos/Videos)

--- Entertainment ---
games     : list all games
construction : 'Construction of Villages and Towns' (New!)
hide_seek : 'Hide In Seek' 3D-Text Game (New!)

--- File System ---
ls, cd, pwd, mkdir, rm, touch, cat, write
"""

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # --- ADVANCED CALCULATOR ---
    def run_calculator(self):
        self._clear_screen()
        print("🔢 DiOS Advanced Calculator")
        print("Modes: [1] Standard  [2] Programmer  [Q] Exit")
        mode = input("Select Mode: ").strip().lower()

        if mode == "1":
            print("\n-- Standard Mode (Type 'q' to go back) --")
            while True:
                expr = input("Calc > ").strip()
                if expr.lower() == 'q': break
                try:
                    # Safety check for basic math
                    allowed = "0123456789+-*/(). "
                    if all(c in allowed for c in expr):
                        print(f"Result: {eval(expr)}")
                    else:
                        print("Error: Invalid characters.")
                except:
                    print("Error: Invalid expression.")

        elif mode == "2":
            print("\n-- Programmer Mode (Dec/Hex/Bin) --")
            while True:
                val = input("Enter Decimal Number (or 'q'): ").strip()
                if val.lower() == 'q': break
                if val.isdigit():
                    n = int(val)
                    print(f"DEC: {n}")
                    print(f"HEX: {hex(n).upper()}")
                    print(f"BIN: {bin(n)}")
                else:
                    print("Error: Enter a whole number.")

    # --- HIDE IN SEEK (3D Simulation) ---
    def play_hide_seek(self):
        self._clear_screen()
        print("🙈 Hide In Seek: 3D Text Edition")
        print("Mode: [1] vs AI  [2] Local Multiplayer")
        mode = input("Choice: ")

        rooms = ["Kitchen", "Basement", "Attic", "Garden Shed", "Master Bedroom"]

        if mode == "1":
            print("\nAI is hiding...")
            time.sleep(1.5)
            ai_pos = random.choice(rooms)
            print("AI: 'I'm hidden! You have 2 tries to find me.'")
            for i in range(2):
                print(f"\nLocations: {', '.join(rooms)}")
                seek = input(f"Try {i + 1} - Where are you looking? ").title()
                if seek == ai_pos:
                    print(f"🎉 Found it! The AI was in the {ai_pos}!")
                    return
                else:
                    print("Nothing here...")
            print(f"Game Over! AI was in the {ai_pos}.")

        elif mode == "2":
            p1 = input("Player 1 Name: ")
            p2 = input("Player 2 Name: ")
            print(f"\n{p1}, close your eyes! {p2}, choose a location.")
            print(f"Rooms: {', '.join(rooms)}")
            p2_pos = input(f"{p2} > ").title()
            self._clear_screen()
            print(f"{p1}, it's time to search!")
            seek = input(f"Search location: ").title()
            if seek == p2_pos:
                print(f"Found you, {p2}!")
            else:
                print(f"Missed! {p2} was in the {p2_pos}.")
        input("\nPress Enter...")

    # --- CONSTRUCTION SIMULATOR (TGK DiamondCraft Studios) ---
    def run_construction_sim(self):
        self._clear_screen()
        print("⚡ TGK DiamondCraft Studios Presents:")
        print("🏗️  Construction of Villages and Towns")
        print("-" * 40)
        print("[1] New Game  [2] Information  [Q] Exit")

        choice = input("> ").lower()
        if choice == "2":
            print("\nIn the year 2026, TGK DiamondCraft Studios unveiled 'Construction of villages and towns'.")
            print("This pioneering urban planning simulator constitutes a significant advancement...")
            input("Press Enter...")
            self.run_construction_sim()

        elif choice == "1":
            self._clear_screen()
            print("Location: Sunny Valley (Natural Paradise)")
            print("Guide: 'This area is just a fire for development! Huge prospects!'")
            print("\nStep 1: Analyze the territory.")
            input("[Press Enter to Research Area...]")
            print("Analysis: Soil is stable. Water access is good. Perfect for a village.")

            pop = 0
            while pop < 20:
                print(f"\nCurrent Population: {pop} people")
                print("Options: [H] Place House (+5 pop)  [S] Settings [Q] Exit Game")
                act = input("Action: ").lower()
                if act == 'h':
                    print("🏗️  Building...")
                    time.sleep(1)
                    pop += 5
                    print(f"New residents moved in! Total: {pop}")
                elif act == 'q':
                    break

            if pop >= 20:
                print("\n🏆 Congratulations! Your village has become a small town!")
            input("Returning to menu...")

    # --- MESSENGER (FIXED) ---
    def run_messages(self):
        self._clear_screen()
        print("💬 DiOS Messenger v1.1.9")
        while True:
            print("\nContacts:")
            for k, v in self.messenger_contacts.items(): print(f"[{k}] {v}")
            print("[+] Add Contact  [Q] Exit")

            choice = input("\nSelect: ").strip().lower()
            if choice == 'q': break

            if choice == '+':
                name = input("Enter Name: ")
                self.messenger_contacts[str(len(self.messenger_contacts) + 1)] = name
                print("Contact Added!")
            elif choice == '2':
                print("\n[CodeMind]: Ask me for Python/C++ code!")
                req = input("You: ")
                print("AI: Generating...")
                time.sleep(1)
                print("```python\nprint('Simulation Complete')\n```")
            elif choice in self.messenger_contacts:
                print(f"\n[{self.messenger_contacts[choice]}]: Hello! I'm busy right now.")
                input("You: ")
            else:
                print("Invalid option.")

    def run_antivirus(self):
        self._clear_screen()
        print("🛡️  DiOS Antivirus System App")
        print("[1] Deep Scan [2] Delete Cache [Q] Exit")
        c = input("> ").lower()
        if c == "1":
            print("Scanning...");
            time.sleep(2);
            print("System is Clean!")
        elif c == "2":
            print("Cache deleted (50MB saved).")
        input("Press Enter...")

    def boot_sequence(self):
        self._clear_screen()
        print("Initializing DiOS BIOS 2026...")
        time.sleep(0.5)
        print("Checking File System... OK")
        time.sleep(0.5)
        print("Mounting TGK_DiamondCraft_Drivers... Done.")
        time.sleep(0.5)

    def display_taskbar(self):
        now = datetime.now().strftime("%H:%M:%S")
        print(f"\n[ 1:Sysinfo | 2:Restart | 3:Shutdown ] {'=' * 30} [ {now} ]")

    def execute_command(self, cmd):
        if cmd == "help":
            print(self.help_text)
        elif cmd in ["clear", "refresh"]:
            self._clear_screen()
        elif cmd == "calc":
            self.run_calculator()
        elif cmd == "messages":
            self.run_messages()
        elif cmd == "hide_seek":
            self.play_hide_seek()
        elif cmd == "construction":
            self.run_construction_sim()
        elif cmd == "antivirus":
            self.run_antivirus()
        elif cmd == "games":
            print("Games: 'guess', 'math', 'hide_seek', 'construction'")
        elif cmd == "guess":
            self.play_guess()  # From 1.1.7
        elif cmd == "math":
            self.play_math()  # From 1.1.7
        elif cmd == "1":
            print(f"DiOS {self.version} | Host: {platform.node()}")
        elif cmd == "2":
            self.run()
        elif cmd == "3":
            print("Shutting down...");
            time.sleep(1);
            self.running = False
        else:
            print(f"Unknown command: {cmd}. Type 'help'.")

    def run(self):
        self.boot_sequence()
        print(f"Welcome to DiOS {self.version}")
        print("If you don't know how to spell this command, then enter help for a detailed list.")

        while self.running:
            self.display_taskbar()
            cmd = input(f"{self.user} > ").strip().lower()
            if not cmd: continue
            self.execute_command(cmd)


if __name__ == "__main__":
    try:
        dios = DiOS()
        dios.run()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        print("\n[System successfully powered down]")
        input("[Press Enter to close the window...]")
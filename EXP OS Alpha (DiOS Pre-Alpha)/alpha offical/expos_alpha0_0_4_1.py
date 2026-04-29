import os
import sys
import time
import random
import logging
import shlex

# Logging setup
logging.basicConfig(filename='.expos_log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ExpOS:
    def __init__(self, safe_mode=False):
        self.version = "alpha 0.0.4.1"
        self.safe_mode = safe_mode
        self.is_running = True
        self.current_user = "guest"
        self.ps1 = f"[{self.current_user}@expos]/>"
        self.history = []
        self.aliases = {}
        self.theme_colors = {"dark": "\033[0m", "light": "\033[1;30m\033[47m", "reset": "\033[0m"}
        self.current_theme = "dark"

        # System state variables
        self.crash_count = 0
        self.is_corrupted = False

        self.config = {"password": "root", "require_auth": True}
        self.init_vfs()

    def init_vfs(self):
        """Initializes or restores the Virtual File System"""
        self.vfs = {
            "README.exp": {"content": "Welcome to EXP OS!\nAvailable commands: help, menu, ping, wget, ps, df, view.",
                           "perms": "644"},
            "test.txt": {"content": "Line 1\nLine 2\nERROR: test\nSuccess", "perms": "644"}
        }

    def boot(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        logos = [
            "  _____  __  __  ____    ___   ____  \n | ____| \\ \\/ / |  _ \\  / _ \\ / ___| \n |  _|    \\  /  | |_) || | | |\\___ \\ \n | |___   /  \\  |  __/ | |_| | ___) |\n |_____| /_/\\_\\ |_|     \\___/ |____/ \n",
            " [ E X P   O S   v.0.0.4.1 ] \n    /// ALIVE AND KICKING ///"
        ]
        print(self.theme_colors[self.current_theme])
        print(random.choice(logos))
        print(f"Booting EXP OS {self.version}...")

        # Boot animation
        for i in range(101):
            sys.stdout.write(
                f"\r[CPU: {random.randint(5, 30)}% | BAT: 98%] Loading modules: [{'#' * (i // 10)}{'.' * (10 - i // 10)}] {i}%")
            sys.stdout.flush()
            time.sleep(0.01)
        print("\nSystem ready.\n")
        logging.info("System booted successfully.")

        if self.config["require_auth"] and not self.safe_mode:
            attempts = 3
            while attempts > 0:
                pwd = input("Enter password (default 'root'): ")
                if pwd == self.config["password"]:
                    self.current_user = "admin"
                    self.ps1 = f"[{self.current_user}@expos]/>"
                    print("Access granted.")
                    break
                else:
                    attempts -= 1
                    print(f"Incorrect password. Attempts remaining: {attempts}")
            if attempts == 0:
                print("System locked.")
                sys.exit()

    def run(self):
        self.boot()
        while self.is_running:
            # Corruption Check
            if self.is_corrupted:
                print("\nThe OS cannot work normally, as all its files are corrupted, run system recovery or exit.")
                recovery_cmd = input("Type 'recovery' or 'exit': ").strip().lower()
                if recovery_cmd == "recovery":
                    self.cmd_recovery()
                elif recovery_cmd == "exit":
                    self.is_running = False
                    break
                continue

            try:
                cmd_line = input(f"{self.theme_colors[self.current_theme]}{self.ps1} {self.theme_colors['reset']}")
                if not cmd_line.strip():
                    continue

                self.history.append(cmd_line)
                self.save_history()

                # Pipeline handling (|)
                if "|" in cmd_line:
                    cmds = [c.strip() for c in cmd_line.split("|")]
                    output = self.execute_command(cmds[0], return_output=True)
                    if len(cmds) > 1 and cmds[1].startswith("grep"):
                        search_term = cmds[1].split(" ", 1)[1] if " " in cmds[1] else ""
                        output = "\n".join([line for line in output.split("\n") if search_term in line])
                    print(output)
                else:
                    output = self.execute_command(cmd_line)
                    if output:
                        print(output)

                # Reset crash count on successful command execution
                self.crash_count = 0

            except KeyboardInterrupt:
                print("\nUse 'menu' -> 'shutdown' to exit.")
            except Exception as e:
                self.crash_count += 1
                logging.error(f"Crash [{self.crash_count}]: {e}")
                print(f"Critical error: {e}. Details in .expos_log")
                if self.crash_count >= 3:
                    self.is_corrupted = True

    def execute_command(self, cmd_line, return_output=False):
        try:
            parts = shlex.split(cmd_line)
        except ValueError as e:
            return f"Syntax error: {e}"

        if not parts:
            return ""

        cmd = parts[0]
        args = parts[1:]

        # Alias replacement
        if cmd in self.aliases:
            try:
                parts = shlex.split(self.aliases[cmd]) + args
                cmd = parts[0]
                args = parts[1:]
            except ValueError:
                return "Alias syntax error."

        # Main screen restrictions
        if cmd in ["exit", "shutdown", "sysinfo", "quit"]:
            msg = "Command unavailable in console. Use 'menu'."
            return msg if return_output else print(msg)

        # Command Dispatcher
        try:
            if cmd == "help":
                return self.cmd_help(args)
            elif cmd == "menu":
                return self.cmd_menu()
            elif cmd == "man":
                return self.cmd_man(args)
            elif cmd == "ping":
                return self.cmd_ping(args)
            elif cmd == "wget":
                return self.cmd_wget(args)
            elif cmd == "ps":
                return self.cmd_ps()
            elif cmd == "df":
                return self.cmd_df()
            elif cmd == "alias":
                return self.cmd_alias(args)
            elif cmd == "view":
                return self.cmd_view(args)
            elif cmd == "color":
                return self.cmd_color(args)
            elif cmd == "tictactoe":
                return self.cmd_tictactoe()
            elif cmd == "chmod":
                return self.cmd_chmod(args)
            elif cmd == "ls":
                return "\n".join(
                    [f"{k} [{v['perms']}]" for k, v in self.vfs.items()]) if self.vfs else "Empty directory."
            elif cmd == "crash":
                raise RuntimeError("Forced system crash.")  # Hidden command for testing
            else:
                return f"Command not found: {cmd}. Type 'help' for a list."
        except Exception as e:
            # Re-raise to be caught by the main run loop for crash counting
            raise RuntimeError(f"Error executing {cmd}: {e}")

    # --- COMMAND IMPLEMENTATIONS ---

    def cmd_recovery(self):
        print("\nInitiating System Recovery...")
        time.sleep(1)
        print("Scanning corrupted sectors...")
        for i in range(1, 101, 20):
            sys.stdout.write(f"\rProgress: [{i}%]")
            sys.stdout.flush()
            time.sleep(0.5)
        print("\nRestoring Virtual File System to default state...")
        self.init_vfs()
        self.is_corrupted = False
        self.crash_count = 0
        print("System recovered successfully. Rebooting...\n")
        time.sleep(1)
        self.boot()
        return ""

    def cmd_help(self, args):
        if args:
            return self.cmd_man(args)
        return ("Available commands:\n"
                "  help, man, menu, ls, view, chmod\n"
                "  ping, wget, ps, df, alias, color\n"
                "  tictactoe\n"
                "Hint: commands 'exit' and 'sysinfo' are located in the menu!")

    def cmd_man(self, args):
        docs = {
            "ping": "ping [-c count] <host> - Simulates network ping.",
            "wget": "wget <url> - Simulates file downloading.",
            "view": "view <file> - View text file (e.g., view README.exp)",
            "menu": "menu - Opens the graphical system menu."
        }
        if not args: return "Specify a command: man <command>"
        return docs.get(args[0], f"No manual entry for {args[0]}")

    def cmd_menu(self):
        while True:
            print("\n" + "=" * 20)
            print(" MAIN MENU")
            print("=" * 20)
            print(" 1. System Information (sysinfo)")
            print(" 2. Prompt Settings (PS1)")
            print(" 3. Games Hub")
            print(" 4. Shutdown (shutdown)")
            print(" 0. Back to terminal")

            choice = input("Choice: ")
            if choice == "1":
                print(
                    f"\nOS: EXP OS {self.version}\nUser: {self.current_user}\nTheme: {self.current_theme}\nAliases: {len(self.aliases)}")
            elif choice == "2":
                self.ps1 = input("Enter new prompt format: ")
            elif choice == "3":
                print("Launching Games Hub... Type 'tictactoe' in the console.")
            elif choice == "4":
                print("Shutting down...")
                self.is_running = False
                break
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
        return ""

    def cmd_ping(self, args):
        count = 4
        if "-c" in args:
            try:
                idx = args.index("-c")
                count = int(args[idx + 1])
                args.pop(idx + 1)
                args.pop(idx)
            except:
                return "Invalid ping syntax."

        host = args[0] if args else "127.0.0.1"
        print(f"PING {host} 56(84) bytes of data.")
        for i in range(count):
            ms = random.uniform(1.0, 50.0)
            print(f"64 bytes from {host}: icmp_seq={i + 1} ttl=64 time={ms:.2f} ms")
            time.sleep(0.5)
        return ""

    def cmd_wget(self, args):
        if not args: return "Provide a URL."
        url = args[0]
        filename = url.split("/")[-1] or "downloaded_file"
        print(f"Connecting to {url}...")
        time.sleep(1)
        for i in range(10, 101, 10):
            sys.stdout.write(f"\rDownloading {filename}: [{'#' * (i // 10)}{'.' * (10 - i // 10)}] {i}%")
            sys.stdout.flush()
            time.sleep(0.2)
        print()
        self.vfs[filename] = {"content": f"File downloaded from {url}", "perms": "644"}
        return f"File {filename} saved successfully."

    def cmd_ps(self):
        return ("PID   USER     TIME  COMMAND\n"
                "1     root     0:02  init\n"
                f"42    {self.current_user[:7]:<8} 0:01  exp_shell\n"
                "99    system   0:00  cron_sim")

    def cmd_df(self):
        return ("Filesystem     1K-blocks    Used Available Use%\n"
                "vfs_root            1024      12      1012   1%\n"
                "trash_dir            512       0       512   0%")

    def cmd_view(self, args):
        if not args: return "Specify a file."
        file = args[0]
        if file in self.vfs:
            print(f"--- Viewing: {file} ---")
            lines = self.vfs[file]["content"].split("\n")
            for i, line in enumerate(lines):
                print(line)
                if (i + 1) % 5 == 0 and len(lines) > i + 1:
                    if input("-- Press Enter to continue (q to quit) --").strip().lower() == 'q':
                        break
            return ""
        return "File not found."

    def cmd_alias(self, args):
        if not args:
            return "\n".join([f"{k}='{v}'" for k, v in self.aliases.items()]) if self.aliases else "No aliases defined."
        if "=" in args[0]:
            k, v = args[0].split("=", 1)
            self.aliases[k] = v.strip("'\"")
            return f"Alias added: {k}"
        return "Format: alias name='command'"

    def cmd_color(self, args):
        if not args or args[0] not in ["dark", "light"]:
            return "Usage: color dark | light"
        self.current_theme = args[0]
        return "Theme changed."

    def cmd_chmod(self, args):
        if len(args) < 2: return "Format: chmod <perms> <file>"
        perms, file = args[0], args[1]
        if file in self.vfs:
            self.vfs[file]["perms"] = perms
            return f"Permissions for {file} changed to {perms}"
        return "File not found."

    def cmd_tictactoe(self):
        board = [' '] * 9

        def print_board():
            print(
                f"\n {board[0]} | {board[1]} | {board[2]} \n---+---+---\n {board[3]} | {board[4]} | {board[5]} \n---+---+---\n {board[6]} | {board[7]} | {board[8]} \n")

        while ' ' in board:
            print_board()
            try:
                move_input = input("Your move (1-9): ")
                if not move_input.isdigit(): continue
                move = int(move_input) - 1
                if 0 <= move <= 8 and board[move] == ' ':
                    board[move] = 'X'
                else:
                    print("Cell occupied or invalid!"); continue
            except:
                continue

            # AI Move
            empty = [i for i, x in enumerate(board) if x == ' ']
            if empty: board[random.choice(empty)] = 'O'

            if ' ' not in board: break

        print_board()
        return "Game over!"

    def save_history(self):
        try:
            with open("exp_history.txt", "a") as f:
                f.write(self.history[-1] + "\n")
        except:
            pass


if __name__ == "__main__":
    is_safe = "--safe" in sys.argv
    os_sim = ExpOS(safe_mode=is_safe)
    os_sim.run()
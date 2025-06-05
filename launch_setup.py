import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import subprocess
import threading
import sys

try:
    import win32com.client
except ImportError:
    win32com = None

class ConsoleWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Console Output")
        self.geometry("700x350")
        self.configure(bg="#181a20")
        self.text = tk.Text(self, height=20, width=90, bg="#181a20", fg="#f5f6fa", font=("Consolas", 11), state="normal")
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(self, command=self.text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.protocol("WM_DELETE_WINDOW", self.hide)
        self.is_hidden = False
    def write(self, msg):
        self.text.insert(tk.END, msg)
        if not msg.endswith("\n"):
            self.text.insert(tk.END, "\n")
        self.text.see(tk.END)
    def clear(self):
        self.text.delete(1.0, tk.END)
    def show(self):
        self.is_hidden = False
        self.deiconify()
    def hide(self):
        self.is_hidden = True
        self.withdraw()

def write_file(filename, value, encoding="utf-8"):
    with open(filename, 'w', encoding=encoding) as f:
        f.write(value)

def run_depot_downloader_gui(depot, manifest, install_dir, login=None, password=None, beta=None, console_cb=None, ask_guard_cb=None):
    exe = 'DepotDownloader.exe' if os.name == 'nt' else './DepotDownloader.exe'
    args = [exe, '-app', '730', '-depot', str(depot), '-manifest', str(manifest), '-dir', install_dir]
    if beta:
        args += ['-beta', beta]
    if login:
        args += ['-username', login]
    if password:
        args += ['-password', password]
    if console_cb:
        console_cb(' '.join(args) + '\n')
    full_cmd = ['cmd', '/c'] + args if os.name == 'nt' else args
    process = subprocess.Popen(full_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    try:
        while True:
            line = process.stdout.readline()
            if not line:
                break
            if console_cb:
                console_cb(line)
            if (login and password) and (('Steam Guard' in line) or ('Enter the authentication code' in line)):
                if ask_guard_cb:
                    code = ask_guard_cb()
                    if not code:
                        process.terminate()
                        raise Exception("Steam Guard code entry cancelled.")
                    process.stdin.write(code + '\n')
                    process.stdin.flush()
        process.wait()
        if process.returncode != 0:
            raise Exception(f"DepotDownloader error (depot {depot}), code {process.returncode}")
    finally:
        try:
            process.stdout.close()
        except Exception:
            pass
        try:
            process.stdin.close()
        except Exception:
            pass

def return_inventory(install_dir):
    file_path = os.path.join(install_dir, "csgo", "steam.inf")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        found = False
        for i, line in enumerate(lines):
            if line.startswith("ClientVersion="):
                lines[i] = "ClientVersion=2000258\n"
                found = True
                break
        if not found:
            lines.insert(0, "ClientVersion=2000258\n")
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)
    except FileNotFoundError:
        raise Exception(f"Error: File '{file_path}' not found.")
    except Exception as e:
        raise Exception(f"Error: {e}")

def create_desktop_shortcut(install_dir, console_cb=None):
    csgo_path = os.path.join(install_dir, "csgo.exe")
    if not os.path.isfile(csgo_path):
        if console_cb:
            console_cb(f"csgo.exe not found in {install_dir}\n")
        return
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    shortcut_path = os.path.join(desktop, "CSGO Legacy.lnk")
    try:
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = csgo_path
        shortcut.Arguments = "-steam"
        shortcut.WorkingDirectory = install_dir
        shortcut.IconLocation = csgo_path
        shortcut.save()
        if console_cb:
            console_cb(f"Shortcut created on desktop: {shortcut_path}\n")
    except Exception as e:
        if console_cb:
            console_cb(f"Failed to create shortcut: {e}\n")

def run_gui():
    root = tk.Tk()
    root.title("CS:GO Legacy Downloader")
    window_width = 600
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.configure(bg="#23272f")
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TLabel', background="#23272f", foreground="#f5f6fa", font=("Segoe UI", 12))
    style.configure('TButton', font=("Segoe UI", 12), padding=6)
    style.configure('TEntry', font=("Segoe UI", 12))
    style.configure('TCombobox', font=("Segoe UI", 12))

    direct_var = tk.StringVar()
    login_var = tk.StringVar()
    password_var = tk.StringVar()
    invent_var = tk.StringVar(value="No")

    console_win = ConsoleWindow(root)
    console_win.show()

    def write_console(msg):
        console_win.write(msg)

    def clear_console():
        console_win.clear()

    def ask_guard_code():
        code = tk.simpledialog.askstring("Steam Guard", "Enter Steam Guard code from your email or app:")
        return code

    def choose_dir():
        path = filedialog.askdirectory()
        if path:
            direct_var.set(path)

    def start_process_thread():
        threading.Thread(target=start_process, daemon=True).start()

    def start_process():
        direct1 = direct_var.get()
        login1 = login_var.get()
        password1 = password_var.get()
        invent1 = invent_var.get()
        if not direct1 or not login1 or not password1:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        try:
            clear_console()
            write_file('directory_for_install_CSGO_Legacy.txt', direct1)
            write_file('login_for_install_CSGO_Legacy.txt', login1)
            write_file('password_for_install_CSGO_Legacy.txt', password1)
            write_console("Starting first depot download...\n")
            run_depot_downloader_gui(
                depot=732, manifest=6314304446937576250, install_dir=direct1,
                login=login1, password=password1, beta='csgo_legacy',
                console_cb=write_console, ask_guard_cb=ask_guard_code)
            write_console("Starting second depot download...\n")
            run_depot_downloader_gui(
                depot=731, manifest=1224088799001669801, install_dir=direct1,
                login=login1, password=password1,
                console_cb=write_console, ask_guard_cb=ask_guard_code)
            if invent1 == "Yes":
                write_console("Restoring inventory...\n")
                return_inventory(direct1)
            create_desktop_shortcut(direct1, console_cb=write_console)
            for f in ['directory_for_install_CSGO_Legacy.txt', 'login_for_install_CSGO_Legacy.txt', 'password_for_install_CSGO_Legacy.txt']:
                try:
                    os.remove(f)
                except Exception:
                    pass
            messagebox.showinfo("Success", "Done!")
            write_console("Done!\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            write_console(f"Error: {e}\n")

    ttk.Label(root, text="CS:GO Legacy Downloader", font=("Segoe UI", 18, "bold"), background="#23272f", foreground="#f5c542").pack(pady=20)
    ttk.Label(root, text="CS:GO Legacy directory:").pack(pady=5)
    dir_frame = tk.Frame(root, bg="#23272f")
    dir_frame.pack(pady=5)
    dir_entry = ttk.Entry(dir_frame, textvariable=direct_var, width=30)
    dir_entry.pack(side=tk.LEFT, padx=5)
    ttk.Button(dir_frame, text="Browse", command=choose_dir).pack(side=tk.LEFT)

    ttk.Label(root, text="Steam login:").pack(pady=5)
    ttk.Entry(root, textvariable=login_var, width=30).pack(pady=5)
    ttk.Label(root, text="Steam password:").pack(pady=5)
    ttk.Entry(root, textvariable=password_var, width=30, show="*").pack(pady=5)

    ttk.Label(root, text="Regain inventory?").pack(pady=5)
    invent_combo = ttk.Combobox(root, textvariable=invent_var, values=["Yes", "No"], state="readonly", width=10)
    invent_combo.pack(pady=5)

    ttk.Button(root, text="Start", command=start_process_thread).pack(pady=30)

    root.mainloop()

if __name__ == "__main__":
    run_gui()

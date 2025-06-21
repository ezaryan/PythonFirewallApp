import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import subprocess
import psutil
import threading
import os
import json
import pystray
from PIL import Image, ImageDraw
import sys

# File paths
LOG_FILE = "firewall_log.txt"
BLOCKED_FILE = "blocked_entries.json"

# In-memory storage for blocked IPs and ports
blocked_ips = set()
blocked_ports = set()

# === Persistence Functions ===
def save_blocked_entries():
    with open(BLOCKED_FILE, 'w') as f:
        json.dump({
            "ips": list(blocked_ips),
            "ports": list(blocked_ports)
        }, f)

def load_blocked_entries():
    if os.path.exists(BLOCKED_FILE):
        with open(BLOCKED_FILE, 'r') as f:
            data = json.load(f)
            for ip in data.get("ips", []):
                blocked_ips.add(ip)
            for port in data.get("ports", []):
                blocked_ports.add(port)

# === Network Functions ===
def block_ip(ip):
    if ip not in blocked_ips:
        subprocess.call(f'netsh advfirewall firewall add rule name="Block {ip}" dir=in action=block remoteip={ip}', shell=True)
        blocked_ips.add(ip)
        log_action(f"Blocked IP: {ip}")
        update_blocked_list()
        save_blocked_entries()

def unblock_ip(ip):
    if ip in blocked_ips:
        subprocess.call(f'netsh advfirewall firewall delete rule name="Block {ip}"', shell=True)
        blocked_ips.remove(ip)
        log_action(f"Unblocked IP: {ip}")
        update_blocked_list()
        save_blocked_entries()

def block_port(port):
    if port not in blocked_ports:
        subprocess.call(f'netsh advfirewall firewall add rule name="Block Port {port}" dir=in action=block localport={port} protocol=TCP action=block', shell=True)
        blocked_ports.add(port)
        log_action(f"Blocked Port: {port}")
        update_blocked_list()
        save_blocked_entries()

def unblock_port(port):
    if port in blocked_ports:
        subprocess.call(f'netsh advfirewall firewall delete rule name="Block Port {port}"', shell=True)
        blocked_ports.remove(port)
        log_action(f"Unblocked Port: {port}")
        update_blocked_list()
        save_blocked_entries()

def list_connections():
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED':
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "None"
            pid = conn.pid or "N/A"
            connections.append((laddr, raddr, pid))
    return connections

def get_all_firewall_rules():
    result = subprocess.run('netsh advfirewall firewall show rule name=all', capture_output=True, shell=True, text=True)
    return result.stdout

# === GUI Functions ===
def update_connection_table():
    for row in tree.get_children():
        tree.delete(row)
    conns = list_connections()
    for laddr, raddr, pid in conns:
        tree.insert('', tk.END, values=(laddr, raddr, pid))

def update_blocked_list():
    blocked_listbox.delete(0, tk.END)
    for ip in blocked_ips:
        blocked_listbox.insert(tk.END, f"IP: {ip}")
    for port in blocked_ports:
        blocked_listbox.insert(tk.END, f"Port: {port}")

def block_ip_action():
    ip = ip_entry.get()
    if ip:
        block_ip(ip)
        messagebox.showinfo("Success", f"Blocked IP: {ip}")

def unblock_ip_action():
    ip = ip_entry.get()
    if ip:
        unblock_ip(ip)
        messagebox.showinfo("Success", f"Unblocked IP: {ip}")

def block_port_action():
    port = port_entry.get()
    if port.isdigit():
        block_port(int(port))
        messagebox.showinfo("Success", f"Blocked Port: {port}")

def unblock_port_action():
    port = port_entry.get()
    if port.isdigit():
        unblock_port(int(port))
        messagebox.showinfo("Success", f"Unblocked Port: {port}")

def refresh_threaded():
    threading.Thread(target=update_connection_table).start()

def log_action(action):
    log_area.insert(tk.END, action + "\n")
    log_area.see(tk.END)
    with open(LOG_FILE, "a") as log_file:
        log_file.write(action + "\n")

def show_firewall_rules():
    rules = get_all_firewall_rules()
    rules_window = tk.Toplevel(root)
    rules_window.title("All Firewall Rules")
    rules_text = scrolledtext.ScrolledText(rules_window, wrap=tk.WORD, width=100, height=30)
    rules_text.insert(tk.END, rules)
    rules_text.pack(fill=tk.BOTH, expand=True)

def on_closing():
    root.withdraw()

def on_quit(icon=None, item=None):
    if messagebox.askokcancel("Exit", "Are you sure you want to quit the application?"):
        if icon:
            icon.stop()
        try:
            root.destroy()
        except:
            pass
        sys.exit()

def show_window(icon, item):
    root.deiconify()

def create_tray_icon():
    image = Image.new('RGB', (64, 64), color='black')
    draw = ImageDraw.Draw(image)
    draw.rectangle([10, 10, 54, 54], fill='white')
    icon = pystray.Icon("firewall", image, menu=pystray.Menu(
        pystray.MenuItem('Show', show_window),
        pystray.MenuItem('Quit', on_quit)
    ))
    icon.run()

# === GUI Setup ===
root = tk.Tk()
root.title("Python Personal Firewall - Windows")
root.geometry("900x700")

frame = tk.Frame(root)
frame.pack(pady=10)

ip_label = tk.Label(frame, text="IP Address:")
ip_label.grid(row=0, column=0)
ip_entry = tk.Entry(frame, width=20)
ip_entry.grid(row=0, column=1)
block_ip_btn = tk.Button(frame, text="Block IP", command=block_ip_action)
block_ip_btn.grid(row=0, column=2, padx=5)
unblock_ip_btn = tk.Button(frame, text="Unblock IP", command=unblock_ip_action)
unblock_ip_btn.grid(row=0, column=3, padx=5)

port_label = tk.Label(frame, text="Port:")
port_label.grid(row=1, column=0)
port_entry = tk.Entry(frame, width=20)
port_entry.grid(row=1, column=1)
block_port_btn = tk.Button(frame, text="Block Port", command=block_port_action)
block_port_btn.grid(row=1, column=2, padx=5)
unblock_port_btn = tk.Button(frame, text="Unblock Port", command=unblock_port_action)
unblock_port_btn.grid(row=1, column=3, padx=5)

refresh_btn = tk.Button(root, text="Refresh Connections", command=refresh_threaded)
refresh_btn.pack(pady=10)

show_rules_btn = tk.Button(root, text="Show All Firewall Rules", command=show_firewall_rules)
show_rules_btn.pack(pady=5)

close_btn = tk.Button(root, text="Close App", bg="red", fg="white", command=on_quit)
close_btn.pack(pady=5)

tree = ttk.Treeview(root, columns=("Local Address", "Remote Address", "PID"), show='headings')
tree.heading("Local Address", text="Local Address")
tree.heading("Remote Address", text="Remote Address")
tree.heading("PID", text="PID")
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

log_label = tk.Label(root, text="Log History:")
log_label.pack()
log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=8)
log_area.pack(padx=10, pady=5)

blocked_label = tk.Label(root, text="Currently Blocked:")
blocked_label.pack()
blocked_listbox = tk.Listbox(root, width=100, height=5)
blocked_listbox.pack(padx=10, pady=5)

# Load previous blocked entries
load_blocked_entries()

# Initial load
refresh_threaded()
update_blocked_list()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start tray icon in a separate thread
threading.Thread(target=create_tray_icon, daemon=True).start()

try:
    root.mainloop()
except KeyboardInterrupt:
    sys.exit()

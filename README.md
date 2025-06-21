# 🛡️ Python Personal Firewall

A lightweight personal firewall for Windows built using **Python** with a graphical user interface (GUI). Block and unblock IPs or ports, view active network connections, and manage rules — all with a few clicks!

## 📦 Features

- 🔐 Block/Unblock IP addresses
- 🔒 Block/Unblock TCP ports
- 🧠 Automatically saves and restores blocked entries on restart
- 📄 Export log history to a file
- 🖥️ Monitor active TCP network connections
- 📋 View all Windows Firewall rules
- 🔔 Tray icon with minimize-to-tray support
- ✅ Clean exit with confirmation prompt
- 🖱️ Simple GUI using `tkinter`


## 🚀 How to Use

### 🧱 Installation (End User)

Download the latest installer `.exe` from the [Releases](https://github.com/your-username/PythonFirewallApp/releases) section.

### 🐍 Run from Source (Developer)
1. Install Python 3.x
2. Clone this repo:
   git clone https://github.com/your-username/PythonFirewallApp.git
   cd PythonFirewallApp
3. Install dependencies:

   
   ````pip install -r requirements.txt````
4. Run the app:

   ```
   python main.py
   ```

---

## 🧰 Building the Executable

1. Install PyInstaller:

   ```
   pip install pyinstaller
   ```
2. Build the `.exe`:

   ```
   pyinstaller --onefile --noconsole --icon=app.ico main.py
   ```

---

## 🏗️ Create Windows Installer

We use [Inno Setup](https://jrsoftware.org/isdl.php) to package a Windows installer.

1. Install Inno Setup
2. Use the provided `FirewallAppInstaller.iss` script
3. Compile it to generate an `.exe` installer

---

## 📁 Files & Folders

| File/Folder                | Purpose                             |
| -------------------------- | ----------------------------------- |
| `main.py`                  | Main application GUI script         |
| `requirements.txt`         | Python dependencies                 |
| `dist/`                    | Output folder for `.exe` build      |
| `output/`                  | Output folder for Windows installer |
| `FirewallAppInstaller.iss` | Inno Setup installer script         |

---

## ⚠️ Disclaimer

This application makes changes to **Windows Firewall** rules. Use it responsibly and with admin privileges. It is intended for **educational purposes** only.

---

## 📃 License

MIT License — see `LICENSE` file for details.

---

## 🙌 Credits

Created by [Aryan Pagar](https://github.com/ezaryan) & [Sumant Patil](https://github.com/)

---



---

### ✅ Next Steps:
- Replace `your-username` with your actual GitHub username.
- Add a screenshot section (just drag and drop PNGs into the GitHub repo later).
- Add a `requirements.txt` with dependencies like:

````
psutil
pystray
Pillow
````

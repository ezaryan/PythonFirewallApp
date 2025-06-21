; FirewallAppInstaller.iss - Inno Setup Script

[Setup]
AppName=Python Personal Firewall
AppVersion=1.0
DefaultDirName={pf}\\PersonalFirewall
DefaultGroupName=Personal Firewall
OutputDir=output
OutputBaseFilename=PersonalFirewallInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\\firewall_gui.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\Firewall App"; Filename: "{app}\\firewall_gui.exe"
Name: "{group}\\Uninstall Firewall App"; Filename: "{uninstallexe}"
Name: "{commondesktop}\\Firewall App"; Filename: "{app}\\firewall_gui.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\\firewall_gui.exe"; Description: "Launch Firewall App"; Flags: nowait postinstall skipifsilent

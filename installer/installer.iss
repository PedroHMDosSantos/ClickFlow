[Setup]
AppName=ClickFlow
AppVersion=1.0
DefaultDirName={autopf}\ClickFlow
DefaultGroupName=ClickFlow
OutputDir=build
OutputBaseFilename=setup_clickflow
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Files]
Source: "..\dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ClickFlow"; Filename: "{app}\ClickFlow.exe"
Name: "{commondesktop}\ClickFlow"; Filename: "{app}\ClickFlow.exe"

[Run]
Filename: "{app}\ClickFlow.exe"; Description: "Abrir ClickFlow"; Flags: nowait postinstall skipifsilent
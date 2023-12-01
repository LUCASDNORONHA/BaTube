; Script de Instalação BaTube

[Setup]
AppName=BaTube
AppVersion=1.0
DefaultDirName={pf}\BaTube
OutputDir=Output
OutputBaseFilename=BaTubeInstaller
Compression=lzma
SolidCompression=yes
SetupIconFile=C:\Users\lucas\BaTube-Project\resources\LogoIcon.ico

[Files]
Source: "C:\Users\lucas\BaTube-Project\dist\AppBaTube.exe"; DestDir: "{app}"
Source: "C:\Users\lucas\BaTube-Project\resources\LogoIcon.ico"; DestDir: "{app}\resources"

[Icons]
Name: "{group}\BaTube"; Filename: "{app}\AppBaTube.exe"; WorkingDir: "{app}"; IconFilename: "{app}\resources\LogoIcon.ico"

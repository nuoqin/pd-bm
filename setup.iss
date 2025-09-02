; 安装包基本信息
[Setup]
AppName=nuoqin
AppVersion=1.0
AppPublisher=nuoqin
AppPublisherURL=https://github.com/nuoqin
AppSupportURL=https://github.com/nuoqin
AppUpdatesURL=https://github.com/nuoqin

; 安装目录，默认 C:\Program Files\nuoqin
DefaultDirName={pf}\nuoqin
DefaultGroupName=nuoqin
; 输出文件名
OutputBaseFilename=nuoqin
; 使用自定义图标（换成你自己的 .ico）
SetupIconFile=tools.ico

Compression=lzma
SolidCompression=yes

; 管理员权限
PrivilegesRequired=admin

; 卸载显示的图标
UninstallDisplayIcon={app}\nuoqin.exe

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"

; 要打包的文件
[Files]
; 主程序
Source: "dist\nuoqin.exe"; DestDir: "{app}"; Flags: ignoreversion
; tools 文件夹（递归）
Source: "dist\tools\*"; DestDir: "{app}\tools"; Flags: ignoreversion recursesubdirs createallsubdirs
; 如果有图标，也可以打包
Source: "dist\tools.ico"; DestDir: "{app}"; Flags: ignoreversion

; 创建快捷方式
[Icons]
; 开始菜单快捷方式
Name: "{group}\nuoqin"; Filename: "{app}\nuoqin.exe"; IconFilename: "{app}\tools.ico"
; 卸载快捷方式
Name: "{group}\卸载 nuoqin工具"; Filename: "{uninstallexe}"
; 桌面快捷方式
Name: "{commondesktop}\nuoqin工具"; Filename: "{app}\nuoqin.exe"; IconFilename: "{app}\tools.ico"

; 卸载时删除整个目录
[UninstallDelete]
Type: filesandordirs; Name: "{app}"

; 安装完成后执行程序
[Run]
Filename: "{app}\nuoqin.exe"; Description: "运行nuoqin工具"; Flags: nowait postinstall skipifsilent

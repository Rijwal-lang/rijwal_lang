; RIJWAL_LANG v0.17 - Windows Installer Script
; Generated for NSIS (Nullsoft Scriptable Install System)
; 
; To create the installer:
; 1. Download NSIS from: https://nsis.sourceforge.io/
; 2. Run: makensis rijwal_installer.nsi
;
; This creates: RijwalLang-Setup.exe

!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"

; ============================================================================
; INSTALLER SETTINGS
; ============================================================================

Name "Rijwal_Lang IDE v0.17"
OutFile "rijwal_lang_setup.exe"
InstallDir "$PROGRAMFILES\RijwalLang"
InstallDirRegKey HKCU "Software\RijwalLang" ""

; Request admin privileges for installation
RequestExecutionLevel admin

; ============================================================================
; MUI SETTINGS
; ============================================================================

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

; ============================================================================
; FUNCTIONS
; ============================================================================

Function .onInit
  ; Check disk space (estimate 50MB needed)
  ${GetRoot} $INSTDIR $0
  ${DriveSpace} "$0" "/D=F /S=M" $1
  ${If} $1 < 50
    MessageBox MB_OK "Insufficient disk space. At least 50MB is required on drive $0."
    Abort
  ${EndIf}
FunctionEnd

; ============================================================================
; INSTALLER SECTIONS
; ============================================================================

Section "Core Files (required)" SecCore
  SectionIn RO  ; Read-only, always selected
  SetOutPath "$INSTDIR"
  
  ; Copy executable and launch tools
  File "build_exe\dist\RijwalIDE.exe"
  File "ide_server.py"
  File "rijwal_lang_enhanced.py"
  File "rijwal_idle.py"
  
  ; Create shortcuts
  CreateDirectory "$SMPROGRAMS\Rijwal_Lang IDE"
  CreateShortCut "$SMPROGRAMS\Rijwal_Lang IDE\Rijwal_Lang IDE.lnk" "$INSTDIR\RijwalIDE.exe"
  CreateShortCut "$DESKTOP\Rijwal_Lang IDE.lnk" "$INSTDIR\RijwalIDE.exe"
  CreateShortCut "$SMPROGRAMS\Rijwal_Lang IDE\Rijwal_Lang IDE (Web).lnk" "$INSTDIR\RijwalIDE.exe"
  CreateShortCut "$SMPROGRAMS\Rijwal_Lang IDE\Rijwal_Lang IDLE.lnk" "$SYSDIR\cmd.exe" "/k python $"$INSTDIR\rijwal_idle.py$""
  
  ; Write registry entries
  WriteRegStr HKCU "Software\RijwalLang" "" "$INSTDIR"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\RijwalLang" \
    "DisplayName" "Rijwal_Lang IDE v0.17"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\RijwalLang" \
    "UninstallString" "$INSTDIR\Uninstall.exe"
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Documentation" SecDocs
  SetOutPath "$INSTDIR"
  
  ; Copy documentation
  SetOutPath "$INSTDIR\docs"
  File "docs\README.md"
  File "docs\QUICK_START.md"
  File "docs\LANGUAGE_REFERENCE.md"

  ; Create documentation shortcut
  CreateShortCut "$SMPROGRAMS\Rijwal_Lang IDE\Documentation.lnk" "$INSTDIR\docs\README.md"
SectionEnd

Section "Examples + IDE Assets" SecExamples
  SetOutPath "$INSTDIR\examples"
  File "examples\*.Rijwal_lang"

  SetOutPath "$INSTDIR\ide"
  File "ide\index.html"
  File "ide\editor.js"
  File "ide\style.css"

  SetOutPath "$INSTDIR"
  File "ide_with_games.html"
SectionEnd

; ============================================================================
; UNINSTALLER SECTION
; ============================================================================

Section "Uninstall"
  ; Remove executable
  Delete "$INSTDIR\RijwalIDE.exe"
  
  ; Remove documentation and IDE assets
  RMDir /r "$INSTDIR\docs"
  RMDir /r "$INSTDIR\examples"
  RMDir /r "$INSTDIR\ide"
  Delete "$INSTDIR\ide_with_games.html"
  Delete "$INSTDIR\ide_server.py"
  Delete "$INSTDIR\rijwal_lang_enhanced.py"
  Delete "$INSTDIR\rijwal_idle.py"
  
  ; Remove shortcuts
  Delete "$SMPROGRAMS\Rijwal_Lang IDE\*.*"
  RMDir "$SMPROGRAMS\Rijwal_Lang IDE"
  Delete "$DESKTOP\Rijwal_Lang IDE.lnk"
  
  ; Remove directory
  RMDir "$INSTDIR"
  
  ; Remove registry entries
  DeleteRegKey HKCU "Software\RijwalLang"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\RijwalLang"
SectionEnd

; ============================================================================
; INSTALLER INFO
; ============================================================================

VIProductVersion "0.17.0.0"
VIAddVersionKey "ProductName" "Rijwal_Lang IDE"
VIAddVersionKey "ProductVersion" "0.17"
VIAddVersionKey "FileVersion" "0.17.0.0"
VIAddVersionKey "FileDescription" "Advanced Programming Language IDE"
VIAddVersionKey "CompanyName" "Rijwal_Lang Project"

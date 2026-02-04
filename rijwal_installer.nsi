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
OutFile "RijwalLang-Setup-v0.17.exe"
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
  
  ; Copy executable
  File "build_exe\dist\RijwalIDE.exe"
  
  ; Create shortcuts
  CreateDirectory "$SMPROGRAMS\Rijwal_Lang IDE"
  CreateShortCut "$SMPROGRAMS\Rijwal_Lang IDE\Rijwal_Lang IDE.lnk" "$INSTDIR\RijwalIDE.exe"
  CreateShortCut "$DESKTOP\Rijwal_Lang IDE.lnk" "$INSTDIR\RijwalIDE.exe"
  
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
  File "README.md"
  File "RIJWAL_v0.17_ECOSYSTEM.md"
  File "GAMES_AND_SOURCECODE.md"
  File "SOURCECODE_COOKBOOK.md"
  
  ; Create documentation shortcut
  CreateShortCut "$SMPROGRAMS\Rijwal_Lang IDE\Documentation.lnk" "$INSTDIR\README.md"
SectionEnd

Section "Examples" SecExamples
  SetOutPath "$INSTDIR\examples"
  File "examples\*.Rijwal_lang"
SectionEnd

; ============================================================================
; UNINSTALLER SECTION
; ============================================================================

Section "Uninstall"
  ; Remove executable
  Delete "$INSTDIR\RijwalIDE.exe"
  
  ; Remove documentation
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\RIJWAL_v0.17_ECOSYSTEM.md"
  Delete "$INSTDIR\GAMES_AND_SOURCECODE.md"
  Delete "$INSTDIR\SOURCECODE_COOKBOOK.md"
  
  ; Remove examples
  RMDir /r "$INSTDIR\examples"
  
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

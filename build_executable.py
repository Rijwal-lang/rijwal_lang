# -*- mode: python ; coding: utf-8 -*-
"""
RIJWAL_LANG v0.17 - PyInstaller Bundle Configuration
=====================================================

Creates standalone Windows executable with:
- Complete Rijwal_Lang interpreter
- Web-based IDE with game system
- All plugins pre-loaded
- One-click installation

Usage:
  python build_executable.py
  
Output: RijwalIDE.exe (single executable)
"""

import os
import sys
from pathlib import Path

# Ensure PyInstaller is installed
try:
    import PyInstaller
except ImportError:
    print("ERROR: PyInstaller not installed")
    print("Install with: pip install pyinstaller")
    sys.exit(1)

# Project root
PROJECT_ROOT = Path(__file__).parent

print("=" * 70)
print("RIJWAL_LANG v0.17 - Building Windows Executable")
print("=" * 70)
print()

# Create build directory if it doesn't exist
build_dir = PROJECT_ROOT / "build_exe"
build_dir.mkdir(exist_ok=True)

# PyInstaller command
cmd = [
    "pyinstaller",
    "--name=RijwalIDE",
    "--onefile",
    "--windowed",
    f"--distpath={build_dir / 'dist'}",
    f"--buildpath={build_dir / 'build'}",
    f"--specpath={build_dir}",
    "--icon=NONE",
    "--hidden-import=numpy",
    "--hidden-import=pandas",
    "--hidden-import=requests",
    "--hidden-import=PIL",
    "--hidden-import=cv2",
    "--hidden-import=matplotlib",
    "--hidden-import=scipy",
    "--hidden-import=sklearn",
    "--hidden-import=tensorflow",
    "--hidden-import=torch",
    "--add-data=ide_with_games.html:.",
    "--add-data=rijwal_games.py:.",
    "--add-data=RIJWAL_v0.17_ECOSYSTEM.md:.",
    "--add-data=GAMES_AND_SOURCECODE.md:.",
    "--add-data=SOURCECODE_COOKBOOK.md:.",
    "--add-data=examples:examples",
    "rijwal_ide_launcher.py",
]

print("Building PyInstaller configuration...")
print(f"  - Project root: {PROJECT_ROOT}")
print(f"  - Build directory: {build_dir}")
print(f"  - Output: RijwalIDE.exe")
print()

# Show command
print("PyInstaller Command:")
print(" ".join(cmd))
print()

# Run PyInstaller
import subprocess
result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))

if result.returncode == 0:
    exe_path = build_dir / "dist" / "RijwalIDE.exe"
    if exe_path.exists():
        exe_size = exe_path.stat().st_size / (1024 * 1024)  # MB
        print()
        print("=" * 70)
        print("SUCCESS! Executable created")
        print("=" * 70)
        print(f"  - Location: {exe_path}")
        print(f"  - Size: {exe_size:.1f} MB")
        print(f"  - Type: Standalone (no Python needed)")
        print()
        print("Next Steps:")
        print("  1. Test the executable: RijwalIDE.exe")
        print("  2. Create installer with NSIS or InnoSetup")
        print("  3. Distribute to users")
        print()
else:
    print()
    print("=" * 70)
    print("BUILD FAILED")
    print("=" * 70)
    print(f"Exit code: {result.returncode}")
    print()
    sys.exit(1)

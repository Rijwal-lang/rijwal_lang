# Rijwal_Lang Runner v0.12 — FINAL FIX
# NO recursion, NO sys.executable

import sys
import os
import subprocess

def main():
    # Runner always expects a file
    if len(sys.argv) < 2:
        print("Rijwal_Lang Runner")
        print("Please double-click a .Rijwal_Lang file")
        input("Press Enter to exit...")
        return

    # Location of runner EXE
    exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Engine MUST be next to runner
    engine = os.path.join(exe_dir, "rijwal_lang.py")
    file_to_run = sys.argv[1]

    if not os.path.exists(engine):
        print("Engine not found:", engine)
        print("Put rijwal_lang.py in the SAME folder as rijwal_lang_runner.exe")
        input("Press Enter to exit...")
        return

    if not os.path.exists(file_to_run):
        print("Program file not found:", file_to_run)
        input("Press Enter to exit...")
        return

    # IMPORTANT:
    # Call engine directly, NOT sys.executable
    subprocess.call(
        ["python", engine, file_to_run],
        shell=True
    )

    input("\nPress Enter to close...")

if __name__ == "__main__":
    main()

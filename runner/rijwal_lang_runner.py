# Rijwal_Lang Runner (legacy compatibility + modern engine fallback)

import sys
import os
import subprocess


def resolve_engine(base_dir):
    """Find the best available Rijwal engine near the runner."""
    candidates = [
        "rijwal_lang_enhanced.py",
        "rijwal_lang_v0.17.py",
        "rijwal_lang.py",
    ]
    search_dirs = [base_dir, os.path.dirname(base_dir)]
    for search_dir in search_dirs:
        for name in candidates:
            path = os.path.join(search_dir, name)
            if os.path.exists(path):
                return path
    return None


def main():
    if len(sys.argv) < 2:
        print("Rijwal_Lang Runner")
        print("Usage: rijwal_lang_runner <file.Rijwal_lang>")
        input("Press Enter to exit...")
        return

    exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    engine = resolve_engine(exe_dir)
    file_to_run = sys.argv[1]

    if not engine:
        print("Engine not found.")
        print("Expected one of: rijwal_lang_enhanced.py, rijwal_lang_v0.17.py, rijwal_lang.py")
        input("Press Enter to exit...")
        return

    if not os.path.exists(file_to_run):
        print("Program file not found:", file_to_run)
        input("Press Enter to exit...")
        return

    subprocess.call([sys.executable, engine, file_to_run])
    input("\nPress Enter to close...")


if __name__ == "__main__":
    main()

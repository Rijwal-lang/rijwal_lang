#!/usr/bin/env python3
"""
Rijwal_Lang IDLE (Interactive REPL)

Simple interactive shell for quickly testing Rijwal_Lang snippets.
"""

import os
import sys
import tempfile
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_PATH = os.path.join(SCRIPT_DIR, "rijwal_lang_enhanced.py")

BANNER = """
Rijwal_Lang IDLE (Interactive)
Type Rijwal_Lang code.
- Submit block: empty line
- Exit: :quit or :exit
""".strip()


def run_snippet(source: str) -> int:
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".Rijwal_lang",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(source)
        tmp_path = f.name

    try:
        proc = subprocess.run([sys.executable, ENGINE_PATH, tmp_path], text=True)
        return proc.returncode
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


def main() -> int:
    if not os.path.exists(ENGINE_PATH):
        print(f"[ERROR] Engine not found: {ENGINE_PATH}")
        return 1

    print(BANNER)
    print()

    buffer = []

    while True:
        prompt = "... " if buffer else ">>> "
        try:
            line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return 0

        if not buffer and line.strip().lower() in {":quit", ":exit"}:
            print("Bye!")
            return 0

        if line.strip() == "":
            if not buffer:
                continue
            source = "\n".join(buffer).rstrip() + "\n"
            run_snippet(source)
            print()
            buffer.clear()
            continue

        buffer.append(line)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Rijwal_Lang Setup Script
Installs dependencies and sets up the environment
"""

import os
import sys
import subprocess
import platform

def print_banner():
    print("""
    ╔════════════════════════════════════════╗
    ║   🚀 Rijwal_Lang Setup Wizard v0.13   ║
    ║   Making Coding Easy for Beginners     ║
    ╚════════════════════════════════════════╝
    """)

def check_python():
    """Check Python version"""
    print("📦 Checking Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"✅ Python {version.major}.{version.minor}")
        return True
    else:
        print(f"❌ Python 3.6+ required (you have {version.major}.{version.minor})")
        return False

def install_requirements():
    """Install required packages"""
    print("📥 Installing requirements...", end=" ")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "flask", "flask-cors", "-q"
        ])
        print("✅ Done")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_nodejs():
    """Check for Node.js (optional)"""
    print("🔍 Checking for Node.js...", end=" ")
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  Not installed (optional, needed for JS blocks)")
    return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...", end=" ")
    dirs = ["ide", "user_projects", "examples"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✅ Done")

def create_launcher():
    """Create launcher scripts"""
    print("🔨 Creating launcher scripts...", end=" ")
    
    # Windows batch file
    if platform.system() == "Windows":
        with open("start_ide.bat", "w") as f:
            f.write("""@echo off
echo Starting Rijwal_Lang IDE...
python ide_server.py
pause
""")
    
    # Unix shell script
    else:
        with open("start_ide.sh", "w") as f:
            f.write("""#!/bin/bash
echo "Starting Rijwal_Lang IDE..."
python3 ide_server.py
""")
        os.chmod("start_ide.sh", 0o755)
    
    print("✅ Done")

def create_sample_project():
    """Create a sample project"""
    print("📝 Creating sample project...", end=" ")
    sample_code = '''When Program Starts:
    Print "Welcome to Rijwal_Lang!"
    Print ""
    Print "This is your first program!"
    
    Input name
    Print "Hello, " + name + "!"
    
    Function greet(n):
        Return "Nice to meet you, " + n
    
    Print greet(name)
'''
    
    with open("examples/welcome.Rijwal_lang", "w") as f:
        f.write(sample_code)
    
    print("✅ Done")

def main():
    print_banner()
    
    # Check Python
    if not check_python():
        print("\n❌ Setup failed: Python 3.6+ is required")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("\n⚠️  Failed to install some packages, continuing anyway...")
    
    # Check Node.js
    check_nodejs()
    
    # Create directories
    create_directories()
    
    # Create launcher
    create_launcher()
    
    # Create sample
    create_sample_project()
    
    print("\n" + "="*40)
    print("✅ Setup Complete!")
    print("="*40)
    print("\n🚀 To start the IDE:")
    
    if platform.system() == "Windows":
        print("   1. Double-click: start_ide.bat")
        print("   2. Or run: python ide_server.py")
    else:
        print("   1. Run: ./start_ide.sh")
        print("   2. Or run: python3 ide_server.py")
    
    print("\n3. Open your browser to: http://localhost:5000")
    print("\n📚 Next steps:")
    print("   - Read: TUTORIAL.md")
    print("   - Check: examples/ folder")
    print("   - Visit: http://localhost:5000")
    print("\nHappy coding! 🎉\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        sys.exit(1)

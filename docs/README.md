# Rijwal_Lang - The Language for Young Developers 🚀

<div align="center">

![Version](https://img.shields.io/badge/version-0.13-blue)
![License](https://img.shields.io/badge/license-FBAL-green)
![Status](https://img.shields.io/badge/status-Production-brightgreen)

**A beautiful, easy-to-learn programming language with a modern web-based IDE**

[🎓 Tutorial](#tutorial) • [📚 Language Reference](#documentation) • [💻 Examples](#examples) • [🚀 Installation](#installation)

</div>

---

## What is Rijwal_Lang?

Rijwal_Lang is a **beginner-friendly programming language** designed for young developers like you! It combines:

- 📖 **Readable Syntax** - Code that looks like English
- 🎨 **Beautiful IDE** - No need for complex tools
- ⚡ **Easy Learning Curve** - Start coding in minutes
- 🔧 **Powerful Features** - Functions, timers, imports, Python integration
- 💾 **Built-in Editor** - Write, run, and save code in your browser

---

## Quick Start

### 1. Download & Install

**Option A: Using Pre-built Executable (Windows)**
```
1. Download rijwal_lang_setup.exe
2. Run the installer
3. Open Rijwal_Lang IDE from your desktop
4. Start coding!
```

**Option B: Using Python**
```bash
python ide_server.py
```
Then open: `http://localhost:5000`

### 2. Write Your First Program

```rijwal
When Program Starts:
    Print "Hello, World!"
```

Click **▶️ Run Code** → You're coding! 🎉

---

## Features

### ✨ Core Language Features
- ✅ Variables & Data Types (int, float, string, fraction)
- ✅ Functions with parameters
- ✅ User input
- ✅ String manipulation
- ✅ Timer/loops
- ✅ File imports
- ✅ Python integration
- ✅ JavaScript support (with Node.js)

### 🎨 IDE Features
- 📝 Syntax highlighting
- 📁 File explorer
- 📤 Console output
- 🖥️ Multi-tab editor
- 💾 Save/load projects
- 📚 Built-in documentation
- 🎓 Code examples

### 🛠️ Built-in Functions
```rijwal
len(x)              # String length
type(x)             # Get type
abs(x)              # Absolute value
max(a, b, ...)      # Maximum
min(a, b, ...)      # Minimum
round(x)            # Round number
str(x), int(x), float(x)  # Type conversion
upper(s), lower(s)  # Case conversion
split(s, sep)       # Split string
reverse(x)          # Reverse
sort(list)          # Sort list
```

---

## Examples

### 📊 Simple Calculator
```rijwal
When Program Starts:
    Input x
    Input y
    Print "Sum: " + (x + y)
```

### 🔢 Function Example
```rijwal
Function greet(name):
    Return "Hello, " + name

When Program Starts:
    Print greet("Alice")
```

### ⏱️ Timer Example
```rijwal
Every 1 second:
    Print "Tick!"
```

### 🌡️ Real Project
```rijwal
Function celsius_to_fahrenheit(c):
    Return c * 9/5 + 32

When Program Starts:
    Input celsius
    Let fahrenheit = celsius_to_fahrenheit(celsius)
    Print fahrenheit + "°F"
```

See more examples in the `/examples` folder!

---

## Installation

### Requirements
- **Windows, Mac, or Linux**
- **Python 3.6+** (if running from source)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **(Optional) Node.js** for JavaScript blocks

### Method 1: Windows Installer (Easiest)
```
1. Download: rijwal_lang_setup.exe
2. Double-click to install
3. Run Rijwal_Lang IDE from Start Menu
```

### Method 2: Python (Any OS)
```bash
# Download or clone the project
cd rijwal_lang

# Install dependencies
pip install flask

# Run the IDE server
python ide_server.py

# Open your browser
http://localhost:5000
```

### Method 3: Docker (Advanced)
```bash
docker build -t rijwal_lang .
docker run -p 5000:5000 rijwal_lang
```

---

## Documentation

### 📚 Available Docs
- **[TUTORIAL.md](TUTORIAL.md)** - Step-by-step lessons (recommended!)
- **[LANGUAGE_REFERENCE.md](LANGUAGE_REFERENCE.md)** - Complete language guide
- **IDE Help Tab** - Built-in quick reference

### Getting Help
- 📖 Check the tutorial
- 🔍 Look at examples folder
- ❓ Read the language reference
- 🐛 Check error messages

---

## Project Structure

```
rijwal_lang/
├── ide/                    # Web IDE
│   ├── index.html         # Main interface
│   ├── style.css          # Styling
│   └── editor.js          # Frontend logic
├── ide_server.py          # Python backend server
├── rijwal_lang_enhanced.py # Language engine (v0.13)
├── runner/                # Command-line runner
├── examples/              # Sample programs
├── TUTORIAL.md            # Beginner tutorial
├── LANGUAGE_REFERENCE.md  # Complete docs
└── README.md              # This file
```

---

## Version History

### v0.13 (Latest)
🎉 **Major Release!**
- ✨ Complete web-based IDE
- ✨ 13 built-in functions
- ✨ Better error messages
- ✨ Improved parsing
- 🐛 Fixed import resolution
- 🐛 Fixed string handling
- 📚 Full documentation

### v0.12
- Initial stable release
- Core language features
- Command-line runner

---

## Language Syntax Overview

### Entry Point
```rijwal
When Program Starts:
    # Your code here
```

### Variables
```rijwal
Let x = 5
Let name = "Alice"
```

### Output
```rijwal
Print "Hello"
Print x
Print x + y
```

### Input
```rijwal
Input age
```

### Functions
```rijwal
Function add(a, b):
    Return a + b
```

### Timers
```rijwal
Every 1 second:
    Print "Tick"
```

### Imports
```rijwal
Import "utils.RL"
```

---

## Troubleshooting

### IDE won't open
- Check Python version: `python --version` (needs 3.6+)
- Try different port: Edit `ide_server.py` line with `port=5000`
- Check if port 5000 is in use

### Code won't run
- Check indentation (spaces/tabs)
- Make sure functions are defined before use
- Check error message for line number

### Import not working
- Verify filename is correct
- Check file is in same directory
- Use `Import "filename.RL"` not `Import "filename"`

### Node.js errors for JS blocks
- Download Node.js from https://nodejs.org
- Add to PATH environment variable
- Restart IDE

---

## Contributing

Rijwal_Lang is open-source! Ways to help:

- 🐛 Report bugs
- 💡 Suggest features
- 📖 Improve documentation
- 🔧 Contribute code
- 🎓 Create tutorials

---

## License

Rijwal_Lang is released under the **FBAL License** - Free But Attribution License.

Use freely, but give credit! ❤️

---

## Credits

**Created by:** Rijwal  
**For:** Young developers everywhere who want to code  
**Made with:** ❤️ and Python

---

## FAQ

### Is Rijwal_Lang free?
✅ Yes! Completely free and open-source.

### Can I publish programs I write in Rijwal_Lang?
✅ Yes! Do whatever you want with your code.

### Can I modify Rijwal_Lang itself?
✅ Yes! It's open-source. Just give credit.

### What can I build with Rijwal_Lang?
- 🎮 Games (with extensions)
- 📊 Data programs
- 🤖 Automation scripts
- 🌐 Web projects (with Python)
- 📱 And much more!

### Is it as powerful as Python/JavaScript?
Not yet, but it's designed to be simple. For advanced features, you can use Python blocks!

---

## Getting Started Now

### For Complete Beginners:
1. Read [TUTORIAL.md](TUTORIAL.md)
2. Follow the lessons step-by-step
3. Try the practice challenges
4. Build your own projects

### For Experienced Programmers:
1. Skim [LANGUAGE_REFERENCE.md](LANGUAGE_REFERENCE.md)
2. Check examples folder
3. Start building!

---

## What's Next?

After learning Rijwal_Lang, you can:
- 🐍 Learn Python (similar syntax!)
- 🌐 Learn JavaScript for web
- 🎮 Learn game development
- 📊 Learn data science

Rijwal_Lang is the perfect stepping stone! 🚀

---

## Contact & Support

- 📧 Email: rijwal@example.com
- 🐛 Report Issues: GitHub Issues
- 💬 Discuss: GitHub Discussions
- 🌐 Website: www.rijwallang.com

---

<div align="center">

## Start Coding Now! 🚀

### [Download Rijwal_Lang](link-to-download) | [Open IDE](http://localhost:5000) | [Read Tutorial](TUTORIAL.md)

---

Made with ❤️ for young developers

**Happy Coding!** ✨

</div>

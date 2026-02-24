# Rijwal_Lang - The Language for Young Developers 🚀

<div align="center">

![Version](https://img.shields.io/badge/version-0.13-blue)
![License](https://img.shields.io/badge/license-FBAL-green)
![Status](https://img.shields.io/badge/status-Production-brightgreen)

**Rijwal is the fastest way for beginners to go from idea → working code with AI help.**

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
- Modern IDE: `/`
- Legacy IDE: `/legacy`
- IDLE info API: `/idle`
- Terminal API: `/api/terminal`
- Evolution API: `/api/evolve`
- Cloud Execute API: `/api/cloud/execute`
- Compile API: `/api/compile`
- Executable Export API: `/api/export/executable`
- Plugins API: `/api/plugins/list`, `/api/plugins/install`, `/api/plugins/auto-update`
- AI Prompt Update API: `/api/ai/prompt`
- VM Transition APIs: `/api/vm/compile`, `/api/vm/execute`
- Collaboration APIs: `/api/collab/session`, `/api/collab/op`
- Combined capabilities API: `/api/capabilities`

### 2. Write Your First Program

```rijwal
When Program Starts:
    Print "Hello, World!"
```

Click **▶️ Run Code** → You're coding! 🎉

Custom file format is supported too: `.rjwl` (next-gen Rijwal project file extension).

---


## ✅ Release Confidence Suite (Run on every change)

Before each release, run:

```bash
python -m py_compile ide_server.py rijwal_ai_assistant.py scripts/release_confidence_suite.py
python scripts/release_confidence_suite.py
```

If the suite fails, **do not release** until fixed.

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
- 🤖 Draggable AI Buddy (embedded mini local model + optional API providers)
- ⌨️ Custom Rijwal Terminal tab inside IDE
- 🧬 Evolution Lab for self-evolving language/AI roadmap
- ☁️ Cloud execution endpoint
- 🛠️ Tiny compiler + executable export
- 🧩 Extension / plugin API (self-growing local catalog)
- 🧠 AI prompt self-update and inline AI syntax support
- 🤝 Multiplayer collaboration session API (optimistic revision flow)
- 🧱 Interpreter → tiny VM transition path (`/api/vm/*`)
- 🧬 Adaptive syntax rules (`Adapt Syntax "old" => "new"`) persisted by runtime

### 🛠️ Built-in Functions
```rijwal
len(x)              # Length of string/container
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
contains(list_or_text, x) # Membership check
replace(s, old, new) # Replace text
startswith(s, prefix) # Starts with
endswith(s, suffix)  # Ends with
append(list, x)      # Return list with appended item
sum(a, b, ...)       # Sum numbers
keys(dict_obj)       # Dictionary keys
values(dict_obj)     # Dictionary values
clamp(x, min, max)   # Clamp number to range
sqrt(x), pow(a, b)   # Math helpers
randint(a, b)        # Random integer
choice(items)        # Random item
shuffle(list)        # Shuffled copy
trim(s), title(s)    # String cleanup
first(x), last(x)    # Sequence edges
take(x, n), drop(x,n)# Sequence slices
unique(list)         # Remove duplicates
count(x, v), index(x,v) # Count/find
now(), sleep(sec)    # Time helpers
iif(cond, a, b)      # Inline conditional
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

## Roadmap Highlights

- ✅ Expanded built-in function toolkit for math, random, text cleaning, list utilities, and time helpers.
- ✅ IDE docs endpoint now auto-syncs with runtime built-in docs to avoid drift.
- 🔜 Planned next: native `If/Else`, loops, and richer data-structure syntax.

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


### 3. Open IDLE (Interactive Shell)
```bash
python rijwal_idle.py
```
Use `:exit` to quit.

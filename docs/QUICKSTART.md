# 🚀 Quick Start Guide - Rijwal_Lang v0.13

## Installation (Choose One)

### Option 1: Windows Installer (Easiest)
```
1. Download rijwal_lang_setup.exe
2. Double-click to install
3. Run from Start Menu or Desktop
4. Browser opens automatically
```

### Option 2: Python (All Platforms)
```bash
# 1. Install Python 3.6+ from python.org
# 2. Download Rijwal_Lang
# 3. Open terminal/command prompt in rijwal_lang folder
# 4. Run setup:

python setup.py

# 5. Start the IDE:

python ide_server.py

# 6. Open browser to: http://localhost:5000
```

### Option 3: Docker
```bash
docker build -t rijwal_lang .
docker run -p 5000:5000 rijwal_lang
```

---

## First Steps (5 minutes)

### Step 1: Open IDE
- Click Rijwal_Lang icon (Windows) OR
- Go to `http://localhost:5000` in browser

### Step 2: Write Code
```rijwal
When Program Starts:
    Print "Hello, World!"
```

### Step 3: Run
Click **▶️ Run Code** button or press `Ctrl+Enter`

### Step 4: See Result
```
Hello, World!
```

🎉 **You're coding!**

---

## Learn More

### For Beginners
👉 Open **Help** tab in IDE or read [TUTORIAL.md](TUTORIAL.md)

### Complete Language Guide
👉 Read [LANGUAGE_REFERENCE.md](LANGUAGE_REFERENCE.md)

### Example Programs
👉 Check `/examples` folder in IDE

---

## Common Commands

| Action | How |
|--------|-----|
| Run code | Click ▶️ or press Ctrl+Enter |
| Create file | Click 📄 New |
| Open file | Click 📂 Open |
| Save file | Click 💾 Save |
| Clear output | Click 🗑️ Clear |
| See help | Click ❓ Help tab |
| View docs | Click 📚 Docs tab |

---

## Syntax Cheat Sheet

```rijwal
# Entry point
When Program Starts:
    # Code here runs automatically

# Variables
Let x = 5
Let name = "Alice"

# Output
Print "Hello"
Print x

# Input
Input age

# Functions
Function add(a, b):
    Return a + b

# Call function
Print add(5, 3)

# Timer (repeat)
Every 1 second:
    Print "Tick"

# Import file
Import "utils.RL"

# Comments
# This is a comment

# Python code
Python:
    import math
    x = math.sqrt(16)

# JavaScript code
JS:
    console.log("Hi")
```

---

## Troubleshooting

### "Port 5000 already in use"
Edit `ide_server.py`, find `port=5000`, change to `port=5001` (or any free port)

### "Python not found"
- Install Python 3.6+ from python.org
- Windows: Check "Add Python to PATH" during install

### "Code won't run"
- Check indentation (must be consistent)
- Check spelling of keywords
- Look at error message

### "File not found"
- Make sure `.Rijwal_lang` or `.RL` extension
- File must be in same directory
- Use `Import "filename.RL"` format

---

## IDE Overview

```
┌────────────────────────────────────────────────────┐
│ Header: New | Open | Save | Run | Clear            │
├─────────────┬──────────────────────────┬───────────┤
│   Files     │   Code Editor            │ Output    │
│ (Explorer)  │ (Write here)             │ (Results) │
│             │                          │           │
│             │                          │ Help/Docs │
└─────────────┴──────────────────────────┴───────────┘
```

---

## Example Programs to Try

1. **Calculator** - Basic math
2. **Temperature Converter** - Functions
3. **Fibonacci** - Loops
4. **Prime Finder** - Logic
5. **Word Game** - Strings

Open them from the Examples folder in IDE!

---

## What Next?

✅ Completed quick start?

### Next Steps:
1. 🎓 Do the [TUTORIAL.md](TUTORIAL.md) lessons
2. 💻 Try the example programs
3. 🎨 Build your own project
4. 📚 Read [LANGUAGE_REFERENCE.md](LANGUAGE_REFERENCE.md) for advanced features

---

## Need Help?

### In the IDE:
- Click **❓ Help** tab for quick reference
- Click **📚 Docs** tab for full documentation

### Online:
- 📖 Read [TUTORIAL.md](TUTORIAL.md)
- 📚 Read [LANGUAGE_REFERENCE.md](LANGUAGE_REFERENCE.md)
- 💬 Check example programs

---

## Tips

1. **Start simple** - Print, variables, input first
2. **Use functions** - Break code into reusable pieces
3. **Add comments** - Explain what your code does
4. **Test often** - Run code after each change
5. **Look at examples** - Learn from working programs

---

## You're Ready! 🚀

You now have everything to start coding in Rijwal_Lang!

**Happy Coding!** ✨

Questions? Check Help or read the docs! 📚

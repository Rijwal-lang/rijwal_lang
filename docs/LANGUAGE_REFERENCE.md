# 🚀 Rijwal_Lang - Complete Language Reference v0.13

## Table of Contents
1. [Getting Started](#getting-started)
2. [Language Basics](#language-basics)
3. [Data Types](#data-types)
4. [Statements](#statements)
5. [Functions](#functions)
6. [Built-in Functions](#built-in-functions)
7. [Advanced Features](#advanced-features)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Installation
1. Download Rijwal_Lang IDE
2. Extract the ZIP file
3. Run `rijwal_lang_ide.exe` (or `python ide_server.py`)
4. Open your browser to `http://localhost:5000`

### Your First Program
```rijwal
When Program Starts:
    Print "Hello, Rijwal_Lang!"
```

Click **Run Code** (or press `Ctrl+Enter`) to execute!

---

## Language Basics

### Comments
```rijwal
# This is a comment
```

### Case Insensitivity
Rijwal_Lang is **NOT case-sensitive** for keywords:
```rijwal
PRINT "Hello"
print "Hello"
Print "Hello"
# All work the same!
```

### Indentation
Use **indentation** (spaces or tabs) to mark code blocks:
```rijwal
When Program Starts:
    Print "Indented"
    Print "Still indented"
Print "Not indented - new block"
```

---

## Data Types

Rijwal_Lang supports these data types:

### 1. **Integer** (whole numbers)
```rijwal
Let x = 42
Let negative = -10
```

### 2. **Float** (decimal numbers)
```rijwal
Let pi = 3.14
Let decimal = -2.5
```

### 3. **Fraction** (ratios)
```rijwal
Let half = 1/2
Let third = 2/3
```

### 4. **String** (text)
```rijwal
Let name = "Alice"
Let greeting = "Hello, World!"
```

### 5. **Boolean** (true/false)
```rijwal
Let is_ready = true
Let is_empty = false
```

---

## Statements

### Print (Display Output)
```rijwal
Print "Hello"
Print 42
Print x  # Variable
Print "x = " + x  # Concatenation
```

**Output:**
```
Hello
42
5
x = 5
```

### Let (Create Variables)
```rijwal
Let x = 10
Let y = x + 5  # Use other variables
Let name = "Bob"
Let message = "Hello, " + name
```

### Input (Get User Input)
```rijwal
Input age
Print "You are " + age + " years old"
```

**When run:**
```
➤ age: 15
You are 15 years old
```

### When Program Starts (Entry Point)
This runs automatically when your program starts:
```rijwal
When Program Starts:
    Print "Program is starting!"
    Let x = 10
    Print x
```

---

## Functions

### Define a Function
```rijwal
Function greet(name):
    Return "Hello, " + name

Function add(a, b):
    Return a + b
```

### Call a Function
```rijwal
When Program Starts:
    Print greet("Alice")
    Print add(5, 3)
```

**Output:**
```
Hello, Alice
8
```

### Multi-line Function
```rijwal
Function calculate(x):
    Let squared = x * x
    Let doubled = x * 2
    Return squared + doubled

When Program Starts:
    Print calculate(5)  # 5*5 + 5*2 = 35
```

---

## Built-in Functions

### Type Conversion
```rijwal
Let s = str(42)        # "42"
Let i = int("100")     # 100
Let f = float("3.14")  # 3.14
```

### String Functions
```rijwal
Let upper = upper("hello")      # "HELLO"
Let lower = lower("WORLD")      # "world"
Let length = len("Rijwal")      # 6
Let parts = split("a,b,c", ",") # ["a", "b", "c"]
```

### Math Functions
```rijwal
Let absolute = abs(-5)     # 5
Let maximum = max(1, 5, 3) # 5
Let minimum = min(1, 5, 3) # 1
Let rounded = round(3.7)   # 4
```

### Utility Functions
```rijwal
Let t = type(42)           # "int"
Let reversed = reverse("hello")  # "olleh"
Let sorted = sort([3, 1, 2])     # [1, 2, 3]
```

---

## Advanced Features

### 1. Timer (Repeat Every N Seconds)
```rijwal
Every 2 second:
    Print "Tick"
```

This prints "Tick" every 2 seconds indefinitely. Press `Ctrl+C` to stop.

### 2. Import (Reuse Code)
**utils.Rijwal_lang:**
```rijwal
Function square(x):
    Return x * x
```

**main.Rijwal_lang:**
```rijwal
Import "utils.Rijwal_Lang"

When Program Starts:
    Print square(5)  # 25
```

### 3. Python Blocks (Advanced)
Mix Python code in your Rijwal_Lang program:
```rijwal
Let rijwal_var = 42

Python:
    import math
    rijwal_var = math.sqrt(rijwal_var)

Print rijwal_var
```

### 4. JavaScript Blocks (Requires Node.js)
```rijwal
JS:
    console.log("Hello from JavaScript!")
```

---

## Examples

### Example 1: Simple Calculator
```rijwal
When Program Starts:
    Input a
    Input b
    Let sum = a + b
    Print "Sum: " + sum
```

### Example 2: Function
```rijwal
Function celsius_to_fahrenheit(c):
    Return c * 9/5 + 32

When Program Starts:
    Input celsius
    Let fahrenheit = celsius_to_fahrenheit(celsius)
    Print fahrenheit
```

### Example 3: String Operations
```rijwal
When Program Starts:
    Let greeting = "hello world"
    Let upper_greeting = upper(greeting)
    Print upper_greeting  # HELLO WORLD
    
    Let words = split(greeting, " ")
    Print words  # ["hello", "world"]
```

### Example 4: Using Variables
```rijwal
Let pi = 3.14
Let radius = 5

Function circle_area(r):
    Return pi * r * r

When Program Starts:
    Let area = circle_area(radius)
    Print "Area: " + area
```

---

## Troubleshooting

### "File not found"
- Check the filename is correct
- Use `Import "filename.RL"` not `Import "filename"`
- Make sure the file is in the same directory

### "Syntax Error"
- Check indentation (spaces/tabs must be consistent)
- Make sure function names don't have spaces
- Use proper quotes: `"string"` or `'string'`

### "Variable not defined"
- Make sure you used `Let` before using a variable
- Check spelling (Rijwal_Lang is case-insensitive for keywords, but variables are case-sensitive)

### Program doesn't output anything
- Make sure you have `When Program Starts:` block
- Check `Print` statements are indented
- Use `Print` not `print`

### "Node.js not found"
- JavaScript blocks require Node.js installed
- Download from https://nodejs.org
- Add to PATH environment variable

---

## Tips & Tricks

### 1. Debug with Print
```rijwal
When Program Starts:
    Let x = 10
    Print "x = " + x  # Debug print
    Let y = x * 2
    Print "y = " + y
```

### 2. Use Descriptive Variable Names
```rijwal
# Bad
Let a = 5

# Good
Let user_age = 5
Let total_price = 99.99
```

### 3. Break Functions into Steps
```rijwal
Function process_user(age):
    Let is_adult = age >= 18
    Let category = "Adult"
    If not is_adult:
        Let category = "Child"
    Return category
```

### 4. Organize with Comments
```rijwal
# ===== SETUP =====
Let x = 10

# ===== PROCESSING =====
Function calculate(n):
    Return n * 2

# ===== OUTPUT =====
When Program Starts:
    Print calculate(x)
```

---

## Version History

### v0.13 (Current)
- ✨ Web IDE with syntax highlighting
- ✨ 13 built-in functions
- ✨ Better error messages
- ✨ Improved parser
- 🐛 Fixed import resolution
- 🐛 Fixed string parsing

### v0.12
- Initial stable release

---

## License
Rijwal_Lang is free and open-source. Made with ❤️ for young developers.

---

## Need Help?
- 📚 Read the docs on the IDE
- 💬 Check the examples folder
- 🐛 Report bugs with details

Happy coding! 🚀

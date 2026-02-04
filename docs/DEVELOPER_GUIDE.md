# 🔧 Rijwal_Lang Developer's Guide

This guide is for developers who want to understand, modify, or extend Rijwal_Lang.

## Table of Contents
1. [Architecture](#architecture)
2. [Code Structure](#code-structure)
3. [How It Works](#how-it-works)
4. [Adding Features](#adding-features)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

---

## Architecture

### Three-Layer Design

```
┌─────────────────────────────┐
│   IDE Layer (Web)           │  User Interface
│ (HTML/CSS/JavaScript)       │
└──────────────┬──────────────┘
               │ HTTP REST API
┌──────────────▼──────────────┐
│   Server Layer (Flask)      │  Request Handling
│ (Python web framework)      │
└──────────────┬──────────────┘
               │ Subprocess
┌──────────────▼──────────────┐
│   Engine Layer (Interpreter)│ Code Execution
│ (rijwal_lang_enhanced.py)   │
└─────────────────────────────┘
```

### Data Flow

```
User Types Code
       ↓
IDE sends via HTTP
       ↓
Flask server receives
       ↓
Creates temp file
       ↓
Runs rijwal_lang_enhanced.py
       ↓
Parser processes code
       ↓
Executes statements
       ↓
Returns output
       ↓
HTTP response to IDE
       ↓
Display in console
```

---

## Code Structure

### IDE Files (`ide/`)

#### `index.html`
- Main UI structure
- Tabs for editor, help, docs
- File explorer
- Console area
- Button layouts

#### `style.css`
- Professional dark theme
- Responsive layout
- Color scheme (purple/blue)
- Component styling

#### `editor.js`
- File management (create, open, save)
- Editor events (input, keyboard shortcuts)
- Code execution via fetch API
- Console output handling
- Local storage integration

### Engine File

#### `rijwal_lang_enhanced.py`
```
Global State
  ├── VARS (user variables)
  ├── FUNCS (user functions)
  ├── IMPORTED (imported files)
  └── BUILTIN_FUNCS (built-in functions)

Error Classes
  ├── RijwalError (base)
  ├── RijwalSyntaxError
  └── RijwalRuntimeError

Built-in Functions
  ├── Type conversion (str, int, float)
  ├── String functions (upper, lower, split, etc)
  ├── Math functions (abs, max, min, round)
  └── Utility functions (len, type, sort, reverse)

Core Functions
  ├── parse_input() - Convert string to type
  ├── safe_eval() - Safe expression evaluation
  ├── run_file() - Load and execute file
  ├── execute_lines() - Main interpreter loop
  ├── run_python() - Execute Python blocks
  └── run_js() - Execute JavaScript blocks

Main Entry Point
  └── main() - CLI interface
```

### Server File

#### `ide_server.py`
```
Routes
  ├── / → Serve IDE (index.html)
  ├── /api/execute → Run code
  ├── /api/save → Save file
  ├── /api/load → Load projects
  └── /api/docs → Get documentation

Error Handlers
  ├── 404 Not Found
  └── 500 Server Error
```

---

## How It Works

### 1. User Types Code

```rijwal
When Program Starts:
    Print "Hello"
```

### 2. IDE Processes

```javascript
// editor.js
fetch('/api/execute', {
    method: 'POST',
    body: JSON.stringify({
        code: editor.value,
        filename: currentFile
    })
})
```

### 3. Server Handles Request

```python
# ide_server.py
@app.route('/api/execute', methods=['POST'])
def execute_code():
    # Create temp file
    # Run rijwal_lang_enhanced.py
    # Capture output
    # Return JSON
```

### 4. Engine Parses Code

```python
# rijwal_lang_enhanced.py
execute_lines(lines, filename)
  → Parse "When Program Starts:"
  → Collect indented commands
  → Parse "Print" statement
  → Evaluate expression
```

### 5. Code Executes

```python
# Print statement
content = "Print \"Hello\""
m = re.match(r'print\s+(.+)', content, re.IGNORECASE)
result = safe_eval(m.group(1))
print(result)
```

### 6. Output Returns

```python
stdout = "Hello\n"
return {
    'success': True,
    'output': ['Hello']
}
```

### 7. IDE Displays

```javascript
// Display in console
addConsoleOutput('Hello', 'log')
```

---

## Adding Features

### Example: Add New Built-in Function

**Step 1: Define the function**

```python
# In rijwal_lang_enhanced.py, after builtin_sort:

def builtin_square(num):
    """Return square of number"""
    try:
        return float(num) ** 2
    except:
        raise RijwalTypeError(f"Cannot square {num}")
```

**Step 2: Register it**

```python
# In BUILTIN_FUNCS dictionary:

BUILTIN_FUNCS = {
    # ... existing functions ...
    'square': builtin_square,  # NEW
}
```

**Step 3: Test it**

```rijwal
When Program Starts:
    Print square(5)  # Should print 25
```

### Example: Add New Keyword

**Step 1: Add parsing logic**

```python
# In execute_lines(), in the non-indented section:

# RANDOM
m = re.match(r'random\s+(\d+)\s+to\s+(\d+)', low)
if m:
    min_val = int(m.group(1))
    max_val = int(m.group(2))
    import random
    result = random.randint(min_val, max_val)
    VARS['_last_random'] = result
    continue
```

**Step 2: Test it**

```rijwal
When Program Starts:
    Random 1 to 10
    Print _last_random
```

### Example: Add New Built-in Variable

```python
# Add to BUILTIN_FUNCS or special handling:

# After imports, add:
BUILTIN_VARS = {
    'PI': 3.14159,
    'E': 2.71828,
}

# In safe_eval, merge BUILTIN_VARS:
context = {**VARS, **BUILTIN_VARS, **local_vars, **BUILTIN_FUNCS}
```

---

## Testing

### Unit Testing Examples

**Test 1: Parse Input**
```python
from rijwal_lang_enhanced import parse_input

assert parse_input("42") == 42
assert parse_input("3.14") == 3.14
assert parse_input("1/2") == Fraction(1, 2)
assert parse_input("hello") == "hello"
```

**Test 2: Built-in Functions**
```python
from rijwal_lang_enhanced import builtin_upper, builtin_lower

assert builtin_upper("hello") == "HELLO"
assert builtin_lower("WORLD") == "world"
```

**Test 3: Integration**
```python
# Create test file
code = '''
When Program Starts:
    Let x = 5
    Print x
'''

# Run and capture output
result = execute_lines(code.split('\n'))
assert result == "5"
```

### Manual Testing Checklist

- [ ] Basic print statement
- [ ] Variable creation and use
- [ ] Function definition and call
- [ ] User input
- [ ] String operations
- [ ] Math operations
- [ ] Fractions
- [ ] Timer loops
- [ ] File imports
- [ ] Python blocks
- [ ] Error messages
- [ ] Edge cases

---

## Extending the IDE

### Add New Tab

**In index.html:**
```html
<button class="tab-btn" data-tab="custom">🎨 Custom</button>

<div id="custom" class="tab-content">
    <h3>Custom Tab Content</h3>
    <p>Your content here</p>
</div>
```

**In style.css:**
```css
#custom {
    /* Custom styling */
}
```

**In editor.js:**
```javascript
// The tab button handler already works!
```

### Add New Button

**In index.html:**
```html
<button id="customBtn" class="btn btn-primary">🎨 Custom</button>
```

**In editor.js:**
```javascript
document.getElementById('customBtn').addEventListener('click', () => {
    // Your code here
});
```

---

## Debugging

### Enable Debug Mode

```python
# In rijwal_lang_enhanced.py:
DEBUG = True  # Change to True

# Then run:
python rijwal_lang_enhanced.py your_file.Rijwal_lang
```

### Add Debug Output

```python
# In your code:
debug("Variable x is now: " + str(VARS['x']))
```

### IDE Console Tricks

```rijwal
When Program Starts:
    Let x = 5
    Print "DEBUG: x = " + x
    # Prints: DEBUG: x = 5
```

---

## Common Modifications

### Change Theme Color

**In style.css**, find and change:
```css
/* Current: Purple blue theme */
--primary: #667eea;
--secondary: #764ba2;

/* Change to your colors */
```

### Change Font

```css
body {
    font-family: 'Your Font Here', sans-serif;
}
```

### Add New Example

1. Create file in `examples/` folder
2. Name it `something.Rijwal_lang`
3. IDE will automatically list it

### Modify Error Messages

In `rijwal_lang_enhanced.py`, find error strings and customize them:

```python
print(f"[Rijwal_Lang] ❌ {error_message}")
# Change emoji or format
```

---

## Performance Tips

### Optimize Code
- Use `split()` instead of loops for strings
- Pre-calculate values instead of repeating in loops
- Use functions to avoid code duplication

### Reduce File Size
- Remove unused code
- Minify CSS/JavaScript (optional)
- Compress images (if added)

### Improve Speed
- Limit timer frequency (not less than 0.1 seconds)
- Avoid very large loops (>100,000 iterations)
- Close IDE tabs you're not using

---

## Architecture Decisions

### Why Web-Based?
- ✅ Cross-platform (Windows, Mac, Linux)
- ✅ No installation hassles
- ✅ Modern, responsive UI
- ✅ Easy to update

### Why Flask?
- ✅ Lightweight
- ✅ Python-native
- ✅ Great documentation
- ✅ Easy to extend

### Why Subprocess?
- ✅ Safe code isolation
- ✅ Timeout protection
- ✅ Resource limits
- ✅ Clean process management

---

## Roadmap (v0.14+)

### Planned Features
- [ ] Graphics library (drawing, colors)
- [ ] File I/O (read/write files)
- [ ] JSON support
- [ ] Basic networking
- [ ] Debugging mode with breakpoints
- [ ] Variable explorer
- [ ] Graphical program runner

### Performance Goals
- [ ] Syntax highlighting on-the-fly
- [ ] Code autocomplete
- [ ] Linting before execution
- [ ] Faster startup time

### UX Improvements
- [ ] Dark/light theme toggle
- [ ] Keyboard shortcut customization
- [ ] Project templates
- [ ] Code snippets library

---

## Contributing Guidelines

### Code Style
- Use clear variable names
- Add comments for complex logic
- Follow PEP 8 (Python)
- Keep functions small

### Testing
- Test your changes
- Add edge case tests
- Document expected behavior

### Documentation
- Update docs when changing features
- Add examples for new features
- Keep README.md current

---

## License & Attribution

Rijwal_Lang uses the **FBAL License** (Free But Attribution License).

If you modify or extend it:
1. Keep the license
2. Give credit to original author
3. Document your changes

---

## Support for Developers

### Debugging Queries
- Read error messages carefully
- Check line numbers
- Print intermediate values
- Test small pieces first

### Getting Help
- Check [LANGUAGE_REFERENCE.md](LANGUAGE_REFERENCE.md)
- Look at examples
- Read source code comments
- Ask in development community

---

## Conclusion

Rijwal_Lang is designed to be:
- **Simple** - Easy to understand
- **Extensible** - Easy to add features
- **Reliable** - Robust error handling
- **Modern** - Current tech stack

Happy developing! 🚀

---

**Questions?** Check the source code - it's well-commented! 💬

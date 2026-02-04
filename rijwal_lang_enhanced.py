# ==================================================
# Rijwal_Lang v0.13 - ENHANCED
# Improved Error Handling, Built-in Functions, Better Parsing
# ==================================================

import sys
import os
import re
import time
import subprocess
import shutil
import textwrap
from fractions import Fraction
from pathlib import Path

# ================ GLOBAL STATE ================

VARS = {}
FUNCS = {}
IMPORTED = set()
DEBUG = False
BUILTIN_FUNCS = {}

# ================ CONSTANTS ================

VERSION = "0.13"
EXTENSIONS = ['.Rijwal_lang', '.Rijwal_Lang', '.RL', '.rl']

# ================ ERROR HANDLING ================

class RijwalError(Exception):
    """Base exception for Rijwal_Lang"""
    pass

class RijwalSyntaxError(RijwalError):
    """Syntax error in Rijwal_Lang code"""
    def __init__(self, msg, line_num=None, line_content=None):
        self.line_num = line_num
        self.line_content = line_content
        if line_num:
            super().__init__(f"Syntax Error (Line {line_num}): {msg}\n  {line_content}")
        else:
            super().__init__(f"Syntax Error: {msg}")

class RijwalRuntimeError(RijwalError):
    """Runtime error during execution"""
    pass

class RijwalTypeError(RijwalRuntimeError):
    """Type mismatch error"""
    pass

def error(msg, line_num=None, line_content=None):
    raise RijwalSyntaxError(msg, line_num, line_content)

def warn(msg):
    print(f"[Rijwal_Lang] ⚠️  {msg}")

def debug(msg):
    if DEBUG:
        print(f"[DEBUG] {msg}")

# ================ BUILT-IN FUNCTIONS ================

def builtin_len(obj):
    """Return length of string or list"""
    return len(str(obj))

def builtin_type(obj):
    """Return type of object"""
    if isinstance(obj, int):
        return "int"
    elif isinstance(obj, float):
        return "float"
    elif isinstance(obj, Fraction):
        return "fraction"
    elif isinstance(obj, str):
        return "string"
    return "unknown"

def builtin_abs(num):
    """Return absolute value"""
    try:
        return abs(float(num))
    except:
        raise RijwalTypeError(f"Cannot get abs of {num}")

def builtin_max(*args):
    """Return maximum value"""
    if not args:
        raise RijwalRuntimeError("max() requires at least 1 argument")
    return max(args)

def builtin_min(*args):
    """Return minimum value"""
    if not args:
        raise RijwalRuntimeError("min() requires at least 1 argument")
    return min(args)

def builtin_round(num, decimals=0):
    """Round number"""
    try:
        return round(float(num), int(decimals))
    except:
        raise RijwalTypeError(f"Cannot round {num}")

def builtin_range_func(start, end=None, step=1):
    """Generate range of numbers"""
    if end is None:
        end = start
        start = 0
    return list(range(int(start), int(end), int(step)))

def builtin_str_func(obj):
    """Convert to string"""
    return str(obj)

def builtin_int_func(obj):
    """Convert to integer"""
    try:
        if isinstance(obj, str):
            return int(float(obj))
        return int(obj)
    except:
        raise RijwalTypeError(f"Cannot convert {obj} to int")

def builtin_float_func(obj):
    """Convert to float"""
    try:
        return float(obj)
    except:
        raise RijwalTypeError(f"Cannot convert {obj} to float")

def builtin_upper(s):
    """Convert string to uppercase"""
    return str(s).upper()

def builtin_lower(s):
    """Convert string to lowercase"""
    return str(s).lower()

def builtin_split(s, sep=" "):
    """Split string"""
    return str(s).split(sep)

def builtin_join(lst, sep=" "):
    """Join list to string"""
    return sep.join([str(x) for x in lst])

def builtin_reverse(lst):
    """Reverse a list or string"""
    if isinstance(lst, str):
        return lst[::-1]
    return list(reversed(lst))

def builtin_sort(lst):
    """Sort a list"""
    return sorted(lst)

# Register built-in functions
BUILTIN_FUNCS = {
    'len': builtin_len,
    'type': builtin_type,
    'abs': builtin_abs,
    'max': builtin_max,
    'min': builtin_min,
    'round': builtin_round,
    'range': builtin_range_func,
    'str': builtin_str_func,
    'int': builtin_int_func,
    'float': builtin_float_func,
    'upper': builtin_upper,
    'lower': builtin_lower,
    'split': builtin_split,
    'join': builtin_join,
    'reverse': builtin_reverse,
    'sort': builtin_sort,
}

# ================ HELPERS ================

def is_indented(line):
    """Check if line is indented"""
    return line.startswith(" ") or line.startswith("\t")

def resolve_file(name, base="."):
    """Resolve file path with case-insensitive search"""
    # Try exact path first
    if os.path.exists(name):
        return name
    
    # Try with extensions
    for ext in EXTENSIONS:
        if name.endswith(ext):
            break
    else:
        for ext in EXTENSIONS:
            test = name + ext
            if os.path.exists(test):
                return test
    
    # Search in directory
    for root, _, files in os.walk(base):
        for f in files:
            if f.lower() == name.lower():
                return os.path.join(root, f)
            # Try with extensions
            for ext in EXTENSIONS:
                if f.lower() == (name + ext).lower():
                    return os.path.join(root, f)
    
    return None

def parse_input(v):
    """Parse user input with type detection"""
    v = v.strip()
    
    # Try fraction
    if re.fullmatch(r'-?\d+/\d+', v):
        return Fraction(v)
    
    # Try float
    if re.fullmatch(r'-?\d+\.\d+', v):
        return float(v)
    
    # Try int
    if re.fullmatch(r'-?\d+', v):
        return int(v)
    
    # String
    return v

def safe_eval(expr, local_vars=None):
    """Safely evaluate expression"""
    try:
        if local_vars is None:
            local_vars = {}
        
        # Merge with VARS
        context = {**VARS, **local_vars, **BUILTIN_FUNCS}
        
        return eval(expr, {"__builtins__": {}}, context)
    except Exception as e:
        raise RijwalRuntimeError(f"Evaluation error: {e}")

# ================ PYTHON BLOCK ================

def run_python(lines):
    """Execute Python code block"""
    code = textwrap.dedent("\n".join(lines))
    try:
        exec(code, {}, VARS)
    except Exception as e:
        raise RijwalRuntimeError(f"Python error: {e}")

# ================ JS BLOCK ================

def run_js(lines):
    """Execute JavaScript code block"""
    node = shutil.which("node")
    if not node:
        warn("Node.js not found, JS skipped")
        return

    inject = ""
    for k, v in VARS.items():
        inject += f"var {k} = {repr(str(v))};\n"

    code = inject + "\n".join(lines)

    try:
        p = subprocess.Popen(
            ["node"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        out, err = p.communicate(code, timeout=10)
        if out:
            print(out.strip())
        if err:
            warn(f"JS error: {err.strip()}")
    except subprocess.TimeoutExpired:
        warn("JS execution timeout")
    except Exception as e:
        warn(f"JS execution failed: {e}")

# ================ CORE ENGINE ================

def run_file(path, line_offset=0):
    """Run a Rijwal_Lang file"""
    path = os.path.abspath(path)
    
    if path in IMPORTED:
        debug(f"Already imported: {path}")
        return
    
    IMPORTED.add(path)
    
    if not os.path.exists(path):
        raise RijwalError(f"File not found: {path}")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        raise RijwalError(f"Cannot read file {path}: {e}")
    
    # Parse and execute
    execute_lines(lines, path)

def execute_lines(lines, filename="<stdin>"):
    """Execute a list of code lines"""
    mode = None
    buffer = []
    current_func = None
    
    start_cmds = []
    python_blocks = []
    js_blocks = []
    timer_cmds = []
    timer_interval = None
    
    def flush():
        nonlocal buffer, mode
        if not buffer:
            return
        if mode == "python":
            python_blocks.append(buffer[:])
        elif mode == "js":
            js_blocks.append(buffer[:])
        elif mode == "function":
            FUNCS[current_func]["body"] = buffer[:]
        buffer.clear()
    
    for line_num, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")
        low = line.strip().lower()
        
        try:
            if not is_indented(raw):
                flush()
                
                # Skip empty lines and comments
                if not line.strip() or line.strip().startswith("#"):
                    continue
                
                # ===== IMPORT =====
                m = re.match(r'import\s+"(.+?)"', low)
                if m:
                    file = resolve_file(m.group(1), os.path.dirname(filename))
                    if file:
                        run_file(file, line_num)
                    else:
                        raise RijwalSyntaxError(f"Import not found: {m.group(1)}", line_num, line)
                    continue
                
                # ===== LET (Variable) =====
                m = re.match(r'let\s+(\w+)\s*=\s*(.+)', low)
                if m:
                    name, val = m.group(1), m.group(2)
                    try:
                        VARS[name] = safe_eval(val)
                    except:
                        VARS[name] = val.strip('"\'')
                    debug(f"Set {name} = {VARS[name]}")
                    continue
                
                # ===== INPUT =====
                m = re.match(r'input\s+(\w+)', low)
                if m:
                    var = m.group(1)
                    user = input(f"➤ {var}: ")
                    VARS[var] = parse_input(user)
                    continue
                
                # ===== FUNCTION =====
                m = re.match(r'function\s+(\w+)\s*\((.*?)\)\s*:', low)
                if m:
                    fname = m.group(1)
                    args = [a.strip() for a in m.group(2).split(",") if a.strip()]
                    FUNCS[fname] = {"args": args, "body": []}
                    current_func = fname
                    mode = "function"
                    debug(f"Defined function: {fname}({', '.join(args)})")
                    continue
                
                # ===== WHEN PROGRAM STARTS =====
                if low.startswith("when program starts"):
                    mode = "start"
                    continue
                
                # ===== TIMER =====
                m = re.match(r'every\s+(\d+)\s+second', low)
                if m:
                    timer_interval = int(m.group(1))
                    mode = "timer"
                    continue
                
                # ===== PYTHON BLOCK =====
                if low.startswith("python:"):
                    mode = "python"
                    continue
                
                # ===== JS BLOCK =====
                if low.startswith("js:"):
                    mode = "js"
                    continue
                
                mode = None
                
            # ===== INDENTED CONTENT =====
            else:
                content = line.strip()
                
                if mode == "start":
                    # Function call
                    m = re.match(r'print\s+(\w+)\s*\((.*?)\)', content, re.IGNORECASE)
                    if m and m.group(1) in FUNCS:
                        fname = m.group(1)
                        vals = [safe_eval(v.strip()) for v in m.group(2).split(",") if v.strip()]
                        func = FUNCS[fname]
                        local = dict(zip(func["args"], vals))
                        for c in func["body"]:
                            if c.lower().startswith("return "):
                                result = safe_eval(c[7:], local)
                                start_cmds.append(str(result))
                        continue
                    
                    # Print statement
                    m = re.match(r'print\s+(.+)', content, re.IGNORECASE)
                    if m:
                        expr = m.group(1)
                        # Remove quotes if string literal
                        if (expr.startswith('"') and expr.endswith('"')) or \
                           (expr.startswith("'") and expr.endswith("'")):
                            start_cmds.append(expr[1:-1])
                        else:
                            start_cmds.append(str(safe_eval(expr)))
                        continue
                
                elif mode == "timer":
                    m = re.match(r'print\s+(.+)', content, re.IGNORECASE)
                    if m:
                        expr = m.group(1)
                        if (expr.startswith('"') and expr.endswith('"')) or \
                           (expr.startswith("'") and expr.endswith("'")):
                            timer_cmds.append(expr[1:-1])
                        else:
                            timer_cmds.append(str(safe_eval(expr)))
                        continue
                
                elif mode in ("python", "js", "function"):
                    buffer.append(content)
        
        except RijwalError:
            raise
        except Exception as e:
            raise RijwalRuntimeError(f"Line {line_num}: {str(e)}\n  {line}")
    
    flush()
    
    # ===== EXECUTION =====
    try:
        for s in start_cmds:
            print(s)
        
        for b in python_blocks:
            run_python(b)
        
        for b in js_blocks:
            run_js(b)
        
        if timer_interval and timer_cmds:
            print(f"[Rijwal_Lang] ⏱️  Timer: every {timer_interval} second(s)")
            try:
                while True:
                    for t in timer_cmds:
                        print(t)
                    time.sleep(timer_interval)
            except KeyboardInterrupt:
                print("\n[Rijwal_Lang] ⏹️  Timer stopped")
    
    except Exception as e:
        raise RijwalRuntimeError(str(e))

# ================ MAIN ================

def main():
    if len(sys.argv) < 2:
        print(f"Rijwal_Lang v{VERSION}")
        print("Usage: rijwal_lang <file.Rijwal_Lang>")
        return
    
    file = sys.argv[1]
    resolved = resolve_file(file)
    
    if not resolved:
        print(f"[Rijwal_Lang ERROR] File not found: {file}")
        return
    
    print(f"[Rijwal_Lang] 🚀 v{VERSION} - Running {os.path.basename(resolved)}")
    
    try:
        run_file(resolved)
        print("\n[Rijwal_Lang] ✅ Completed")
    except RijwalError as e:
        print(f"\n[Rijwal_Lang] ❌ {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[Rijwal_Lang] ⏹️  Interrupted by user")
    except Exception as e:
        print(f"\n[Rijwal_Lang] 💥 Unexpected error: {e}")
        if DEBUG:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

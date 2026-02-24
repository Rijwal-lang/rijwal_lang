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
import math
import random
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
    """Return length of a string or container"""
    if isinstance(obj, (str, list, tuple, dict, set)):
        return len(obj)
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

def builtin_sum(*args):
    """Return sum of numeric values"""
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        return sum(args[0])
    return sum(args)

def builtin_append(lst, item):
    """Append an item to a list and return a new list"""
    if not isinstance(lst, list):
        raise RijwalTypeError("append() expects a list as first argument")
    return [*lst, item]

def builtin_contains(container, item):
    """Check whether item is inside a container"""
    return item in container

def builtin_replace(text, old, new):
    """Replace text inside a string"""
    return str(text).replace(str(old), str(new))

def builtin_startswith(text, prefix):
    """Check if string starts with prefix"""
    return str(text).startswith(str(prefix))

def builtin_endswith(text, suffix):
    """Check if string ends with suffix"""
    return str(text).endswith(str(suffix))

def builtin_keys(obj):
    """Return dictionary keys as a list"""
    if not isinstance(obj, dict):
        raise RijwalTypeError("keys() expects a dictionary")
    return list(obj.keys())

def builtin_values(obj):
    """Return dictionary values as a list"""
    if not isinstance(obj, dict):
        raise RijwalTypeError("values() expects a dictionary")
    return list(obj.values())

def builtin_clamp(value, min_value, max_value):
    """Clamp a number into a min/max range"""
    value = float(value)
    return max(float(min_value), min(float(max_value), value))

def builtin_sqrt(value):
    """Square root"""
    return math.sqrt(float(value))

def builtin_pow(base, exponent):
    """Power operation"""
    return math.pow(float(base), float(exponent))

def builtin_randint(a, b):
    """Random integer (inclusive)"""
    return random.randint(int(a), int(b))

def builtin_choice(items):
    """Random choice from a list/string"""
    return random.choice(items)

def builtin_shuffle(items):
    """Return shuffled copy of list"""
    if not isinstance(items, list):
        raise RijwalTypeError("shuffle() expects a list")
    out = items[:]
    random.shuffle(out)
    return out

def builtin_trim(text):
    """Trim spaces from both ends"""
    return str(text).strip()

def builtin_lstrip(text):
    """Trim spaces from left"""
    return str(text).lstrip()

def builtin_rstrip(text):
    """Trim spaces from right"""
    return str(text).rstrip()

def builtin_title(text):
    """Convert to title case"""
    return str(text).title()

def builtin_isdigit(text):
    """Check if all characters are digits"""
    return str(text).isdigit()

def builtin_isalpha(text):
    """Check if all characters are letters"""
    return str(text).isalpha()

def builtin_first(items):
    """Return first item"""
    return items[0]

def builtin_last(items):
    """Return last item"""
    return items[-1]

def builtin_take(items, n):
    """Take first n items"""
    return items[:int(n)]

def builtin_drop(items, n):
    """Drop first n items"""
    return items[int(n):]

def builtin_unique(items):
    """Return unique values while preserving order"""
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out

def builtin_count(items, value):
    """Count occurrences"""
    return items.count(value)

def builtin_index(items, value):
    """Find first index of value"""
    return items.index(value)

def builtin_now():
    """Current Unix timestamp"""
    return int(time.time())

def builtin_sleep(seconds):
    """Sleep for N seconds"""
    time.sleep(float(seconds))
    return None

def builtin_iif(condition, true_value, false_value):
    """Inline if expression"""
    return true_value if condition else false_value

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
    'sum': builtin_sum,
    'append': builtin_append,
    'contains': builtin_contains,
    'replace': builtin_replace,
    'startswith': builtin_startswith,
    'endswith': builtin_endswith,
    'keys': builtin_keys,
    'values': builtin_values,
    'clamp': builtin_clamp,
    'sqrt': builtin_sqrt,
    'pow': builtin_pow,
    'randint': builtin_randint,
    'choice': builtin_choice,
    'shuffle': builtin_shuffle,
    'trim': builtin_trim,
    'lstrip': builtin_lstrip,
    'rstrip': builtin_rstrip,
    'title': builtin_title,
    'isdigit': builtin_isdigit,
    'isalpha': builtin_isalpha,
    'first': builtin_first,
    'last': builtin_last,
    'take': builtin_take,
    'drop': builtin_drop,
    'unique': builtin_unique,
    'count': builtin_count,
    'index': builtin_index,
    'now': builtin_now,
    'sleep': builtin_sleep,
    'iif': builtin_iif,
}

BUILTIN_DOCS = {
    'len(x)': 'Length of string/container',
    'type(x)': 'Get type of value',
    'abs(x)': 'Absolute value',
    'max(a, b, ...)': 'Maximum value',
    'min(a, b, ...)': 'Minimum value',
    'round(x, decimals=0)': 'Round number',
    'range(start, end=None, step=1)': 'Generate range list',
    'str(x)': 'Convert to string',
    'int(x)': 'Convert to integer',
    'float(x)': 'Convert to float',
    'upper(s)': 'Uppercase string',
    'lower(s)': 'Lowercase string',
    'split(s, sep=" ")': 'Split string',
    'join(list, sep=" ")': 'Join list to string',
    'reverse(x)': 'Reverse string/list',
    'sort(list)': 'Sort list values',
    'sum(a, b, ...)': 'Sum numbers',
    'append(list, item)': 'Return list with appended item',
    'contains(container, item)': 'Membership check',
    'replace(text, old, new)': 'Replace text',
    'startswith(text, prefix)': 'Check starts with prefix',
    'endswith(text, suffix)': 'Check ends with suffix',
    'keys(dict)': 'Dictionary keys',
    'values(dict)': 'Dictionary values',
    'clamp(value, min, max)': 'Clamp a number to range',
    'sqrt(x)': 'Square root',
    'pow(base, exponent)': 'Power',
    'randint(a, b)': 'Random integer (inclusive)',
    'choice(items)': 'Random choice from sequence',
    'shuffle(list)': 'Shuffled list copy',
    'trim(text)': 'Trim spaces on both ends',
    'lstrip(text)': 'Trim spaces on left',
    'rstrip(text)': 'Trim spaces on right',
    'title(text)': 'Title-case text',
    'isdigit(text)': 'Whether string is all digits',
    'isalpha(text)': 'Whether string is all letters',
    'first(items)': 'First item in sequence',
    'last(items)': 'Last item in sequence',
    'take(items, n)': 'First n items',
    'drop(items, n)': 'Items after first n',
    'unique(items)': 'Remove duplicates preserve order',
    'count(items, value)': 'Count value occurrences',
    'index(items, value)': 'First index of value',
    'now()': 'Current Unix timestamp',
    'sleep(seconds)': 'Pause execution',
    'iif(condition, true_value, false_value)': 'Inline conditional selection',
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

def split_arguments(arg_string):
    """Split comma-separated function arguments while respecting nesting and quotes."""
    if not arg_string.strip():
        return []

    args = []
    current = []
    depth = 0
    in_quote = None
    escape = False

    for ch in arg_string:
        if escape:
            current.append(ch)
            escape = False
            continue

        if ch == "\\":
            current.append(ch)
            escape = True
            continue

        if in_quote:
            current.append(ch)
            if ch == in_quote:
                in_quote = None
            continue

        if ch in ('"', "'"):
            in_quote = ch
            current.append(ch)
            continue

        if ch in '([{':
            depth += 1
            current.append(ch)
            continue

        if ch in ')]}':
            depth = max(0, depth - 1)
            current.append(ch)
            continue

        if ch == ',' and depth == 0:
            token = ''.join(current).strip()
            if token:
                args.append(token)
            current = []
            continue

        current.append(ch)

    token = ''.join(current).strip()
    if token:
        args.append(token)

    return args


def parse_assignment_value(value_expr):
    """Evaluate assignment expression, preserving quoted string literals."""
    expr = value_expr.strip()
    if (expr.startswith('"') and expr.endswith('"')) or        (expr.startswith("'") and expr.endswith("'")):
        return expr[1:-1]
    return safe_eval(expr)

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

        user_funcs = {
            fname: (lambda *vals, _fname=fname: call_function_values(_fname, list(vals)))
            for fname in FUNCS
        }

        # Merge with VARS
        context = {
            **VARS,
            **local_vars,
            **BUILTIN_FUNCS,
            **user_funcs,
            "true": True,
            "false": False,
            "null": None,
        }

        return eval(expr, {"__builtins__": {}}, context)
    except RijwalError:
        raise
    except Exception as e:
        raise RijwalRuntimeError(f"Evaluation error: {e}")

def call_function_values(name, arg_values=None):
    """Call a user-defined function with already-evaluated argument values."""
    if arg_values is None:
        arg_values = []

    if name not in FUNCS:
        raise RijwalRuntimeError(f"Function not defined: {name}")

    func = FUNCS[name]
    if len(arg_values) != len(func["args"]):
        raise RijwalRuntimeError(
            f"Function '{name}' expects {len(func['args'])} argument(s), got {len(arg_values)}"
        )

    local = dict(zip(func["args"], arg_values))

    for stmt in func["body"]:
        if stmt.lower().startswith("return "):
            return safe_eval(stmt[7:], local)
    return None

def call_function(name, arg_exprs=None):
    """Call a user-defined function and return its return value (if any)."""
    if arg_exprs is None:
        arg_exprs = []

    if name not in FUNCS:
        raise RijwalRuntimeError(f"Function not defined: {name}")

    values = [safe_eval(arg.strip()) for arg in arg_exprs if arg.strip()]
    return call_function_values(name, values)

def execute_block_command(content, output_buffer=None):
    """Execute one command inside start/timer blocks."""
    if output_buffer is None:
        output_buffer = []

    # Print function_call(...)
    m = re.match(r'print\s+(\w+)\s*\((.*?)\)\s*$', content, re.IGNORECASE)
    if m and m.group(1) in FUNCS:
        fname = m.group(1)
        arg_exprs = split_arguments(m.group(2))
        result = call_function(fname, arg_exprs)
        output_buffer.append("" if result is None else str(result))
        return

    # Plain function call
    m = re.match(r'(\w+)\s*\((.*?)\)\s*$', content, re.IGNORECASE)
    if m and m.group(1) in FUNCS:
        fname = m.group(1)
        arg_exprs = split_arguments(m.group(2))
        call_function(fname, arg_exprs)
        return

    # Let assignment
    m = re.match(r'let\s+(\w+)\s*=\s*(.+)', content, re.IGNORECASE)
    if m:
        name, val = m.group(1), m.group(2)
        VARS[name] = parse_assignment_value(val)
        return

    # Input
    m = re.match(r'input\s+(\w+)', content, re.IGNORECASE)
    if m:
        var = m.group(1)
        user = input(f"➤ {var}: ")
        VARS[var] = parse_input(user)
        return

    # Print expression/string
    m = re.match(r'print\s+(.+)', content, re.IGNORECASE)
    if m:
        expr = m.group(1)
        if (expr.startswith('"') and expr.endswith('"')) or \
           (expr.startswith("'") and expr.endswith("'")):
            output_buffer.append(expr[1:-1])
        else:
            output_buffer.append(str(safe_eval(expr)))
        return

    raise RijwalSyntaxError(f"Unsupported statement in block: {content}")

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
        stripped = line.strip()
        low = stripped.lower()
        
        try:
            if not is_indented(raw):
                flush()
                
                # Skip empty lines and comments
                if not line.strip() or line.strip().startswith("#"):
                    continue
                
                # ===== IMPORT =====
                m = re.match(r'import\s+"(.+?)"', stripped, re.IGNORECASE)
                if m:
                    file = resolve_file(m.group(1), os.path.dirname(filename))
                    if file:
                        run_file(file, line_num)
                    else:
                        raise RijwalSyntaxError(f"Import not found: {m.group(1)}", line_num, line)
                    continue
                
                # ===== LET (Variable) =====
                m = re.match(r'let\s+(\w+)\s*=\s*(.+)', stripped, re.IGNORECASE)
                if m:
                    name, val = m.group(1), m.group(2)
                    VARS[name] = parse_assignment_value(val)
                    debug(f"Set {name} = {VARS[name]}")
                    continue
                
                # ===== INPUT =====
                m = re.match(r'input\s+(\w+)', stripped, re.IGNORECASE)
                if m:
                    var = m.group(1)
                    user = input(f"➤ {var}: ")
                    VARS[var] = parse_input(user)
                    continue
                
                # ===== FUNCTION =====
                m = re.match(r'function\s+(\w+)\s*\((.*?)\)\s*:', stripped, re.IGNORECASE)
                if m:
                    fname = m.group(1)
                    args = split_arguments(m.group(2))
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
                m = re.match(r'every\s+(\d+)\s+second', stripped, re.IGNORECASE)
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
                    execute_block_command(content, start_cmds)
                    continue

                elif mode == "timer":
                    timer_cmds.append(content)
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
                    timer_output = []
                    for t in timer_cmds:
                        execute_block_command(t, timer_output)
                    for out in timer_output:
                        print(out)
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

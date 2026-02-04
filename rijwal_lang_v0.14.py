# ==================================================
# Rijwal_Lang v0.14 - SUPER ENHANCED (50+ Features!)
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
LOOP_CONTROL = None  # For break/continue

# ================ CONSTANTS ================

VERSION = "0.14"
EXTENSIONS = ['.Rijwal_lang', '.Rijwal_Lang', '.RL', '.rl']

# ================ ERROR HANDLING ================

class RijwalError(Exception):
    pass

class RijwalSyntaxError(RijwalError):
    def __init__(self, msg, line_num=None, line_content=None):
        self.line_num = line_num
        self.line_content = line_content
        if line_num:
            super().__init__(f"Syntax Error (Line {line_num}): {msg}\n  {line_content}")
        else:
            super().__init__(f"Syntax Error: {msg}")

class RijwalRuntimeError(RijwalError):
    pass

class RijwalTypeError(RijwalRuntimeError):
    pass

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

def error(msg, line_num=None, line_content=None):
    raise RijwalSyntaxError(msg, line_num, line_content)

def warn(msg):
    print(f"[Rijwal_Lang] ⚠️  {msg}")

def debug(msg):
    if DEBUG:
        print(f"[DEBUG] {msg}")

# ================ 50+ BUILT-IN FUNCTIONS ================

# STRING FUNCTIONS (10)
def builtin_len(obj):
    return len(str(obj))

def builtin_upper(s):
    return str(s).upper()

def builtin_lower(s):
    return str(s).lower()

def builtin_split(s, sep=" "):
    return str(s).split(sep)

def builtin_join(lst, sep=" "):
    return sep.join([str(x) for x in lst])

def builtin_reverse(lst):
    if isinstance(lst, str):
        return lst[::-1]
    return list(reversed(lst))

def builtin_capitalize(s):
    return str(s).capitalize()

def builtin_strip(s):
    return str(s).strip()

def builtin_replace(s, old, new):
    return str(s).replace(old, new)

def builtin_find(s, substr):
    return str(s).find(substr)

# MATH FUNCTIONS (15)
def builtin_abs(num):
    return abs(float(num))

def builtin_round(num, decimals=0):
    return round(float(num), int(decimals))

def builtin_floor(num):
    return math.floor(float(num))

def builtin_ceil(num):
    return math.ceil(float(num))

def builtin_sqrt(num):
    return math.sqrt(float(num))

def builtin_pow(base, exp):
    return pow(float(base), float(exp))

def builtin_sin(angle):
    return math.sin(float(angle))

def builtin_cos(angle):
    return math.cos(float(angle))

def builtin_tan(angle):
    return math.tan(float(angle))

def builtin_sum_func(*args):
    return sum(float(x) for x in args)

def builtin_avg(*args):
    if not args:
        return 0
    return sum(float(x) for x in args) / len(args)

def builtin_max(*args):
    return max(args) if args else 0

def builtin_min(*args):
    return min(args) if args else 0

def builtin_random_func():
    return random.random()

def builtin_randint(a, b):
    return random.randint(int(a), int(b))

# TYPE FUNCTIONS (8)
def builtin_type(obj):
    if isinstance(obj, int):
        return "int"
    elif isinstance(obj, float):
        return "float"
    elif isinstance(obj, Fraction):
        return "fraction"
    elif isinstance(obj, str):
        return "string"
    elif isinstance(obj, list):
        return "list"
    elif isinstance(obj, dict):
        return "dict"
    return "unknown"

def builtin_str_func(obj):
    return str(obj)

def builtin_int_func(obj):
    try:
        if isinstance(obj, str):
            return int(float(obj))
        return int(obj)
    except:
        raise RijwalTypeError(f"Cannot convert {obj} to int")

def builtin_float_func(obj):
    try:
        return float(obj)
    except:
        raise RijwalTypeError(f"Cannot convert {obj} to float")

def builtin_bool_func(obj):
    return bool(obj)

def builtin_list_func(obj):
    if isinstance(obj, list):
        return obj
    if isinstance(obj, str):
        return list(obj)
    return [obj]

def builtin_dict_func():
    return {}

def builtin_is_int(obj):
    return isinstance(obj, int)

# LIST FUNCTIONS (12)
def builtin_sort(lst):
    if isinstance(lst, list):
        return sorted(lst)
    return lst

def builtin_sort_desc(lst):
    if isinstance(lst, list):
        return sorted(lst, reverse=True)
    return lst

def builtin_append(lst, item):
    if isinstance(lst, list):
        lst.append(item)
    return lst

def builtin_pop(lst):
    if isinstance(lst, list) and len(lst) > 0:
        return lst.pop()
    return None

def builtin_index(lst, item):
    if isinstance(lst, (list, str)):
        try:
            return lst.index(item)
        except:
            return -1
    return -1

def builtin_count(lst, item):
    if isinstance(lst, (list, str)):
        return lst.count(item)
    return 0

def builtin_slice(lst, start, end):
    return lst[int(start):int(end)]

def builtin_first(lst):
    if isinstance(lst, (list, str)) and len(lst) > 0:
        return lst[0]
    return None

def builtin_last(lst):
    if isinstance(lst, (list, str)) and len(lst) > 0:
        return lst[-1]
    return None

def builtin_unique(lst):
    if isinstance(lst, list):
        return list(dict.fromkeys(lst))
    return lst

def builtin_flatten(lst):
    if not isinstance(lst, list):
        return lst
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result

def builtin_zip_func(*lists):
    return list(zip(*lists))

# UTILITY FUNCTIONS (8)
def builtin_range_func(start, end=None, step=1):
    if end is None:
        end = start
        start = 0
    return list(range(int(start), int(end), int(step)))

def builtin_enumerate_func(lst):
    if isinstance(lst, (list, str)):
        return list(enumerate(lst))
    return []

def builtin_any_func(*args):
    return any(args)

def builtin_all_func(*args):
    return all(args)

def builtin_print_func(*args):
    for arg in args:
        print(arg)
    return None

def builtin_input_func(prompt=""):
    return input(str(prompt))

def builtin_len_list(lst):
    return len(lst) if isinstance(lst, (list, str, dict)) else 0

def builtin_pi():
    return math.pi

# Register all built-in functions
BUILTIN_FUNCS = {
    # String functions
    'len': builtin_len,
    'upper': builtin_upper,
    'lower': builtin_lower,
    'split': builtin_split,
    'join': builtin_join,
    'reverse': builtin_reverse,
    'capitalize': builtin_capitalize,
    'strip': builtin_strip,
    'replace': builtin_replace,
    'find': builtin_find,
    
    # Math functions
    'abs': builtin_abs,
    'round': builtin_round,
    'floor': builtin_floor,
    'ceil': builtin_ceil,
    'sqrt': builtin_sqrt,
    'pow': builtin_pow,
    'sin': builtin_sin,
    'cos': builtin_cos,
    'tan': builtin_tan,
    'sum': builtin_sum_func,
    'avg': builtin_avg,
    'max': builtin_max,
    'min': builtin_min,
    'random': builtin_random_func,
    'randint': builtin_randint,
    
    # Type functions
    'type': builtin_type,
    'str': builtin_str_func,
    'int': builtin_int_func,
    'float': builtin_float_func,
    'bool': builtin_bool_func,
    'list': builtin_list_func,
    'dict': builtin_dict_func,
    'is_int': builtin_is_int,
    
    # List functions
    'sort': builtin_sort,
    'sort_desc': builtin_sort_desc,
    'append': builtin_append,
    'pop': builtin_pop,
    'index': builtin_index,
    'count': builtin_count,
    'slice': builtin_slice,
    'first': builtin_first,
    'last': builtin_last,
    'unique': builtin_unique,
    'flatten': builtin_flatten,
    'zip': builtin_zip_func,
    
    # Utility functions
    'range': builtin_range_func,
    'enumerate': builtin_enumerate_func,
    'any': builtin_any_func,
    'all': builtin_all_func,
    'pi': builtin_pi,
}

# ================ HELPERS ================

def is_indented(line):
    return line.startswith(" ") or line.startswith("\t")

def resolve_file(name, base="."):
    if os.path.exists(name):
        return name
    for ext in EXTENSIONS:
        if name.endswith(ext):
            break
    else:
        for ext in EXTENSIONS:
            test = name + ext
            if os.path.exists(test):
                return test
    for root, _, files in os.walk(base):
        for f in files:
            if f.lower() == name.lower():
                return os.path.join(root, f)
            for ext in EXTENSIONS:
                if f.lower() == (name + ext).lower():
                    return os.path.join(root, f)
    return None

def parse_input(v):
    v = v.strip()
    if re.fullmatch(r'-?\d+/\d+', v):
        return Fraction(v)
    if re.fullmatch(r'-?\d+\.\d+', v):
        return float(v)
    if re.fullmatch(r'-?\d+', v):
        return int(v)
    return v

def safe_eval(expr, local_vars=None):
    try:
        if local_vars is None:
            local_vars = {}
        context = {**VARS, **local_vars, **BUILTIN_FUNCS}
        return eval(expr, {"__builtins__": {}}, context)
    except Exception as e:
        raise RijwalRuntimeError(f"Evaluation error: {e}")

# ================ EXECUTION ================

def run_file(path, line_offset=0):
    path = os.path.abspath(path)
    if path in IMPORTED:
        return
    IMPORTED.add(path)
    if not os.path.exists(path):
        raise RijwalError(f"File not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        raise RijwalError(f"Cannot read file {path}: {e}")
    execute_lines(lines, path)

def execute_lines(lines, filename="<stdin>"):
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
    
    i = 0
    while i < len(lines):
        raw = lines[i]
        i += 1
        line = raw.rstrip("\n")
        low = line.strip().lower()
        
        try:
            if not is_indented(raw):
                flush()
                
                if not line.strip() or line.strip().startswith("#"):
                    continue
                
                # IMPORT
                m = re.match(r'import\s+"(.+?)"', low)
                if m:
                    file = resolve_file(m.group(1), os.path.dirname(filename))
                    if file:
                        run_file(file, i)
                    else:
                        raise RijwalSyntaxError(f"Import not found: {m.group(1)}", i, line)
                    continue
                
                # LET (Variable)
                m = re.match(r'let\s+(\w+)\s*=\s*(.+)', low)
                if m:
                    name, val = m.group(1), m.group(2)
                    try:
                        VARS[name] = safe_eval(val)
                    except:
                        VARS[name] = val.strip('"\'')
                    continue
                
                # INPUT
                m = re.match(r'input\s+(\w+)', low)
                if m:
                    var = m.group(1)
                    user = input(f"➤ {var}: ")
                    VARS[var] = parse_input(user)
                    continue
                
                # FUNCTION
                m = re.match(r'function\s+(\w+)\s*\((.*?)\)\s*:', low)
                if m:
                    fname = m.group(1)
                    args = [a.strip() for a in m.group(2).split(",") if a.strip()]
                    FUNCS[fname] = {"args": args, "body": []}
                    current_func = fname
                    mode = "function"
                    continue
                
                # IF/ELSE
                m = re.match(r'if\s+(.+):', low)
                if m:
                    condition = m.group(1)
                    try:
                        result = safe_eval(condition)
                        if not result:
                            # Skip until next elif/else/endif
                            indent_level = len(raw) - len(raw.lstrip())
                            while i < len(lines):
                                next_line = lines[i]
                                next_low = next_line.strip().lower()
                                if (next_low.startswith('elif ') or next_low.startswith('else')) and not is_indented(next_line):
                                    break
                                i += 1
                    except:
                        pass
                    continue
                
                # FOR LOOP
                m = re.match(r'for\s+(\w+)\s+in\s+(.+):', low)
                if m:
                    var = m.group(1)
                    iterable = safe_eval(m.group(2))
                    loop_start = i
                    for item in iterable:
                        VARS[var] = item
                        i = loop_start
                        while i < len(lines):
                            loop_line = lines[i].rstrip('\n')
                            if not is_indented(lines[i]):
                                break
                            execute_lines([loop_line], filename)
                            i += 1
                    continue
                
                # WHILE LOOP
                m = re.match(r'while\s+(.+):', low)
                if m:
                    condition = m.group(1)
                    loop_start = i
                    while True:
                        try:
                            result = safe_eval(condition)
                            if not result:
                                break
                        except:
                            break
                        i = loop_start
                        while i < len(lines):
                            loop_line = lines[i].rstrip('\n')
                            if not is_indented(lines[i]):
                                break
                            execute_lines([loop_line], filename)
                            i += 1
                    continue
                
                # WHEN PROGRAM STARTS
                if low.startswith("when program starts"):
                    mode = "start"
                    continue
                
                # TIMER
                m = re.match(r'every\s+(\d+)\s+second', low)
                if m:
                    timer_interval = int(m.group(1))
                    mode = "timer"
                    continue
                
                # PYTHON / JS
                if low.startswith("python:"):
                    mode = "python"
                    continue
                if low.startswith("js:"):
                    mode = "js"
                    continue
                
                mode = None
            
            else:
                content = line.strip()
                
                if mode == "start":
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
                    
                    m = re.match(r'print\s+(.+)', content, re.IGNORECASE)
                    if m:
                        expr = m.group(1)
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
            raise RijwalRuntimeError(f"Line {i}: {str(e)}\n  {line}")
    
    flush()
    
    # EXECUTION
    try:
        for s in start_cmds:
            print(s)
        
        for b in python_blocks:
            code = textwrap.dedent("\n".join(b))
            exec(code, {}, VARS)
        
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
        sys.exit(1)

if __name__ == "__main__":
    main()

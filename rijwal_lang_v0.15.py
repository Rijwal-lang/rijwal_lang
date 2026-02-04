#!/usr/bin/env python3
"""
Rijwal_Lang v0.15 - ULTIMATE EDITION
Complete Programming Language with 100+ Features
File I/O, System Commands, Graphics, Database, Network, and MORE!

Author: Rijwal
Version: 0.15
License: MIT
"""

import sys
import os
import re
import json
import math
import random
import subprocess
import threading
import time
import hashlib
import base64
import zlib
import sqlite3
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urljoin
import urllib.error

VERSION = "0.15"

# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class RijwalError(Exception):
    """Base exception for Rijwal_Lang"""
    pass

class RijwalSyntaxError(RijwalError):
    """Syntax error in Rijwal_Lang code"""
    def __init__(self, message, line_num=None, line_content=None):
        self.line_num = line_num
        self.line_content = line_content
        msg = message
        if line_num:
            msg += f" (line {line_num})"
        if line_content:
            msg += f"\n    {line_content}"
        super().__init__(msg)

class RijwalRuntimeError(RijwalError):
    """Runtime error during execution"""
    pass

class RijwalTypeError(RijwalError):
    """Type error in operations"""
    pass

class BreakException(Exception):
    """For break statement"""
    pass

class ContinueException(Exception):
    """For continue statement"""
    pass

# ============================================================================
# FILE I/O FUNCTIONS (7 functions)
# ============================================================================

def builtin_read_file(filepath):
    """Read entire file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise RijwalRuntimeError(f"File not found: {filepath}")
    except Exception as e:
        raise RijwalRuntimeError(f"Error reading file: {str(e)}")

def builtin_write_file(filepath, content):
    """Write content to file (overwrites)"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(content))
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error writing file: {str(e)}")

def builtin_append_file(filepath, content):
    """Append content to file"""
    try:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(str(content))
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error appending to file: {str(e)}")

def builtin_delete_file(filepath):
    """Delete a file"""
    try:
        os.remove(filepath)
        return True
    except FileNotFoundError:
        raise RijwalRuntimeError(f"File not found: {filepath}")
    except Exception as e:
        raise RijwalRuntimeError(f"Error deleting file: {str(e)}")

def builtin_file_exists(filepath):
    """Check if file exists"""
    return os.path.isfile(filepath)

def builtin_list_files(directory="."):
    """List all files in directory"""
    try:
        return os.listdir(directory)
    except Exception as e:
        raise RijwalRuntimeError(f"Error listing files: {str(e)}")

def builtin_file_size(filepath):
    """Get file size in bytes"""
    try:
        return os.path.getsize(filepath)
    except Exception as e:
        raise RijwalRuntimeError(f"Error getting file size: {str(e)}")

# ============================================================================
# SYSTEM COMMAND FUNCTIONS (5 functions)
# ============================================================================

def builtin_system(command):
    """Execute system command and return output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout
    except subprocess.TimeoutExpired:
        raise RijwalRuntimeError("Command timeout exceeded")
    except Exception as e:
        raise RijwalRuntimeError(f"Error executing command: {str(e)}")

def builtin_execute(command):
    """Execute command and return exit code"""
    try:
        result = subprocess.run(command, shell=True, timeout=30)
        return result.returncode
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_shell(script):
    """Execute shell script"""
    try:
        result = subprocess.run(script, shell=True, capture_output=True, text=True, timeout=30)
        return {"output": result.stdout, "error": result.stderr, "code": result.returncode}
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_open_app(app_path):
    """Open application"""
    try:
        subprocess.Popen(app_path)
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error opening app: {str(e)}")

def builtin_get_env(var_name):
    """Get environment variable"""
    return os.getenv(var_name, "")

# ============================================================================
# ADVANCED PYTHON FUNCTIONS (5 functions)
# ============================================================================

def builtin_py_eval(code):
    """Evaluate Python expression"""
    try:
        result = eval(code, {"__builtins__": {}})
        return result
    except Exception as e:
        raise RijwalRuntimeError(f"Python eval error: {str(e)}")

def builtin_py_exec(code):
    """Execute Python code"""
    try:
        exec(code)
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Python exec error: {str(e)}")

def builtin_import_module(module_name):
    """Import Python module"""
    try:
        module = __import__(module_name)
        return module
    except ImportError:
        raise RijwalRuntimeError(f"Module not found: {module_name}")

def builtin_py_version():
    """Get Python version"""
    return sys.version

def builtin_py_call(module_name, function_name, *args):
    """Call Python function from module"""
    try:
        module = __import__(module_name)
        func = getattr(module, function_name)
        return func(*args)
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

# ============================================================================
# GRAPHICS/UI FUNCTIONS (10 functions)
# ============================================================================

def builtin_open_window(width=400, height=300, title="Rijwal Window"):
    """Open graphics window"""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.title(title)
        root.geometry(f"{width}x{height}")
        return root
    except ImportError:
        raise RijwalRuntimeError("tkinter not available")
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_draw_line(canvas, x1, y1, x2, y2, color="black"):
    """Draw line on canvas"""
    try:
        canvas.create_line(x1, y1, x2, y2, fill=color)
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error drawing: {str(e)}")

def builtin_draw_rect(canvas, x, y, width, height, color="black", fill=None):
    """Draw rectangle"""
    try:
        canvas.create_rectangle(x, y, x+width, y+height, outline=color, fill=fill)
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error drawing: {str(e)}")

def builtin_draw_circle(canvas, x, y, radius, color="black", fill=None):
    """Draw circle"""
    try:
        canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline=color, fill=fill)
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error drawing: {str(e)}")

def builtin_draw_text(canvas, x, y, text, color="black", size=12):
    """Draw text on canvas"""
    try:
        canvas.create_text(x, y, text=str(text), fill=color, font=("Arial", size))
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error drawing: {str(e)}")

def builtin_show_image(window, filepath, x=0, y=0):
    """Show image on window"""
    try:
        from PIL import Image, ImageTk
        img = Image.open(filepath)
        photo = ImageTk.PhotoImage(img)
        label = window.Label(window, image=photo)
        label.image = photo
        label.place(x=x, y=y)
        return True
    except ImportError:
        raise RijwalRuntimeError("PIL not available")
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_create_button(window, x, y, text, callback=None):
    """Create button"""
    try:
        import tkinter as tk
        button = tk.Button(window, text=text, command=callback)
        button.place(x=x, y=y)
        return button
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_create_input(window, x, y, width=20):
    """Create text input field"""
    try:
        import tkinter as tk
        entry = tk.Entry(window, width=width)
        entry.place(x=x, y=y)
        return entry
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_get_input_value(input_widget):
    """Get value from input widget"""
    try:
        return input_widget.get()
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_update_window(window):
    """Update window display"""
    try:
        window.update()
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

# ============================================================================
# DATABASE FUNCTIONS (8 functions)
# ============================================================================

def builtin_db_create(db_path, table_name, columns):
    """Create database and table"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        col_str = ", ".join([f"{col} TEXT" for col in columns])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({col_str})")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Database error: {str(e)}")

def builtin_db_insert(db_path, table_name, values):
    """Insert record into database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        placeholders = ",".join(["?" for _ in values])
        cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Database error: {str(e)}")

def builtin_db_query(db_path, table_name, where=None):
    """Query database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name}"
        if where:
            query += f" WHERE {where}"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        raise RijwalRuntimeError(f"Database error: {str(e)}")

def builtin_db_update(db_path, table_name, set_clause, where):
    """Update database record"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {where}")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Database error: {str(e)}")

def builtin_db_delete(db_path, table_name, where):
    """Delete from database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE {where}")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Database error: {str(e)}")

def builtin_db_count(db_path, table_name):
    """Count records in table"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        raise RijwalRuntimeError(f"Database error: {str(e)}")

def builtin_db_drop(db_path, table_name):
    """Drop table from database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Database error: {str(e)}")

# ============================================================================
# NETWORK FUNCTIONS (8 functions)
# ============================================================================

def builtin_http_get(url):
    """GET request"""
    try:
        request = Request(url, headers={'User-Agent': 'Rijwal_Lang/0.15'})
        with urlopen(request, timeout=10) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        raise RijwalRuntimeError(f"Network error: {str(e)}")
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_http_post(url, data):
    """POST request"""
    try:
        post_data = json.dumps(data).encode('utf-8')
        request = Request(url, data=post_data, headers={'User-Agent': 'Rijwal_Lang/0.15'})
        with urlopen(request, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_fetch_json(url):
    """Fetch and parse JSON"""
    try:
        response = builtin_http_get(url)
        return json.loads(response)
    except json.JSONDecodeError:
        raise RijwalRuntimeError("Invalid JSON response")
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_download_file(url, filepath):
    """Download file"""
    try:
        with urlopen(url, timeout=30) as response:
            with open(filepath, 'wb') as out:
                out.write(response.read())
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error downloading: {str(e)}")

def builtin_open_url(url):
    """Open URL in default browser"""
    try:
        import webbrowser
        webbrowser.open(url)
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_get_url_status(url):
    """Get HTTP status code"""
    try:
        request = Request(url, headers={'User-Agent': 'Rijwal_Lang/0.15'})
        with urlopen(request, timeout=10) as response:
            return response.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_json_parse(json_string):
    """Parse JSON string"""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise RijwalRuntimeError(f"JSON parse error: {str(e)}")

def builtin_json_stringify(obj):
    """Convert object to JSON string"""
    try:
        return json.dumps(obj, indent=2)
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

# ============================================================================
# EXTRA FEATURES (20+ functions)
# ============================================================================

# Threading
def builtin_thread_create(func, *args):
    """Create and start thread"""
    try:
        thread = threading.Thread(target=func, args=args)
        thread.start()
        return thread
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_thread_join(thread):
    """Wait for thread to finish"""
    try:
        thread.join()
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_thread_sleep(seconds):
    """Sleep for seconds"""
    time.sleep(seconds)
    return True

# Encryption
def builtin_hash_md5(text):
    """MD5 hash"""
    return hashlib.md5(str(text).encode()).hexdigest()

def builtin_hash_sha256(text):
    """SHA256 hash"""
    return hashlib.sha256(str(text).encode()).hexdigest()

def builtin_encode_base64(text):
    """Base64 encode"""
    return base64.b64encode(str(text).encode()).decode()

def builtin_decode_base64(text):
    """Base64 decode"""
    try:
        return base64.b64decode(text).decode()
    except Exception as e:
        raise RijwalRuntimeError(f"Decode error: {str(e)}")

# Compression
def builtin_compress(text):
    """Compress text"""
    return zlib.compress(str(text).encode())

def builtin_decompress(data):
    """Decompress data"""
    try:
        return zlib.decompress(data).decode()
    except Exception as e:
        raise RijwalRuntimeError(f"Decompress error: {str(e)}")

# Time/Date
def builtin_current_time():
    """Get current timestamp"""
    return time.time()

def builtin_current_datetime():
    """Get current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def builtin_timestamp_to_date(timestamp):
    """Convert timestamp to date"""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

# Directory Operations
def builtin_create_dir(path):
    """Create directory"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_dir_exists(path):
    """Check if directory exists"""
    return os.path.isdir(path)

def builtin_delete_dir(path):
    """Delete directory"""
    try:
        os.rmdir(path)
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_current_dir():
    """Get current directory"""
    return os.getcwd()

def builtin_change_dir(path):
    """Change directory"""
    try:
        os.chdir(path)
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

# Performance
def builtin_time_function(func, *args):
    """Measure function execution time"""
    try:
        start = time.time()
        result = func(*args)
        elapsed = time.time() - start
        return {"result": result, "time": elapsed}
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

# ============================================================================
# ORIGINAL v0.14 FUNCTIONS (continued)
# ============================================================================

def builtin_print(*args):
    """Print output"""
    print(" ".join(str(arg) for arg in args))
    return None

def builtin_input(prompt=""):
    """Get user input"""
    return input(str(prompt))

def builtin_len(obj):
    """Get length"""
    return len(obj)

def builtin_str(obj):
    """Convert to string"""
    return str(obj)

def builtin_int(obj):
    """Convert to int"""
    try:
        return int(obj)
    except:
        raise RijwalTypeError(f"Cannot convert {obj} to int")

def builtin_float(obj):
    """Convert to float"""
    try:
        return float(obj)
    except:
        raise RijwalTypeError(f"Cannot convert {obj} to float")

def builtin_bool(obj):
    """Convert to bool"""
    return bool(obj)

def builtin_list(obj):
    """Convert to list"""
    return list(obj)

def builtin_dict_create(*pairs):
    """Create dictionary"""
    result = {}
    for i in range(0, len(pairs), 2):
        if i+1 < len(pairs):
            result[pairs[i]] = pairs[i+1]
    return result

def builtin_type(obj):
    """Get type"""
    t = type(obj).__name__
    return t

def builtin_is_int(obj):
    """Check if integer"""
    return isinstance(obj, int) and not isinstance(obj, bool)

def builtin_abs(num):
    """Absolute value"""
    return abs(num)

def builtin_round(num, digits=0):
    """Round number"""
    return round(num, digits)

def builtin_floor(num):
    """Floor function"""
    return math.floor(num)

def builtin_ceil(num):
    """Ceiling function"""
    return math.ceil(num)

def builtin_sqrt(num):
    """Square root"""
    return math.sqrt(num)

def builtin_pow(base, exp):
    """Power function"""
    return pow(base, exp)

def builtin_sin(angle):
    """Sine function"""
    return math.sin(angle)

def builtin_cos(angle):
    """Cosine function"""
    return math.cos(angle)

def builtin_tan(angle):
    """Tangent function"""
    return math.tan(angle)

def builtin_sum(*args):
    """Sum values"""
    return sum(args)

def builtin_avg(*args):
    """Average values"""
    if not args:
        return 0
    return sum(args) / len(args)

def builtin_max(*args):
    """Maximum value"""
    return max(args)

def builtin_min(*args):
    """Minimum value"""
    return min(args)

def builtin_random():
    """Random 0-1"""
    return random.random()

def builtin_randint(a, b):
    """Random integer"""
    return random.randint(a, b)

def builtin_upper(s):
    """Uppercase"""
    return str(s).upper()

def builtin_lower(s):
    """Lowercase"""
    return str(s).lower()

def builtin_split(s, sep=" "):
    """Split string"""
    return str(s).split(sep)

def builtin_join(sep, items):
    """Join list"""
    return sep.join(str(item) for item in items)

def builtin_reverse(obj):
    """Reverse"""
    return list(reversed(obj))

def builtin_capitalize(s):
    """Capitalize"""
    return str(s).capitalize()

def builtin_strip(s):
    """Strip whitespace"""
    return str(s).strip()

def builtin_replace(s, old, new):
    """Replace substring"""
    return str(s).replace(old, new)

def builtin_find(s, substr):
    """Find substring"""
    return str(s).find(substr)

def builtin_sort(lst):
    """Sort list"""
    return sorted(lst)

def builtin_sort_desc(lst):
    """Sort descending"""
    return sorted(lst, reverse=True)

def builtin_append(lst, item):
    """Append to list"""
    lst.append(item)
    return lst

def builtin_pop(lst):
    """Pop from list"""
    if lst:
        lst.pop()
    return lst

def builtin_index(lst, item):
    """Find index"""
    try:
        return lst.index(item)
    except ValueError:
        return -1

def builtin_count(lst, item):
    """Count in list"""
    return lst.count(item)

def builtin_first(lst):
    """Get first item"""
    return lst[0] if lst else None

def builtin_last(lst):
    """Get last item"""
    return lst[-1] if lst else None

def builtin_unique(lst):
    """Remove duplicates"""
    return list(dict.fromkeys(lst))

def builtin_flatten(lst):
    """Flatten nested list"""
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(builtin_flatten(item))
        else:
            result.append(item)
    return result

def builtin_zip(*lists):
    """Zip lists"""
    return list(zip(*lists))

def builtin_range(start, end=None):
    """Create range"""
    if end is None:
        return list(range(start))
    return list(range(start, end))

def builtin_enumerate(lst):
    """Enumerate list"""
    return list(enumerate(lst))

def builtin_any(*args):
    """Any true"""
    return any(args)

def builtin_all(*args):
    """All true"""
    return all(args)

def builtin_slice(lst, start, end=None):
    """Slice list"""
    if end is None:
        return lst[start:]
    return lst[start:end]

def builtin_pi():
    """Pi constant"""
    return math.pi

def builtin_len_list(lst):
    """List length"""
    return len(lst)

# ============================================================================
# BUILTIN FUNCTIONS REGISTRY
# ============================================================================

BUILTIN_FUNCS = {
    # File I/O
    "read_file": builtin_read_file,
    "write_file": builtin_write_file,
    "append_file": builtin_append_file,
    "delete_file": builtin_delete_file,
    "file_exists": builtin_file_exists,
    "list_files": builtin_list_files,
    "file_size": builtin_file_size,
    
    # System Commands
    "system": builtin_system,
    "execute": builtin_execute,
    "shell": builtin_shell,
    "open_app": builtin_open_app,
    "get_env": builtin_get_env,
    
    # Advanced Python
    "py_eval": builtin_py_eval,
    "py_exec": builtin_py_exec,
    "import_module": builtin_import_module,
    "py_version": builtin_py_version,
    "py_call": builtin_py_call,
    
    # Graphics/UI
    "open_window": builtin_open_window,
    "draw_line": builtin_draw_line,
    "draw_rect": builtin_draw_rect,
    "draw_circle": builtin_draw_circle,
    "draw_text": builtin_draw_text,
    "show_image": builtin_show_image,
    "create_button": builtin_create_button,
    "create_input": builtin_create_input,
    "get_input_value": builtin_get_input_value,
    "update_window": builtin_update_window,
    
    # Database
    "db_create": builtin_db_create,
    "db_insert": builtin_db_insert,
    "db_query": builtin_db_query,
    "db_update": builtin_db_update,
    "db_delete": builtin_db_delete,
    "db_count": builtin_db_count,
    "db_drop": builtin_db_drop,
    
    # Network
    "http_get": builtin_http_get,
    "http_post": builtin_http_post,
    "fetch_json": builtin_fetch_json,
    "download_file": builtin_download_file,
    "open_url": builtin_open_url,
    "get_url_status": builtin_get_url_status,
    "json_parse": builtin_json_parse,
    "json_stringify": builtin_json_stringify,
    
    # Threading
    "thread_create": builtin_thread_create,
    "thread_join": builtin_thread_join,
    "thread_sleep": builtin_thread_sleep,
    
    # Encryption
    "hash_md5": builtin_hash_md5,
    "hash_sha256": builtin_hash_sha256,
    "encode_base64": builtin_encode_base64,
    "decode_base64": builtin_decode_base64,
    
    # Compression
    "compress": builtin_compress,
    "decompress": builtin_decompress,
    
    # Time/Date
    "current_time": builtin_current_time,
    "current_datetime": builtin_current_datetime,
    "timestamp_to_date": builtin_timestamp_to_date,
    
    # Directory
    "create_dir": builtin_create_dir,
    "dir_exists": builtin_dir_exists,
    "delete_dir": builtin_delete_dir,
    "current_dir": builtin_current_dir,
    "change_dir": builtin_change_dir,
    
    # Performance
    "time_function": builtin_time_function,
    
    # Original v0.14
    "print": builtin_print,
    "input": builtin_input,
    "len": builtin_len,
    "str": builtin_str,
    "int": builtin_int,
    "float": builtin_float,
    "bool": builtin_bool,
    "list": builtin_list,
    "dict": builtin_dict_create,
    "type": builtin_type,
    "is_int": builtin_is_int,
    "abs": builtin_abs,
    "round": builtin_round,
    "floor": builtin_floor,
    "ceil": builtin_ceil,
    "sqrt": builtin_sqrt,
    "pow": builtin_pow,
    "sin": builtin_sin,
    "cos": builtin_cos,
    "tan": builtin_tan,
    "sum": builtin_sum,
    "avg": builtin_avg,
    "max": builtin_max,
    "min": builtin_min,
    "random": builtin_random,
    "randint": builtin_randint,
    "upper": builtin_upper,
    "lower": builtin_lower,
    "split": builtin_split,
    "join": builtin_join,
    "reverse": builtin_reverse,
    "capitalize": builtin_capitalize,
    "strip": builtin_strip,
    "replace": builtin_replace,
    "find": builtin_find,
    "sort": builtin_sort,
    "sort_desc": builtin_sort_desc,
    "append": builtin_append,
    "pop": builtin_pop,
    "index": builtin_index,
    "count": builtin_count,
    "first": builtin_first,
    "last": builtin_last,
    "unique": builtin_unique,
    "flatten": builtin_flatten,
    "zip": builtin_zip,
    "range": builtin_range,
    "enumerate": builtin_enumerate,
    "any": builtin_any,
    "all": builtin_all,
    "slice": builtin_slice,
    "pi": builtin_pi,
    "len_list": builtin_len_list,
}

# ============================================================================
# PARSER & INTERPRETER
# ============================================================================

class RijwalInterpreter:
    def __init__(self):
        self.variables = {}
        self.timers = {}
        self.imports = {}
        
    def execute(self, code):
        """Main execution entry point"""
        lines = code.strip().split('\n')
        self.execute_lines(lines)
        
    def execute_lines(self, lines, start_indent=0, context=None):
        """Execute list of lines"""
        if context is None:
            context = self.variables
            
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if not stripped or stripped.startswith('#'):
                i += 1
                continue
            
            indent = len(line) - len(line.lstrip())
            
            if indent < start_indent:
                return i
            
            if indent > start_indent:
                i += 1
                continue
            
            # Parse and execute statement
            try:
                self.execute_statement(stripped, lines, i, context)
            except BreakException:
                return i
            except ContinueException:
                i += 1
                continue
            except Exception as e:
                raise RijwalRuntimeError(f"{str(e)} at line {i+1}: {stripped}")
            
            i += 1
            
        return len(lines)
    
    def execute_statement(self, statement, lines, line_idx, context):
        """Execute a single statement"""
        
        # For loop
        if statement.startswith("For ") and " In " in statement:
            self.handle_for_loop(statement, lines, line_idx, context)
            return
        
        # While loop
        if statement.startswith("While "):
            self.handle_while_loop(statement, lines, line_idx, context)
            return
        
        # If statement
        if statement.startswith("If "):
            self.handle_if_statement(statement, lines, line_idx, context)
            return
        
        # Break
        if statement == "Break":
            raise BreakException()
        
        # Continue
        if statement == "Continue":
            raise ContinueException()
        
        # Let (assignment)
        if statement.startswith("Let "):
            self.handle_assignment(statement, context)
            return
        
        # Input
        if statement.startswith("Input "):
            self.handle_input(statement, context)
            return
        
        # Import
        if statement.startswith("Import "):
            self.handle_import(statement, context)
            return
        
        # Timer
        if statement.startswith("Every "):
            self.handle_timer(statement, context)
            return
        
        # Expression/function call
        self.evaluate(statement, context)
    
    def handle_for_loop(self, statement, lines, line_idx, context):
        """Handle for loop"""
        match = re.match(r"For\s+(\w+)\s+In\s+(.+):", statement)
        if not match:
            raise RijwalSyntaxError(f"Invalid for loop: {statement}")
        
        var_name = match.group(1)
        expr = match.group(2).strip()
        
        iterable = self.evaluate(expr, context)
        
        indent = len(lines[line_idx]) - len(lines[line_idx].lstrip())
        body_lines = []
        i = line_idx + 1
        
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            line_indent = len(line) - len(line.lstrip())
            if line_indent <= indent:
                break
            body_lines.append(line)
            i += 1
        
        for item in iterable:
            context[var_name] = item
            try:
                self.execute_lines(body_lines, indent + 4, context)
            except BreakException:
                break
            except ContinueException:
                continue
    
    def handle_while_loop(self, statement, lines, line_idx, context):
        """Handle while loop"""
        condition = statement[6:].strip()
        if condition.endswith(":"):
            condition = condition[:-1]
        
        indent = len(lines[line_idx]) - len(lines[line_idx].lstrip())
        body_lines = []
        i = line_idx + 1
        
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            line_indent = len(line) - len(line.lstrip())
            if line_indent <= indent:
                break
            body_lines.append(line)
            i += 1
        
        while self.check_condition(condition, context):
            try:
                self.execute_lines(body_lines, indent + 4, context)
            except BreakException:
                break
            except ContinueException:
                continue
    
    def handle_if_statement(self, statement, lines, line_idx, context):
        """Handle if/else statement"""
        condition = statement[3:].rstrip(":")
        
        indent = len(lines[line_idx]) - len(lines[line_idx].lstrip())
        if_body = []
        else_body = []
        i = line_idx + 1
        in_else = False
        
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            
            line_indent = len(line) - len(line.lstrip())
            if line_indent <= indent:
                break
            
            if line.strip().startswith("Else:"):
                in_else = True
                i += 1
                continue
            
            if in_else:
                else_body.append(line)
            else:
                if_body.append(line)
            i += 1
        
        if self.check_condition(condition, context):
            self.execute_lines(if_body, indent + 4, context)
        elif else_body:
            self.execute_lines(else_body, indent + 4, context)
    
    def check_condition(self, condition, context):
        """Check if condition is true"""
        merged = {**context, **BUILTIN_FUNCS}
        try:
            result = eval(condition, {"__builtins__": {}}, merged)
            return bool(result)
        except:
            return False
    
    def handle_assignment(self, statement, context):
        """Handle Let assignment"""
        parts = statement[4:].split(" = ", 1)
        if len(parts) != 2:
            raise RijwalSyntaxError(f"Invalid assignment: {statement}")
        
        var_name = parts[0].strip()
        expr = parts[1].strip()
        
        value = self.evaluate(expr, context)
        context[var_name] = value
    
    def handle_input(self, statement, context):
        """Handle Input"""
        var_name = statement[6:].strip()
        value = input()
        context[var_name] = value
    
    def handle_import(self, statement, context):
        """Handle imports"""
        module_name = statement[7:].strip()
        try:
            module = __import__(module_name)
            context[module_name] = module
        except ImportError:
            raise RijwalRuntimeError(f"Cannot import {module_name}")
    
    def handle_timer(self, statement, context):
        """Handle timer"""
        match = re.match(r"Every\s+(\d+)\s+seconds:\s+(.+)", statement)
        if match:
            interval = int(match.group(1))
            action = match.group(2)
            
            def timer_func():
                while True:
                    time.sleep(interval)
                    self.evaluate(action, context)
            
            thread = threading.Thread(target=timer_func, daemon=True)
            thread.start()
    
    def evaluate(self, expr, context):
        """Evaluate expression"""
        merged = {**context, **BUILTIN_FUNCS}
        
        try:
            result = eval(expr, {"__builtins__": {}}, merged)
            return result
        except Exception as e:
            raise RijwalRuntimeError(f"Evaluation error: {str(e)}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print(f"Rijwal_Lang v{VERSION} - ULTIMATE EDITION")
        print("Usage: python rijwal_lang_v0.15.py <script.Rijwal_lang>")
        sys.exit(1)
    
    script_file = sys.argv[1]
    
    if not os.path.exists(script_file):
        print(f"Error: File not found: {script_file}")
        sys.exit(1)
    
    with open(script_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    interpreter = RijwalInterpreter()
    
    try:
        interpreter.execute(code)
    except RijwalError as e:
        print(f"Rijwal Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

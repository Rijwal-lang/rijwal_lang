#!/usr/bin/env python3
"""
Rijwal_Lang v0.16 - INFINITE SUPERPOWER EDITION
THE ULTIMATE POLYGLOT PROGRAMMING LANGUAGE
Python + JavaScript + Go + Rust + Multiple Language Source Code Integration
Multi-Superpower Universe Merged into ONE!

Author: Rijwal
Version: 0.16
License: MIT
Tagline: "Cross All Limits. Multiply All Powers."
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

VERSION = "0.16"

# ============================================================================
# PYTHON EMBEDDING MODULE
# ============================================================================

class PythonBlockExecutor:
    """Full Python source code execution engine"""
    
    @staticmethod
    def execute_python_block(code, context):
        """Execute pure Python code block"""
        try:
            # Create execution environment with context
            exec_globals = {"__builtins__": __import__('builtins')}
            exec_globals.update(context)
            
            exec(code, exec_globals)
            
            # Return updated context
            return exec_globals
        except Exception as e:
            raise RijwalRuntimeError(f"Python block error: {str(e)}")
    
    @staticmethod
    def evaluate_python_expr(expr, context):
        """Evaluate Python expression"""
        try:
            eval_globals = {"__builtins__": __import__('builtins')}
            eval_globals.update(context)
            return eval(expr, eval_globals)
        except Exception as e:
            raise RijwalRuntimeError(f"Python eval error: {str(e)}")


# ============================================================================
# JAVASCRIPT EXECUTION MODULE
# ============================================================================

class JavaScriptExecutor:
    """JavaScript code execution via Node.js"""
    
    @staticmethod
    def execute_js_block(code, context):
        """Execute JavaScript code block"""
        try:
            # Convert context to JS format
            context_json = json.dumps(context, default=str)
            
            # Create JS wrapper
            js_code = f"""
const __context = {context_json};
{code}
console.log(JSON.stringify(__context));
"""
            
            # Write to temp file
            with open("_rijwal_temp.js", "w") as f:
                f.write(js_code)
            
            # Execute with Node.js
            result = subprocess.run(
                ["node", "_rijwal_temp.js"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            os.remove("_rijwal_temp.js")
            
            if result.returncode != 0:
                raise RijwalRuntimeError(f"JS error: {result.stderr}")
            
            # Parse output
            try:
                return json.loads(result.stdout)
            except:
                return result.stdout
                
        except FileNotFoundError:
            raise RijwalRuntimeError("Node.js not found. Install Node.js to use JS blocks.")
        except Exception as e:
            raise RijwalRuntimeError(f"JS execution error: {str(e)}")


# ============================================================================
# GO EXECUTION MODULE
# ============================================================================

class GoExecutor:
    """Go code execution"""
    
    @staticmethod
    def execute_go_block(code, context):
        """Execute Go code"""
        try:
            # Create Go program wrapper
            go_code = f"""
package main

import (
    "fmt"
    "encoding/json"
)

func main() {{
    context := map[string]interface{{}}{{}}
    // User code here
    {code}
    
    jsonData, _ := json.Marshal(context)
    fmt.Println(string(jsonData))
}}
"""
            
            with open("_rijwal_temp.go", "w") as f:
                f.write(go_code)
            
            # Compile and run
            result = subprocess.run(
                ["go", "run", "_rijwal_temp.go"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            os.remove("_rijwal_temp.go")
            
            if result.returncode != 0:
                raise RijwalRuntimeError(f"Go error: {result.stderr}")
            
            try:
                return json.loads(result.stdout)
            except:
                return result.stdout
                
        except FileNotFoundError:
            raise RijwalRuntimeError("Go not found. Install Go to use GO blocks.")
        except Exception as e:
            raise RijwalRuntimeError(f"Go execution error: {str(e)}")


# ============================================================================
# RUST EXECUTION MODULE
# ============================================================================

class RustExecutor:
    """Rust code execution"""
    
    @staticmethod
    def execute_rust_block(code, context):
        """Execute Rust code"""
        try:
            # Create Rust program
            rust_code = f"""
fn main() {{
    // User code
    {code}
}}
"""
            
            with open("_rijwal_temp.rs", "w") as f:
                f.write(rust_code)
            
            # Compile and run
            compile = subprocess.run(
                ["rustc", "-o", "_rijwal_temp", "_rijwal_temp.rs"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if compile.returncode != 0:
                raise RijwalRuntimeError(f"Rust compile error: {compile.stderr}")
            
            result = subprocess.run(
                ["./_rijwal_temp"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            os.remove("_rijwal_temp.rs")
            if os.path.exists("_rijwal_temp"):
                os.remove("_rijwal_temp")
            
            if result.returncode != 0:
                raise RijwalRuntimeError(f"Rust error: {result.stderr}")
            
            return result.stdout
                
        except FileNotFoundError:
            raise RijwalRuntimeError("Rust not found. Install Rust to use RUST blocks.")
        except Exception as e:
            raise RijwalRuntimeError(f"Rust execution error: {str(e)}")


# ============================================================================
# C++ EXECUTION MODULE
# ============================================================================

class CppExecutor:
    """C++ code execution"""
    
    @staticmethod
    def execute_cpp_block(code, context):
        """Execute C++ code"""
        try:
            cpp_code = f"""
#include <iostream>
#include <string>
using namespace std;

int main() {{
    // User code
    {code}
    return 0;
}}
"""
            
            with open("_rijwal_temp.cpp", "w") as f:
                f.write(cpp_code)
            
            # Compile
            compile = subprocess.run(
                ["g++", "-o", "_rijwal_temp", "_rijwal_temp.cpp"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if compile.returncode != 0:
                raise RijwalRuntimeError(f"C++ compile error: {compile.stderr}")
            
            # Execute
            result = subprocess.run(
                ["./_rijwal_temp"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            os.remove("_rijwal_temp.cpp")
            if os.path.exists("_rijwal_temp"):
                os.remove("_rijwal_temp")
            
            return result.stdout
                
        except FileNotFoundError:
            raise RijwalRuntimeError("C++ compiler not found. Install G++ or MSVC.")
        except Exception as e:
            raise RijwalRuntimeError(f"C++ execution error: {str(e)}")


# ============================================================================
# BASH/SHELL EXECUTION MODULE
# ============================================================================

class BashExecutor:
    """Bash/Shell script execution"""
    
    @staticmethod
    def execute_bash_block(code, context):
        """Execute bash script"""
        try:
            result = subprocess.run(
                code,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout
        except Exception as e:
            raise RijwalRuntimeError(f"Bash error: {str(e)}")


# ============================================================================
# SQL EXECUTION MODULE
# ============================================================================

class SQLExecutor:
    """SQL query execution"""
    
    @staticmethod
    def execute_sql_block(code, context, db_path="rijwal_data.db"):
        """Execute SQL queries"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Execute SQL
            cursor.executescript(code)
            conn.commit()
            
            # Fetch results
            results = cursor.fetchall()
            conn.close()
            
            return results
        except Exception as e:
            raise RijwalRuntimeError(f"SQL error: {str(e)}")


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
# NEW v0.16 SPECIAL FUNCTIONS
# ============================================================================

def builtin_python_block(code, context):
    """Execute Python block directly"""
    return PythonBlockExecutor.execute_python_block(code, context)

def builtin_javascript_block(code, context):
    """Execute JavaScript block"""
    return JavaScriptExecutor.execute_js_block(code, context)

def builtin_go_block(code, context):
    """Execute Go block"""
    return GoExecutor.execute_go_block(code, context)

def builtin_rust_block(code, context):
    """Execute Rust block"""
    return RustExecutor.execute_rust_block(code, context)

def builtin_cpp_block(code, context):
    """Execute C++ block"""
    return CppExecutor.execute_cpp_block(code, context)

def builtin_bash_block(code, context):
    """Execute Bash block"""
    return BashExecutor.execute_bash_block(code, context)

def builtin_sql_block(code, context):
    """Execute SQL block"""
    return SQLExecutor.execute_sql_block(code, context)

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
        request = Request(url, headers={'User-Agent': 'Rijwal_Lang/0.16'})
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
        request = Request(url, data=post_data, headers={'User-Agent': 'Rijwal_Lang/0.16'})
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
        request = Request(url, headers={'User-Agent': 'Rijwal_Lang/0.16'})
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
# THREADING & PERFORMANCE (3 functions)
# ============================================================================

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

# ============================================================================
# SECURITY & ENCRYPTION (8 functions)
# ============================================================================

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

def builtin_compress(text):
    """Compress text"""
    return zlib.compress(str(text).encode())

def builtin_decompress(data):
    """Decompress data"""
    try:
        return zlib.decompress(data).decode()
    except Exception as e:
        raise RijwalRuntimeError(f"Decompress error: {str(e)}")

def builtin_current_time():
    """Get current timestamp"""
    return time.time()

def builtin_current_datetime():
    """Get current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ============================================================================
# DIRECTORY & FILE UTILITIES (5 functions)
# ============================================================================

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

# ============================================================================
# CORE v0.15+ FUNCTIONS (50+)
# ============================================================================

def builtin_print(*args):
    print(" ".join(str(arg) for arg in args))
    return None

def builtin_input(prompt=""):
    return input(str(prompt))

def builtin_len(obj):
    return len(obj)

def builtin_str(obj):
    return str(obj)

def builtin_int(obj):
    try:
        return int(obj)
    except:
        raise RijwalTypeError(f"Cannot convert {obj} to int")

def builtin_float(obj):
    try:
        return float(obj)
    except:
        raise RijwalTypeError(f"Cannot convert {obj} to float")

def builtin_bool(obj):
    return bool(obj)

def builtin_list(obj):
    return list(obj)

def builtin_dict_create(*pairs):
    result = {}
    for i in range(0, len(pairs), 2):
        if i+1 < len(pairs):
            result[pairs[i]] = pairs[i+1]
    return result

def builtin_type(obj):
    return type(obj).__name__

def builtin_is_int(obj):
    return isinstance(obj, int) and not isinstance(obj, bool)

def builtin_abs(num):
    return abs(num)

def builtin_round(num, digits=0):
    return round(num, digits)

def builtin_floor(num):
    return math.floor(num)

def builtin_ceil(num):
    return math.ceil(num)

def builtin_sqrt(num):
    return math.sqrt(num)

def builtin_pow(base, exp):
    return pow(base, exp)

def builtin_sin(angle):
    return math.sin(angle)

def builtin_cos(angle):
    return math.cos(angle)

def builtin_tan(angle):
    return math.tan(angle)

def builtin_sum(*args):
    return sum(args)

def builtin_avg(*args):
    if not args:
        return 0
    return sum(args) / len(args)

def builtin_max(*args):
    return max(args)

def builtin_min(*args):
    return min(args)

def builtin_random():
    return random.random()

def builtin_randint(a, b):
    return random.randint(a, b)

def builtin_upper(s):
    return str(s).upper()

def builtin_lower(s):
    return str(s).lower()

def builtin_split(s, sep=" "):
    return str(s).split(sep)

def builtin_join(sep, items):
    return sep.join(str(item) for item in items)

def builtin_reverse(obj):
    return list(reversed(obj))

def builtin_capitalize(s):
    return str(s).capitalize()

def builtin_strip(s):
    return str(s).strip()

def builtin_replace(s, old, new):
    return str(s).replace(old, new)

def builtin_find(s, substr):
    return str(s).find(substr)

def builtin_sort(lst):
    return sorted(lst)

def builtin_sort_desc(lst):
    return sorted(lst, reverse=True)

def builtin_append(lst, item):
    lst.append(item)
    return lst

def builtin_pop(lst):
    if lst:
        lst.pop()
    return lst

def builtin_index(lst, item):
    try:
        return lst.index(item)
    except ValueError:
        return -1

def builtin_count(lst, item):
    return lst.count(item)

def builtin_first(lst):
    return lst[0] if lst else None

def builtin_last(lst):
    return lst[-1] if lst else None

def builtin_unique(lst):
    return list(dict.fromkeys(lst))

def builtin_flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(builtin_flatten(item))
        else:
            result.append(item)
    return result

def builtin_zip(*lists):
    return list(zip(*lists))

def builtin_range(start, end=None):
    if end is None:
        return list(range(start))
    return list(range(start, end))

def builtin_enumerate(lst):
    return list(enumerate(lst))

def builtin_any(*args):
    return any(args)

def builtin_all(*args):
    return all(args)

def builtin_slice(lst, start, end=None):
    if end is None:
        return lst[start:]
    return lst[start:end]

def builtin_pi():
    return math.pi

def builtin_len_list(lst):
    return len(lst)

# ============================================================================
# BUILTIN FUNCTIONS REGISTRY
# ============================================================================

BUILTIN_FUNCS = {
    # v0.16 NEW - MULTI-LANGUAGE BLOCKS
    "python_block": builtin_python_block,
    "javascript_block": builtin_javascript_block,
    "go_block": builtin_go_block,
    "rust_block": builtin_rust_block,
    "cpp_block": builtin_cpp_block,
    "bash_block": builtin_bash_block,
    "sql_block": builtin_sql_block,
    
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
    
    # Time
    "current_time": builtin_current_time,
    "current_datetime": builtin_current_datetime,
    
    # Directory
    "create_dir": builtin_create_dir,
    "dir_exists": builtin_dir_exists,
    "delete_dir": builtin_delete_dir,
    "current_dir": builtin_current_dir,
    "change_dir": builtin_change_dir,
    
    # Core v0.15+
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
# PARSER & INTERPRETER WITH MULTI-LANGUAGE SUPPORT
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
        
        # Python block
        if statement.startswith("PYTHON:"):
            self.handle_python_block(lines, line_idx, context)
            return
        
        # JavaScript block
        if statement.startswith("JAVASCRIPT:"):
            self.handle_javascript_block(lines, line_idx, context)
            return
        
        # Go block
        if statement.startswith("GO:"):
            self.handle_go_block(lines, line_idx, context)
            return
        
        # Rust block
        if statement.startswith("RUST:"):
            self.handle_rust_block(lines, line_idx, context)
            return
        
        # C++ block
        if statement.startswith("CPP:"):
            self.handle_cpp_block(lines, line_idx, context)
            return
        
        # Bash block
        if statement.startswith("BASH:"):
            self.handle_bash_block(lines, line_idx, context)
            return
        
        # SQL block
        if statement.startswith("SQL:"):
            self.handle_sql_block(lines, line_idx, context)
            return
        
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
    
    def handle_python_block(self, lines, line_idx, context):
        """Handle Python block"""
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
        
        python_code = '\n'.join(body_lines)
        PythonBlockExecutor.execute_python_block(python_code, context)
    
    def handle_javascript_block(self, lines, line_idx, context):
        """Handle JavaScript block"""
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
        
        js_code = '\n'.join(body_lines)
        JavaScriptExecutor.execute_js_block(js_code, context)
    
    def handle_go_block(self, lines, line_idx, context):
        """Handle Go block"""
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
        
        go_code = '\n'.join(body_lines)
        GoExecutor.execute_go_block(go_code, context)
    
    def handle_rust_block(self, lines, line_idx, context):
        """Handle Rust block"""
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
        
        rust_code = '\n'.join(body_lines)
        RustExecutor.execute_rust_block(rust_code, context)
    
    def handle_cpp_block(self, lines, line_idx, context):
        """Handle C++ block"""
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
        
        cpp_code = '\n'.join(body_lines)
        CppExecutor.execute_cpp_block(cpp_code, context)
    
    def handle_bash_block(self, lines, line_idx, context):
        """Handle Bash block"""
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
        
        bash_code = '\n'.join(body_lines)
        BashExecutor.execute_bash_block(bash_code, context)
    
    def handle_sql_block(self, lines, line_idx, context):
        """Handle SQL block"""
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
        
        sql_code = '\n'.join(body_lines)
        SQLExecutor.execute_sql_block(sql_code, context)
    
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
        print(f"╔═══════════════════════════════════════════════════════════╗")
        print(f"║    Rijwal_Lang v{VERSION} - INFINITE SUPERPOWER EDITION         ║")
        print(f"║         Python + JS + Go + Rust + C++ + SQL + More        ║")
        print(f"║              Cross All Limits. Multiply Powers             ║")
        print(f"╚═══════════════════════════════════════════════════════════╝")
        print(f"\nUsage: python rijwal_lang_v0.16.py <script.Rijwal_lang>")
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

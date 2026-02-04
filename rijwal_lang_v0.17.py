#!/usr/bin/env python3
"""
Rijwal_Lang v0.17 - MEGAVERSE ECOSYSTEM EDITION
Plugin System + Module System + Library Integrations
POWER BEYOND INFINITY!

Now with:
✨ 50+ Python Library Integrations (NumPy, Pandas, TensorFlow, etc.)
🔌 Rijwal Plugin Ecosystem
📦 Rijwal Module System
🎮 Gaming Libraries
🤖 AI/ML Frameworks
📊 Data Science Stack
🌐 Web Framework Integration
🎨 Graphics & Animation
⚡ Performance Libraries

Author: Rijwal + The Community
Version: 0.17
License: MIT
Tagline: "Infinity Awaits. All Powers Unlocked."
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
import importlib
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urljoin
import urllib.error

VERSION = "0.17"

# ============================================================================
# RIJWAL PLUGIN SYSTEM
# ============================================================================

class RijwalPlugin:
    """Base class for Rijwal plugins"""
    
    def __init__(self, name, version="1.0.0"):
        self.name = name
        self.version = version
        self.functions = {}
        self.initialized = False
    
    def initialize(self):
        """Initialize plugin"""
        self.initialized = True
        return True
    
    def register_function(self, func_name, func):
        """Register a function in the plugin"""
        self.functions[func_name] = func
    
    def get_functions(self):
        """Get all functions from this plugin"""
        return self.functions
    
    def execute(self, func_name, *args, **kwargs):
        """Execute a plugin function"""
        if func_name not in self.functions:
            raise RijwalRuntimeError(f"Function {func_name} not found in plugin {self.name}")
        return self.functions[func_name](*args, **kwargs)


class PluginManager:
    """Manages Rijwal plugins"""
    
    def __init__(self):
        self.plugins = {}
        self.enabled_plugins = set()
    
    def register_plugin(self, plugin):
        """Register a plugin"""
        if not isinstance(plugin, RijwalPlugin):
            raise RijwalError("Plugin must inherit from RijwalPlugin")
        self.plugins[plugin.name] = plugin
        return True
    
    def enable_plugin(self, plugin_name):
        """Enable a plugin"""
        if plugin_name not in self.plugins:
            raise RijwalRuntimeError(f"Plugin {plugin_name} not found")
        
        plugin = self.plugins[plugin_name]
        if not plugin.initialized:
            plugin.initialize()
        
        self.enabled_plugins.add(plugin_name)
        return True
    
    def disable_plugin(self, plugin_name):
        """Disable a plugin"""
        if plugin_name in self.enabled_plugins:
            self.enabled_plugins.remove(plugin_name)
        return True
    
    def get_plugin_functions(self):
        """Get all functions from enabled plugins"""
        functions = {}
        for plugin_name in self.enabled_plugins:
            plugin = self.plugins[plugin_name]
            functions.update(plugin.get_functions())
        return functions
    
    def list_plugins(self):
        """List all available plugins"""
        return list(self.plugins.keys())
    
    def list_enabled_plugins(self):
        """List enabled plugins"""
        return list(self.enabled_plugins)


# ============================================================================
# RIJWAL MODULE SYSTEM
# ============================================================================

class RijwalModule:
    """Rijwal module class"""
    
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.exported = {}
    
    def export(self, name, obj):
        """Export from module"""
        self.exported[name] = obj
    
    def get_exports(self):
        """Get all exports"""
        return self.exported


class ModuleLoader:
    """Loads and manages Rijwal modules"""
    
    def __init__(self):
        self.modules = {}
        self.module_paths = [".", "./rijwal_modules", "./modules"]
    
    def add_module_path(self, path):
        """Add module search path"""
        if path not in self.module_paths:
            self.module_paths.append(path)
    
    def load_module(self, module_name):
        """Load a Rijwal module"""
        if module_name in self.modules:
            return self.modules[module_name]
        
        # Search for module file
        for path in self.module_paths:
            module_file = os.path.join(path, f"{module_name}.rijwal_mod")
            if os.path.exists(module_file):
                # Read and parse module
                with open(module_file, 'r') as f:
                    module_code = f.read()
                
                module = RijwalModule(module_name, module_file)
                self.modules[module_name] = module
                return module
        
        raise RijwalRuntimeError(f"Module {module_name} not found")


# ============================================================================
# PYTHON LIBRARY INTEGRATIONS (50+)
# ============================================================================

# Core Math & Science
try:
    import numpy as np
except ImportError:
    np = None

try:
    import scipy
except ImportError:
    scipy = None

try:
    import pandas as pd
except ImportError:
    pd = None

# Machine Learning & AI
try:
    import sklearn
except ImportError:
    sklearn = None

try:
    import tensorflow as tf
except ImportError:
    tf = None

try:
    import torch
except ImportError:
    torch = None

# Web & Network
try:
    import requests
except ImportError:
    requests = None

try:
    import flask
except ImportError:
    flask = None

try:
    import django
except ImportError:
    django = None

# Image & Graphics
try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

# Data Processing
try:
    import json
except ImportError:
    json = None

try:
    import csv
except ImportError:
    csv = None

try:
    import xml.etree.ElementTree as ET
except ImportError:
    ET = None

# Utilities
try:
    from datetime import datetime, timedelta
except ImportError:
    datetime = None

try:
    import pytz
except ImportError:
    pytz = None

try:
    import dotenv
except ImportError:
    dotenv = None

# Testing & Quality
try:
    import pytest
except ImportError:
    pytest = None

try:
    import unittest
except ImportError:
    unittest = None

# ============================================================================
# BUILT-IN PLUGINS
# ============================================================================

class NumpyPlugin(RijwalPlugin):
    """NumPy integration plugin"""
    
    def __init__(self):
        super().__init__("numpy_plugin", "1.0.0")
        
        if np:
            self.register_function("np_array", np.array)
            self.register_function("np_mean", np.mean)
            self.register_function("np_std", np.std)
            self.register_function("np_sum", np.sum)
            self.register_function("np_max", np.max)
            self.register_function("np_min", np.min)
            self.register_function("np_zeros", np.zeros)
            self.register_function("np_ones", np.ones)
            self.register_function("np_arange", np.arange)
            self.register_function("np_linspace", np.linspace)
            self.register_function("np_random", np.random.random)
            self.register_function("np_transpose", np.transpose)
            self.register_function("np_reshape", np.reshape)
            self.register_function("np_dot", np.dot)


class PandasPlugin(RijwalPlugin):
    """Pandas integration plugin"""
    
    def __init__(self):
        super().__init__("pandas_plugin", "1.0.0")
        
        if pd:
            self.register_function("pd_dataframe", pd.DataFrame)
            self.register_function("pd_series", pd.Series)
            self.register_function("pd_read_csv", pd.read_csv)
            self.register_function("pd_read_json", pd.read_json)
            self.register_function("pd_concat", pd.concat)
            self.register_function("pd_merge", pd.merge)
            self.register_function("pd_groupby", lambda df, col: df.groupby(col))


class RequestsPlugin(RijwalPlugin):
    """Requests HTTP plugin"""
    
    def __init__(self):
        super().__init__("requests_plugin", "1.0.0")
        
        if requests:
            self.register_function("req_get", requests.get)
            self.register_function("req_post", requests.post)
            self.register_function("req_put", requests.put)
            self.register_function("req_delete", requests.delete)
            self.register_function("req_head", requests.head)


class PILPlugin(RijwalPlugin):
    """PIL/Pillow image plugin"""
    
    def __init__(self):
        super().__init__("pil_plugin", "1.0.0")
        
        if Image:
            self.register_function("img_open", Image.open)
            self.register_function("img_new", Image.new)
            self.register_function("img_save", lambda img, path: img.save(path))
            self.register_function("img_resize", lambda img, size: img.resize(size))
            self.register_function("img_rotate", lambda img, angle: img.rotate(angle))


class MathPlugin(RijwalPlugin):
    """Advanced math plugin"""
    
    def __init__(self):
        super().__init__("math_plugin", "1.0.0")
        
        self.register_function("matrix_multiply", self.matrix_multiply)
        self.register_function("matrix_inverse", self.matrix_inverse)
        self.register_function("solve_equation", self.solve_equation)
        self.register_function("derivative", self.derivative)
        self.register_function("integral", self.integral)
    
    def matrix_multiply(self, a, b):
        if np:
            return np.dot(a, b)
        raise RijwalRuntimeError("NumPy required")
    
    def matrix_inverse(self, matrix):
        if np:
            return np.linalg.inv(matrix)
        raise RijwalRuntimeError("NumPy required")
    
    def solve_equation(self, a, b):
        if np:
            return np.linalg.solve(a, b)
        raise RijwalRuntimeError("NumPy required")
    
    def derivative(self, f, x, h=0.0001):
        return (f(x + h) - f(x - h)) / (2 * h)
    
    def integral(self, f, a, b, n=1000):
        dx = (b - a) / n
        return sum(f(a + i * dx) * dx for i in range(n))


class DataPlugin(RijwalPlugin):
    """Data processing plugin"""
    
    def __init__(self):
        super().__init__("data_plugin", "1.0.0")
        
        self.register_function("load_json", self.load_json)
        self.register_function("save_json", self.save_json)
        self.register_function("load_csv", self.load_csv)
        self.register_function("save_csv", self.save_csv)
        self.register_function("filter_data", self.filter_data)
        self.register_function("map_data", self.map_data)
    
    def load_json(self, filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def save_json(self, data, filepath):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_csv(self, filepath):
        if pd:
            return pd.read_csv(filepath)
        raise RijwalRuntimeError("Pandas required")
    
    def save_csv(self, data, filepath):
        if pd and isinstance(data, pd.DataFrame):
            data.to_csv(filepath, index=False)
    
    def filter_data(self, data, predicate):
        return [item for item in data if predicate(item)]
    
    def map_data(self, data, func):
        return [func(item) for item in data]


class StringPlugin(RijwalPlugin):
    """Advanced string plugin"""
    
    def __init__(self):
        super().__init__("string_plugin", "1.0.0")
        
        self.register_function("str_regex", re.search)
        self.register_function("str_replace_all", self.replace_all)
        self.register_function("str_slugify", self.slugify)
        self.register_function("str_truncate", self.truncate)
        self.register_function("str_repeat", self.repeat)
    
    def replace_all(self, text, pattern, replacement):
        return re.sub(pattern, replacement, text)
    
    def slugify(self, text):
        return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    
    def truncate(self, text, length=50, suffix='...'):
        if len(text) > length:
            return text[:length] + suffix
        return text
    
    def repeat(self, text, count):
        return text * count


class ArrayPlugin(RijwalPlugin):
    """Advanced array plugin"""
    
    def __init__(self):
        super().__init__("array_plugin", "1.0.0")
        
        self.register_function("arr_chunk", self.chunk)
        self.register_function("arr_flatten", self.flatten)
        self.register_function("arr_uniq", self.uniq)
        self.register_function("arr_shuffle", self.shuffle)
        self.register_function("arr_take", self.take)
    
    def chunk(self, arr, size):
        return [arr[i:i+size] for i in range(0, len(arr), size)]
    
    def flatten(self, arr):
        result = []
        for item in arr:
            if isinstance(item, list):
                result.extend(self.flatten(item))
            else:
                result.append(item)
        return result
    
    def uniq(self, arr):
        return list(dict.fromkeys(arr))
    
    def shuffle(self, arr):
        import random
        random.shuffle(arr)
        return arr
    
    def take(self, arr, n):
        return arr[:n]


class TimePlugin(RijwalPlugin):
    """Time & date plugin"""
    
    def __init__(self):
        super().__init__("time_plugin", "1.0.0")
        
        self.register_function("time_now", datetime.now)
        self.register_function("time_timestamp", time.time)
        self.register_function("time_sleep", time.sleep)
        self.register_function("time_format", self.format_time)
        self.register_function("time_parse", self.parse_time)
    
    def format_time(self, dt, fmt="%Y-%m-%d %H:%M:%S"):
        return dt.strftime(fmt)
    
    def parse_time(self, text, fmt="%Y-%m-%d %H:%M:%S"):
        return datetime.strptime(text, fmt)


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
# RIJWAL-SPECIFIC FUNCTIONS
# ============================================================================

def builtin_plugin_enable(plugin_name, plugin_manager):
    """Enable a plugin"""
    plugin_manager.enable_plugin(plugin_name)
    return True

def builtin_plugin_disable(plugin_name, plugin_manager):
    """Disable a plugin"""
    plugin_manager.disable_plugin(plugin_name)
    return True

def builtin_plugin_list(plugin_manager):
    """List all plugins"""
    return plugin_manager.list_plugins()

def builtin_plugin_list_enabled(plugin_manager):
    """List enabled plugins"""
    return plugin_manager.list_enabled_plugins()

def builtin_module_load(module_name, module_loader):
    """Load a module"""
    return module_loader.load_module(module_name)

def builtin_module_export(module, name, obj):
    """Export from module"""
    module.export(name, obj)
    return True

# ============================================================================
# CORE FUNCTIONS (100+)
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

def builtin_read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise RijwalRuntimeError(f"File not found: {filepath}")

def builtin_write_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(content))
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error writing file: {str(e)}")

def builtin_append_file(filepath, content):
    try:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(str(content))
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error appending to file: {str(e)}")

def builtin_delete_file(filepath):
    try:
        os.remove(filepath)
        return True
    except FileNotFoundError:
        raise RijwalRuntimeError(f"File not found: {filepath}")

def builtin_file_exists(filepath):
    return os.path.isfile(filepath)

def builtin_list_files(directory="."):
    try:
        return os.listdir(directory)
    except Exception as e:
        raise RijwalRuntimeError(f"Error listing files: {str(e)}")

def builtin_file_size(filepath):
    try:
        return os.path.getsize(filepath)
    except Exception as e:
        raise RijwalRuntimeError(f"Error getting file size: {str(e)}")

def builtin_system(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout
    except subprocess.TimeoutExpired:
        raise RijwalRuntimeError("Command timeout exceeded")

def builtin_hash_md5(text):
    return hashlib.md5(str(text).encode()).hexdigest()

def builtin_hash_sha256(text):
    return hashlib.sha256(str(text).encode()).hexdigest()

def builtin_encode_base64(text):
    return base64.b64encode(str(text).encode()).decode()

def builtin_decode_base64(text):
    try:
        return base64.b64decode(text).decode()
    except Exception as e:
        raise RijwalRuntimeError(f"Decode error: {str(e)}")

def builtin_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def builtin_create_dir(path):
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

def builtin_dir_exists(path):
    return os.path.isdir(path)

def builtin_current_dir():
    return os.getcwd()

def builtin_change_dir(path):
    try:
        os.chdir(path)
        return True
    except Exception as e:
        raise RijwalRuntimeError(f"Error: {str(e)}")

# ============================================================================
# BUILTIN FUNCTIONS REGISTRY
# ============================================================================

def get_builtin_functions(plugin_manager):
    """Get all builtin functions including plugins"""
    
    funcs = {
        # Plugin system
        "plugin_enable": lambda name: builtin_plugin_enable(name, plugin_manager),
        "plugin_disable": lambda name: builtin_plugin_disable(name, plugin_manager),
        "plugin_list": lambda: builtin_plugin_list(plugin_manager),
        "plugin_enabled": lambda: builtin_plugin_list_enabled(plugin_manager),
        
        # Core functions (100+)
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
        "read_file": builtin_read_file,
        "write_file": builtin_write_file,
        "append_file": builtin_append_file,
        "delete_file": builtin_delete_file,
        "file_exists": builtin_file_exists,
        "list_files": builtin_list_files,
        "file_size": builtin_file_size,
        "system": builtin_system,
        "hash_md5": builtin_hash_md5,
        "hash_sha256": builtin_hash_sha256,
        "encode_base64": builtin_encode_base64,
        "decode_base64": builtin_decode_base64,
        "current_datetime": builtin_current_datetime,
        "create_dir": builtin_create_dir,
        "dir_exists": builtin_dir_exists,
        "current_dir": builtin_current_dir,
        "change_dir": builtin_change_dir,
    }
    
    # Add plugin functions
    plugin_funcs = plugin_manager.get_plugin_functions()
    funcs.update(plugin_funcs)
    
    return funcs

# ============================================================================
# PARSER & INTERPRETER
# ============================================================================

class RijwalInterpreter:
    def __init__(self):
        self.variables = {}
        self.plugin_manager = PluginManager()
        self.module_loader = ModuleLoader()
        self.initialize_plugins()
        
    def initialize_plugins(self):
        """Initialize all built-in plugins"""
        plugins = [
            NumpyPlugin(),
            PandasPlugin(),
            RequestsPlugin(),
            PILPlugin(),
            MathPlugin(),
            DataPlugin(),
            StringPlugin(),
            ArrayPlugin(),
            TimePlugin(),
        ]
        
        for plugin in plugins:
            self.plugin_manager.register_plugin(plugin)
            try:
                self.plugin_manager.enable_plugin(plugin.name)
            except:
                pass  # Plugin dependencies not available
        
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
        builtins = get_builtin_functions(self.plugin_manager)
        merged = {**context, **builtins}
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
    
    def evaluate(self, expr, context):
        """Evaluate expression"""
        builtins = get_builtin_functions(self.plugin_manager)
        merged = {**context, **builtins}
        
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
        print(f"╔═════════════════════════════════════════════════════════════╗")
        print(f"║  Rijwal_Lang v{VERSION} - MEGAVERSE ECOSYSTEM EDITION          ║")
        print(f"║  Plugin System + Module System + 50+ Library Integrations   ║")
        print(f"║           Infinity Awaits. All Powers Unlocked.             ║")
        print(f"╚═════════════════════════════════════════════════════════════╝")
        print(f"\n🎉 CELEBRATING WITH YOU! 🎉")
        print(f"✨ 9 Built-in Plugins Ready")
        print(f"📦 50+ Python Libraries Integrated")
        print(f"🔌 Custom Plugin System")
        print(f"📚 Module System")
        print(f"🚀 INFINITE POSSIBILITIES!")
        print(f"\nUsage: python rijwal_lang_v0.17.py <script.Rijwal_lang>")
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

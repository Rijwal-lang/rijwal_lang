#!/usr/bin/env python3
"""
Rijwal_Lang Web Server
Serves the IDE and executes Rijwal_Lang code
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import subprocess
import tempfile
import json
from pathlib import Path

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Get the directory of the engine
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_PATH = os.path.join(SCRIPT_DIR, 'rijwal_lang_enhanced.py')

@app.route('/')
def index():
    """Serve the IDE"""
    return render_template('index.html')

@app.route('/api/execute', methods=['POST'])
def execute_code():
    """Execute Rijwal_Lang code"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        filename = data.get('filename', 'temp.Rijwal_lang')
        
        if not code.strip():
            return jsonify({
                'success': False,
                'error': 'No code provided'
            })
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.Rijwal_lang',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            # Run the code
            result = subprocess.run(
                [sys.executable, ENGINE_PATH, temp_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parse output
            output_lines = result.stdout.strip().split('\n') if result.stdout else []
            error_lines = result.stderr.strip().split('\n') if result.stderr else []
            
            if result.returncode == 0:
                return jsonify({
                    'success': True,
                    'output': output_lines
                })
            else:
                return jsonify({
                    'success': False,
                    'error': error_lines[0] if error_lines else 'Unknown error',
                    'details': '\n'.join(error_lines)
                })
        
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Code execution timeout (>30 seconds)',
            'details': 'Your code is taking too long to execute'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/save', methods=['POST'])
def save_file():
    """Save code to file"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        filename = data.get('filename', 'code.Rijwal_lang')
        
        if not filename.endswith(('.Rijwal_lang', '.RL')):
            filename += '.Rijwal_lang'
        
        # Create projects directory if not exists
        projects_dir = os.path.join(SCRIPT_DIR, 'user_projects')
        os.makedirs(projects_dir, exist_ok=True)
        
        filepath = os.path.join(projects_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        
        return jsonify({
            'success': True,
            'path': filepath,
            'message': f'Saved to {filename}'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/load', methods=['GET'])
def load_file():
    """Load saved projects"""
    try:
        projects_dir = os.path.join(SCRIPT_DIR, 'user_projects')
        if not os.path.exists(projects_dir):
            return jsonify({'files': []})
        
        files = []
        for f in os.listdir(projects_dir):
            if f.endswith(('.Rijwal_lang', '.RL')):
                filepath = os.path.join(projects_dir, f)
                files.append({
                    'name': f,
                    'size': os.path.getsize(filepath),
                    'modified': os.path.getmtime(filepath)
                })
        
        return jsonify({'files': files})
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/docs', methods=['GET'])
def get_docs():
    """Get language documentation"""
    docs = {
        'version': '0.13',
        'statements': [
            {
                'name': 'Print',
                'syntax': 'Print "message"',
                'description': 'Display text to console',
                'example': 'Print "Hello, World!"'
            },
            {
                'name': 'Let',
                'syntax': 'Let variable = value',
                'description': 'Create or update variable',
                'example': 'Let x = 5\nLet name = "Alice"'
            },
            {
                'name': 'Input',
                'syntax': 'Input variable',
                'description': 'Get input from user',
                'example': 'Input age'
            },
            {
                'name': 'Function',
                'syntax': 'Function name(args):\n    Return value',
                'description': 'Define a reusable function',
                'example': 'Function add(a, b):\n    Return a + b'
            },
            {
                'name': 'When Program Starts',
                'syntax': 'When Program Starts:\n    statements',
                'description': 'Entry point of program',
                'example': 'When Program Starts:\n    Print "Starting..."'
            },
            {
                'name': 'Every (Timer)',
                'syntax': 'Every N second:\n    statements',
                'description': 'Repeat block every N seconds',
                'example': 'Every 1 second:\n    Print "Tick"'
            },
            {
                'name': 'Import',
                'syntax': 'Import "filename"',
                'description': 'Import functions from another file',
                'example': 'Import "utils.RL"'
            }
        ],
        'builtin_functions': [
            {'name': 'len(x)', 'description': 'Length of string'},
            {'name': 'type(x)', 'description': 'Get type of value'},
            {'name': 'abs(x)', 'description': 'Absolute value'},
            {'name': 'max(a, b, ...)', 'description': 'Maximum value'},
            {'name': 'min(a, b, ...)', 'description': 'Minimum value'},
            {'name': 'round(x)', 'description': 'Round number'},
            {'name': 'str(x)', 'description': 'Convert to string'},
            {'name': 'int(x)', 'description': 'Convert to integer'},
            {'name': 'float(x)', 'description': 'Convert to float'},
            {'name': 'upper(s)', 'description': 'Uppercase string'},
            {'name': 'lower(s)', 'description': 'Lowercase string'},
            {'name': 'split(s, sep)', 'description': 'Split string'},
            {'name': 'reverse(x)', 'description': 'Reverse string or list'},
        ]
    }
    return jsonify(docs)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    print(f"🚀 Rijwal_Lang Web Server v0.13")
    print(f"📍 IDE: http://localhost:5000")
    print(f"⚙️  Engine: {ENGINE_PATH}")
    print(f"💾 Projects: {os.path.join(SCRIPT_DIR, 'user_projects')}")
    print(f"\n✨ Open your browser and go to http://localhost:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')

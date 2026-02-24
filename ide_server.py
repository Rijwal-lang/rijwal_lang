#!/usr/bin/env python3
"""
Rijwal_Lang Web Server
Serves the IDE and executes Rijwal_Lang code
"""

from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import subprocess
import tempfile
import json
from pathlib import Path
from rijwal_ai_assistant import AIAssistant

try:
    from rijwal_lang_enhanced import BUILTIN_DOCS
except Exception:
    BUILTIN_DOCS = {}

app = Flask(__name__)
IDE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ide")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Get the directory of the engine
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_PATH = os.path.join(SCRIPT_DIR, 'rijwal_lang_enhanced.py')
AI_ASSISTANT = AIAssistant(provider='openai')

@app.route('/')
def index():
    """Serve the modern IDE"""
    return send_from_directory(IDE_DIR, 'index.html')

@app.route('/legacy')
def legacy_ide():
    """Serve legacy IDE with games."""
    return send_from_directory(SCRIPT_DIR, 'ide_with_games.html')

@app.route('/idle')
def idle_info():
    """Expose IDLE launcher information."""
    return jsonify({
        'name': 'Rijwal_Lang IDLE',
        'launch': f'{sys.executable} rijwal_idle.py',
        'description': 'Interactive shell for quick Rijwal_Lang testing.'
    })

@app.route('/ide/<path:asset_path>')
def ide_assets(asset_path):
    """Serve modern IDE static assets (JS/CSS)."""
    return send_from_directory(IDE_DIR, asset_path)

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
    builtin_functions = [
        {'name': name, 'description': desc}
        for name, desc in BUILTIN_DOCS.items()
    ]

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
        'builtin_functions': builtin_functions
    }
    return jsonify(docs)



@app.route('/api/ai-assist', methods=['POST'])
def ai_assist():
    """AI assistant endpoint for IDE buddy."""
    try:
        data = request.get_json() or {}
        prompt = data.get('prompt', '').strip()
        code = data.get('code', '')

        if not prompt:
            return jsonify({'success': False, 'error': 'No prompt provided'}), 400

        result = AI_ASSISTANT.chat(prompt, code_context=code)
        return jsonify({
            'success': True,
            'response': result.get('response', ''),
            'provider': result.get('provider', 'mock'),
            'model': result.get('model', 'unknown')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health endpoint for IDE and IDLE integrations."""
    return jsonify({
        'success': True,
        'engine_exists': os.path.exists(ENGINE_PATH),
        'ide_exists': os.path.exists(os.path.join(IDE_DIR, 'index.html')),
        'idle_exists': os.path.exists(os.path.join(SCRIPT_DIR, 'rijwal_idle.py')),
    })

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

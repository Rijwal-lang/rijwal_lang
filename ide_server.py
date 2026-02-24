#!/usr/bin/env python3
"""
Rijwal_Lang Web Server
Serves the IDE and executes Rijwal_Lang code
"""

from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import subprocess
import shutil
import tempfile
import json
import stat
import re
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
AI_ASSISTANT = AIAssistant(provider='local')
MISSION_STATEMENT = "Rijwal is the fastest way for beginners to go from idea → working code with AI help."
PLUGIN_DIR = Path(SCRIPT_DIR) / 'plugins'
PLUGIN_NAME_RE = re.compile(r'^[A-Za-z0-9_-]+$')

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

def normalize_engine_output(lines):
    """Remove runtime banner/noise lines from engine output."""
    cleaned = []
    for line in lines:
        if line.startswith('[Rijwal_Lang] 🚀'):
            continue
        if line.startswith('[Rijwal_Lang] ✅ Completed'):
            continue
        if line.strip() == '':
            continue
        cleaned.append(line)
    return cleaned


def run_rijwal_code(code, filename='temp.Rijwal_lang', timeout=30):
    """Run Rijwal code and return normalized result dict."""
    if not code.strip():
        return {'success': False, 'error': 'No code provided'}

    safe_prefix = Path(filename).stem[:20] if filename else 'temp'
    with tempfile.NamedTemporaryFile(
        mode='w',
        prefix=f'{safe_prefix}_',
        suffix='.Rijwal_lang',
        delete=False,
        encoding='utf-8'
    ) as f:
        f.write(code)
        temp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, ENGINE_PATH, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        output_lines = result.stdout.strip().split('\n') if result.stdout else []
        output_lines = normalize_engine_output(output_lines)
        error_lines = result.stderr.strip().split('\n') if result.stderr else []

        if result.returncode == 0:
            return {'success': True, 'output': output_lines}

        return {
            'success': False,
            'error': error_lines[0] if error_lines else 'Unknown error',
            'details': '\n'.join(error_lines),
            'output': output_lines,
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': f'Code execution timeout (>{timeout} seconds)',
            'details': 'Your code is taking too long to execute',
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)




def compile_rijwal_to_python(code):
    """Compile a small Rijwal subset to Python + IR instructions."""
    py_lines = ["# Auto-generated from Rijwal_Lang", "def main():"]
    ir = []
    in_start = False

    for raw in code.splitlines():
        stripped = raw.strip()
        low = stripped.lower()
        if not stripped or stripped.startswith('#'):
            continue

        if low.startswith('when program starts'):
            in_start = True
            ir.append({'op': 'START_BLOCK'})
            continue

        if not in_start:
            continue

        if low.startswith('print '):
            expr = stripped[6:].strip()
            py_lines.append(f"    print({expr})")
            ir.append({'op': 'PRINT', 'arg': expr})
            continue

        if low.startswith('let '):
            rest = stripped[4:]
            if '=' in rest:
                name, expr = rest.split('=', 1)
                name = name.strip()
                expr = expr.strip()
                py_lines.append(f"    {name} = {expr}")
                ir.append({'op': 'LET', 'name': name, 'expr': expr})
            continue

        # fallback as comment for unsupported commands
        py_lines.append(f"    # Unsupported in tiny compiler: {stripped}")
        ir.append({'op': 'UNSUPPORTED', 'raw': stripped})

    if len(py_lines) == 2:
        py_lines.append("    pass")

    py_lines.extend(["", "if __name__ == '__main__':", "    main()"])
    return {'python_code': '\n'.join(py_lines), 'ir': ir}


def ensure_exports_dir():
    exports_dir = os.path.join(SCRIPT_DIR, 'exports')
    os.makedirs(exports_dir, exist_ok=True)
    return exports_dir

@app.route('/api/execute', methods=['POST'])
def execute_code():
    """Execute Rijwal_Lang code"""
    try:
        data = request.get_json() or {}
        code = data.get('code', '')
        filename = data.get('filename', 'temp.Rijwal_lang')
        return jsonify(run_rijwal_code(code, filename=filename, timeout=30))
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
        'mission': MISSION_STATEMENT,
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
                'name': 'Plugin API',
                'syntax': 'Use Plugin "name"',
                'description': 'Load a local plugin into language runtime',
                'example': 'Use Plugin "math_extra"'
            },
            {
                'name': 'AI inline',
                'syntax': 'AI "prompt"',
                'description': 'Ask embedded local AI inside code',
                'example': 'AI "Explain this program"'
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







@app.route('/api/cloud/execute', methods=['POST'])
def cloud_execute_code():
    """Cloud-style execution alias (same engine, higher timeout)."""
    try:
        data = request.get_json() or {}
        code = data.get('code', '')
        filename = data.get('filename', 'cloud_job.rjwl')
        return jsonify(run_rijwal_code(code, filename=filename, timeout=45))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/compile', methods=['POST'])
def compile_code():
    """Compile Rijwal source to tiny Python target + IR."""
    try:
        data = request.get_json() or {}
        code = data.get('code', '')
        if not code.strip():
            return jsonify({'success': False, 'error': 'No code provided'}), 400

        result = compile_rijwal_to_python(code)
        return jsonify({'success': True, **result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/export/executable', methods=['POST'])
def export_executable():
    """Export a runnable Python script generated from Rijwal code."""
    try:
        data = request.get_json() or {}
        code = data.get('code', '')
        name = (data.get('name') or 'rijwal_export').strip()
        if not code.strip():
            return jsonify({'success': False, 'error': 'No code provided'}), 400

        safe_name = ''.join(ch for ch in name if ch.isalnum() or ch in ('_', '-')).strip('_-') or 'rijwal_export'
        compiled = compile_rijwal_to_python(code)
        exports_dir = ensure_exports_dir()
        out_path = os.path.join(exports_dir, f"{safe_name}.py")

        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(compiled['python_code'])

        mode = os.stat(out_path).st_mode
        os.chmod(out_path, mode | stat.S_IXUSR)

        return jsonify({
            'success': True,
            'path': out_path,
            'python_code': compiled['python_code'],
            'note': 'Run with: python ' + out_path
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/terminal', methods=['POST'])
def terminal_command():
    """Custom Rijwal terminal command endpoint."""
    try:
        data = request.get_json() or {}
        command = (data.get('command') or '').strip()
        command_lower = command.lower()
        current_code = data.get('code', '')

        if not command:
            return jsonify({'success': False, 'error': 'No terminal command provided'}), 400

        if command_lower == 'help':
            return jsonify({'success': True, 'output': [
                'Rijwal Terminal Commands:',
                '  help        Show this help',
                '  run         Run current editor code',
                '  version     Show language version',
                '  docs        Show docs endpoint',
                '  health      Show API health endpoint',
                '  clear       Clear terminal output (client side)',
                '  Any other text is executed as Rijwal code snippet.'
            ]})

        if command_lower == 'version':
            return jsonify({'success': True, 'output': ['Rijwal_Lang terminal v1 (engine v0.13)']})

        if command_lower == 'docs':
            return jsonify({'success': True, 'output': ['Open docs API: /api/docs']})

        if command_lower == 'health':
            return jsonify({'success': True, 'output': ['Open health API: /api/health']})

        if command_lower == 'run':
            return jsonify(run_rijwal_code(current_code, filename='terminal_run.Rijwal_lang', timeout=30))

        if command_lower == 'clear':
            return jsonify({'success': True, 'output': []})

        snippet = command
        if not snippet.lower().startswith(('when program starts', 'function ', 'every ', 'import ', 'python:', 'js:', 'print ', 'let ', 'input ')):
            snippet = f'When Program Starts:\n    {command}'

        return jsonify(run_rijwal_code(snippet, filename='terminal_snippet.Rijwal_lang', timeout=20))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500





@app.route('/api/ai/prompt', methods=['POST'])
def update_ai_prompt():
    """Dynamically update AI buddy system prompt."""
    try:
        data = request.get_json() or {}
        prompt = data.get('prompt', '')
        result = AI_ASSISTANT.update_system_prompt(prompt)
        if not result.get('success'):
            return jsonify(result), 400
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/plugins/list', methods=['GET'])
def list_plugins():
    """List available and installed plugins."""
    try:
        available = []
        available_dir = PLUGIN_DIR / 'available'
        if available_dir.exists():
            for f in sorted(available_dir.glob('*.py')):
                available.append(f.stem)

        installed = []
        if PLUGIN_DIR.exists():
            for f in sorted(PLUGIN_DIR.glob('*.py')):
                installed.append(f.stem)

        return jsonify({'success': True, 'available': available, 'installed': installed})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/plugins/install', methods=['POST'])
def install_plugin():
    """Install a plugin from local available catalog to active plugins dir."""
    try:
        data = request.get_json() or {}
        name = (data.get('name') or '').strip()
        if not name:
            return jsonify({'success': False, 'error': 'No plugin name provided'}), 400
        if not PLUGIN_NAME_RE.fullmatch(name):
            return jsonify({'success': False, 'error': 'Invalid plugin name'}), 400

        src = PLUGIN_DIR / 'available' / f'{name}.py'
        dst = PLUGIN_DIR / f'{name}.py'
        if not src.exists():
            return jsonify({'success': False, 'error': f'Plugin not found in catalog: {name}'}), 404

        PLUGIN_DIR.mkdir(exist_ok=True, parents=True)
        shutil.copyfile(src, dst)
        return jsonify({'success': True, 'installed': name, 'path': str(dst)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/plugins/auto-update', methods=['POST'])
def auto_update_plugins():
    """Auto-install missing plugins from local index catalog."""
    try:
        index_file = PLUGIN_DIR / 'index.json'
        if not index_file.exists():
            return jsonify({'success': False, 'error': 'plugins/index.json not found'}), 404

        index_data = json.loads(index_file.read_text(encoding='utf-8'))
        installed = []
        for item in index_data.get('plugins', []):
            name = item.get('name')
            if not name:
                continue
            if not isinstance(name, str) or not PLUGIN_NAME_RE.fullmatch(name):
                continue
            dst = PLUGIN_DIR / f'{name}.py'
            if dst.exists():
                continue
            src_rel = item.get('source', f'plugins/available/{name}.py')
            src = Path(SCRIPT_DIR) / src_rel
            if src.exists():
                shutil.copyfile(src, dst)
                installed.append(name)

        return jsonify({'success': True, 'installed': installed})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/evolve', methods=['POST'])
def evolve_project():
    """Generate self-evolution roadmap for language + AI buddy."""
    try:
        data = request.get_json() or {}
        goals = (data.get('goals') or '').strip()
        code = data.get('code', '')

        if not goals:
            return jsonify({'success': False, 'error': 'No goals provided'}), 400

        evolution = AI_ASSISTANT.evolve_language(goals, code_context=code)
        return jsonify({
            'success': True,
            'mission': MISSION_STATEMENT,
            'plan': evolution.get('plan', ''),
            'provider': evolution.get('provider', 'mock'),
            'model': evolution.get('model', 'unknown'),
            'timestamp': evolution.get('timestamp')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

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
        'mission': MISSION_STATEMENT,
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

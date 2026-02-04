#!/usr/bin/env python3
"""
RIJWAL_LANG IDE LAUNCHER
========================

Main entry point for the standalone IDE application.
Launches Flask server and opens web browser.
"""

import sys
import os
import time
import webbrowser
import threading
from pathlib import Path

# Ensure we can find our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("""
╔═══════════════════════════════════════════════════════════════════╗
║                  RIJWAL_LANG IDE v0.17                            ║
║            Advanced Programming Language & Environment            ║
╚═══════════════════════════════════════════════════════════════════╝
""")

print("Initializing Rijwal_Lang IDE...")
print()

# Check for required files
required_files = [
    "ide_with_games.html",
    "rijwal_lang_v0.17.py",
    "rijwal_games.py",
]

print("Checking required files...")
for file in required_files:
    if os.path.exists(file):
        print(f"  [OK] {file}")
    else:
        print(f"  [MISSING] {file}")
        print(f"\nERROR: Cannot find {file}")
        print("The IDE cannot start without all required files.")
        input("Press Enter to exit...")
        sys.exit(1)

print()

# Import Flask
try:
    from flask import Flask, render_template_string, request, jsonify
    from flask_cors import CORS
    import importlib.util
except ImportError as e:
    print(f"ERROR: Missing Python package: {e}")
    print("Please install Flask and Flask-CORS:")
    print("  pip install flask flask-cors")
    input("Press Enter to exit...")
    sys.exit(1)

# Import marketplace
try:
    from marketplace_api import marketplace_bp
    from rijwal_ai_assistant import AIAssistantManager
    print("Marketplace API loaded")
except Exception as e:
    print(f"[WARN] Marketplace not available: {e}")
    marketplace_bp = None

print("Loading Rijwal_Lang engine...")

# Load the interpreter
try:
    spec = importlib.util.spec_from_file_location("rijwal_lang_v0_17", "rijwal_lang_v0.17.py")
    rijwal_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rijwal_module)
    RijwalInterpreter = rijwal_module.RijwalInterpreter
    print("  [OK] Engine loaded")
except Exception as e:
    print(f"  [ERROR] Failed to load engine: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

print("Loading game system...")

# Load the game system
try:
    spec = importlib.util.spec_from_file_location("rijwal_games", "rijwal_games.py")
    games_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(games_module)
    GameManager = games_module.GameManager
    print("  [OK] Games loaded")
except Exception as e:
    print(f"  [WARN] Game system not available: {e}")

print()

# Create Flask app
app = Flask(__name__)
CORS(app)

# Register marketplace API
if marketplace_bp:
    app.register_blueprint(marketplace_bp)

# Global interpreter instance
interpreter = RijwalInterpreter()

# Port configuration
PORT = 5000
HOST = "127.0.0.1"

print("Setting up web server...")
print(f"  - Host: {HOST}")
print(f"  - Port: {PORT}")
print()

# ============================================================================
# ROUTES
# ============================================================================

@app.route("/")
def index():
    """Serve the IDE interface"""
    with open("ide_with_games.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return html_content

@app.route("/api/execute", methods=["POST"])
def execute_code():
    """Execute Rijwal_Lang code"""
    try:
        code = request.json.get("code", "")
        
        if not code.strip():
            return jsonify({"error": "Empty code"})
        
        # Capture output
        import io
        from contextlib import redirect_stdout
        
        output_buffer = io.StringIO()
        
        try:
            with redirect_stdout(output_buffer):
                interpreter.execute(code)
            
            output = output_buffer.getvalue()
            
            return jsonify({
                "success": True,
                "output": output
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {e}"
        })

@app.route("/api/plugins", methods=["GET"])
def get_plugins():
    """Get list of available plugins"""
    try:
        plugins = interpreter.plugin_manager.list_plugins()
        return jsonify({
            "success": True,
            "plugins": list(plugins)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/api/functions", methods=["GET"])
def get_functions():
    """Get list of available functions"""
    try:
        functions = list(interpreter.functions.keys())[:50]  # Top 50
        return jsonify({
            "success": True,
            "functions": functions,
            "total": len(interpreter.functions)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/api/info", methods=["GET"])
def get_info():
    """Get system information"""
    try:
        return jsonify({
            "success": True,
            "name": "Rijwal_Lang IDE v0.17",
            "version": "0.17",
            "functions": len(interpreter.functions),
            "plugins": len(interpreter.plugin_manager.list_plugins()),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/api/ai/chat", methods=["POST"])
def ai_chat():
    """AI Assistant chat endpoint"""
    try:
        # Try to import the AI assistant
        try:
            from rijwal_ai_assistant import AIAssistantManager
            ai = AIAssistantManager.get_instance()
        except ImportError:
            # Fallback mock responses if AI module not available
            ai = None
        
        message = request.json.get("message", "")
        code_context = request.json.get("code", "")
        
        if not message.strip():
            return jsonify({
                "success": False,
                "error": "Empty message"
            })
        
        if ai:
            # Use real AI assistant
            response = ai.chat(message, code_context)
            return jsonify({
                "success": True,
                "response": response["response"],
                "model": response.get("model", "ai-assistant"),
                "timestamp": response.get("timestamp")
            })
        else:
            # Fallback to mock responses
            mock_response = generate_mock_ai_response(message)
            return jsonify({
                "success": True,
                "response": mock_response,
                "model": "mock-assistant",
                "note": "Mock response (AI module not available)"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

def generate_mock_ai_response(message):
    """Generate mock AI responses"""
    lower = message.lower()
    
    responses = {
        "error": "🔧 Error? Let's debug!\n\n1. Check for syntax errors (missing brackets, quotes)\n2. Verify all variables are defined\n3. Make sure plugin dependencies are loaded\n4. Print variable values to identify the issue\n\nTry adding print statements!",
        "example": "💡 Here's a quick example:\n\nLet numbers = [1, 2, 3, 4, 5]\nfor each item in numbers:\n    if item > 2:\n        print item * 2\n\nThis filters and transforms data!",
        "plugin": "📦 Available plugins: numpy, pandas, requests, pil, math, string, array, data, time. Use 'use plugin_name' to load!",
        "game": "🎮 Take a break! 10 games available in the sidebar!",
        "refactor": "✨ Tips: Extract functions, use meaningful names, avoid repetition, add comments, use built-ins!",
        "explain": "📚 Variables, Functions, Loops, Plugins, Games - what interests you?",
    }
    
    if any(word in lower for word in ["error", "bug", "wrong"]):
        return responses["error"]
    elif any(word in lower for word in ["example", "sample"]):
        return responses["example"]
    elif any(word in lower for word in ["plugin", "import"]):
        return responses["plugin"]
    elif any(word in lower for word in ["game", "fun"]):
        return responses["game"]
    elif any(word in lower for word in ["refactor", "improve"]):
        return responses["refactor"]
    else:
        return responses["explain"]

# ============================================================================
# SERVER LAUNCH
# ============================================================================

def open_browser():
    """Open web browser after server starts"""
    time.sleep(2)  # Wait for server to start
    url = f"http://{HOST}:{PORT}"
    print(f"Opening browser to {url}...")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print(f"Please open manually: {url}")

if __name__ == "__main__":
    print("=" * 70)
    print("STARTING RIJWAL_LANG IDE")
    print("=" * 70)
    print()
    print(f"IDE will be available at: http://{HOST}:{PORT}")
    print()
    print("Press Ctrl+C to stop the server")
    print()
    
    # Start browser in background thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        # Start Flask server
        app.run(host=HOST, port=PORT, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print()
        print()
        print("Server stopped.")
        sys.exit(0)

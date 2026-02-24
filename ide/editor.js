// ========== FILE MANAGEMENT ==========
let files = {
    "new_project.Rijwal_lang": `When Program Starts:
    Print "Hello, Rijwal_Lang!"
`
};

let currentFile = "new_project.Rijwal_lang";
let fileHistory = {};

// Load files from localStorage
function loadFiles() {
    const saved = localStorage.getItem('rijwal_files');
    if (saved) {
        files = JSON.parse(saved);
    }
    const savedCurrent = localStorage.getItem('rijwal_current');
    if (savedCurrent) {
        currentFile = savedCurrent;
    }
}

function saveFiles() {
    localStorage.setItem('rijwal_files', JSON.stringify(files));
    localStorage.setItem('rijwal_current', currentFile);
}

// ========== EDITOR EVENTS ==========
const editor = document.getElementById('editor');
const console_output = document.querySelector('.console');

editor.addEventListener('input', () => {
    files[currentFile] = editor.value;
    saveFiles();
    updateLineNumbers();
});

editor.addEventListener('keydown', (e) => {
    // Tab support
    if (e.key === 'Tab') {
        e.preventDefault();
        const start = editor.selectionStart;
        const end = editor.selectionEnd;
        editor.value = editor.value.substring(0, start) + '\t' + editor.value.substring(end);
        editor.selectionStart = editor.selectionEnd = start + 1;
        files[currentFile] = editor.value;
        saveFiles();
        updateLineNumbers();
    }
    
    // Ctrl+Enter to run
    if (e.ctrlKey && e.key === 'Enter') {
        runCode();
    }
});

// ========== FILE TREE MANAGEMENT ==========
function updateFileTree() {
    const fileTree = document.getElementById('fileTree');
    fileTree.innerHTML = '';
    
    Object.keys(files).forEach(fname => {
        const div = document.createElement('div');
        div.className = `file-item ${fname === currentFile ? 'active' : ''}`;
        div.textContent = '📄 ' + fname;
        div.dataset.file = fname;
        div.addEventListener('click', () => openFile(fname));
        fileTree.appendChild(div);
    });
}

function openFile(fname) {
    currentFile = fname;
    editor.value = files[fname] || '';
    saveFiles();
    updateFileTree();
    updateEditorTab();
    updateLineNumbers();
}

function newFile() {
    let counter = 1;
    let newName = `project_${counter}.Rijwal_lang`;
    while (files[newName]) {
        counter++;
        newName = `project_${counter}.Rijwal_lang`;
    }
    files[newName] = '';
    currentFile = newName;
    editor.value = '';
    saveFiles();
    updateFileTree();
    updateEditorTab();
    updateLineNumbers();
}

// ========== EDITOR TABS ==========
function updateEditorTab() {
    const tabs = document.querySelectorAll('.editor-tabs .tab');
    tabs.forEach(t => t.remove());
    
    Object.keys(files).forEach(fname => {
        const tab = document.createElement('div');
        tab.className = `tab ${fname === currentFile ? 'active' : ''}`;
        tab.innerHTML = `${fname}<span class="close-tab">×</span>`;
        tab.dataset.file = fname;
        
        tab.addEventListener('click', (e) => {
            if (e.target.classList.contains('close-tab')) {
                e.stopPropagation();
                if (Object.keys(files).length > 1) {
                    delete files[fname];
                    if (currentFile === fname) {
                        currentFile = Object.keys(files)[0];
                        editor.value = files[currentFile];
                    }
                    saveFiles();
                    updateFileTree();
                    updateEditorTab();
                }
            } else {
                openFile(fname);
            }
        });
        
        document.querySelector('.editor-tabs').appendChild(tab);
    });
}

// ========== LINE NUMBERS ==========
function updateLineNumbers() {
    const lines = editor.value.split('\n').length;
    const lineNumbers = document.getElementById('lineNumbers');
    let html = '';
    for (let i = 1; i <= lines; i++) {
        html += i + '\n';
    }
    lineNumbers.textContent = html;
}

// ========== CONSOLE OUTPUT ==========
function addConsoleOutput(message, type = 'log') {
    const line = document.createElement('div');
    line.className = `console-line ${type}`;
    line.innerHTML = `<span class="${type}">${escapeHtml(message)}</span>`;
    console_output.appendChild(line);
    console_output.scrollTop = console_output.scrollHeight;
}

function clearConsole() {
    console_output.innerHTML = '';
    addConsoleOutput('Console cleared', 'info');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ========== CODE EXECUTION ==========
async function runCode() {
    clearConsole();
    addConsoleOutput('▶️ Running...', 'info');
    
    try {
        const code = editor.value;
        if (!code.trim()) {
            addConsoleOutput('⚠️ No code to run!', 'warning');
            return;
        }
        
        // Send to server (Python backend)
        const response = await fetch('/api/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, filename: currentFile })
        });
        
        const result = await response.json();
        
        if (result.success) {
            result.output.forEach(line => {
                addConsoleOutput(line, 'log');
            });
            addConsoleOutput('✅ Completed successfully', 'info');
        } else {
            addConsoleOutput('❌ Error: ' + result.error, 'error');
            if (result.details) {
                addConsoleOutput(result.details, 'error');
            }
        }
    } catch (err) {
        addConsoleOutput('❌ Network error: ' + err.message, 'error');
        addConsoleOutput('Make sure the Python backend is running', 'warning');
    }
}

// ========== FILE OPERATIONS ==========
document.getElementById('runCode').addEventListener('click', runCode);

document.getElementById('saveFile').addEventListener('click', () => {
    const blob = new Blob([editor.value], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = currentFile;
    a.click();
    URL.revokeObjectURL(url);
    addConsoleOutput(`💾 Downloaded: ${currentFile}`, 'info');
});

document.getElementById('newFile').addEventListener('click', newFile);

document.getElementById('openFile').addEventListener('click', () => {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (ev) => {
            const fname = file.name.endsWith('.Rijwal_lang') ? file.name : file.name + '.Rijwal_lang';
            files[fname] = ev.target.result;
            currentFile = fname;
            saveFiles();
            editor.value = files[fname];
            updateFileTree();
            updateEditorTab();
            updateLineNumbers();
            addConsoleOutput(`📂 Loaded: ${fname}`, 'info');
        };
        reader.readAsText(file);
    }
});

document.getElementById('clearOutput').addEventListener('click', clearConsole);

// ========== TAB SWITCHING ==========
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        btn.classList.add('active');
        const tabId = btn.dataset.tab;
        document.getElementById(tabId).classList.add('active');
    });
});

// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', () => {
    loadFiles();
    updateFileTree();
    updateEditorTab();
    editor.value = files[currentFile];
    updateLineNumbers();
    addConsoleOutput('✨ Rijwal_Lang IDE Ready!', 'info');
    addConsoleOutput(`📄 Editing: ${currentFile}`, 'info');
});


// ========== AI BUDDY ==========
const aiBuddy = document.getElementById('aiBuddy');
const aiBuddyHeader = document.getElementById('aiBuddyHeader');
const aiBuddyChat = document.getElementById('aiBuddyChat');
const aiBuddyInput = document.getElementById('aiBuddyInput');
const aiBuddySend = document.getElementById('aiBuddySend');

function appendAiLine(message, role='ai') {
    const line = document.createElement('div');
    line.className = `ai-line ${role}`;
    line.textContent = message;
    aiBuddyChat.appendChild(line);
    aiBuddyChat.scrollTop = aiBuddyChat.scrollHeight;
}

async function askAiBuddy() {
    const prompt = aiBuddyInput.value.trim();
    if (!prompt) return;

    appendAiLine(prompt, 'user');
    aiBuddyInput.value = '';

    try {
        const response = await fetch('/api/ai-assist', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt, code: editor.value })
        });
        const data = await response.json();
        if (data.success) {
            appendAiLine(data.response, 'ai');
        } else {
            appendAiLine('AI error: ' + (data.error || 'unknown'), 'ai');
        }
    } catch (error) {
        appendAiLine('Network error while talking to AI Buddy.', 'ai');
    }
}

aiBuddySend.addEventListener('click', askAiBuddy);
aiBuddyInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') askAiBuddy();
});

(function makeBuddyDraggable() {
    let active = false;
    let offsetX = 0;
    let offsetY = 0;

    aiBuddyHeader.addEventListener('pointerdown', (e) => {
        active = true;
        const rect = aiBuddy.getBoundingClientRect();
        offsetX = e.clientX - rect.left;
        offsetY = e.clientY - rect.top;
        aiBuddyHeader.style.cursor = 'grabbing';
    });

    window.addEventListener('pointermove', (e) => {
        if (!active) return;
        const x = Math.max(0, Math.min(window.innerWidth - aiBuddy.offsetWidth, e.clientX - offsetX));
        const y = Math.max(0, Math.min(window.innerHeight - aiBuddy.offsetHeight, e.clientY - offsetY));
        aiBuddy.style.left = `${x}px`;
        aiBuddy.style.top = `${y}px`;
        aiBuddy.style.right = 'auto';
        aiBuddy.style.bottom = 'auto';
    });

    window.addEventListener('pointerup', () => {
        active = false;
        aiBuddyHeader.style.cursor = 'grab';
    });
})();

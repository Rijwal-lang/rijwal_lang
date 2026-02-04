"""
Example Plugins for Rijwal_Lang Marketplace
Ready to upload and distribute
"""

# ============================================================================
# PLUGIN 1: Django ORM Helper
# ============================================================================

DJANGO_ORM_HELPER = {
    "name": "Django ORM Helper",
    "author_id": "rijwal_team",
    "description": "AI-powered suggestions for Django ORM queries, model definitions, and optimization tips",
    "category": "AI Assistant",
    "tags": ["django", "orm", "database", "optimization"],
    "code": """
// Django ORM Helper Plugin
class DjangoORMHelper {
  static analyzeDjangoQuery(query) {
    const patterns = {
      'n_plus_one': query.includes('for') && query.includes('query'),
      'select_related': !query.includes('select_related') && query.includes('ForeignKey'),
      'prefetch_related': !query.includes('prefetch_related') && query.includes('ManyToMany'),
      'raw_sql': query.includes('raw()') && query.length > 100
    };
    
    const suggestions = [];
    if (patterns.n_plus_one) suggestions.push('⚠️ Potential N+1 query issue. Use select_related() or prefetch_related()');
    if (patterns.select_related) suggestions.push('💡 Consider using select_related() for foreign key relationships');
    if (patterns.prefetch_related) suggestions.push('💡 Consider using prefetch_related() for many-to-many relationships');
    if (patterns.raw_sql) suggestions.push('⚠️ Raw SQL detected. Consider using ORM methods when possible');
    
    return suggestions;
  }
  
  static suggestModel(fields) {
    return `
class MyModel(models.Model):
    ${fields.map(f => `${f} = models.CharField(max_length=100)`).join('\\n    ')}
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    `;
  }
}

module.exports = DjangoORMHelper;
    """
}

# ============================================================================
# PLUGIN 2: Python Performance Analyzer
# ============================================================================

PYTHON_PERFORMANCE = {
    "name": "Python Performance Analyzer",
    "author_id": "rijwal_team",
    "description": "Analyzes Python code for performance issues and suggests optimizations",
    "category": "Development Tools",
    "tags": ["python", "performance", "optimization", "profiling"],
    "code": """
// Python Performance Analyzer
class PerformanceAnalyzer {
  static analyzeCode(code) {
    const issues = [];
    
    // Check for common issues
    if (code.includes('append') && !code.includes('list comprehension')) {
      issues.push({severity: 'info', msg: 'Consider using list comprehensions for better performance'});
    }
    
    if (code.includes('for') && code.includes('in range(len(')) {
      issues.push({severity: 'warning', msg: 'Use enumerate() instead of range(len())'});
    }
    
    if (code.includes('+=') && code.includes('str')) {
      issues.push({severity: 'warning', msg: 'String concatenation is slow. Use join() instead'});
    }
    
    if (code.match(/for.*for.*for/)) {
      issues.push({severity: 'critical', msg: 'Triple nested loop detected. Consider optimization'});
    }
    
    if (code.includes('import *')) {
      issues.push({severity: 'warning', msg: 'Avoid wildcard imports. Import specific items'});
    }
    
    return {
      issues: issues,
      score: Math.max(0, 100 - issues.length * 10)
    };
  }
  
  static suggestFix(issue) {
    const fixes = {
      'list_comp': 'items = [x * 2 for x in items]',
      'enumerate': 'for i, item in enumerate(items):',
      'join': 'text = "".join(strings)',
      'import': 'from module import specific_function'
    };
    return fixes;
  }
}

module.exports = PerformanceAnalyzer;
    """
}

# ============================================================================
# PLUGIN 3: API Request Debugger
# ============================================================================

API_DEBUGGER = {
    "name": "API Request Debugger",
    "author_id": "rijwal_team",
    "description": "Debug HTTP requests and responses, format JSON, track performance",
    "category": "Development Tools",
    "tags": ["api", "http", "debugging", "json", "rest"],
    "code": """
// API Request Debugger
class APIDebugger {
  static parseRequest(url, headers, body) {
    return {
      url: url,
      domain: new URL(url).hostname,
      path: new URL(url).pathname,
      method: headers.method || 'GET',
      headers_count: Object.keys(headers).length,
      body_size: body ? body.length : 0
    };
  }
  
  static validateJSON(json_string) {
    try {
      const obj = JSON.parse(json_string);
      return {valid: true, formatted: JSON.stringify(obj, null, 2)};
    } catch (e) {
      return {valid: false, error: e.message};
    }
  }
  
  static analyzeResponse(status, headers, body) {
    const analysis = {
      status: status,
      is_error: status >= 400,
      content_type: headers['content-type'] || 'unknown',
      size_bytes: body.length,
      time_estimate: 'fast'
    };
    
    if (status === 200) analysis.status_text = '✅ OK';
    if (status === 404) analysis.status_text = '❌ Not Found';
    if (status === 500) analysis.status_text = '❌ Server Error';
    
    return analysis;
  }
}

module.exports = APIDebugger;
    """
}

# ============================================================================
# PLUGIN 4: Code Complexity Calculator
# ============================================================================

CODE_COMPLEXITY = {
    "name": "Code Complexity Calculator",
    "author_id": "rijwal_team",
    "description": "Calculate cyclomatic complexity, LOC, and suggest refactoring",
    "category": "Code Analysis",
    "tags": ["complexity", "refactoring", "metrics", "analysis"],
    "code": """
// Code Complexity Calculator
class ComplexityCalculator {
  static calculateCyclomaticComplexity(code) {
    let complexity = 1;
    const conditions = (code.match(/if|else|case|for|while|catch/g) || []).length;
    complexity += conditions;
    return complexity;
  }
  
  static countLines(code) {
    return code.split('\\n').filter(line => line.trim().length > 0).length;
  }
  
  static findLongFunctions(code) {
    const functions = code.match(/def\\s+\\w+|function\\s+\\w+/g) || [];
    const lines = code.split('\\n');
    
    return {
      function_count: functions.length,
      avg_lines_per_function: Math.round(lines.length / functions.length),
      recommendation: functions.length > 10 ? 'Consider breaking into smaller modules' : 'Good structure'
    };
  }
  
  static getComplexityScore(code) {
    const cc = this.calculateCyclomaticComplexity(code);
    const loc = this.countLines(code);
    
    let score = 10;
    if (cc > 10) score -= 3;
    if (cc > 20) score -= 2;
    if (loc > 100) score -= 1;
    
    return Math.max(1, score);
  }
}

module.exports = ComplexityCalculator;
    """
}

# ============================================================================
# PLUGIN 5: Regex Pattern Tester
# ============================================================================

REGEX_TESTER = {
    "name": "Regex Pattern Tester",
    "author_id": "rijwal_team",
    "description": "Test regex patterns, explain patterns, suggest improvements",
    "category": "Development Tools",
    "tags": ["regex", "pattern", "testing", "strings"],
    "code": """
// Regex Pattern Tester
class RegexTester {
  static testPattern(pattern, text) {
    try {
      const regex = new RegExp(pattern);
      const matches = text.match(regex);
      return {
        valid: true,
        matches: matches ? matches.length : 0,
        result: matches
      };
    } catch (e) {
      return {valid: false, error: e.message};
    }
  }
  
  static explainPattern(pattern) {
    const explanations = {
      '^': 'Start of line',
      '$': 'End of line',
      '.': 'Any character',
      '*': 'Zero or more',
      '+': '+ One or more',
      '?': 'Zero or one',
      '[]': 'Character class',
      '()': 'Group',
      '|': 'Alternation',
      '\\\\': 'Escape character'
    };
    
    let explanation = 'Pattern: ' + pattern + '\\n\\n';
    for (const [key, value] of Object.entries(explanations)) {
      if (pattern.includes(key)) {
        explanation += `${key}: ${value}\\n`;
      }
    }
    return explanation;
  }
  
  static commonPatterns() {
    return {
      email: '/^[^@]+@[^@]+\\.[^@]+$/',
      phone: '/^\\d{10}$/',
      url: '/^https?:\\/\\/.+/',
      zip: '/^\\d{5}(-\\d{4})?$/',
      date: '/^\\d{4}-\\d{2}-\\d{2}$/'
    };
  }
}

module.exports = RegexTester;
    """
}

# ============================================================================
# PLUGIN 6: Database Query Optimizer
# ============================================================================

DB_OPTIMIZER = {
    "name": "Database Query Optimizer",
    "author_id": "rijwal_team",
    "description": "Analyze SQL queries, suggest indexes, identify slow queries",
    "category": "Database",
    "tags": ["sql", "database", "optimization", "performance"],
    "code": """
// Database Query Optimizer
class QueryOptimizer {
  static analyzeSQLQuery(query) {
    const issues = [];
    
    if (query.includes('SELECT *')) {
      issues.push('⚠️ SELECT * found. Specify only needed columns');
    }
    
    if (query.includes('OR') && query.includes('AND')) {
      issues.push('💡 Consider using IN clause for multiple OR conditions');
    }
    
    if (query.toUpperCase().includes('JOIN') && !query.toUpperCase().includes('INDEX')) {
      issues.push('💡 Consider adding indexes on JOIN columns');
    }
    
    if (query.includes('LIKE') && query.includes('%')) {
      issues.push('⚠️ LIKE with % is slow. Consider full-text search');
    }
    
    return {issues: issues, optimized: false};
  }
  
  static suggestIndexes(table, columns) {
    return {
      primary_key: `CREATE INDEX idx_${table}_id ON ${table}(id)`,
      composite: `CREATE INDEX idx_${table}_composite ON ${table}(${columns.join(', ')})`
    };
  }
  
  static estimateQueryTime(complexity) {
    if (complexity < 5) return 'Very Fast (< 10ms)';
    if (complexity < 10) return 'Fast (10-100ms)';
    if (complexity < 20) return 'Moderate (100ms-1s)';
    return 'Slow (> 1s)';
  }
}

module.exports = QueryOptimizer;
    """
}

# ============================================================================
# PLUGIN 7: Code Documentation Generator
# ============================================================================

DOC_GENERATOR = {
    "name": "Code Documentation Generator",
    "author_id": "rijwal_team",
    "description": "Auto-generate docstrings, API documentation, README templates",
    "category": "Documentation",
    "tags": ["documentation", "docstring", "api", "readme"],
    "code": """
// Documentation Generator
class DocGenerator {
  static generateDocstring(functionName, params) {
    return `
/**
 * ${functionName}
 * 
 * @param {*} ${params.join(' - parameter\\n * @param {*} ')} - parameter
 * @returns {*} result
 * 
 * @example
 * const result = ${functionName}(arg);
 */
    `.trim();
  }
  
  static generateAPIDoc(endpoints) {
    let doc = '# API Documentation\\n\\n';
    endpoints.forEach(ep => {
      doc += `## ${ep.method} ${ep.path}\\n`;
      doc += `${ep.description}\\n\\n`;
    });
    return doc;
  }
  
  static generateREADME(projectName, description) {
    return `
# ${projectName}

${description}

## Installation
\`\`\`bash
pip install ${projectName}
\`\`\`

## Usage
\`\`\`python
from ${projectName} import something
\`\`\`

## Features
- Feature 1
- Feature 2
- Feature 3

## License
MIT
    `.trim();
  }
}

module.exports = DocGenerator;
    """
}

# ============================================================================
# PLUGIN 8: Security Vulnerability Scanner
# ============================================================================

SECURITY_SCANNER = {
    "name": "Security Vulnerability Scanner",
    "author_id": "rijwal_team",
    "description": "Scan code for common security vulnerabilities and best practices",
    "category": "Security",
    "tags": ["security", "vulnerability", "best-practices", "scanning"],
    "code": """
// Security Vulnerability Scanner
class SecurityScanner {
  static scanCode(code) {
    const vulnerabilities = [];
    
    if (code.includes('eval(') || code.includes('exec(')) {
      vulnerabilities.push({severity: 'critical', msg: 'eval() detected - security risk'});
    }
    
    if (code.includes('password') && code.includes('=')) {
      vulnerabilities.push({severity: 'critical', msg: 'Hardcoded password detected'});
    }
    
    if (code.includes('http://') && !code.includes('https://')) {
      vulnerabilities.push({severity: 'high', msg: 'Unencrypted HTTP detected'});
    }
    
    if (code.includes('pickle.load') || code.includes('yaml.load')) {
      vulnerabilities.push({severity: 'high', msg: 'Unsafe deserialization detected'});
    }
    
    if (code.includes('import os') && code.includes('os.system')) {
      vulnerabilities.push({severity: 'high', msg: 'Shell command execution detected'});
    }
    
    if (!code.includes('try') || !code.includes('except')) {
      vulnerabilities.push({severity: 'medium', msg: 'No error handling detected'});
    }
    
    return {
      vulnerabilities: vulnerabilities,
      security_score: Math.max(0, 100 - vulnerabilities.length * 15)
    };
  }
}

module.exports = SecurityScanner;
    """
}

# ============================================================================
# PLUGIN 9: TypeScript Type Checker
# ============================================================================

TS_CHECKER = {
    "name": "TypeScript Type Checker",
    "author_id": "rijwal_team",
    "description": "Analyze TypeScript types, suggest type annotations, check compatibility",
    "category": "Development Tools",
    "tags": ["typescript", "types", "type-checking"],
    "code": """
// TypeScript Type Checker
class TypeScriptChecker {
  static inferTypes(code) {
    const types = {};
    
    const varMatches = code.matchAll(/const (\\w+)\\s*=/g);
    for (const match of varMatches) {
      const varName = match[1];
      const value = code.substring(match.index + match[0].length, code.indexOf(';', match.index));
      
      if (value.includes('[')) types[varName] = 'Array';
      else if (value.includes('{')) types[varName] = 'Object';
      else if (value.includes('"')) types[varName] = 'string';
      else if (!isNaN(value)) types[varName] = 'number';
    }
    
    return types;
  }
  
  static suggestTypeAnnotations(code) {
    const suggestions = [];
    if (!code.includes(': ')) {
      suggestions.push('💡 Add type annotations to function parameters');
    }
    if (!code.includes('interface ') && code.includes('{')) {
      suggestions.push('💡 Consider defining interfaces for objects');
    }
    return suggestions;
  }
}

module.exports = TypeScriptChecker;
    """
}

# ============================================================================
# PLUGIN 10: Git Helper
# ============================================================================

GIT_HELPER = {
    "name": "Git Helper",
    "author_id": "rijwal_team",
    "description": "Git commands, commit messages, branch management, merge helpers",
    "category": "Development Tools",
    "tags": ["git", "version-control", "commands", "workflow"],
    "code": """
// Git Helper
class GitHelper {
  static suggestCommitMessage(changes) {
    if (changes.includes('fix')) return 'fix: resolve issue';
    if (changes.includes('feature')) return 'feat: add new feature';
    if (changes.includes('doc')) return 'docs: update documentation';
    if (changes.includes('refactor')) return 'refactor: improve code structure';
    return 'chore: update files';
  }
  
  static getCommonCommands() {
    return {
      'stage_all': 'git add .',
      'commit': 'git commit -m "message"',
      'push': 'git push origin branch_name',
      'pull': 'git pull origin main',
      'create_branch': 'git checkout -b feature/branch_name',
      'merge': 'git merge feature/branch_name',
      'log': 'git log --oneline --graph',
      'diff': 'git diff'
    };
  }
  
  static generateBranchName(feature) {
    return 'feature/' + feature.toLowerCase().replace(/ /g, '-');
  }
}

module.exports = GitHelper;
    """
}

# ============================================================================
# EXPORT ALL PLUGINS
# ============================================================================

EXAMPLE_PLUGINS = [
    DJANGO_ORM_HELPER,
    PYTHON_PERFORMANCE,
    API_DEBUGGER,
    CODE_COMPLEXITY,
    REGEX_TESTER,
    DB_OPTIMIZER,
    DOC_GENERATOR,
    SECURITY_SCANNER,
    TS_CHECKER,
    GIT_HELPER
]

if __name__ == "__main__":
    print("📦 Example Plugins for Rijwal Marketplace")
    print("=" * 50)
    for i, plugin in enumerate(EXAMPLE_PLUGINS, 1):
        print(f"{i}. {plugin['name']}")
        print(f"   Category: {plugin['category']}")
        print(f"   Tags: {', '.join(plugin['tags'])}")
        print()
    
    print(f"✅ {len(EXAMPLE_PLUGINS)} example plugins ready to upload!")

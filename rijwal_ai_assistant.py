#!/usr/bin/env python3
"""
RIJWAL_LANG v0.18 - AI CODE ASSISTANT
======================================

Integrates with Claude/OpenAI for:
- Code suggestions
- Error explanations
- Code refactoring
- Example generation
- Documentation help
- Learning assistance
"""

import os
import json
from typing import Optional, List, Dict, Any
from datetime import datetime


class AIAssistant:
    """AI-powered code assistant for the Rijwal IDE"""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "claude"):
        """
        Initialize AI assistant with API credentials
        
        Args:
            api_key: API key for Claude or OpenAI
            provider: "claude" or "openai"
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.provider = provider
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 20
        
    def _prepare_system_prompt(self) -> str:
        """System prompt for the AI"""
        return """You are a helpful code assistant for Rijwal_Lang, a programming language IDE.

You help developers with:
1. **Code Suggestions** - Improve their code
2. **Error Explanations** - Explain what went wrong
3. **Refactoring** - Make code cleaner
4. **Examples** - Show working examples
5. **Documentation** - Explain how things work
6. **Learning** - Teach programming concepts

Keep responses concise, practical, and include code examples when relevant.
Rijwal_Lang supports: Python, JavaScript, Go, Rust, C++, Bash, SQL.
Built-in functions: 150+. Plugins available: 9 (NumPy, Pandas, Requests, PIL, Math, String, Array, Data, Time)."""

    def _format_message(self, role: str, content: str) -> Dict[str, str]:
        """Format message for conversation"""
        return {"role": role, "content": content}
    
    def chat(self, user_message: str, code_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Send message to AI with optional code context
        
        Args:
            user_message: User's question/request
            code_context: Optional code snippet for context
            
        Returns:
            Dict with response, usage, timestamp
        """
        # Add code context if provided
        if code_context:
            formatted_message = f"CODE CONTEXT:\n```\n{code_context}\n```\n\nQUESTION: {user_message}"
        else:
            formatted_message = user_message
        
        # Add to history
        self.conversation_history.append(
            self._format_message("user", formatted_message)
        )
        
        # Trim history if too long
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
        
        # Get response
        response = self._call_api(formatted_message)
        
        # Add to history
        self.conversation_history.append(
            self._format_message("assistant", response["content"])
        )
        
        return {
            "response": response["content"],
            "provider": self.provider,
            "timestamp": datetime.now().isoformat(),
            "usage": response.get("usage", {}),
            "model": response.get("model", "unknown")
        }
    


    def evolve_language(self, goals: str, code_context: Optional[str] = None) -> Dict[str, Any]:
        """Generate a practical evolution plan for Rijwal language + IDE."""
        prompt = (
            "Create a concise self-evolution plan for Rijwal_Lang. "
            "Return: (1) top 5 next features, (2) top 5 hardening tasks, "
            "(3) a 7-day execution plan, (4) one sample Rijwal code snippet.\n\n"
            f"GOALS: {goals}\n\n"
            f"CODE CONTEXT:\n{code_context or ''}"
        )
        result = self.chat(prompt, code_context=code_context)
        return {
            "plan": result.get("response", ""),
            "provider": result.get("provider", self.provider),
            "model": result.get("model", "unknown"),
            "timestamp": result.get("timestamp"),
        }

    def _call_api(self, message: str) -> Dict[str, Any]:
        """
        Call the actual API (Claude or OpenAI)
        Falls back to mock if no API key
        """
        if not self.api_key:
            return self._mock_response(message)
        
        if self.provider == "claude":
            return self._call_claude(message)
        elif self.provider == "openai":
            return self._call_openai(message)
        else:
            return self._mock_response(message)
    
    def _call_claude(self, message: str) -> Dict[str, Any]:
        """Call Claude API"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=self._prepare_system_prompt(),
                messages=[{"role": "user", "content": message}]
            )
            
            return {
                "content": response.content[0].text,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "model": "claude-3-5-sonnet"
            }
        except Exception as e:
            return self._mock_response(f"(Claude API error: {str(e)}) Using mock response...")
    
    def _call_openai(self, message: str) -> Dict[str, Any]:
        """Call OpenAI API"""
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._prepare_system_prompt()},
                    {"role": "user", "content": message}
                ],
                max_tokens=1024
            )
            
            return {
                "content": response.choices[0].message.content,
                "usage": {
                    "input_tokens": response.usage.prompt_tokens,
                    "output_tokens": response.usage.completion_tokens
                },
                "model": "gpt-4"
            }
        except Exception as e:
            return self._mock_response(f"(OpenAI API error: {str(e)}) Using mock response...")
    
    def _mock_response(self, user_message: str) -> Dict[str, Any]:
        """
        Fallback mock responses when API not available
        Still helpful for development/demo
        """
        mock_responses = {
            "error": """🔧 **Error Explanation**

It looks like your code has an issue. Here are common causes:

1. **Syntax Error** - Check brackets, quotes, colons
2. **Variable Not Defined** - Make sure variables are declared before use
3. **Type Mismatch** - Ensure types match (number vs string)
4. **Plugin Missing** - Load required plugins first with `use plugin_name`

Try printing variable values to debug! 🐛""",
            
            "refactor": """✨ **Refactoring Suggestions**

Your code can be improved by:

1. **Extract Functions** - Break into smaller pieces
2. **Use Built-ins** - We have 150+ functions available
3. **Better Names** - Use descriptive variable names
4. **Remove Duplication** - DRY principle

Example: Instead of repeating code, create a function! 📝""",
            
            "suggest": """💡 **Code Suggestion**

Based on your code, you might want to:

1. Use **List manipulation** functions for arrays
2. Try **NumPy plugin** for numerical operations
3. Consider **Pandas plugin** for data processing
4. Use **String plugin** functions for text

Check examples/ folder for working code! 🎯""",
            
            "example": """📚 **Example Code**

Here's a practical example:

```rijwal
# Processing data
data = [1, 2, 3, 4, 5]
result = []

for item in data:
    if item > 2:
        result.append(item * 2)

print(result)  # [6, 8, 10]
```

You can also use plugins like NumPy for advanced operations! 🚀""",
            
            "learn": """📖 **Learning Tip**

Key concepts:

1. **Variables** - Store data with `x = value`
2. **Functions** - Reusable code with `func = (params) -> { }`
3. **Loops** - Repeat code with `for` or `while`
4. **Plugins** - Extend features with `use plugin_name`
5. **Games** - 10 games available for breaks!

Start with examples/ and build from there! 🎮"""
,
            "evolution": """🧬 **Rijwal Self-Evolution Plan**

1) Language core
- Add structured control flow (`If/Else`, loops) with beginner-friendly errors
- Add module packaging and test blocks

2) IDE + terminal quality
- Keep terminal and runner output deterministic
- Add starter templates and guided lessons

3) AI Buddy growth
- Add one-click actions: Explain, Fix, Generate, Next Step
- Add history-based contextual coaching

4) 7-day solo plan
- Day 1-2: tests and stability
- Day 3-4: language ergonomics
- Day 5: docs + examples
- Day 6: AI actions and prompts
- Day 7: release and user feedback

5) Starter snippet
```rijwal
When Program Starts:
    Print "Idea → Plan → Code → Run"
```
"""
        }
        
        # Smart response selection
        lower_msg = user_message.lower()
        
        if any(word in lower_msg for word in ["error", "bug", "wrong", "fail", "crash"]):
            base_response = mock_responses["error"]
        elif any(word in lower_msg for word in ["improve", "refactor", "better", "clean"]):
            base_response = mock_responses["refactor"]
        elif any(word in lower_msg for word in ["example", "sample", "code", "how"]):
            base_response = mock_responses["example"]
        elif any(word in lower_msg for word in ["evolution", "self-evolving", "roadmap", "next generation"]):
            base_response = mock_responses["evolution"]
        elif any(word in lower_msg for word in ["learn", "teach", "explain", "what"]):
            base_response = mock_responses["learn"]
        else:
            base_response = mock_responses["suggest"]
        
        return {
            "content": base_response,
            "usage": {"input_tokens": 0, "output_tokens": 0},
            "model": "mock-assistant",
            "note": "⚠️ Mock response (no API key). Set ANTHROPIC_API_KEY or OPENAI_API_KEY for real AI!"
        }
    
    def suggest_fixes(self, error_message: str, code: Optional[str] = None) -> Dict[str, Any]:
        """Get AI suggestions for fixing an error"""
        context = f"ERROR: {error_message}"
        if code:
            context += f"\n\nCODE:\n```\n{code}\n```"
        
        return self.chat(f"Help me fix this error:\n{context}")
    
    def generate_docs(self, code: str) -> Dict[str, Any]:
        """Generate documentation for code"""
        return self.chat(f"Generate documentation/docstring for this code:\n```\n{code}\n```")
    
    def refactor_code(self, code: str) -> Dict[str, Any]:
        """Get refactoring suggestions"""
        return self.chat(f"Suggest improvements for this code:\n```\n{code}\n```")
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def explain_concept(self, concept: str) -> Dict[str, Any]:
        """Explain a programming concept"""
        return self.chat(f"Explain this concept in simple terms: {concept}")


class AIAssistantManager:
    """Manages AI assistant instance for the IDE"""
    
    _instance: Optional[AIAssistant] = None
    
    @classmethod
    def get_instance(cls, api_key: Optional[str] = None, provider: str = "claude") -> AIAssistant:
        """Get or create singleton AI assistant"""
        if cls._instance is None:
            cls._instance = AIAssistant(api_key=api_key, provider=provider)
        return cls._instance
    
    @classmethod
    def set_api_key(cls, api_key: str, provider: str = "claude") -> None:
        """Update API key"""
        cls._instance = AIAssistant(api_key=api_key, provider=provider)


# Default instance
ai_assistant = AIAssistant()


if __name__ == "__main__":
    # Demo usage
    print("=" * 70)
    print("🤖 RIJWAL AI ASSISTANT - DEMO")
    print("=" * 70)
    print()
    
    # Create assistant
    assistant = AIAssistant()
    
    # Test queries
    queries = [
        "I'm getting a syntax error, can you help?",
        "How do I use the NumPy plugin?",
        "Can you show me an example with loops?",
        "Explain what a function is"
    ]
    
    for query in queries:
        print(f"👤 User: {query}")
        response = assistant.chat(query)
        print(f"🤖 Assistant: {response['response']}")
        print()
    
    print("✅ Demo complete!")

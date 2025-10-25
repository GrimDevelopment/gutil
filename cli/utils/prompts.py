from typing import Dict, Any

def get_codex_prompt(prompt_type: str) -> str:
    prompts: Dict[str, str] = {
        "generate_code": "Generate code for the following requirements: {requirements}",
        "explain_code": "Explain the following code: {code}",
        "debug_code": "Identify issues in the following code: {code}",
        "refactor_code": "Refactor the following code for better performance: {code}",
    }
    
    return prompts.get(prompt_type, "Prompt type not found.") 

def format_prompt(prompt: str, **kwargs: Any) -> str:
    return prompt.format(**kwargs)
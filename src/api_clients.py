import requests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import config

def call_openrouter(model, system_prompt, user_prompt):
    """Call OpenRouter API."""
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/username/repo",
        "X-Title": "AI Safety Test"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error OpenRouter: {e}")
        return None

def call_gemini(system_prompt, user_prompt):
    """Call Gemini API (if key exists)."""
    if not config.GEMINI_API_KEY:
        return None

    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        model = "gemini-3.1-pro-preview"
        
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=user_prompt),
                ],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            thinking_config=types.ThinkingConfig(
                thinking_level="HIGH",
            )
        )
        
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=generate_content_config,
                )
                
                # Convert response to match the OpenRouter format for compatibility
                return {
                    "choices": [{
                        "message": {
                            "role": "assistant",
                            "content": response.text
                        }
                    }],
                    "model": model,
                    "usage": {
                        "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                        "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                        "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
                    }
                }
            except Exception as api_e:
                if "429" in str(api_e) and attempt < max_retries - 1:
                    print(f"Rate limited by Gemini. Waiting 30 seconds before retry {attempt + 1}/{max_retries}...")
                    time.sleep(30)
                else:
                    raise api_e

    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return None

def call_mistral(system_prompt, user_prompt):
    """Call Mistral API (if key exists)."""
    if not config.MISTRAL_API_KEY:
        return None

    headers = {
        "Authorization": f"Bearer {config.MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-small-latest", # or whatever model
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error Mistral: {e}")
        return None

def call_opencode(system_prompt, user_prompt):
    """Call OpenCode (Zen Minmax) API (if key exists)."""
    if not config.OPENCODE_API_KEY:
        return None

    print("OpenCode not implemented yet.")
    return None

def route_request(model, system_prompt, user_prompt):
    """Route request to appropriate client."""
    # Check specific keys first
    if "gemini" in model.lower() and config.GEMINI_API_KEY:
        return call_gemini(system_prompt, user_prompt)
    if "mistral" in model.lower() and config.MISTRAL_API_KEY:
        return call_mistral(system_prompt, user_prompt)
    if "opencode" in model.lower() and config.OPENCODE_API_KEY:
        return call_opencode(system_prompt, user_prompt)
    
    # Fallback to OpenRouter (handles :free models or direct routing if key is set)
    return call_openrouter(model, system_prompt, user_prompt)

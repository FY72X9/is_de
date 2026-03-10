import json
import time
import requests
import sys
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent))
import config
from api_clients import route_request

# Setup Logging
log_file = config.PROJECT_ROOT / "logs" / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
config.LOGS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def load_prompts():
    """Load prompt battery from JSON file."""
    with open(config.PROMPTS_DIR / "battery_v1.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_existing_results():
    """Load existing results to resume."""
    files = list(config.RAW_DATA_DIR.glob("api_responses_*.json"))
    all_results = []
    seen = set()
    
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as file:
                data = json.load(file)
                for r in data:
                    key = f"{r.get('prompt_id')}|{r.get('model')}|{r.get('condition')}"
                    if key not in seen:
                        seen.add(key)
                        all_results.append(r)
        except Exception as e:
            logger.error(f"Error reading {f}: {e}")
            
    logger.info(f"Loaded {len(all_results)} unique existing results from {len(files)} files.")
    return all_results

def call_openrouter(model, system_prompt, user_prompt):
    """Call OpenRouter API."""
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Only add Referer if it is not empty
    if config.OPENROUTER_REFERRER:
        headers["HTTP-Referer"] = config.OPENROUTER_REFERRER

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
        logger.error(f"Error calling API: {e}")
        return None

def save_results(results, output_file):
    """Save results to a file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(results)} records to {output_file}")

def main():
    logger.info("Starting API Safety Test...")
    
    # Debug Keys
    print(f"Config loaded.")
    print(f"OpenRouter Key present: {bool(config.OPENROUTER_API_KEY)}")
    print(f"Gemini Key present: {bool(config.GEMINI_API_KEY)}")
    print(f"Mistral Key present: {bool(config.MISTRAL_API_KEY)}")
    
    logger.info(f"API Key loaded: {config.OPENROUTER_API_KEY[:10]}..." if config.OPENROUTER_API_KEY else "WARNING: NO API KEY LOADED")
    print(f"API Key loaded: {config.OPENROUTER_API_KEY[:10]}..." if config.OPENROUTER_API_KEY else "WARNING: NO API KEY LOADED")

    prompts = load_prompts()
    results = load_existing_results()
    
    output_file = config.RAW_DATA_DIR / f"api_responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Create a set of completed combinations to avoid duplicates
    # Format: "prompt_id|model|condition"
    completed = set()
    for r in results:
        key = f"{r['prompt_id']}|{r['model']}|{r['condition']}"
        completed.add(key)

    logger.info(f"Loaded {len(results)} existing results. {len(completed)} unique combinations already done.")

    # Iterate over all prompts
    for prompt in prompts:
        # Iterate over all models
        for model in config.MODELS:
            # Iterate over all conditions
            for condition_key, system_prompt in config.CONDITIONS.items():
                
                # Check if already done
                key = f"{prompt['id']}|{model}|{condition_key}"
                if key in completed:
                    logger.info(f"Skipping {key} (already done)")
                    continue

                logger.info(f"Testing {prompt['id']} with {model} ({condition_key})...")
                print(f"Testing {prompt['id']} with {model} ({condition_key})...")

                # Call API
                # response_data = call_openrouter(model, system_prompt, prompt['prompt_text'])
                response_data = route_request(model, system_prompt, prompt['prompt_text'])

                # Save raw result
                if response_data:
                    result_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "prompt_id": prompt['id'],
                        "intent_category": prompt['intent_category'],
                        "language": prompt['language'],
                        "model": model,
                        "condition": condition_key,
                        "response": response_data
                    }
                    results.append(result_entry)
                    completed.add(key)

                    # Auto-save frequently
                    if len(results) % 5 == 0:
                        save_results(results, output_file)

                # Rate limiting
                time.sleep(20)

    # Final save
    save_results(results, output_file)
    logger.info("Data collection complete.")

if __name__ == "__main__":
    if not config.OPENROUTER_API_KEY:
        print("WARNING: OPENROUTER_API_KEY is not set.")
    main()

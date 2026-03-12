import os
import re
from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import config

def analyze_corpus():
    """Analyze the regulatory corpus for gaps."""
    docs_dir = config.DOCS_DIR / "regulatory_corpus"
    logs_dir = config.PROJECT_ROOT / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    log_path = logs_dir / "regulatory_report.txt"
    
    with open(log_path, "w", encoding="utf-8") as log_file:
        def log_print(*args, **kwargs):
            print(*args, **kwargs)
            print(*args, file=log_file, **kwargs)

        results = []

        # Keywords to search
        keywords = {
            "API": ["API", "Application Programming Interface", "endpoint"],
            "Developer": ["developer", "pengembang", "pengembang AI"],
            "Safety": ["keamanan", "safety", "aman", "bahaya"],
            "Deployment": ["deployment", "penempatan", "implementasi"]
        }

        log_print("=== Regulatory Gap Analysis ===\n")

        for file in docs_dir.glob("*.txt"):
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()
                word_count = len(text.split())

            # Check for keyword presence
            coverage = {}
            for category, terms in keywords.items():
                count = sum(1 for term in terms if term.lower() in text.lower())
                coverage[category] = count

            # Calculate density (mentions per 1000 words)
            density = {k: (v / word_count) * 1000 for k, v in coverage.items()}

            log_print(f"Document: {file.name}")
            log_print(f"Word Count: {word_count}")
            log_print(f"Keyword Density (per 1000 words):")
            for k, v in density.items():
                log_print(f"  - {k}: {v:.2f}")

            # Determine if "API" is covered
            has_api = "API" in text or "Application Programming Interface" in text

            results.append({
                "document": file.name,
                "word_count": word_count,
                "has_api_mention": has_api,
                "api_density": density.get("API", 0),
                "developer_density": density.get("Developer", 0)
            })
            log_print()

        # Gap Conclusion
        log_print("=== Gap Assessment ===")
        api_coverage = [r['has_api_mention'] for r in results]
        if not any(api_coverage):
            log_print("CRITICAL FINDING: No Indonesian regulatory documents explicitly mention 'API' or 'Application Programming Interface' in the context of AI safety.")
        else:
            log_print("API mentioned in some documents, but densities remain critically low.")

if __name__ == "__main__":
    analyze_corpus()

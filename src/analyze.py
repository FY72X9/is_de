import json
import pandas as pd
from scipy import stats
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import config

def load_data():
    """Load the evaluated JSON data."""
    with open(config.PROCESSED_DATA_DIR / "evaluated_responses.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def analyze_safety_degradation(df):
    """Analyze safety scores by condition and language."""
    print("=== Safety Degradation Analysis ===\n")

    # Group by Condition
    condition_means = df.groupby('condition')['safety_score'].mean()
    print("Mean Safety Score by Condition:")
    print(condition_means)
    print()

    # Group by Language
    language_means = df.groupby('language')['safety_score'].mean()
    print("Mean Safety Score by Language:")
    print(language_means)
    print()

    # Hypothesis Testing
    # H1: C1 vs C2
    c1_scores = df[df['condition'] == 'C1_BASELINE']['safety_score']
    c2_scores = df[df['condition'] == 'C2_NEUTRAL']['safety_score']
    c3_scores = df[df['condition'] == 'C3_STRIPPED']['safety_score']

    # T-test C1 vs C2
    t_stat, p_val = stats.ttest_ind(c1_scores, c2_scores)
    print(f"H1 (Baseline vs Neutral): t={t_stat:.3f}, p={p_val:.5f}")

    # ANOVA (C1, C2, C3)
    f_stat, p_val_anova = stats.f_oneway(c1_scores, c2_scores, c3_scores)
    print(f"H3 (Configuration Collapse): F={f_stat:.3f}, p={p_val_anova:.5f}")

    print("\nAnalysis complete.")

def main():
    df = load_data()
    analyze_safety_degradation(df)

if __name__ == "__main__":
    main()

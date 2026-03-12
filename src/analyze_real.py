import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
import textwrap
import os

def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_xticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width, break_long_words=break_long_words))
    ax.set_xticklabels(labels, rotation=0)

def analyze_and_plot():
    processed_dir = Path("data/processed")
    data_path = processed_dir / "evaluated_responses.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    # Create required directories
    diagrams_dir = Path("diagrams")
    diagrams_dir.mkdir(parents=True, exist_ok=True)
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    log_path = logs_dir / "analysis_report.txt"
    
    with open(log_path, "w", encoding="utf-8") as log_file:
        def log_print(*args, **kwargs):
            print(*args, **kwargs)
            print(*args, file=log_file, **kwargs)
            
        log_print("=== Safety Degradation Empirical Analysis Report ===\n")
        
        # Output descriptive statistics
        log_print("--- Descriptive Statistics: By Condition ---")
        cond_stats = df.groupby('condition')['safety_score'].describe()
        log_print(cond_stats.to_string())
        log_print("\n")
        
        log_print("--- Descriptive Statistics: By Language & Condition ---")
        lang_cond_stats = df.groupby(['language', 'condition'])['safety_score'].mean()
        log_print(lang_cond_stats.to_string())
        log_print("\n")
        
        log_print("--- Hypothesis Testing ---")
        
        # H1: Safety Degradation from Baseline to Neutral
        c1 = df[df['condition'] == 'C1_BASELINE']['safety_score']
        c2 = df[df['condition'] == 'C2_NEUTRAL']['safety_score']
        t_stat, p_val = stats.ttest_ind(c1, c2)
        log_print(f"H1 (C1_BASELINE vs C2_NEUTRAL): t={t_stat:.3f}, p={p_val:.5e}")
        if p_val < 0.05:
            log_print("Result: Significant safety degradation observed when removing safety guidelines.")
        
        # H2: Disproportionate degradation in Indonesian vs English
        en_c1 = df[(df['condition'] == 'C1_BASELINE') & (df['language'] == 'English')]['safety_score']
        en_c2 = df[(df['condition'] == 'C2_NEUTRAL') & (df['language'] == 'English')]['safety_score']
        id_c1 = df[(df['condition'] == 'C1_BASELINE') & (df['language'] == 'Bahasa Indonesia')]['safety_score']
        id_c2 = df[(df['condition'] == 'C2_NEUTRAL') & (df['language'] == 'Bahasa Indonesia')]['safety_score']
        
        en_diff = en_c1.mean() - en_c2.mean()
        id_diff = id_c1.mean() - id_c2.mean()
        
        log_print(f"\nEnglish Degradation (C1-C2): {en_diff:.3f}")
        log_print(f"Indonesian Degradation (C1-C2): {id_diff:.3f}")
        log_print(f"Baseline Difference (English vs Indonesian): {(en_c1.mean() - id_c1.mean()):.3f}")

    # Common plot settings for better aesthetics
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    palette = sns.color_palette("deep")

    # 1. Bar chart of Safety Score by Condition
    plt.figure(figsize=(10, 6))
    order_cond = df.groupby('condition')['safety_score'].mean().sort_values(ascending=False).index
    ax = sns.barplot(x="condition", y="safety_score", data=df, order=order_cond, errorbar='ci', capsize=.1, palette=palette)
    plt.title("Mean Safety Score by System Prompt Condition", fontweight='bold', fontsize=16, pad=15)
    plt.ylabel("Safety Score (Higher is Safer)", fontsize=14)
    plt.xlabel("System Prompt Condition", fontsize=14)
    plt.ylim(0, 3.2)
    plt.tight_layout()
    plt.savefig(diagrams_dir / "safety_by_condition.png", dpi=300)
    plt.close()
    
    # 2. Bar chart of Safety Score by Language and Condition
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x="condition", y="safety_score", hue="language", data=df, order=order_cond, errorbar='ci', capsize=.1, palette="Set2")
    plt.title("Safety Degradation: English vs Bahasa Indonesia", fontweight='bold', fontsize=16, pad=15)
    plt.ylabel("Safety Score", fontsize=14)
    plt.xlabel("Condition", fontsize=14)
    plt.legend(title="Language", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.ylim(0, 3.2)
    plt.tight_layout()
    plt.savefig(diagrams_dir / "safety_by_language_condition.png", dpi=300)
    plt.close()
    
    # 3. Bar chart of Safety Score by Intent Category
    plt.figure(figsize=(14, 7))
    order_intent = df.groupby('intent_category')['safety_score'].mean().sort_values(ascending=False).index
    ax = sns.barplot(x="intent_category", y="safety_score", data=df, order=order_intent, errorbar='ci', palette="husl")
    plt.title("Safety Score by Malicious Intent Category", fontweight='bold', fontsize=16, pad=15)
    plt.ylabel("Mean Safety Score", fontsize=14)
    plt.xlabel("Intent Category", fontsize=14)
    wrap_labels(ax, 15)
    plt.ylim(0, 3.2)
    plt.tight_layout()
    plt.savefig(diagrams_dir / "safety_by_intent.png", dpi=300)
    plt.close()
    
    # 4. Bar chart of Safety Score by Model
    plt.figure(figsize=(14, 7))
    order_model = df.groupby('model')['safety_score'].mean().sort_values(ascending=False).index
    ax = sns.barplot(x="model", y="safety_score", data=df, order=order_model, errorbar='ci', palette="viridis")
    plt.title("Safety Score by Model Architecture", fontweight='bold', fontsize=16, pad=15)
    plt.ylabel("Mean Safety Score", fontsize=14)
    plt.xlabel("Model", fontsize=14)
    wrap_labels(ax, 20)
    plt.ylim(0, 3.2)
    plt.tight_layout()
    plt.savefig(diagrams_dir / "safety_by_model.png", dpi=300)
    plt.close()
    
    print(f"\nAnalysis complete. Visualizations saved to '{diagrams_dir}/' and verbose log saved to '{log_path}'.")

if __name__ == '__main__':
    analyze_and_plot()

"""
generate_charts.py
==================
Generates all comparative visualisation figures for the QWEN vs SeaLLM evaluator analysis.

Data source: Extracted from analysis logs (res_1_qwen2.5_3B_instruct & res_2_SEALM).
SeaLLM ordinal score distribution is estimated from aggregate statistics (mean=2.395, N=902,
refusal rates by language and condition), as exact per-score counts were not logged.

Output: PNG files in  ../diagrams/charts/
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec

# ── Output directory ─────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "..", "diagrams", "charts")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Colour palette ────────────────────────────────────────────────────────────
C_QWEN = "#1D4ED8"   # blue  – Qwen model
C_SEAL = "#B91C1C"   # red   – SeaLLM model
C_EN   = "#D97706"   # amber – English language
C_ID   = "#15803D"   # green – Bahasa Indonesia
C_CN   = "#7C3AED"   # purple – CN origin
C_EU   = "#0891B2"   # cyan  – EU origin
C_US   = "#9A3412"   # rust  – US origin

# ── Global style ──────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "font.size":         10,
    "axes.linewidth":    1.2,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.dpi":        150,
    "savefig.dpi":       150,
    "axes.grid":         False,
})


# ─────────────────────────────────────────────────────────────────────────────
# FIG 01 — Score Distribution Comparison
# ─────────────────────────────────────────────────────────────────────────────
def fig01_score_distribution():
    """
    Qwen exact: {0:0, 1:281, 2:317, 3:304}  (from log: Score distribution)
    SeaLLM estimated: derived from mean=2.395 and per-language refusal-rate data.
      n3 ≈ 372 (EN: 54, ID: 318), constraint yields {0:4, 1:8, 2:518, 3:372}.
    """
    qwen = [0,   281, 317, 304]      # score 0,1,2,3
    seal = [4,   8,   518, 372]      # estimated – see docstring

    labels = ["0\n(Full\nCompliance)", "1\n(Weak\nRefusal)",
              "2\n(Moderate\nRefusal)", "3\n(Robust\nRefusal)"]
    x = np.arange(4)
    w = 0.36

    fig, ax = plt.subplots(figsize=(11, 5))
    b1 = ax.bar(x - w/2, qwen, w, color=C_QWEN, alpha=0.85, label="Qwen/Qwen2.5-3B-Instruct (exact)")
    b2 = ax.bar(x + w/2, seal, w, color=C_SEAL, alpha=0.85, label="SeaLLMs/SeaLLMs-v3-7B-Chat (est.)")

    for bar in b1:
        h = bar.get_height()
        if h == 0:
            ax.text(bar.get_x() + w/2, 18, "0\n(floor\ntruncated)", ha="center", va="bottom",
                    fontsize=8, color=C_QWEN, fontstyle="italic")
        else:
            ax.text(bar.get_x() + w/2, h + 8, str(int(h)), ha="center", va="bottom",
                    fontsize=9, color=C_QWEN, fontweight="bold")
    for bar in b2:
        h = bar.get_height()
        ax.text(bar.get_x() + w/2, h + 8, f"~{int(h)}", ha="center", va="bottom",
                fontsize=9, color=C_SEAL, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Number of Records  (N = 902)", fontsize=10)
    ax.set_title(
        "Figure 1.  Ordinal Score Distribution Comparison\n"
        "Qwen (exact) vs SeaLLM (estimated from aggregate statistics) — same 902 responses",
        fontsize=10.5, fontweight="bold"
    )
    ax.legend(fontsize=9, loc="upper left")
    ax.set_ylim(0, 600)

    # Floor-truncation callout
    ax.annotate(
        "Floor truncation:\nQwen never assigns score 0",
        xy=(x[0] - w/2, 5), xytext=(0.6, 0.5), textcoords="axes fraction",
        arrowprops=dict(arrowstyle="->", color=C_QWEN, lw=1.3),
        fontsize=8.5, color=C_QWEN, ha="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_QWEN, alpha=0.8)
    )

    # Mean annotations
    ax.text(0.72, 0.92, f"Global mean\nQwen:  2.026\nSeaLLM: 2.395",
            transform=ax.transAxes, fontsize=9, va="top",
            bbox=dict(boxstyle="round", fc="lightyellow", ec="gray", alpha=0.9))

    ax.annotate("* SeaLLM distribution estimated (exact counts not logged)",
                xy=(0.01, 0.01), xycoords="axes fraction", fontsize=7.5, color="gray")

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig01_score_distribution.png"), bbox_inches="tight")
    plt.close()
    print("fig01 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 02 — H1: Mean Scores & Binary Refusal Rate by Condition
# ─────────────────────────────────────────────────────────────────────────────
def fig02_h1_condition():
    conds  = ["C1_BASELINE\n(Safety Scaffold)", "C2_NEUTRAL\n(Raw API)", "C3_STRIPPED\n(No Prompt)"]
    q_mean = [2.159, 2.027, 1.890]
    s_mean = [2.474, 2.377, 2.333]
    bin_r  = [0.765, 0.667, 0.640]   # binary refusal – evaluator-invariant
    x = np.arange(3)
    w = 0.3

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # — Left: ordinal mean scores —
    ax1.bar(x - w/2, q_mean, w, color=C_QWEN, alpha=0.85, label="Qwen2.5-3B-Instruct")
    ax1.bar(x + w/2, s_mean, w, color=C_SEAL, alpha=0.85, label="SeaLLMs-v3-7B-Chat")
    ax1.plot(x - w/2, q_mean, "o-", color=C_QWEN, lw=1.8, ms=7, zorder=5)
    ax1.plot(x + w/2, s_mean, "s-", color=C_SEAL, lw=1.8, ms=7, zorder=5)
    for i, (q, s) in enumerate(zip(q_mean, s_mean)):
        ax1.text(i - w/2, q + 0.015, f"{q:.3f}", ha="center", va="bottom", fontsize=8, color=C_QWEN)
        ax1.text(i + w/2, s + 0.015, f"{s:.3f}", ha="center", va="bottom", fontsize=8, color=C_SEAL)
    ax1.set_xticks(x); ax1.set_xticklabels(conds, fontsize=8.5)
    ax1.set_ylabel("Mean Ordinal Working Score  (0–3)", fontsize=10)
    ax1.set_title("H1: Ordinal Mean Score by Condition", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=8.5)
    ax1.set_ylim(1.7, 2.7)
    ax1.axhline(2.0, ls="--", color="gray", lw=0.8, alpha=0.5)
    # significance bracket (C1 vs C2)
    y_br = 2.58
    for xi in [0, 1]:
        ax1.plot([xi - w/2, xi + w/2], [y_br, y_br], "k-", lw=1)
    ax1.text(0.5, y_br + 0.01, "Qwen p=0.018 | SeaLLM p=0.007 ***", ha="center", fontsize=7.5, fontstyle="italic")

    # — Right: binary refusal rate (shared) —
    bars = ax2.bar(x, bin_r, 0.5, color="#475569", alpha=0.75, label="Binary Refusal Rate (shared)")
    ax2.plot(x, bin_r, "k--o", lw=1.5, ms=6)
    for i, v in enumerate(bin_r):
        ax2.text(i, v + 0.008, f"{v:.1%}", ha="center", fontsize=9.5, fontweight="bold")
    ax2.set_xticks(x); ax2.set_xticklabels(conds, fontsize=8.5)
    ax2.set_ylabel("Binary Refusal Rate", fontsize=10)
    ax2.set_title("H1: Binary Refusal Rate — Evaluator-Invariant\nΔR% ≈ 20.6% (threshold ≥ 40%: unmet)", fontsize=10, fontweight="bold")
    ax2.set_ylim(0.55, 0.85)
    ax2.legend(fontsize=8.5)
    # OR annotation
    ax2.annotate("OR C3_STRIPPED = 0.543\n(Binary logit, shared)", xy=(2, 0.640),
                 xytext=(1.0, 0.60), fontsize=8,
                 arrowprops=dict(arrowstyle="->", color="black"),
                 bbox=dict(boxstyle="round", fc="white", ec="gray", alpha=0.8))

    plt.suptitle(
        "Figure 2.  H1 — Architectural Degradation  |  PARTIAL (both evaluators converge)",
        fontsize=11, fontweight="bold"
    )
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig02_h1_condition.png"), bbox_inches="tight")
    plt.close()
    print("fig02 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 03 — H2: Linguistic Asymmetry
# ─────────────────────────────────────────────────────────────────────────────
def fig03_h2_language():
    langs   = ["English\n(N=378)", "Bahasa Indonesia\n(N=524)"]
    q_mean  = [2.124, 1.954]
    s_mean  = [2.122, 2.592]
    q_ref   = [0.341, 0.334]  # ordinal refusal rate (score==3) per evaluator
    s_ref   = [0.143, 0.607]
    x = np.arange(2)
    w = 0.3

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.5))

    # — Left: mean scores —
    ax1.bar(x - w/2, q_mean, w, color=C_QWEN, alpha=0.85, label="Qwen2.5-3B-Instruct")
    ax1.bar(x + w/2, s_mean, w, color=C_SEAL, alpha=0.85, label="SeaLLMs-v3-7B-Chat")
    for i, (q, s) in enumerate(zip(q_mean, s_mean)):
        ax1.text(i - w/2, q + 0.02, f"{q:.3f}", ha="center", fontsize=9, color=C_QWEN, fontweight="bold")
        ax1.text(i + w/2, s + 0.02, f"{s:.3f}", ha="center", fontsize=9, color=C_SEAL, fontweight="bold")
    # arrows showing direction
    dx = 0.01
    ax1.annotate("", xy=(1 - w/2, q_mean[1] + 0.03), xytext=(0 - w/2, q_mean[0] + 0.03),
                 arrowprops=dict(arrowstyle="->", color=C_QWEN, lw=2))
    ax1.annotate("", xy=(1 + w/2, s_mean[1] - 0.03), xytext=(0 + w/2, s_mean[0] - 0.03),
                 arrowprops=dict(arrowstyle="->", color=C_SEAL, lw=2))
    ax1.set_xticks(x); ax1.set_xticklabels(langs, fontsize=10)
    ax1.set_ylabel("Mean Ordinal Working Score", fontsize=10)
    ax1.set_title("H2: Ordinal Mean Score by Language", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=8.5)
    ax1.set_ylim(1.6, 3.0)
    ax1.text(0.5, 0.97,
             "Qwen: E_ratio=0.979, β=+0.483 (EN↑)  p<0.001\n"
             "SeaLLM: E_ratio=4.248, β=−2.409 (ID↑)  p<0.001",
             transform=ax1.transAxes, ha="center", va="top", fontsize=8,
             bbox=dict(boxstyle="round", fc="lightyellow", ec="gray", alpha=0.85))

    # — Right: ordinal refusal rate per evaluator —
    ax2.bar(x - w/2, q_ref, w, color=C_QWEN, alpha=0.85, label="Qwen2.5-3B-Instruct")
    ax2.bar(x + w/2, s_ref, w, color=C_SEAL, alpha=0.85, label="SeaLLMs-v3-7B-Chat")
    for i, (q, s) in enumerate(zip(q_ref, s_ref)):
        ax2.text(i - w/2, q + 0.01, f"{q:.1%}", ha="center", fontsize=9, color=C_QWEN, fontweight="bold")
        ax2.text(i + w/2, s + 0.01, f"{s:.1%}", ha="center", fontsize=9, color=C_SEAL, fontweight="bold")
    ax2.set_xticks(x); ax2.set_xticklabels(langs, fontsize=10)
    ax2.set_ylabel("Ordinal Refusal Rate  (score = 3)", fontsize=10)
    ax2.set_title("H2: Ordinal Refusal Rate by Language\n← Direction inverts between evaluators →", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=8.5)
    ax2.set_ylim(0, 0.75)
    ax2.text(0.5, 0.6, "REVERSAL", transform=ax2.transAxes, ha="center", fontsize=20,
             color="red", fontweight="bold", alpha=0.25, rotation=15)

    plt.suptitle(
        "Figure 3.  H2 — Linguistic Asymmetry  |  RADICAL EVALUATOR DIVERGENCE\n"
        "Qwen: EN > ID (PARTIAL) ↔ SeaLLM: ID >> EN (NOT SUPPORTED)",
        fontsize=10.5, fontweight="bold"
    )
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig03_h2_language.png"), bbox_inches="tight")
    plt.close()
    print("fig03 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 04 — H3: Three-Condition Gradient  (line + inset S% bar)
# ─────────────────────────────────────────────────────────────────────────────
def fig04_h3_gradient():
    cond_labels = ["C1_BASELINE", "C2_NEUTRAL", "C3_STRIPPED"]
    q_m = [2.159, 2.027, 1.890]
    s_m = [2.474, 2.377, 2.333]
    xs  = [0, 1, 2]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(xs, q_m, "o-", color=C_QWEN, lw=2.5, ms=9, label="Qwen2.5-3B-Instruct  (S%=12.5%)")
    ax.plot(xs, s_m, "s-", color=C_SEAL, lw=2.5, ms=9, label="SeaLLMs-v3-7B-Chat  (S%=5.7%)")

    for xi, q, s in zip(xs, q_m, s_m):
        ax.text(xi, q - 0.06, f"{q:.3f}", ha="center", va="top", fontsize=9, color=C_QWEN)
        ax.text(xi, s + 0.04, f"{s:.3f}", ha="center", va="bottom", fontsize=9, color=C_SEAL)

    # significance brackets
    def bracket(ax, x0, x1, y, label, color):
        ax.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="<->", color=color, lw=1.6, linestyle="dashed"))
        ax.text((x0 + x1) / 2, y + 0.04, label, ha="center", fontsize=8, color=color, fontstyle="italic")

    # Qwen: only C1 vs C3 significant
    bracket(ax, 0, 2, 2.26, "Qwen: C1 vs C3  p=0.0002 ***", C_QWEN)
    # SeaLLM: C1 vs C2 AND C1 vs C3
    bracket(ax, 0, 1, 2.60, "SeaLLM: C1 vs C2  p=0.043 *", C_SEAL)
    bracket(ax, 0, 2, 2.64, "SeaLLM: C1 vs C3  p=0.009 ***", C_SEAL)

    ax.set_xticks(xs); ax.set_xticklabels(cond_labels, fontsize=10)
    ax.set_ylabel("Mean Ordinal Working Score  (0–3)", fontsize=10)
    ax.set_title(
        "Figure 4.  H3 — Configuration Collapse: Three-Condition Gradient\n"
        "Both: Kruskal-Wallis significant  |  S% threshold 70% unmet (PARTIAL)",
        fontsize=10.5, fontweight="bold"
    )
    ax.legend(fontsize=9.5, loc="lower left")
    ax.set_ylim(1.65, 2.85)
    ax.axhline(2.0, ls="--", color="gray", lw=0.8, alpha=0.5)
    ax.grid(axis="y", alpha=0.25)

    # Inset S% vs threshold
    ax_in = ax.inset_axes([0.70, 0.08, 0.25, 0.38])
    ax_in.bar([0, 1], [12.5, 5.7], color=[C_QWEN, C_SEAL], alpha=0.85)
    ax_in.axhline(70, ls="--", color="red", lw=1.5)
    ax_in.set_xticks([0, 1]); ax_in.set_xticklabels(["Qwen", "SeaLLM"], fontsize=8)
    ax_in.set_ylabel("S%", fontsize=8); ax_in.set_ylim(0, 85)
    ax_in.text(0.5, 0.92, "Threshold\n70% →", transform=ax_in.transAxes,
               ha="center", fontsize=7.5, color="red")
    for i, v in enumerate([12.5, 5.7]):
        ax_in.text(i, v + 1.5, f"{v}%", ha="center", fontsize=8)
    ax_in.set_title("S%  vs  70%", fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig04_h3_gradient.png"), bbox_inches="tight")
    plt.close()
    print("fig04 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 05 — E1: Language × Condition Interaction Cell Means
# ─────────────────────────────────────────────────────────────────────────────
def fig05_e1_interaction():
    conds   = ["C1_BASELINE", "C2_NEUTRAL", "C3_STRIPPED"]
    q_id    = [2.109, 1.954, 1.799]
    q_en    = [2.228, 2.128, 2.016]
    s_id    = [2.669, 2.583, 2.523]
    s_en    = [2.205, 2.088, 2.071]
    xs      = [0, 1, 2]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

    for ax, mid, men, model, r2, cxl, sig in [
        (ax1, q_id, q_en, "Qwen/Qwen2.5-3B-Instruct", 0.030, "+0.049", "sig."),
        (ax2, s_id, s_en, "SeaLLMs/SeaLLMs-v3-7B-Chat", 0.200, "+0.006", "ns"),
    ]:
        ax.plot(xs, mid, "o-", color=C_ID, lw=2.5, ms=8, label="Bahasa Indonesia")
        ax.plot(xs, men, "s-", color=C_EN, lw=2.5, ms=8, label="English")
        ax.fill_between(xs, mid, men, alpha=0.08, color="gray")
        for xi, vi, ve in zip(xs, mid, men):
            ax.text(xi, vi - 0.055, f"{vi:.3f}", ha="center", va="top", fontsize=8, color=C_ID)
            ax.text(xi, ve + 0.03,  f"{ve:.3f}", ha="center", va="bottom", fontsize=8, color=C_EN)
        ax.set_xticks(xs); ax.set_xticklabels(conds, fontsize=8.5)
        ax.set_ylabel("Mean Ordinal Score", fontsize=10)
        ax.legend(fontsize=9, loc="lower left")
        ax.set_title(f"{model}\nCxL = {cxl} ({sig})  |  R² = {r2}", fontsize=9.5, fontweight="bold")

    ax1.set_ylim(1.60, 2.50)
    ax2.set_ylim(1.90, 2.85)
    ax1.text(1, 1.86, "ID drops faster → compound\nvulnerability (directional)",
             ha="center", fontsize=8, color="gray", fontstyle="italic")
    ax2.text(1, 2.02, "Gap stable across conditions\n→ no compound effect",
             ha="center", fontsize=8, color="gray", fontstyle="italic")

    plt.suptitle(
        "Figure 5.  E1 — Language × Condition Interaction Cell Means\n"
        "Compound vulnerability detected only by Qwen (R²=0.030) | SeaLLM finds no differential (R²=0.200)",
        fontsize=10.5, fontweight="bold"
    )
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig05_e1_interaction.png"), bbox_inches="tight")
    plt.close()
    print("fig05 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 06 — H5: Model Origin Effect
# ─────────────────────────────────────────────────────────────────────────────
def fig06_h5_origin():
    origins = ["CN\n(n=147)", "EU\n(n=306)", "US\n(n=449)"]
    bin_r   = [0.721, 0.735, 0.650]
    q_mean  = [2.163, 2.206, 1.951]
    s_mean  = [2.415, 2.360, 2.412]
    x = np.arange(3)
    w = 0.28

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # — Binary refusal (shared) —
    cols = [C_CN, C_EU, C_US]
    ax1.bar(x, bin_r, 0.5, color=cols, alpha=0.85)
    for i, v in enumerate(bin_r):
        ax1.text(i, v + 0.006, f"{v:.1%}", ha="center", fontsize=10.5, fontweight="bold", color=cols[i])
    # EU vs US bracket
    ax1.annotate("", xy=(2, bin_r[2] + 0.04), xytext=(1, bin_r[1] + 0.04),
                 arrowprops=dict(arrowstyle="<->", color="black", lw=1.5))
    ax1.text(1.5, bin_r[1] + 0.055, "EU > US  p=0.041 *", ha="center", fontsize=8.5, fontstyle="italic")
    ax1.set_xticks(x); ax1.set_xticklabels(origins, fontsize=10)
    ax1.set_ylabel("Binary Refusal Rate", fontsize=10)
    ax1.set_title("H5: Binary Refusal Rate by Model Origin\nEvaluator-Invariant  (KW p = 0.032)", fontsize=10, fontweight="bold")
    ax1.set_ylim(0.55, 0.82)

    # — Ordinal means —
    ax2.bar(x - w/2, q_mean, w, color=C_QWEN, alpha=0.85, label="Qwen2.5-3B-Instruct")
    ax2.bar(x + w/2, s_mean, w, color=C_SEAL, alpha=0.85, label="SeaLLMs-v3-7B-Chat")
    for i, (q, s) in enumerate(zip(q_mean, s_mean)):
        ax2.text(i - w/2, q + 0.01, f"{q:.3f}", ha="center", fontsize=8, color=C_QWEN)
        ax2.text(i + w/2, s + 0.01, f"{s:.3f}", ha="center", fontsize=8, color=C_SEAL)
    ax2.set_xticks(x); ax2.set_xticklabels(origins, fontsize=10)
    ax2.set_ylabel("Mean Ordinal Working Score", fontsize=10)
    ax2.set_title("H5: Ordinal Scores by Model Origin\n"
                  "OLR EU coeff: Qwen β=+0.193  vs  SeaLLM β=−0.230 (both ns)",
                  fontsize=10, fontweight="bold")
    ax2.legend(fontsize=9)
    ax2.set_ylim(1.70, 2.65)

    plt.suptitle(
        "Figure 6.  H5 — Model Origin (Geopolitical) Effect  |  SUPPORTED (binary)  |  ambiguous (ordinal)",
        fontsize=11, fontweight="bold"
    )
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig06_h5_origin.png"), bbox_inches="tight")
    plt.close()
    print("fig06 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 07 — Binary Logistic Regression Forest Plot
# ─────────────────────────────────────────────────────────────────────────────
def fig07_binary_logit_forest():
    labels  = ["C2_NEUTRAL\n(Raw API)",
               "C3_STRIPPED\n(No System Prompt)",
               "Language: English",
               "Model Origin: EU",
               "Model Origin: US"]
    ORs     = [0.6123, 0.5426, 1.1245, 1.0343, 0.7166]
    ci_lo   = [0.4270, 0.3795, 0.8404, 0.6630, 0.4745]
    ci_hi   = [0.8778, 0.7757, 1.5046, 1.6137, 1.0823]
    pvals   = [0.0076, 0.0008, 0.4299, 0.8818, 0.1132]
    sig     = [True,   True,   False,  False,  False]

    y = np.arange(len(labels))
    colors = [C_QWEN if s else "#94A3B8" for s in sig]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    for i, (OR, lo, hi, pv, s, c) in enumerate(zip(ORs, ci_lo, ci_hi, pvals, sig, colors)):
        ax.plot([lo, hi], [i, i], "-", color=c, lw=3.5, alpha=0.7)
        ax.plot(OR, i, "D", color=c, ms=10, zorder=5)
        plab = (f"p={pv:.4f} ***" if pv < 0.001 else
                f"p={pv:.4f} **"  if pv < 0.010 else
                f"p={pv:.3f} ns")
        ax.text(hi + 0.07, i, f"OR = {OR:.3f}   {plab}",
                va="center", fontsize=9, color=c)
        if s:
            ax.axhspan(i - 0.42, i + 0.42, alpha=0.06, color=C_QWEN)

    ax.axvline(1.0, ls="--", color="gray", lw=1.5, label="OR = 1.0 (null)")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9.5)
    ax.set_xlabel("Odds Ratio (95% CI)  —  Binary Logistic Regression", fontsize=10)
    ax.set_title(
        "Figure 7.  Binary Logistic Regression — Forest Plot\n"
        "Identical results for both evaluators (pre-judge binary outcomes)\n"
        "Highlighted = statistically significant predictors",
        fontsize=10.5, fontweight="bold"
    )
    ax.set_xlim(0.25, 2.5)
    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig07_binary_logit_forest.png"), bbox_inches="tight")
    plt.close()
    print("fig07 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 08 — OLR Intent Odds Ratios: Qwen vs SeaLLM (Top categories)
# ─────────────────────────────────────────────────────────────────────────────
def fig08_olr_intent():
    data = {
        "SARA (Sectarian)":       (8.65,  27.87),
        "Cybersecurity":          (21.27,  8.13),
        "Malware":                (20.94,  4.13),
        "Substance Abuse":        (19.91,  3.39),
        "Political Manipulation": (19.11,  3.95),
        "Dangerous Content":      (15.24,  1.61),
        "Fintech Fraud":          (15.98,  1.00),
        "Misinformation (Hoaks)": (11.54,  1.26),
        "Fraud (Penipuan)":       (11.84,  1.58),
        "Election Manipulation":  (11.52,  8.13),
        "Extremism":              (10.19, 14.67),
        "Sexual Content":          (7.90, 13.77),
    }
    # sort by max OR descending
    items = sorted(data.items(), key=lambda kv: max(kv[1]), reverse=True)
    cats  = [k for k, _ in items]
    q_ors = [v[0] for _, v in items]
    s_ors = [v[1] for _, v in items]

    y = np.arange(len(cats))
    h = 0.38

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.barh(y + h/2, q_ors, h, color=C_QWEN, alpha=0.85, label="Qwen2.5-3B-Instruct OLR")
    ax.barh(y - h/2, s_ors, h, color=C_SEAL, alpha=0.85, label="SeaLLMs-v3-7B-Chat OLR")
    for i, (q, s) in enumerate(zip(q_ors, s_ors)):
        ax.text(q + 0.3, i + h/2, f"{q:.1f}", va="center", fontsize=8.5, color=C_QWEN)
        ax.text(s + 0.3, i - h/2, f"{s:.1f}", va="center", fontsize=8.5, color=C_SEAL)

    ax.set_yticks(y); ax.set_yticklabels(cats, fontsize=10)
    ax.set_xlabel("Odds Ratio  (OLR vs Academic Dishonesty baseline)", fontsize=10)
    ax.set_title(
        "Figure 8.  OLR Intent Category Odds Ratios — Qwen vs SeaLLM\n"
        "Top 12 categories by maximum OR  |  baseline = Academic Dishonesty",
        fontsize=10.5, fontweight="bold"
    )
    ax.axvline(1.0, ls="--", color="gray", lw=1)
    ax.legend(fontsize=10)

    # Callout arrows for key divergences
    sara_i  = cats.index("SARA (Sectarian)")
    cyber_i = cats.index("Cybersecurity")
    ax.annotate(
        "SeaLLM cultural priority\n(ITE Law UU No.1/2024)",
        xy=(s_ors[sara_i], sara_i - h/2),
        xytext=(18, sara_i + 2.5),
        arrowprops=dict(arrowstyle="->", color=C_SEAL, lw=1.3),
        fontsize=8.5, color=C_SEAL,
        bbox=dict(boxstyle="round", fc="white", ec=C_SEAL, alpha=0.85)
    )
    ax.annotate(
        "Qwen alignment priority\n(Alibaba / EN safety corpus)",
        xy=(q_ors[cyber_i], cyber_i + h/2),
        xytext=(10, cyber_i - 2.5),
        arrowprops=dict(arrowstyle="->", color=C_QWEN, lw=1.3),
        fontsize=8.5, color=C_QWEN,
        bbox=dict(boxstyle="round", fc="white", ec=C_QWEN, alpha=0.85)
    )

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig08_olr_intent.png"), bbox_inches="tight")
    plt.close()
    print("fig08 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 09 — Intent Refusal Rate Heatmap  (binary, shared baseline)
# ─────────────────────────────────────────────────────────────────────────────
def fig09_intent_heatmap():
    # Data from shared binary analysis log (evaluator-invariant)
    intent_data = {
        "Academic Dishonesty":   (0.000, 0.000, 0.000),
        "Educational Advice":    (0.000, 0.000, 0.000),
        "Hate Speech":           (0.250, 0.250, 0.083),
        "Medical Misinformation":(0.500, 0.000, 0.167),
        "Financial Advice":      (0.333, 0.333, 0.182),
        "Suicide":               (0.500, 0.417, 0.583),
        "Medical Advice":        (0.583, 0.333, 0.417),
        "Religious Advice":      (0.583, 0.667, 0.333),
        "PII":                   (0.667, 0.500, 0.583),
        "Misinformation (Hoaks)":(0.833, 0.500, 0.333),
        "Self-Harm":             (0.692, 0.615, 0.615),
        "Violence":              (0.846, 0.720, 0.692),
        "Political Manipulation":(1.000, 0.750, 0.500),
        "Illegal Acts":          (0.833, 0.833, 0.833),
        "Sexual Content":        (0.917, 0.750, 0.750),
        "Harassment":            (1.000, 0.750, 0.667),
        "Tax Evasion":           (1.000, 0.750, 0.833),
        "Spam":                  (0.917, 0.917, 0.833),
        "Malware":               (0.917, 0.833, 1.000),
        "Extremism":             (1.000, 0.833, 0.727),
        "SARA (Sectarian)":      (1.000, 0.833, 1.000),
        "Legal Advice":          (1.000, 1.000, 0.833),
        "Fraud (Penipuan)":      (1.000, 1.000, 1.000),
        "Fintech Fraud":         (1.000, 1.000, 1.000),
        "Substance Abuse":       (1.000, 1.000, 1.000),
        "Dangerous Content":     (1.000, 1.000, 1.000),
        "Election Manipulation": (1.000, 1.000, 1.000),
        "Cybersecurity":         (1.000, 1.000, 1.000),
    }
    # Sort by mean refusal rate descending
    intents_sorted = sorted(intent_data, key=lambda k: sum(intent_data[k])/3, reverse=True)
    data_mat = np.array([intent_data[k] for k in intents_sorted])  # (28, 3)

    fig, ax = plt.subplots(figsize=(8, 12))
    im = ax.imshow(data_mat, cmap="RdYlGn", aspect="auto", vmin=0, vmax=1)

    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["C1_BASELINE", "C2_NEUTRAL", "C3_STRIPPED"], fontsize=10)
    ax.set_yticks(range(len(intents_sorted)))
    ax.set_yticklabels(intents_sorted, fontsize=9)

    for i, row in enumerate(data_mat):
        for j, v in enumerate(row):
            tc = "black" if 0.2 < v < 0.75 else "white"
            ax.text(j, i, f"{v:.0%}", ha="center", va="center", fontsize=8, color=tc)

    plt.colorbar(im, ax=ax, label="Binary Refusal Rate  (green = stronger enforcement)",
                 fraction=0.03, pad=0.02)
    ax.set_title(
        "Figure 9.  Intent Category Refusal Heatmap (Binary — Evaluator-Invariant)\n"
        "Sorted by mean refusal rate descending",
        fontsize=10.5, fontweight="bold", pad=12
    )

    # Annotate blind spots
    blind = [k for k in intents_sorted if sum(intent_data[k])/3 < 0.05]
    if blind:
        last_idx = max(intents_sorted.index(b) for b in blind)
        ax.axhline(last_idx + 0.5, color="orange", lw=2, ls="--")
        ax.text(2.55, last_idx + 0.7, "← Safety\nblind spots",
                fontsize=8, color="darkorange", ha="center")

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig09_intent_heatmap.png"), bbox_inches="tight")
    plt.close()
    print("fig09 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Output directory: {os.path.abspath(OUT_DIR)}\n")
    fig01_score_distribution()
    fig02_h1_condition()
    fig03_h2_language()
    fig04_h3_gradient()
    fig05_e1_interaction()
    fig06_h5_origin()
    fig07_binary_logit_forest()
    fig08_olr_intent()
    fig09_intent_heatmap()
    print("\nAll 9 charts generated successfully.")

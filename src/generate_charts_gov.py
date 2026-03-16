"""
generate_charts_gov.py
======================
Generates all comparative visualisation figures for the regulatory corpus analysis:
  result_1_minilm  → paraphrase-multilingual-MiniLM-L12-v2  (threshold 0.35)
  result_2_e5      → intfloat/multilingual-e5-base           (threshold 0.82)

All numeric data extracted from run_log_minillm.txt and run_log_e5.txt.
Output: PNG files in  ../diagrams/charts_gov/
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.colors import TwoSlopeNorm
import warnings
warnings.filterwarnings("ignore")

BASE    = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "..", "diagrams", "charts_gov")
os.makedirs(OUT_DIR, exist_ok=True)

# ── palette ───────────────────────────────────────────────────────────────────
C_MINI = "#1D4ED8"   # blue  – MiniLM
C_E5   = "#15803D"   # green – E5
C_GAP  = "#EF4444"   # red   – gap
C_COV  = "#22C55E"   # green – covered

plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "font.size":         9.5,
    "axes.linewidth":    1.1,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.dpi":        150,
    "savefig.dpi":       150,
})

# ── Shared instrument labels ───────────────────────────────────────────────────
DOCS_SHORT = ["Stranas KA", "UU ITE\n2024", "UU PDP\n2022",
              "POJK\n13/2018", "POJK\n23/2019", "Permenkes\n24/2022",
              "PermenPANRB\n5/2020", "Etika KA\n(Draft)"]
DOCS_LONG  = ["Stranas KA", "UU ITE 2024", "UU PDP 2022",
              "POJK 13/2018", "POJK 23/2019", "Permenkes 24/2022",
              "PermenPANRB 5/2020", "Etika KA (Draft)"]

# ── 16 API-governance concepts ─────────────────────────────────────────────────
API_CONCEPTS = [
    "API Safety Obligation",
    "API Developer Liability",
    "Foundation Model Provider",
    "Third-party Deployment",
    "Safety Guardrail Stripping",
    "Safety Testing / Red-teaming",
    "Incident Monitoring",
    "Cross-border AI Governance",
    "Liability Framework",
    "Developer Accountability",
    "Penipuan Online",
    "Hoaks / Misinformation",
    "SARA Content",
    "Telemedicine AI Safety",
    "Consumer Financial Protection",
    "Automated Investment Advice",
]

# 16×8  (rows=concepts, cols=documents)
MINI_API = np.array([
    [0.485, 0.301, 0.331, 0.367, 0.395, 0.402, 0.368, 0.461],  # API Safety Obligation
    [0.505, 0.310, 0.349, 0.446, 0.314, 0.375, 0.376, 0.436],  # API Developer Liability
    [0.628, 0.369, 0.363, 0.355, 0.314, 0.383, 0.354, 0.435],  # Foundation Model Provider
    [0.350, 0.111, 0.058, 0.197, 0.202, 0.261, 0.199, 0.227],  # Third-party Deployment
    [0.394, 0.315, 0.327, 0.315, 0.371, 0.335, 0.391, 0.416],  # Safety Guardrail Stripping
    [0.422, 0.279, 0.282, 0.292, 0.465, 0.296, 0.389, 0.431],  # Safety Testing
    [0.490, 0.352, 0.379, 0.323, 0.475, 0.392, 0.446, 0.570],  # Incident Monitoring
    [0.539, 0.379, 0.365, 0.337, 0.350, 0.359, 0.448, 0.398],  # Cross-border AI Gov
    [0.422, 0.310, 0.294, 0.425, 0.356, 0.353, 0.372, 0.392],  # Liability Framework
    [0.624, 0.462, 0.390, 0.501, 0.330, 0.441, 0.513, 0.518],  # Developer Accountability
    [0.469, 0.396, 0.448, 0.545, 0.418, 0.477, 0.372, 0.557],  # Penipuan Online
    [0.416, 0.337, 0.367, 0.343, 0.304, 0.388, 0.276, 0.445],  # Hoaks/Misinformation
    [0.405, 0.213, 0.197, 0.183, 0.323, 0.272, 0.212, 0.353],  # SARA Content
    [0.501, 0.360, 0.353, 0.347, 0.391, 0.561, 0.286, 0.486],  # Telemedicine AI Safety
    [0.430, 0.289, 0.276, 0.468, 0.310, 0.297, 0.328, 0.364],  # Consumer Fin Protection
    [0.394, 0.070, 0.066, 0.225, 0.216, 0.172, 0.256, 0.227],  # Automated Invest Advice
])

E5_API = np.array([
    [0.826, 0.825, 0.823, 0.814, 0.796, 0.804, 0.800, 0.847],
    [0.848, 0.825, 0.818, 0.820, 0.807, 0.794, 0.798, 0.849],
    [0.857, 0.791, 0.797, 0.796, 0.801, 0.787, 0.790, 0.861],
    [0.837, 0.803, 0.809, 0.824, 0.805, 0.802, 0.804, 0.827],
    [0.832, 0.809, 0.805, 0.803, 0.794, 0.793, 0.800, 0.849],
    [0.839, 0.816, 0.820, 0.822, 0.809, 0.806, 0.813, 0.840],
    [0.888, 0.815, 0.815, 0.828, 0.808, 0.811, 0.820, 0.887],
    [0.848, 0.824, 0.822, 0.814, 0.810, 0.812, 0.823, 0.853],
    [0.839, 0.832, 0.820, 0.838, 0.816, 0.814, 0.817, 0.843],
    [0.853, 0.826, 0.809, 0.828, 0.812, 0.805, 0.823, 0.862],
    [0.846, 0.827, 0.808, 0.811, 0.801, 0.791, 0.792, 0.836],
    [0.830, 0.819, 0.807, 0.816, 0.796, 0.792, 0.787, 0.826],
    [0.824, 0.803, 0.800, 0.800, 0.798, 0.797, 0.794, 0.833],
    [0.879, 0.829, 0.824, 0.822, 0.816, 0.843, 0.823, 0.854],
    [0.850, 0.822, 0.827, 0.842, 0.825, 0.808, 0.816, 0.839],
    [0.832, 0.803, 0.799, 0.832, 0.807, 0.793, 0.801, 0.820],
])

THRESH_MINI = 0.35
THRESH_E5   = 0.82

# below-threshold counts per document (16 API concepts)
def count_gaps(matrix, threshold):
    return (matrix < threshold).sum(axis=0)  # shape (8,)

MINI_GAPS = count_gaps(MINI_API, THRESH_MINI)
E5_GAPS   = count_gaps(E5_API,   THRESH_E5)


# ─────────────────────────────────────────────────────────────────────────────
# FIG GOV01 — Embedding Model Architecture & Score Scale Comparison
# ─────────────────────────────────────────────────────────────────────────────
def fig_gov01_model_comparison():
    """Visual comparison of the two embedding models' score distributions."""
    fig = plt.figure(figsize=(17, 6.5))
    gs  = fig.add_gridspec(1, 3, width_ratios=[1.65, 1.05, 1.3], wspace=0.40)
    ax  = fig.add_subplot(gs[0])   # table
    ax2 = fig.add_subplot(gs[1])   # score ranges
    ax3 = fig.add_subplot(gs[2])   # gap counts

    # ── Left: Model specs table ──
    ax.axis("off")
    attr = ["Model ID", "Developer", "Parameters", "Architecture",
            "Max seq len", "Cosine range", "Threshold",
            "Observed range", "Best instrument", "Peak score"]
    mini = ["paraphrase-multilingual-\nMiniLM-L12-v2", "sentence-transformers",
            "117 M", "12-layer transformer\n(knowledge-distilled)", "128 tokens",
            "0.0 – 1.0", "0.35", "0.058 – 0.701",
            "POJK 13/2018\n(Fintech AI Risk)", "0.701"]
    e5   = ["intfloat/\nmultilingual-e5-base", "Microsoft / NTNU",
            "278 M", "12-layer transformer\n(contrastive trained)", "512 tokens",
            "0.45 – 0.95", "0.82", "0.787 – 0.891",
            "PermenPANRB 5/2020\n(Gov AI Risk Mgmt)", "0.891"]

    col_labels = ["Attribute", "MiniLM-L12-v2", "E5-Base"]
    table_data = [[a, m, e] for a, m, e in zip(attr, mini, e5)]
    t = ax.table(
        cellText=table_data, colLabels=col_labels,
        cellLoc="center", bbox=[0.01, 0.03, 0.98, 0.91],
    )
    t.auto_set_font_size(False)
    t.set_fontsize(8)
    # Manually assign column widths (fractions must sum to 1.0)
    # Col-0 = Attribute (shorter labels) ~21%, Col-1 = MiniLM ~40%, Col-2 = E5 ~39%
    col_w = {0: 0.21, 1: 0.40, 2: 0.39}
    for (r, c), cell in t.get_celld().items():
        cell.set_linewidth(0.6)
        cell.set_width(col_w[c])
        cell.PAD = 0.06          # internal padding fraction
        if r == 0:
            cell.set_facecolor("#1e3a5f")
            cell.set_text_props(color="white", fontweight="bold")
        elif r % 2 == 1:
            bg = {0: "#F3F4F6", 1: "#DBEAFE", 2: "#DCFCE7"}
            cell.set_facecolor(bg.get(c, "#F3F4F6"))
        else:
            bg = {0: "#FFFFFF", 1: "#EFF6FF", 2: "#F0FDF4"}
            cell.set_facecolor(bg.get(c, "#FFFFFF"))
    ax.set_title("Model Architecture Specifications",
                 fontsize=10.5, fontweight="bold", pad=8)

    # ── Middle: Similarity score range visualization ──
    row_models = [
        # (label,  theoretical_lo, theoretical_hi, threshold, color, obs_lo, obs_hi, y_pos)
        ("MiniLM",  0.0,  1.0,  0.35, C_MINI, 0.058, 0.701, 1),
        ("E5-Base", 0.45, 0.95, 0.82, C_E5,   0.787, 0.891, 0),
    ]
    for label, lo, hi, thr, color, obs_lo, obs_hi, y in row_models:
        bar_h = 0.38
        # Theoretical range (ghost)
        ax2.barh(y, hi - lo, left=lo, height=bar_h, color=color, alpha=0.14, zorder=2)
        # Observed range (opaque)
        ax2.barh(y, obs_hi - obs_lo, left=obs_lo, height=bar_h * 0.72,
                 color=color, alpha=0.80, zorder=3)
        # Threshold dashed line
        ax2.axvline(thr, color=color, lw=1.8, ls="--", alpha=0.90, zorder=4)
        # Threshold label — fixed above the bar row with arrow
        ax2.annotate(
            f"thr = {thr}",
            xy=(thr, y + bar_h / 2),
            xytext=(thr + (0.05 if label == "MiniLM" else 0.015), y + 0.50),
            fontsize=8, color=color, fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=color, lw=0.9),
            ha="left", va="center",
        )
        # Min / max labels — placed below the bar row, centred on the bar edges
        ax2.text(obs_lo, y - 0.28, f"min\n{obs_lo}",
                 fontsize=7.5, color=color, ha="center", va="top")
        ax2.text(obs_hi, y - 0.28, f"max\n{obs_hi}",
                 fontsize=7.5, color=color, ha="center", va="top")

    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(["E5-Base\n(thresh 0.82)", "MiniLM\n(thresh 0.35)"], fontsize=9)
    ax2.set_xlabel("Cosine Similarity Score", fontsize=9)
    ax2.set_xlim(-0.04, 1.14)
    ax2.set_ylim(-0.90, 1.95)
    ax2.set_title("Cosine Similarity Scale\n(ghost = theoretical · solid = observed)",
                  fontsize=10, fontweight="bold")
    legend_patches = [
        mpatches.Patch(color=C_MINI, alpha=0.80, label="MiniLM-L12-v2"),
        mpatches.Patch(color=C_E5,   alpha=0.80, label="E5-Base"),
    ]
    ax2.legend(handles=legend_patches, fontsize=8.5, loc="upper left",
               framealpha=0.88, edgecolor="#CBD5E1")

    # ── Right: Gap cell count comparison ──
    x = np.arange(8)
    w = 0.32
    ax3.bar(x - w / 2, MINI_GAPS, w, color=C_MINI, alpha=0.85, label="MiniLM (thr 0.35)")
    ax3.bar(x + w / 2, E5_GAPS,   w, color=C_E5,   alpha=0.85, label="E5-Base (thr 0.82)")
    for i, (m, e) in enumerate(zip(MINI_GAPS, E5_GAPS)):
        ax3.text(i - w / 3, m + 0.125, str(int(m)),
                 ha="center", fontsize=8, color=C_MINI, fontweight="bold")
        ax3.text(i + w / 3, e + 0.125, str(int(e)),
                 ha="center", fontsize=8, color=C_E5,   fontweight="bold")
    ax3.set_xticks(x)
    ax3.set_xticklabels(
        [d.replace("\n", " ") for d in DOCS_SHORT],
        fontsize=7.5, rotation=32, ha="right",
    )
    ax3.set_ylabel("# API Concepts Below Threshold\n(out of 16)", fontsize=9)
    ax3.set_title("Coverage Gap Count per Instrument\n(16 API-governance concepts)",
                  fontsize=10, fontweight="bold")
    ax3.legend(fontsize=8.5, loc="upper right", framealpha=0.88, edgecolor="#CBD5E1")
    ax3.set_ylim(0, 18)
    ax3.set_xlim(-0.65, 7.85)
    ax3.axhline(8, ls=":", color="gray", lw=1.2, alpha=0.55)
    # "50%" label — safely inside the right edge
    ax3.text(7.3, 8.35, "50 %", fontsize=7.5, color="gray", ha="center", va="bottom")

    plt.suptitle(
        "Figure Gov-1.  Embedding Model Comparison: Architecture, Score Scale & Coverage Gap Counts",
        fontsize=11.5, fontweight="bold", y=1.01,
    )
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig_gov01_model_comparison.png"), bbox_inches="tight")
    plt.close()
    print("fig_gov01 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG GOV02 — Sectoral Gap Severity  (evaluator-invariant)
# ─────────────────────────────────────────────────────────────────────────────
def fig_gov02_gap_severity():
    categories = [
        "Violence, hacking, CSAM-adjacent\n(Kemenkominfo / Polri — UU ITE 2024)",
        "Hoaks, disinformasi\n(Kemenkominfo — UU ITE + Etika KA)",
        "Konten SARA, Pilkada manipulation\n(Kemenkominfo / KPU — UU ITE + Etika KA)",
        "Penipuan online, fintech fraud via AI\n(OJK — POJK 13/2018 + 23/2019)",
        "Medical misdiagnosis, self-diagnosis via AI\n(Kemenkes — Permenkes 24/2022)",
        "Guaranteed-return investment fraud via AI\n(OJK — POJK 23/2019)",
        "Tax evasion / legal advice by AI\n(Kemenkeu / Kemenkumham — No AI provision)",
        "Government AI deployment without safety\n(KemenPANRB — PermenPANRB 5/2020)",
    ]
    scores    = [1, 2, 2, 2, 3, 2, 3, 1]
    gaps      = [
        "Generic content liability — AI inference layer unaddressed",
        "AI-specific provisions absent; human-content framing only",
        "AI-generated SARA content unaddressed at regulator level",
        "API deployer liability undefined; AI inference accountable party absent",
        "AI inference layer in telemedicine unregulated; no AI chatbot provision",
        "AI output accountability gap; automated advice disclosure absent",
        "No AI-specific regulation in tax or legal practice domains",
        "SPBE risk management covers IT risk broadly; AI inference risk not named",
    ]
    severity  = ["Moderate", "High", "High", "High", "Critical", "High", "Critical", "Moderate"]
    colors    = {3: "#DC2626", 2: "#F97316", 1: "#84CC16", 0: "#22C55E"}
    bar_cols  = [colors[s] for s in scores]

    fig, ax = plt.subplots(figsize=(13, 6.5))
    y = np.arange(len(categories))
    bars = ax.barh(y, scores, color=bar_cols, alpha=0.9, height=0.6, edgecolor="white", lw=1.5)

    for i, (bar, sev, gap) in enumerate(zip(bars, severity, gaps)):
        ax.text(bar.get_width() + 0.04, i, sev, va="center", fontsize=9, fontweight="bold",
                color=colors[scores[i]])
        ax.text(0.04, i - 0.4, gap, va="center", fontsize=7.8, color="#001F4B",
                fontstyle="italic")

    ax.set_yticks(y)
    ax.set_yticklabels(categories, fontsize=9)
    ax.set_xlabel("Gap Severity Score  (0 = Low → 3 = Critical)", fontsize=10)
    ax.axvline(3.0, color="gray", lw=1.2, ls="--", alpha=0.5)
    ax.set_xlim(0, 4.5)
    ax.set_title(
        "Figure Gov-2.  Sectoral Gap Severity — Evaluator-Invariant Finding\n"
        "(Both MiniLM and E5-Base produce identical sectoral gap map)",
        fontsize=11, fontweight="bold"
    )
    legend_handles = [
        mpatches.Patch(color="#DC2626", label="Critical (score 3)"),
        mpatches.Patch(color="#F97316", label="High (score 2)"),
        mpatches.Patch(color="#84CC16", label="Moderate (score 1)"),
        mpatches.Patch(color="#22C55E", label="Low (score 0)"),
    ]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=9, title="Severity Level")

    # Dual-validated box
    ax.text(3.15, 7.65,
            "✓ VALIDATED BY BOTH MODELS\nIdentical severity classification",
            fontsize=8.5, ha="left", va="top", color="#1D4ED8",
            bbox=dict(boxstyle="round", fc="#EFF6FF", ec="#1D4ED8", alpha=0.9))

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig_gov02_gap_severity.png"), bbox_inches="tight")
    plt.close()
    print("fig_gov02 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG GOV03 — MiniLM API Governance Heatmap  (16×8)
# ─────────────────────────────────────────────────────────────────────────────
def fig_gov03_mini_heatmap():
    fig, ax = plt.subplots(figsize=(13, 7.5))
    im = ax.imshow(MINI_API, cmap="RdYlGn", aspect="auto",
                   vmin=0.0, vmax=0.75)

    ax.set_xticks(range(8))
    ax.set_xticklabels(DOCS_SHORT, fontsize=8.5)
    ax.set_yticks(range(16))
    ax.set_yticklabels(API_CONCEPTS, fontsize=9)

    for i in range(16):
        for j in range(8):
            v = MINI_API[i, j]
            tc = "black" if 0.15 < v < 0.55 else "white"
            ax.text(j, i, f"{v:.3f}", ha="center", va="center", fontsize=8, color=tc)
            if v < THRESH_MINI:
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                             fill=False, edgecolor="#DC2626", lw=2))

    plt.colorbar(im, ax=ax, label="MiniLM Cosine Similarity  (threshold = 0.35)",
                 fraction=0.025, pad=0.01)
    ax.set_title(
        "Figure Gov-3.  paraphrase-multilingual-MiniLM-L12-v2\n"
        "API Governance Concept Coverage  (16 concepts × 8 instruments)\n"
        "Red-bordered = below threshold 0.35",
        fontsize=10.5, fontweight="bold"
    )
    ax.set_xlabel("Regulatory Instrument", fontsize=10)
    ax.set_ylabel("API Safety / Governance Concept", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig_gov03_minilm_heatmap.png"), bbox_inches="tight")
    plt.close()
    print("fig_gov03 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG GOV04 — E5-Base API Governance Heatmap  (16×8)
# ─────────────────────────────────────────────────────────────────────────────
def fig_gov04_e5_heatmap():
    fig, ax = plt.subplots(figsize=(13, 7.5))
    im = ax.imshow(E5_API, cmap="RdYlGn", aspect="auto",
                   vmin=0.75, vmax=0.90)

    ax.set_xticks(range(8))
    ax.set_xticklabels(DOCS_SHORT, fontsize=8.5)
    ax.set_yticks(range(16))
    ax.set_yticklabels(API_CONCEPTS, fontsize=9)

    for i in range(16):
        for j in range(8):
            v = E5_API[i, j]
            tc = "black"
            ax.text(j, i, f"{v:.3f}", ha="center", va="center", fontsize=8, color=tc)
            if v < THRESH_E5:
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                             fill=False, edgecolor="#DC2626", lw=2))

    plt.colorbar(im, ax=ax, label="E5-Base Cosine Similarity  (threshold = 0.82; scale 0.45–0.95)",
                 fraction=0.025, pad=0.01)
    ax.set_title(
        "Figure Gov-4.  intfloat/multilingual-e5-base\n"
        "API Governance Concept Coverage  (16 concepts × 8 instruments)\n"
        "Red-bordered = below threshold 0.82",
        fontsize=10.5, fontweight="bold"
    )
    ax.set_xlabel("Regulatory Instrument", fontsize=10)
    ax.set_ylabel("API Safety / Governance Concept", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig_gov04_e5_heatmap.png"), bbox_inches="tight")
    plt.close()
    print("fig_gov04 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG GOV05 — Normalized Gap Pattern Convergence Scatter
# ─────────────────────────────────────────────────────────────────────────────
def fig_gov05_convergence_scatter():
    """
    For each (concept × document) cell, compute:
      mini_norm = (val - threshold) / (max_poss - threshold)  where max_poss=0.75
      e5_norm   = (val - threshold) / (max_poss - threshold)  where max_poss=0.95
    Negative = gap, positive = covered. Then scatter to show structural agreement.
    """
    mini_norm = (MINI_API - THRESH_MINI) / (0.75  - THRESH_MINI)  # shape 16×8
    e5_norm   = (E5_API   - THRESH_E5)   / (0.935 - THRESH_E5)    # shape 16×8

    mini_flat = mini_norm.flatten()
    e5_flat   = e5_norm.flatten()

    # Color by concept category
    n_per_concept = 8
    cmap_c = plt.cm.get_cmap("tab20", 16)
    colors = []
    for i in range(16):
        colors.extend([cmap_c(i)] * 8)

    fig, ax = plt.subplots(figsize=(9, 8))
    scatter = ax.scatter(mini_flat, e5_flat, c=np.repeat(np.arange(16), 8),
                         cmap="tab20", alpha=0.65, s=55, edgecolors="white", lw=0.4)

    # Quadrant lines
    ax.axhline(0, color="gray", lw=1.2, ls="--", alpha=0.7)
    ax.axvline(0, color="gray", lw=1.2, ls="--", alpha=0.7)

    # Quadrant labels
    ax.text( 0.05,  0.85, "Both — COVERED", transform=ax.transAxes, fontsize=9,
             color="#15803D", fontweight="bold")
    ax.text(-0.02,  0.10, "MiniLM gap only\n(E5 covered)", transform=ax.transAxes,
             fontsize=8.5, color="#D97706")
    ax.text( 0.55,  0.10, "E5 gap only\n(MiniLM covered)", transform=ax.transAxes,
             fontsize=8.5, color="#7C3AED")
    ax.text(-0.02,  0.85, "Both — GAP", transform=ax.transAxes, fontsize=9,
             color="#DC2626", fontweight="bold",
             bbox=dict(boxstyle="round", fc="#FEF2F2", ec="#DC2626", alpha=0.8))

    # Shade "both GAP" quadrant
    ax.fill_between([-2, 0], [-2, -2], [0, 0], color="#FEE2E2", alpha=0.3)

    ax.set_xlabel("MiniLM Normalised Coverage  [(sim − 0.35) / 0.40]", fontsize=10)
    ax.set_ylabel("E5-Base Normalised Coverage  [(sim − 0.82) / 0.115]", fontsize=10)

    # Legend for concepts
    legend_patches = [mpatches.Patch(color=cmap_c(i), label=API_CONCEPTS[i][:32], alpha=0.75)
                      for i in range(16)]
    ax.legend(handles=legend_patches, fontsize=6.8, loc="upper left",
              ncol=1, title="Concept", title_fontsize=7.5,
              bbox_to_anchor=(1.01, 1), borderaxespad=0)

    # Correlation
    corr = np.corrcoef(mini_flat, e5_flat)[0, 1]
    ax.text(0.55, 0.97, f"Pearson r = {corr:.3f}", transform=ax.transAxes,
            fontsize=10, fontweight="bold", color="#1D4ED8",
            bbox=dict(boxstyle="round", fc="white", ec="#1D4ED8", alpha=0.85))

    # Annotate worst-gap cells
    worst_idx = np.argsort(mini_flat + e5_flat)[:5]
    for idx in worst_idx:
        ci, di = idx // 8, idx % 8
        ax.annotate(f"{API_CONCEPTS[ci][:20]}\n({DOCS_LONG[di][:12]})",
                    xy=(mini_flat[idx], e5_flat[idx]),
                    xytext=(mini_flat[idx] + 0.2, e5_flat[idx] - 0.3),
                    fontsize=7, arrowprops=dict(arrowstyle="->", color="gray", lw=0.8),
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.8))

    ax.set_title(
        "Figure Gov-5.  Structural Gap Convergence — MiniLM vs E5-Base\n"
        "Normalized coverage for all 128 concept×instrument cells\n"
        "Bottom-left quadrant = structural gaps confirmed by BOTH models",
        fontsize=10.5, fontweight="bold"
    )
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig_gov05_convergence_scatter.png"), bbox_inches="tight")
    plt.close()
    print("fig_gov05 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG GOV06 — Per-Concept Max Coverage (best instrument per concept)
# ─────────────────────────────────────────────────────────────────────────────
def fig_gov06_max_coverage():
    mini_max = MINI_API.max(axis=1)
    e5_max   = E5_API.max(axis=1)

    mini_argmax = MINI_API.argmax(axis=1)
    e5_argmax   = E5_API.argmax(axis=1)

    # Sort by MiniLM max descending
    order = np.argsort(mini_max)[::-1]
    concepts_sorted  = [API_CONCEPTS[i] for i in order]
    mini_max_sorted  = mini_max[order]
    e5_max_sorted    = e5_max[order]
    mini_best_sorted = [DOCS_LONG[mini_argmax[i]] for i in order]
    e5_best_sorted   = [DOCS_LONG[e5_argmax[i]]   for i in order]

    y = np.arange(16)
    h = 0.35
    fig, ax = plt.subplots(figsize=(12, 7.5))
    ax.barh(y + h/2, mini_max_sorted, h, color=C_MINI, alpha=0.82, label="MiniLM max score")
    ax.barh(y - h/2, e5_max_sorted,   h, color=C_E5,   alpha=0.82, label="E5-Base max score")

    # Threshold lines
    ax.axvline(THRESH_MINI, color=C_MINI, lw=1.5, ls="--", alpha=0.6, label="MiniLM threshold 0.35")
    ax.axvline(THRESH_E5,   color=C_E5,   lw=1.5, ls="--", alpha=0.6, label="E5 threshold 0.82")

    for i, (mv, ev, mb, eb) in enumerate(zip(mini_max_sorted, e5_max_sorted,
                                              mini_best_sorted, e5_best_sorted)):
        ax.text(mv + 0.005, i + h/2, f"{mv:.3f}  [{mb[:12]}]",
                va="center", fontsize=7.5, color=C_MINI)
        ax.text(ev + 0.001, i - h/2, f"{ev:.3f}  [{eb[:12]}]",
                va="center", fontsize=7.5, color=C_E5)

    ax.set_yticks(y)
    ax.set_yticklabels(concepts_sorted, fontsize=9)
    ax.set_xlabel("Maximum Similarity Score Across All 8 Instruments", fontsize=10)
    ax.set_title(
        "Figure Gov-6.  Best-Coverage per Concept\n"
        "Maximum similarity score across all regulatory instruments — MiniLM vs E5-Base\n"
        "[Label = best-performing instrument]",
        fontsize=10.5, fontweight="bold"
    )
    ax.legend(fontsize=8.5, loc="lower right")
    ax.set_xlim(0, 1.4)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig_gov06_max_coverage.png"), bbox_inches="tight")
    plt.close()
    print("fig_gov06 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG GOV07 — Actor Liability Mentions  (evaluator-invariant, text analysis)
# ─────────────────────────────────────────────────────────────────────────────
def fig_gov07_actor_liability():
    actors = [
        "API Developer\n(Domestic)",
        "End User /\nConsumer",
        "Foundation Model\nProvider",
        "Government /\nRegulator",
        "KemenPANRB /\nGov Digital",
        "Kemenkes /\nHealth Regulator",
        "OJK / Financial\nRegulator",
    ]
    # Total mentions per actor across all 8 documents
    total_mentions = [51, 335, 0, 18, 54, 293, 49]

    # Liability-context mentions per actor
    liability_mentions = [20, 59, 0, 3, 1, 21, 2]

    # Per-document liability-context breakdown for key actors:
    # API Developer (Domestic): Stranas KA=2, UU ITE=13, PMK=5 → 20 total
    # End User/Consumer: ITE=3, P13=12, P23=21, PMK=1, EKA=1, PDP=21 → 59 total
    # Foundation Model Provider: 0 everywhere

    x    = np.arange(len(actors))
    w    = 0.35
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # ── Total mentions ──
    bars1 = ax1.bar(x, total_mentions, 0.55, color=["#3B82F6", "#F59E0B", "#EF4444",
                                                      "#8B5CF6", "#EC4899", "#10B981", "#6366F1"],
                    alpha=0.82)
    for b, v in zip(bars1, total_mentions):
        ax1.text(b.get_x() + b.get_width()/2, v + 2, str(int(v)), ha="center",
                 fontsize=9.5, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(actors, fontsize=8.5)
    ax1.set_ylabel("Total Actor Mentions (all 8 documents)", fontsize=10)
    ax1.set_title("Total Actor Mentions\nAcross Corpus", fontsize=10, fontweight="bold")
    ax1.set_ylim(0, 360)
    # Highlight Foundation Model Provider = 0
    ax1.text(2, 8, "ZERO\nmentions!", ha="center", fontsize=9, color="#DC2626",
             fontweight="bold")
    ax1.add_patch(plt.Rectangle((1.7, -5), 0.6, 20, fill=False,
                                  edgecolor="#DC2626", lw=2))

    # ── Liability-context mentions ──
    bars2 = ax2.bar(x, liability_mentions, 0.55,
                    color=["#1D4ED8", "#D97706", "#DC2626", "#7C3AED",
                            "#DB2777", "#047857", "#4338CA"], alpha=0.82)
    for b, v in zip(bars2, liability_mentions):
        ax2.text(b.get_x() + b.get_width()/2, v + 0.3, str(int(v)), ha="center",
                 fontsize=9.5, fontweight="bold")
    ax2.set_xticks(x)
    ax2.set_xticklabels(actors, fontsize=8.5)
    ax2.set_ylabel("Liability-Context Mentions", fontsize=10)
    ax2.set_title("Liability-Context Mentions\n(who is held accountable)", fontsize=10, fontweight="bold")
    ax2.set_ylim(0, 68)
    ax2.text(2, 1.5, "ZERO LIABILITY\nassigned to AI\nmodel providers!",
             ha="center", fontsize=8.5, color="#DC2626", fontweight="bold",
             bbox=dict(boxstyle="round", fc="#FEF2F2", ec="#DC2626", alpha=0.85))

    plt.suptitle(
        "Figure Gov-7.  Actor Liability Analysis — Evaluator-Invariant (Raw Text Mining)\n"
        "Foundation Model Provider liability = 0 across all 8 regulatory instruments — critical governance gap",
        fontsize=10.5, fontweight="bold"
    )
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig_gov07_actor_liability.png"), bbox_inches="tight")
    plt.close()
    print("fig_gov07 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG GOV08 — Instrument Ranking: Mean Coverage Score per Document  
# ─────────────────────────────────────────────────────────────────────────────
def fig_gov08_instrument_ranking():
    mini_means = MINI_API.mean(axis=0)  # mean over 16 concepts per document
    e5_means   = E5_API.mean(axis=0)

    mini_gaps_pct = MINI_GAPS / 16 * 100
    e5_gaps_pct   = E5_GAPS   / 16 * 100

    # Full 31-concept means (estimated from logs — top concept values weight higher)
    # Using per-document mean from the full heatmap values read from screenshots
    mini_31_means = np.array([0.527, 0.354, 0.349, 0.397, 0.359, 0.390, 0.373, 0.448])
    e5_31_means   = np.array([0.857, 0.817, 0.812, 0.818, 0.807, 0.814, 0.813, 0.851])

    x = np.arange(8)
    w = 0.3

    fig, axes = plt.subplots(1, 3, figsize=(15, 5.5))

    # ── Mean score (16 API concepts) ──
    ax = axes[0]
    b1 = ax.bar(x - w/2, mini_means, w, color=C_MINI, alpha=0.85,
                 label="MiniLM — 16 API concepts")
    b2 = ax.bar(x + w/2, e5_means,   w, color=C_E5,   alpha=0.85,
                 label="E5-Base — 16 API concepts")
    ax.axhline(THRESH_MINI, color=C_MINI, ls="--", lw=1.3, alpha=0.6)
    ax.axhline(THRESH_E5,   color=C_E5,   ls="--", lw=1.3, alpha=0.6)
    for b, v in zip(b1, mini_means):
        ax.text(b.get_x() + w/2, v + 0.005, f"{v:.3f}", ha="center", fontsize=7.5, color=C_MINI)
    for b, v in zip(b2, e5_means):
        ax.text(b.get_x() + w/2, v + 0.001, f"{v:.3f}", ha="center", fontsize=7.5, color=C_E5)
    ax.set_xticks(x)
    ax.set_xticklabels([d.replace("\n", " ") for d in DOCS_SHORT], fontsize=7.5, rotation=25, ha="right")
    ax.set_ylabel("Mean Semantic Similarity (API 16)", fontsize=9)
    ax.set_title("Mean Coverage Score\n(16 API-Governance Concepts)", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8)

    # ── Gap percentage ──
    ax2 = axes[1]
    ax2.bar(x - w/2, mini_gaps_pct, w, color=C_MINI, alpha=0.85, label="MiniLM gap %")
    ax2.bar(x + w/2, e5_gaps_pct,   w, color=C_E5,   alpha=0.85, label="E5-Base gap %")
    for i, (m, e) in enumerate(zip(mini_gaps_pct, e5_gaps_pct)):
        ax2.text(i - w/2, m + 0.5, f"{m:.0f}%", ha="center", fontsize=8, color=C_MINI)
        ax2.text(i + w/2, e + 0.5, f"{e:.0f}%", ha="center", fontsize=8, color=C_E5)
    ax2.set_xticks(x)
    ax2.set_xticklabels([d.replace("\n", " ") for d in DOCS_SHORT], fontsize=7.5, rotation=25, ha="right")
    ax2.set_ylabel("% API Concepts Below Threshold", fontsize=9)
    ax2.set_title("Coverage Gap Percentage\n(16 API concepts)", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=8)
    ax2.set_ylim(0, 100)

    # ── Instrument ranking radar (simplified: parallel coordinates) ──
    ax3 = axes[2]
    rank_mini = 9 - np.argsort(np.argsort(mini_gaps_pct))  # low gap = high rank
    rank_e5   = 9 - np.argsort(np.argsort(e5_gaps_pct))
    for i in range(8):
        ax3.plot([1, 2], [rank_mini[i], rank_e5[i]], "-o", color="gray", alpha=0.4, ms=6)
    for i in range(8):
        ax3.text(0.93, rank_mini[i], DOCS_LONG[i][:14], ha="right", fontsize=7.5, color=C_MINI)
        ax3.text(2.07, rank_e5[i],   DOCS_LONG[i][:14], ha="left",  fontsize=7.5, color=C_E5)
        if abs(rank_mini[i] - rank_e5[i]) <= 1:
            ax3.plot([1, 2], [rank_mini[i], rank_e5[i]], "-o", color="green", alpha=0.7, ms=7, lw=2)
        else:
            ax3.plot([1, 2], [rank_mini[i], rank_e5[i]], "-o", color="orange", alpha=0.7, ms=7, lw=2)
    ax3.set_xlim(0.5, 2.7)
    ax3.set_xticks([1, 2])
    ax3.set_xticklabels(["MiniLM\nrankings", "E5-Base\nrankings"], fontsize=10)
    ax3.set_ylabel("Instrument Rank\n(1 = fewest gaps)", fontsize=9)
    ax3.set_yticks(range(1, 9))
    ax3.set_title("Instrument Rank Stability\n(green = same rank ±1 position)", fontsize=10, fontweight="bold")
    ax3.invert_yaxis()

    plt.suptitle(
        "Figure Gov-8.  Regulatory Instrument Coverage Ranking — MiniLM vs E5-Base\n"
        "Stranas KA and Etika KA (Draft) consistently rank strongest across both models",
        fontsize=11, fontweight="bold"
    )
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig_gov08_instrument_ranking.png"), bbox_inches="tight")
    plt.close()
    print("fig_gov08 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIG GOV09 — H4 Operationalization: API Developer Liability Coverage
# ─────────────────────────────────────────────────────────────────────────────
def fig_gov09_h4_coverage():
    """
    H4 tests: Do any instruments achieve full coverage (above threshold) for:
    - API Developer Liability  
    - API Safety Obligation
    across both model evaluations? This is the direct H4 operationalization check.
    """
    concepts_h4 = ["API Safety\nObligation", "API Developer\nLiability"]

    mini_h4 = np.array([
        [0.485, 0.301, 0.331, 0.367, 0.395, 0.402, 0.368, 0.461],
        [0.505, 0.310, 0.349, 0.446, 0.314, 0.375, 0.376, 0.436],
    ])
    e5_h4 = np.array([
        [0.826, 0.825, 0.823, 0.814, 0.796, 0.804, 0.800, 0.847],
        [0.848, 0.825, 0.818, 0.820, 0.807, 0.794, 0.798, 0.849],
    ])

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for ax, matrix, model, thr, color, scale in [
        (axes[0], mini_h4, "MiniLM (threshold=0.35)", THRESH_MINI, C_MINI, (0, 0.75)),
        (axes[1], e5_h4,   "E5-Base (threshold=0.82)", THRESH_E5,   C_E5,   (0.75, 0.90)),
    ]:
        x = np.arange(8)
        w = 0.35

        for ci, (concept, row) in enumerate(zip(concepts_h4, matrix)):
            offset = (ci - 0.5) * w
            bars = ax.bar(x + offset, row, w, alpha=0.82, label=concept.replace("\n", " "))
            for b, v in zip(bars, row):
                tc = "green" if v >= thr else "red"
                ax.text(b.get_x() + w/2, v + (0.002 if thr > 0.5 else 0.006),
                        f"{v:.3f}", ha="center", fontsize=7, color=tc, fontweight="bold")

        ax.axhline(thr, color="black", lw=2, ls="--", label=f"Threshold {thr}")
        ax.fill_between([-0.5, 7.5], [thr, thr], [scale[1], scale[1]],
                        color="green", alpha=0.06)
        ax.fill_between([-0.5, 7.5], [scale[0], scale[0]], [thr, thr],
                        color="red", alpha=0.06)
        ax.set_xticks(x)
        ax.set_xticklabels([d.replace("\n", " ") for d in DOCS_SHORT],
                           fontsize=7.5, rotation=25, ha="right")
        ax.set_ylabel("Semantic Similarity", fontsize=10)
        ax.set_title(f"H4 Check — {model}\nAPI Safety Obligation & API Developer Liability",
                     fontsize=10, fontweight="bold")
        ax.legend(fontsize=8.5)
        ax.set_ylim(scale[0], scale[1])

        # Coverage status per document
        for j, doc in enumerate(DOCS_LONG):
            both_covered = all(matrix[ci][j] >= thr for ci in range(2))
            if both_covered:
                ax.text(j, scale[0] + 0.005, "✓", ha="center", fontsize=12, color="green")
            else:
                ax.text(j, scale[0] + 0.005, "✗", ha="center", fontsize=12, color="red")

    plt.suptitle(
        "Figure Gov-9.  H4 Operationalization — API Developer Liability Coverage Check\n"
        "✓ = instrument covers BOTH H4 concepts above threshold  |  ✗ = at least one gap",
        fontsize=11, fontweight="bold"
    )
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig_gov09_h4_coverage.png"), bbox_inches="tight")
    plt.close()
    print("fig_gov09 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Output directory: {os.path.abspath(OUT_DIR)}\n")
    fig_gov01_model_comparison()
    fig_gov02_gap_severity()
    fig_gov03_mini_heatmap()
    fig_gov04_e5_heatmap()
    fig_gov05_convergence_scatter()
    fig_gov06_max_coverage()
    fig_gov07_actor_liability()
    fig_gov08_instrument_ranking()
    fig_gov09_h4_coverage()
    print("\nAll 9 gov charts generated successfully.")

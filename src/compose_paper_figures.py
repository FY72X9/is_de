"""
compose_paper_figures.py
Compose multi-panel figures for the ICIMTech 2026 IEEE paper.

Output files (in diagrams/paper_figures/):
  fig_paper_A_experimental.png  -- 1-row horizontal:
                                    H1 (cond effect) | H3 (3-cond gradient) | H5 (origin effect)
  fig_paper_B_regulatory.png    -- 1-row horizontal:
                                    (a) actor liability | (b) gap severity
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE      = Path(__file__).resolve().parent.parent
CHARTS    = BASE / "diagrams" / "charts"
GOVCHARTS = BASE / "diagrams" / "charts_gov"
OUT       = BASE / "diagrams" / "paper_figures"
OUT.mkdir(parents=True, exist_ok=True)

BG = (250, 250, 250)

# ── helpers ──────────────────────────────────────────────────────────────────

def load(path: Path, target_h: int) -> Image.Image:
    """Resize proportionally so height == target_h."""
    img = Image.open(path).convert("RGB")
    w, h = img.size
    new_w = int(w * target_h / h)
    return img.resize((new_w, target_h), Image.LANCZOS)

def load_w(path: Path, target_w: int) -> Image.Image:
    """Resize proportionally so width == target_w."""
    img = Image.open(path).convert("RGB")
    w, h = img.size
    new_h = int(h * target_w / w)
    return img.resize((target_w, new_h), Image.LANCZOS)

def add_label(img: Image.Image, label: str, size: int = 44) -> Image.Image:
    """Paint a panel label at top-left with white halo."""
    img = img.copy()
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", size)
    except (IOError, OSError):
        font = ImageFont.load_default()
    x, y = 16, 12
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        draw.text((x+dx, y+dy), label, fill=(255,255,255), font=font)
    draw.text((x, y), label, fill=(15, 15, 15), font=font)
    return img

def hstack(imgs, gap=20):
    total_w = sum(i.width for i in imgs) + gap*(len(imgs)-1)
    max_h   = max(i.height for i in imgs)
    c = Image.new("RGB", (total_w, max_h), BG)
    x = 0
    for im in imgs:
        c.paste(im, (x, (max_h - im.height)//2))
        x += im.width + gap
    return c

def vstack(imgs, gap=24):
    max_w   = max(i.width for i in imgs)
    total_h = sum(i.height for i in imgs) + gap*(len(imgs)-1)
    c = Image.new("RGB", (max_w, total_h), BG)
    y = 0
    for im in imgs:
        c.paste(im, ((max_w - im.width)//2, y))
        y += im.height + gap
    return c

def pad_width(img, target_w):
    """Centre-pad image to target_w with BG colour."""
    if img.width >= target_w:
        return img
    c = Image.new("RGB", (target_w, img.height), BG)
    c.paste(img, ((target_w - img.width)//2, 0))
    return c

# ── Figure A: Experimental track ─────────────────────────────────────────────
# All 3 panels side by side in one row so aspect ratio stays wide,
# letting width=\textwidth drive the scale (not height).  Higher target
# height means more pixels per panel => bigger text on page.

ROW_H = 720   # px height for every panel

h1_img = add_label(load(CHARTS / "fig02_h1_condition.png", ROW_H), "(a)")
h3_img = add_label(load(CHARTS / "fig04_h3_gradient.png",  ROW_H), "(b)")
h5_img = add_label(load(CHARTS / "fig06_h5_origin.png",    ROW_H), "(c)")

fig_A = hstack([h1_img, h3_img, h5_img], gap=22)
fig_A.save(OUT / "fig_paper_A_experimental.png", dpi=(300, 300))
print(f"fig_paper_A_experimental.png  → {fig_A.size[0]}×{fig_A.size[1]} px")

# ── Figure B: Regulatory track (dual-model governance coverage heatmaps) ─────
# MiniLM heatmap | E5 heatmap — side by side; same height normalisation.
# Replaces actor-liability+gap-severity panels; actor data is already in
# Table III, and the heatmaps communicate the 31-concept × 8-instrument
# coverage matrix more directly.

REG_H = 720

minilm = add_label(load(GOVCHARTS / "fig_gov03_minilm_heatmap.png", REG_H), "(a)")
e5     = add_label(load(GOVCHARTS / "fig_gov04_e5_heatmap.png",     REG_H), "(b)")

fig_B = hstack([minilm, e5], gap=28)
fig_B.save(OUT / "fig_paper_B_regulatory.png", dpi=(300, 300))
print(f"fig_paper_B_regulatory.png    → {fig_B.size[0]}×{fig_B.size[1]} px")

print("Done — output in diagrams/paper_figures/")

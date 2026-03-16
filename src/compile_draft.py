"""
compile_draft.py
----------------
Compiles all chapter draft files from draft/md/ into a single
full-script_vXXX.md file in draft/md/, where XXX is an auto-incremented
version number padded to 3 digits (001, 002, ...).

Usage:
    python src/compile_draft.py
"""

import re
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
DRAFT_DIR = Path(__file__).resolve().parent.parent / "draft" / "md"
OUTPUT_DIR = DRAFT_DIR

# Chapter files in canonical order (explicit list to avoid spurious matches)
CHAPTER_FILES = [
    "01-abstract.md",
    "02-introduction.md",
    "03-literature-review.md",
    "04-theoretical-framework.md",
    "05-methodology.md",
    "06-results.md",
    "07-discussion.md",
    "08-conclusion.md",
    "09-references.md",
]


# ── Version resolution ─────────────────────────────────────────────────────────
def next_version(output_dir: Path) -> int:
    """Return the next compilation version number (1-based)."""
    pattern = re.compile(r"^full-script_v(\d{3})\.md$", re.IGNORECASE)
    existing = [
        int(m.group(1))
        for f in output_dir.iterdir()
        if (m := pattern.match(f.name))
    ]
    return max(existing, default=0) + 1


# ── Main compilation ───────────────────────────────────────────────────────────
def compile_draft() -> Path:
    version = next_version(OUTPUT_DIR)
    version_str = f"{version:03d}"
    output_path = OUTPUT_DIR / f"full-script_v{version_str}.md"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parts: list[str] = []

    # ── Cover banner ──────────────────────────────────────────────────────────
    parts.append(
        f"<!-- COMPILED DRAFT — v{version_str} — {timestamp} -->\n"
        f"<!-- Source: {DRAFT_DIR} -->\n"
        f"<!-- Chapters: {', '.join(CHAPTER_FILES)} -->\n"
    )

    # ── Chapter contents ──────────────────────────────────────────────────────
    for filename in CHAPTER_FILES:
        filepath = DRAFT_DIR / filename
        if not filepath.exists():
            print(f"  [WARN] Missing chapter file: {filename} — skipped.")
            continue

        content = filepath.read_text(encoding="utf-8").strip()

        # Separator between chapters
        parts.append(
            f"\n\n---\n\n"  # horizontal rule between chapters
            + content
        )

    # ── Trailing newline ──────────────────────────────────────────────────────
    parts.append("\n")

    # ── Write output ──────────────────────────────────────────────────────────
    output_path.write_text("\n".join(parts), encoding="utf-8")

    print(f"  [OK] Compiled {len(CHAPTER_FILES)} chapters → {output_path.name}")
    print(f"       Version : v{version_str}")
    print(f"       Size    : {output_path.stat().st_size:,} bytes")
    print(f"       Path    : {output_path}")
    return output_path


if __name__ == "__main__":
    compile_draft()

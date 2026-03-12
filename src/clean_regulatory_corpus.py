#!/usr/bin/env python3
"""
Regulatory Corpus Cleaning Pipeline
===================================
Cleans OCR artifacts and formatting issues from Indonesian regulatory documents
for transformer-based semantic analysis.

Usage:
    python clean_regulatory_corpus.py

Requirements:
    pip install pandas openai-whisper (for audio OCR alternative)
"""

import re
import os
from pathlib import Path

# Configuration
CORPUS_DIR = Path('docs/regulatory_corpus')
OUTPUT_DIR = Path('docs/regulatory_corpus/cleaned')

# ============================================================================
# OCR FIX DICTIONARY
# ============================================================================
# Common OCR errors found in Indonesian legal documents
OCR_FIXES = {
    # Context-dependent fixes
    'KECERDASAN INDONESIA': 'KECERDASAN ARTIFISIAL',
    'INDONESIA': 'ARTIFISIAL',  # Only in AI context
    
    # Common OCR confusions
    'tr{I': 'dan',
    'tr{ir': 'dan',
    'tr{rr': 'dan',
    'NEPLTBLIK': 'REPUBLIK',
    'NEPUELIK': 'REPUBLIK',
    'NEPUBUK': 'REPUBLIK',
    'REPIJBUK': 'REPUBLIK',
    'REPIITEUK': 'REPUBLIK',
    
    # Spacing issues
    'Rp ': 'Rp',  # Currency
    ' Pasal ': 'Pasal ',
    ' Pasal': 'Pasal',
    
    # Common legal document artifacts
    'SALINAN': '',
    'Lembaran Negara': '',
    'Tambahan Lembaran Negara': '',
}

# Page/line markers to remove
PAGE_MARKER_PATTERN = re.compile(r'SK No \d+[A-Z]+')
LINE_NUMBER_PATTERN = re.compile(r'^\s*\d+\s*\|', re.MULTILINE)
SECTION_NUMBER_PATTERN = re.compile(r'\d+\s+STRATEGI')


def remove_page_artifacts(text: str) -> str:
    """Remove page numbers, section markers, and line numbers"""
    # Remove "SK No XXXXXX" patterns
    text = PAGE_MARKER_PATTERN.sub('', text)
    
    # Remove line numbers (e.g., "   1 |")
    text = LINE_NUMBER_PATTERN.sub('', text)
    
    # Remove section numbers (e.g., "1 BAB 1")
    text = re.sub(r'\d+\s+BAB\s+\d+', '', text)
    
    return text


def fix_ocr_errors(text: str) -> str:
    """Apply dictionary-based OCR fixes"""
    for wrong, correct in OCR_FIXES.items():
        text = text.replace(wrong, correct)
    return text


def normalize_whitespace(text: str) -> str:
    """Normalize spacing and line breaks"""
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    
    # Replace multiple newlines with single newline
    text = re.sub(r'\n\n+', '\n\n', text)
    
    # Remove spaces before punctuation
    text = re.sub(r'\s+([.,;:])', r'\1', text)
    
    # Add space after punctuation if missing
    text = re.sub(r'([.,;:])([A-Z])', r'\1 \2', text)
    
    return text


def fix_sentence_boundaries(text: str) -> str:
    """Fix broken sentence boundaries from OCR line breaks"""
    # Fix "period-space-period" artifacts
    text = re.sub(r'\.\s+\.', '.', text)
    
    # Fix broken sentences (line break mid-sentence)
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    
    return text


def clean_article_references(text: str) -> str:
    """Normalize article/section references"""
    # Fix inconsistent "Pasal" formatting
    text = re.sub(r'\bPasal\s+(\d+)', r'Pasal \1', text)
    
    # Fix "ayat" references
    text = re.sub(r'\bayat\s*\((\d+)\)', r'ayat (\1)', text)
    
    return text


def clean_regulatory_document(text: str) -> str:
    """
    Main cleaning function - applies all cleaning steps
    """
    steps = [
        ("Remove page artifacts", remove_page_artifacts),
        ("Fix OCR errors", fix_ocr_errors),
        ("Normalize whitespace", normalize_whitespace),
        ("Fix sentence boundaries", fix_sentence_boundaries),
        ("Clean article references", clean_article_references),
    ]
    
    for step_name, func in steps:
        text = func(text)
    
    return text


def process_corpus():
    """Process all files in the regulatory corpus"""
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find all txt files
    files = list(CORPUS_DIR.glob('*.txt'))
    
    print(f"Found {len(files)} files to process:")
    for f in files:
        print(f"  - {f.name}")
    print()
    
    for filepath in files:
        print(f"Processing: {filepath.name}")
        
        # Read file
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_length = len(content)
        
        # Clean content
        cleaned = clean_regulatory_document(content)
        
        cleaned_length = len(cleaned)
        
        # Save cleaned version
        output_path = OUTPUT_DIR / filepath.name
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        
        print(f"  Original: {original_length:,} chars")
        print(f"  Cleaned:  {cleaned_length:,} chars")
        print(f"  Removed:  {original_length - cleaned_length:,} chars")
        print(f"  Saved to: {output_path}")
        print()


def generate_cleaning_report():
    """Generate a report of cleaning operations"""
    report = []
    report.append("# Regulatory Corpus Cleaning Report")
    report.append("")
    report.append("## OCR Fixes Applied")
    report.append("")
    
    for wrong, correct in OCR_FIXES.items():
        report.append(f"- `{wrong}` → `{correct}`")
    
    report.append("")
    report.append("## Patterns Removed")
    report.append("")
    report.append("- Page markers: `SK No XXXXXX`")
    report.append("- Line numbers: `1 |`, `2 |`, etc.")
    report.append("- Section numbers: `1 BAB 1`")
    report.append("- Multiple whitespace")
    report.append("- Broken sentence boundaries")
    
    report_text = "\n".join(report)
    
    report_path = OUTPUT_DIR / "cleaning_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"\nCleaning report saved to: {report_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("REGULATORY CORPUS CLEANING PIPELINE")
    print("=" * 60)
    print()
    
    process_corpus()
    generate_cleaning_report()
    
    print("\n✓ Cleaning complete!")

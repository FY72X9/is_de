import pdfplumber
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import config

def convert_pdf_to_text(pdf_path, output_path):
    """Convert a single PDF to text."""
    print(f"Converting {pdf_path}...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Saved to {output_path}")
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")

def main():
    pdf_dir = config.DOCS_DIR / "pdf"
    txt_dir = config.DOCS_DIR / "regulatory_corpus"

    if not pdf_dir.exists():
        print(f"Directory {pdf_dir} does not exist.")
        return

    for pdf_file in pdf_dir.glob("*.pdf"):
        # Create output filename
        txt_filename = pdf_file.stem + ".txt"
        txt_path = txt_dir / txt_filename

        convert_pdf_to_text(pdf_file, txt_path)

if __name__ == "__main__":
    main()

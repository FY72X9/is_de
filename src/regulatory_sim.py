import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import config

# Simulated text excerpts

STRANAS_KA = """
STRATEGI NASIONAL PENGEMBANGAN ARTIFICIAL INTELLIGENCE 2020-2045
...
3. Pengamanan dan Keamanan
Pengembangan AI harus memperhatikan aspek keamanan data dan privasi pengguna.
Pemanfaatan AI secara bertanggung jawab harus memastikan tidak adanya diskriminasi...
...
"""

UU_PDP = """
UNDANG-UNDANG REPUBLIK INDONESIA NOMOR 27 TAHUN 2022
TENTANG PERLINDUNGAN DATA PRIBADI
...
Pasal 16
(1) Pengendali Data Pribadi wajib memastikan...
(2) Pengendali Data Pribadi wajib menerapkan...
"""

UU_ITE = """
UNDANG-UNDANG REPUBLIK INDONESIA NOMOR 11 TAHUN 2008
TENTANG INFORMASI DAN TRANSAKSI ELEKTRONIK
...
Pasal 27
(1) Setiap Orang dengan sengaja dan tanpa hak mendistribusikan dan/atau mentransmisikan...
"""

def save_corpus():
    """Save the simulated regulatory text to files."""
    docs_dir = config.DOCS_DIR / "regulatory_corpus"
    docs_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "Stranas_KA_2020-2045.txt": STRANAS_KA,
        "UU_PDP_27_2022.txt": UU_PDP,
        "UU_ITE_11_2008.txt": UU_ITE
    }

    for filename, content in files.items():
        with open(docs_dir / filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved {filename}")

if __name__ == "__main__":
    save_corpus()

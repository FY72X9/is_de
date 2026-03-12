# Regulatory Corpus Cleaning Report

## OCR Fixes Applied

- `KECERDASAN INDONESIA` → `KECERDASAN ARTIFISIAL`
- `INDONESIA` → `ARTIFISIAL`
- `tr{I` → `dan`
- `tr{ir` → `dan`
- `tr{rr` → `dan`
- `NEPLTBLIK` → `REPUBLIK`
- `NEPUELIK` → `REPUBLIK`
- `NEPUBUK` → `REPUBLIK`
- `REPIJBUK` → `REPUBLIK`
- `REPIITEUK` → `REPUBLIK`
- `Rp ` → `Rp`
- ` Pasal ` → `Pasal `
- ` Pasal` → `Pasal`
- `SALINAN` → ``
- `Lembaran Negara` → ``
- `Tambahan Lembaran Negara` → ``

## Patterns Removed

- Page markers: `SK No XXXXXX`
- Line numbers: `1 |`, `2 |`, etc.
- Section numbers: `1 BAB 1`
- Multiple whitespace
- Broken sentence boundaries
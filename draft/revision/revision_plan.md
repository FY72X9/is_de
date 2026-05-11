# ICIMTech 2026 — Revision Plan
**Paper**: Measuring Artificial Intelligence Safety Degradation and Regulatory Gaps in Indonesian Application-Layer Deployments  
**File**: `draft/latex/icimtech2026_revision.tex`  
**Status**: Post-review revision  
**Last updated**: 2026-05-11

---

## Execution Plan: 6 Sessions

| Session | Focus | Items | Rationale |
|---------|-------|-------|-----------|
| **Session 1** | Mechanical / factual fixes | K1, F1, F2, F4, F5, S1, S2 | Word-level changes, zero ambiguity, verifiable immediately |
| **Session 2** | Methodology transparency — Section IV | M1, M2, M4, M5 | All edits in the same section; no new data needed |
| **Session 3** | Construct, analytical argument, corpus evidence | M3, C1, C2, B1, B2 | Substantive rewrites; require careful framing to stay within 6-page limit |
| **Session 4** | Data verification + final QC | F3 + proofread | Depends on `data/raw/evaluated_responses.json` lookup |
| **Session 5** | Second-pass audit (11 items) | A1–A4, P1–P2, G1–G2, D1–D3 | Factual, grammar, style, and missing-argument fixes found in audit |
| **Session 6** | Residual reviewer gaps (3 items) | R6a, R6b, R6c | Items partially addressed in S1–S5 but not fully resolved |

---

## Todo List

### BLOK K — Minor Mandatory

| Code | Done | Todo | Technical Detail | Session |
|------|------|------|-----------------|---------|
| K1 | ☑ | Change "Index Terms" label → "Keywords" | Add `\renewcommand\IEEEkeywordsname{Keywords}` before `\begin{IEEEkeywords}` in `.tex` | 1 |

---

### BLOK F — Factual Errors

| Code | Done | Todo | Evidence | Session |
|------|------|------|----------|---------|
| F1 | ☑ | Fix "seven models" → "six models" in Abstract | Run_log: 3 US + 2 EU + 1 CN = 6 models only | 1 |
| F2 | ☑ | Fix "93,293" → "94,293" in Abstract, Section IV.D, and Conclusion | Post-cleaning sum from run_log = 94,293; paper off by exactly 1,000 (digit typo) | 1 |
| F3 | ☑ | Resolve C3 × Bahasa Indonesia compliance rate: 37.4% (H2 body) vs 37.6% (Abstract + para after Table II) | Requires lookup in `data/raw/evaluated_responses.json` for ground-truth value | 4 |
| F4 | ☑ | Fix "Table 1" → "Table~\ref{tab:actor}" in Discussion Section VI.A | Cross-reference points to deployment conditions table (Table I) instead of actor liability table (Table III) | 1 |
| F5 | ☑ | Fix typo "result yieds" → "result yields" in Section V.A (resolved via S1) | Reviewer 1, Comment 3; also fix surrounding grammatically broken sentence | 1 |

---

### BLOK S — Structural Inconsistencies

| Code | Done | Todo | Notes | Session |
|------|------|------|-------|---------|
| S1 | ☑ | Remove duplicate paragraph in Section V.A (H1); merge unique elements into one | Second paragraph is an unmerged draft remnant; removal frees ~5 lines for Methodology additions | 1 |
| S2 | ☑ | Reduce IEEEkeywords from 6 → 5 terms; remove "application programming interface" | Most generic term; already implicit in title and body | 1 |

---

### BLOK M — Methodology Transparency

| Code | Done | Todo | What Is Needed | Session |
|------|------|------|----------------|---------|
| M1 | ☑ | Add distribution of 893 observations per harm category and language in Section IV.A | 2–3 compact sentences + inline numbers; no new table (space constraint); data from `data/prompts/battery_v1.json` | 2 |
| M2 | ☑ | Clarify distinct roles of Qwen (primary evaluator) vs SeaLLMs (cross-validation) + conflict resolution rule in Section IV.B | Reorganize existing text; add 1 sentence on tiebreaker (binary logistic regression over raw scores) | 2 |
| M3 | ☑ | Add explicit citation for 40% ΔR threshold (H1) and 70% S% threshold (H3) in Section V | If threshold not literally in [b3]/[b18]: state as "preregistered decision threshold, following [b3]'s operationalization of systematic safety failure" | 3 |
| M4 | ☑ | Add scoring rubric transparency to Section IV.B: judge prompt structure, L1 vs L2 criteria, inter-judge agreement metric, Qwen floor truncation implication | ~3–4 additional sentences; use space freed by S1 | 2 |
| M5 | ☑ | Explain harm category origin (reference framework) + Bahasa Indonesia prompt construction in Section IV.A | 2–3 sentences; cite framework source (Weidinger [b27] / Röttger [b3] / custom); state whether BI prompts are translated or independently authored | 2 |

---

### BLOK C — Construct & Analytical Argument

| Code | Done | Todo | Corpus Evidence | Session |
|------|------|------|-----------------|---------|
| C1 | ☑ | Sharpen construct boundaries in Section III opening: state explicitly which dimensions are *directly demonstrated* vs *inferred* | Architectural + configurational: demonstrated by experimental data. Observational + temporal-domain: inferred from pattern + literature | 3 |
| C2 | ☑ | Replace rhetorical paragraph in Discussion VI.A with explicit 4-row deployment → actor → regulatory blind spot mapping table | Every row grounded in corpus: UU ITE technology-neutral; Etika KA defines actors but non-binding; Permenkes zero AI mentions; FMP = 0 liability mentions across 94,293 words | 3 |

**Proposed C2 table structure:**

| Deployment Condition | Primary Actor | Indonesian Regulatory Status |
|---------------------|---------------|------------------------------|
| C1 — Consumer Simulation | Application Provider / Penyelenggara Sistem KA | Etika KA Draft (non-binding) defines role; zero binding obligation instrument |
| C2 — Raw API Access | API Developer / Domestic Integrator | UU ITE covers "Penyelenggara SE" broadly; 5/8 instruments assign zero deployer obligations |
| C3 — Safety-Stripped | API Integrator (via system prompt config) | Zero instruments mandate minimum system prompt safety standard |
| All conditions | Foundation Model Provider | 0 liability-context mentions across all 8 instruments (94,293 words) |

---

### BLOK B — Argument Strengthening (Corpus-Grounded)

| Code | Done | Todo | Pasal Reference | Session |
|------|------|------|-----------------|---------|
| B1 | ☑ | Cite Etika KA Draft Bab VII/VIII in Discussion/R3: "Penyedia Sistem KA" already defined but non-binding — strengthens urgency of Policy Recommendation R3 | Etika KA Draft Bab VIII: explicit 4-actor taxonomy (Pengembang KA, Penyedia Sistem KA, Penyelenggara Sistem KA, Pengguna) without per-actor binding obligation | 3 |
| B2 | ☑ | Cite Permenkes Pasal 7 ayat 1 in H4 discussion: telemedicine *recognized* but AI inference layer *absent* — frame as precision gap, not total regulatory absence | Permenkes 24/2022 line 150: "menyelenggarakan pelayanan telemedisin" with zero mention of AI, chatbot, algoritma, or kecerdasan artifisial in entire document | 3 |

---

## Key Verified Facts (for reference during editing)

| Claim | Correct Value | Source |
|-------|--------------|--------|
| Total models tested | 6 (3 US, 2 EU, 1 CN) | `run_log_minilm.txt` |
| Total regulatory words (post-cleaning) | 94,293 | `run_log_minilm.txt` sum |
| Total regulatory words (raw) | 95,075 | Direct word count on corpus files |
| FMP liability mentions | 0 across all 8 instruments | `run_log_minilm.txt` actor liability table |
| API Developer liability mentions total | 20 (13 in UU ITE, 5 in Permenkes, 2 in Stranas KA) | `run_log_minilm.txt` |
| Permenkes 24/2022 AI-related terms | 0 mentions of: kecerdasan, artifisial, AI, chatbot, algoritma | Direct grep of corpus file |
| UU ITE 2024 AI-related terms | 0 — fully technology-neutral | Direct grep of corpus file |
| Etika KA actor taxonomy | Defines 4 sub-actors explicitly (Bab VIII) | Corpus file lines 259–290 |
| C3 harmful compliance rate | Conflict: Abstract=37.6%, H2 body=37.4% | Resolve from `evaluated_responses.json` in Session 4 |
| Critical regulatory gaps (dual-confirmed) | 2: Medical AI (Permenkes), Tax/Legal AI (no instrument) | Both MiniLM + E5 models agree |

---

---

## Session 5 — Second-Pass Audit Findings (post Session 1–4)

Ditemukan setelah audit menyeluruh terhadap full `.tex` + verifikasi data. Semua item di bawah belum ditangani.

### BLOK A2 — Factual Errors (ditemukan di audit kedua)

| Code | Done | Problem | Ground Truth | Priority |
|------|------|---------|--------------|----------|
| A1 | ☑ | TikZ node (line 125): `93{,}293 words` | → `94{,}293` (F2 batch hanya fix 3 lokasi, TikZ terlewat) | Critical |
| A2 | ☑ | Discussion VI.A (line 406): `"resulting in 36.0% in harmful compliance"` | → **36.4%** (dari Table II C3 Comply%) | Critical |
| A3 | ☑ | Abstract (line 43): `"maps 18 AI safety concepts"` | → **16** (run_log: "API-specific concepts: 16"; 18 tidak ada di data manapun) | Critical |
| A4 | ☑ | Discussion VI.B: `"Binary invariance is identical at 69.1%"` | → **68.8%** (dari clean dataset N=893; 69.1% dari intermediate run N=902) | High |

### BLOK B2 — Missing Content (dari reviewer feedback, belum dijawab)

| Code | Done | Problem | Action |
|------|------|---------|--------|
| P1 | ☑ | R2.3 partial unanswered: tidak ada kalimat tentang human validation / pilot calibration | Tambah 1 kalimat di IV.B: no human validation conducted; binary cross-check (68.8% agreement) serves as inter-rater proxy | High |
| P2 | ☑ | Argumen "partial support ≠ null result" hilang dari Discussion VI.A (terhapus saat C2 table ditambah Session 3) | Tambah 2 kalimat setelah table: thresholds derived from red-teaming; effects reproducible + policy-actionable | High |

### BLOK G — Grammar / Prose Broken

| Code | Done | Problem | Fix |
|------|------|---------|-----|
| G1 | ☑ | H2 body: `"Though, this is cultural calibration of judges is Southeast Asian vs Chinese/English"` — double "is", broken syntax | Rewrite: `"This divergence reflects cultural calibration: Qwen-3B applies Chinese/English refusal norms; SeaLLMs-7B applies Southeast Asian discourse norms."` |
| G2 | ☑ | Background II.D: frasa `"provides the vocabulary for understanding the regulatory gaps identified in this work"` muncul **verbatim dua kali** berturutan | Hapus kalimat kedua (Diver) atau merge menjadi satu kalimat |

### BLOK D — Style / Redundancy / Minor

| Code | Done | Problem | Fix |
|------|------|---------|-----|
| D1 | ☑ | IV.A: `"Table 1 (Table~\ref{tab:conditions})"` — "Table 1" redundant dengan cross-reference | Hapus "Table 1 " → hanya `(Table~\ref{tab:conditions})` |
| D2 | ☑ | IV.D: `"four actor types: Foundation Model Provider, API Developer, End User, Government)"` — missing opening parenthesis | Tambah `(` sebelum "Foundation" atau hapus `)` |
| D3 | ☑ | Introduction ¶2: `"a quantification yet to be conducted in the context of Indonesia but not the focus of this research"` — self-contradictory (paper ini justru mengkuantifikasi hal tersebut) | Rewrite: hapus "but not the focus of this research" atau restructure |

### BLOK I — Image (scope terpisah)

| Code | Done | Problem | Action |
|------|------|---------|--------|
| I1 | ☑ | R1.4: Font dalam subplot `fig_paper_A_experimental.png` terlalu kecil | global `font.size` 10→13, dpi 150→200, figsize fig02/fig06 (12,5)→(14,6), fig04 (9,6)→(11,7), ROW_H 720→900; semua explicit fontsize di fig02/fig04/fig06 dinaikkan ~25%; regenerasi via `python src/generate_charts.py` + `compose_paper_figures.py` |

---

## Session 6 — Residual Reviewer Gaps (post Session 1–5)

Ditemukan dari cross-check sistematis antara reviewer feedback vs versi revision terkini. Tiga item ini **sebagian** dijawab di session sebelumnya tetapi tidak secara eksplisit atau tidak dengan angka yang benar.

### BLOK R6 — Reviewer Gap Residual

| Code | Done | Reviewer | Problem | Fix Applied | Ground Truth |
|------|------|----------|---------|-------------|--------------|
| R6a | ☑ | R1.1 | EN vs BI observation count tidak pernah disebutkan numerik | Tambah di IV.A: "521 (58.3%) Bahasa Indonesia dan 372 (41.7%) English" | Dari `evaluated_responses_clean.json`: BI=521, EN=372 |
| R6b | ☑ | R1.1 | Sampling bias (unequal model counts) tidak diakui sebagai limitation H5 | Extend kalimat "not a stratified sampling design" → tambah "EU-origin H5 finding therefore rests on two models only; interpret as exploratory" | US: 3 model, EU: 2 model, CN: 1 model |
| R6c | ☑ | R2.4 | BI prompt authorship method tidak dijelaskan (terjemahan atau authored independently?) | Tambah di IV.A: "Bahasa Indonesia versions translated directly from English source prompts" (8 BI-only categories authored independently) | Dari `battery_v1.json`: R1_EN/R1_ID paired → translations; 8 BI-only categories confirmed |

**Verified from:** `data/processed/evaluated_responses_clean.json` (language counts) + `data/prompts/battery_v1.json` (prompt authorship structure).

---

## Space Budget (6-page constraint)

| Action | Space Change |
|--------|-------------|
| S1: Remove duplicate H1 paragraph | **−5 lines** |
| S2: Remove 1 keyword | −1 line |
| C2: Replace rhetorical paragraph with table | ≈ neutral (table ≈ paragraph size) |
| M4 + M2: Methodology additions | +4–5 lines |
| M1 + M5: Protocol additions | +3–4 lines |
| C1 + B1 + B2: Inline additions | +3–4 lines |
| **Net** | **≈ +4–8 lines above current** |

> If net addition exceeds 6-page limit after Session 2, trim Discussion VI.A rhetorical paragraph (target of C2) first before any other cut.

---

## Session C1 — Word Compression (~205 kata, 1 prompt)

**Trigger**: Paper humanized oleh user → masih ~200 kata di atas 6-page limit.  
**Execution**: 1 prompt (single `multi_replace_string_in_file` batch, 10 edits sekaligus).  
**Status**: 🔲 Pending

| Code | Done | Location | Problem | Estimated Saving |
|------|------|----------|---------|-----------------|
| C-1 | ☑ | Section III — 4 dimensions | "is concerned with the process of" × 4 → "captures / addresses" | ~35 kata |
| C-2 | ☑ | Conclusion ¶1 — First/Second/Third | 3 poin bernomor → 1 kalimat convergence | ~30 kata |
| C-3 | ☑ | IV.A — sampling caveat | Angka per-origin counts diulang → "These per-origin counts..." | ~15 kata |
| C-4 | ☑ | H2 Results — methodological finding | 2 kalimat → 1 kalimat "requiring a gold standard to resolve directionally" | ~5 kata |
| C-5 | ☑ | Background II.A | "have shown that... This motivates" → "show that..., motivating" | ~8 kata |
| C-6 | ☑ | Background II.B | "have demonstrated that... which permits" → "show that..., enabling" | ~10 kata |
| C-6b | ☑ | Background II.C | "have demonstrated the effectiveness in Indonesian... which is attributed to the use of" → "report Indonesian safety... attributed to" | ~9 kata |
| C-7 | ☑ | IV.B — 68.8% disebut 2x | "the 68.8\% binary inter-judge agreement" → "this figure" | ~4 kata |
| C-8 | ☑ | IV.B — transition sentence removed | "The study also used architecturally different evaluation frameworks to evaluate each response:" → dihapus | ~12 kata |
| C-9 | ☑ | H3 Results — typo + redundansi | "Both evaluators report... The Kruskal-Wallis test results are Qwen: Qwen" → 1 kalimat, typo fixed | ~6 kata |
| C-10 | ☑ | Discussion VI.A — dua kalimat pembuka | Lebur menjadi 1 kalimat | ~11 kata |
| C-11 | ☑ | Policy R1 | "This reform is significant, with an odds ratio of 0.543, p=0.0008." → dihapus | ~12 kata |
| **C-11b** | ☑ | **Policy R4 — factual fix** | **"two of three critical gaps" → "both critical gaps"** + "Annexes on sectoral regulations" → "Sectoral annexes" | **factual fix + ~3 kata** |
| C-12 | ☑ | Conclusion — future work | "The study's results should be extended to include..." → "Future work should..." | ~20 kata |

**Total aktual: ~200 kata — ☑ Selesai.**

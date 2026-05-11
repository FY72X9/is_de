# ICIMTech 2026 — Revision Plan
**Paper**: Measuring Artificial Intelligence Safety Degradation and Regulatory Gaps in Indonesian Application-Layer Deployments  
**File**: `draft/latex/icimtech2026_revision.tex`  
**Status**: Post-review revision  
**Last updated**: 2026-05-11

---

## Execution Plan: 4 Sessions

| Session | Focus | Items | Rationale |
|---------|-------|-------|-----------|
| **Session 1** | Mechanical / factual fixes | K1, F1, F2, F4, F5, S1, S2 | Word-level changes, zero ambiguity, verifiable immediately |
| **Session 2** | Methodology transparency — Section IV | M1, M2, M4, M5 | All edits in the same section; no new data needed |
| **Session 3** | Construct, analytical argument, corpus evidence | M3, C1, C2, B1, B2 | Substantive rewrites; require careful framing to stay within 6-page limit |
| **Session 4** | Data verification + final QC | F3 + proofread | Depends on `data/raw/evaluated_responses.json` lookup |

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
| F3 | ☐ | Resolve C3 × Bahasa Indonesia compliance rate: 37.4% (H2 body) vs 37.6% (Abstract + para after Table II) | Requires lookup in `data/raw/evaluated_responses.json` for ground-truth value | 4 |
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
| M1 | ☐ | Add distribution of 893 observations per harm category and language in Section IV.A | 2–3 compact sentences + inline numbers; no new table (space constraint); data from `data/prompts/battery_v1.json` | 2 |
| M2 | ☐ | Clarify distinct roles of Qwen (primary evaluator) vs SeaLLMs (cross-validation) + conflict resolution rule in Section IV.B | Reorganize existing text; add 1 sentence on tiebreaker (binary logistic regression over raw scores) | 2 |
| M3 | ☐ | Add explicit citation for 40% ΔR threshold (H1) and 70% S% threshold (H3) in Section V | If threshold not literally in [b3]/[b18]: state as "preregistered decision threshold, following [b3]'s operationalization of systematic safety failure" | 3 |
| M4 | ☐ | Add scoring rubric transparency to Section IV.B: judge prompt structure, L1 vs L2 criteria, inter-judge agreement metric, Qwen floor truncation implication | ~3–4 additional sentences; use space freed by S1 | 2 |
| M5 | ☐ | Explain harm category origin (reference framework) + Bahasa Indonesia prompt construction in Section IV.A | 2–3 sentences; cite framework source (Weidinger [b27] / Röttger [b3] / custom); state whether BI prompts are translated or independently authored | 2 |

---

### BLOK C — Construct & Analytical Argument

| Code | Done | Todo | Corpus Evidence | Session |
|------|------|------|-----------------|---------|
| C1 | ☐ | Sharpen construct boundaries in Section III opening: state explicitly which dimensions are *directly demonstrated* vs *inferred* | Architectural + configurational: demonstrated by experimental data. Observational + temporal-domain: inferred from pattern + literature | 3 |
| C2 | ☐ | Replace rhetorical paragraph in Discussion VI.A with explicit 4-row deployment → actor → regulatory blind spot mapping table | Every row grounded in corpus: UU ITE technology-neutral; Etika KA defines actors but non-binding; Permenkes zero AI mentions; FMP = 0 liability mentions across 94,293 words | 3 |

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
| B1 | ☐ | Cite Etika KA Draft Bab VII/VIII in Discussion/R3: "Penyedia Sistem KA" already defined but non-binding — strengthens urgency of Policy Recommendation R3 | Etika KA Draft Bab VIII: explicit 4-actor taxonomy (Pengembang KA, Penyedia Sistem KA, Penyelenggara Sistem KA, Pengguna) without per-actor binding obligation | 3 |
| B2 | ☐ | Cite Permenkes Pasal 7 ayat 1 in H4 discussion: telemedicine *recognized* but AI inference layer *absent* — frame as precision gap, not total regulatory absence | Permenkes 24/2022 line 150: "menyelenggarakan pelayanan telemedisin" with zero mention of AI, chatbot, algoritma, or kecerdasan artifisial in entire document | 3 |

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

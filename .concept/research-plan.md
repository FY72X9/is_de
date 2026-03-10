# Research Execution Plan: API-Mediated AI Safety Asymmetry in Indonesia

This document details the step-by-step execution strategy for the research project defined in [`research-concept.md`](research-concept.md) and [`reenhance-concept.md`](reenhance-concept.md).

## 1. Pre-Execution Setup

### 1.1 Environment & Dependencies
*   **Language:** Python 3.10+ (Anaconda recommended)
*   **Core Libraries:**
    *   `requests`: For API calls to OpenRouter.
    *   `pandas`: For data handling and statistical analysis.
    *   `scikit-learn`: For statistical modeling (if needed beyond scipy).
    *   `scipy`: For ANOVA and t-tests.
    *   `matplotlib` / `seaborn`: For visualization (heatmaps, bar charts).
*   **Infrastructure:**
    *   OpenRouter Account (Free Tier).
    *   VPN/Proxy service (Indonesian IP) - *Optional, depending on testing strategy.*
    *   Version Control: Git.

### 1.2 Directory Structure
```text
.
├── src/
│   ├── __init__.py
│   ├── config.py           # API keys and constants
│   ├── prompt_loader.py    # Loads and structures the prompt battery
│   ├── api_client.py       # Wrapper for OpenRouter API calls
│   ├── evaluator.py        # Automated scoring logic
│   └── main.py             # Orchestration script
├── data/
│   ├── prompts/
│   │   └── battery_v1.json # The synthetic prompt dataset
│   ├── raw/
│   │   └── api_responses.jsonl
│   └── processed/
│       └── analyzed_data.csv
├── docs/
│   ├── regulatory_corpus/  # PDFs/Text of Stranas KA, UU PDP, etc.
│   └── coding_scheme.pdf
├── notebooks/
│   └── analysis.ipynb       # Jupyter notebook for stats
├── logs/
│   └── execution.log
└── README.md
```

---

## 2. Phase 1: Infrastructure Development (Weeks 1-2)

### Step 1.1: OpenRouter Integration
*   **Objective:** Establish a stable connection to the API without manual intervention.
*   **Action:**
    1.  Sign up for OpenRouter and obtain the API key.
    2.  Write `src/api_client.py` to handle authentication headers (`Authorization: Bearer <KEY>`).
    3.  Implement a simple test script to query a free model (e.g., `meta-llama/llama-3-8b-instruct`) and verify response format.
*   **Validation:** Ensure the script can handle rate limit errors (HTTP 429) gracefully (e.g., exponential backoff).

### Step 1.2: Prompt Battery Construction
*   **Objective:** Create the `battery_v1.json` structured dataset.
*   **Action:**
    1.  Populate the prompt battery based on the categories defined in the concept:
        *   *Uji Penolakan Dasar* (Basic Refusal) - English & Bahasa Indonesia.
        *   *Uji Konteks Lokal* (Local Context) - Indonesian specific harms.
    2.  Structure the JSON with fields: `id`, `intent_category`, `language`, `prompt_text_en`, `prompt_text_id`.
    3.  Store in `data/prompts/`.
*   **Validation:** Manual review by a native Indonesian speaker to ensure prompts are semantically equivalent and correctly categorized.

### Step 1.3: Execution Loop
*   **Objective:** Automate the process of loading prompts -> calling API -> saving raw output.
*   **Action:**
    1.  Implement `src/main.py` to iterate through `battery_v1.json`.
    2.  Implement the **Three Conditions** logic:
        *   **Condition A:** Inject the "Robust System Prompt" (Safety Scaffolding).
        *   **Condition B:** Inject the "Neutral System Prompt" (Default API).
        *   **Condition C:** Inject the "Permissive System Prompt" (Adversarial).
    3.  Log every API call (timestamp, model, prompt hash, response tokens) to `data/raw/`.
*   **Validation:** Run a pilot test (n=10 prompts) to ensure the loop functions correctly and data is saved as JSONL.

---

## 3. Phase 2: Data Collection (Weeks 3-5)

### Step 3.1: Full-Scale Testing
*   **Objective:** Execute the full prompt battery across all models and conditions.
*   **Strategy:**
    *   Target Models: `meta-llama/llama-3-8b-instruct`, `qwen/qwen-2.5-7b-instruct`, `mistralai/mistral-7b-instruct-v0.3`.
    *   Limit: Stay within free-tier limits (approx. 200-500 requests/day depending on load).
*   **Monitoring:** Check `execution.log` daily for failures.
*   **Backup:** If API access is throttled, switch to a secondary free-tier model (e.g., `google/gemma-2-9b-it`) to maintain sample size.

### Step 3.2: Regulatory Corpus Compilation
*   **Objective:** Gather official documents for qualitative analysis.
*   **Action:**
    1.  Download PDFs of *Stranas KA*, *UU PDP*, and *UU ITE*.
    2.  Convert PDF text to raw `.txt` files for analysis.
    3.  Store in `docs/regulatory_corpus/`.
*   **Validation:** Ensure text is machine-readable (OCR if necessary).

---

## 4. Phase 3: Analysis & Synthesis (Weeks 6-8)

### Step 4.1: Quantitative Safety Scoring
*   **Objective:** Translate raw API outputs into quantifiable safety scores (0-3).
*   **Action:**
    1.  Load `api_responses.jsonl` into a Pandas DataFrame.
    2.  Implement a classification heuristic in `src/evaluator.py`:
        *   *Keyword Matching:* "I cannot help with that" (Refusal).
        *   *Length Check:* Zero tokens (Failure).
        *   *Content Check:* Presence of specific harmful keywords (if feasible).
    3.  **Manual Coding (Gold Standard):** Randomly sample 20% of outputs for manual human coding to validate the heuristic. Calculate Inter-Rater Reliability (Cohen's Kappa).
*   **Tool:** `notebooks/analysis.ipynb`.

### Step 4.2: Statistical Testing
*   **Objective:** Test H1, H2, and H3.
*   **Action:**
    *   **H1 (Architectural):** Chi-Square test on refusal rates (Condition A vs. B).
    *   **H2 (Linguistic):** T-test on refusal quality scores (English vs. Bahasa Indonesia).
    *   **H3 (Configurational):** ANOVA on refusal scores across Conditions A, B, and C.
*   **Visualization:** Generate bar charts comparing refusal rates across conditions and languages.

### Step 4.3: Regulatory Gap Mapping
*   **Objective:** Analyze the textual corpus.
*   **Action:**
    1.  Use simple frequency analysis or keyword search (Regex) to identify mentions of "API", "deployment", "developer", "security", and "safety".
    2.  Map these mentions to the coding scheme (from the concept: *API mention*, *Safety scope*, *Actor identification*).
    3.  Identify the "Zero Regulatory Coverage" gap (H4).
*   **Tool:** `docs/regulatory_corpus/` analysis or Python text analysis.

---

## 5. Phase 4: Dissemination (Weeks 9-10)

### Step 5.1: Code Release
*   **Action:**
    1.  Clean up `src/` code, remove API keys (use environment variables).
    2.  Create a `requirements.txt`.
    3.  Push to a public GitHub repository (MIT License).
    4.  Upload the `analyzed_data.csv` (sanitized) to the repository.

### Step 5.2: Manuscript Drafting
*   **Structure:**
    1.  **Introduction:** The adoption paradox in Indonesia (High adoption, Low safety scrutiny).
    2.  **Theoretical Framework:** Agency Theory & STS.
    3.  **Methodology:** Technical Empiricism (The "Probe" method).
    4.  **Findings:** Quantitative results (H1-H3) + Regulatory gaps.
    5.  **Discussion:** Implications for *Stranas KA*.
    6.  **Conclusion:** Call for API-specific governance.

---

## 6. Contingency Planning

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **API Key Exhaustion** | Medium | High | Switch to alternative free models; Apply for research grants for API credits. |
| **VPN/IP Blocking** | Low | Medium | Use residential proxies; Report "Geographic Simulation" as a limitation. |
| **Model Version Drift** | High | Low | Pin specific model versions in code; Document exact timestamps of API calls. |
| **Ethical Review Delay** | Medium | Medium | Draft the IRB exemption rationale early (no human subjects). |

---

## 7. Final Checklist

- [ ] `config.py` created with dummy API key placeholder.
- [ ] `prompt_battery.json` loaded with ≥50 distinct prompts.
- [ ] `main.py` executes loop without manual intervention.
- [ ] `data/raw/` populated with ≥500 API responses.
- [ ] Regulatory PDFs downloaded and converted.
- [ ] `analysis.ipynb` contains Chi-Square and ANOVA results.
- [ ] GitHub repository initialized and pushed.

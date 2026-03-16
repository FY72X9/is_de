# Abstract

**Title:** Configurable Compliance: Empirical Measurement of API-Mediated AI Safety Asymmetry in Indonesia Through LLM-as-a-Judge Ordinal Evaluation and Semantic Regulatory Gap Analysis

**Running Head:** API-Mediated AI Safety Asymmetry in Indonesia

---

## Abstract

Indonesia's AI adoption trajectory depends overwhelmingly on API-mediated deployment of global foundation models, yet no empirical study quantifies how safety properties degrade during this transition. This research executes a direct API testing protocol via OpenRouter infrastructure, generating 902 original observations across three deployment conditions — consumer simulation (C1), raw API (C2), and safety-stripped (C3) — for English and Bahasa Indonesia prompt batteries covering 28 harm-intent categories across seven foundation models from three geographic origins. A dual LLM-as-a-Judge ordinal scoring framework (0–3) operationalizes safety assessment: Qwen2.5-3B-Instruct serves as the primary judge and SeaLLMs-v3-7B-Chat as cross-validation, enabling semantic discrimination among robust refusal, partial guardrail, inadequate guardrail, and full compliance. Statistical analysis confirms three of five hypotheses: API configuration degrades safety significantly (Kruskal-Wallis H=16.57, p=0.0003; C3 binary OR=0.543, p=0.0008); architectural degradation from C1 to C2 is significant (Mann-Whitney U p=0.018); model geographic origin modulates safety (EU 73.5% > CN 72.1% > US 65.0%; EU vs. US p=0.041). Linguistic asymmetry achieves ordinal-level significance in the Proportional Odds Model (language_English OR=1.62, p<0.001), though evaluator divergence across judge architectures reveals this finding as instrument-dependent. The worst vulnerability cell — C3_STRIPPED combined with Bahasa Indonesia prompts — produces 37.4% harmful-content compliance. Parallel regulatory semantic analysis of all eight Indonesian governance instruments, employing `paraphrase-multilingual-MiniLM-L12-v2` and `intfloat/multilingual-e5-base` as independent evaluators across 31 AI safety concepts, reveals that Foundation Model Provider liability achieves zero mentions across the entire corpus and API deployer obligations are absent from five of eight instruments. Two sectors — medical AI and tax/legal AI — exhibit critical regulatory gaps with no instrument assigning inference-layer safety obligations. This study provides the first quantitative evidence of API safety asymmetry as a structurally unregulated phenomenon in Indonesia.

**Keywords:** API safety testing; LLM-as-a-Judge; Bahasa Indonesia AI safety; Proportional Odds Model; regulatory gap analysis

---

*Word count: 247*

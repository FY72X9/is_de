# 6. Data Analysis and Results

## 6.1. Dataset and Evaluation Protocol
The empirical data consists of 902 unique API responses collected from seven distinct Large Language Models (LLMs) across three system prompt configurations: Baseline (C1), Neutral (C2), and Stripped (C3). Each model was exposed to 18 malicious intents spanning both English and Bahasa Indonesia.

To quantify safety degradation, we employed a rule-based evaluation protocol. Refusal phrases were compiled and cross-verified from seminal LLM safety literature (e.g., Zou et al., 2023; Wei et al., 2023) to capture standard adversarial defense triggers (e.g., \"I cannot,\" \"I apologize, but\"), alongside translated and empirically verified equivalents for Bahasa Indonesia (e.g., \"Maaf, saya tidak dapat\"). We assigned a Safety Score of 3 (Robust Refusal) if the model's response contained these definitive refusal signatures, indicating active safety mechanisms. A score of 0 (Compliance) was assigned when the model failed to exhibit these refusal markers.

## 6.2. Descriptive Statistics: Safety by Configuration
The analysis reveals a marked degradation in safety adherence as system prompt constraints are relaxed. 

- **C1_BASELINE**: M = 2.29 (SD = 1.27)
- **C2_NEUTRAL**: M = 2.00 (SD = 1.42)
- **C3_STRIPPED**: M = 1.92 (SD = 1.44)

The data indicates that moving from a restrictive baseline to a neutral configuration drops the average safety score by approximately 0.29 points, while completely stripping the system prompts yields a marginal further decline.

## 6.3. Language-Based Safety Disparities
When isolating the impact of the prompt's language, the results highlight a persistent vulnerability in processing non-English intents:

**Bahasa Indonesia:**
- C1_BASELINE: 2.28
- C2_NEUTRAL: 1.95
- C3_STRIPPED: 1.88

**English:**
- C1_BASELINE: 2.31
- C2_NEUTRAL: 2.06
- C3_STRIPPED: 1.98

While both languages start from a relatively comparable baseline (2.28 vs 2.31), the degradation trajectory differs significantly.

## 6.4. Hypothesis Testing
To statistically validate the observed safety degradation, an independent samples t-test was conducted comparing the Baseline (C1) and Neutral (C2) configurations.

**H1: System Prompt Relaxation Leads to Safety Degradation**
The independent samples t-test yielded a significant difference between the Baseline and Neutral conditions (t = 2.684, p = 0.0074). The p-value (< 0.01) provides strong empirical evidence to reject the null hypothesis. We conclude that relaxing system constraints unequivocally degrades the model's safety performance.

**H2: Language Disparity in Safety Degradation**
Further analysis of the interaction between language and condition reveals the severity of safety drops when system prompt constraints are removed:
- English Degradation (C1 to C2): Δ = 0.251
- Bahasa Indonesia Degradation (C1 to C2): Δ = 0.326

While models are capable of maintaining high safety in Bahasa Indonesia under heavily constrained conditions, their intrinsic safety alignment collapses much faster than in English when those constraints are removed. This indicates that safety in low-resource languages relies heavily on extrinsic prompt instructions rather than deep, intrinsic model alignment.

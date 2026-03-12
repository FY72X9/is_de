# 7. Discussion and Implications

## 7.1. The Mechanics of Safety Degradation
The empirical results demonstrate a statistically significant degradation in LLM safety mechanisms when restrictive system prompts are removed (t = 2.684, p < 0.01). This finding fundamentally challenges the assumption that modern LLMs possess intrinsic, robust safety guardrails. Rather, it reveals that safety is heavily contingent on extrinsic, contextual framing—specifically, the overarching system prompt instructions. When a model operates in a \"Neutral\" or \"Stripped\" condition, its predictive algorithms prioritize compliance over safety, suggesting that foundational alignment (e.g., RLHF) is easily overridden by conversational context. This causal mechanism exposes a critical vulnerability: end-users can systematically bypass safety protocols simply by providing \"clean\" or non-restrictive system-level instructions in API environments.

## 7.2. The Multilingual Safety Gap: Fragility Beyond English
The analysis uncovers a nuanced but severe safety disparity between English and Bahasa Indonesia. While models exhibited comparable safety scores in the Baseline condition (English = 2.31, Bahasa Indonesia = 2.28), their behavior diverged sharply when system constraints were relaxed. Bahasa Indonesia experienced a much steeper degradation trajectory (Δ = 0.326) compared to English (Δ = 0.251).

This contradiction highlights a structural deficiency in global AI development. It indicates that while models can be explicitly instructed to be safe in non-English languages via rigid system prompts, their *intrinsic* safety alignment—the safety built into the core model weights—is disproportionately optimized for the English language. Safety filters lack the deep semantic nuance required to independently intercept harmful intents masked within local idioms or translated syntax once the explicit extrinsic instructions are removed. 

## 7.3. Alignment with Theoretical Predictions
These findings align closely with the \"Contextual Fragility\" theory in AI safety, which posits that guardrails are not rigid boundaries but probabilistic weights heavily influenced by immediate context. The data confirms the theoretical prediction that API endpoints, which grant developers full control over system prompts, create a significantly larger attack surface compared to consumer-facing chat interfaces. The results contradict the industry narrative of \"inherent safety,\" proving empirically that safety is a fragile, context-dependent state.

## 7.4. The Regulatory Blind Spot in Indonesia
The vulnerability of LLMs via API endpoints, coupled with their specific fragility in processing Bahasa Indonesia, creates a hazardous environment that current Indonesian law is ill-equipped to handle. Our regulatory corpus analysis revealed critically low keyword densities for terms like \"API\" and \"Developer\" across primary legal frameworks, including *Stranas KA 2045*, *UU Nomor 1 Tahun 2024*, and *UU Nomor 27 Tahun 2022*. 

Crucially, the analysis confirmed that there is absolutely no explicit mention of \"API\" or \"Application Programming Interface\" in the context of AI safety within these documents. This represents a profound regulatory blind spot. Lawmakers are currently regulating AI as a monolithic, consumer-facing product, completely ignoring the developer-side infrastructure where safety protocols are most easily bypassed.

## 7.5. Implications

### 7.5.1. Theoretical Implications
The study demands a reevaluation of current AI alignment theories. It necessitates a shift from \"extrinsic prompting\" models to \"intrinsic architectural safety,\" where ethical constraints are embedded deeper into the model's core weights across multiple languages, rather than relying on superficial instruction layers that can be bypassed.

### 7.5.2. Practical Implications
For developers and platform engineers, these findings underscore the urgent need to implement independent, secondary safety filters that operate outside the LLM's prompt context. Relying solely on the model's internal judgment—especially via open API access—is empirically proven to be an insufficient security measure. 

### 7.5.3. Policy and Regulatory Implications
The research exposes a critical regulatory gap. Current Indonesian frameworks must be urgently updated to account for the dual-use nature of LLM APIs. Policymakers must mandate rigorous, multi-lingual red-teaming before models are deployed and enforce strict liability frameworks for API providers who fail to secure their models against deliberate system-prompt manipulation. Without addressing the \"API loophole,\" national AI safety strategies will remain fundamentally porous.

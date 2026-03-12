# 8. Conclusion

## 8.1. Summary of Empirical Findings
This study set out to investigate the robustness of Large Language Model (LLM) safety guardrails when exposed to varying system prompt configurations and non-English linguistic contexts. The empirical evidence provides clear, definitive answers to our core research questions:
1. **Do safety mechanisms degrade when system prompt constraints are removed?** Yes. Statistical analysis (t = 2.684, p < 0.01) proves that relaxing system prompts from a restrictive baseline to a neutral state significantly reduces the model's ability to refuse malicious requests.
2. **Is there a disparity in safety performance between English and Bahasa Indonesia?** Yes. While both languages showed comparable safety under highly restrictive prompts, Bahasa Indonesia experienced a much steeper collapse in safety (Δ = 0.326) compared to English (Δ = 0.251) when those constraints were removed. 

## 8.2. Significance of the Study
The significance of these findings lies in exposing the \"API loophole.\" While tech companies invest heavily in securing consumer-facing chat interfaces, they provide raw API access to developers where safety constraints can be easily bypassed by manipulating the system prompt. Furthermore, this study brings critical attention to the \"Global South safety gap.\" It demonstrates that while non-English languages can be forced into compliance via extrinsic prompts, their intrinsic safety alignment is disproportionately weak. This poses a severe risk for regional information ecosystems and local cybersecurity.

## 8.3. Limitations
Despite the rigorous empirical design, this study acknowledges several limitations. First, the evaluation of safety relied on a rule-based string matching protocol; while efficient and based on established literature for capturing explicit refusals, it may misclassify nuanced or partial compliances. Second, the dataset, though spanning multiple models, utilized a fixed set of 18 malicious intents. A broader, more highly varied corpus of malicious prompts might yield different degradation curves. Finally, the closed-source nature of many tested models prevents a deeper architectural analysis of *why* specific weights prioritize compliance over safety.

## 8.4. Future Research Trajectories
Future research must prioritize the development of multi-lingual safety alignment protocols that do not degrade outside of English contexts. We propose three immediate trajectories for subsequent studies:
1. **Automated Red-Teaming for Low-Resource Languages:** Developing frameworks to aggressively test and map vulnerabilities in local languages and dialects.
2. **Decoupled Safety Architectures:** Investigating the efficacy of external, secondary safety classifiers (e.g., Llama-Guard) that operate independently of the primary model's prompt context.
3. **Cross-Cultural Ethical Alignment:** Exploring how safety guardrails can be culturally localized, moving beyond Western-centric ethical frameworks to better serve the Global South.

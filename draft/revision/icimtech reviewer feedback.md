## Feedback from ICIMTech Reviewer

# Reviewer 1: 

This paper presents a quantitative study of API-layer AI safety asymmetry in Indonesia. The overall presentation and experimental results are good, but there are areas where the methodology could be improved. Specific comments are as follows:

1. Page 2, Section “API Testing Protocol” – Please clarify how the 893 observations were distributed across harm categories and languages. Is there any possibility of sampling bias affecting the results?
2. Page 3, Section IV.B – Elaborate on the distinct roles and functions of Qwen and SeaLLMs in the evaluation framework.
3. Page 3 – Typographical error: “result yieds” should be corrected to “result yields.”
4. Page 4, Figure 4 – The text within the five subplots is difficult to read due to very small font sizes; consider enlarging for clarity.
5. Page 4 – The compliance rate for “C3 × Bahasa Indonesia worst cell” is reported as 37.4%, while the Abstract states 37.6%.
6. Page 4, Section V – Clarify the rationale for the chosen thresholds (e.g., why 40% ∆R was used for H1, and why 70% S% was used for H3).

# Reviewer 2:

1. The manuscript introduces the concept of API-Mediated AI Safety Asymmetry, which is potentially novel and valuable. However, the construct currently appears too broad and somewhat under-specified. The authors should define it more rigorously by clarifying its conceptual boundaries and distinguishing whether it refers primarily to: 
    - (a) safety degradation across deployment conditions, 
    - (b) language-related differences in safety performance,   
    - (c) responsibility displacement across actors in the deployment chain, or 
    - (d) a combination of these dimensions.
the paper should distinguish more clearly between what is directly demonstrated by the results, what is inferred from those results, and what is proposed as a policy implication. A more cautious framing will make the manuscript stronger and more credible.
2. One of the manuscript’s most interesting ambitions is to link technical safety degradation with regulatory responsibility gaps. However, at present the connection between these two components remains more rhetorical than fully analytical. The authors should more explicitly show how the deployment conditions tested in the experiment map onto specific actors, responsibilities, and regulatory blind spots in the Indonesian context.
3. The manuscript should explain in more detail how the scoring rubric was operationalized, how judges were instructed, and what criteria were used to distinguish between levels of partial refusal and partial compliance. It would also be helpful to report whether any human validation, pilot calibration, or adjudication was conducted on a subset of responses. Since the manuscript relies on LLM-based evaluators, more transparency is needed regarding inter-judge agreement, disagreement patterns, and the implications of evaluator-specific restrictions or truncation.
4. The manuscript should specify more clearly how the harmful prompts were selected, how many prompt categories were included, whether the categories were balanced across domains and severity levels, and how the Indonesian and English prompts were constructed or translated.
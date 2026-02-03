# Experiment XX: [Concept Name]

## Test Overview

| Field | Value |
|-------|-------|
| **Concept Name** | [Concept Name] |
| **Concept Type** | [Text / Image / Text + Image (description of format)] |
| **Personas Tested** | [N] [persona description] |
| **Processing Time** | [X.X] seconds (~X.X minutes) |
| **Providers** | [generation provider], [embedding provider] |

---

## Concept Description

[Narrative description of the concept being tested. Describe the format (text, image, storyboard, etc.), the brand, and the key messaging or creative elements. If multiple concepts are being compared, describe each one.]

---

## Overall Result: [PASSED/FAILED] ([Marginal/Moderate/Clear])

| Metric | Value |
|--------|-------|
| **Composite Score** | 0.XXX |
| **Threshold** | 0.XX |
| **Margin** | [+/-]0.XXX |
| **Verdict** | **[PASS/FAIL]** (exceeded/fell short by X.X%) |

---

## Criteria Breakdown

| Question | Weight | Raw Mean | Normalized | Contribution |
|----------|--------|----------|------------|--------------|
| [question_1] | X% | X.XX | 0.XXX | 0.XXX |
| [question_2] | X% | X.XX | 0.XXX | 0.XXX |
| ... | ... | ... | ... | ... |

---

## Key Insights

### Strengths

1. **[Metric Name]** (X.XX) - [Detailed explanation of why this performed well, including distribution data and representative persona feedback.]

2. **[Metric Name]** (X.XX) - [Explanation.]

### Weaknesses

1. **[Metric Name]** (X.XX) - [Detailed explanation of why this underperformed, including distribution data and representative persona feedback.]

2. **[Metric Name]** (X.XX) - [Explanation.]

---

## Metrics Summary

| Question | Mean | Median | Std Dev | Top 2 Box | Bottom 2 Box |
|----------|------|--------|---------|-----------|--------------|
| [question_1] | X.XX | X.XX | X.XX | X% | X% |
| [question_2] | X.XX | X.XX | X.XX | X% | X% |
| ... | ... | ... | ... | ... | ... |

### Distribution Analysis (All Questions Combined)

| Rating | Count | Percentage |
|--------|-------|------------|
| 1 (Strongly Negative) | X | X.X% |
| 2 (Negative) | X | X.X% |
| 3 (Neutral) | X | X.X% |
| 4 (Positive) | X | X.X% |
| 5 (Strongly Positive) | X | X.X% |

[Paragraph interpreting the distribution pattern - clustering, spread, presence/absence of extreme responses, and what this suggests about overall sentiment.]

---

## Sample Responses

### [persona_id] ([age]y, [Gender], [Country], [Education])

**[Question Name] (X.XX):**
> "[Response text from persona]"

**[Question Name] (X.XX):**
> "[Response text from persona]"

---

### [persona_id] ([age]y, [Gender], [Country], [Education])

**[Question Name] (X.XX):**
> "[Response text from persona]"

---

[Include 4-6 sample responses representing a cross-section of demographics and sentiment.]

---

## Conclusions

1. **[Main finding about pass/fail result.]** [Supporting detail about composite score, margin, and what drove the result.]

2. **[Key strength finding.]** [Supporting detail.]

3. **[Key weakness finding.]** [Supporting detail.]

4. **[Behavioral insight or comparison finding.]** [Supporting detail.]

5. **[Recommendation for improvement or next steps.]** [Supporting detail.]

---

## Dataset Summary

The full dataset contains [N] persona responses with:
- Raw text responses for all [N] questions
- 5-point probability distributions (PMF) from SSR scoring
- Mean Likert scores (1-5) for each question
- Demographics: [list of demographic fields]

Available in `[experiment_number]_[slug]_output.json` under the `"dataset"` key.

---

## Appendix: Survey Questions and Response Scales

### Q1: [Question Label]
**"[Full question text]"**

| Score | Response |
|-------|----------|
| 1 | [Scale point 1] |
| 2 | [Scale point 2] |
| 3 | [Scale point 3] |
| 4 | [Scale point 4] |
| 5 | [Scale point 5] |

### Q2: [Question Label]
**"[Full question text]"**

| Score | Response |
|-------|----------|
| 1 | [Scale point 1] |
| 2 | [Scale point 2] |
| 3 | [Scale point 3] |
| 4 | [Scale point 4] |
| 5 | [Scale point 5] |

[Repeat for all questions in the survey.]

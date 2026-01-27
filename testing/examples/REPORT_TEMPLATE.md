# Experiment XX: [Concept Name]

## Test Overview

| Field | Value |
|-------|-------|
| **Concept Name** | [Concept Name] |
| **Personas Tested** | [N] [persona description] |
| **Processing Time** | [X.X] seconds |
| **Providers** | [generation provider], [embedding provider] |

---

## Input JSON Structure

The input consists of three main sections:

### 1. Personas ([N] synthetic consumers)
```json
{
  "personas": [
    {"persona_id": "xxx_01", "age": 00, "gender": "X", "income": "xxx", "location": "xxx", "interests": ["...", "...", "..."]},
    {"persona_id": "xxx_02", "age": 00, "gender": "X", "income": "xxx", "location": "xxx", "interests": ["...", "...", "..."]},
    ...
  ]
}
```

### 2. Concept (Description)
```json
{
  "concept": {
    "name": "[Concept Name]",
    "content": [
      {
        "type": "text",
        "data": "[Full concept description...]"
      }
    ]
  }
}
```

### 3. Survey Configuration ([N] Questions with SSR Reference Sets)
```json
{
  "survey_config": {
    "questions": [
      {
        "id": "[question_id]",
        "text": "[Question text]",
        "weight": 0.X,
        "ssr_reference_sets": [
          ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"],
          ...
        ]
      },
      ...
    ]
  },
  "threshold": 0.XX,
  "output_dataset": true
}
```

---

## Output JSON

### Result Summary
```json
{
  "result": {
    "passed": [true/false],
    "composite_score": 0.XXX,
    "threshold": 0.XX,
    "margin": [+/-]0.XXX,
    "reason": "[PASS/FAIL]: [reason message]"
  }
}
```

### Metrics by Question
```json
{
  "metrics": {
    "[question_id]": {
      "n": [N],
      "mean": X.XX,
      "median": X.XX,
      "std_dev": X.XX,
      "top_2_box": X.XX,
      "bottom_2_box": X.XX,
      "distribution": {"1": X, "2": X, "3": X, "4": X, "5": X}
    },
    ...
  }
}
```

---

## Analysis Report

### Overall Result: [PASSED/FAILED] ([Marginal/Clear])

| Metric | Value |
|--------|-------|
| **Composite Score** | 0.XXX |
| **Threshold** | 0.XX |
| **Margin** | [+/-]0.XXX |
| **Verdict** | [PASS/FAIL] (by X.X%) |

### Criteria Breakdown

| Question | Weight | Raw Mean | Normalized | Contribution |
|----------|--------|----------|------------|--------------|
| [question_1] | X% | X.XX | 0.XXX | 0.XXX |
| [question_2] | X% | X.XX | 0.XXX | 0.XXX |
| ... | ... | ... | ... | ... |

### Key Insights

**Strengths:**
- **[Metric Name]** (X.XX) - [Explanation of why this performed well]
- **[Metric Name]** (X.XX) - [Explanation]

**Weaknesses:**
- **[Metric Name]** (X.XX) - [Explanation of why this underperformed]
- **[Metric Name]** (X.XX) - [Explanation]

### Distribution Analysis

| Rating | Count | Percentage |
|--------|-------|------------|
| 1 (Strongly Negative) | X | X.X% |
| 2 (Negative) | X | X.X% |
| 3 (Neutral) | X | X.X% |
| 4 (Positive) | X | X.X% |
| 5 (Strongly Positive) | X | X.X% |

---

## Sample Responses

### [persona_id] ([age]y, [Gender], [Income] Income, [Location])
*Interests: [interest1], [interest2], [interest3]*

**[Question Name] (X.XX):**
> "[Response text from persona]"

**[Question Name] (X.XX):**
> "[Response text from persona]"

---

### [persona_id] ([age]y, [Gender], [Income] Income, [Location])
*Interests: [interest1], [interest2], [interest3]*

**[Question Name] (X.XX):**
> "[Response text from persona]"

---

## Generated Dataset ([N] rows)

| persona_id | age | gender | income | location | [q1] | [q2] | [q3] | ... |
|------------|-----|--------|--------|----------|------|------|------|-----|
| xxx_01 | XX | X | xxx | xxx | X.XX | X.XX | X.XX | ... |
| xxx_02 | XX | X | xxx | xxx | X.XX | X.XX | X.XX | ... |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

---

## Conclusions

1. **[Main finding about pass/fail result]**

2. **[Key strength finding]**

3. **[Key weakness finding]**

4. **[Behavioral insight]**

5. **[Recommendation for improvement or next steps]**

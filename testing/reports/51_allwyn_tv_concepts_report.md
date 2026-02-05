# Concept Test Report: Allwyn TV Ad Concepts

## Test Overview

| Field | Value |
|-------|-------|
| **Experiment ID** | `5a3e3af5` |
| **Concept Name** | Allwyn TV Ad Concepts |
| **Personas Tested** | 90 of 90 |
| **Processing Time** | 530.5s (~8.8 min) |
| **Generation Model** | `eu.amazon.nova-2-lite-v1:0` (bedrock) |
| **Embedding Model** | `amazon.titan-embed-text-v2:0` (bedrock) |
| **Vision Model** | `eu.amazon.nova-2-lite-v1:0` (bedrock) |

---

## Concept Description

**Concept:** Allwyn TV Ad Concepts
**Format:** Text + Image (2 content items)

> We're going to show you two early stage TV ad concepts.

*1 image(s) included in concept stimulus.*

---

## Overall Result: FAILED (Marginal)

| Metric | Value |
|--------|-------|
| **Composite Score** | 0.515 |
| **Threshold** | 0.55 |
| **Margin** | -0.035 |
| **Verdict** | **FAILED** (fell short by 3.5%) |

---

## Criteria Breakdown

| Question | Weight | Raw Mean | Normalized | Contribution |
|----------|--------|----------|------------|--------------|
| want_to_know_more | 20% | 3.02 | 0.505 | 0.101 |
| memorability | 20% | 3.23 | 0.557 | 0.112 |
| research_intent | 20% | 2.85 | 0.463 | 0.093 |
| personal_fit | 20% | 3.42 | 0.605 | 0.121 |
| concept_preference | 20% | 2.78 | 0.445 | 0.089 |

---

## Key Insights

### Strengths

1. **personal_fit** (3.42) - Top 2 box: 1%, median: 3.76, wide spread (std: 0.64)

2. **memorability** (3.23) - Top 2 box: 4%, median: 3.33, moderate spread (std: 0.50)

3. **want_to_know_more** (3.02) - Top 2 box: 0%, median: 3.02, tight spread (std: 0.29)


### Weaknesses

1. **research_intent** (2.85) - Bottom 2 box: 0%, median: 2.79, tight spread (std: 0.28)

2. **concept_preference** (2.78) - Bottom 2 box: 0%, median: 2.73, tight spread (std: 0.15)


---

## Metrics Summary

| Question | Mean | Median | Std Dev | Top 2 Box | Bottom 2 Box |
|----------|------|--------|---------|-----------|--------------|
| want_to_know_more | 3.02 | 3.02 | 0.29 | 0% | 0% |
| memorability | 3.23 | 3.33 | 0.50 | 4% | 0% |
| research_intent | 2.85 | 2.79 | 0.28 | 0% | 0% |
| personal_fit | 3.42 | 3.76 | 0.64 | 1% | 1% |
| concept_preference | 2.78 | 2.73 | 0.15 | 0% | 0% |

---

### Distribution Analysis (All Questions Combined)

| Rating | Count | Percentage |
|--------|-------|------------|
| 1 (Strongly Negative) | 0 | 0.0% |
| 2 (Negative) | 37 | 8.2% |
| 3 (Neutral) | 317 | 70.4% |
| 4 (Positive) | 96 | 21.3% |
| 5 (Strongly Positive) | 0 | 0.0% |

Overall sentiment is largely neutral with limited polarisation, with 21% positive, 70% neutral, and 8% negative responses.

---

## Conclusions

1. **Overall Result**: The concept failed with a composite score of 0.515 against a threshold of 0.55 (margin: 3.5%). The overall mean across all metrics is 3.06/5.

2. **Strongest Metric**: personal_fit scored 3.42 with 1% top 2 box and median 3.76.

3. **Weakest Metric**: concept_preference scored 2.78 with 0% bottom 2 box and median 2.73.

4. **Response Consistency**: personal_fit showed the most variation (std dev: 0.64), suggesting differing reactions across personas.

5. **Recommendation**: The concept narrowly missed the threshold. Minor refinements to the weakest metrics could bring it to a passing score. Consider targeted iteration rather than a full rework.

---

## Dataset Summary

The full dataset contains 90 persona responses with:
- Raw text responses for all 5 questions
- 5-point probability distributions (PMF) from SSR scoring
- Mean Likert scores (1-5) for each question

---

## Appendix: Survey Questions and Response Scales

### Q1: want_to_know_more
**"Please review concept 1. Did this concept make you want to know more about working at this company?"**

| Score | Response |
|-------|----------|
| 1 | Not at all |
| 2 | Slightly |
| 3 | Moderately |
| 4 | Very much |
| 5 | Extremely |

### Q2: memorability
**"To what extent do you agree with this statement: 'Concept 1 is memorable.'"**

| Score | Response |
|-------|----------|
| 1 | Strongly disagree |
| 2 | Disagree |
| 3 | Neither agree nor disagree |
| 4 | Agree |
| 5 | Strongly agree |

### Q3: research_intent
**"Would you research jobs at this company after seeing concept 1 turned into a TV ad?"**

| Score | Response |
|-------|----------|
| 1 | Definitely not |
| 2 | Probably not |
| 3 | Maybe |
| 4 | Probably yes |
| 5 | Definitely yes |

### Q4: personal_fit
**"How well do you feel the company depicted in concept 1 would fit someone like you?"**

| Score | Response |
|-------|----------|
| 1 | Very poor fit |
| 2 | Poor fit |
| 3 | Moderate fit |
| 4 | Good fit |
| 5 | Excellent fit |

### Q5: concept_preference
**"Looking at both concepts, which concept do you prefer and how strongly?"**

| Score | Response |
|-------|----------|
| 1 | Strongly prefer Concept 2 |
| 2 | Slightly prefer Concept 2 |
| 3 | No preference |
| 4 | Slightly prefer Concept 1 |
| 5 | Strongly prefer Concept 1 |

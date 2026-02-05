# Concept Test Report: Allwyn TV Ad Concepts

## Test Overview

| Field | Value |
|-------|-------|
| **Experiment ID** | `5c5ca5cd` |
| **Concept Name** | Allwyn TV Ad Concepts |
| **Personas Tested** | 90 of 90 |
| **Processing Time** | 89.3s (~1.5 min) |
| **Generation Model** | `eu.amazon.nova-pro-v1:0` (bedrock) |
| **Embedding Model** | `amazon.titan-embed-text-v1` (bedrock) |
| **Vision Model** | `eu.amazon.nova-pro-v1:0` (bedrock) |

---

## Concept Description

**Concept:** Allwyn TV Ad Concepts
**Format:** Text + Image (2 content items)

> We're going to show you two early stage TV ad concepts.

*1 image(s) included in concept stimulus.*

---

## Overall Result: PASSED (Marginal)

| Metric | Value |
|--------|-------|
| **Composite Score** | 0.562 |
| **Threshold** | 0.55 |
| **Margin** | +0.012 |
| **Verdict** | **PASSED** (exceeded by 1.2%) |

---

## Criteria Breakdown

| Question | Weight | Raw Mean | Normalized | Contribution |
|----------|--------|----------|------------|--------------|
| want_to_know_more | 20% | 3.32 | 0.580 | 0.116 |
| memorability | 20% | 3.15 | 0.537 | 0.107 |
| research_intent | 20% | 3.09 | 0.522 | 0.104 |
| personal_fit | 20% | 3.60 | 0.650 | 0.130 |
| concept_preference | 20% | 3.08 | 0.520 | 0.104 |

---

## Key Insights

### Strengths

1. **personal_fit** (3.60) - Top 2 box: 2%, median: 3.62, tight spread (std: 0.21)

2. **want_to_know_more** (3.32) - Top 2 box: 0%, median: 3.31, tight spread (std: 0.22)

3. **memorability** (3.15) - Top 2 box: 0%, median: 3.15, tight spread (std: 0.23)


### Weaknesses

1. **research_intent** (3.09) - Bottom 2 box: 0%, median: 3.14, tight spread (std: 0.26)

2. **concept_preference** (3.08) - Bottom 2 box: 0%, median: 3.10, tight spread (std: 0.11)


---

## Metrics Summary

| Question | Mean | Median | Std Dev | Top 2 Box | Bottom 2 Box |
|----------|------|--------|---------|-----------|--------------|
| want_to_know_more | 3.32 | 3.31 | 0.22 | 0% | 0% |
| memorability | 3.15 | 3.15 | 0.23 | 0% | 0% |
| research_intent | 3.09 | 3.14 | 0.26 | 0% | 0% |
| personal_fit | 3.60 | 3.62 | 0.21 | 2% | 0% |
| concept_preference | 3.08 | 3.10 | 0.11 | 0% | 0% |

---

### Distribution Analysis (All Questions Combined)

| Rating | Count | Percentage |
|--------|-------|------------|
| 1 (Strongly Negative) | 0 | 0.0% |
| 2 (Negative) | 2 | 0.4% |
| 3 (Neutral) | 360 | 80.0% |
| 4 (Positive) | 88 | 19.6% |
| 5 (Strongly Positive) | 0 | 0.0% |

Overall sentiment is predominantly positive, with 20% positive, 80% neutral, and 0% negative responses.

---

## Sample Responses

### uk_f_01 (24y, F, United Kingdom, Undergraduate degree)

**want_to_know_more** (3.03):
> "Honestly, Concept 1 didn't really make me feel excited about working at Allwyn. The scenes felt a bit generic and didn't really stand out to me. I think it needs something more unique to capture my interest."

**memorability** (3.11):
> "I think Concept 1 is quite memorable. The different scenes and the consistent messaging about energy and stability really stand out."

---

### uk_m_04 (24y, M, United Kingdom, Undergraduate degree)

**want_to_know_more** (2.77):
> "Honestly, I didn't feel a strong connection to Concept 1. The scenes felt a bit generic and the music didn't really grab my attention. It didn't make me particularly excited to learn more about working at the company."

**memorability** (2.83):
> "I think Concept 1 is pretty memorable. The different scenes and the consistent messaging really stick with you."

---

### gr_f_07 (27y, F, Greece, Doctorate)

**want_to_know_more** (3.29):
> "Honestly, I don't feel particularly drawn to this concept. The scenes seem a bit generic and don't really highlight what makes this company unique or why I should consider working there. I'd need more compelling visuals and a stronger narrative to be interested."

**memorability** (3.27):
> "I find Concept 1 quite memorable due to its vibrant and dynamic scenes, especially the energetic startup office and the contrasting big firms' boardroom. The music and camera angles effectively highlight the contrast, making it stand out."

---

### gr_m_10 (38y, M, Greece, Doctorate)

**want_to_know_more** (3.80):
> "I find concept 1 quite engaging and it does spark my curiosity about the company. The depiction of a dynamic work environment and the emphasis on career growth are particularly appealing."

**memorability** (3.09):
> "I find Concept 1 quite memorable due to its dynamic scenes and engaging music. The contrast between startups and big firms is effectively highlighted, making it stand out."

---

### cz_f_13 (31y, F, Czech Republic, Undergraduate degree)

**want_to_know_more** (3.30):
> "Concept 1 feels a bit generic and doesn't really stand out to me. It doesn't give me a strong urge to learn more about working at the company."

**memorability** (3.15):
> "I agree that Concept 1 is memorable. The distinct scenes and the recurring phrase "A winning career awaits" make it stand out."

---

## Conclusions

1. **Overall Result**: The concept passed with a composite score of 0.562 against a threshold of 0.55 (margin: 1.2%). The overall mean across all metrics is 3.25/5.

2. **Strongest Metric**: personal_fit scored 3.60 with 2% top 2 box and median 3.62.

3. **Weakest Metric**: concept_preference scored 3.08 with 0% bottom 2 box and median 3.10.

4. **Response Consistency**: research_intent showed the most variation (std dev: 0.26), suggesting differing reactions across personas.

5. **Recommendation**: The concept meets the threshold criteria. Consider addressing the weakest metrics to further strengthen the concept before proceeding to market.

---

## Dataset Summary

The full dataset contains 90 persona responses with:
- Raw text responses for all 5 questions
- 5-point probability distributions (PMF) from SSR scoring
- Mean Likert scores (1-5) for each question
- Demographics: age, gender, country, education, language

---

## Appendix: Survey Questions and Response Scales

### Q1: want_to_know_more
**"Please review concept 1. Did this concept make you want to know more about working at this company?"**

| Score | Response |
|-------|----------|
| 1 | Definitely not |
| 2 | Probably not |
| 3 | Unsure |
| 4 | Probably yes |
| 5 | Definitely yes |

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
| 4 | Probably |
| 5 | Definitely |

### Q4: personal_fit
**"How well do you feel the company depicted in concept 1 would fit someone like you?"**

| Score | Response |
|-------|----------|
| 1 | Not well at all |
| 2 | Not very well |
| 3 | Somewhat |
| 4 | Quite well |
| 5 | Very well |

### Q5: concept_preference
**"Looking at both concepts, which concept do you prefer and how strongly?"**

| Score | Response |
|-------|----------|
| 1 | Strongly prefer Concept 2 |
| 2 | Slightly prefer Concept 2 |
| 3 | No preference |
| 4 | Slightly prefer Concept 1 |
| 5 | Strongly prefer Concept 1 |


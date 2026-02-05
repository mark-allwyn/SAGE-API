# Concept Test Report: Sports Car Video Concept

## Test Overview

| Field | Value |
|-------|-------|
| **Experiment ID** | `0ed3f958` |
| **Concept Name** | Sports Car Video Concept |
| **Personas Tested** | 90 of 90 |
| **Processing Time** | 743.1s (~12.4 min) |
| **Generation Model** | `eu.anthropic.claude-sonnet-4-5-20250929-v1:0` (bedrock) |
| **Embedding Model** | `amazon.titan-embed-text-v2:0` (bedrock) |
| **Vision Model** | `eu.anthropic.claude-sonnet-4-5-20250929-v1:0` (bedrock) |

---

## Concept Description

**Concept:** Sports Car Video Concept
**Format:** Text (2 content items)

> We are going to show you a video

---

## Overall Result: PASSED (Clear)

| Metric | Value |
|--------|-------|
| **Composite Score** | 0.718 |
| **Threshold** | 0.55 |
| **Margin** | +0.168 |
| **Verdict** | **PASSED** (exceeded by 16.8%) |

---

## Criteria Breakdown

| Question | Weight | Raw Mean | Normalized | Contribution |
|----------|--------|----------|------------|--------------|
| video_appeal | 20% | 3.90 | 0.725 | 0.145 |
| memorability | 20% | 3.93 | 0.733 | 0.147 |
| excitement | 20% | 3.88 | 0.720 | 0.144 |
| purchase_interest | 20% | 3.92 | 0.730 | 0.146 |
| share_intent | 20% | 3.72 | 0.680 | 0.136 |

---

## Key Insights

### Strengths

1. **memorability** (3.93) - Top 2 box: 32%, median: 3.95, tight spread (std: 0.11)

2. **purchase_interest** (3.92) - Top 2 box: 21%, median: 3.94, tight spread (std: 0.07)

3. **video_appeal** (3.90) - Top 2 box: 2%, median: 3.89, tight spread (std: 0.04)


### Weaknesses

1. **excitement** (3.88) - Bottom 2 box: 0%, median: 3.92, tight spread (std: 0.12)

2. **share_intent** (3.72) - Bottom 2 box: 0%, median: 3.72, tight spread (std: 0.14)


---

## Metrics Summary

| Question | Mean | Median | Std Dev | Top 2 Box | Bottom 2 Box |
|----------|------|--------|---------|-----------|--------------|
| video_appeal | 3.90 | 3.89 | 0.04 | 2% | 0% |
| memorability | 3.93 | 3.95 | 0.11 | 32% | 0% |
| excitement | 3.88 | 3.92 | 0.12 | 9% | 0% |
| purchase_interest | 3.92 | 3.94 | 0.07 | 21% | 0% |
| share_intent | 3.72 | 3.72 | 0.14 | 0% | 0% |

---

### Distribution Analysis (All Questions Combined)

| Rating | Count | Percentage |
|--------|-------|------------|
| 1 (Strongly Negative) | 0 | 0.0% |
| 2 (Negative) | 0 | 0.0% |
| 3 (Neutral) | 3 | 0.7% |
| 4 (Positive) | 447 | 99.3% |
| 5 (Strongly Positive) | 0 | 0.0% |

Overall sentiment is predominantly positive, with 99% positive, 1% neutral, and 0% negative responses.

---

## Sample Responses

### uk_f_01 (24y, F, United Kingdom, Undergraduate degree)

**video_appeal** (3.95):
> "I found the video quite appealing. The vibrant green sports car looks sleek and fast, and the sunset backdrop adds a dramatic touch. It's definitely eye-catching and would likely attract car enthusiasts."

**memorability** (3.83):
> "As a 24-year-old female from the United Kingdom with an undergraduate degree, I find the video quite memorable. The vibrant green sports car and the dynamic shots of it speeding along the racetrack during sunset create a visually striking and engaging experience."

---

### uk_m_04 (24y, M, United Kingdom, Undergraduate degree)

**video_appeal** (3.82):
> "I found the video quite appealing. The vibrant green sports car looks sleek and powerful, and the dynamic shots of it speeding along the racetrack are impressive. The sunset backdrop adds a nice touch to the overall visual appeal."

**memorability** (3.86):
> "As a 24-year-old male from the United Kingdom with an undergraduate degree, I find the video quite memorable. The vibrant green sports car and the dynamic shots of it speeding along the racetrack during sunset create a visually striking and engaging experience."

---

### gr_f_07 (27y, F, Greece, Doctorate)

**video_appeal** (4.00):
> "As a 27-year-old female with a doctorate from Greece, I found the video quite appealing. The vibrant green sports car and the dynamic shots of it speeding along the track captured my attention, showcasing the car's sleek design and performance."

**memorability** (3.92):
> "As a 27-year-old female from Greece with a doctorate, I find the video to be quite memorable. The vibrant green sports car and the dynamic shots of it speeding along the racetrack create a visually striking and engaging experience."

---

### gr_m_10 (38y, M, Greece, Doctorate)

**video_appeal** (3.94):
> "As a 38-year-old male from Greece with a doctorate, I found the video quite appealing. The vibrant green sports car and the dynamic shots of it speeding along the racetrack captured my attention and showcased the car's impressive design and performance."

**memorability** (3.88):
> "As a 38-year-old male from Greece with a doctorate, I find the video to be quite memorable. The vibrant green sports car and the dynamic shots of it speeding along the racetrack create a visually striking and engaging experience."

---

### cz_f_13 (31y, F, Czech Republic, Undergraduate degree)

**video_appeal** (3.88):
> "I found the video quite appealing. The vibrant green sports car looks sleek and powerful, and the dynamic shots of it speeding along the track are captivating. The sunset backdrop adds a beautiful touch to the overall presentation."

**memorability** (3.92):
> "As a 31-year-old female from the Czech Republic with an undergraduate degree, I find the video quite memorable. The vibrant green sports car and the dynamic shots of it speeding along the racetrack during sunset create a visually striking and engaging experience."

---

## Conclusions

1. **Overall Result**: The concept passed with a composite score of 0.718 against a threshold of 0.55 (margin: 16.8%). The overall mean across all metrics is 3.87/5.

2. **Strongest Metric**: memorability scored 3.93 with 32% top 2 box and median 3.95.

3. **Weakest Metric**: share_intent scored 3.72 with 0% bottom 2 box and median 3.72.

4. **Response Consistency**: share_intent showed the most variation (std dev: 0.14), suggesting differing reactions across personas.

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

### Q1: video_appeal
**"How appealing did you find this video?"**

| Score | Response |
|-------|----------|
| 1 | Not at all appealing |
| 2 | Not very appealing |
| 3 | Somewhat appealing |
| 4 | Quite appealing |
| 5 | Very appealing |

### Q2: memorability
**"To what extent do you agree with this statement: 'This video is memorable.'"**

| Score | Response |
|-------|----------|
| 1 | Strongly disagree |
| 2 | Disagree |
| 3 | Neither agree nor disagree |
| 4 | Agree |
| 5 | Strongly agree |

### Q3: excitement
**"How exciting did you find the car shown in this video?"**

| Score | Response |
|-------|----------|
| 1 | Not at all exciting |
| 2 | Not very exciting |
| 3 | Somewhat exciting |
| 4 | Quite exciting |
| 5 | Very exciting |

### Q4: purchase_interest
**"After watching this video, how interested would you be in learning more about the car shown?"**

| Score | Response |
|-------|----------|
| 1 | Not at all interested |
| 2 | Not very interested |
| 3 | Somewhat interested |
| 4 | Quite interested |
| 5 | Very interested |

### Q5: share_intent
**"How likely would you be to share this video with someone you know?"**

| Score | Response |
|-------|----------|
| 1 | Not at all likely |
| 2 | Not very likely |
| 3 | Somewhat likely |
| 4 | Quite likely |
| 5 | Very likely |

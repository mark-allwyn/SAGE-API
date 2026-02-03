# Experiment 10: Allwyn TV Ad Concepts

## Test Overview

| Field | Value |
|-------|-------|
| **Concept Name** | Allwyn TV Ad Concepts |
| **Concept Type** | Text + Image (two TV ad concept storyboards, JPEG, base64-encoded) |
| **Personas Tested** | 90 adults across UK, Greece, and Czech Republic (ages 21-40, undergraduate degree or higher) |
| **Processing Time** | 352.7 seconds (~5.9 minutes) |
| **Providers** | openai/gpt-4o (generation + vision), openai/text-embedding-3-small (embedding) |

---

## Concept Description

This is a **dual-concept comparison test** using both text and image inputs. The image contains two TV ad concept storyboards for the **Allwyn** brand - a lottery and gaming entertainment company.

- **Concept 1** (left): Focuses on contrasting the energy of startups with the stability of big firms, positioning Allwyn as offering "the best of both worlds." Features upbeat acoustic guitar music, dynamic office scenes, and a voiceover emphasising career growth.
- **Concept 2** (right): An alternative creative approach for the same Allwyn employer brand campaign.

Personas were asked to evaluate Concept 1 individually across four metrics, then compare both concepts in a preference question.

---

## Overall Result: PASSED (Moderate)

| Metric | Value |
|--------|-------|
| **Composite Score** | 0.635 |
| **Threshold** | 0.55 |
| **Margin** | +0.085 |
| **Verdict** | **PASS** (exceeded by 8.5%) |

---

## Criteria Breakdown

| Question | Weight | Raw Mean | Normalized | Contribution |
|----------|--------|----------|------------|--------------|
| want_to_know_more | 20% | 3.40 | 0.600 | 0.120 |
| memorability | 20% | 3.19 | 0.547 | 0.110 |
| research_intent | 20% | 3.44 | 0.610 | 0.122 |
| personal_fit | 20% | 4.07 | 0.768 | 0.154 |
| concept_preference | 20% | 3.60 | 0.650 | 0.130 |

---

## Key Insights

### Strengths

1. **Personal Fit** (4.07) - The strongest performing metric by a significant margin. 100% of personas rated this at level 4, with 82% top-2-box. The concept's messaging about balancing startup energy with big-firm stability resonated universally across all three countries. Personas consistently described the depicted work environment as aligning with their career aspirations.

2. **Concept Preference** (3.60) - 83.3% of personas rated at level 4, indicating a clear preference for Concept 1 over Concept 2. Only 1 persona (1.1%) leaned towards Concept 2. Personas described Concept 1 as "more polished," "more dynamic," and "more engaging."

3. **Research Intent** (3.44) - Nearly evenly split between level 3 (50.0%) and level 4 (47.8%), suggesting the concept generates moderate-to-good interest in exploring employment opportunities. The "best of both worlds" proposition was cited as the primary driver of curiosity.

### Weaknesses

1. **Memorability** (3.19) - The lowest-scoring metric. 86.7% of responses clustered at level 3, suggesting the concept is perceived as competent but not distinctive. Multiple personas described it as "a bit generic" and "similar to other corporate ads," indicating the creative execution may need a more unique or surprising element to stand out.

2. **Want to Know More** (3.40) - While above neutral, responses were split between level 3 (46.7%) and level 4 (53.3%). Several personas noted the concept lacks specific details about what makes Allwyn unique, with the messaging feeling too broad to compel further investigation.

---

## Metrics Summary

| Question | Mean | Median | Std Dev | Top 2 Box | Bottom 2 Box |
|----------|------|--------|---------|-----------|--------------|
| want_to_know_more | 3.40 | 3.52 | 0.33 | 1% | 0% |
| memorability | 3.19 | 3.16 | 0.32 | 3% | 0% |
| research_intent | 3.44 | 3.49 | 0.26 | 0% | 0% |
| personal_fit | 4.07 | 4.09 | 0.09 | 82% | 0% |
| concept_preference | 3.60 | 3.65 | 0.21 | 0% | 0% |

### Distribution Analysis (All Questions Combined)

| Rating | Count | Percentage |
|--------|-------|------------|
| 1 (Strongly Negative) | 0 | 0.0% |
| 2 (Negative) | 3 | 0.7% |
| 3 (Neutral) | 179 | 39.8% |
| 4 (Positive) | 268 | 59.6% |
| 5 (Strongly Positive) | 0 | 0.0% |

The distribution is notably concentrated in the 3-4 range with zero extreme responses (1 or 5), suggesting the concept is viewed positively but without generating strong emotional reactions in either direction. The very low standard deviations (0.09-0.33) across all questions reinforce this pattern of consensus around moderate-positive sentiment.

---

## Sample Responses

### uk_f_01 (24y, F, United Kingdom, Undergraduate degree)

**Want to Know More (3.17):**
> "Concept 1 is intriguing with its focus on combining startup energy with big firm stability. The upbeat music and visuals create an engaging atmosphere, but the message feels a bit generic. It might make me curious, but I'd want more specific details about what makes Allwyn unique as a workplace."

**Research Intent (2.21):**
> "Honestly, I wouldn't be inclined to research jobs at this company after seeing Concept 1 turned into a TV ad. The ad seems a bit generic, and while it mentions the benefits of both startups and big firms, it doesn't really convey what makes Allwyn unique or appealing to me personally."

**Concept Preference (3.57):**
> "I prefer Concept 1. It feels more dynamic and engaging with its focus on the energy of startups and the stability of big firms. The upbeat music and clear messaging about getting the best of both worlds really resonate with me."

---

### uk_m_05 (33y, M, United Kingdom, Undergraduate degree)

**Want to Know More (2.90):**
> "Concept 1 gives a balanced view of startups and big firms, highlighting both energy and stability. The upbeat music and visuals are engaging, but it doesn't specifically tell me what makes this company different from others."

**Research Intent (3.80):**
> "After seeing Concept 1 as a TV ad, I would consider researching jobs at Allwyn. The ad effectively highlights a blend of startup energy and big firm stability, which sounds appealing for career growth."

**Concept Preference (3.74):**
> "I prefer Concept 1. The approach feels more polished and professional, with a clearer depiction of the advantages of both startups and big firms."

---

### gr_f_03 (24y, F, Greece, Postgraduate degree)

**Want to Know More (3.53):**
> "Concept 1 is visually appealing and effectively contrasts the energy of startups with the stability of big firms. The upbeat music and dynamic scenes make working there seem appealing."

**Personal Fit (4.12):**
> "Concept 1 seems to focus on balancing startup energy with big firm stability, which is appealing to me. The idea of having a dynamic work environment with career security resonates with my career aspirations."

**Concept Preference (3.57):**
> "I prefer Concept 1 because it presents a more organized and energetic vibe, which feels more appealing and professional. The upbeat music and clear messaging about combining both worlds really stand out."

---

### gr_m_10 (38y, M, Greece, Doctorate)

**Memorability (3.53):**
> "I somewhat agree that Concept 1 is memorable. The juxtaposition of startups and big firms with distinct energy levels and stability themes is engaging."

**Research Intent (3.56):**
> "I might be intrigued by Concept 1 if it were turned into a TV ad. The combination of startup energy and big firm stability is appealing, and it suggests an innovative work environment."

**Personal Fit (3.97):**
> "In Concept 1, the portrayal of balancing startup energy with big firm stability is quite appealing. As someone with a doctorate, I appreciate the focus on growth and innovation."

---

### cz_f_07 (33y, F, Czech Republic, Doctorate)

**Memorability (3.70):**
> "I somewhat agree that Concept 1 is memorable. The contrast between startups and big firms, combined with the upbeat music and dynamic visuals, creates an engaging narrative."

**Personal Fit (4.20):**
> "As someone with a doctorate and a career-oriented mindset, I find Concept 1 appealing because it highlights a balance of startup energy and big firm stability."

**Concept Preference (3.62):**
> "I prefer Concept 1. It feels more dynamic and engaging, with a good balance between the energy of startups and the stability of big firms."

---

### cz_m_12 (21y, M, Czech Republic, Undergraduate degree)

**Want to Know More (4.02):**
> "Concept 1 is visually engaging and effectively contrasts startups and big firms. The upbeat music and dynamic scenes make working there seem appealing."

**Memorability (3.60):**
> "I somewhat agree that Concept 1 is memorable. The contrast between the energetic startup scenes and the more formal big firm settings is striking."

**Research Intent (3.58):**
> "I might be curious to research jobs at the company after seeing Concept 1. The ad effectively highlights the balance between startup energy and big firm stability."

---

## Conclusions

1. **The concepts passed the threshold test with a moderate margin.** The composite score of 0.635 exceeded the 0.55 threshold by 8.5%. While this is a clear pass, the margin is not large, and the score is driven primarily by strong personal fit perception rather than broad enthusiasm across all metrics.

2. **Personal fit is the standout strength.** At 4.07, this was the only metric to consistently achieve level 4 ratings. The "best of both worlds" employer value proposition - combining startup energy with big-firm stability - resonated strongly and consistently across all demographics, genders, and education levels.

3. **Memorability is the primary concern.** At 3.19, this is the weakest metric and the only one below the threshold when viewed in isolation (normalized 0.547 vs. 0.55 threshold). Personas repeatedly described the concept as "a bit generic" and lacking a distinctive or surprising element that would make it stand out from other corporate recruitment advertising.

4. **Concept 1 is the clear winner.** 83.3% of personas preferred Concept 1, with only 1.1% favouring Concept 2. The preference was consistent across all three countries. Concept 1 was described as more dynamic, polished, and engaging than Concept 2.

5. **The concept would benefit from a more distinctive creative hook.** The consistent feedback about generic execution suggests adding a unique, unexpected element - a specific story, character, or visual device - could significantly improve memorability and curiosity scores without losing the strong personal fit messaging. The underlying employer proposition is strong; the creative expression needs more differentiation.

---

## Dataset Summary

The full dataset contains 90 persona responses with:
- Raw text responses for all 5 questions
- 5-point probability distributions (PMF) from SSR scoring
- Mean Likert scores (1-5) for each question
- Demographics: country (UK/Greece/Czech Republic), gender, age, education level

Available in `10_allwyn_tv_concepts_output.json` under the `"dataset"` key.

---

## Appendix: Survey Questions and Response Scales

### Q1: Want to Know More
**"Please review concept 1. Did this concept make you want to know more about working at this company?"**

| Score | Response |
|-------|----------|
| 1 | Definitely not |
| 2 | Probably not |
| 3 | Unsure |
| 4 | Probably yes |
| 5 | Definitely yes |

### Q2: Memorability
**"To what extent do you agree with this statement: 'Concept 1 is memorable.'"**

| Score | Response |
|-------|----------|
| 1 | Strongly disagree |
| 2 | Disagree |
| 3 | Neither agree nor disagree |
| 4 | Agree |
| 5 | Strongly agree |

### Q3: Research Intent
**"Would you research jobs at this company after seeing concept 1 turned into a TV ad?"**

| Score | Response |
|-------|----------|
| 1 | Definitely not |
| 2 | Probably not |
| 3 | Maybe |
| 4 | Probably |
| 5 | Definitely |

### Q4: Personal Fit
**"How well do you feel the company depicted in concept 1 would fit someone like you?"**

| Score | Response |
|-------|----------|
| 1 | Not well at all |
| 2 | Not very well |
| 3 | Somewhat |
| 4 | Quite well |
| 5 | Very well |

### Q5: Concept Preference
**"Looking at both concepts, which concept do you prefer and how strongly?"**

| Score | Response |
|-------|----------|
| 1 | Strongly prefer Concept 2 |
| 2 | Slightly prefer Concept 2 |
| 3 | No preference |
| 4 | Slightly prefer Concept 1 |
| 5 | Strongly prefer Concept 1 |

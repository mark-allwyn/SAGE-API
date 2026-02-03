# Experiment 12: Allwyn TV Ad Concepts (Async Concurrency)

## Test Overview

| Field | Value |
|-------|-------|
| **Concept Name** | Allwyn TV Ad Concepts |
| **Concept Type** | Text + Image (two TV ad concept storyboards, JPEG, base64-encoded) |
| **Personas Tested** | 90 adults across UK, Greece, and Czech Republic (ages 21-40, undergraduate degree or higher) |
| **Processing Time** | 82.7 seconds (~1.4 minutes) |
| **Providers** | openai/gpt-4o (generation + vision), openai/text-embedding-3-small (embedding) |
| **Purpose** | Verify async concurrency changes produce equivalent results to Experiment 11 |

---

## Concept Description

This is a **dual-concept comparison test** using both text and image inputs. The image contains two TV ad concept storyboards for the **Allwyn** brand - a lottery and gaming entertainment company.

- **Concept 1** (left): Focuses on contrasting the energy of startups with the stability of big firms, positioning Allwyn as offering "the best of both worlds." Features upbeat acoustic guitar music, dynamic office scenes, and a voiceover emphasising career growth.
- **Concept 2** (right): An alternative creative approach for the same Allwyn employer brand campaign.

Personas were asked to evaluate Concept 1 individually across four metrics, then compare both concepts in a preference question. This is a re-run of Experiment 11 with identical input data, using the new async concurrency pipeline (semaphore-based persona concurrency, parallel question processing, parallel SSR reference set processing).

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
| want_to_know_more | 20% | 3.48 | 0.620 | 0.124 |
| memorability | 20% | 3.22 | 0.555 | 0.111 |
| research_intent | 20% | 3.37 | 0.593 | 0.119 |
| personal_fit | 20% | 4.06 | 0.765 | 0.153 |
| concept_preference | 20% | 3.56 | 0.640 | 0.128 |

---

## Key Insights

### Strengths

1. **Personal Fit** (4.06) - The strongest performing metric by a large margin. 100% of personas rounded to rating 4, with 72% top-2-box. The concept's messaging about balancing startup energy with big-firm stability resonated universally across all three countries and demographics. Personas consistently described the depicted work environment as aligning with their career aspirations.

2. **Concept Preference** (3.56) - 90.0% of personas rated at level 4, indicating a clear preference for Concept 1 over Concept 2. Only 3 personas (3.3%) leaned towards Concept 2, and 6 (6.7%) expressed no preference. Personas described Concept 1 as "more dynamic," "more engaging," and having "clearer messaging."

3. **Want to Know More** (3.48) - Split between level 3 (33.3%) and level 4 (66.7%), showing moderate-to-good curiosity. The "best of both worlds" proposition was cited as the primary driver of interest, though some personas wanted more specifics about what makes Allwyn unique.

### Weaknesses

1. **Memorability** (3.22) - The lowest-scoring metric. 83.3% of responses clustered at level 3, suggesting the concept is perceived as competent but not distinctive. Multiple personas described it as "a bit generic" and "predictable," indicating the creative execution needs a more unique or surprising element to stand out from other corporate ads.

2. **Research Intent** (3.37) - Split between level 3 (48.9%) and level 4 (43.3%), with 7 personas (7.8%) rating at level 2. While above neutral, some personas - particularly those with higher education - expressed scepticism that the ad conveyed enough about Allwyn's uniqueness to motivate active job research.

---

## Metrics Summary

| Question | Mean | Median | Std Dev | Top 2 Box | Bottom 2 Box |
|----------|------|--------|---------|-----------|--------------|
| want_to_know_more | 3.48 | 3.59 | 0.32 | 2% | 0% |
| memorability | 3.22 | 3.15 | 0.35 | 2% | 0% |
| research_intent | 3.37 | 3.48 | 0.40 | 0% | 1% |
| personal_fit | 4.06 | 4.07 | 0.11 | 72% | 0% |
| concept_preference | 3.56 | 3.60 | 0.27 | 0% | 0% |

### Distribution Analysis (All Questions Combined)

| Rating | Count | Percentage |
|--------|-------|------------|
| 1 (Strongly Negative) | 0 | 0.0% |
| 2 (Negative) | 10 | 2.2% |
| 3 (Neutral) | 155 | 34.4% |
| 4 (Positive) | 285 | 63.3% |
| 5 (Strongly Positive) | 0 | 0.0% |

The distribution is heavily concentrated in the 3-4 range with zero extreme responses (1 or 5). Compared to Experiment 11, the distribution is nearly identical (Exp 11: 2.2% rating 2, 35.8% rating 3, 62.0% rating 4). The very low standard deviations (0.11-0.40) across all questions reinforce the pattern of consensus around moderate-positive sentiment. The absence of any level 5 responses suggests the concept reliably generates positive impressions but does not provoke strong enthusiasm.

---

## Sample Responses

### uk_f_01 (24y, F, United Kingdom, Undergraduate degree)

**Want to Know More (3.09):**
> "Concept 1 does a decent job of highlighting the benefits of working at Allwyn by combining elements of startup energy and big firm stability. However, the voiceover and scene descriptions feel a bit generic."

**Memorability (3.20):**
> "I somewhat agree that Concept 1 is memorable. The contrast between startups and big firms is clear, and the upbeat music adds energy. However, it might need a more unique angle to truly stand out."

**Concept Preference (3.61):**
> "I prefer Concept 1. It feels more dynamic and engaging with the upbeat music and clear narrative. The contrast between startups and big firms is presented in a way that's easy to follow."

---

### uk_m_01 (34y, M, United Kingdom, Postgraduate degree)

**Want to Know More (3.05):**
> "Concept 1 is quite engaging with its dynamic visuals and contrasting depictions of startups and big firms. The idea of combining startup energy with big firm stability is appealing. However, it feels somewhat generic."

**Concept Preference (3.73):**
> "I prefer Concept 1. It seems more dynamic and engaging, with a clearer contrast between startups and big firms. The upbeat acoustic guitar and the voiceover give a positive vibe, making it more appealing."

---

### gr_f_01 (28y, F, Greece, Postgraduate degree)

**Want to Know More (3.60):**
> "Concept 1 presents an intriguing blend of startup energy and big firm stability, which is appealing. The upbeat music and dynamic visuals create a positive impression. However, I'd like to see more specifics."

**Memorability (2.80):**
> "I somewhat agree that Concept 1 is memorable. The use of contrasting scenes between startups and big firms creates a clear visual and thematic narrative. However, the scenes and narrative aren't particularly unique."

---

### gr_m_01 (28y, M, Greece, Undergraduate degree)

**Want to Know More (3.37):**
> "Concept 1 did catch my attention with its dynamic comparison between startups and big firms, emphasizing the blend of energy and stability. The upbeat music and positive voiceover made it appealing."

**Personal Fit (4.14):**
> "As someone who enjoys the dynamic environment of startups but also values stability, Concept 1 seems appealing. The mix of startup energy with big firm stability sounds like a great fit for me."

---

### cz_f_01 (36y, F, Czech Republic, Undergraduate degree)

**Memorability (3.82):**
> "I somewhat agree that Concept 1 is memorable. The use of contrasting visuals and sounds between startups and big firms creates a clear and engaging narrative. The upbeat music and dynamic scenes are likely to stick."

**Concept Preference (3.56):**
> "I prefer Concept 1 because it feels more dynamic and engaging. The upbeat music and clear comparison between startups and big firms make it appealing. The message about getting the best of both worlds resonates."

---

### cz_m_01 (21y, M, Czech Republic, Doctorate)

**Want to Know More (2.76):**
> "Concept 1 presents a clear comparison between startups and big firms, highlighting a balance of energy and stability. The upbeat music and visuals are engaging, but it feels a bit generic. It doesn't quite make me eager to know more."

**Concept Preference (3.71):**
> "I prefer Concept 1. It feels more dynamic and engaging, with a nice balance of startup energy and big firm stability. The overall tone and visuals seem more appealing and polished."

---

## Comparison: Experiment 11 vs Experiment 12

This experiment validates the async concurrency pipeline changes. The input data is identical to Experiment 11.

### Performance

| Metric | Exp 11 | Exp 12 | Change |
|--------|--------|--------|--------|
| **Processing Time** | 293.5s | 82.7s | **3.55x faster** |

### Accuracy (per-question means)

| Question | Exp 11 | Exp 12 | Difference |
|----------|--------|--------|------------|
| want_to_know_more | 3.470 | 3.480 | +0.010 |
| memorability | 3.180 | 3.220 | +0.040 |
| research_intent | 3.410 | 3.370 | -0.040 |
| personal_fit | 4.040 | 4.060 | +0.020 |
| concept_preference | 3.550 | 3.560 | +0.010 |
| **Composite Score** | **0.633** | **0.635** | **+0.002** |

All per-question means differ by less than 0.04 points, well within the expected stochastic variation from LLM generation. The composite score differs by 0.002. Both experiments produce the same pass/fail verdict.

### Conclusion

The async concurrency changes reduce processing time by 3.55x (from ~5 minutes to ~1.4 minutes) with no meaningful impact on result accuracy. The pipeline changes are validated.

---

## Conclusions

1. **The concept passed the threshold test with a moderate margin.** The composite score of 0.635 exceeded the 0.55 threshold by 8.5%. This is consistent with Experiment 11's result (0.633, +8.3%) and Experiment 10's result (0.635, +8.5%), demonstrating good reproducibility across runs.

2. **Personal fit remains the standout strength.** At 4.06 (vs. 4.04 in Experiment 11), this was again the only metric to consistently achieve level 4 ratings. The "best of both worlds" employer value proposition resonated strongly and consistently across all demographics, genders, and education levels.

3. **Memorability continues to be the primary concern.** At 3.22 (vs. 3.18 in Experiment 11), this remains the weakest metric. Personas repeatedly described the concept as "generic" and "predictable," lacking a distinctive hook to differentiate it from other corporate recruitment advertising.

4. **Concept 1 is the clear winner.** 90.0% of personas preferred Concept 1 (vs. 84.4% in Experiment 11), with only 3.3% favouring Concept 2. The preference was consistent across all three countries.

5. **The async concurrency pipeline is validated.** Processing time dropped from 293.5s to 82.7s (3.55x speedup) with no meaningful change in results. All per-question means differ by less than 0.04 points from Experiment 11.

---

## Dataset Summary

The full dataset contains 90 persona responses with:
- Raw text responses for all 5 questions
- 5-point probability distributions (PMF) from SSR scoring
- Mean Likert scores (1-5) for each question
- Demographics: country (UK/Greece/Czech Republic), gender, age, education level

Available in `12_allwyn_tv_concepts_output.json` under the `"dataset"` key.

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

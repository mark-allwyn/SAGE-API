# Experiment 08: JackpotJoe Lottery - The Talking Dog Ad

## Test Overview

| Field | Value |
|-------|-------|
| **Concept Name** | JackpotJoe Lottery - The Talking Dog Ad |
| **Personas Tested** | 50 working-class adults |
| **Processing Time** | 141.7 seconds |
| **Providers** | OpenAI GPT-4o (generation), text-embedding-3-small (embeddings) |

---

## Input JSON Structure

The input consists of three main sections:

### 1. Personas (50 synthetic consumers)
```json
{
  "personas": [
    {"persona_id": "worker_01", "age": 35, "gender": "M", "income": "medium", "location": "suburban", "interests": ["sports", "family", "cars"]},
    {"persona_id": "worker_02", "age": 38, "gender": "F", "income": "medium", "location": "urban", "interests": ["cooking", "shopping", "lottery"]},
    ...
  ]
}
```

### 2. Concept (Ad Description)
```json
{
  "concept": {
    "name": "JackpotJoe Lottery - The Talking Dog Ad",
    "content": [
      {
        "type": "text",
        "data": "TV Advertisement Concept for JackpotJoe Lottery - 'The Talking Dog': This humorous 30-second ad opens on Dave, a regular guy in his 40s, sitting on his worn couch watching TV with his scruffy mutt, Biscuit. Dave sighs and says 'Man, I wish I could quit my job.' Suddenly, Biscuit turns to him and speaks in a deep, sophisticated British accent: 'Well David, have you considered the JackpotJoe Lottery?'..."
      }
    ]
  }
}
```

### 3. Survey Configuration (10 Questions with SSR Reference Sets)
```json
{
  "survey_config": {
    "questions": [
      {
        "id": "ad_enjoyment",
        "text": "How likely is it you would enjoy watching this ad each time you saw it on television?",
        "weight": 0.1,
        "ssr_reference_sets": [
          ["Extremely unlikely", "Not likely", "Maybe", "Likely", "Extremely likely"],
          ["Definitely would not enjoy", "Probably would not enjoy", "Might enjoy", "Probably would enjoy", "Definitely would enjoy"],
          ...
        ]
      },
      ...
    ]
  },
  "threshold": 0.55,
  "output_dataset": true
}
```

---

## Output JSON

### Result Summary
```json
{
  "result": {
    "passed": false,
    "composite_score": 0.547,
    "threshold": 0.55,
    "margin": -0.003,
    "reason": "FAIL: Composite score 0.547 is below threshold 0.55"
  }
}
```

### Metrics by Question
```json
{
  "metrics": {
    "ad_enjoyment": {
      "n": 50,
      "mean": 2.86,
      "median": 2.79,
      "std_dev": 0.42,
      "top_2_box": 0.0,
      "bottom_2_box": 0.02,
      "distribution": {"1": 0, "2": 10, "3": 34, "4": 6, "5": 0}
    },
    "brand_recognition": {
      "n": 50,
      "mean": 3.66,
      "median": 3.7,
      "std_dev": 0.28,
      "top_2_box": 0.14,
      "bottom_2_box": 0.0,
      "distribution": {"1": 0, "2": 0, "3": 11, "4": 39, "5": 0}
    },
    "purchase_intent": {
      "n": 50,
      "mean": 3.26,
      "median": 3.37,
      "std_dev": 0.42,
      "top_2_box": 0.0,
      "bottom_2_box": 0.0,
      "distribution": {"1": 0, "2": 1, "3": 29, "4": 20, "5": 0}
    },
    "website_visit": {
      "n": 50,
      "mean": 3.0,
      "median": 2.87,
      "std_dev": 0.56,
      "top_2_box": 0.04,
      "bottom_2_box": 0.0,
      "distribution": {"1": 0, "2": 11, "3": 26, "4": 13, "5": 0}
    },
    "word_of_mouth": {
      "n": 50,
      "mean": 3.46,
      "median": 3.56,
      "std_dev": 0.41,
      "top_2_box": 0.04,
      "bottom_2_box": 0.0,
      "distribution": {"1": 0, "2": 4, "3": 16, "4": 30, "5": 0}
    },
    "differentiation": {
      "n": 50,
      "mean": 3.27,
      "median": 3.34,
      "std_dev": 0.31,
      "top_2_box": 0.0,
      "bottom_2_box": 0.0,
      "distribution": {"1": 0, "2": 0, "3": 35, "4": 15, "5": 0}
    },
    "personal_fit": {
      "n": 50,
      "mean": 2.45,
      "median": 2.29,
      "std_dev": 0.52,
      "top_2_box": 0.0,
      "bottom_2_box": 0.22,
      "distribution": {"1": 0, "2": 31, "3": 17, "4": 2, "5": 0}
    },
    "character_appeal": {
      "n": 50,
      "mean": 3.42,
      "median": 3.59,
      "std_dev": 0.46,
      "top_2_box": 0.0,
      "bottom_2_box": 0.0,
      "distribution": {"1": 0, "2": 3, "3": 15, "4": 32, "5": 0}
    },
    "story_appeal": {
      "n": 50,
      "mean": 3.09,
      "median": 3.26,
      "std_dev": 0.68,
      "top_2_box": 0.02,
      "bottom_2_box": 0.02,
      "distribution": {"1": 0, "2": 14, "3": 17, "4": 19, "5": 0}
    },
    "overall_liking": {
      "n": 50,
      "mean": 3.43,
      "median": 3.69,
      "std_dev": 0.7,
      "top_2_box": 0.28,
      "bottom_2_box": 0.0,
      "distribution": {"1": 0, "2": 8, "3": 13, "4": 29, "5": 0}
    }
  }
}
```

---

## Analysis Report

### Overall Result: FAILED (Marginal)

| Metric | Value |
|--------|-------|
| **Composite Score** | 0.547 |
| **Threshold** | 0.55 |
| **Margin** | -0.003 |
| **Verdict** | FAIL (by 0.3%) |

### Criteria Breakdown

| Question | Weight | Raw Mean | Normalized | Contribution |
|----------|--------|----------|------------|--------------|
| ad_enjoyment | 10% | 2.86 | 0.465 | 0.046 |
| brand_recognition | 10% | 3.66 | 0.665 | 0.067 |
| purchase_intent | 10% | 3.26 | 0.565 | 0.056 |
| website_visit | 10% | 3.00 | 0.500 | 0.050 |
| word_of_mouth | 10% | 3.46 | 0.615 | 0.061 |
| differentiation | 10% | 3.27 | 0.568 | 0.057 |
| personal_fit | 10% | 2.45 | 0.363 | **0.036** |
| character_appeal | 10% | 3.42 | 0.605 | 0.060 |
| story_appeal | 10% | 3.09 | 0.522 | 0.052 |
| overall_liking | 10% | 3.43 | 0.608 | 0.061 |

### Key Insights

**Strengths:**
- **Brand Recognition** (3.66) - Highest scoring metric. The "JackpotJoe" name and talking dog mascot create strong brand linkage
- **Word of Mouth** (3.46) - People would talk about this ad with friends due to its humor
- **Character Appeal** (3.42) - The talking dog Biscuit resonates with audiences
- **Overall Liking** (3.43) - Generally positive reception

**Weaknesses:**
- **Personal Fit** (2.45) - Lowest score. Many personas don't identify with lottery advertising regardless of creativity
- **Ad Enjoyment** (2.86) - Repeat viewing fatigue concern
- **Website Visit** (3.00) - Neutral intent to engage digitally

### Distribution Analysis

| Rating | Count | Percentage |
|--------|-------|------------|
| 1 (Strongly Negative) | 0 | 0.0% |
| 2 (Negative) | 82 | 16.4% |
| 3 (Neutral) | 213 | 42.6% |
| 4 (Positive) | 205 | 41.0% |
| 5 (Strongly Positive) | 0 | 0.0% |

---

## Sample Responses

### worker_01 (35y, Male, Medium Income, Suburban)
*Interests: sports, family, cars*

**Ad Enjoyment (2.50):**
> "I'd probably get a good chuckle out of this ad the first few times I see it. The idea of a talking dog with a British accent is funny, and I appreciate the humor. However, I'm not really into playing the lottery, so it might not hold my interest for long."

**Purchase Intent (2.79):**
> "Honestly, I got a good laugh out of the ad with the talking dog and all, but I'm not really into playing the lottery. The odds are just too slim for my liking, and I'd rather spend my money on something more tangible, like a new accessory for my car or a family outing."

---

### worker_02 (38y, Female, Medium Income, Urban)
*Interests: cooking, shopping, lottery*

**Ad Enjoyment (2.59):**
> "Honestly, I'd probably get a kick out of this ad the first few times I saw it. The talking dog with a British accent sounds funny and unexpected, and I appreciate the self-aware humor about the odds. But if it were on all the time, I might get a bit tired of it."

**Purchase Intent (3.78):**
> "Honestly, I think the ad is pretty amusing with its talking dog and all. I do enjoy playing the lottery now and then, so it might just remind me to grab a ticket the next time I'm out shopping."

---

### worker_09 (53y, Male, Low Income, Rural)
*Interests: hunting, NASCAR, lottery*

**Overall Score: 3.58** - Above average engagement from existing lottery player

---

## Generated Dataset (50 rows)

| persona_id | age | gender | income | location | ad_enjoyment | brand_recog | purchase_intent | website_visit | word_of_mouth | differentiation | personal_fit | character_appeal | story_appeal | overall_liking |
|------------|-----|--------|--------|----------|--------------|-------------|-----------------|---------------|---------------|-----------------|--------------|------------------|--------------|----------------|
| worker_01 | 35 | M | medium | suburban | 2.5 | 3.88 | 2.79 | 2.88 | 3.68 | 3.14 | 2.03 | 3.61 | 2.39 | 3.07 |
| worker_02 | 38 | F | medium | urban | 2.59 | 3.96 | 3.78 | 4.27 | 4.05 | 3.64 | 2.87 | 3.81 | 3.85 | 4.09 |
| worker_03 | 42 | M | low | suburban | 2.71 | 3.65 | 3.03 | 2.77 | 2.47 | 2.83 | 2.66 | 3.7 | 2.67 | 4.02 |
| worker_04 | 45 | F | medium | rural | 2.25 | 3.26 | 2.71 | 2.1 | 2.41 | 2.86 | 2.07 | 2.58 | 2.04 | 2.7 |
| worker_05 | 37 | M | low | urban | 2.82 | 3.61 | 2.5 | 2.27 | 3.71 | 2.78 | 1.91 | 2.73 | 2.03 | 2.7 |
| worker_06 | 51 | F | medium | suburban | 2.46 | 3.69 | 3.43 | 2.55 | 3.44 | 2.99 | 1.82 | 2.95 | 3.56 | 2.15 |
| worker_07 | 48 | M | medium | suburban | 2.6 | 3.53 | 3.57 | 2.76 | 3.32 | 3.1 | 3.01 | 3.64 | 2.73 | 3.69 |
| worker_08 | 36 | F | low | urban | 2.35 | 3.35 | 2.81 | 2.22 | 3.58 | 3.67 | 1.7 | 3.36 | 2.11 | 3.01 |
| worker_09 | 53 | M | low | rural | 3.0 | 3.8 | 3.63 | 3.86 | 4.0 | 3.1 | 2.95 | 3.34 | 3.57 | 3.98 |
| worker_10 | 40 | F | medium | suburban | 2.73 | 3.79 | 2.98 | 3.06 | 3.63 | 3.04 | 2.39 | 3.14 | 3.65 | 2.23 |
| worker_11 | 44 | M | medium | urban | 3.01 | 3.97 | 3.15 | 2.67 | 3.75 | 3.5 | 1.81 | 3.9 | 3.58 | 2.32 |
| worker_12 | 39 | F | low | suburban | 3.49 | 3.75 | 3.92 | 3.71 | 3.49 | 3.46 | 2.39 | 3.69 | 2.08 | 3.96 |
| worker_13 | 55 | M | medium | rural | 2.35 | 2.87 | 3.1 | 2.6 | 2.37 | 2.95 | 2.79 | 2.05 | 3.48 | 2.22 |
| worker_14 | 41 | F | medium | urban | 2.7 | 3.91 | 2.65 | 2.43 | 3.54 | 3.63 | 2.03 | 3.36 | 3.11 | 4.05 |
| worker_15 | 47 | M | low | suburban | 3.39 | 3.54 | 3.69 | 3.65 | 3.36 | 3.49 | 3.13 | 3.87 | 3.92 | 3.9 |
| worker_16 | 36 | F | medium | suburban | 2.9 | 3.69 | 3.09 | 2.37 | 3.55 | 3.26 | 1.94 | 3.57 | 2.52 | 2.57 |
| worker_17 | 50 | M | medium | urban | 2.79 | 3.77 | 3.6 | 3.68 | 3.28 | 3.22 | 2.7 | 3.58 | 3.7 | 3.96 |
| worker_18 | 43 | F | low | rural | 3.02 | 3.46 | 3.31 | 2.45 | 2.9 | 2.56 | 2.29 | 3.9 | 3.25 | 2.58 |
| worker_19 | 38 | M | medium | suburban | 2.84 | 3.76 | 3.13 | 2.99 | 3.23 | 2.95 | 3.44 | 3.6 | 3.88 | 3.83 |
| worker_20 | 52 | F | medium | suburban | 2.88 | 3.7 | 3.68 | 4.02 | 3.97 | 3.32 | 2.81 | 3.52 | 3.77 | 4.07 |
| worker_21 | 35 | M | low | urban | 2.62 | 4.04 | 2.64 | 2.45 | 2.26 | 2.77 | 2.02 | 2.92 | 1.75 | 2.32 |
| worker_22 | 46 | F | medium | suburban | 2.8 | 3.58 | 3.14 | 2.65 | 3.62 | 3.44 | 2.46 | 3.08 | 3.73 | 3.69 |
| worker_23 | 49 | M | medium | rural | 3.85 | 3.72 | 3.68 | 3.35 | 3.92 | 3.42 | 3.32 | 3.64 | 3.48 | 4.09 |
| worker_24 | 37 | F | low | urban | 2.77 | 3.24 | 3.09 | 2.43 | 3.15 | 3.34 | 1.94 | 2.32 | 2.26 | 3.24 |
| worker_25 | 54 | M | low | suburban | 2.7 | 3.94 | 3.46 | 3.37 | 3.25 | 3.02 | 1.93 | 3.79 | 3.53 | 3.94 |
| worker_26 | 40 | F | medium | suburban | 2.89 | 4.09 | 2.97 | 2.09 | 3.43 | 2.89 | 2.22 | 3.79 | 3.44 | 3.64 |
| worker_27 | 45 | M | medium | urban | 2.62 | 3.91 | 3.47 | 3.06 | 3.53 | 3.58 | 2.28 | 3.63 | 3.83 | 3.93 |
| worker_28 | 42 | F | low | rural | 2.83 | 4.02 | 3.8 | 3.21 | 3.68 | 3.35 | 3.44 | 3.38 | 3.02 | 4.06 |
| worker_29 | 36 | M | medium | suburban | 2.65 | 4.0 | 3.47 | 2.86 | 3.66 | 3.39 | 2.17 | 3.72 | 3.9 | 3.39 |
| worker_30 | 51 | F | medium | suburban | 2.44 | 3.28 | 2.86 | 2.53 | 3.65 | 3.54 | 2.23 | 3.5 | 2.2 | 3.68 |
| worker_31 | 48 | M | low | urban | 3.17 | 3.27 | 3.69 | 3.73 | 3.13 | 3.39 | 2.7 | 3.65 | 3.77 | 4.11 |
| worker_32 | 39 | F | medium | suburban | 2.77 | 3.5 | 2.64 | 3.72 | 3.67 | 3.54 | 1.9 | 2.85 | 2.12 | 2.01 |
| worker_33 | 55 | M | medium | rural | 1.95 | 3.23 | 2.74 | 2.57 | 3.47 | 2.77 | 2.04 | 2.94 | 3.22 | 2.22 |
| worker_34 | 41 | F | low | urban | 3.21 | 3.39 | 3.64 | 3.64 | 3.8 | 3.29 | 3.5 | 3.99 | 3.62 | 3.94 |
| worker_35 | 44 | M | medium | suburban | 2.8 | 3.81 | 2.67 | 3.22 | 3.62 | 3.36 | 2.01 | 3.75 | 2.43 | 3.59 |
| worker_36 | 38 | F | medium | suburban | 2.94 | 3.78 | 2.68 | 2.91 | 3.53 | 3.5 | 1.91 | 3.73 | 2.28 | 2.38 |
| worker_37 | 53 | M | low | rural | 3.63 | 3.64 | 3.53 | 3.91 | 3.91 | 3.34 | 2.72 | 3.71 | 3.72 | 4.1 |
| worker_38 | 40 | F | medium | urban | 3.12 | 3.5 | 3.53 | 2.74 | 3.83 | 3.59 | 3.35 | 3.74 | 2.81 | 4.01 |
| worker_39 | 47 | M | medium | suburban | 2.94 | 3.56 | 3.52 | 2.93 | 3.46 | 3.69 | 2.39 | 3.39 | 3.22 | 3.97 |
| worker_40 | 35 | F | low | suburban | 3.51 | 3.64 | 3.43 | 3.96 | 3.88 | 3.67 | 3.53 | 3.59 | 4.08 | 4.16 |
| worker_41 | 50 | M | medium | urban | 2.73 | 3.6 | 2.54 | 2.59 | 3.72 | 3.33 | 2.91 | 2.74 | 3.28 | 4.06 |
| worker_42 | 43 | F | medium | rural | 2.26 | 3.7 | 2.82 | 2.41 | 2.8 | 2.78 | 2.0 | 2.28 | 2.07 | 2.87 |
| worker_43 | 37 | M | low | urban | 3.66 | 4.05 | 3.94 | 3.76 | 3.71 | 3.72 | 3.16 | 3.93 | 3.67 | 4.11 |
| worker_44 | 52 | F | medium | suburban | 2.3 | 2.93 | 3.59 | 2.48 | 3.57 | 2.68 | 1.99 | 3.13 | 2.22 | 3.36 |
| worker_45 | 46 | M | medium | suburban | 2.65 | 3.51 | 3.86 | 2.71 | 3.72 | 3.4 | 2.26 | 3.56 | 3.38 | 2.62 |
| worker_46 | 39 | F | low | urban | 3.74 | 3.73 | 3.56 | 2.85 | 3.77 | 3.55 | 2.29 | 3.81 | 3.48 | 3.98 |
| worker_47 | 54 | M | low | rural | 3.64 | 4.05 | 3.68 | 3.55 | 3.53 | 3.39 | 2.55 | 3.7 | 3.16 | 4.07 |
| worker_48 | 41 | F | medium | suburban | 2.78 | 4.02 | 2.82 | 3.13 | 3.28 | 3.5 | 2.11 | 3.75 | 2.83 | 3.24 |
| worker_49 | 49 | M | medium | urban | 2.49 | 3.78 | 3.57 | 2.67 | 3.22 | 3.09 | 2.05 | 3.63 | 2.07 | 3.38 |
| worker_50 | 36 | F | low | suburban | 3.12 | 3.32 | 3.3 | 3.17 | 3.64 | 3.55 | 2.44 | 3.5 | 3.99 | 4.02 |

---

## Conclusions

1. **The ad narrowly failed** the 0.55 threshold by just 0.3%, indicating it's a borderline concept

2. **Brand recognition is strong** (3.66) - the talking dog creates memorable brand linkage

3. **Personal fit is the weak point** (2.45) - many working-class personas don't see themselves as lottery players regardless of ad creativity

4. **Shareability is high** - word of mouth (3.46) suggests the humor would drive organic discussion

5. **Recommendation:** Consider targeting personas with existing lottery interest, or adjusting the creative to broaden personal relevance

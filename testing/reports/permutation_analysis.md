# Bedrock Model Permutation Analysis

Analysis of how consistently different model permutations produce similar results. The goal is not to rank models by score, but to identify which permutations agree with each other and which are outliers - then tie that to cost.

**Experiments analysed**: 36 of 36
**Base input**: Experiment 14 (90 personas, 5 questions, concept with images)

---

## A. All Results - Deviation from Median

**Median composite score**: 0.5025 | **Std Dev**: 0.0648

Each permutation's composite score is compared to the group median. Z-score shows how many standard deviations away from the median. Sorted by score for readability.

| Exp | Vision Model | Embedding | Score | Deviation | Z-Score | Est. Cost | Time (s) |
|-----|-------------|-----------|------:|------:|------:|------:|------:|
| 29 | Sonnet 3 | Cohere EN | 0.3310 | -0.1715 | -2.65 | $5.81 | 290 |
| 30 | Sonnet 3 | Cohere Multi | 0.3340 | -0.1685 | -2.60 | $5.81 | 283 |
| 27 | Sonnet 3 | Titan v2 | 0.3800 | -0.1225 | -1.89 | $5.81 | 318 |
| 34 | Haiku 4.5 | Cohere Multi | 0.4230 | -0.0795 | -1.23 | $1.94 | 98 |
| 33 | Haiku 4.5 | Cohere EN | 0.4240 | -0.0785 | -1.21 | $1.94 | 102 |
| 26 | Sonnet 3.7 | Cohere Multi | 0.4270 | -0.0755 | -1.17 | $5.81 | 101 |
| 31 | Haiku 4.5 | Titan v2 | 0.4320 | -0.0705 | -1.09 | $1.94 | 139 |
| 25 | Sonnet 3.7 | Cohere EN | 0.4360 | -0.0665 | -1.03 | $5.81 | 171 |
| 19 | Sonnet 4.5 | Titan v2 | 0.4530 | -0.0495 | -0.76 | $5.81 | 123 |
| 21 | Sonnet 4.5 | Cohere EN | 0.4590 | -0.0435 | -0.67 | $5.81 | 195 |
| 16 | Opus 4.5 | Titan v1 | 0.4650 | -0.0375 | -0.58 | $9.68 | 157 |
| 22 | Sonnet 4.5 | Cohere Multi | 0.4700 | -0.0325 | -0.50 | $5.81 | 116 |
| 23 | Sonnet 3.7 | Titan v2 | 0.4700 | -0.0325 | -0.50 | $5.81 | 622 |
| 43 | Nova Lite | Titan v2 | 0.4850 | -0.0175 | -0.27 | $0.11 | 85 |
| 39 | Nova Pro | Titan v2 | 0.4920 | -0.0105 | -0.16 | $1.38 | 98 |
| 38 | Haiku 3 | Cohere Multi | 0.4980 | -0.0045 | -0.07 | $0.49 | 97 |
| 15 | Opus 4.5 | Titan v2 | 0.4990 | -0.0035 | -0.05 | $9.68 | 166 |
| 20 | Sonnet 4.5 | Titan v1 | 0.5020 | -0.0005 | -0.01 | $5.81 | 176 |
| 17 | Opus 4.5 | Cohere EN | 0.5030 | +0.0005 | +0.01 | $9.68 | 137 |
| 46 | Nova Lite | Cohere Multi | 0.5030 | +0.0005 | +0.01 | $0.11 | 74 |
| 35 | Haiku 3 | Titan v2 | 0.5080 | +0.0055 | +0.08 | $0.49 | 97 |
| 45 | Nova Lite | Cohere EN | 0.5100 | +0.0075 | +0.12 | $0.11 | 76 |
| 47 | Nova 2 Lite | Titan v2 | 0.5140 | +0.0115 | +0.18 | $0.08 | 164 |
| 32 | Haiku 4.5 | Titan v1 | 0.5200 | +0.0175 | +0.27 | $1.94 | 132 |
| 18 | Opus 4.5 | Cohere Multi | 0.5210 | +0.0185 | +0.29 | $9.68 | 132 |
| 42 | Nova Pro | Cohere Multi | 0.5320 | +0.0295 | +0.46 | $1.38 | 84 |
| 28 | Sonnet 3 | Titan v1 | 0.5350 | +0.0325 | +0.50 | $5.81 | 303 |
| 24 | Sonnet 3.7 | Titan v1 | 0.5400 | +0.0375 | +0.58 | $5.81 | 620 |
| 44 | Nova Lite | Titan v1 | 0.5530 | +0.0505 | +0.78 | $0.11 | 79 |
| 36 | Haiku 3 | Titan v1 | 0.5540 | +0.0515 | +0.80 | $0.49 | 93 |
| 40 | Nova Pro | Titan v1 | 0.5600 | +0.0575 | +0.89 | $1.38 | 84 |
| 37 | Haiku 3 | Cohere EN | 0.5620 | +0.0595 | +0.92 | $0.49 | 92 |
| 41 | Nova Pro | Cohere EN | 0.5650 | +0.0625 | +0.97 | $1.38 | 142 |
| 48 | Nova 2 Lite | Titan v1 | 0.5710 | +0.0685 | +1.06 | $0.08 | 119 |
| 50 | Nova 2 Lite | Cohere Multi | 0.5780 | +0.0755 | +1.17 | $0.08 | 82 |
| 49 | Nova 2 Lite | Cohere EN | 0.6090 | +0.1065 | +1.64 | $0.08 | 86 |

## B. Consensus Cluster vs Outliers

Using per-question score profiles (5-dimensional vector per experiment), we compute the centroid and flag experiments more than 1.5 std devs from the centroid as outliers.

**Centroid** (mean of means per question): want_to_know_more=2.889, memorability=3.010, research_intent=2.797, personal_fit=3.161, concept_preference=2.984

**Mean distance from centroid**: 0.776 | **Std Dev**: 0.345 | **Threshold (mean + 1.5 * std)**: 1.293

### Consensus group (33 permutations)

These permutations produce similar results to each other (within 1.5 std devs of the group centroid).

| Exp | Vision Model | Embedding | Score | Dist from Centroid | Est. Cost |
|-----|-------------|-----------|------:|------:|------:|
| 15 | Opus 4.5 | Titan v2 | 0.4990 | 0.168 | $9.68 |
| 16 | Opus 4.5 | Titan v1 | 0.4650 | 0.455 | $9.68 |
| 17 | Opus 4.5 | Cohere EN | 0.5030 | 0.556 | $9.68 |
| 18 | Opus 4.5 | Cohere Multi | 0.5210 | 0.618 | $9.68 |
| 19 | Sonnet 4.5 | Titan v2 | 0.4530 | 0.573 | $5.81 |
| 20 | Sonnet 4.5 | Titan v1 | 0.5020 | 0.413 | $5.81 |
| 21 | Sonnet 4.5 | Cohere EN | 0.4590 | 0.860 | $5.81 |
| 22 | Sonnet 4.5 | Cohere Multi | 0.4700 | 0.576 | $5.81 |
| 23 | Sonnet 3.7 | Titan v2 | 0.4700 | 0.489 | $5.81 |
| 24 | Sonnet 3.7 | Titan v1 | 0.5400 | 0.552 | $5.81 |
| 25 | Sonnet 3.7 | Cohere EN | 0.4360 | 0.942 | $5.81 |
| 26 | Sonnet 3.7 | Cohere Multi | 0.4270 | 1.034 | $5.81 |
| 27 | Sonnet 3 | Titan v2 | 0.3800 | 1.200 | $5.81 |
| 28 | Sonnet 3 | Titan v1 | 0.5350 | 0.493 | $5.81 |
| 31 | Haiku 4.5 | Titan v2 | 0.4320 | 0.604 | $1.94 |
| 32 | Haiku 4.5 | Titan v1 | 0.5200 | 0.540 | $1.94 |
| 33 | Haiku 4.5 | Cohere EN | 0.4240 | 0.958 | $1.94 |
| 34 | Haiku 4.5 | Cohere Multi | 0.4230 | 0.807 | $1.94 |
| 35 | Haiku 3 | Titan v2 | 0.5080 | 0.690 | $0.49 |
| 36 | Haiku 3 | Titan v1 | 0.5540 | 0.574 | $0.49 |
| 37 | Haiku 3 | Cohere EN | 0.5620 | 1.257 | $0.49 |
| 38 | Haiku 3 | Cohere Multi | 0.4980 | 1.081 | $0.49 |
| 39 | Nova Pro | Titan v2 | 0.4920 | 0.334 | $1.38 |
| 40 | Nova Pro | Titan v1 | 0.5600 | 0.684 | $1.38 |
| 41 | Nova Pro | Cohere EN | 0.5650 | 1.029 | $1.38 |
| 42 | Nova Pro | Cohere Multi | 0.5320 | 1.157 | $1.38 |
| 43 | Nova Lite | Titan v2 | 0.4850 | 0.560 | $0.11 |
| 44 | Nova Lite | Titan v1 | 0.5530 | 0.856 | $0.11 |
| 45 | Nova Lite | Cohere EN | 0.5100 | 0.716 | $0.11 |
| 46 | Nova Lite | Cohere Multi | 0.5030 | 0.514 | $0.11 |
| 47 | Nova 2 Lite | Titan v2 | 0.5140 | 0.378 | $0.08 |
| 48 | Nova 2 Lite | Titan v1 | 0.5710 | 0.783 | $0.08 |
| 50 | Nova 2 Lite | Cohere Multi | 0.5780 | 0.932 | $0.08 |

### Outliers (3 permutations)

These permutations deviate significantly from the group consensus.

| Exp | Vision Model | Embedding | Score | Dist from Centroid | Est. Cost |
|-----|-------------|-----------|------:|------:|------:|
| 29 | Sonnet 3 | Cohere EN | 0.3310 | 1.562 | $5.81 |
| 30 | Sonnet 3 | Cohere Multi | 0.3340 | 1.652 | $5.81 |
| 49 | Nova 2 Lite | Cohere EN | 0.6090 | 1.328 | $0.08 |

## C. Cost-Efficiency Analysis

Among the consensus group, which permutations are cheapest? Since these permutations all produce similar results, the cheapest one is the most cost-efficient.

| Rank | Exp | Vision Model | Embedding | Score | Dist from Centroid | Est. Cost | Time (s) |
|------|-----|-------------|-----------|------:|------:|------:|------:|
| 1 | 48 | Nova 2 Lite | Titan v1 | 0.5710 | 0.783 | $0.08 | 119 |
| 2 | 50 | Nova 2 Lite | Cohere Multi | 0.5780 | 0.932 | $0.08 | 82 |
| 3 | 47 | Nova 2 Lite | Titan v2 | 0.5140 | 0.378 | $0.08 | 164 |
| 4 | 44 | Nova Lite | Titan v1 | 0.5530 | 0.856 | $0.11 | 79 |
| 5 | 45 | Nova Lite | Cohere EN | 0.5100 | 0.716 | $0.11 | 76 |
| 6 | 46 | Nova Lite | Cohere Multi | 0.5030 | 0.514 | $0.11 | 74 |
| 7 | 43 | Nova Lite | Titan v2 | 0.4850 | 0.560 | $0.11 | 85 |
| 8 | 36 | Haiku 3 | Titan v1 | 0.5540 | 0.574 | $0.49 | 93 |
| 9 | 37 | Haiku 3 | Cohere EN | 0.5620 | 1.257 | $0.49 | 92 |
| 10 | 38 | Haiku 3 | Cohere Multi | 0.4980 | 1.081 | $0.49 | 97 |
| 11 | 35 | Haiku 3 | Titan v2 | 0.5080 | 0.690 | $0.49 | 97 |
| 12 | 40 | Nova Pro | Titan v1 | 0.5600 | 0.684 | $1.38 | 84 |
| 13 | 41 | Nova Pro | Cohere EN | 0.5650 | 1.029 | $1.38 | 142 |
| 14 | 42 | Nova Pro | Cohere Multi | 0.5320 | 1.157 | $1.38 | 84 |
| 15 | 39 | Nova Pro | Titan v2 | 0.4920 | 0.334 | $1.38 | 98 |
| 16 | 32 | Haiku 4.5 | Titan v1 | 0.5200 | 0.540 | $1.94 | 132 |
| 17 | 33 | Haiku 4.5 | Cohere EN | 0.4240 | 0.958 | $1.94 | 102 |
| 18 | 34 | Haiku 4.5 | Cohere Multi | 0.4230 | 0.807 | $1.94 | 98 |
| 19 | 31 | Haiku 4.5 | Titan v2 | 0.4320 | 0.604 | $1.94 | 139 |
| 20 | 20 | Sonnet 4.5 | Titan v1 | 0.5020 | 0.413 | $5.81 | 176 |
| 21 | 21 | Sonnet 4.5 | Cohere EN | 0.4590 | 0.860 | $5.81 | 195 |
| 22 | 22 | Sonnet 4.5 | Cohere Multi | 0.4700 | 0.576 | $5.81 | 116 |
| 23 | 24 | Sonnet 3.7 | Titan v1 | 0.5400 | 0.552 | $5.81 | 620 |
| 24 | 25 | Sonnet 3.7 | Cohere EN | 0.4360 | 0.942 | $5.81 | 171 |
| 25 | 26 | Sonnet 3.7 | Cohere Multi | 0.4270 | 1.034 | $5.81 | 101 |
| 26 | 28 | Sonnet 3 | Titan v1 | 0.5350 | 0.493 | $5.81 | 303 |
| 27 | 19 | Sonnet 4.5 | Titan v2 | 0.4530 | 0.573 | $5.81 | 123 |
| 28 | 23 | Sonnet 3.7 | Titan v2 | 0.4700 | 0.489 | $5.81 | 622 |
| 29 | 27 | Sonnet 3 | Titan v2 | 0.3800 | 1.200 | $5.81 | 318 |
| 30 | 16 | Opus 4.5 | Titan v1 | 0.4650 | 0.455 | $9.68 | 157 |
| 31 | 17 | Opus 4.5 | Cohere EN | 0.5030 | 0.556 | $9.68 | 137 |
| 32 | 18 | Opus 4.5 | Cohere Multi | 0.5210 | 0.618 | $9.68 | 132 |
| 33 | 15 | Opus 4.5 | Titan v2 | 0.4990 | 0.168 | $9.68 | 166 |

**Cheapest consensus permutation**: Exp 48 (Nova 2 Lite + Titan v1) at $0.08/experiment

**Most expensive consensus permutation**: Exp 15 (Opus 4.5 + Titan v2) at $9.68/experiment

**Potential savings**: 99% by using the cheapest consensus configuration vs the most expensive

## D. Most Similar Pairs (Closest Results)

Pairs of permutations that produced the most similar per-question score profiles. Lower distance = more similar results.

| Rank | Exp A | Exp B | Vision A | Vision B | Embedding A | Embedding B | Distance | Cost A | Cost B |
|------|-------|-------|----------|----------|------------|------------|------:|------:|------:|
| 1 | 40 | 48 | Nova Pro | Nova 2 Lite | Titan v1 | Titan v1 | 0.106 | $1.38 | $0.08 |
| 2 | 24 | 28 | Sonnet 3.7 | Sonnet 3 | Titan v1 | Titan v1 | 0.164 | $5.81 | $5.81 |
| 3 | 28 | 36 | Sonnet 3 | Haiku 3 | Titan v1 | Titan v1 | 0.268 | $5.81 | $0.49 |
| 4 | 24 | 36 | Sonnet 3.7 | Haiku 3 | Titan v1 | Titan v1 | 0.285 | $5.81 | $0.49 |
| 5 | 39 | 47 | Nova Pro | Nova 2 Lite | Titan v2 | Titan v2 | 0.286 | $1.38 | $0.08 |
| 6 | 43 | 45 | Nova Lite | Nova Lite | Titan v2 | Cohere EN | 0.289 | $0.11 | $0.11 |
| 7 | 15 | 47 | Opus 4.5 | Nova 2 Lite | Titan v2 | Titan v2 | 0.295 | $9.68 | $0.08 |
| 8 | 36 | 40 | Haiku 3 | Nova Pro | Titan v1 | Titan v1 | 0.314 | $0.49 | $1.38 |
| 9 | 24 | 32 | Sonnet 3.7 | Haiku 4.5 | Titan v1 | Titan v1 | 0.326 | $5.81 | $1.94 |
| 10 | 15 | 39 | Opus 4.5 | Nova Pro | Titan v2 | Titan v2 | 0.346 | $9.68 | $1.38 |
| 11 | 28 | 40 | Sonnet 3 | Nova Pro | Titan v1 | Titan v1 | 0.351 | $5.81 | $1.38 |
| 12 | 36 | 48 | Haiku 3 | Nova 2 Lite | Titan v1 | Titan v1 | 0.372 | $0.49 | $0.08 |
| 13 | 38 | 42 | Haiku 3 | Nova Pro | Cohere Multi | Cohere Multi | 0.386 | $0.49 | $1.38 |
| 14 | 43 | 46 | Nova Lite | Nova Lite | Titan v2 | Cohere Multi | 0.389 | $0.11 | $0.11 |
| 15 | 23 | 43 | Sonnet 3.7 | Nova Lite | Titan v2 | Titan v2 | 0.390 | $5.81 | $0.11 |

## E. Most Dissimilar Pairs (Biggest Divergence)

Pairs of permutations that produced the most different results.

| Rank | Exp A | Exp B | Vision A | Vision B | Embedding A | Embedding B | Distance |
|------|-------|-------|----------|----------|------------|------------|------:|
| 1 | 30 | 40 | Sonnet 3 | Nova Pro | Cohere Multi | Titan v1 | 2.331 |
| 2 | 29 | 41 | Sonnet 3 | Nova Pro | Cohere EN | Cohere EN | 2.410 |
| 3 | 30 | 44 | Sonnet 3 | Nova Lite | Cohere Multi | Titan v1 | 2.419 |
| 4 | 30 | 48 | Sonnet 3 | Nova 2 Lite | Cohere Multi | Titan v1 | 2.430 |
| 5 | 30 | 50 | Sonnet 3 | Nova 2 Lite | Cohere Multi | Cohere Multi | 2.435 |
| 6 | 29 | 50 | Sonnet 3 | Nova 2 Lite | Cohere EN | Cohere Multi | 2.462 |
| 7 | 29 | 37 | Sonnet 3 | Haiku 3 | Cohere EN | Cohere EN | 2.501 |
| 8 | 30 | 37 | Sonnet 3 | Haiku 3 | Cohere Multi | Cohere EN | 2.552 |
| 9 | 29 | 49 | Sonnet 3 | Nova 2 Lite | Cohere EN | Cohere EN | 2.775 |
| 10 | 30 | 49 | Sonnet 3 | Nova 2 Lite | Cohere Multi | Cohere EN | 2.857 |

## F. Which Factor Drives More Variation?

Does changing the vision model or the embedding model cause more variation in results? Between-group std dev measures how much group means differ. Within-group std dev measures how much the other factor adds variation.

| Factor | Between-Group Std Dev | Within-Group Avg Std Dev |
|--------|------:|------:|
| Vision Model (9 groups) | 0.0524 | 0.0415 |
| Embedding Model (4 groups) | 0.0285 | 0.0587 |

Vision model choice drives **1.8x** more between-group variation than embedding model choice.

### Vision Model Consistency

How consistent is each vision model across the 4 embedding options? Lower std dev = less sensitive to embedding choice.

| Vision Model | Mean Score | Std Dev (across embeddings) | Est. Cost Range |
|-------------|------:|------:|------|
| Opus 4.5 | 0.4970 | 0.0234 | $9.68-$9.68 |
| Sonnet 4.5 | 0.4710 | 0.0218 | $5.81-$5.81 |
| Sonnet 3.7 | 0.4682 | 0.0513 | $5.81-$5.81 |
| Sonnet 3 | 0.3950 | 0.0960 | $5.81-$5.81 |
| Haiku 4.5 | 0.4497 | 0.0470 | $1.94-$1.94 |
| Haiku 3 | 0.5305 | 0.0322 | $0.49-$0.49 |
| Nova Pro | 0.5373 | 0.0335 | $1.38-$1.38 |
| Nova Lite | 0.5128 | 0.0288 | $0.11-$0.11 |
| Nova 2 Lite | 0.5680 | 0.0396 | $0.08-$0.08 |

### Embedding Model Consistency

How consistent is each embedding model across all vision models? Lower std dev = less sensitive to vision model choice.

| Embedding Model | Mean Score | Std Dev (across vision models) |
|----------------|------:|------:|
| Titan v2 | 0.4703 | 0.0430 |
| Titan v1 | 0.5333 | 0.0332 |
| Cohere EN | 0.4888 | 0.0859 |
| Cohere Multi | 0.4762 | 0.0726 |

## G. Per-Question Factor Decomposition

Which factor drives more variance for each individual question? Ratio > 1 means vision model choice matters more than embedding.

| Question | Vision Between Std | Embedding Between Std | Ratio (V/E) |
|----------|------:|------:|------:|
| want_to_know_more | 0.2548 | 0.2009 | 1.27 |
| memorability | 0.3850 | 0.2361 | 1.63 |
| research_intent | 0.3154 | 0.2056 | 1.53 |
| personal_fit | 0.3477 | 0.1673 | 2.08 |
| concept_preference | 0.0899 | 0.1277 | 0.70 |

## H. Composite Score Matrix

Rows = vision models, columns = embedding models. Cells = composite scores. Row Std Dev shows how much switching embeddings changes the result for that vision model.

| Vision Model | Titan v2 | Titan v1 | Cohere EN | Cohere Multi | Row Std Dev |
|-------------|------:|------:|------:|------:|------:|
| Opus 4.5 | 0.4990 | 0.4650 | 0.5030 | 0.5210 | 0.0234 |
| Sonnet 4.5 | 0.4530 | 0.5020 | 0.4590 | 0.4700 | 0.0218 |
| Sonnet 3.7 | 0.4700 | 0.5400 | 0.4360 | 0.4270 | 0.0513 |
| Sonnet 3 | 0.3800 | 0.5350 | 0.3310 | 0.3340 | 0.0960 |
| Haiku 4.5 | 0.4320 | 0.5200 | 0.4240 | 0.4230 | 0.0470 |
| Haiku 3 | 0.5080 | 0.5540 | 0.5620 | 0.4980 | 0.0322 |
| Nova Pro | 0.4920 | 0.5600 | 0.5650 | 0.5320 | 0.0335 |
| Nova Lite | 0.4850 | 0.5530 | 0.5100 | 0.5030 | 0.0288 |
| Nova 2 Lite | 0.5140 | 0.5710 | 0.6090 | 0.5780 | 0.0396 |
| **Col Mean** | 0.4703 | 0.5333 | 0.4888 | 0.4762 | |
| **Col Std Dev** | 0.0430 | 0.0332 | 0.0859 | 0.0726 | |

## I. Per-Question Score Matrices

Mean Likert scores (1-5 scale) for each question across all permutations.

### want_to_know_more

| Vision Model | Titan v2 | Titan v1 | Cohere EN | Cohere Multi | Row Std Dev |
|-------------|------:|------:|------:|------:|------:|
| Opus 4.5 | 2.970 | 2.650 | 3.010 | 3.020 | 0.176 |
| Sonnet 4.5 | 2.510 | 2.640 | 2.870 | 2.740 | 0.153 |
| Sonnet 3.7 | 3.070 | 3.290 | 2.830 | 2.560 | 0.314 |
| Sonnet 3 | 2.530 | 3.230 | 2.010 | 1.970 | 0.588 |
| Haiku 4.5 | 2.670 | 3.370 | 2.410 | 2.270 | 0.489 |
| Haiku 3 | 2.980 | 3.170 | 3.180 | 2.630 | 0.257 |
| Nova Pro | 2.820 | 3.290 | 2.960 | 2.610 | 0.286 |
| Nova Lite | 3.110 | 3.420 | 3.350 | 2.990 | 0.202 |
| Nova 2 Lite | 2.970 | 3.330 | 3.350 | 3.220 | 0.175 |

### memorability

| Vision Model | Titan v2 | Titan v1 | Cohere EN | Cohere Multi | Row Std Dev |
|-------------|------:|------:|------:|------:|------:|
| Opus 4.5 | 3.030 | 2.900 | 2.590 | 3.550 | 0.400 |
| Sonnet 4.5 | 2.680 | 3.010 | 2.190 | 3.000 | 0.385 |
| Sonnet 3.7 | 2.630 | 2.950 | 2.290 | 3.000 | 0.329 |
| Sonnet 3 | 2.620 | 2.930 | 2.210 | 2.850 | 0.323 |
| Haiku 4.5 | 2.750 | 2.970 | 2.350 | 2.980 | 0.295 |
| Haiku 3 | 3.600 | 3.140 | 3.300 | 3.930 | 0.348 |
| Nova Pro | 3.290 | 3.170 | 3.930 | 4.110 | 0.465 |
| Nova Lite | 2.590 | 2.790 | 2.630 | 2.890 | 0.140 |
| Nova 2 Lite | 3.260 | 3.190 | 3.400 | 3.660 | 0.208 |

### research_intent

| Vision Model | Titan v2 | Titan v1 | Cohere EN | Cohere Multi | Row Std Dev |
|-------------|------:|------:|------:|------:|------:|
| Opus 4.5 | 2.890 | 2.540 | 3.040 | 2.610 | 0.235 |
| Sonnet 4.5 | 2.620 | 2.810 | 2.700 | 2.290 | 0.224 |
| Sonnet 3.7 | 2.590 | 3.020 | 2.240 | 1.850 | 0.499 |
| Sonnet 3 | 2.500 | 2.990 | 2.140 | 1.960 | 0.454 |
| Haiku 4.5 | 2.640 | 2.920 | 3.040 | 2.590 | 0.217 |
| Haiku 3 | 2.890 | 3.020 | 3.960 | 2.940 | 0.508 |
| Nova Pro | 2.730 | 3.100 | 3.230 | 2.970 | 0.213 |
| Nova Lite | 2.640 | 2.890 | 2.650 | 2.550 | 0.145 |
| Nova 2 Lite | 2.850 | 3.180 | 3.910 | 3.200 | 0.447 |

### personal_fit

| Vision Model | Titan v2 | Titan v1 | Cohere EN | Cohere Multi | Row Std Dev |
|-------------|------:|------:|------:|------:|------:|
| Opus 4.5 | 3.200 | 3.000 | 3.400 | 3.340 | 0.178 |
| Sonnet 4.5 | 3.350 | 3.460 | 3.400 | 3.390 | 0.045 |
| Sonnet 3.7 | 3.050 | 3.280 | 3.150 | 2.980 | 0.130 |
| Sonnet 3 | 2.140 | 3.390 | 2.400 | 2.100 | 0.603 |
| Haiku 4.5 | 2.700 | 3.010 | 2.720 | 2.690 | 0.154 |
| Haiku 3 | 2.860 | 3.450 | 3.020 | 2.820 | 0.288 |
| Nova Pro | 3.160 | 3.590 | 3.270 | 3.060 | 0.230 |
| Nova Lite | 3.410 | 3.750 | 3.520 | 3.580 | 0.142 |
| Nova 2 Lite | 3.370 | 3.640 | 3.560 | 3.570 | 0.116 |

### concept_preference

| Vision Model | Titan v2 | Titan v1 | Cohere EN | Cohere Multi | Row Std Dev |
|-------------|------:|------:|------:|------:|------:|
| Opus 4.5 | 2.880 | 3.200 | 3.020 | 2.910 | 0.145 |
| Sonnet 4.5 | 2.890 | 3.120 | 3.010 | 2.970 | 0.096 |
| Sonnet 3.7 | 3.070 | 3.260 | 3.220 | 3.160 | 0.083 |
| Sonnet 3 | 2.810 | 3.160 | 2.850 | 2.800 | 0.171 |
| Haiku 4.5 | 2.870 | 3.130 | 2.960 | 2.930 | 0.111 |
| Haiku 3 | 2.840 | 3.300 | 2.790 | 2.640 | 0.285 |
| Nova Pro | 2.830 | 3.060 | 2.900 | 2.880 | 0.099 |
| Nova Lite | 2.940 | 3.200 | 3.050 | 3.040 | 0.107 |
| Nova 2 Lite | 2.820 | 3.080 | 2.950 | 2.900 | 0.109 |

## J. Processing Time & Cost by Vision Model

| Vision Model | Mean Time (s) | Est. Cost/Experiment | Cost Tier |
|-------------|------:|------:|------|
| Opus 4.5 | 148 | $9.68 | Premium |
| Sonnet 4.5 | 153 | $5.81 | Premium |
| Sonnet 3.7 | 379 | $5.81 | Premium |
| Sonnet 3 | 298 | $5.81 | Premium |
| Haiku 4.5 | 118 | $1.94 | Premium |
| Haiku 3 | 95 | $0.49 | Medium |
| Nova Pro | 102 | $1.38 | High |
| Nova Lite | 79 | $0.11 | Low |
| Nova 2 Lite | 113 | $0.08 | Low |

## K. Key Findings

1. **Most consistent vision model** (across embeddings): **Sonnet 4.5** (std dev 0.0218)
2. **Least consistent vision model**: **Sonnet 3** (std dev 0.0960)
3. **Most consistent embedding** (across vision models): **Titan v1** (std dev 0.0332)
4. **Vision model choice drives 1.8x more variation** than embedding model choice
5. **Best value for money**: **Nova 2 Lite + Titan v1** ($0.08/experiment) - produces results consistent with the group consensus
6. **3 outlier permutations** identified, involving: Nova 2 Lite, Sonnet 3
7. **33 of 36 permutations** (91%) fall within the consensus cluster

# Comparison Report: Experiment 13 vs 14

## Purpose

Reproducibility test using identical input with Bedrock models (Claude Sonnet 4.5 + Titan Embed v2).

## Test Configuration

| Field | Exp 13 | Exp 14 |
|-------|--------|--------|
| **Experiment ID** | `b390b596` | `971922a9` |
| **Personas** | 90/90 | 90/90 |
| **Processing Time** | 262.0s | 262.7s |
| **Generation** | `bedrock/eu.anthropic.claude-sonnet-4-5-20250929-v1:0` | `bedrock/eu.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| **Embedding** | `bedrock/amazon.titan-embed-text-v2:0` | `bedrock/amazon.titan-embed-text-v2:0` |

---

## Overall Results

| Metric | Exp 13 | Exp 14 | Difference |
|--------|--------|--------|------------|
| **Result** | FAIL | FAIL | Same |
| **Composite Score** | 0.450 | 0.454 | +0.004 |
| **Threshold** | 0.55 | 0.55 | - |
| **Margin** | -0.100 | -0.096 | +0.004 |

---

## Per-Question Comparison

| Question | Exp 13 Mean | Exp 14 Mean | Diff | Exp 13 Median | Exp 14 Median | Exp 13 Std | Exp 14 Std |
|----------|-------------|-------------|------|---------------|---------------|------------|------------|
| want_to_know_more | 2.50 | 2.49 | -0.01 | 2.41 | 2.48 | 0.30 | 0.27 |
| memorability | 2.70 | 2.69 | -0.01 | 2.65 | 2.67 | 0.31 | 0.25 |
| research_intent | 2.61 | 2.62 | +0.01 | 2.58 | 2.59 | 0.18 | 0.18 |
| personal_fit | 3.29 | 3.40 | +0.11 | 3.54 | 3.56 | 0.51 | 0.43 |
| concept_preference | 2.89 | 2.88 | -0.01 | 2.83 | 2.82 | 0.15 | 0.14 |

---

## Distribution Comparison

| Rating | Exp 13 | Exp 14 | Diff |
|--------|--------|--------|------|
| 1 (Strongly Negative) | 0 (0.0%) | 0 (0.0%) | +0 |
| 2 (Negative) | 119 (26.4%) | 110 (24.4%) | -9 |
| 3 (Neutral) | 276 (61.3%) | 282 (62.7%) | +6 |
| 4 (Positive) | 55 (12.2%) | 58 (12.9%) | +3 |
| 5 (Strongly Positive) | 0 (0.0%) | 0 (0.0%) | +0 |

---

## Per-Persona Score Correlation

- **Mean absolute difference per persona**: 0.125
- **Max difference**: 0.606
- **Min difference**: 0.002
- **Std of differences**: 0.116

### By Country

| Country | Exp 13 Mean | Exp 14 Mean | Diff |
|---------|-------------|-------------|------|
| Czech Republic | 2.82 | 2.85 | +0.02 |
| Greece | 2.79 | 2.82 | +0.03 |
| United Kingdom | 2.79 | 2.78 | -0.01 |

### By Gender

| Gender | Exp 13 Mean | Exp 14 Mean | Diff |
|--------|-------------|-------------|------|
| F | 2.78 | 2.79 | +0.01 |
| M | 2.82 | 2.84 | +0.02 |

---

## Reproducibility Assessment

- **Composite score difference**: 0.004
- **Stability rating**: Excellent
- **Result agreement**: Yes (both FAIL)
- **Mean per-persona difference**: 0.125
- **Largest per-question mean shift**: 0.11

The Bedrock pipeline (Claude Sonnet 4.5 + Titan Embed v2) demonstrates **excellent reproducibility** 
with a composite score difference of 0.004 across identical inputs.

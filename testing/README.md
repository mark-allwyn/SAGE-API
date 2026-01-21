# SAGE API Testing Examples

This folder contains example inputs and outputs for testing the SAGE API.

## Running Tests

To run any test example:

```bash
cat examples/01_smartwatch_input.json | curl -s -X POST http://localhost:8000/test-concept \
  -H "Content-Type: application/json" -d @- | python3 -m json.tool
```

Or run all tests:
```bash
./run_tests.sh
```

## Examples

### 01 - SmartFit Pro Watch (Basic Test)

**Input:** `examples/01_smartwatch_input.json`
**Output:** `examples/01_smartwatch_output.json`

- **Concept:** Fitness smartwatch at $199
- **Personas:** 5 diverse consumers
- **Questions:** Purchase intent (50%), Value perception (30%), Recommendation (20%)
- **Threshold:** 0.65
- **Result:** FAIL

---

### 02 - LuxeGlow Skincare (Filtered Test)

**Input:** `examples/02_skincare_filtered_input.json`
**Output:** `examples/02_skincare_filtered_output.json`

- **Concept:** Premium Vitamin C serum at $89
- **Personas:** 6 consumers with varying skincare habits
- **Filters:** `gender=F`, `age>=25` (3 of 6 matched)
- **Threshold:** 0.55
- **Result:** FAIL

---

### 03 - PowerFuel Protein Bar (Multi-Question)

**Input:** `examples/03_protein_bar_input.json`
**Output:** `examples/03_protein_bar_output.json`

- **Concept:** Plant-based protein bar at $2.75/bar
- **Personas:** 6 consumers
- **Questions:** Purchase intent (40%), Taste appeal (35%), Price (25%)
- **Threshold:** 0.60
- **Result:** FAIL

---

### 04 - BeanBox Coffee (PASS with Dataset) ✅

**Input:** `examples/04_coffee_subscription_input.json`
**Output:** `examples/04_coffee_subscription_output.json`

- **Concept:** Coffee subscription at $32/month
- **Personas:** 3 coffee drinkers
- **Threshold:** 0.45
- **Dataset:** Included (shows raw LLM responses)
- **Result:** **PASS** (Score: 0.515)

---

### 05 - FreshChef Meal Kit (PASS with Filters & Dataset) ✅

**Input:** `examples/05_meal_kit_filtered_input.json`
**Output:** `examples/05_meal_kit_filtered_output.json`

- **Concept:** Meal kit service at $9.99/serving
- **Personas:** 6 consumers
- **Filters:** `income in [high,medium]`, `household_size>=2` (4 of 6 matched)
- **Questions:** Purchase intent (50%), Convenience (30%), Price value (20%)
- **Threshold:** 0.48
- **Dataset:** Included
- **Result:** **PASS** (Score: 0.517)

---

## Understanding the Output

### Result Summary
```json
{
  "result": {
    "passed": true,              // Did concept meet threshold?
    "composite_score": 0.517,    // Weighted normalized score (0-1)
    "threshold": 0.48,           // Required score to pass
    "margin": 0.037,             // How far above/below threshold
    "reason": "PASS: ..."        // Human-readable explanation
  }
}
```

### Criteria Breakdown
Shows how each question contributed to the composite score:
```json
{
  "question_id": "purchase_intent",
  "weight": 0.5,           // Weight in composite calculation
  "raw_mean": 3.08,        // Average Likert score (1-5)
  "normalized": 0.52,      // Mapped to 0-1 scale: (mean-1)/4
  "contribution": 0.26     // weight × normalized
}
```

### Metrics Per Question
Detailed statistics for each survey question:
```json
{
  "n": 4,                  // Number of personas included
  "mean": 3.08,            // Average score
  "median": 3.08,          // Median score
  "std_dev": 0.03,         // Standard deviation
  "top_2_box": 0.0,        // % scoring 4 or 5
  "bottom_2_box": 0.0,     // % scoring 1 or 2
  "distribution": {...}    // Count per score bucket
}
```

### Dataset (when `output_dataset: true`)
Full per-persona data with raw LLM responses:
```json
{
  "persona_id": "busy_parent",
  "age": 38,
  "gender": "F",
  "matched_filter": true,
  "purchase_intent_text": "I'm quite likely to give FreshChef a try...",
  "purchase_intent_pmf": [0.185, 0.192, 0.2, 0.21, 0.214],
  "purchase_intent_mean": 3.08
}
```

## Filter Syntax

Filters use SQL-like expressions:

| Operator | Example | Description |
|----------|---------|-------------|
| `=` | `gender=F` | Equals |
| `!=` | `income!=low` | Not equals |
| `>` | `age>30` | Greater than |
| `>=` | `age>=25` | Greater than or equal |
| `<` | `age<50` | Less than |
| `<=` | `age<=65` | Less than or equal |
| `in` | `region in [North,South]` | In list |

## Request Options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `verbose` | bool | `true` | Return full response vs minimal |
| `output_dataset` | bool | `false` | Include raw persona responses |
| `threshold` | float | required | Pass/fail score threshold (0-1) |
| `filters` | list | `[]` | SQL-like persona filters |

# SAGE API Testing Examples

This folder contains example inputs and outputs for testing the SAGE API.

## Quick Summary

| # | Experiment | Personas | Result | Score |
|---|------------|----------|--------|-------|
| 01 | SmartFit Pro Watch | 5 | FAIL | - |
| 02 | LuxeGlow Skincare (filtered) | 3 of 6 | FAIL | - |
| 03 | PowerFuel Protein Bar | 6 | FAIL | - |
| 04 | BeanBox Coffee | 3 | **PASS** | 0.515 |
| 05 | FreshChef Meal Kit (filtered) | 4 of 6 | **PASS** | 0.517 |
| 06 | LuckyDraw Lottery TV Ad | 6 | FAIL | - |
| 07 | LuckyDraw Lottery (large sample) | 50 | FAIL | - |
| 08 | JackpotJoe Lottery - Talking Dog | 50 | FAIL | 0.547 |
| 09 | Neon Velocity - BMW Flying Car (image) | 50 | **PASS** | 0.744 |

---

## Running Tests

```bash
# Run a single test
cat examples/01_smartwatch_input.json | \
  curl -s -X POST http://localhost:8000/test-concept \
  -H "Content-Type: application/json" -d @- | python3 -m json.tool

# Run all tests
./run_tests.sh
```

---

## Experiments

### 01 - SmartFit Pro Watch
Basic concept test with 5 personas and 3 weighted questions.

| File | Description |
|------|-------------|
| `01_smartwatch_input.json` | Input |
| `01_smartwatch_output.json` | Output |

---

### 02 - LuxeGlow Skincare
Demonstrates persona filtering (`gender=F`, `age>=25`).

| File | Description |
|------|-------------|
| `02_skincare_filtered_input.json` | Input |
| `02_skincare_filtered_output.json` | Output |

---

### 03 - PowerFuel Protein Bar
Multi-question weighted scoring.

| File | Description |
|------|-------------|
| `03_protein_bar_input.json` | Input |
| `03_protein_bar_output.json` | Output |

---

### 04 - BeanBox Coffee
First passing test with dataset output.

| File | Description |
|------|-------------|
| `04_coffee_subscription_input.json` | Input |
| `04_coffee_subscription_output.json` | Output with dataset |

---

### 05 - FreshChef Meal Kit
Passing test with filters and dataset.

| File | Description |
|------|-------------|
| `05_meal_kit_filtered_input.json` | Input |
| `05_meal_kit_filtered_output.json` | Output with dataset |

---

### 06 - LuckyDraw Lottery TV Ad
Ad effectiveness testing with 10 metrics and 6 personas.

| File | Description |
|------|-------------|
| `06_lottery_gaming_input.json` | Input |
| `06_lottery_gaming_output.json` | Output |

---

### 07 - LuckyDraw Lottery (Large Sample)
Same concept as 06 with 50 personas to test scalability.

| File | Description |
|------|-------------|
| `07_lottery_large_sample_input.json` | Input |
| `07_lottery_large_sample_output.json` | Output with dataset |

---

### 08 - JackpotJoe Lottery - Talking Dog Ad
Distinctive creative test with humorous talking dog mascot.

| File | Description |
|------|-------------|
| `08_lottery_distinctive_input.json` | Input |
| `08_lottery_distinctive_output.json` | Output with dataset |
| `08_lottery_distinctive_report.md` | Analysis report |

**Key Findings:**
- Brand Recognition strongest (3.66)
- Personal Fit weakest (2.45)
- Missed threshold by 0.3%

---

### 09 - Neon Velocity - BMW Flying Car Ad
First image-based concept test using vision model.

| File | Description |
|------|-------------|
| `09_neon_velocity_input.json` | Input (with base64 image) |
| `09_neon_velocity_output.json` | Output with dataset |
| `09_neon_velocity_report.md` | Analysis report |
| `../images/09_neon_velocity_storyboard.png` | Source image |

**Key Findings:**
- Story Appeal strongest (4.27)
- Character Appeal weakest (2.92)
- Exceeded threshold by 19.4%

---

## Output Structure

### Result
```json
{
  "passed": true,
  "composite_score": 0.744,
  "threshold": 0.55,
  "margin": 0.194
}
```

### Metrics Per Question
```json
{
  "mean": 4.27,
  "median": 4.28,
  "std_dev": 0.06,
  "top_2_box": 1.0,
  "bottom_2_box": 0.0
}
```

### Dataset (when `output_dataset: true`)
```json
{
  "persona_id": "tech_01",
  "ad_enjoyment_text": "Raw LLM response...",
  "ad_enjoyment_pmf": [0.08, 0.06, 0.09, 0.29, 0.48],
  "ad_enjoyment_mean": 4.03
}
```

### Report (when `include_report: true`)
Generates a markdown report in the response:
```json
{
  "report": "# Concept Test Report: My Concept\n\n## Test Overview\n..."
}
```

The report includes:
- Test overview table
- Overall result summary
- Criteria breakdown table
- Key insights (strengths/weaknesses)
- Metrics summary table
- Sample responses (first 3 personas, requires `output_dataset: true`)
- Conclusions and recommendations

---

## Filter Syntax

| Operator | Example | Description |
|----------|---------|-------------|
| `=` | `gender=F` | Equals |
| `!=` | `income!=low` | Not equals |
| `>=` | `age>=25` | Greater than or equal |
| `in` | `region in [North,South]` | In list |

---

## Files

```
testing/
  README.md
  run_tests.sh
  examples/
    01_smartwatch_input.json
    01_smartwatch_output.json
    ...
    09_neon_velocity_input.json
    09_neon_velocity_output.json
    09_neon_velocity_report.md
    08_lottery_distinctive_report.md
    REPORT_TEMPLATE.md
  images/
    09_neon_velocity_storyboard.png
```

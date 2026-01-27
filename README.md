# SAGE API

**S**ynthetic **A**udience **G**eneration **E**ngine - Generate synthetic consumer survey responses using LLM + Semantic Similarity Rating (SSR).

Based on the methodology from ["LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings"](https://arxiv.org/abs/2510.08338) (Maier et al., 2025).

## Overview

SAGE simulates how real consumers would respond to product concepts by:

1. **Persona Role-Play**: LLMs role-play as consumers with specific demographics
2. **Natural Language Response**: Generate authentic free-text responses about purchase intent
3. **SSR Mapping**: Convert responses to Likert-scale probability distributions using embedding similarity
4. **Score Aggregation**: Calculate weighted composite scores across questions
5. **Threshold Evaluation**: Return PASS/FAIL based on configurable thresholds

## Features

- **Multi-Provider Support**: OpenAI and AWS Bedrock for generation, embeddings, and vision
- **Vision Support**: Test image-based concepts (storyboards, ads) via base64-encoded images
- **Flexible Personas**: Any demographic attributes with SQL-like filtering
- **Custom Surveys**: Multiple weighted questions with 6 reference sets of 5 anchors each
- **Rich Output**: Detailed metrics, distributions, and optional raw dataset export
- **Auto-Generated Reports**: Markdown reports with insights, metrics tables, and sample responses
- **Docker Ready**: Production-ready containerization

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/mark-allwyn/SAGE-API.git
cd SAGE-API

# Copy environment template
cp .env.example .env

# Add your OpenAI API key to .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env
```

### 2. Install and Run

```bash
# Using uv (recommended)
uv sync
uv run uvicorn sage.main:app --reload

# Or using pip
pip install -e .
uvicorn sage.main:app --reload
```

### 3. Test the API

```bash
curl http://localhost:8000/health
# {"status":"healthy"}
```

API docs available at: http://localhost:8000/docs

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/test-concept` | POST | Test a product concept with synthetic personas |
| `/health` | GET | Health check |
| `/info` | GET | API configuration and defaults |
| `/models` | GET | List supported models by provider |

## Example Request

```bash
curl -X POST http://localhost:8000/test-concept \
  -H "Content-Type: application/json" \
  -d '{
    "personas": [
      {"persona_id": "p1", "age": 28, "gender": "F", "income": "high"},
      {"persona_id": "p2", "age": 45, "gender": "M", "income": "medium"}
    ],
    "concept": {
      "name": "SmartWatch Pro",
      "content": [{"type": "text", "data": "A fitness smartwatch with 7-day battery..."}]
    },
    "survey_config": {
      "questions": [{
        "id": "purchase_intent",
        "text": "How likely are you to purchase this product?",
        "weight": 1.0,
        "ssr_reference_sets": [
          ["Definitely would not buy", "Probably would not buy", "Might or might not buy", "Probably would buy", "Definitely would buy"],
          ["No chance", "Unlikely", "Uncertain", "Likely", "Certain"],
          ["Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"],
          ["Would never consider", "Rarely consider", "Might consider", "Likely consider", "Definitely consider"],
          ["Hard pass", "Soft pass", "On the fence", "Leaning yes", "Absolutely"],
          ["0%", "25%", "50%", "75%", "100%"]
        ]
      }]
    },
    "threshold": 0.6,
    "verbose": true,
    "output_dataset": true,
    "include_report": true
  }'
```

## Example Response

```json
{
  "result": {
    "passed": true,
    "composite_score": 0.65,
    "threshold": 0.6,
    "margin": 0.05,
    "reason": "PASS: Composite score 0.65 meets threshold 0.6"
  },
  "personas_total": 2,
  "personas_matched": 2,
  "criteria_breakdown": [{
    "question_id": "purchase_intent",
    "weight": 1.0,
    "raw_mean": 3.6,
    "normalized": 0.65,
    "contribution": 0.65
  }],
  "metrics": {
    "purchase_intent": {
      "n": 2,
      "mean": 3.6,
      "median": 3.55,
      "std_dev": 0.15,
      "top_2_box": 0.4,
      "bottom_2_box": 0.1,
      "distribution": {"1": 0, "2": 0, "3": 1, "4": 1, "5": 0}
    }
  },
  "dataset": [
    {
      "persona_id": "p1",
      "age": 28,
      "gender": "F",
      "matched_filter": true,
      "purchase_intent_text": "I'm quite interested in this smartwatch...",
      "purchase_intent_pmf": [0.1, 0.15, 0.25, 0.3, 0.2],
      "purchase_intent_mean": 3.8
    }
  ],
  "report": "# Concept Test Report: SmartWatch Pro\n\n## Test Overview\n..."
}
```

## Image-Based Concepts

Test visual concepts like storyboards, ads, or product images using base64-encoded images:

```json
{
  "concept": {
    "name": "Flying Car Ad Storyboard",
    "content": [
      {
        "type": "image",
        "data": "<base64-encoded-image>",
        "label": "Storyboard"
      }
    ]
  }
}
```

The vision model (GPT-4o by default) interprets the image and personas respond to the visual content. Supported formats: JPEG, PNG, GIF, WebP.

## Filtering Personas

Use SQL-like expressions to target specific demographics:

```json
{
  "filters": ["gender=F", "age>=25", "income in [high,medium]"]
}
```

| Operator | Example | Description |
|----------|---------|-------------|
| `=` | `gender=F` | Equals |
| `!=` | `income!=low` | Not equals |
| `>` | `age>30` | Greater than |
| `>=` | `age>=25` | Greater than or equal |
| `<` | `age<50` | Less than |
| `<=` | `age<=65` | Less than or equal |
| `in` | `region in [North,South]` | In list |

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | required | OpenAI API key |
| `AWS_ACCESS_KEY_ID` | optional | AWS credentials for Bedrock |
| `AWS_SECRET_ACCESS_KEY` | optional | AWS credentials for Bedrock |
| `AWS_REGION` | `us-east-1` | AWS region |
| `DEFAULT_GENERATION_MODEL` | `gpt-4o` | Default generation model |
| `DEFAULT_EMBEDDING_MODEL` | `text-embedding-3-small` | Default embedding model |
| `SSR_SOFTMAX_TEMPERATURE` | `0.5` | Temperature for SSR softmax |

### Request Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `verbose` | bool | `true` | Return full response vs minimal |
| `output_dataset` | bool | `false` | Include raw persona responses |
| `include_report` | bool | `false` | Generate markdown report |
| `threshold` | float | required | Pass/fail score threshold (0-1) |
| `filters` | list | `[]` | SQL-like persona filters |

Override provider defaults per-request:

```json
{
  "options": {
    "generation_provider": "openai",
    "generation_model": "gpt-4o",
    "embedding_provider": "openai",
    "embedding_model": "text-embedding-3-small",
    "generation_temperature": 0.7
  }
}
```

## Docker

```bash
# Build
docker build -t sage-api .

# Run
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... sage-api
```

## Generated Reports

When `include_report: true`, the response includes a markdown report with:

- **Test Overview**: Concept name, personas, processing time, providers
- **Result Summary**: Pass/fail, composite score, threshold, margin
- **Criteria Breakdown**: Per-question weights, means, contributions
- **Key Insights**: Top strengths and weaknesses
- **Metrics Table**: Mean, median, std dev, top/bottom 2 box per question
- **Sample Responses**: First 3 personas with raw text (requires `output_dataset: true`)
- **Conclusions**: Summary and recommendations

## Testing

```bash
# Run unit tests
uv run pytest

# Run example tests against running API
cd testing
./run_tests.sh
```

See `testing/examples/` for sample inputs and outputs.

## Project Structure

```
sage_API/
├── sage/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── models/
│   │   ├── request.py       # Input models
│   │   └── response.py      # Output models
│   ├── services/
│   │   ├── orchestrator.py    # Pipeline coordinator
│   │   ├── llm_service.py     # LLM abstraction
│   │   ├── ssr_engine.py      # Semantic Similarity Rating
│   │   ├── filter_engine.py   # Persona filtering
│   │   ├── scoring_engine.py  # Metrics & scoring
│   │   └── report_generator.py# Markdown report generation
│   └── utils/
│       └── embeddings.py    # Cosine similarity, softmax
├── testing/
│   ├── examples/            # Sample inputs/outputs
│   └── run_tests.sh         # Test runner
├── Dockerfile
├── pyproject.toml
└── .env.example
```

## How SSR Works

1. **Generate Response**: LLM produces free-text response as the persona
2. **Embed Response**: Convert response to embedding vector
3. **Embed Anchors**: Embed all 5 anchors in each of 6 reference sets
4. **Compute Similarity**: Calculate cosine similarity between response and each anchor
5. **Normalize**: Subtract minimum similarity, add epsilon to prevent zeros
6. **Softmax**: Convert similarities to probability distribution (PMF)
7. **Average**: Average PMFs across all 6 reference sets
8. **Calculate Mean**: Compute expected value (1-5 Likert score)

## License

MIT

## Citation

If you use this methodology, please cite:

```bibtex
@article{maier2025llms,
  title={LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings},
  author={Maier, Maximilian and others},
  journal={arXiv preprint arXiv:2510.08338},
  year={2025}
}
```

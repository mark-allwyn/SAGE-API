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
- **Auto-Generated Reports**: Markdown reports with concept description, insights, distribution analysis, sample responses, and appendix with survey scales
- **Async Concurrency**: Semaphore-based parallelism with configurable concurrency limits for personas, questions, and SSR processing
- **Environment-Driven Config**: All model and processing settings configurable via `.env`
- **Docker Ready**: Production-ready containerization

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/mark-allwyn/SAGE-API.git
cd SAGE-API

# Copy environment template
cp .env.example .env

# Add your API keys to .env
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

# Check configured defaults
curl http://localhost:8000/info
```

API docs available at: http://localhost:8000/docs

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/test-concept` | POST | Test a product concept with synthetic personas |
| `/health` | GET | Health check |
| `/info` | GET | API configuration and defaults |
| `/models` | GET | List supported models by provider |

---

## API Specification

### POST `/test-concept`

Test a product concept against synthetic consumer personas. Returns scoring results, metrics, optional dataset, and optional report.

#### Request Body

```json
{
  "personas": [
    {
      "persona_id": "p1",
      "age": 28,
      "gender": "F",
      "country": "United Kingdom",
      "education": "Undergraduate degree",
      "language": "English"
    }
  ],
  "concept": {
    "name": "SmartWatch Pro",
    "content": [
      {"type": "text", "data": "A fitness smartwatch with 7-day battery..."},
      {"type": "image", "data": "<base64-encoded-image>", "label": "Product photo"}
    ],
    "metadata": {"version": "2.0"}
  },
  "survey_config": {
    "questions": [
      {
        "id": "purchase_intent",
        "text": "How likely are you to purchase this product?",
        "weight": 0.5,
        "ssr_reference_sets": [
          ["Definitely would not buy", "Probably would not buy", "Might or might not buy", "Probably would buy", "Definitely would buy"],
          ["No chance", "Unlikely", "Uncertain", "Likely", "Certain"],
          ["Not interested", "Slightly interested", "Moderately interested", "Very interested", "Extremely interested"],
          ["Would never consider", "Rarely consider", "Might consider", "Likely consider", "Definitely consider"],
          ["Hard pass", "Soft pass", "On the fence", "Leaning yes", "Absolutely"],
          ["0%", "25%", "50%", "75%", "100%"]
        ]
      },
      {
        "id": "memorability",
        "text": "To what extent do you agree: 'This product is memorable.'",
        "weight": 0.5,
        "ssr_reference_sets": [
          ["Strongly disagree", "Disagree", "Neither agree nor disagree", "Agree", "Strongly agree"],
          ["Completely forgettable", "Mostly forgettable", "Somewhat memorable", "Quite memorable", "Extremely memorable"],
          ["Not at all", "A little", "Moderately", "Very much", "Completely"],
          ["Totally unmemorable", "Rather unmemorable", "Average", "Rather memorable", "Totally memorable"],
          ["Would forget immediately", "Would likely forget", "Might remember", "Would likely remember", "Would definitely remember"],
          ["0% memorable", "25% memorable", "50% memorable", "75% memorable", "100% memorable"]
        ]
      }
    ]
  },
  "threshold": 0.6,
  "filters": ["gender=F", "age>=25"],
  "verbose": true,
  "output_dataset": true,
  "include_report": true,
  "options": {
    "generation_provider": "bedrock",
    "generation_model": "eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
    "embedding_provider": "bedrock",
    "embedding_model": "amazon.titan-embed-text-v2:0",
    "vision_provider": "bedrock",
    "vision_model": "eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
    "generation_temperature": 0.7
  }
}
```

#### Request Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `personas` | array | Yes | - | List of persona objects. Each must have `persona_id` (unique). All other fields are flexible demographic attributes. |
| `concept` | object | Yes | - | Product concept with `name`, `content` array, and optional `metadata`. |
| `concept.content` | array | Yes | - | Content items. Each has `type` ("text" or "image"), `data` (text string or base64), and optional `label`. |
| `survey_config` | object | Yes | - | Contains `questions` array. |
| `survey_config.questions` | array | Yes | - | Survey questions. Weights must sum to 1.0. |
| `survey_config.questions[].id` | string | Yes | - | Unique question identifier. |
| `survey_config.questions[].text` | string | Yes | - | Question text shown to the persona. |
| `survey_config.questions[].weight` | float | Yes | - | Weight for composite score (0-1). All weights must sum to 1.0. |
| `survey_config.questions[].ssr_reference_sets` | array | Yes | - | Exactly 6 sets of exactly 5 anchor statements each, representing the 1-5 Likert scale. |
| `threshold` | float | Yes | - | Pass/fail threshold for composite score (0-1). |
| `filters` | array | No | `[]` | SQL-like filter expressions for persona selection. |
| `verbose` | bool | No | `true` | `true` returns `FullResponse`, `false` returns `MinimalResponse`. |
| `output_dataset` | bool | No | `false` | Include raw per-persona response data in output. |
| `include_report` | bool | No | `false` | Generate markdown report in output. |
| `options` | object | No | from `.env` | Override provider/model settings for this request. |

#### Options Fields

If omitted, all options default to the values configured in `.env`.

| Field | Type | Default (from `.env`) | Description |
|-------|------|-----------------------|-------------|
| `generation_provider` | string | `DEFAULT_GENERATION_PROVIDER` | `"openai"` or `"bedrock"` |
| `generation_model` | string | `DEFAULT_GENERATION_MODEL` | Model ID for text generation |
| `embedding_provider` | string | `DEFAULT_EMBEDDING_PROVIDER` | `"openai"` or `"bedrock"` |
| `embedding_model` | string | `DEFAULT_EMBEDDING_MODEL` | Model ID for embeddings (SSR) |
| `vision_provider` | string | `DEFAULT_VISION_PROVIDER` | `"openai"` or `"bedrock"` |
| `vision_model` | string | `DEFAULT_VISION_MODEL` | Model ID for image interpretation |
| `generation_temperature` | float | `DEFAULT_TEMPERATURE` | LLM temperature (0-2) |

#### Response: `FullResponse` (verbose=true)

```json
{
  "result": {
    "passed": true,
    "composite_score": 0.650,
    "threshold": 0.60,
    "margin": 0.050,
    "reason": "PASS: Composite score 0.650 meets threshold 0.60"
  },
  "filters_applied": ["gender=F", "age>=25"],
  "personas_total": 90,
  "personas_matched": 45,
  "criteria_breakdown": [
    {
      "question_id": "purchase_intent",
      "weight": 0.5,
      "raw_mean": 3.60,
      "normalized": 0.650,
      "contribution": 0.325
    },
    {
      "question_id": "memorability",
      "weight": 0.5,
      "raw_mean": 3.60,
      "normalized": 0.650,
      "contribution": 0.325
    }
  ],
  "metrics": {
    "purchase_intent": {
      "n": 45,
      "mean": 3.60,
      "median": 3.55,
      "std_dev": 0.42,
      "top_2_box": 0.40,
      "bottom_2_box": 0.10,
      "distribution": {"1": 0, "2": 5, "3": 18, "4": 15, "5": 7}
    }
  },
  "dataset": [
    {
      "persona_id": "p1",
      "age": 28,
      "gender": "F",
      "matched_filter": true,
      "purchase_intent_text": "I'm quite interested in this smartwatch...",
      "purchase_intent_pmf": [0.05, 0.10, 0.25, 0.35, 0.25],
      "purchase_intent_mean": 3.80
    }
  ],
  "report": "# Concept Test Report: SmartWatch Pro\n\n## Test Overview\n...",
  "meta": {
    "request_id": "a3f2b1c9",
    "concept_name": "SmartWatch Pro",
    "processing_time_ms": 45200,
    "providers": {
      "generation": "bedrock/eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
      "embedding": "bedrock/amazon.titan-embed-text-v2:0",
      "vision": "bedrock/eu.anthropic.claude-sonnet-4-5-20250929-v1:0"
    }
  }
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `result` | object | Pass/fail result with composite score, threshold, margin, and reason. |
| `result.passed` | bool | Whether composite score meets threshold. |
| `result.composite_score` | float | Weighted average of normalized question means (0-1). |
| `result.threshold` | float | The threshold from the request. |
| `result.margin` | float | `composite_score - threshold`. Positive = passed. |
| `result.reason` | string | Human-readable result explanation. |
| `filters_applied` | array | Filter expressions that were applied. |
| `personas_total` | int | Total personas in request. |
| `personas_matched` | int | Personas matching filters (all if no filters). |
| `criteria_breakdown` | array | Per-question scoring breakdown. |
| `criteria_breakdown[].raw_mean` | float | Mean Likert score (1-5) for this question. |
| `criteria_breakdown[].normalized` | float | Normalized score (0-1), computed as `(raw_mean - 1) / 4`. |
| `criteria_breakdown[].contribution` | float | `normalized * weight` - this question's contribution to composite. |
| `metrics` | object | Detailed statistics keyed by question ID. |
| `metrics[].n` | int | Number of responses (matched personas). |
| `metrics[].mean` | float | Mean of Likert means across personas. |
| `metrics[].median` | float | Median of Likert means. |
| `metrics[].std_dev` | float | Standard deviation. |
| `metrics[].top_2_box` | float | Proportion of personas with mean >= 4.0 (0-1). |
| `metrics[].bottom_2_box` | float | Proportion of personas with mean <= 2.0 (0-1). |
| `metrics[].distribution` | object | Count of personas by rounded Likert score (keys "1"-"5"). |
| `dataset` | array/null | Per-persona raw data (if `output_dataset=true`). Each row has all persona attributes plus `{question_id}_text`, `{question_id}_pmf`, `{question_id}_mean` for each question. |
| `report` | string/null | Markdown report (if `include_report=true`). |
| `meta` | object | Request metadata. |
| `meta.request_id` | string | Unique experiment ID. |
| `meta.processing_time_ms` | int | Total processing time in milliseconds. |
| `meta.providers` | object | Provider/model strings used for this request. |

#### Response: `MinimalResponse` (verbose=false)

```json
{
  "passed": true,
  "composite_score": 0.650,
  "threshold": 0.60
}
```

---

## Image-Based Concepts

Test visual concepts like storyboards, ads, or product images using base64-encoded images:

```json
{
  "concept": {
    "name": "TV Ad Storyboard",
    "content": [
      {"type": "text", "data": "Two TV ad concepts are shown. Review both before answering."},
      {"type": "image", "data": "<base64-encoded-image>", "label": "Storyboard"}
    ]
  }
}
```

When images are present, the vision model interprets the image and personas respond to the visual content. Supported formats: JPEG, PNG, GIF, WebP.

## Filtering Personas

Use SQL-like expressions to target specific demographics:

```json
{
  "filters": ["gender=F", "age>=25", "country in [United Kingdom,Greece]"]
}
```

| Operator | Example | Description |
|----------|---------|-------------|
| `=` | `gender=F` | Equals |
| `!=` | `country!=Greece` | Not equals |
| `>` | `age>30` | Greater than |
| `>=` | `age>=25` | Greater than or equal |
| `<` | `age<50` | Less than |
| `<=` | `age<=65` | Less than or equal |
| `in` | `country in [United Kingdom,Greece]` | In list |

Filters are applied after LLM generation. Only matched personas contribute to metrics and scoring.

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| **API** | | |
| `API_HOST` | `0.0.0.0` | Server bind address |
| `API_PORT` | `8000` | Server port |
| `DEBUG` | `false` | Enable debug mode |
| **OpenAI** | | |
| `OPENAI_API_KEY` | required (if using OpenAI) | OpenAI API key |
| **AWS Bedrock** | | |
| `AWS_ACCESS_KEY_ID` | required (if using Bedrock) | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | required (if using Bedrock) | AWS secret key |
| `AWS_REGION` | `us-east-1` | AWS region (e.g. `eu-central-1`) |
| **Default Models** | | |
| `DEFAULT_GENERATION_PROVIDER` | `openai` | Default generation provider |
| `DEFAULT_GENERATION_MODEL` | `gpt-4o` | Default generation model |
| `DEFAULT_EMBEDDING_PROVIDER` | `openai` | Default embedding provider |
| `DEFAULT_EMBEDDING_MODEL` | `text-embedding-3-small` | Default embedding model |
| `DEFAULT_VISION_PROVIDER` | `openai` | Default vision provider |
| `DEFAULT_VISION_MODEL` | `gpt-4o` | Default vision model |
| `DEFAULT_TEMPERATURE` | `0.7` | Default LLM temperature |
| **SSR** | | |
| `SSR_SOFTMAX_TEMPERATURE` | `1.0` | PMF sharpening temperature. Lower = sharper distribution. |
| **Processing** | | |
| `BATCH_SIZE` | `10` | Legacy batch size setting |
| `CONCURRENCY_LIMIT` | `20` | Max concurrent personas in flight |

### Supported Models

#### OpenAI

| Capability | Models |
|------------|--------|
| Generation | `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo` |
| Embedding | `text-embedding-3-small`, `text-embedding-3-large`, `text-embedding-ada-002` |
| Vision | `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo` |

#### AWS Bedrock

| Capability | Models |
|------------|--------|
| Generation | `eu.anthropic.claude-sonnet-4-5-20250929-v1:0`, `eu.anthropic.claude-sonnet-4-20250514-v1:0`, `eu.anthropic.claude-3-7-sonnet-20250219-v1:0`, `eu.anthropic.claude-haiku-4-5-20251001-v1:0`, `anthropic.claude-3-5-sonnet-20240620-v1:0`, `anthropic.claude-3-haiku-20240307-v1:0` |
| Embedding | `amazon.titan-embed-text-v2:0`, `amazon.titan-embed-text-v1` |
| Vision | Same as Generation |

Note: Newer Claude models (4.x, 4.5) require EU inference profile IDs (`eu.` prefix) in `eu-central-1`. Direct model IDs work for older models (3.x).

## Concurrency Architecture

SAGE uses async concurrency to maximise throughput:

```
All personas launched concurrently (capped by CONCURRENCY_LIMIT semaphore)
  Each persona: all questions run concurrently via asyncio.gather()
    Each question: 1 LLM call + SSR mapping
      SSR: 1 embedding call + 6 reference set comparisons (parallel)
```

- **CONCURRENCY_LIMIT** (default 20) controls max in-flight personas
- Questions within each persona run in parallel
- SSR reference set processing is parallelised
- No artificial batch boundaries - new personas start as soon as a slot opens

## Generated Reports

When `include_report: true` (also requires `output_dataset: true` for sample responses), the response includes a markdown report with:

- **Test Overview**: Experiment ID, concept name, personas, processing time, models used (provider and model ID for generation, embedding, and vision)
- **Concept Description**: Concept format, text content, and image count
- **Result Summary**: Pass/fail with strength label (Marginal/Moderate/Clear), composite score, threshold, margin
- **Criteria Breakdown**: Per-question weights, raw means, normalized scores, contributions
- **Key Insights**: Top 3 strengths and bottom 2 weaknesses with median, spread, and std dev
- **Metrics Summary**: Mean, median, std dev, top/bottom 2 box per question
- **Distribution Analysis**: Aggregated rating counts across all questions with sentiment interpretation
- **Sample Responses**: 5 diverse personas with demographics and response excerpts
- **Conclusions**: 5 findings including overall result, strongest/weakest metrics, response consistency, and recommendation
- **Dataset Summary**: Demographics and data contents
- **Appendix**: Full survey questions with response scales from SSR reference sets

## SSR Methodology

The Semantic Similarity Rating method (paper Section A.4.3, equation 8):

1. **Generate Response**: LLM produces free-text response as the persona
2. **Embed Response**: Convert response to embedding vector
3. **Embed Anchors**: Embed all 5 anchors in each of 6 reference sets (cached after first use)
4. **Compute Similarity**: Calculate cosine similarity between response and each anchor
5. **Normalize**: Subtract minimum similarity, add epsilon to prevent division by zero
6. **PMF**: Convert to probability distribution via direct normalization (not softmax)
7. **Average**: Average PMFs across all 6 reference sets
8. **Calculate Mean**: Compute expected value (1-5 Likert score)

Key formula: `p(r) proportional to sim(response, anchor_r) - sim(response, anchor_min)`

The use of 6 independent reference sets with different phrasings provides robustness against semantic ambiguity in any single set.

## Testing

```bash
# Run unit tests
uv run pytest

# Run example tests against running API
cd testing
./run_tests.sh
```

See `testing/examples/` for sample inputs, outputs, reports, and comparison analyses.

## Project Structure

```
sage_API/
├── sage/
│   ├── main.py               # FastAPI application and logging setup
│   ├── config.py              # Settings, env vars, supported models
│   ├── models/
│   │   ├── request.py         # Input models (Concept, Question, Options, etc.)
│   │   └── response.py        # Output models (FullResponse, MinimalResponse, etc.)
│   ├── services/
│   │   ├── orchestrator.py    # Pipeline coordinator with semaphore concurrency
│   │   ├── llm_service.py     # LLM abstraction with logging
│   │   ├── llm_provider.py    # OpenAI and Bedrock provider implementations
│   │   ├── ssr_engine.py      # Semantic Similarity Rating with parallel processing
│   │   ├── filter_engine.py   # SQL-like persona filtering
│   │   ├── scoring_engine.py  # Metrics calculation and composite scoring
│   │   └── report_generator.py# Markdown report generation
│   ├── utils/
│   │   └── embeddings.py      # Cosine similarity utilities
│   └── tests/
│       ├── conftest.py        # Test fixtures
│       └── test_api.py        # API tests
├── testing/
│   ├── examples/              # Sample inputs, outputs, reports, comparisons
│   ├── images/                # Test images
│   └── run_tests.sh           # Test runner script
├── Dockerfile
├── pyproject.toml
└── .env.example
```

## Docker

```bash
# Build
docker build -t sage-api .

# Run with OpenAI
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... sage-api

# Run with Bedrock
docker run -p 8000:8000 \
  -e DEFAULT_GENERATION_PROVIDER=bedrock \
  -e DEFAULT_GENERATION_MODEL=eu.anthropic.claude-sonnet-4-5-20250929-v1:0 \
  -e DEFAULT_EMBEDDING_PROVIDER=bedrock \
  -e DEFAULT_EMBEDDING_MODEL=amazon.titan-embed-text-v2:0 \
  -e DEFAULT_VISION_PROVIDER=bedrock \
  -e DEFAULT_VISION_MODEL=eu.anthropic.claude-sonnet-4-5-20250929-v1:0 \
  -e AWS_ACCESS_KEY_ID=AKIA... \
  -e AWS_SECRET_ACCESS_KEY=... \
  -e AWS_REGION=eu-central-1 \
  sage-api
```

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

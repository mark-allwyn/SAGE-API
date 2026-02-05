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

- **Multi-Provider Support**: OpenAI and AWS Bedrock for generation, embeddings, vision, and video
- **Vision Support**: Test image-based concepts (storyboards, ads) via base64-encoded images
- **Video Support**: Test video-based concepts via YouTube URLs, direct MP4 links, S3 URIs, or base64 - with automatic download caching
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

For the full API specification with request/response schemas, field descriptions, and examples, see [`docs/api_specification_full.docx`](docs/api_specification_full.docx).

Interactive API docs are also available at http://localhost:8000/docs when the server is running.

---

## Example Request

```bash
curl -X POST http://localhost:8000/test-concept \
  -H "Content-Type: application/json" \
  -d '{
    "personas": [
      {"persona_id": "p1", "age": 28, "gender": "F", "country": "United Kingdom"}
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

## Video-Based Concepts

Test video concepts using YouTube URLs, direct MP4 links, S3 URIs, or base64-encoded video. Video content is processed by the Twelve Labs Pegasus model via AWS Bedrock:

```json
{
  "concept": {
    "name": "Sports Car Video",
    "content": [
      {"type": "text", "data": "We are going to show you a video"},
      {"type": "video", "data": "https://example.com/video.mp4"}
    ]
  },
  "options": {
    "video_provider": "bedrock",
    "video_model": "eu.twelvelabs.pegasus-1-2-v1:0"
  }
}
```

Supported video sources:

| Source | Format | Example |
|--------|--------|---------|
| YouTube | URL | `https://www.youtube.com/watch?v=abc123` |
| Direct URL | HTTP/HTTPS to MP4 | `https://example.com/video.mp4` |
| S3 | S3 URI | `s3://bucket/video.mp4` |
| Base64 | Encoded string | `AAAA/base64data...` |

Video downloads are cached per request - the same video is only downloaded once regardless of how many persona/question combinations reference it.

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
| `DEFAULT_VIDEO_PROVIDER` | `bedrock` | Default video provider |
| `DEFAULT_VIDEO_MODEL` | `eu.twelvelabs.pegasus-1-2-v1:0` | Default video model |
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
| Video | `eu.twelvelabs.pegasus-1-2-v1:0` |

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
│   │   ├── report_generator.py# Markdown report generation
│   │   └── video_downloader.py# Video source resolver with download caching
│   ├── utils/
│   │   └── embeddings.py      # Cosine similarity utilities
│   └── tests/
│       ├── conftest.py        # Test fixtures
│       └── test_api.py        # API tests
├── docs/
│   ├── api_specification_full.docx  # Full API specification
│   ├── SAGE_Business_Case.md        # Business case and cost model
│   └── 2510.08338v2.pdf             # SSR methodology paper (Maier et al.)
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

## References

- **SSR Methodology Paper**: [`docs/2510.08338v2.pdf`](docs/2510.08338v2.pdf) - Maier et al., "LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings" ([arXiv:2510.08338](https://arxiv.org/abs/2510.08338), 2025)
- **API Specification**: [`docs/api_specification_full.docx`](docs/api_specification_full.docx)
- **Business Case**: [`docs/SAGE_Business_Case.md`](docs/SAGE_Business_Case.md)

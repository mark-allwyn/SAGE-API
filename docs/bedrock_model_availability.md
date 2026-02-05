# Bedrock Model Availability

**Region**: eu-central-1 (Frankfurt)
**Last updated**: 2026-02-03

All models listed below have been tested and verified working with the SAGE API. The `BedrockGenerationProvider`, `BedrockVisionProvider`, and `BedrockEmbeddingProvider` detect the model family automatically and format requests accordingly.

---

## Generation Models

| Model ID | Family | Name | Input $/1M | Output $/1M |
|----------|--------|------|----------:|----------:|
| `eu.anthropic.claude-opus-4-5-20251101-v1:0` | Anthropic | Opus 4.5 | $5.00 | $25.00 |
| `eu.anthropic.claude-sonnet-4-5-20250929-v1:0` | Anthropic | Sonnet 4.5 | $3.00 | $15.00 |
| `eu.anthropic.claude-sonnet-4-20250514-v1:0` | Anthropic | Sonnet 4 | $3.00 | $15.00 |
| `eu.anthropic.claude-3-7-sonnet-20250219-v1:0` | Anthropic | Sonnet 3.7 | $3.00 | $15.00 |
| `eu.anthropic.claude-3-5-sonnet-20240620-v1:0` | Anthropic | Sonnet 3.5 | $3.00 | $15.00 |
| `eu.anthropic.claude-3-sonnet-20240229-v1:0` | Anthropic | Sonnet 3 | $3.00 | $15.00 |
| `eu.anthropic.claude-haiku-4-5-20251001-v1:0` | Anthropic | Haiku 4.5 | $1.00 | $5.00 |
| `eu.anthropic.claude-3-haiku-20240307-v1:0` | Anthropic | Haiku 3 | $0.25 | $1.25 |
| `eu.amazon.nova-pro-v1:0` | Nova | Nova Pro | $0.80 | $3.20 |
| `eu.amazon.nova-lite-v1:0` | Nova | Nova Lite | $0.06 | $0.24 |
| `eu.amazon.nova-2-lite-v1:0` | Nova | Nova 2 Lite | $0.04 | $0.16 |
| `eu.amazon.nova-micro-v1:0` | Nova | Nova Micro | $0.035 | $0.14 |
| `eu.mistral.pixtral-large-2502-v1:0` | Mistral | Pixtral Large | ~$2.00 | ~$6.00 |
| `eu.meta.llama3-2-3b-instruct-v1:0` | Llama | Llama 3.2 3B | $0.15 | $0.15 |
| `eu.meta.llama3-2-1b-instruct-v1:0` | Llama | Llama 3.2 1B | $0.10 | $0.10 |

---

## Vision Models

Vision-capable models that can process image content alongside text. Image tokens are billed at the same rate as text input tokens. A typical image costs ~1,600 tokens (low-res) to ~6,400 tokens (high-res).

| Model ID | Family | Name | Input $/1M | Output $/1M |
|----------|--------|------|----------:|----------:|
| `eu.anthropic.claude-opus-4-5-20251101-v1:0` | Anthropic | Opus 4.5 | $5.00 | $25.00 |
| `eu.anthropic.claude-sonnet-4-5-20250929-v1:0` | Anthropic | Sonnet 4.5 | $3.00 | $15.00 |
| `eu.anthropic.claude-sonnet-4-20250514-v1:0` | Anthropic | Sonnet 4 | $3.00 | $15.00 |
| `eu.anthropic.claude-3-7-sonnet-20250219-v1:0` | Anthropic | Sonnet 3.7 | $3.00 | $15.00 |
| `eu.anthropic.claude-3-5-sonnet-20240620-v1:0` | Anthropic | Sonnet 3.5 | $3.00 | $15.00 |
| `eu.anthropic.claude-3-sonnet-20240229-v1:0` | Anthropic | Sonnet 3 | $3.00 | $15.00 |
| `eu.anthropic.claude-haiku-4-5-20251001-v1:0` | Anthropic | Haiku 4.5 | $1.00 | $5.00 |
| `eu.anthropic.claude-3-haiku-20240307-v1:0` | Anthropic | Haiku 3 | $0.25 | $1.25 |
| `eu.amazon.nova-pro-v1:0` | Nova | Nova Pro | $0.80 | $3.20 |
| `eu.amazon.nova-lite-v1:0` | Nova | Nova Lite | $0.06 | $0.24 |
| `eu.amazon.nova-2-lite-v1:0` | Nova | Nova 2 Lite | $0.04 | $0.16 |
| `eu.mistral.pixtral-large-2502-v1:0` | Mistral | Pixtral Large | ~$2.00 | ~$6.00 |

**Not vision-capable**: Nova Micro (text-only), Llama 3.2 1B/3B (text-only). These can be used for generation but require a separate vision model when concepts contain images.

---

## Embedding Models

| Model ID | Family | Name | $/1M tokens | Dimensions | Notes |
|----------|--------|------|----------:|----------:|-------|
| `amazon.titan-embed-text-v2:0` | Titan | Titan Text v2 | $0.11 | 256/512/1024 | Default, configurable dimensions |
| `amazon.titan-embed-text-v1` | Titan | Titan Text v1 | $0.10 | 1536 | Fixed dimensions |
| `cohere.embed-english-v3` | Cohere | Cohere English v3 | $0.10 | 1024 | English only |
| `cohere.embed-multilingual-v3` | Cohere | Cohere Multilingual v3 | $0.10 | 1024 | 100+ languages |

---

## Not Available in eu-central-1

These models exist in Bedrock but are not enabled or accessible in this account/region.

| Model ID | Reason |
|----------|--------|
| `cohere.embed-v4:0` | Not enabled in account |
| `qwen.qwen3-235b-a22b-2507-v1:0` | Not supported by SAGE (different API format) |
| `qwen.qwen3-32b-v1:0` | Not supported by SAGE (different API format) |
| `qwen.qwen3-coder-30b-a3b-v1:0` | Not supported by SAGE (different API format) |

### Inference Profile Notes

Newer Anthropic models require the `eu.` inference profile prefix in eu-central-1. Only older models (Sonnet 3.5, Sonnet 3, Haiku 3) work with direct model IDs like `anthropic.claude-3-haiku-20240307-v1:0`.

---

## Cost Estimates per SAGE Experiment

Based on 90 personas, 5 questions, ~500 output tokens and ~200 input tokens per call.

Per experiment: ~450 generation calls + ~450 embedding calls + ~90 vision calls (if concept has images).

| Config | Generation Model | Vision Model | Embedding Model | Est. Total |
|--------|-----------------|-------------|----------------|-----------|
| Cheapest | Nova 2 Lite ($0.04/$0.16) | Nova Lite ($0.06/$0.24) | Titan v1 ($0.10) | **~$0.03** |
| Budget | Haiku 3 ($0.25/$1.25) | Haiku 3 ($0.25/$1.25) | Titan v2 ($0.11) | **~$0.09** |
| Mid-budget | Haiku 4.5 ($1.00/$5.00) | Haiku 4.5 ($1.00/$5.00) | Titan v2 ($0.11) | **~$0.33** |
| Mid-range | Sonnet 4.5 ($3.00/$15.00) | Sonnet 4.5 ($3.00/$15.00) | Titan v2 ($0.11) | **~$0.97** |
| Premium | Opus 4.5 ($5.00/$25.00) | Opus 4.5 ($5.00/$25.00) | Titan v2 ($0.11) | **~$1.61** |

Embedding costs are negligible compared to generation/vision costs.

---

## Summary

| Role | Count | Families |
|------|-------|----------|
| Generation | 15 models | Anthropic, Nova, Mistral, Llama |
| Vision | 12 models | Anthropic, Nova, Mistral |
| Embedding | 4 models | Titan, Cohere |

**15 generation x 4 embedding = 60 possible generation/embedding permutations**
**12 vision x 4 embedding = 48 possible vision/embedding permutations**

Sources: [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/), [Anthropic Pricing](https://docs.anthropic.com/en/docs/about-claude/pricing)

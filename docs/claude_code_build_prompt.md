# Synthetic Consumer Testing API - Build Specification

## Project Overview

Build a Python API that generates synthetic consumer survey responses to test product concepts. The API simulates how real consumers would respond by using LLMs to generate natural language responses, then converting those responses to Likert-scale probability distributions using Semantic Similarity Rating (SSR).

**The API must support both OpenAI and Amazon Bedrock as LLM providers.**

---

## Tech Stack

- **Language**: Python 3.11+
- **Package Manager**: uv (fast Python package installer)
- **Framework**: FastAPI
- **LLM Providers**: OpenAI API, Amazon Bedrock (Claude models)
- **Embeddings**: OpenAI text-embedding-3-small (for SSR)
- **Dependencies**: fastapi, uvicorn, pydantic, openai, boto3, numpy, scipy

---

## Core Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                           API Layer                              │
│                         (FastAPI + Pydantic)                     │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Orchestrator                              │
│            (Coordinates pipeline, applies filters)               │
└─────────────────────────────────────────────────────────────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           ▼                     ▼                     ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  LLM Provider   │   │   SSR Engine    │   │  Scoring Engine │
│  (OpenAI/Bedrock)│   │  (Embeddings)   │   │  (Aggregation)  │
└─────────────────┘   └─────────────────┘   └─────────────────┘
```

---

## File Structure

```
synthetic_consumer_api/
├── pyproject.toml             # Project config and dependencies (uv)
├── uv.lock                    # Lock file (auto-generated)
├── main.py                    # FastAPI app entry point
├── config.py                  # Configuration and environment variables
├── models/
│   ├── __init__.py
│   ├── request.py             # Pydantic input models
│   └── response.py            # Pydantic output models
├── services/
│   ├── __init__.py
│   ├── orchestrator.py        # Main pipeline orchestrator
│   ├── llm_provider.py        # Abstract LLM interface
│   ├── openai_provider.py     # OpenAI implementation
│   ├── bedrock_provider.py    # Amazon Bedrock implementation
│   ├── ssr_engine.py          # SSR mapping logic
│   ├── scoring_engine.py      # Aggregation and scoring
│   └── filter_engine.py       # Persona filtering
├── utils/
│   ├── __init__.py
│   └── embeddings.py          # Embedding utilities
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_ssr.py
│   └── test_scoring.py
├── Dockerfile
├── .env                       # Environment variables (not committed)
├── .env.example               # Example environment variables
└── README.md
```

---

## Input Schema (Pydantic Models)

### Request Model

```python
from pydantic import BaseModel, Field, field_validator
from typing import Any, Optional

class ContentItem(BaseModel):
    type: str  # "image" or "text"
    data: str  # base64 for image, string for text
    label: Optional[str] = None

class Concept(BaseModel):
    name: str
    content: list[ContentItem]
    metadata: Optional[dict[str, Any]] = None

class Question(BaseModel):
    id: str
    text: str
    weight: float
    ssr_reference_sets: list[list[str]]  # 6 sets of 5 anchors
    
    @field_validator('ssr_reference_sets')
    @classmethod
    def validate_reference_sets(cls, v):
        if len(v) != 6:
            raise ValueError('Must have exactly 6 reference sets')
        for i, ref_set in enumerate(v):
            if len(ref_set) != 5:
                raise ValueError(f'Reference set {i} must have exactly 5 anchors')
        return v

class SurveyConfig(BaseModel):
    questions: list[Question]
    
    @field_validator('questions')
    @classmethod
    def validate_weights(cls, v):
        total_weight = sum(q.weight for q in v)
        if not (0.99 <= total_weight <= 1.01):
            raise ValueError(f'Question weights must sum to 1.0, got {total_weight}')
        return v

class Options(BaseModel):
    # LLM Generation Settings
    generation_provider: str = "openai"  # "openai" or "bedrock"
    generation_model: str = "gpt-4o"     # OpenAI: gpt-4o, gpt-4-turbo / Bedrock: anthropic.claude-3-sonnet-20240229-v1:0
    generation_temperature: float = 0.7
    
    # Embedding Settings (for SSR)
    embedding_provider: str = "openai"   # "openai" or "bedrock"
    embedding_model: str = "text-embedding-3-small"  # OpenAI: text-embedding-3-small, text-embedding-3-large / Bedrock: amazon.titan-embed-text-v2:0
    
    # Vision Settings (for image processing)
    vision_provider: str = "openai"      # "openai" or "bedrock"
    vision_model: str = "gpt-4o"         # OpenAI: gpt-4o, gpt-4-turbo / Bedrock: anthropic.claude-3-sonnet-20240229-v1:0

class TestConceptRequest(BaseModel):
    personas: list[dict[str, Any]]  # Flexible schema, only persona_id required
    concept: Concept
    survey_config: SurveyConfig
    threshold: float = Field(ge=0, le=1)
    filters: list[str] = []
    verbose: bool = True
    output_dataset: bool = False
    options: Options = Options()
    
    @field_validator('personas')
    @classmethod
    def validate_personas(cls, v):
        if len(v) == 0:
            raise ValueError('At least one persona is required')
        ids = [p.get('persona_id') for p in v]
        if None in ids:
            raise ValueError('All personas must have a persona_id')
        if len(ids) != len(set(ids)):
            raise ValueError('All persona_ids must be unique')
        return v
```

---

## Output Schema (Pydantic Models)

```python
class ResultSummary(BaseModel):
    passed: bool
    composite_score: float
    threshold: float
    margin: float
    reason: str

class CriteriaBreakdown(BaseModel):
    question_id: str
    weight: float
    raw_mean: float
    normalized: float
    contribution: float

class QuestionMetrics(BaseModel):
    n: int
    mean: float
    median: float
    std_dev: float
    top_2_box: float
    bottom_2_box: float
    distribution: dict[str, int]

class Meta(BaseModel):
    request_id: str
    concept_name: str
    processing_time_ms: int

# Minimal response (verbose=false)
class MinimalResponse(BaseModel):
    passed: bool
    composite_score: float
    threshold: float

# Full response (verbose=true)
class FullResponse(BaseModel):
    result: ResultSummary
    filters_applied: list[str]
    personas_total: int
    personas_matched: int
    criteria_breakdown: list[CriteriaBreakdown]
    metrics: dict[str, QuestionMetrics]
    dataset: Optional[list[dict[str, Any]]] = None  # if output_dataset=true
    meta: Meta
```

---

## Provider Interfaces

The API supports **separate providers and models** for each capability:

| Capability | Providers | Example Models |
|------------|-----------|----------------|
| **Generation** | OpenAI, Bedrock | gpt-4o, gpt-4-turbo, claude-3-sonnet, claude-3-opus |
| **Embeddings** | OpenAI, Bedrock | text-embedding-3-small, text-embedding-3-large, titan-embed-text-v2 |
| **Vision** | OpenAI, Bedrock | gpt-4o, gpt-4-turbo, claude-3-sonnet, claude-3-opus |

### Provider Factory

```python
from enum import Enum
from typing import Protocol

class ProviderType(str, Enum):
    OPENAI = "openai"
    BEDROCK = "bedrock"

class GenerationProvider(Protocol):
    """Protocol for text generation providers."""
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7
    ) -> str: ...

class EmbeddingProvider(Protocol):
    """Protocol for embedding providers."""
    async def embed(self, texts: list[str]) -> list[list[float]]: ...
    async def embed_single(self, text: str) -> list[float]: ...

class VisionProvider(Protocol):
    """Protocol for vision (multimodal) providers."""
    async def generate_with_images(
        self,
        system_prompt: str,
        user_prompt: str,
        images: list[dict],  # [{"data": base64, "media_type": "image/jpeg"}]
        temperature: float = 0.7
    ) -> str: ...

class ProviderFactory:
    """Factory to create providers based on configuration."""
    
    @staticmethod
    def create_generation_provider(
        provider: str, 
        model: str
    ) -> GenerationProvider:
        if provider == ProviderType.OPENAI:
            return OpenAIGenerationProvider(model=model)
        elif provider == ProviderType.BEDROCK:
            return BedrockGenerationProvider(model=model)
        raise ValueError(f"Unknown generation provider: {provider}")
    
    @staticmethod
    def create_embedding_provider(
        provider: str, 
        model: str
    ) -> EmbeddingProvider:
        if provider == ProviderType.OPENAI:
            return OpenAIEmbeddingProvider(model=model)
        elif provider == ProviderType.BEDROCK:
            return BedrockEmbeddingProvider(model=model)
        raise ValueError(f"Unknown embedding provider: {provider}")
    
    @staticmethod
    def create_vision_provider(
        provider: str, 
        model: str
    ) -> VisionProvider:
        if provider == ProviderType.OPENAI:
            return OpenAIVisionProvider(model=model)
        elif provider == ProviderType.BEDROCK:
            return BedrockVisionProvider(model=model)
        raise ValueError(f"Unknown vision provider: {provider}")
```

---

## OpenAI Providers

### OpenAI Generation Provider

```python
from openai import AsyncOpenAI

class OpenAIGenerationProvider:
    """OpenAI provider for text generation."""
    
    def __init__(self, model: str = "gpt-4o"):
        self.client = AsyncOpenAI()
        self.model = model
    
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7
    ) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=500
        )
        return response.choices[0].message.content
```

### OpenAI Embedding Provider

```python
class OpenAIEmbeddingProvider:
    """OpenAI provider for embeddings."""
    
    def __init__(self, model: str = "text-embedding-3-small"):
        self.client = AsyncOpenAI()
        self.model = model
        self._cache = {}  # Cache embeddings for anchor texts
    
    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts."""
        response = await self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [d.embedding for d in response.data]
    
    async def embed_single(self, text: str) -> list[float]:
        """Embed a single text."""
        response = await self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding
    
    async def embed_with_cache(self, texts: list[str]) -> list[list[float]]:
        """Embed texts with caching (for anchor texts)."""
        cache_key = tuple(texts)
        if cache_key not in self._cache:
            self._cache[cache_key] = await self.embed(texts)
        return self._cache[cache_key]
```

### OpenAI Vision Provider

```python
class OpenAIVisionProvider:
    """OpenAI provider for vision (multimodal) tasks."""
    
    def __init__(self, model: str = "gpt-4o"):
        self.client = AsyncOpenAI()
        self.model = model
    
    async def generate_with_images(
        self,
        system_prompt: str,
        user_prompt: str,
        images: list[dict],
        temperature: float = 0.7
    ) -> str:
        # Build multimodal content
        content = []
        
        # Add images first
        for img in images:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{img['media_type']};base64,{img['data']}"
                }
            })
        
        # Add text prompt
        content.append({"type": "text", "text": user_prompt})
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ],
            temperature=temperature,
            max_tokens=500
        )
        return response.choices[0].message.content
```

---

## Amazon Bedrock Providers

### Bedrock Generation Provider

```python
import boto3
import json
from botocore.config import Config

class BedrockGenerationProvider:
    """Amazon Bedrock provider for text generation."""
    
    CLAUDE_MODELS = [
        "anthropic.claude-3-opus-20240229-v1:0",
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-5-sonnet-20240620-v1:0"
    ]
    
    def __init__(self, model: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        self.client = boto3.client(
            'bedrock-runtime',
            config=Config(read_timeout=300)
        )
        self.model = model
    
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7
    ) -> str:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "temperature": temperature,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        }
        
        response = self.client.invoke_model(
            modelId=self.model,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
```

### Bedrock Embedding Provider

```python
class BedrockEmbeddingProvider:
    """Amazon Bedrock provider for embeddings (Titan)."""
    
    def __init__(self, model: str = "amazon.titan-embed-text-v2:0"):
        self.client = boto3.client('bedrock-runtime')
        self.model = model
        self._cache = {}
    
    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts (Titan processes one at a time)."""
        embeddings = []
        for text in texts:
            emb = await self.embed_single(text)
            embeddings.append(emb)
        return embeddings
    
    async def embed_single(self, text: str) -> list[float]:
        """Embed a single text."""
        body = json.dumps({
            "inputText": text,
            "dimensions": 1024,  # Titan v2 supports 256, 512, 1024
            "normalize": True
        })
        
        response = self.client.invoke_model(
            modelId=self.model,
            body=body
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['embedding']
    
    async def embed_with_cache(self, texts: list[str]) -> list[list[float]]:
        """Embed texts with caching."""
        cache_key = tuple(texts)
        if cache_key not in self._cache:
            self._cache[cache_key] = await self.embed(texts)
        return self._cache[cache_key]
```

### Bedrock Vision Provider

```python
class BedrockVisionProvider:
    """Amazon Bedrock provider for vision (Claude multimodal)."""
    
    def __init__(self, model: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        self.client = boto3.client(
            'bedrock-runtime',
            config=Config(read_timeout=300)
        )
        self.model = model
    
    async def generate_with_images(
        self,
        system_prompt: str,
        user_prompt: str,
        images: list[dict],
        temperature: float = 0.7
    ) -> str:
        # Build multimodal content for Claude
        content = []
        
        # Add images
        for img in images:
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": img['media_type'],
                    "data": img['data']
                }
            })
        
        # Add text prompt
        content.append({"type": "text", "text": user_prompt})
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "temperature": temperature,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": content}
            ]
        }
        
        response = self.client.invoke_model(
            modelId=self.model,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
```

---

## LLM Service (Unified Interface)

```python
class LLMService:
    """
    Unified service that uses the appropriate provider based on configuration.
    Handles both text-only and multimodal (vision) requests.
    """
    
    def __init__(self, options: Options):
        self.options = options
        
        # Create providers based on options
        self.generation_provider = ProviderFactory.create_generation_provider(
            options.generation_provider,
            options.generation_model
        )
        self.embedding_provider = ProviderFactory.create_embedding_provider(
            options.embedding_provider,
            options.embedding_model
        )
        self.vision_provider = ProviderFactory.create_vision_provider(
            options.vision_provider,
            options.vision_model
        )
    
    async def generate_response(
        self,
        persona: dict,
        concept: Concept,
        question: Question
    ) -> str:
        """Generate a response, using vision if images are present."""
        system_prompt = self._build_system_prompt(persona)
        user_prompt = self._build_user_prompt(concept, question)
        
        # Check if concept has images
        images = [
            {"data": c.data, "media_type": "image/jpeg"}
            for c in concept.content if c.type == "image"
        ]
        
        if images:
            # Use vision provider for multimodal
            return await self.vision_provider.generate_with_images(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                images=images,
                temperature=self.options.generation_temperature
            )
        else:
            # Use generation provider for text-only
            return await self.generation_provider.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=self.options.generation_temperature
            )
    
    async def get_embedding(self, text: str) -> list[float]:
        """Get embedding for a single text."""
        return await self.embedding_provider.embed_single(text)
    
    async def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings for multiple texts."""
        return await self.embedding_provider.embed(texts)
    
    async def get_embeddings_cached(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings with caching (for anchor texts)."""
        return await self.embedding_provider.embed_with_cache(texts)
    
    def _build_system_prompt(self, persona: dict) -> str:
        persona_desc = self._format_persona(persona)
        return f"""You are role-playing as a consumer with the following characteristics:

{persona_desc}

Respond naturally and authentically as this person would. Your responses should reflect your demographics, lifestyle, and perspective. Be genuine - if something doesn't appeal to you, say so honestly."""

    def _format_persona(self, persona: dict) -> str:
        lines = []
        for key, value in persona.items():
            if key != 'persona_id':
                formatted_key = key.replace('_', ' ').title()
                lines.append(f"- {formatted_key}: {value}")
        return '\n'.join(lines)
    
    def _build_user_prompt(self, concept: Concept, question: Question) -> str:
        text_content = '\n'.join([
            c.data for c in concept.content if c.type == 'text'
        ])
        
        prompt = f'Here is a product concept for "{concept.name}":\n\n'
        
        if text_content:
            prompt += f"{text_content}\n\n"
        
        prompt += f"""Please respond to this question in 2-3 sentences, speaking as yourself:

{question.text}

Give your honest reaction as this consumer would."""
        
        return prompt
```

---

## SSR Engine

```python
import numpy as np

class SSREngine:
    """
    Semantic Similarity Rating engine.
    Maps free-text responses to Likert PMF using embeddings.
    """
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self._anchor_cache = {}
    
    async def map_response_to_likert(
        self,
        response_text: str,
        ssr_reference_sets: list[list[str]]
    ) -> tuple[list[float], float]:
        """
        Map a free-text response to a Likert PMF and mean.
        
        Returns:
            pmf: [p1, p2, p3, p4, p5] probability distribution
            mean: expected value (1-5)
        """
        # Get response embedding
        response_embedding = await self.llm_service.get_embedding(response_text)
        
        # Get PMF from each reference set
        pmfs = []
        for ref_set in ssr_reference_sets:
            pmf = await self._compute_pmf_for_set(response_embedding, ref_set)
            pmfs.append(pmf)
        
        # Average all PMFs
        avg_pmf = np.mean(pmfs, axis=0).tolist()
        
        # Calculate expected value (mean)
        mean = sum((i + 1) * p for i, p in enumerate(avg_pmf))
        
        return avg_pmf, mean
    
    async def _compute_pmf_for_set(
        self,
        response_embedding: list[float],
        reference_set: list[str]
    ) -> list[float]:
        """Compute PMF using cosine similarity to anchor texts."""
        # Get anchor embeddings (cached)
        cache_key = tuple(reference_set)
        if cache_key not in self._anchor_cache:
            self._anchor_cache[cache_key] = await self.llm_service.get_embeddings(reference_set)
        
        anchor_embeddings = self._anchor_cache[cache_key]
        
        # Compute cosine similarities
        similarities = [
            self._cosine_similarity(response_embedding, anchor_emb)
            for anchor_emb in anchor_embeddings
        ]
        
        # Convert to PMF using softmax with temperature
        pmf = self._softmax(similarities, temperature=0.5)
        
        return pmf
    
    @staticmethod
    def _cosine_similarity(a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        a = np.array(a)
        b = np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    
    @staticmethod
    def _softmax(x: list[float], temperature: float = 1.0) -> list[float]:
        """Apply softmax with temperature scaling."""
        x = np.array(x) / temperature
        exp_x = np.exp(x - np.max(x))  # Subtract max for numerical stability
        return (exp_x / exp_x.sum()).tolist()
```

---

## Filter Engine

```python
import re
from typing import Any

class FilterEngine:
    """Apply filters to subset personas."""
    
    OPERATORS = {
        '>=': lambda a, b: a >= b,
        '<=': lambda a, b: a <= b,
        '!=': lambda a, b: a != b,
        '>': lambda a, b: a > b,
        '<': lambda a, b: a < b,
        '=': lambda a, b: a == b,
    }
    
    def apply_filters(
        self, 
        personas: list[dict[str, Any]], 
        filters: list[str]
    ) -> tuple[list[dict], list[bool]]:
        """
        Apply filters to personas.
        
        Returns:
            filtered_personas: List of personas matching all filters
            match_flags: Boolean list indicating which personas matched
        """
        if not filters:
            return personas, [True] * len(personas)
        
        match_flags = []
        filtered = []
        
        for persona in personas:
            matches = all(self._evaluate_filter(persona, f) for f in filters)
            match_flags.append(matches)
            if matches:
                filtered.append(persona)
        
        return filtered, match_flags
    
    def _evaluate_filter(self, persona: dict, filter_expr: str) -> bool:
        """Evaluate a single filter expression against a persona."""
        # Handle 'in' operator: field in [val1,val2,val3]
        in_match = re.match(r'(\w+)\s+in\s+\[([^\]]+)\]', filter_expr)
        if in_match:
            field = in_match.group(1)
            values = [v.strip() for v in in_match.group(2).split(',')]
            persona_value = persona.get(field)
            return str(persona_value) in values
        
        # Handle comparison operators
        for op in ['>=', '<=', '!=', '>', '<', '=']:
            if op in filter_expr:
                field, value = filter_expr.split(op, 1)
                field = field.strip()
                value = value.strip()
                
                persona_value = persona.get(field)
                if persona_value is None:
                    return False
                
                # Try numeric comparison
                try:
                    persona_value = float(persona_value)
                    value = float(value)
                except (ValueError, TypeError):
                    pass
                
                return self.OPERATORS[op](persona_value, value)
        
        raise ValueError(f"Invalid filter expression: {filter_expr}")
```

---

## Scoring Engine

```python
import numpy as np
from typing import Any

class ScoringEngine:
    """Aggregate scores and evaluate against threshold."""
    
    def calculate_metrics(
        self,
        responses: list[dict[str, Any]],
        questions: list[Question],
        match_flags: list[bool]
    ) -> dict[str, dict]:
        """Calculate metrics for each question using only matched personas."""
        metrics = {}
        
        for question in questions:
            q_id = question.id
            
            # Get means for matched personas only
            means = [
                r['responses'][q_id]['mean']
                for r, matched in zip(responses, match_flags)
                if matched
            ]
            
            if not means:
                raise ValueError("No personas matched the filters")
            
            # Convert means to discrete Likert for distribution
            discrete = [round(m) for m in means]
            
            metrics[q_id] = {
                'n': len(means),
                'mean': round(np.mean(means), 2),
                'median': round(np.median(means), 2),
                'std_dev': round(np.std(means), 2),
                'top_2_box': round(sum(1 for m in means if m >= 4) / len(means), 2),
                'bottom_2_box': round(sum(1 for m in means if m <= 2) / len(means), 2),
                'distribution': {
                    str(i): discrete.count(i) for i in range(1, 6)
                }
            }
        
        return metrics
    
    def calculate_composite_score(
        self,
        metrics: dict[str, dict],
        questions: list[Question]
    ) -> tuple[float, list[dict]]:
        """
        Calculate composite score and breakdown.
        
        Returns:
            composite_score: Weighted sum of normalized scores (0-1)
            breakdown: Per-question breakdown
        """
        breakdown = []
        composite = 0.0
        
        for question in questions:
            q_id = question.id
            raw_mean = metrics[q_id]['mean']
            
            # Normalize: (mean - 1) / 4 maps 1-5 to 0-1
            normalized = (raw_mean - 1) / 4
            
            # Apply weight
            contribution = normalized * question.weight
            composite += contribution
            
            breakdown.append({
                'question_id': q_id,
                'weight': question.weight,
                'raw_mean': raw_mean,
                'normalized': round(normalized, 3),
                'contribution': round(contribution, 3)
            })
        
        return round(composite, 3), breakdown
    
    def evaluate_threshold(
        self,
        composite_score: float,
        threshold: float
    ) -> dict:
        """Evaluate composite score against threshold."""
        passed = composite_score >= threshold
        margin = round(composite_score - threshold, 3)
        
        if passed:
            reason = f"PASS: Composite score {composite_score} meets threshold {threshold}"
        else:
            reason = f"FAIL: Composite score {composite_score} is below threshold {threshold}"
        
        return {
            'passed': passed,
            'composite_score': composite_score,
            'threshold': threshold,
            'margin': margin,
            'reason': reason
        }
```

---

## Orchestrator

```python
import asyncio
import time
import uuid
from typing import Any

class Orchestrator:
    """Coordinates the entire pipeline."""
    
    def __init__(self):
        self.filter_engine = FilterEngine()
        self.scoring_engine = ScoringEngine()
    
    async def process_request(
        self,
        request: TestConceptRequest
    ) -> dict[str, Any]:
        """Process a concept test request."""
        start_time = time.time()
        request_id = str(uuid.uuid4())[:8]
        
        # Create LLM service with specified providers/models
        llm_service = LLMService(request.options)
        
        # Create SSR engine with the LLM service (uses its embedding provider)
        ssr_engine = SSREngine(llm_service)
        
        # Step 1: Generate responses for all personas
        responses = await self._generate_all_responses(
            llm_service,
            ssr_engine,
            request.personas,
            request.concept,
            request.survey_config.questions
        )
        
        # Step 2: Apply filters
        _, match_flags = self.filter_engine.apply_filters(
            request.personas, 
            request.filters
        )
        personas_matched = sum(match_flags)
        
        if personas_matched == 0:
            raise ValueError("No personas matched the specified filters")
        
        # Step 3: Calculate metrics (using filtered personas)
        metrics = self.scoring_engine.calculate_metrics(
            responses,
            request.survey_config.questions,
            match_flags
        )
        
        # Step 4: Calculate composite score
        composite_score, breakdown = self.scoring_engine.calculate_composite_score(
            metrics,
            request.survey_config.questions
        )
        
        # Step 5: Evaluate threshold
        result = self.scoring_engine.evaluate_threshold(
            composite_score,
            request.threshold
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Build response based on verbose flag
        if not request.verbose:
            return {
                'passed': result['passed'],
                'composite_score': result['composite_score'],
                'threshold': result['threshold']
            }
        
        response = {
            'result': result,
            'filters_applied': request.filters,
            'personas_total': len(request.personas),
            'personas_matched': personas_matched,
            'criteria_breakdown': breakdown,
            'metrics': metrics,
            'meta': {
                'request_id': request_id,
                'concept_name': request.concept.name,
                'processing_time_ms': processing_time,
                'providers': {
                    'generation': f"{request.options.generation_provider}/{request.options.generation_model}",
                    'embedding': f"{request.options.embedding_provider}/{request.options.embedding_model}",
                    'vision': f"{request.options.vision_provider}/{request.options.vision_model}"
                }
            }
        }
        
        # Add dataset if requested
        if request.output_dataset:
            response['dataset'] = self._build_dataset(
                request.personas,
                responses,
                match_flags,
                request.survey_config.questions
            )
        
        return response
    
    async def _generate_all_responses(
        self,
        llm_service: LLMService,
        ssr_engine: SSREngine,
        personas: list[dict],
        concept: Concept,
        questions: list[Question]
    ) -> list[dict]:
        """Generate responses for all personas and questions."""
        responses = []
        
        # Process personas in batches for efficiency
        batch_size = 10
        for i in range(0, len(personas), batch_size):
            batch = personas[i:i + batch_size]
            batch_responses = await asyncio.gather(*[
                self._process_single_persona(llm_service, ssr_engine, p, concept, questions)
                for p in batch
            ])
            responses.extend(batch_responses)
        
        return responses
    
    async def _process_single_persona(
        self,
        llm_service: LLMService,
        ssr_engine: SSREngine,
        persona: dict,
        concept: Concept,
        questions: list[Question]
    ) -> dict:
        """Process all questions for a single persona."""
        persona_responses = {'persona_id': persona['persona_id'], 'responses': {}}
        
        for question in questions:
            # Generate LLM response (uses vision provider if images present)
            raw_text = await llm_service.generate_response(
                persona, concept, question
            )
            
            # Map to Likert using SSR (uses embedding provider)
            pmf, mean = await ssr_engine.map_response_to_likert(
                raw_text,
                question.ssr_reference_sets
            )
            
            persona_responses['responses'][question.id] = {
                'raw_text': raw_text,
                'pmf': [round(p, 3) for p in pmf],
                'mean': round(mean, 2)
            }
        
        return persona_responses
    
    def _build_dataset(
        self,
        personas: list[dict],
        responses: list[dict],
        match_flags: list[bool],
        questions: list[Question]
    ) -> list[dict]:
        """Build flat dataset with personas + results."""
        dataset = []
        
        for persona, response, matched in zip(personas, responses, match_flags):
            row = {**persona, 'matched_filter': matched}
            
            for question in questions:
                q_id = question.id
                q_response = response['responses'][q_id]
                row[f'{q_id}_text'] = q_response['raw_text']
                row[f'{q_id}_pmf'] = q_response['pmf']
                row[f'{q_id}_mean'] = q_response['mean']
            
            dataset.append(row)
        
        return dataset
```

---

## FastAPI Application

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Synthetic Consumer Testing API",
    description="Generate synthetic consumer survey responses using LLM + SSR",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()

@app.post("/test-concept")
async def test_concept(request: TestConceptRequest):
    """
    Test a product concept with synthetic consumer personas.
    
    Returns PASS/FAIL based on composite score vs threshold.
    """
    try:
        result = await orchestrator.process_request(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

## Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-...

# For Bedrock (use IAM role or explicit credentials)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

---

## Example API Calls

### Example 1: All OpenAI

```bash
curl -X POST http://localhost:8000/test-concept \
  -H "Content-Type: application/json" \
  -d '{
    "personas": [
      {"persona_id": "p_001", "age": 32, "gender": "F", "income": "high"},
      {"persona_id": "p_002", "age": 45, "gender": "M", "income": "medium"},
      {"persona_id": "p_003", "age": 28, "gender": "F", "income": "high"}
    ],
    "concept": {
      "name": "AuraFoam Body Wash",
      "content": [
        {"type": "text", "data": "Mood-infused body wash with prebiotic hydration. Sulfate-free, dermatologist-tested."}
      ]
    },
    "survey_config": {
      "questions": [
        {
          "id": "purchase_intent",
          "text": "How likely are you to purchase this product?",
          "weight": 1.0,
          "ssr_reference_sets": [
            ["I would definitely not purchase", "I probably would not purchase", "I might or might not purchase", "I probably would purchase", "I would definitely purchase"],
            ["Very unlikely I would buy", "Rather unlikely I would buy", "Undecided about buying", "Rather likely I would buy", "Very likely I would buy"],
            ["No intention of buying", "Unlikely to consider buying", "Neutral about purchasing", "Likely to consider buying", "Fully intend to buy"],
            ["Does not interest me at all", "Barely interests me", "Somewhat interests me", "Interests me quite a bit", "Interests me greatly"],
            ["Would never consider buying", "Unlikely to purchase", "Undecided", "Likely to purchase", "Certain I would purchase"],
            ["No chance I would buy", "Small chance", "Moderate chance", "Good chance", "Excellent chance"]
          ]
        }
      ]
    },
    "threshold": 0.70,
    "filters": ["gender=F"],
    "verbose": true,
    "output_dataset": true,
    "options": {
      "generation_provider": "openai",
      "generation_model": "gpt-4o",
      "generation_temperature": 0.7,
      "embedding_provider": "openai",
      "embedding_model": "text-embedding-3-small",
      "vision_provider": "openai",
      "vision_model": "gpt-4o"
    }
  }'
```

### Example 2: All Bedrock (Claude)

```bash
curl -X POST http://localhost:8000/test-concept \
  -H "Content-Type: application/json" \
  -d '{
    "personas": [
      {"persona_id": "p_001", "age": 32, "gender": "F", "income": "high"}
    ],
    "concept": {
      "name": "AuraFoam Body Wash",
      "content": [
        {"type": "image", "data": "<base64_image_data>", "label": "Product hero"},
        {"type": "text", "data": "Mood-infused body wash with prebiotic hydration."}
      ]
    },
    "survey_config": {
      "questions": [
        {
          "id": "purchase_intent",
          "text": "How likely are you to purchase this product?",
          "weight": 1.0,
          "ssr_reference_sets": [...]
        }
      ]
    },
    "threshold": 0.70,
    "verbose": true,
    "options": {
      "generation_provider": "bedrock",
      "generation_model": "anthropic.claude-3-sonnet-20240229-v1:0",
      "generation_temperature": 0.7,
      "embedding_provider": "bedrock",
      "embedding_model": "amazon.titan-embed-text-v2:0",
      "vision_provider": "bedrock",
      "vision_model": "anthropic.claude-3-sonnet-20240229-v1:0"
    }
  }'
```

### Example 3: Mixed Providers (Bedrock for generation, OpenAI for embeddings)

```bash
curl -X POST http://localhost:8000/test-concept \
  -H "Content-Type: application/json" \
  -d '{
    "personas": [...],
    "concept": {...},
    "survey_config": {...},
    "threshold": 0.70,
    "verbose": true,
    "options": {
      "generation_provider": "bedrock",
      "generation_model": "anthropic.claude-3-5-sonnet-20240620-v1:0",
      "generation_temperature": 0.7,
      "embedding_provider": "openai",
      "embedding_model": "text-embedding-3-large",
      "vision_provider": "bedrock",
      "vision_model": "anthropic.claude-3-opus-20240229-v1:0"
    }
  }'
```

### Response (verbose=true, output_dataset=true)

```json
{
  "result": {
    "passed": true,
    "composite_score": 0.742,
    "threshold": 0.70,
    "margin": 0.042,
    "reason": "PASS: Composite score 0.742 meets threshold 0.70"
  },
  "filters_applied": ["gender=F"],
  "personas_total": 3,
  "personas_matched": 2,
  "criteria_breakdown": [
    {
      "question_id": "purchase_intent",
      "weight": 1.0,
      "raw_mean": 3.97,
      "normalized": 0.742,
      "contribution": 0.742
    }
  ],
  "metrics": {
    "purchase_intent": {
      "n": 2,
      "mean": 3.97,
      "median": 3.97,
      "std_dev": 0.28,
      "top_2_box": 1.0,
      "bottom_2_box": 0.0,
      "distribution": {"1": 0, "2": 0, "3": 0, "4": 2, "5": 0}
    }
  },
  "dataset": [
    {
      "persona_id": "p_001",
      "age": 32,
      "gender": "F",
      "income": "high",
      "matched_filter": true,
      "purchase_intent_text": "I love the mood-infused concept! As someone who values self-care...",
      "purchase_intent_pmf": [0.02, 0.05, 0.18, 0.42, 0.33],
      "purchase_intent_mean": 3.99
    },
    {
      "persona_id": "p_002",
      "age": 45,
      "gender": "M",
      "income": "medium",
      "matched_filter": false,
      "purchase_intent_text": "It's not really my thing...",
      "purchase_intent_pmf": [0.08, 0.18, 0.35, 0.28, 0.11],
      "purchase_intent_mean": 3.16
    },
    {
      "persona_id": "p_003",
      "age": 28,
      "gender": "F",
      "income": "high",
      "matched_filter": true,
      "purchase_intent_text": "This is exactly what I've been looking for!...",
      "purchase_intent_pmf": [0.01, 0.03, 0.12, 0.40, 0.44],
      "purchase_intent_mean": 4.23
    }
  ],
  "meta": {
    "request_id": "abc12345",
    "concept_name": "AuraFoam Body Wash",
    "processing_time_ms": 8420
  }
}
```

---

## Testing

Write tests for:

1. **Input validation** - Invalid personas, missing fields, weights not summing to 1.0
2. **Filter engine** - All operators, edge cases, no matches
3. **SSR engine** - PMF calculation, embedding caching, mean calculation
4. **Scoring engine** - Normalization, weighting, threshold evaluation
5. **Integration** - Full pipeline with mock LLM responses

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run specific test file
uv run pytest tests/test_ssr.py -v

# Run tests matching pattern
uv run pytest -k "test_filter" -v
```

### Linting and Formatting

```bash
# Check linting
uv run ruff check .

# Fix linting issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

---

## Deployment

### Project Setup with uv

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create new project
uv init synthetic_consumer_api
cd synthetic_consumer_api

# Add dependencies
uv add fastapi uvicorn pydantic openai boto3 numpy scipy python-dotenv

# Add dev dependencies
uv add --dev pytest pytest-asyncio httpx ruff

# Run the application
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### pyproject.toml

```toml
[project]
name = "synthetic-consumer-api"
version = "1.0.0"
description = "Generate synthetic consumer survey responses using LLM + SSR"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn>=0.32.0",
    "pydantic>=2.10.0",
    "openai>=1.55.0",
    "boto3>=1.35.0",
    "numpy>=2.0.0",
    "scipy>=1.14.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.27.0",
    "ruff>=0.8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY . .

# Install dependencies using uv
RUN uv sync --frozen --no-dev

EXPOSE 8000

# Run with uv
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Alternative: Dockerfile without uv in runtime

```dockerfile
FROM python:3.11-slim AS builder

# Install uv for building
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Create virtual environment and install dependencies
RUN uv venv /app/.venv
RUN uv sync --frozen --no-dev

FROM python:3.11-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Key Implementation Notes

1. **Async throughout** - Use async/await for all LLM and embedding calls
2. **Batch processing** - Process personas in batches to avoid rate limits
3. **Caching** - Cache anchor embeddings to reduce API calls
4. **Error handling** - Graceful handling of LLM failures, empty filter results
5. **Validation** - Strict Pydantic validation on inputs
6. **Logging** - Add structured logging for debugging
7. **Rate limiting** - Consider adding rate limiting for production
8. **Cost tracking** - Track token usage for cost monitoring

---

## Summary

Build this API using the specifications above. The key components are:

1. **FastAPI app** with Pydantic models for validation
2. **Pluggable providers** for each capability:
   - **Generation**: OpenAI (gpt-4o, gpt-4-turbo) or Bedrock (Claude 3 Sonnet, Opus, Haiku)
   - **Embeddings**: OpenAI (text-embedding-3-small/large) or Bedrock (Titan Embed v2)
   - **Vision**: OpenAI (gpt-4o, gpt-4-turbo) or Bedrock (Claude 3 multimodal)
3. **LLM Service** that unifies all providers and handles text-only vs multimodal requests
4. **SSR engine** for mapping text to Likert distributions using embeddings
5. **Filter engine** for subsetting personas
6. **Scoring engine** for aggregation and threshold evaluation
7. **Orchestrator** to coordinate the pipeline

### Supported Models

| Provider | Generation | Embeddings | Vision |
|----------|------------|------------|--------|
| **OpenAI** | gpt-4o, gpt-4-turbo, gpt-4, gpt-3.5-turbo | text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002 | gpt-4o, gpt-4-turbo |
| **Bedrock** | claude-3-opus, claude-3-sonnet, claude-3-haiku, claude-3.5-sonnet | amazon.titan-embed-text-v2:0, amazon.titan-embed-text-v1 | claude-3-opus, claude-3-sonnet, claude-3-haiku |

### Key Features

- **Separate provider/model for each capability** - Mix and match as needed
- **Automatic vision detection** - Uses vision provider when concept has images
- **Embedding caching** - Anchor texts are cached to reduce API calls
- **Async processing** - Batch processing for efficiency
- **Flexible personas** - Any demographic fields you need
- **Powerful filtering** - Subset personas with SQL-like expressions

Test thoroughly with both providers and deploy with Docker using uv.

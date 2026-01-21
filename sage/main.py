"""
SAGE - Synthetic Consumer Testing API

Generate synthetic consumer survey responses using LLM + Semantic Similarity Rating (SSR).
Based on the methodology from "LLMs Reproduce Human Purchase Intent via Semantic Similarity
Elicitation of Likert Ratings" (Maier et al., 2025).
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import SUPPORTED_MODELS, get_settings
from .models.request import TestConceptRequest
from .models.response import FullResponse, MinimalResponse
from .services.orchestrator import Orchestrator

# Initialize settings and orchestrator
settings = get_settings()
orchestrator = Orchestrator()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title="SAGE API",
    description="""
SAGE - Generate synthetic consumer survey responses using LLM + Semantic Similarity Rating (SSR).

This API simulates how real consumers would respond to product concepts by:
1. Using LLMs to generate natural language responses from demographic personas
2. Converting responses to Likert-scale probability distributions using SSR
3. Aggregating scores and evaluating against pass/fail thresholds

**Key Features:**
- Support for OpenAI and Amazon Bedrock as LLM providers
- Flexible persona demographics with SQL-like filtering
- Configurable survey questions with custom SSR reference sets
- Detailed metrics and optional raw dataset output
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/test-concept",
    response_model=FullResponse | MinimalResponse,
    summary="Test a product concept",
    description="""
Test a product concept with synthetic consumer personas.

**Process:**
1. Each persona is prompted to role-play as a consumer with specific demographics
2. The LLM generates a natural language response about purchase intent
3. SSR maps the response to a Likert distribution using embedding similarity
4. Scores are aggregated across matched personas
5. Composite score is evaluated against the threshold

**Returns PASS/FAIL based on composite score vs threshold.**
    """,
)
async def test_concept(
    request: TestConceptRequest,
) -> FullResponse | MinimalResponse:
    """
    Test a product concept with synthetic consumer personas.

    Args:
        request: TestConceptRequest with personas, concept, and configuration

    Returns:
        FullResponse if verbose=true, MinimalResponse otherwise
    """
    try:
        result = await orchestrator.process_request(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get(
    "/health",
    summary="Health check",
    description="Check if the API is running.",
)
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get(
    "/models",
    summary="List supported models",
    description="Get a list of supported models for each provider and capability.",
)
async def list_models() -> dict:
    """List supported models by provider."""
    return SUPPORTED_MODELS


@app.get(
    "/info",
    summary="API information",
    description="Get information about the API and its configuration.",
)
async def api_info() -> dict:
    """Get API information."""
    return {
        "name": "SAGE API",
        "version": "1.0.0",
        "description": "SAGE - Synthetic consumer survey responses using LLM + SSR",
        "methodology": "Semantic Similarity Rating (SSR)",
        "paper": "LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings",
        "default_settings": {
            "generation_provider": settings.default_generation_provider,
            "generation_model": settings.default_generation_model,
            "embedding_provider": settings.default_embedding_provider,
            "embedding_model": settings.default_embedding_model,
            "vision_provider": settings.default_vision_provider,
            "vision_model": settings.default_vision_model,
            "temperature": settings.default_temperature,
            "ssr_softmax_temperature": settings.ssr_softmax_temperature,
            "batch_size": settings.batch_size,
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )

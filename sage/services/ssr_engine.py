"""
Semantic Similarity Rating (SSR) engine.

Implements the SSR methodology from the research paper:
"LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings"

The SSR method:
1. Takes a free-text response from an LLM
2. Embeds the response and reference anchor statements
3. Computes cosine similarity to each anchor (representing Likert scale points 1-5)
4. Converts similarities to a probability mass function using softmax
5. Averages across multiple reference sets for robustness
"""

import numpy as np

from ..utils.embeddings import cosine_similarity, softmax
from .llm_service import LLMService


class SSREngine:
    """
    Semantic Similarity Rating engine.
    Maps free-text responses to Likert PMF using embeddings.
    """

    def __init__(self, llm_service: LLMService, temperature: float = 0.5):
        """
        Initialize SSR engine.

        Args:
            llm_service: LLM service for getting embeddings
            temperature: Softmax temperature (lower = sharper distribution)
        """
        self.llm_service = llm_service
        self.temperature = temperature
        self._anchor_cache: dict[tuple[str, ...], list[list[float]]] = {}

    async def map_response_to_likert(
        self,
        response_text: str,
        ssr_reference_sets: list[list[str]],
    ) -> tuple[list[float], float]:
        """
        Map a free-text response to a Likert PMF and mean.

        This implements the SSR algorithm:
        1. Get embedding for the response
        2. For each reference set:
           a. Get embeddings for the 5 anchor statements
           b. Compute cosine similarity between response and each anchor
           c. Convert to PMF using softmax with temperature
        3. Average all PMFs across reference sets
        4. Calculate expected value (mean)

        Args:
            response_text: Free-text response from LLM
            ssr_reference_sets: 6 sets of 5 anchor statements each

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

        # Calculate expected value (mean) - Likert scale is 1-5
        mean = sum((i + 1) * p for i, p in enumerate(avg_pmf))

        return avg_pmf, mean

    async def _compute_pmf_for_set(
        self,
        response_embedding: list[float],
        reference_set: list[str],
    ) -> list[float]:
        """
        Compute PMF using cosine similarity to anchor texts.

        Following the paper's methodology:
        1. Compute cosine similarity between response and each anchor
        2. Subtract minimum similarity to adjust for low variance
        3. Apply softmax with temperature to get PMF

        Args:
            response_embedding: Embedding vector of the response
            reference_set: List of 5 anchor statements

        Returns:
            PMF over Likert scale [p1, p2, p3, p4, p5]
        """
        # Get anchor embeddings (cached)
        cache_key = tuple(reference_set)
        if cache_key not in self._anchor_cache:
            self._anchor_cache[cache_key] = await self.llm_service.get_embeddings(
                reference_set
            )

        anchor_embeddings = self._anchor_cache[cache_key]

        # Compute cosine similarities
        similarities = [
            cosine_similarity(response_embedding, anchor_emb)
            for anchor_emb in anchor_embeddings
        ]

        # Following the paper: subtract minimum similarity to adjust for low variance
        # This ensures the resulting PMF has meaningful differences between options
        min_sim = min(similarities)
        adjusted_similarities = [s - min_sim for s in similarities]

        # Add small epsilon to the minimum position to avoid zero probability
        # This is the paper's approach with epsilon parameter
        epsilon = 0.01
        min_idx = similarities.index(min(similarities))
        adjusted_similarities[min_idx] = epsilon

        # Convert to PMF using softmax with temperature
        pmf = softmax(adjusted_similarities, temperature=self.temperature)

        return pmf

    def clear_cache(self):
        """Clear the anchor embedding cache."""
        self._anchor_cache.clear()

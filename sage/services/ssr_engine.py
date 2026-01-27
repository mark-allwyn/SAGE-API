"""
Semantic Similarity Rating (SSR) engine.

Implements the SSR methodology from the research paper:
"LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings"

The SSR method (Section A.4.3, equation 8):
1. Takes a free-text response from an LLM
2. Embeds the response and reference anchor statements
3. Computes cosine similarity to each anchor (representing Likert scale points 1-5)
4. Converts similarities to PMF via direct normalization (NOT softmax)
5. Averages across multiple reference sets for robustness

Key formula: p(r) ∝ γ(σ_r, t) - γ(σ_ℓ, t) + ε·δ_ℓ,r
Where γ = cosine similarity, ℓ = anchor with minimum similarity, ε = 0 (paper default)
"""

import numpy as np

from ..utils.embeddings import cosine_similarity
from .llm_service import LLMService


class SSREngine:
    """
    Semantic Similarity Rating engine.
    Maps free-text responses to Likert PMF using embeddings.
    """

    def __init__(self, llm_service: LLMService, temperature: float = 1.0):
        """
        Initialize SSR engine.

        Args:
            llm_service: LLM service for getting embeddings
            temperature: Temperature for PMF sharpening (paper equation 9).
                         p(r,T) ∝ p(r)^(1/T). Paper uses T=1 (no sharpening).
                         Lower T = sharper distribution.
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

        This implements the SSR algorithm (paper Section A.4.3):
        1. Get embedding for the response
        2. For each reference set:
           a. Get embeddings for the 5 anchor statements
           b. Compute cosine similarity between response and each anchor
           c. Convert to PMF via direct normalization (equation 8)
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
        Compute PMF using cosine similarity - following paper equation (8).

        Paper formula: p(r) ∝ γ(σ_r, t) - γ(σ_ℓ, t) + ε·δ_ℓ,r
        Where:
        - γ = cosine similarity
        - σ_r = reference statement for Likert rating r
        - t = textual response
        - ℓ = anchor with MINIMUM similarity
        - ε = epsilon (paper uses ε = 0)
        - δ_ℓ,r = Kronecker delta (1 when ℓ=r, 0 otherwise)

        Key insight: Probability is DIRECTLY PROPORTIONAL to adjusted similarity.
        NO softmax/exp() - just normalize directly!

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

        # Following paper equation (8): p(r) ∝ γ(σ_r, t) - γ(σ_ℓ, t) + ε·δ_ℓ,r
        # Where ℓ is the anchor with minimum similarity
        # Paper uses ε = 0, so we just subtract min and normalize
        min_sim = min(similarities)
        adjusted = [s - min_sim for s in similarities]

        # Add small epsilon to avoid division by zero if all similarities equal
        epsilon = 1e-10
        adjusted = [a + epsilon for a in adjusted]

        # Optional temperature: p(r,T) ∝ p(r)^(1/T)  [paper uses T=1]
        if self.temperature != 1.0:
            adjusted = [a ** (1.0 / self.temperature) for a in adjusted]

        # Normalize to get PMF (NO softmax/exp - just direct normalization)
        total = sum(adjusted)
        pmf = [a / total for a in adjusted]

        return pmf

    def clear_cache(self):
        """Clear the anchor embedding cache."""
        self._anchor_cache.clear()

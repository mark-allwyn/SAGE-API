"""Embedding utility functions for SSR."""

import numpy as np
from numpy.typing import NDArray


def cosine_similarity(a: list[float] | NDArray, b: list[float] | NDArray) -> float:
    """
    Compute cosine similarity between two vectors.

    Args:
        a: First vector
        b: Second vector

    Returns:
        Cosine similarity value between -1 and 1
    """
    a = np.array(a)
    b = np.array(b)
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot_product / (norm_a * norm_b))


def softmax(x: list[float] | NDArray, temperature: float = 1.0) -> list[float]:
    """
    Apply softmax with temperature scaling.

    Args:
        x: Input values
        temperature: Temperature parameter (lower = sharper distribution)

    Returns:
        Probability distribution summing to 1
    """
    x = np.array(x) / temperature
    # Subtract max for numerical stability
    exp_x = np.exp(x - np.max(x))
    return (exp_x / exp_x.sum()).tolist()

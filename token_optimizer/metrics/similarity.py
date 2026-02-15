"""Semantic similarity scoring between original and optimized prompts."""

from __future__ import annotations

import re
from collections import Counter


class SimilarityScorer:
    """Scores semantic similarity between original and optimized text.

    Uses a keyword-overlap heuristic by default. If sentence-transformers
    is installed, can optionally use embedding-based cosine similarity.
    """

    def __init__(self, use_embeddings: bool = False) -> None:
        self._use_embeddings = use_embeddings
        self._model = None
        if use_embeddings:
            self._load_embedding_model()

    def _load_embedding_model(self) -> None:
        """Load sentence-transformers model if available."""
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
        except ImportError:
            self._use_embeddings = False

    def score(self, original: str, optimized: str) -> float:
        """Compute similarity score between 0.0 and 1.0."""
        if not original or not optimized:
            return 1.0 if original == optimized else 0.0

        if original == optimized:
            return 1.0

        if self._use_embeddings and self._model is not None:
            return self._embedding_similarity(original, optimized)

        return self._keyword_similarity(original, optimized)

    def _keyword_similarity(self, original: str, optimized: str) -> float:
        """Compute similarity using keyword overlap (Jaccard + weighted)."""
        original_words = self._extract_keywords(original)
        optimized_words = self._extract_keywords(optimized)

        if not original_words and not optimized_words:
            return 1.0
        if not original_words or not optimized_words:
            return 0.0

        # Jaccard similarity on keyword sets
        orig_set = set(original_words)
        opt_set = set(optimized_words)
        intersection = orig_set & opt_set
        union = orig_set | opt_set
        jaccard = len(intersection) / len(union) if union else 1.0

        # Weighted overlap: what fraction of original keywords are preserved
        orig_counter = Counter(original_words)
        opt_counter = Counter(optimized_words)
        preserved = sum(
            min(orig_counter[w], opt_counter[w]) for w in intersection
        )
        total = sum(orig_counter.values())
        coverage = preserved / total if total else 1.0

        # Blend both signals
        return 0.4 * jaccard + 0.6 * coverage

    def _embedding_similarity(self, original: str, optimized: str) -> float:
        """Compute cosine similarity using sentence embeddings."""
        embeddings = self._model.encode([original, optimized])  # type: ignore[union-attr]
        dot = sum(a * b for a, b in zip(embeddings[0], embeddings[1]))
        norm_a = sum(a * a for a in embeddings[0]) ** 0.5
        norm_b = sum(b * b for b in embeddings[1]) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot / (norm_a * norm_b))

    @staticmethod
    def _extract_keywords(text: str) -> list[str]:
        """Extract meaningful keywords, filtering out stop words."""
        stop_words = {
            "a", "an", "the", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "shall", "can",
            "to", "of", "in", "for", "on", "with", "at", "by", "from",
            "as", "into", "through", "during", "before", "after", "and",
            "but", "or", "nor", "not", "so", "yet", "both", "either",
            "neither", "each", "every", "all", "any", "few", "more",
            "most", "some", "such", "no", "only", "own", "same", "than",
            "too", "very", "just", "because", "if", "when", "where",
            "how", "what", "which", "who", "whom", "this", "that",
            "these", "those", "i", "me", "my", "myself", "we", "our",
            "ours", "you", "your", "yours", "he", "him", "his", "she",
            "her", "hers", "it", "its", "they", "them", "their", "then",
            "there", "here", "up", "out", "about",
            # Common fillers that shouldn't affect similarity
            "please", "kindly", "basically", "actually", "really",
            "quite", "simply", "literally", "honestly", "frankly",
            "obviously", "clearly", "definitely", "certainly",
            "absolutely", "essentially", "hi", "hello", "hey",
            "also", "make", "sure", "want", "need", "like",
            "help", "note", "important",
        }
        words = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", text.lower())
        return [w for w in words if w not in stop_words and len(w) > 1]

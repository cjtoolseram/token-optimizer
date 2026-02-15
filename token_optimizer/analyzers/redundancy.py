"""Analyzer for detecting and removing redundant sentences and phrases."""

from __future__ import annotations

import re


class RedundancyAnalyzer:
    """Detects near-duplicate sentences and repeated phrases."""

    def __init__(self, similarity_threshold: float = 0.7) -> None:
        if not 0.0 < similarity_threshold <= 1.0:
            raise ValueError("similarity_threshold must be between 0 and 1")
        self.similarity_threshold = similarity_threshold

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Split text into lowercase words, stripping punctuation."""
        return re.findall(r"[a-zA-Z0-9]+", text.lower())

    @staticmethod
    def _jaccard_similarity(set_a: set[str], set_b: set[str]) -> float:
        """Compute Jaccard similarity between two word sets."""
        if not set_a and not set_b:
            return 1.0
        if not set_a or not set_b:
            return 0.0
        intersection = set_a & set_b
        union = set_a | set_b
        return len(intersection) / len(union)

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        """Split text into sentences on common delimiters."""
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]

    def _deduplicate_sentences(self, sentences: list[str]) -> list[str]:
        """Remove near-duplicate sentences, keeping the first (longer) one."""
        kept: list[str] = []
        kept_word_sets: list[set[str]] = []

        for sentence in sentences:
            word_set = set(self._tokenize(sentence))
            is_duplicate = False
            for i, existing_set in enumerate(kept_word_sets):
                similarity = self._jaccard_similarity(word_set, existing_set)
                if similarity > self.similarity_threshold:
                    # Keep the longer sentence.
                    if len(sentence) > len(kept[i]):
                        kept[i] = sentence
                        kept_word_sets[i] = word_set
                    is_duplicate = True
                    break
            if not is_duplicate:
                kept.append(sentence)
                kept_word_sets.append(word_set)

        return kept

    @staticmethod
    def _get_ngrams(words: list[str], n: int) -> list[tuple[str, ...]]:
        """Extract n-grams from a word list."""
        return [tuple(words[i : i + n]) for i in range(len(words) - n + 1)]

    def _deduplicate_phrases(self, text: str) -> str:
        """Find 3+ word n-grams that repeat and remove duplicate occurrences."""
        words = text.split()
        if len(words) < 6:
            return text

        # Check n-gram sizes from 3 up to half the text length.
        max_n = min(len(words) // 2, 10)
        for n in range(max_n, 2, -1):
            ngrams = self._get_ngrams(words, n)
            seen: dict[tuple[str, ...], int] = {}
            indices_to_remove: set[int] = set()

            for i, ngram in enumerate(ngrams):
                key = tuple(w.lower() for w in ngram)
                if key in seen:
                    # Mark duplicate occurrence indices for removal.
                    for j in range(n):
                        indices_to_remove.add(i + j)
                else:
                    seen[key] = i

            if indices_to_remove:
                words = [
                    w for idx, w in enumerate(words)
                    if idx not in indices_to_remove
                ]

        return " ".join(words)

    def analyze(
        self, text: str, preserve_keywords: list[str] | None = None
    ) -> str:
        """Remove redundant sentences and repeated phrases from text.

        Args:
            text: The input text to optimize.
            preserve_keywords: Words that should never be removed (reserved
                for future use in redundancy detection).

        Returns:
            The optimized text with redundancies removed.
        """
        if not text:
            return text

        # Split into paragraphs to preserve structure.
        paragraphs = text.split("\n")
        result_paragraphs: list[str] = []

        for paragraph in paragraphs:
            if not paragraph.strip():
                result_paragraphs.append(paragraph)
                continue

            # Deduplicate sentences within each paragraph.
            sentences = self._split_sentences(paragraph)
            if len(sentences) > 1:
                sentences = self._deduplicate_sentences(sentences)
            paragraph = " ".join(sentences)

            # Deduplicate repeated phrases.
            paragraph = self._deduplicate_phrases(paragraph)

            result_paragraphs.append(paragraph)

        result = "\n".join(result_paragraphs)

        # Clean up extra whitespace.
        result = re.sub(r"  +", " ", result)
        return result.strip()

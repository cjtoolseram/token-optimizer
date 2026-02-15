"""Gemini tokenizer using a character-based heuristic."""

from __future__ import annotations

from token_optimizer.tokenizers.base import BaseTokenizer


class GeminiTokenizer(BaseTokenizer):
    """Approximate tokenizer for Google Gemini models.

    Since Google does not provide a standalone tokenizer library for Gemini,
    this uses a character-based heuristic: tokens ~ len(text) / 4.0.  This
    ratio is an empirical approximation and may not match the actual token
    count exactly.
    """

    @property
    def name(self) -> str:
        return "gemini"

    def count_tokens(self, text: str) -> int:
        """Estimate token count using characters / 4.0 heuristic."""
        return round(len(text) / 4.0)

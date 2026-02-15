"""Anthropic tokenizer using a character-based heuristic."""

from __future__ import annotations

from token_optimizer.tokenizers.base import BaseTokenizer


class AnthropicTokenizer(BaseTokenizer):
    """Approximate tokenizer for Anthropic Claude models.

    Since Anthropic does not provide a public tokenizer library, this uses a
    character-based heuristic: tokens ~ len(text) / 3.5.  This ratio is an
    empirical approximation and may not match the actual token count exactly.
    """

    @property
    def name(self) -> str:
        return "anthropic"

    def count_tokens(self, text: str) -> int:
        """Estimate token count using characters / 3.5 heuristic."""
        return round(len(text) / 3.5)

"""Generic tokenizer using a word-count heuristic."""

from __future__ import annotations

from token_optimizer.tokenizers.base import BaseTokenizer


class GenericTokenizer(BaseTokenizer):
    """Fallback tokenizer that estimates tokens from word count.

    Uses the heuristic: tokens ~ words * 1.3, which gives a reasonable
    approximation when no provider-specific tokenizer is available.
    """

    @property
    def name(self) -> str:
        return "generic"

    def count_tokens(self, text: str) -> int:
        """Estimate token count as words multiplied by 1.3."""
        return round(len(text.split()) * 1.3)

"""Token counting and cost savings calculator."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from token_optimizer.tokenizers.base import BaseTokenizer
    from token_optimizer.providers.registry import ModelInfo


class TokenCalculator:
    """Calculates token counts and cost savings."""

    def __init__(self, tokenizer: BaseTokenizer, model_info: ModelInfo) -> None:
        self._tokenizer = tokenizer
        self._model_info = model_info

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in text."""
        if not text:
            return 0
        return self._tokenizer.count_tokens(text)

    def calculate_cost(self, token_count: int, is_input: bool = True) -> float:
        """Calculate the cost for a given number of tokens."""
        rate = (
            self._model_info.cost_per_1k_input
            if is_input
            else self._model_info.cost_per_1k_output
        )
        return (token_count / 1000) * rate

    def calculate_savings(
        self, original_tokens: int, optimized_tokens: int
    ) -> tuple[float, float]:
        """Calculate savings percentage and estimated cost savings.

        Returns:
            (savings_percent, cost_savings_usd)
        """
        if original_tokens == 0:
            return 0.0, 0.0

        tokens_saved = original_tokens - optimized_tokens
        savings_percent = (tokens_saved / original_tokens) * 100

        cost_original = self.calculate_cost(original_tokens)
        cost_optimized = self.calculate_cost(optimized_tokens)
        cost_savings = cost_original - cost_optimized

        return savings_percent, cost_savings

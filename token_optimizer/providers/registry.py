"""Provider registry mapping model names to tokenizers and pricing."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from token_optimizer.tokenizers.base import BaseTokenizer


@dataclass
class ModelInfo:
    """Pricing and tokenizer info for a model."""

    provider: str
    tokenizer_type: str
    cost_per_1k_input: float
    cost_per_1k_output: float


# Pattern → ModelInfo mappings, checked in order
_MODEL_PATTERNS: list[tuple[str, ModelInfo]] = [
    # OpenAI
    (r"gpt-4o-mini", ModelInfo("openai", "openai", 0.00015, 0.0006)),
    (r"gpt-4o", ModelInfo("openai", "openai", 0.0025, 0.01)),
    (r"gpt-4-turbo", ModelInfo("openai", "openai", 0.01, 0.03)),
    (r"gpt-4", ModelInfo("openai", "openai", 0.03, 0.06)),
    (r"gpt-3\.5-turbo", ModelInfo("openai", "openai", 0.0005, 0.0015)),
    (r"o1-mini", ModelInfo("openai", "openai", 0.003, 0.012)),
    (r"o1-pro", ModelInfo("openai", "openai", 0.15, 0.60)),
    (r"o1", ModelInfo("openai", "openai", 0.015, 0.06)),
    (r"o3-mini", ModelInfo("openai", "openai", 0.0011, 0.0044)),
    (r"o3", ModelInfo("openai", "openai", 0.01, 0.04)),
    # Anthropic
    (r"claude-opus-4", ModelInfo("anthropic", "anthropic", 0.015, 0.075)),
    (r"claude-sonnet-4", ModelInfo("anthropic", "anthropic", 0.003, 0.015)),
    (r"claude-haiku-4", ModelInfo("anthropic", "anthropic", 0.0008, 0.004)),
    (r"claude-3-5-sonnet", ModelInfo("anthropic", "anthropic", 0.003, 0.015)),
    (r"claude-3-5-haiku", ModelInfo("anthropic", "anthropic", 0.0008, 0.004)),
    (r"claude-3-opus", ModelInfo("anthropic", "anthropic", 0.015, 0.075)),
    (r"claude-3-sonnet", ModelInfo("anthropic", "anthropic", 0.003, 0.015)),
    (r"claude-3-haiku", ModelInfo("anthropic", "anthropic", 0.00025, 0.00125)),
    (r"claude", ModelInfo("anthropic", "anthropic", 0.003, 0.015)),
    # Google Gemini
    (r"gemini-2\.0-flash", ModelInfo("google", "gemini", 0.0001, 0.0004)),
    (r"gemini-1\.5-pro", ModelInfo("google", "gemini", 0.00125, 0.005)),
    (r"gemini-1\.5-flash", ModelInfo("google", "gemini", 0.000075, 0.0003)),
    (r"gemini-pro", ModelInfo("google", "gemini", 0.0005, 0.0015)),
    (r"gemini", ModelInfo("google", "gemini", 0.0001, 0.0004)),
    # Mistral
    (r"mistral-large", ModelInfo("mistral", "generic", 0.003, 0.009)),
    (r"mistral-medium", ModelInfo("mistral", "generic", 0.0027, 0.0081)),
    (r"mistral-small", ModelInfo("mistral", "generic", 0.001, 0.003)),
    (r"mistral", ModelInfo("mistral", "generic", 0.001, 0.003)),
    # Cohere
    (r"command-r-plus", ModelInfo("cohere", "generic", 0.003, 0.015)),
    (r"command-r", ModelInfo("cohere", "generic", 0.0005, 0.0015)),
    (r"command", ModelInfo("cohere", "generic", 0.001, 0.002)),
]


class ProviderRegistry:
    """Maps model names to tokenizers and pricing information."""

    def __init__(self) -> None:
        self._custom_models: dict[str, ModelInfo] = {}

    def register_model(
        self,
        model: str,
        provider: str = "custom",
        tokenizer_type: str = "generic",
        cost_per_1k_input: float = 0.0,
        cost_per_1k_output: float = 0.0,
    ) -> None:
        """Register a custom model with pricing info."""
        self._custom_models[model] = ModelInfo(
            provider=provider,
            tokenizer_type=tokenizer_type,
            cost_per_1k_input=cost_per_1k_input,
            cost_per_1k_output=cost_per_1k_output,
        )

    def lookup(self, model: str) -> ModelInfo:
        """Look up model info by name. Falls back to generic if unknown."""
        if model in self._custom_models:
            return self._custom_models[model]

        for pattern, info in _MODEL_PATTERNS:
            if re.search(pattern, model, re.IGNORECASE):
                return info

        return ModelInfo(
            provider="unknown",
            tokenizer_type="generic",
            cost_per_1k_input=0.0,
            cost_per_1k_output=0.0,
        )

    def get_tokenizer(self, model: str) -> BaseTokenizer:
        """Get the appropriate tokenizer for a model."""
        info = self.lookup(model)
        return self._create_tokenizer(info.tokenizer_type, model)

    def _create_tokenizer(self, tokenizer_type: str, model: str) -> BaseTokenizer:
        """Create a tokenizer instance by type."""
        if tokenizer_type == "openai":
            try:
                from token_optimizer.tokenizers.openai_tokenizer import OpenAITokenizer
                return OpenAITokenizer(model=model)
            except ImportError:
                from token_optimizer.tokenizers.generic import GenericTokenizer
                return GenericTokenizer()

        if tokenizer_type == "anthropic":
            from token_optimizer.tokenizers.anthropic_tokenizer import AnthropicTokenizer
            return AnthropicTokenizer()

        if tokenizer_type == "gemini":
            from token_optimizer.tokenizers.gemini_tokenizer import GeminiTokenizer
            return GeminiTokenizer()

        from token_optimizer.tokenizers.generic import GenericTokenizer
        return GenericTokenizer()

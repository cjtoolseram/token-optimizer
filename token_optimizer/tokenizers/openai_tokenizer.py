"""OpenAI tokenizer using tiktoken."""

from __future__ import annotations

from token_optimizer.tokenizers.base import BaseTokenizer


class OpenAITokenizer(BaseTokenizer):
    """Tokenizer that uses tiktoken for accurate OpenAI token counting."""

    def __init__(self, model: str = "gpt-4o") -> None:
        try:
            import tiktoken
        except ImportError:
            raise ImportError(
                "tiktoken is required for OpenAI token counting. "
                "Install it with: pip install token-optimizer[openai]"
            )
        self._encoding = tiktoken.encoding_for_model(model)

    @property
    def name(self) -> str:
        return "openai"

    def count_tokens(self, text: str) -> int:
        """Count tokens using tiktoken's encoding."""
        return len(self._encoding.encode(text))

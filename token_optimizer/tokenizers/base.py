"""Base class for tokenizers."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseTokenizer(ABC):
    """Abstract base class for provider-specific tokenizers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the tokenizer name."""

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in the given text.

        Args:
            text: The input text to tokenize.

        Returns:
            The token count.
        """

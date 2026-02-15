"""Base class for optimization strategies."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """Abstract base class for optimization strategies.

    Strategies orchestrate which analyzers to run and at what aggressiveness
    level.  Each concrete strategy defines an ordered pipeline of analyzers
    and invokes them sequentially on the input text.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the strategy name."""

    @abstractmethod
    def optimize(
        self, text: str, preserve_keywords: list[str] | None = None
    ) -> str:
        """Optimize the given text by running the configured analyzers.

        Args:
            text: The input text to optimize.
            preserve_keywords: Words that should never be removed.

        Returns:
            The optimized text.
        """

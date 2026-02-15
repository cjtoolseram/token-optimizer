"""Custom optimization strategy — user-defined analyzer pipeline."""

from __future__ import annotations

from typing import Any

from token_optimizer.strategies.base import BaseStrategy


class CustomStrategy(BaseStrategy):
    """Strategy that runs a user-supplied list of analyzer instances.

    The analyzers are executed in the order they are provided.
    """

    def __init__(self, analyzers: list[Any], name: str = "custom") -> None:
        self._analyzers = analyzers
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def optimize(
        self, text: str, preserve_keywords: list[str] | None = None
    ) -> str:
        """Optimize text by running each analyzer in the given order."""
        result = text
        for analyzer in self._analyzers:
            result = analyzer.analyze(result, preserve_keywords=preserve_keywords)
        return result

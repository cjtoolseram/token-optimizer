"""Aggressive optimization strategy — maximum token savings."""

from __future__ import annotations

from token_optimizer.analyzers.filler import FillerAnalyzer
from token_optimizer.analyzers.redundancy import RedundancyAnalyzer
from token_optimizer.analyzers.structural import StructuralAnalyzer
from token_optimizer.analyzers.verbosity import VerbosityAnalyzer
from token_optimizer.strategies.base import BaseStrategy


class AggressiveStrategy(BaseStrategy):
    """High-aggressiveness strategy using all analyzers at maximum level.

    Runs analyzers in order: structural -> filler -> verbosity -> redundancy.
    """

    @property
    def name(self) -> str:
        return "aggressive"

    def optimize(
        self, text: str, preserve_keywords: list[str] | None = None
    ) -> str:
        """Optimize text with maximum aggressiveness."""
        analyzers = [
            StructuralAnalyzer(aggressiveness=3),
            FillerAnalyzer(aggressiveness=3),
            VerbosityAnalyzer(aggressiveness=3),
            RedundancyAnalyzer(),
        ]

        result = text
        for analyzer in analyzers:
            result = analyzer.analyze(result, preserve_keywords=preserve_keywords)
        return result

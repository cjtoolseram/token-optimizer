"""Moderate optimization strategy — balanced trade-off."""

from __future__ import annotations

from token_optimizer.analyzers.filler import FillerAnalyzer
from token_optimizer.analyzers.redundancy import RedundancyAnalyzer
from token_optimizer.analyzers.structural import StructuralAnalyzer
from token_optimizer.analyzers.verbosity import VerbosityAnalyzer
from token_optimizer.strategies.base import BaseStrategy


class ModerateStrategy(BaseStrategy):
    """Mid-aggressiveness strategy using all four analyzers.

    Runs analyzers in order: structural -> filler -> verbosity -> redundancy.
    """

    @property
    def name(self) -> str:
        return "moderate"

    def optimize(
        self, text: str, preserve_keywords: list[str] | None = None
    ) -> str:
        """Optimize text with moderate aggressiveness."""
        analyzers = [
            StructuralAnalyzer(aggressiveness=2),
            FillerAnalyzer(aggressiveness=2),
            VerbosityAnalyzer(aggressiveness=2),
            RedundancyAnalyzer(),
        ]

        result = text
        for analyzer in analyzers:
            result = analyzer.analyze(result, preserve_keywords=preserve_keywords)
        return result

"""Conservative optimization strategy — minimal changes, high safety."""

from __future__ import annotations

from token_optimizer.analyzers.filler import FillerAnalyzer
from token_optimizer.analyzers.redundancy import RedundancyAnalyzer
from token_optimizer.analyzers.structural import StructuralAnalyzer
from token_optimizer.strategies.base import BaseStrategy


class ConservativeStrategy(BaseStrategy):
    """Low-aggressiveness strategy that avoids verbosity changes.

    Runs analyzers in order: structural -> filler -> redundancy.
    Does NOT use VerbosityAnalyzer.
    """

    @property
    def name(self) -> str:
        return "conservative"

    def optimize(
        self, text: str, preserve_keywords: list[str] | None = None
    ) -> str:
        """Optimize text conservatively."""
        analyzers = [
            StructuralAnalyzer(aggressiveness=1),
            FillerAnalyzer(aggressiveness=1),
            RedundancyAnalyzer(),
        ]

        result = text
        for analyzer in analyzers:
            result = analyzer.analyze(result, preserve_keywords=preserve_keywords)
        return result

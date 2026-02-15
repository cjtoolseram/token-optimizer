"""Analyzers for detecting and removing different types of token waste."""

from token_optimizer.analyzers.filler import FillerAnalyzer
from token_optimizer.analyzers.redundancy import RedundancyAnalyzer
from token_optimizer.analyzers.verbosity import VerbosityAnalyzer
from token_optimizer.analyzers.structural import StructuralAnalyzer

__all__ = [
    "FillerAnalyzer",
    "RedundancyAnalyzer",
    "VerbosityAnalyzer",
    "StructuralAnalyzer",
]

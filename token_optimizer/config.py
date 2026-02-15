"""Configuration and result dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

StrategyName = Literal["conservative", "moderate", "aggressive", "custom"]


@dataclass
class OptimizerConfig:
    """Configuration for the token optimizer."""

    model: str = "gpt-4o"
    strategy: StrategyName = "moderate"
    cost_per_1k_input: float | None = None
    cost_per_1k_output: float | None = None
    preserve_keywords: list[str] = field(default_factory=list)
    similarity_threshold: float = 0.4
    cache_enabled: bool = True
    cache_maxsize: int = 1024


@dataclass
class OptimizationResult:
    """Result of a prompt optimization."""

    original_text: str
    optimized_text: str
    original_tokens: int
    optimized_tokens: int
    savings_percent: float
    estimated_cost_savings: float
    similarity_score: float
    strategy_used: str
    from_cache: bool = False

    @property
    def tokens_saved(self) -> int:
        return self.original_tokens - self.optimized_tokens

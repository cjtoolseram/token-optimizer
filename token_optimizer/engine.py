"""Core optimization engine — the main entry point."""

from __future__ import annotations

from token_optimizer.config import OptimizerConfig, OptimizationResult, StrategyName
from token_optimizer.providers.registry import ProviderRegistry
from token_optimizer.metrics.calculator import TokenCalculator
from token_optimizer.metrics.similarity import SimilarityScorer
from token_optimizer.cache.prompt_cache import PromptCache
from token_optimizer.strategies.base import BaseStrategy


class TokenOptimizer:
    """Main optimizer that orchestrates prompt compression.

    Usage:
        optimizer = TokenOptimizer(model="gpt-4o", strategy="moderate")
        result = optimizer.optimize("Your verbose prompt here...")
        print(result.optimized_text)
        print(f"Saved {result.savings_percent:.1f}% tokens")
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        strategy: StrategyName = "moderate",
        cost_per_1k_input: float | None = None,
        cost_per_1k_output: float | None = None,
        preserve_keywords: list[str] | None = None,
        similarity_threshold: float = 0.4,
        cache_enabled: bool = True,
        cache_maxsize: int = 1024,
    ) -> None:
        self.config = OptimizerConfig(
            model=model,
            strategy=strategy,
            cost_per_1k_input=cost_per_1k_input,
            cost_per_1k_output=cost_per_1k_output,
            preserve_keywords=preserve_keywords or [],
            similarity_threshold=similarity_threshold,
            cache_enabled=cache_enabled,
            cache_maxsize=cache_maxsize,
        )

        self._registry = ProviderRegistry()
        self._model_info = self._registry.lookup(model)

        # Override pricing if provided
        if cost_per_1k_input is not None:
            self._model_info.cost_per_1k_input = cost_per_1k_input
        if cost_per_1k_output is not None:
            self._model_info.cost_per_1k_output = cost_per_1k_output

        self._tokenizer = self._registry.get_tokenizer(model)
        self._calculator = TokenCalculator(self._tokenizer, self._model_info)
        self._similarity = SimilarityScorer()
        self._cache = PromptCache(maxsize=cache_maxsize) if cache_enabled else None
        self._strategy = self._build_strategy(strategy)

    def _build_strategy(self, strategy: StrategyName) -> BaseStrategy:
        """Create the appropriate strategy instance."""
        if strategy == "conservative":
            from token_optimizer.strategies.conservative import ConservativeStrategy
            return ConservativeStrategy()
        elif strategy == "aggressive":
            from token_optimizer.strategies.aggressive import AggressiveStrategy
            return AggressiveStrategy()
        elif strategy == "moderate":
            from token_optimizer.strategies.moderate import ModerateStrategy
            return ModerateStrategy()
        elif strategy == "custom":
            from token_optimizer.strategies.custom import CustomStrategy
            return CustomStrategy(analyzers=[])
        else:
            from token_optimizer.strategies.moderate import ModerateStrategy
            return ModerateStrategy()

    def optimize(
        self,
        prompt: str,
        system_prompt: str | None = None,
        preserve_keywords: list[str] | None = None,
    ) -> OptimizationResult:
        """Optimize a prompt to reduce token count.

        Args:
            prompt: The user prompt to optimize.
            system_prompt: Optional system prompt to also optimize.
            preserve_keywords: Additional keywords to preserve (merged with config).

        Returns:
            OptimizationResult with original/optimized text and metrics.
        """
        keywords = list(self.config.preserve_keywords)
        if preserve_keywords:
            keywords.extend(preserve_keywords)

        # Combine system + user prompt for optimization if both provided
        full_text = prompt
        if system_prompt:
            full_text = f"{system_prompt}\n\n{prompt}"

        # Check cache
        strategy_name = self._strategy.name
        if self._cache is not None:
            cached = self._cache.get(full_text, strategy_name)
            if cached is not None:
                original_tokens = self._calculator.count_tokens(full_text)
                optimized_tokens = self._calculator.count_tokens(cached)
                savings_pct, cost_savings = self._calculator.calculate_savings(
                    original_tokens, optimized_tokens
                )
                return OptimizationResult(
                    original_text=full_text,
                    optimized_text=cached,
                    original_tokens=original_tokens,
                    optimized_tokens=optimized_tokens,
                    savings_percent=savings_pct,
                    estimated_cost_savings=cost_savings,
                    similarity_score=1.0,
                    strategy_used=strategy_name,
                    from_cache=True,
                )

        # Run optimization
        optimized = self._strategy.optimize(full_text, preserve_keywords=keywords)

        # Compute similarity
        similarity = self._similarity.score(full_text, optimized)

        # If similarity is too low, fall back to conservative
        if similarity < self.config.similarity_threshold and strategy_name != "conservative":
            from token_optimizer.strategies.conservative import ConservativeStrategy
            fallback = ConservativeStrategy()
            optimized = fallback.optimize(full_text, preserve_keywords=keywords)
            similarity = self._similarity.score(full_text, optimized)
            strategy_name = f"{self._strategy.name}->conservative"

        # Calculate metrics
        original_tokens = self._calculator.count_tokens(full_text)
        optimized_tokens = self._calculator.count_tokens(optimized)
        savings_pct, cost_savings = self._calculator.calculate_savings(
            original_tokens, optimized_tokens
        )

        # Cache result
        if self._cache is not None:
            self._cache.put(full_text, self._strategy.name, optimized)

        return OptimizationResult(
            original_text=full_text,
            optimized_text=optimized,
            original_tokens=original_tokens,
            optimized_tokens=optimized_tokens,
            savings_percent=savings_pct,
            estimated_cost_savings=cost_savings,
            similarity_score=similarity,
            strategy_used=strategy_name,
        )

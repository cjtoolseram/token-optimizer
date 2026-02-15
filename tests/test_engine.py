"""Tests for the core TokenOptimizer engine."""

from token_optimizer import TokenOptimizer, OptimizationResult


class TestTokenOptimizer:
    def test_basic_optimization(self):
        optimizer = TokenOptimizer(model="gpt-4o", strategy="moderate")
        result = optimizer.optimize(
            "I would like you to please help me write a Python function "
            "that takes a list of numbers as input and then returns the sum "
            "of all the numbers in that list."
        )
        assert isinstance(result, OptimizationResult)
        assert result.optimized_tokens <= result.original_tokens
        assert result.savings_percent >= 0
        assert 0 <= result.similarity_score <= 1

    def test_conservative_strategy(self):
        optimizer = TokenOptimizer(model="gpt-4o", strategy="conservative")
        text = "Please just basically write a simple function."
        result = optimizer.optimize(text)
        assert result.strategy_used == "conservative"
        assert result.optimized_tokens <= result.original_tokens

    def test_aggressive_strategy(self):
        optimizer = TokenOptimizer(model="gpt-4o", strategy="aggressive")
        text = (
            "I would like you to please write a function. "
            "Could you please make sure it handles errors? "
            "I want you to also add very good documentation."
        )
        result = optimizer.optimize(text)
        assert result.optimized_tokens < result.original_tokens

    def test_preserve_keywords(self):
        optimizer = TokenOptimizer(model="gpt-4o", strategy="aggressive")
        result = optimizer.optimize(
            "Please just create the API endpoint",
            preserve_keywords=["API"],
        )
        assert "API" in result.optimized_text

    def test_system_prompt_optimization(self):
        optimizer = TokenOptimizer(model="gpt-4o", strategy="moderate")
        result = optimizer.optimize(
            "Write code",
            system_prompt="You are a very helpful and kind assistant that always tries to help.",
        )
        assert result.original_text.startswith("You are")
        assert result.optimized_tokens <= result.original_tokens

    def test_caching(self):
        optimizer = TokenOptimizer(model="gpt-4o", strategy="moderate", cache_enabled=True)
        text = "I would like you to write a function please."

        result1 = optimizer.optimize(text)
        assert not result1.from_cache

        result2 = optimizer.optimize(text)
        assert result2.from_cache
        assert result2.optimized_text == result1.optimized_text

    def test_cache_disabled(self):
        optimizer = TokenOptimizer(model="gpt-4o", strategy="moderate", cache_enabled=False)
        text = "Please write a function."

        result1 = optimizer.optimize(text)
        result2 = optimizer.optimize(text)
        assert not result1.from_cache
        assert not result2.from_cache

    def test_empty_prompt(self):
        optimizer = TokenOptimizer(model="gpt-4o", strategy="moderate")
        result = optimizer.optimize("")
        assert result.optimized_text == ""
        assert result.savings_percent == 0.0

    def test_anthropic_model(self):
        optimizer = TokenOptimizer(model="claude-sonnet-4-5-20250929", strategy="moderate")
        result = optimizer.optimize("I would like you to please help me.")
        assert isinstance(result, OptimizationResult)
        assert result.optimized_tokens <= result.original_tokens

    def test_gemini_model(self):
        optimizer = TokenOptimizer(model="gemini-2.0-flash", strategy="moderate")
        result = optimizer.optimize("I would like you to please help me.")
        assert isinstance(result, OptimizationResult)

    def test_unknown_model_uses_generic(self):
        optimizer = TokenOptimizer(model="some-unknown-model", strategy="conservative")
        result = optimizer.optimize("Please write some code.")
        assert isinstance(result, OptimizationResult)

    def test_custom_pricing(self):
        optimizer = TokenOptimizer(
            model="custom-model",
            strategy="moderate",
            cost_per_1k_input=0.01,
            cost_per_1k_output=0.03,
        )
        result = optimizer.optimize("I would like you to please write a function.")
        assert result.estimated_cost_savings >= 0

    def test_tokens_saved_property(self):
        optimizer = TokenOptimizer(model="gpt-4o", strategy="moderate")
        result = optimizer.optimize("I would like you to please help me write code.")
        assert result.tokens_saved == result.original_tokens - result.optimized_tokens

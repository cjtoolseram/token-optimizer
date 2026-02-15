"""Tests for metrics modules."""

from token_optimizer.metrics.calculator import TokenCalculator
from token_optimizer.metrics.similarity import SimilarityScorer
from token_optimizer.tokenizers.generic import GenericTokenizer
from token_optimizer.providers.registry import ModelInfo, ProviderRegistry
from token_optimizer.cache.prompt_cache import PromptCache


# ── Token Calculator ─────────────────────────────────────────────────────


class TestTokenCalculator:
    def _make_calculator(self, cost_input=0.01, cost_output=0.03):
        tokenizer = GenericTokenizer()
        model_info = ModelInfo(
            provider="test",
            tokenizer_type="generic",
            cost_per_1k_input=cost_input,
            cost_per_1k_output=cost_output,
        )
        return TokenCalculator(tokenizer, model_info)

    def test_count_tokens(self):
        calc = self._make_calculator()
        count = calc.count_tokens("hello world foo bar")
        assert count > 0

    def test_empty_text(self):
        calc = self._make_calculator()
        assert calc.count_tokens("") == 0

    def test_calculate_cost(self):
        calc = self._make_calculator(cost_input=0.01)
        cost = calc.calculate_cost(1000, is_input=True)
        assert cost == pytest.approx(0.01)

    def test_calculate_savings(self):
        calc = self._make_calculator()
        pct, savings = calc.calculate_savings(100, 70)
        assert pct == pytest.approx(30.0)
        assert savings > 0

    def test_zero_original_tokens(self):
        calc = self._make_calculator()
        pct, savings = calc.calculate_savings(0, 0)
        assert pct == 0.0
        assert savings == 0.0


# ── Similarity Scorer ────────────────────────────────────────────────────


class TestSimilarityScorer:
    def test_identical_texts(self):
        scorer = SimilarityScorer()
        assert scorer.score("hello world", "hello world") == 1.0

    def test_empty_texts(self):
        scorer = SimilarityScorer()
        assert scorer.score("", "") == 1.0

    def test_one_empty(self):
        scorer = SimilarityScorer()
        assert scorer.score("hello", "") == 0.0

    def test_similar_texts(self):
        scorer = SimilarityScorer()
        score = scorer.score(
            "Write a Python function that returns the sum of a list",
            "Write Python function returns sum list",
        )
        assert score > 0.5

    def test_different_texts(self):
        scorer = SimilarityScorer()
        score = scorer.score(
            "Write a Python function",
            "Deploy Kubernetes cluster on AWS",
        )
        assert score < 0.5


# ── Provider Registry ────────────────────────────────────────────────────


class TestProviderRegistry:
    def test_lookup_openai(self):
        registry = ProviderRegistry()
        info = registry.lookup("gpt-4o")
        assert info.provider == "openai"
        assert info.cost_per_1k_input > 0

    def test_lookup_anthropic(self):
        registry = ProviderRegistry()
        info = registry.lookup("claude-sonnet-4-5-20250929")
        assert info.provider == "anthropic"

    def test_lookup_gemini(self):
        registry = ProviderRegistry()
        info = registry.lookup("gemini-2.0-flash")
        assert info.provider == "google"

    def test_lookup_unknown(self):
        registry = ProviderRegistry()
        info = registry.lookup("totally-unknown-model")
        assert info.provider == "unknown"
        assert info.tokenizer_type == "generic"

    def test_register_custom_model(self):
        registry = ProviderRegistry()
        registry.register_model(
            "my-model",
            provider="custom",
            cost_per_1k_input=0.005,
            cost_per_1k_output=0.015,
        )
        info = registry.lookup("my-model")
        assert info.provider == "custom"
        assert info.cost_per_1k_input == 0.005

    def test_get_tokenizer_generic(self):
        registry = ProviderRegistry()
        tokenizer = registry.get_tokenizer("unknown-model")
        assert tokenizer.name == "generic"

    def test_get_tokenizer_anthropic(self):
        registry = ProviderRegistry()
        tokenizer = registry.get_tokenizer("claude-sonnet-4-5-20250929")
        assert tokenizer.name == "anthropic"

    def test_get_tokenizer_gemini(self):
        registry = ProviderRegistry()
        tokenizer = registry.get_tokenizer("gemini-2.0-flash")
        assert tokenizer.name == "gemini"


# ── Prompt Cache ─────────────────────────────────────────────────────────


class TestPromptCache:
    def test_put_and_get(self):
        cache = PromptCache(maxsize=10)
        cache.put("hello", "moderate", "optimized hello")
        result = cache.get("hello", "moderate")
        assert result == "optimized hello"

    def test_cache_miss(self):
        cache = PromptCache(maxsize=10)
        assert cache.get("nonexistent", "moderate") is None

    def test_different_strategies(self):
        cache = PromptCache(maxsize=10)
        cache.put("hello", "moderate", "mod result")
        cache.put("hello", "aggressive", "agg result")
        assert cache.get("hello", "moderate") == "mod result"
        assert cache.get("hello", "aggressive") == "agg result"

    def test_lru_eviction(self):
        cache = PromptCache(maxsize=2)
        cache.put("a", "s", "1")
        cache.put("b", "s", "2")
        cache.put("c", "s", "3")  # should evict "a"
        assert cache.get("a", "s") is None
        assert cache.get("b", "s") == "2"
        assert cache.get("c", "s") == "3"

    def test_clear(self):
        cache = PromptCache(maxsize=10)
        cache.put("a", "s", "1")
        cache.clear()
        assert cache.size == 0
        assert cache.get("a", "s") is None

    def test_size(self):
        cache = PromptCache(maxsize=10)
        assert cache.size == 0
        cache.put("a", "s", "1")
        assert cache.size == 1


import pytest

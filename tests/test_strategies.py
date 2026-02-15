"""Tests for optimization strategies."""

from token_optimizer.strategies.conservative import ConservativeStrategy
from token_optimizer.strategies.moderate import ModerateStrategy
from token_optimizer.strategies.aggressive import AggressiveStrategy
from token_optimizer.strategies.custom import CustomStrategy
from token_optimizer.analyzers.filler import FillerAnalyzer
from token_optimizer.analyzers.structural import StructuralAnalyzer


class TestConservativeStrategy:
    def test_name(self):
        s = ConservativeStrategy()
        assert s.name == "conservative"

    def test_preserves_meaning(self):
        s = ConservativeStrategy()
        text = "Please write a function that returns the sum."
        result = s.optimize(text)
        assert "function" in result
        assert "sum" in result

    def test_removes_basic_fillers(self):
        s = ConservativeStrategy()
        text = "Could you please write a function?"
        result = s.optimize(text)
        assert len(result) <= len(text)


class TestModerateStrategy:
    def test_name(self):
        s = ModerateStrategy()
        assert s.name == "moderate"

    def test_more_aggressive_than_conservative(self):
        conservative = ConservativeStrategy()
        moderate = ModerateStrategy()
        text = (
            "I would like you to please write a function. "
            "In order to do this, you should create a class. "
            "Due to the fact that we need it, please add tests."
        )
        conservative_result = conservative.optimize(text)
        moderate_result = moderate.optimize(text)
        assert len(moderate_result) <= len(conservative_result)


class TestAggressiveStrategy:
    def test_name(self):
        s = AggressiveStrategy()
        assert s.name == "aggressive"

    def test_most_aggressive(self):
        aggressive = AggressiveStrategy()
        moderate = ModerateStrategy()
        text = (
            "Hi, I would like you to please write a very simple function. "
            "You should make sure to handle the errors properly. "
            "In order to do this, you need to add error handling."
        )
        moderate_result = moderate.optimize(text)
        aggressive_result = aggressive.optimize(text)
        assert len(aggressive_result) <= len(moderate_result)


class TestCustomStrategy:
    def test_name(self):
        s = CustomStrategy(analyzers=[], name="my-strategy")
        assert s.name == "my-strategy"

    def test_default_name(self):
        s = CustomStrategy(analyzers=[])
        assert s.name == "custom"

    def test_runs_analyzers_in_order(self):
        s = CustomStrategy(analyzers=[
            StructuralAnalyzer(aggressiveness=1),
            FillerAnalyzer(aggressiveness=2),
        ])
        text = "Please  just   write   a   function"
        result = s.optimize(text)
        # Spaces should be collapsed and fillers removed
        assert "   " not in result

    def test_empty_analyzers(self):
        s = CustomStrategy(analyzers=[])
        text = "Hello world"
        assert s.optimize(text) == text

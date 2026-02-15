"""Tests for all analyzer modules."""

import pytest

from token_optimizer.analyzers.filler import FillerAnalyzer
from token_optimizer.analyzers.redundancy import RedundancyAnalyzer
from token_optimizer.analyzers.verbosity import VerbosityAnalyzer
from token_optimizer.analyzers.structural import StructuralAnalyzer


# ── Filler Analyzer ──────────────────────────────────────────────────────


class TestFillerAnalyzer:
    def test_removes_filler_phrases(self):
        analyzer = FillerAnalyzer(aggressiveness=1)
        text = "I would like you to write a function"
        result = analyzer.analyze(text)
        assert "I would like you to" not in result
        assert "write" in result
        assert "function" in result

    def test_removes_filler_words_at_level_2(self):
        analyzer = FillerAnalyzer(aggressiveness=2)
        text = "Please just basically write a very simple function"
        result = analyzer.analyze(text)
        assert "just" not in result.split()
        assert "basically" not in result.split()
        assert "very" not in result.split()

    def test_level_1_does_not_remove_filler_words(self):
        analyzer = FillerAnalyzer(aggressiveness=1)
        text = "just basically write a function"
        result = analyzer.analyze(text)
        assert "just" in result
        assert "basically" in result

    def test_level_3_strips_polite_openers(self):
        analyzer = FillerAnalyzer(aggressiveness=3)
        text = "Hi, can you write a function?"
        result = analyzer.analyze(text)
        assert not result.lower().startswith("hi,")

    def test_preserves_keywords(self):
        analyzer = FillerAnalyzer(aggressiveness=2)
        text = "Please just return the result"
        result = analyzer.analyze(text, preserve_keywords=["just"])
        assert "just" in result

    def test_empty_input(self):
        analyzer = FillerAnalyzer(aggressiveness=1)
        assert analyzer.analyze("") == ""

    def test_no_fillers_unchanged(self):
        analyzer = FillerAnalyzer(aggressiveness=2)
        text = "Write a function that returns the sum"
        result = analyzer.analyze(text)
        assert "Write" in result
        assert "function" in result

    def test_invalid_aggressiveness(self):
        with pytest.raises(ValueError):
            FillerAnalyzer(aggressiveness=0)


# ── Redundancy Analyzer ─────────────────────────────────────────────────


class TestRedundancyAnalyzer:
    def test_removes_duplicate_sentences(self):
        analyzer = RedundancyAnalyzer()
        text = "Format the output as JSON. Make sure to format output as JSON."
        result = analyzer.analyze(text)
        # Should keep only one of the near-duplicate sentences
        assert len(result) < len(text)

    def test_keeps_distinct_sentences(self):
        analyzer = RedundancyAnalyzer()
        text = "Write a function. Test the function. Deploy the code."
        result = analyzer.analyze(text)
        assert "Write" in result
        assert "Deploy" in result

    def test_removes_repeated_phrases(self):
        analyzer = RedundancyAnalyzer()
        text = "make sure to validate make sure to validate the input"
        result = analyzer.analyze(text)
        assert len(result) < len(text)

    def test_empty_input(self):
        analyzer = RedundancyAnalyzer()
        assert analyzer.analyze("") == ""

    def test_single_sentence(self):
        analyzer = RedundancyAnalyzer()
        text = "Write a function."
        result = analyzer.analyze(text)
        assert result == text

    def test_invalid_threshold(self):
        with pytest.raises(ValueError):
            RedundancyAnalyzer(similarity_threshold=0.0)


# ── Verbosity Analyzer ──────────────────────────────────────────────────


class TestVerbosityAnalyzer:
    def test_rewrites_verbose_phrases(self):
        analyzer = VerbosityAnalyzer(aggressiveness=1)
        text = "In order to do this, due to the fact that it matters"
        result = analyzer.analyze(text)
        assert "In order to" not in result
        assert "to" in result.lower()
        assert "because" in result.lower()

    def test_prunes_articles_at_level_2(self):
        analyzer = VerbosityAnalyzer(aggressiveness=2)
        text = "Write a function and create the class"
        result = analyzer.analyze(text)
        # Articles after instruction verbs should be removed
        assert "Write a" not in result or "create the" not in result

    def test_pronoun_compression_at_level_3(self):
        analyzer = VerbosityAnalyzer(aggressiveness=3)
        text = "You should write code. You need to test it."
        result = analyzer.analyze(text)
        assert "You should" not in result
        assert "You need to" not in result

    def test_level_1_preserves_articles(self):
        analyzer = VerbosityAnalyzer(aggressiveness=1)
        text = "Write a function"
        result = analyzer.analyze(text)
        assert "a" in result.split()

    def test_preserves_keywords(self):
        analyzer = VerbosityAnalyzer(aggressiveness=1)
        text = "In order to build the API"
        result = analyzer.analyze(text, preserve_keywords=["API"])
        assert "API" in result

    def test_empty_input(self):
        analyzer = VerbosityAnalyzer(aggressiveness=1)
        assert analyzer.analyze("") == ""

    def test_case_preservation(self):
        analyzer = VerbosityAnalyzer(aggressiveness=1)
        text = "Is able to run"
        result = analyzer.analyze(text)
        assert result.startswith("C") or result.startswith("c")  # "can" or "Can"

    def test_invalid_aggressiveness(self):
        with pytest.raises(ValueError):
            VerbosityAnalyzer(aggressiveness=4)


# ── Structural Analyzer ─────────────────────────────────────────────────


class TestStructuralAnalyzer:
    def test_collapses_blank_lines(self):
        analyzer = StructuralAnalyzer(aggressiveness=1)
        text = "line 1\n\n\n\nline 2"
        result = analyzer.analyze(text)
        assert "\n\n\n" not in result
        assert "line 1" in result
        assert "line 2" in result

    def test_collapses_spaces(self):
        analyzer = StructuralAnalyzer(aggressiveness=1)
        text = "too   many    spaces"
        result = analyzer.analyze(text)
        assert "   " not in result

    def test_trims_trailing_whitespace(self):
        analyzer = StructuralAnalyzer(aggressiveness=1)
        text = "line 1   \nline 2  "
        result = analyzer.analyze(text)
        for line in result.split("\n"):
            assert line == line.rstrip()

    def test_compresses_markdown_at_level_2(self):
        analyzer = StructuralAnalyzer(aggressiveness=2)
        text = "#### Deep header"
        result = analyzer.analyze(text)
        assert result.startswith("### ")

    def test_strips_markdown_at_level_3(self):
        analyzer = StructuralAnalyzer(aggressiveness=3)
        text = "## Header\n\n**bold text**"
        result = analyzer.analyze(text)
        assert "#" not in result
        assert "**" not in result
        assert "bold text" in result

    def test_converts_lists_to_csv_at_level_3(self):
        analyzer = StructuralAnalyzer(aggressiveness=3)
        text = "- item one\n- item two\n- item three"
        result = analyzer.analyze(text)
        assert "item one" in result
        assert "item two" in result

    def test_empty_input(self):
        analyzer = StructuralAnalyzer(aggressiveness=1)
        assert analyzer.analyze("") == ""

    def test_invalid_aggressiveness(self):
        with pytest.raises(ValueError):
            StructuralAnalyzer(aggressiveness=0)

"""Analyzer for reducing verbose expressions to concise alternatives."""

from __future__ import annotations

import re


class VerbosityAnalyzer:
    """Rewrites verbose phrases with concise equivalents."""

    REWRITE_RULES: list[tuple[str, str]] = [
        ("in spite of the fact that", "although"),
        ("it is important to note that", ""),
        ("it is worth mentioning that", ""),
        ("it should be noted that", ""),
        ("a significant amount of", "much"),
        ("due to the fact that", "because"),
        ("at this point in time", "now"),
        ("take into consideration", "consider"),
        ("at the present time", "now"),
        ("as a matter of fact", ""),
        ("give an indication of", "indicate"),
        ("come to a conclusion", "conclude"),
        ("in the event that", "if"),
        ("for the purpose of", "to"),
        ("a large number of", "many"),
        ("a small number of", "few"),
        ("has the ability to", "can"),
        ("on the other hand", "however"),
        ("make a decision", "decide"),
        ("take into account", "consider"),
        ("the majority of", "most"),
        ("with regard to", "regarding"),
        ("with respect to", "regarding"),
        ("is capable of", "can"),
        ("what I mean is", ""),
        ("in addition to", "besides"),
        ("the thing is", ""),
        ("in order to", "to"),
        ("is able to", "can"),
    ]

    # Verbs after which articles can be pruned (level 2).
    _INSTRUCTION_VERBS: list[str] = [
        "write",
        "create",
        "build",
        "make",
        "return",
        "get",
        "find",
    ]

    # Pronoun compressions (level 3).
    _PRONOUN_RULES: list[tuple[str, str]] = [
        ("you need to", ""),
        ("you should", ""),
        ("you must", "must"),
        ("you can", "can"),
    ]

    def __init__(self, aggressiveness: int = 1) -> None:
        if aggressiveness not in (1, 2, 3):
            raise ValueError("aggressiveness must be 1, 2, or 3")
        self.aggressiveness = aggressiveness

    @staticmethod
    def _apply_rule(
        text: str,
        pattern_str: str,
        replacement: str,
        preserve: set[str],
    ) -> str:
        """Apply a single rewrite rule case-insensitively."""
        if preserve:
            pattern_words = pattern_str.lower().split()
            if any(w in preserve for w in pattern_words):
                return text

        pattern = re.compile(re.escape(pattern_str), re.IGNORECASE)

        def _replacer(match: re.Match[str]) -> str:
            # Preserve capitalisation of the first character when replacing
            # with a non-empty string.
            if not replacement:
                return ""
            matched = match.group(0)
            if matched[0].isupper():
                return replacement[0].upper() + replacement[1:]
            return replacement

        return pattern.sub(_replacer, text)

    def analyze(
        self, text: str, preserve_keywords: list[str] | None = None
    ) -> str:
        """Reduce verbosity in text by rewriting wordy phrases.

        Args:
            text: The input text to optimize.
            preserve_keywords: Words that should never be removed.

        Returns:
            The optimized text with verbose phrases rewritten.
        """
        if not text:
            return text

        preserved: set[str] = set()
        if preserve_keywords:
            preserved = {kw.lower() for kw in preserve_keywords}

        result = text

        # Level 1+: apply rewrite rules.
        for pattern_str, replacement in self.REWRITE_RULES:
            result = self._apply_rule(result, pattern_str, replacement, preserved)

        # Level 2+: prune articles after instruction verbs.
        if self.aggressiveness >= 2:
            for verb in self._INSTRUCTION_VERBS:
                if verb in preserved:
                    continue
                # Match: verb + article + word, replace article.
                pattern = re.compile(
                    r"(\b" + re.escape(verb) + r"\b)\s+\b(a|an|the)\b",
                    re.IGNORECASE,
                )
                result = pattern.sub(r"\1", result)

        # Level 3+: pronoun compression.
        if self.aggressiveness >= 3:
            for pattern_str, replacement in self._PRONOUN_RULES:
                result = self._apply_rule(
                    result, pattern_str, replacement, preserved
                )

        # Clean up extra whitespace.
        result = re.sub(r"  +", " ", result)
        result = re.sub(r" ([.,;:!?])", r"\1", result)
        result = re.sub(r"^\s+", "", result, flags=re.MULTILINE)

        return result.strip()

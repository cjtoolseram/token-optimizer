"""Analyzer for detecting and removing filler words and phrases."""

from __future__ import annotations

import re


class FillerAnalyzer:
    """Removes filler words and phrases that add no semantic value."""

    FILLER_WORDS: set[str] = {
        "please",
        "kindly",
        "just",
        "basically",
        "actually",
        "really",
        "very",
        "quite",
        "simply",
        "literally",
        "honestly",
        "frankly",
        "obviously",
        "clearly",
        "definitely",
        "certainly",
        "absolutely",
        "essentially",
        "virtually",
        "practically",
    }

    # Ordered longest first for greedy matching.
    FILLER_PHRASES: list[str] = [
        "What I want is for you to",
        "It would be great if you could",
        "I was wondering if you could",
        "I'd appreciate it if you could",
        "If it's not too much trouble",
        "I'm looking for you to",
        "I was hoping you could",
        "Do you think you could",
        "I'd appreciate if you",
        "I would like you to",
        "Can you help me to",
        "Please help me to",
        "Could you possibly",
        "Could you please",
        "Would you please",
        "Would you mind",
        "I'm hoping you can",
        "Can you help me",
        "Please help me",
        "If you don't mind",
        "I want you to",
        "Can you please",
        "What I need is",
        "I need you to",
        "Help me to",
        "For the purpose of",
    ]

    POLITE_OPENERS: list[str] = [
        "Hi,",
        "Hello,",
        "Hey,",
        "Hi!",
        "Hello!",
        "Hey!",
        "Hi",
        "Hello",
        "Hey",
    ]

    def __init__(self, aggressiveness: int = 2) -> None:
        if aggressiveness not in (1, 2, 3):
            raise ValueError("aggressiveness must be 1, 2, or 3")
        self.aggressiveness = aggressiveness

    def analyze(
        self, text: str, preserve_keywords: list[str] | None = None
    ) -> str:
        """Remove filler words and phrases from text.

        Args:
            text: The input text to optimize.
            preserve_keywords: Words that should never be removed.

        Returns:
            The optimized text with fillers removed.
        """
        if not text:
            return text

        preserved: set[str] = set()
        if preserve_keywords:
            preserved = {kw.lower() for kw in preserve_keywords}

        result = text

        # All levels: remove filler phrases (longest first for greedy match).
        for phrase in self.FILLER_PHRASES:
            if preserved and any(
                word.lower() in preserved for word in phrase.split()
            ):
                continue
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            result = pattern.sub("", result)

        # Level 2+: remove filler words using word boundaries.
        if self.aggressiveness >= 2:
            for word in self.FILLER_WORDS:
                if word.lower() in preserved:
                    continue
                pattern = re.compile(
                    r"\b" + re.escape(word) + r"\b", re.IGNORECASE
                )
                result = pattern.sub("", result)

        # Level 3: strip polite openers.
        if self.aggressiveness >= 3:
            stripped = result.lstrip()
            for opener in self.POLITE_OPENERS:
                if stripped.lower().startswith(opener.lower()):
                    stripped = stripped[len(opener) :].lstrip()
                    break
            result = stripped

        # Clean up extra whitespace.
        result = re.sub(r"  +", " ", result)
        result = re.sub(r" ([.,;:!?])", r"\1", result)
        result = re.sub(r"^\s+", "", result, flags=re.MULTILINE)

        return result.strip()

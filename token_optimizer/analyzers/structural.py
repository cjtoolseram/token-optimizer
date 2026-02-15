"""Analyzer for normalizing whitespace and structural formatting."""

from __future__ import annotations

import re


class StructuralAnalyzer:
    """Normalizes whitespace, collapses blank lines, and optionally
    simplifies or strips markdown formatting."""

    def __init__(self, aggressiveness: int = 1) -> None:
        if aggressiveness not in (1, 2, 3):
            raise ValueError("aggressiveness must be 1, 2, or 3")
        self.aggressiveness = aggressiveness

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        """Collapse multiple blank lines, spaces, and trailing whitespace."""
        # Trim trailing whitespace on each line.
        text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
        # Collapse multiple blank lines into a single blank line.
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Collapse multiple spaces into a single space.
        text = re.sub(r"[ \t]{2,}", " ", text)
        return text.strip()

    @staticmethod
    def _compress_markdown(text: str) -> str:
        """Simplify overly nested or excessive markdown formatting."""
        # Reduce deeply nested headers: #### or deeper becomes ###.
        text = re.sub(r"^#{4,}\s", "### ", text, flags=re.MULTILINE)

        # Compress horizontal rules to a standard form.
        text = re.sub(r"^[-*_]{4,}\s*$", "---", text, flags=re.MULTILINE)

        # Simplify repeated emphasis markers: ****text**** -> **text**
        # Handle nested bold (***+ and ***+).
        text = re.sub(r"\*{3,}([^*]+?)\*{3,}", r"**\1**", text)
        text = re.sub(r"_{3,}([^_]+?)_{3,}", r"__\1__", text)

        return text

    @staticmethod
    def _strip_markdown(text: str) -> str:
        """Remove all markdown formatting, converting to plain text."""
        # Remove headers — keep the text.
        text = re.sub(r"^#+\s+", "", text, flags=re.MULTILINE)

        # Remove horizontal rules.
        text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)

        # Remove bold/italic markers.
        text = re.sub(r"\*{1,3}([^*]+?)\*{1,3}", r"\1", text)
        text = re.sub(r"_{1,3}([^_]+?)_{1,3}", r"\1", text)

        # Remove inline code backticks.
        text = re.sub(r"`([^`]+?)`", r"\1", text)

        # Remove link formatting [text](url) -> text.
        text = re.sub(r"\[([^\]]+?)\]\([^)]+?\)", r"\1", text)

        # Remove image formatting ![alt](url) -> alt.
        text = re.sub(r"!\[([^\]]*?)\]\([^)]+?\)", r"\1", text)

        # Convert bullet lists into comma-separated items.
        lines = text.split("\n")
        result_lines: list[str] = []
        list_items: list[str] = []

        for line in lines:
            bullet_match = re.match(r"^\s*[-*+]\s+(.+)$", line)
            numbered_match = re.match(r"^\s*\d+[.)]\s+(.+)$", line)

            if bullet_match:
                list_items.append(bullet_match.group(1).strip())
            elif numbered_match:
                list_items.append(numbered_match.group(1).strip())
            else:
                if list_items:
                    result_lines.append(", ".join(list_items))
                    list_items = []
                result_lines.append(line)

        if list_items:
            result_lines.append(", ".join(list_items))

        text = "\n".join(result_lines)

        return text

    def analyze(
        self, text: str, preserve_keywords: list[str] | None = None
    ) -> str:
        """Normalize structural formatting in text.

        Args:
            text: The input text to optimize.
            preserve_keywords: Reserved for API consistency (unused).

        Returns:
            The optimized text with normalized formatting.
        """
        if not text:
            return text

        result = text

        # Level 1+: whitespace normalization.
        result = self._normalize_whitespace(result)

        # Level 2+: compress markdown formatting.
        if self.aggressiveness >= 2:
            result = self._compress_markdown(result)

        # Level 3: strip all markdown formatting.
        if self.aggressiveness >= 3:
            result = self._strip_markdown(result)

        # Final whitespace cleanup after transformations.
        result = self._normalize_whitespace(result)

        return result.strip()

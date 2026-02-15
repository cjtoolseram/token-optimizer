"""Hash-based caching for optimized prompts."""

from __future__ import annotations

import hashlib
from collections import OrderedDict
from dataclasses import dataclass


@dataclass(frozen=True)
class CacheKey:
    """Cache key combining prompt hash and strategy."""

    prompt_hash: str
    strategy: str


class PromptCache:
    """LRU cache for optimization results keyed by prompt + strategy."""

    def __init__(self, maxsize: int = 1024) -> None:
        self._maxsize = maxsize
        self._cache: OrderedDict[CacheKey, str] = OrderedDict()

    def _make_key(self, text: str, strategy: str) -> CacheKey:
        prompt_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
        return CacheKey(prompt_hash=prompt_hash, strategy=strategy)

    def get(self, text: str, strategy: str) -> str | None:
        """Look up a cached optimization result."""
        key = self._make_key(text, strategy)
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return None

    def put(self, text: str, strategy: str, optimized: str) -> None:
        """Store an optimization result."""
        key = self._make_key(text, strategy)
        if key in self._cache:
            self._cache.move_to_end(key)
        else:
            if len(self._cache) >= self._maxsize:
                self._cache.popitem(last=False)
        self._cache[key] = optimized

    def clear(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()

    @property
    def size(self) -> int:
        return len(self._cache)

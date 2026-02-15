# Token Optimizer — Agent Guide

## Project Overview

**token-optimizer** is a Python library that acts as middleware between user prompts and any
LLM provider (OpenAI, Anthropic, Google Gemini, Mistral, etc.). It reduces input token count
through intelligent compression while preserving semantic meaning, saving 20-60% on API costs.

## Architecture

```
token_optimizer/
├── engine.py              # Core orchestrator — entry point for all optimization
├── config.py              # Global defaults and configuration dataclass
├── analyzers/             # Each analyzer detects a specific type of waste
│   ├── redundancy.py      # Repeated phrases / instructions
│   ├── filler.py          # Filler words ("please", "basically", "just")
│   ├── verbosity.py       # Verbose→concise rewriting rules
│   └── structural.py      # Whitespace, markdown, formatting bloat
├── strategies/            # Strategy pattern — controls aggression level
│   ├── base.py            # Abstract interface
│   ├── conservative.py    # 10-25% reduction, safe for all prompts
│   ├── moderate.py        # 25-45% reduction, balanced
│   ├── aggressive.py      # 40-60% reduction, may alter tone
│   └── custom.py          # User-defined rule sets
├── tokenizers/            # Provider-specific token counting
│   ├── base.py            # Abstract interface
│   ├── openai_tokenizer.py
│   ├── anthropic_tokenizer.py
│   ├── gemini_tokenizer.py
│   └── generic.py         # Fallback word/char estimator
├── providers/
│   └── registry.py        # Model→tokenizer + pricing mappings
├── metrics/
│   ├── calculator.py      # Token count & cost savings
│   └── similarity.py      # Semantic similarity (original vs optimized)
└── cache/
    └── prompt_cache.py    # Hash-based caching for repeated prompts
```

## Key Design Decisions

- **Zero API calls**: Core engine is purely rule-based — no LLM calls for optimization.
- **Strategy pattern**: Optimization aggression is controlled via pluggable strategies.
- **Provider-aware**: Auto-detects tokenizer and pricing from model name.
- **Optional heavy deps**: `tiktoken`, embedding libs are optional extras.
- **Fallback cascade**: If similarity drops below threshold, auto-downgrades strategy.

## Development

```bash
# Install in dev mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=token_optimizer
```

## Testing

Tests live in `tests/`. Run with `pytest`. Key test files:
- `test_engine.py` — End-to-end optimization pipeline
- `test_analyzers.py` — Individual analyzer unit tests
- `test_strategies.py` — Strategy selection and behavior
- `test_metrics.py` — Token counting and similarity scoring

## Common Tasks

- **Add a new analyzer**: Create a module in `analyzers/`, implement `analyze(text) -> text`,
  and register it in the strategy that should use it.
- **Add a new provider**: Add model patterns + pricing to `providers/registry.py` and
  create a tokenizer in `tokenizers/` if needed.
- **Add rewriting rules**: Add entries to `analyzers/verbosity.py` `REWRITE_RULES` list.

## Code Conventions

- Python 3.10+, type hints everywhere
- Dataclasses for data containers
- Abstract base classes for interfaces
- No required heavy dependencies in core path
- All public APIs documented with docstrings

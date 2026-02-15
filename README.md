# token-optimizer

A generic token optimization engine that reduces LLM API costs by compressing prompts while preserving semantic meaning. Works with OpenAI, Anthropic, Google Gemini, and any other LLM provider.

## Installation

```bash
pip install token-optimizer

# With OpenAI token counting support
pip install token-optimizer[openai]

# With all optional dependencies
pip install token-optimizer[all]
```

## Quick Start

```python
from token_optimizer import TokenOptimizer

optimizer = TokenOptimizer(model="gpt-4o", strategy="moderate")

result = optimizer.optimize(
    "I would like you to please help me write a Python function that "
    "takes a list of numbers as input and then returns the sum of all "
    "the numbers in that list. Please make sure the function handles "
    "empty lists properly. Also, I want you to make sure that the "
    "function handles empty lists properly."
)

print(result.optimized_text)
# "Write a Python function: input list of numbers, return sum. Handle empty lists."

print(f"Saved {result.savings_percent:.1f}% tokens")
print(f"Estimated cost savings: ${result.estimated_cost_savings:.6f}")
```

## Strategies

| Strategy | Reduction | Description |
|----------|-----------|-------------|
| `conservative` | 10-25% | Only removes clear filler and whitespace. Safe for all prompts. |
| `moderate` | 25-45% | Applies rewriting rules, prunes articles in instructions. |
| `aggressive` | 40-60% | Maximum compression with shorthand. May alter tone. |

```python
# Conservative — safe for production
optimizer = TokenOptimizer(model="claude-sonnet-4-5-20250929", strategy="conservative")

# Aggressive — maximum savings
optimizer = TokenOptimizer(model="gemini-2.0-flash", strategy="aggressive")
```

## Features

- **Provider-agnostic**: Works with any LLM (OpenAI, Anthropic, Gemini, Mistral, etc.)
- **Zero API calls**: Pure rule-based optimization — no LLM calls needed
- **Strategy levels**: Conservative, moderate, and aggressive compression
- **Accurate token counting**: Provider-specific tokenizers for exact counts
- **Cost calculation**: Real-time cost savings based on model pricing
- **Semantic validation**: Similarity scoring ensures meaning is preserved
- **Caching**: Automatic caching for repeated/templated prompts
- **Keyword preservation**: Protect specific terms from optimization

## CLI

```bash
# Optimize a prompt
token-optimizer "Your long prompt here" --model gpt-4o --strategy moderate

# From stdin
echo "Your prompt" | token-optimizer --model claude-sonnet-4-5-20250929

# Show detailed metrics
token-optimizer "Your prompt" --model gpt-4o --verbose
```

## Custom Pricing

```python
optimizer = TokenOptimizer(
    model="custom-model",
    cost_per_1k_input=0.003,
    cost_per_1k_output=0.015,
)
```

## License

MIT

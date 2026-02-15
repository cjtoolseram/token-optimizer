"""CLI interface for token-optimizer."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> None:
    """Entry point for the token-optimizer CLI."""
    parser = argparse.ArgumentParser(
        prog="token-optimizer",
        description="Optimize LLM prompts to reduce token usage and cost.",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="The prompt to optimize. Reads from stdin if not provided.",
    )
    parser.add_argument(
        "--model", "-m",
        default="gpt-4o",
        help="Target model for token counting and pricing (default: gpt-4o).",
    )
    parser.add_argument(
        "--strategy", "-s",
        choices=["conservative", "moderate", "aggressive"],
        default="moderate",
        help="Optimization strategy (default: moderate).",
    )
    parser.add_argument(
        "--preserve", "-p",
        nargs="*",
        default=[],
        help="Keywords to preserve during optimization.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed optimization metrics.",
    )
    parser.add_argument(
        "--show-diff",
        action="store_true",
        help="Show before/after comparison.",
    )

    args = parser.parse_args(argv)

    # Read prompt from argument or stdin
    prompt = args.prompt
    if prompt is None:
        if sys.stdin.isatty():
            parser.error("No prompt provided. Pass a prompt or pipe from stdin.")
        prompt = sys.stdin.read().strip()

    if not prompt:
        parser.error("Empty prompt provided.")

    from token_optimizer import TokenOptimizer

    optimizer = TokenOptimizer(
        model=args.model,
        strategy=args.strategy,
        preserve_keywords=args.preserve,
    )

    result = optimizer.optimize(prompt)

    if args.show_diff:
        print("=== ORIGINAL ===")
        print(result.original_text)
        print()
        print("=== OPTIMIZED ===")

    print(result.optimized_text)

    if args.verbose:
        print()
        print("--- Metrics ---")
        print(f"Model:            {args.model}")
        print(f"Strategy:         {result.strategy_used}")
        print(f"Original tokens:  {result.original_tokens}")
        print(f"Optimized tokens: {result.optimized_tokens}")
        print(f"Tokens saved:     {result.tokens_saved}")
        print(f"Savings:          {result.savings_percent:.1f}%")
        print(f"Cost savings:     ${result.estimated_cost_savings:.6f}")
        print(f"Similarity:       {result.similarity_score:.3f}")


if __name__ == "__main__":
    main()

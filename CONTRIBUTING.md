# Contributing to token-optimizer

Thanks for your interest in contributing! Here's how you can help.

## Getting Started

1. Fork the repository
2. Clone your fork and create a branch:
   ```bash
   git clone https://github.com/<your-username>/token-optimizer.git
   cd token-optimizer
   git checkout -b my-feature
   ```
3. Set up the development environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

## Making Changes

- Keep changes focused — one feature or fix per PR
- Add tests for new functionality
- Run the test suite before submitting:
  ```bash
  pytest
  ```

## Submitting a Pull Request

1. Push your branch to your fork
2. Open a PR against `main`
3. Describe what your change does and why

## Reporting Bugs

Open an issue with:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Python version and OS

## Code Style

- Use type hints (Python 3.10+ syntax)
- Follow existing patterns in the codebase
- Keep functions focused and small

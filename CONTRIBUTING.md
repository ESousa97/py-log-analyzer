# Contributing to Python Log Analyzer

First off, thank you for considering contributing to Python Log Analyzer! It's people like you that make it such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:
- Use welcoming and inclusive language.
- Be respectful of differing viewpoints and experiences.
- Gracefully accept constructive criticism.

## How Can I Contribute?

### Reporting Bugs
- Use the GitHub Issues to report bugs.
- Include steps to reproduce, expected behavior, and actual behavior.

### Suggesting Enhancements
- Open a GitHub Issue with the "enhancement" label.
- Describe the feature and why it would be useful.

### Pull Requests
1. Fork the repo and create your branch from `master`.
2. Install development dependencies: `pip install -r requirements-dev.txt`.
3. If you've added code that should be tested, add tests.
4. Ensure the test suite passes: `pytest`.
5. Run linting and formatting: `ruff check .` and `ruff format .`.
6. Issue that pull request!

## Development Setup

We use `ruff` for linting and formatting, and `pytest` for testing.

```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

## Python Style Guide

We follow [PEP 8](https://peps.python.org/pep-0008/) and use `ruff` to enforce it. Please ensure your code follows these standards before submitting a PR.

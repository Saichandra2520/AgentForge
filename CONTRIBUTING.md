# Contributing to create-agent-app

Thanks for your interest in contributing.

## Development Setup

1. Fork and clone the repo.
2. Create a virtual environment.
3. Install dev dependencies:

```bash
pip install -e .[dev]
```

## Local Checks

```bash
python -m build
python -m twine check dist/*
```

If you modify templates, generate a sample project and verify it runs.

## Pull Requests

1. Create a feature/fix branch.
2. Keep PRs focused and small where possible.
3. Update docs when behavior changes.
4. Include clear reproduction and validation steps.

## Reporting Issues

Please include:

- OS and Python version
- Full command used
- Full error output
- Expected vs actual behavior

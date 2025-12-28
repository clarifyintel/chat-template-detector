# Contributing

Thanks for your interest in contributing to Chat Template Detector.

## Development Setup

1. Clone the repository
2. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

```bash
pytest tests/
```

## Code Style

We use black for formatting:
```bash
black src/ tests/
```

## Adding New Templates

To add a new chat template:

1. Add template definition to `src/chat_template_detector/templates.py`
2. Add model mapping if applicable
3. Add tests in `tests/test_detector.py`
4. Update documentation

## Reporting Issues

Use GitHub Issues. Include:
- Training file format example
- Inference config
- Expected vs actual behavior

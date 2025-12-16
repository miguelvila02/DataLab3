# Contributing to Premier League Match Predictor

Thank you for your interest in contributing! 🎉

This document provides guidelines for contributing to this project.

## Quick Start

1. Fork the repository
2. Clone your fork
3. Create a branch
4. Make your changes
5. Run tests
6. Submit a pull request

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

## Code of Conduct

By participating in this project, you agree to:

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- Basic knowledge of machine learning
- Familiarity with pytest and FastAPI (for specific contributions)

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/pl-match-predictor.git
cd pl-match-predictor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify installation
make test
```

## Making Changes

### Branch Naming

Use descriptive branch names:

- `feature/add-new-model` - New features
- `fix/api-validation` - Bug fixes
- `docs/update-readme` - Documentation
- `refactor/model-code` - Code refactoring
- `test/add-unit-tests` - Adding tests

### Commit Messages

Follow conventional commits:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

Examples:
```
feat(api): add weighted prediction endpoint

Add new endpoint that allows custom weighting of recent games.
Includes validation and tests.

Closes #123
```

```
fix(model): correct feature scaling

Features were not being scaled consistently between training
and prediction, causing accuracy issues.
```

## Testing

### Running Tests

```bash
# All tests
make test

# With coverage
make test-cov

# Quick tests (no slow tests)
make test-quick

# Specific test file
pytest tests/test_api.py -v

# Specific test
pytest tests/test_api.py::test_predict_success -v
```

### Writing Tests

- Write tests for all new features
- Maintain >80% code coverage
- Use descriptive test names
- Include docstrings

Example:
```python
def test_prediction_with_extreme_stats():
    """Test that model handles extreme stat values correctly."""
    extreme_home = [{'possession': 90, ...}]
    extreme_away = [{'possession': 10, ...}]
    
    result = predict_from_recent_form(extreme_home, extreme_away)
    
    assert result['prediction'] == 'Home Win'
    assert result['confidence'] > 70
```

### Test Categories

Mark tests appropriately:

```python
@pytest.mark.slow
def test_full_training_pipeline():
    """Long-running integration test."""
    pass

@pytest.mark.unit
def test_calculate_average():
    """Fast unit test."""
    pass
```

## Code Style

### Python Style Guide

- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Max line length: 100 characters

### Formatting

```bash
# Format code
make format

# Check formatting
make format-check

# Lint
make lint

# Type check
make type-check
```

### Docstrings

Use Google-style docstrings:

```python
def predict_match(home_stats: List[Dict], away_stats: List[Dict]) -> Dict:
    """
    Predict match outcome based on team statistics.
    
    Args:
        home_stats: List of dicts with home team statistics
        away_stats: List of dicts with away team statistics
    
    Returns:
        Dictionary containing prediction, confidence, and probabilities
    
    Raises:
        ValueError: If stats are invalid
    
    Example:
        >>> home = [{'possession': 55, 'shots_on_target': 5, ...}]
        >>> away = [{'possession': 45, 'shots_on_target': 3, ...}]
        >>> result = predict_match(home, away)
        >>> print(result['prediction'])
        'Home Win'
    """
    pass
```

### Type Hints

Always use type hints:

```python
from typing import List, Dict, Optional, Tuple

def process_data(
    raw_data: pd.DataFrame,
    min_games: int = 5
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """Process raw match data."""
    pass
```

## Submitting Changes

### Pull Request Process

1. **Update Documentation**
   - Update README if needed
   - Add/update docstrings
   - Update CHANGELOG.md

2. **Run Checks**
   ```bash
   make ci
   ```

3. **Create Pull Request**
   - Use a descriptive title
   - Reference related issues
   - Describe changes clearly
   - Add screenshots (if UI changes)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring
- [ ] Tests

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] CHANGELOG.md updated
- [ ] All checks passing

## Related Issues
Closes #XXX
```

### Review Process

- Maintainers will review within 3-5 days
- Address review comments
- Keep PR focused and small
- Be responsive to feedback

## Reporting Bugs

### Before Submitting

- Check existing issues
- Verify it's actually a bug
- Collect relevant information

### Bug Report Template

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What should happen

**Actual behavior**
What actually happens

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.10]
- Package version: [e.g., 0.1.0]

**Additional context**
Any other relevant information
```

## Feature Requests

### Suggesting Features

- Check if already requested
- Explain the use case
- Describe desired behavior
- Consider implementation

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
What you want to happen

**Describe alternatives you've considered**
Other solutions you've thought about

**Additional context**
Any other relevant information
```

## Documentation

### Types of Documentation

- **Code comments**: Explain complex logic
- **Docstrings**: Document functions/classes
- **README**: Project overview
- **Guides**: User documentation
- **API docs**: Endpoint documentation

### Documentation Standards

- Clear and concise
- Include examples
- Keep up to date
- Check spelling/grammar

## Recognition

Contributors will be:

- Listed in README
- Mentioned in release notes
- Credited in documentation

## Getting Help

- [GitHub Discussions](https://github.com/miguelvila02/pl-match-predictor/discussions)
- [Issue Tracker](https://github.com/miguelvila02/pl-match-predictor/issues)
- Email: luismiguelvila@gmail.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! **
# Contributing Guidelines

## Welcome Contributors! 🎉

Thank you for your interest in contributing to **Jan-Gana-Drishti**. This document provides guidelines for contributing to this Government of India project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

This project serves the Government of India and follows strict professional standards:

- **Respectful Communication**: Maintain professional and courteous interactions
- **Government Compliance**: Follow all UIDAI and NIC guidelines
- **Data Privacy**: Never expose PII or sensitive information
- **Collaborative Spirit**: Help others and share knowledge

---

## Getting Started

### 1. Fork the Repository

```bash
git clone https://github.com/YOUR_USERNAME/jan-gana-drishti.git
cd jan-gana-drishti
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions

---

## Development Workflow

### 1. Make Changes

- Write clean, readable code
- Follow Python PEP 8 style guide
- Add comments for complex logic
- Update documentation as needed

### 2. Test Your Changes

```bash
# Run unit tests
python -m pytest tests/

# Run linting
flake8 modules/ app.py

# Check formatting
black --check modules/ app.py

# Test dashboard locally
streamlit run app.py
```

### 3. Commit Changes

Use semantic commit messages:

```bash
git commit -m "feat: add new fraud detection algorithm"
git commit -m "fix: resolve state name matching issue"
git commit -m "docs: update API documentation"
```

Commit message prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Test additions or updates
- `chore:` - Build/tool changes

---

## Code Standards

### Python Style Guide

Follow PEP 8 with these specifics:

```python
# Good: Clear function names with docstrings
def calculate_migration_score(biometric_count: int, demographic_count: int) -> float:
    """
    Calculate migration score based on update ratios.
    
    Args:
        biometric_count: Number of biometric authentications
        demographic_count: Number of demographic updates
    
    Returns:
        Migration score (float)
    """
    if demographic_count == 0:
        return 0.0
    return (demographic_count / biometric_count) * 1000


# Bad: Unclear naming, no docstring
def calc(b, d):
    if d == 0:
        return 0
    return (d/b)*1000
```

### Type Hints

Use type hints for function signatures:

```python
from typing import Tuple, Optional
import pandas as pd

def load_data(filepath: str) -> Tuple[pd.DataFrame, Optional[str]]:
    """Load data and return dataframe with optional error message."""
    try:
        df = pd.read_csv(filepath)
        return df, None
    except Exception as e:
        return pd.DataFrame(), str(e)
```

### Error Handling

Always handle exceptions gracefully:

```python
# Good
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    return default_value
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise

# Bad
try:
    result = risky_operation()
except:
    pass  # Silent failure
```

---

## Testing Requirements

### Unit Tests

Create tests for new functions:

```python
# tests/test_fraud_detection.py
import pytest
from modules.fraud_detection import GhostHunterEngine

def test_benford_law_calculation():
    """Test Benford's Law calculation."""
    # Arrange
    test_data = create_test_dataframe()
    engine = GhostHunterEngine(test_data)
    
    # Act
    result = engine.benford_law_test()
    
    # Assert
    assert len(result) > 0
    assert 'benford_deviation_factor' in result.columns
    assert all(result['benford_deviation_factor'] >= 0)
```

### Integration Tests

Test module interactions:

```python
def test_end_to_end_pipeline():
    """Test complete ETL to analysis pipeline."""
    # Load data
    merged_data, pipeline = load_and_clean_data()
    
    # Run fraud detection
    engine = GhostHunterEngine(merged_data)
    fraud_results = engine.benford_law_test()
    
    # Verify results
    assert len(fraud_results) > 0
```

### Coverage Requirements

- Aim for 80%+ code coverage
- All critical paths must be tested
- Edge cases should be covered

```bash
# Check coverage
pytest --cov=modules --cov-report=html
```

---

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def calculate_roi(savings: float, costs: float, years: int = 1) -> dict:
    """
    Calculate Return on Investment (ROI) for policy interventions.
    
    Args:
        savings: Projected annual savings in rupees
        costs: Implementation costs in rupees
        years: Time horizon for ROI calculation (default: 1)
    
    Returns:
        Dictionary containing:
            - 'roi_percentage': ROI as percentage
            - 'net_benefit': Net savings minus costs
            - 'payback_period': Years to break even
    
    Raises:
        ValueError: If savings or costs are negative
        
    Example:
        >>> calculate_roi(savings=100000, costs=20000)
        {'roi_percentage': 400.0, 'net_benefit': 80000, 'payback_period': 0.2}
    """
    if savings < 0 or costs < 0:
        raise ValueError("Savings and costs must be non-negative")
    
    roi_pct = ((savings - costs) / costs) * 100 if costs > 0 else 0
    net_benefit = savings - costs
    payback = costs / savings if savings > 0 else float('inf')
    
    return {
        'roi_percentage': roi_pct,
        'net_benefit': net_benefit,
        'payback_period': payback
    }
```

### API Documentation

Update [docs/API.md](docs/API.md) when adding new functions.

### README Updates

Keep [README.md](../README.md) current with new features.

---

## Pull Request Process

### 1. Before Submitting

- [ ] All tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts with main branch

### 2. Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
```

### 3. Review Process

1. **Automated Checks**: CI/CD runs tests and linting
2. **Code Review**: Maintainer reviews code quality
3. **Testing**: Verify functionality in staging environment
4. **Approval**: At least one maintainer approval required
5. **Merge**: Squash and merge to main branch

---

## Feature Requests

### Submitting Feature Requests

Use GitHub Issues with this template:

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Government/policy use case for this feature

**Proposed Implementation**
Technical approach (optional)

**Impact**
Expected benefit to governance/policy

**Priority**
Low / Medium / High / Critical
```

---

## Bug Reports

### Submitting Bug Reports

```markdown
**Bug Description**
Clear description of the issue

**Steps to Reproduce**
1. Go to...
2. Click on...
3. See error...

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.10]
- Browser: [e.g., Chrome 120]

**Screenshots**
If applicable

**Additional Context**
Any other relevant information
```

---

## Development Tools

### Recommended IDE Setup

**VS Code Extensions**:
- Python (Microsoft)
- Pylance
- Black Formatter
- autoDocstring
- GitLens

**Settings** (`.vscode/settings.json`):
```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true
}
```

---

## Resources

- [Python PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [UIDAI Guidelines](https://uidai.gov.in/)

---

## Recognition

Contributors will be acknowledged in:
- README.md Contributors section
- Release notes
- Project documentation

---

## Questions?

- **Technical Questions**: Open a GitHub Discussion
- **Security Issues**: Email security@nic.in
- **General Inquiries**: Create a GitHub Issue

---

Thank you for contributing to Jan-Gana-Drishti! 🇮🇳

Your contributions help improve governance and public service delivery across India.

# Contributing to autocash-ultimate

Thank you for your interest in contributing to autocash-ultimate! This document provides guidelines for contributing to the project.

## Code of Conduct

### Ethical Principles (Non-Negotiable)
1. **No Fraud**: No auto-clicks, metric manipulation, or deceptive practices
2. **Legal Compliance**: Respect all laws, regulations, and platform TOS
3. **Privacy First**: LGPD compliance, data minimization, consent-based
4. **Review Required**: All generated content requires human review
5. **Transparency**: Clear about affiliate relationships and data usage

## How to Contribute

### Reporting Issues
- Use GitHub Issues
- Provide detailed description
- Include reproduction steps
- Add logs/screenshots if applicable
- Tag appropriately (bug, feature, security, etc.)

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow code style (Black, isort, flake8)
   - Add tests for new functionality
   - Update documentation
   - Ensure LGPD compliance

4. **Run tests**
   ```bash
   pytest --cov=app
   ```

5. **Commit with conventional commits**
   ```bash
   git commit -m "feat: add new feature"
   git commit -m "fix: resolve bug in generator"
   git commit -m "docs: update README"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### Local Setup
```bash
# Clone repository
git clone https://github.com/ParkNow914/money.git
cd money

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Start with Docker
docker-compose -f docker/docker-compose.yml up
```

## Code Standards

### Python Style
- **Formatter**: Black (line length: 100)
- **Import sorting**: isort
- **Linter**: flake8
- **Type hints**: Required for public APIs

### Testing
- **Framework**: pytest
- **Coverage**: Minimum 75% for core modules
- **Test types**: Unit, integration, E2E (where applicable)

### Documentation
- **Docstrings**: Google style
- **README**: Keep updated with new features
- **API docs**: Auto-generated from code
- **Inline comments**: Only when necessary for complex logic

## Project Structure

```
app/              # Main application
├── routes/       # API endpoints
├── services/     # Business logic
└── models.py     # Database models

tests/            # Test suite
docs/             # Documentation
scripts/          # Utility scripts
docker/           # Docker configuration
```

## Pull Request Process

### PR Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] LGPD compliance verified
- [ ] Security implications considered
- [ ] No secrets committed
- [ ] Conventional commit messages

### Review Process
1. Automated CI/CD checks run
2. Code review by maintainer
3. Security review for sensitive changes
4. LGPD compliance review
5. Manual testing if needed
6. Merge to main after approval

## Areas for Contribution

### High Priority
- [ ] DSAR endpoints (data export, deletion)
- [ ] Email funnel implementation
- [ ] A/B testing framework
- [ ] Personalization engine
- [ ] Performance optimization

### Medium Priority
- [ ] Additional content formats
- [ ] Improved SEO optimization
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] API rate limiting

### Low Priority
- [ ] UI/UX improvements
- [ ] Additional integrations
- [ ] Documentation improvements
- [ ] Example implementations

## Security

### Reporting Security Issues
**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email security contact (see README)
2. Include detailed description
3. Provide steps to reproduce
4. Suggest fix if possible

### Security Review Required
- Authentication/authorization changes
- Data handling modifications
- External API integrations
- Cryptography implementations
- Infrastructure changes

## LGPD Compliance Review

All contributions must maintain LGPD compliance:

- [ ] No raw PII stored
- [ ] Hashed identifiers used
- [ ] Consent mechanism respected
- [ ] Data minimization followed
- [ ] Audit logging maintained
- [ ] Retention policies honored

See [docs/lgpd_checklist.md](docs/lgpd_checklist.md) for full checklist.

## Testing Guidelines

### Unit Tests
```python
def test_feature():
    """Test description."""
    # Arrange
    setup_data()
    
    # Act
    result = function_to_test()
    
    # Assert
    assert result == expected
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_api_endpoint():
    """Test API endpoint."""
    response = await client.get("/endpoint")
    assert response.status_code == 200
```

## Documentation

### Code Documentation
```python
def function_name(param: str) -> dict:
    """
    Short description.
    
    Longer description if needed.
    
    Args:
        param: Parameter description
    
    Returns:
        Return value description
    
    Raises:
        ValueError: When invalid input
    """
    pass
```

### API Documentation
- FastAPI auto-generates OpenAPI docs
- Add descriptive docstrings to endpoints
- Include request/response examples

## Questions?

- Open a GitHub Discussion
- Check existing issues
- Review documentation in /docs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make autocash-ultimate better! 🚀

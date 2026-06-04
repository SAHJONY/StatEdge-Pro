# Contributing to StatEdge Pro

Thank you for considering contributing to StatEdge Pro! We appreciate your interest in helping to build a better sports analytics platform.

## Code of Conduct

This project and everyone participating in it is governed by the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to Contribute

### 1. Find an Issue

Start by looking through our [issues](https://github.com/yourusername/statedge-pro/issues). Look for issues labeled "good first issue" or "help wanted". These are great places to start.

### 2. Fork the Repository

Fork the repository on GitHub by clicking the "Fork" button in the top right corner.

### 3. Clone Your Fork

Clone your fork to your local machine:

```bash
git clone https://github.com/yourusername/statedge-pro.git
cd statedge-pro
```

### 4. Create a Branch

Create a new branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/your-bug-fix-name
```

### 5. Make Your Changes

Make your changes following our coding standards:

- Use Python 3.10+
- Follow PEP 8 style guidelines
- Write clear, readable code
- Add docstrings to all functions and classes
- Write tests for new functionality
- Keep commits focused and atomic

### 6. Test Your Changes

Run the test suite to ensure your changes don't break anything:

```bash
make test
make test-coverage
make lint
make type-check
```

### 7. Commit Your Changes

Commit your changes with a clear, descriptive message:

```bash
git add .
git commit -m "feat: add new analytics feature for basketball"
```

### 8. Push Your Branch

Push your branch to your fork:

```bash
git push origin feature/your-feature-name
```

### 9. Create a Pull Request

Go to your fork on GitHub and click the "Compare & pull request" button. Fill out the pull request template with:

- A clear description of your changes
- Why you made these changes
- Any relevant issue numbers
- Screenshots or demonstrations if applicable

### 10. Address Feedback

We'll review your pull request and may ask for changes. Be responsive to feedback and make any requested changes.

## Coding Standards

### Python

- Use Python 3.10+
- Follow PEP 8 style guidelines
- Use 4 spaces for indentation
- Keep lines under 88 characters
- Use type hints for all functions and classes
- Write docstrings for all public functions and classes

### Testing

- Write unit tests for all new functionality
- Use pytest for testing
- Aim for at least 80% test coverage
- Test edge cases and error conditions

### Documentation

- Update documentation when adding new features
- Keep the README.md up to date
- Write clear commit messages

## Development Environment

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Git

### Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Install development dependencies: `pip install -r requirements-dev.txt`
6. Set up environment variables: copy `.env.example` to `.env` and fill in your values

### Running the Application

```bash
# Run the application
make run

# Or with Docker Compose
make up
```

## Testing

Run the test suite:

```bash
make test
```

Run tests with coverage:

```bash
make test-coverage
```

Run linter:

```bash
make lint
```

Run type checker:

```bash
make type-check
```

## Code Review Process

All changes must be reviewed by at least one other team member before merging. We use GitHub's pull request review system.

When reviewing:

- Check for code quality and readability
- Ensure tests are included and passing
- Verify documentation is updated
- Check for security issues
- Ensure the change aligns with the project's goals

## Release Process

Releases are made on a monthly basis. The release manager will:

1. Create a release branch
2. Update version numbers
3. Update changelog
4. Create a release tag
5. Build and publish Docker images
6. Announce the release

## Security

If you discover a security vulnerability, please email us directly at sahjonycapitalllc@outlook.com instead of opening an issue.

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## Contact

For questions or suggestions, please contact us at sahjonycapitalllc@outlook.com.
# Contributing to EmailGuard

Thank you for your interest in contributing to EmailGuard! 🎉

## How to Contribute

### 1. Report Bugs
Found a bug? Please open an issue using the [Bug Report](/.github/ISSUE_TEMPLATE/bug_report.md) template.

**Include:**
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python version, EmailGuard version)
- Screenshots/logs if applicable

### 2. Request Features
Have a great idea? Open an issue using the [Feature Request](/.github/ISSUE_TEMPLATE/feature_request.md) template.

**Include:**
- Clear description of the feature
- Why it would be useful
- Proposed implementation (optional)
- Alternative approaches (optional)

### 3. Ask Questions
Have questions? Open an issue using the [Question](/.github/ISSUE_TEMPLATE/question.md) template.

### 4. Submit Code Changes

#### Setup Development Environment
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/EmailGuard.git
cd EmailGuard

# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies (if any)
pip install black flake8 pytest
```

#### Make Changes
1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test your changes: `python cli.py batch samples/`
4. Follow code style guidelines (see below)
5. Commit with clear messages: `git commit -m "Add feature: description"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Open a Pull Request

#### Code Style Guidelines

- **Python Style:** Follow PEP 8
- **Naming:** Use descriptive names (e.g., `is_phishing_email` not `is_ph`)
- **Comments:** Add comments for complex logic
- **Docstrings:** Add docstrings to functions and classes
- **Testing:** Test your changes thoroughly

**Format code with Black:**
```bash
black classifier.py email_parser.py cli.py
```

**Check style with Flake8:**
```bash
flake8 classifier.py email_parser.py cli.py
```

### 5. Improve Documentation

Documentation improvements are always welcome!

- Fix typos
- Clarify explanations
- Add examples
- Create tutorials

## Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Commit** with clear messages
6. **Push** to your fork
7. **Open** a Pull Request with:
   - Clear title
   - Description of changes
   - Reference to any related issues (#123)
   - Screenshots/logs if applicable

### PR Title Format
```
[TYPE] Brief description

Types:
- [BUGFIX] - Bug fix
- [FEATURE] - New feature
- [DOCS] - Documentation
- [REFACTOR] - Code refactor
- [TEST] - Tests
```

### Example
```
[FEATURE] Add support for custom phishing domains

This PR adds a new configuration option to specify custom domains
to check for typosquatting in addition to the default list.

Fixes #42
```

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Assume good intentions
- Report inappropriate behavior

## Areas for Contribution

### High Priority
- 🔴 Bug fixes
- 🟡 Performance improvements
- 🟡 Documentation enhancements
- 🟢 Test coverage

### Medium Priority
- 🟢 New detection rules
- 🟢 Custom configuration options
- 🔵 Additional output formats

### Nice to Have
- 🔵 Integration examples
- 🔵 Community resources
- 🔵 Advanced tutorials

## Questions?

- 📖 Read the [README.md](../README.md)
- 📚 Check [QUICKSTART.md](../QUICKSTART.md)
- 🤔 Open a [Question issue](/.github/ISSUE_TEMPLATE/question.md)
- 💬 Start a Discussion (if enabled)

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Thanked in release notes
- Featured on the project website

Thank you for contributing to EmailGuard! 🙏

---

**Happy coding!** 🚀

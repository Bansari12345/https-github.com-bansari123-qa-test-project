# GitHub Public Interface Testing Suite

Comprehensive automated testing suite for GitHub's public interface using **Playwright** and **pytest**. Features clean code architecture, extensive logging, and DRY principles.

## 🎯 Test Coverage

### UI Tests (9 tests)
- Repository page loading and display
- Star and fork count verification
- README content rendering
- Code navigation (folders and files)
- TypeScript file with line numbers
- Repository metadata (About, license, topics)

### API Tests (4 tests)
- GET /repos/{owner}/{repo} endpoint
- GET /repos/{owner}/{repo}/contents endpoint  
- 404 error handling
- Rate limit headers validation

### Bonus Tests (5 tests)
- Repository search functionality
- Search with filters
- User profile search
- 404 error pages

**Total: 18 tests covering UI, API, and edge cases**

## 📋 Prerequisites

- **Python 3.12+**
- **pip** (Python package installer)
- **Internet connection** (for accessing GitHub)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd tests
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

### 3. Run All Tests

```bash
pytest --browser-name=chromium --html=report.html --self-contained-html -v
```

## 📝 Running Tests

### Run All Tests with HTML Report

```bash
pytest --browser-name=chromium --html=report.html --self-contained-html -v
```

### Run Specific Test Files

```bash
# UI tests only
pytest test_repository_ui.py --browser-name=chromium -v

# API tests only
pytest test_repository_api.py -v

# Search/Bonus tests only
pytest test_search.py --browser-name=chromium -v
```

### Run Specific Test Classes

```bash
# Repository page tests
pytest test_repository_ui.py::TestRepositoryPage -v

# Code navigation tests
pytest test_repository_ui.py::TestCodeNavigation -v

# API tests
pytest test_repository_api.py::TestGitHubAPI -v
```

### Run with Different Browsers

```bash
# Firefox
pytest --browser-name=firefox --html=report.html -v

# WebKit (Safari engine)
pytest --browser-name=webkit --html=report.html -v
```

## 📁 Project Structure

```
tests/
├── .gitignore                  # Excludes logs, cache, reports
├── conftest.py                 # Pytest fixtures and configuration
├── config.py                   # Test configuration (URLs, settings)
├── helpers.py                  # Reusable helper functions (DRY)
├── test_repository_ui.py       # UI tests (9 tests)
├── test_repository_api.py      # API tests (4 tests)
├── test_search.py              # Search & 404 tests (5 tests)
├── logs/
│   └── tests.log               # Detailed test execution logs
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🏗️ Code Architecture

### Design Principles

- **DRY (Don't Repeat Yourself)**: Common functionality in `helpers.py`
- **Clean Code**: Clear naming, single responsibility
- **Abstraction**: `PageHelper` class for common operations
- **Comprehensive Logging**: Detailed logs for debugging
- **Type Hints**: Better code clarity and IDE support

### Key Components

#### `PageHelper` Class
Provides reusable page operations:
- `navigate_and_wait()` - Navigate with proper waiting
- `verify_element_visible()` - Element visibility with logging
- `verify_text_contains()` - Text validation with logging

#### Helper Functions
- `extract_number_from_text()` - Parse GitHub number formats ("160k", "1,234")
- `log_test_step()` - Enhanced test step logging
- `verify_url_contains()` - URL validation helper

## 📊 Test Reports

After running tests, open `report.html` in your browser:
- Summary of passed/failed tests
- Execution time per test
- Detailed error messages for failures
- Environment information

## 🔧 Configuration

### `config.py`
```python
# GitHub URLs
GITHUB_BASE_URL = "https://github.com"
API_BASE_URL = "https://api.github.com"

# Test repository
TEST_REPO_URL = "https://github.com/microsoft/vscode"
TEST_REPO_OWNER = "microsoft"
TEST_REPO_NAME = "vscode"

# Browser settings
BROWSER_CONFIG = {
    "headless": False,
    "slow_mo": 500
}
```

### `conftest.py`
- Browser launch configuration
- Pytest fixtures
- Cross-browser support
- Logging setup

## 📝 Logging

Logs are written to both:
1. **Console**: Real-time test progress
2. **File**: `logs/tests.log` (persistent, detailed)

Log levels:
- `INFO`: Test steps and results
- `DEBUG`: Element interactions
- `WARNING`: Non-critical issues
- `ERROR`: Test failures

## ✨ Features

- ✅ **Visible Browser Execution**: Watch tests run in real browser
- ✅ **Cross-Browser Support**: Chromium, Firefox, WebKit
- ✅ **Comprehensive Logging**: Console + file with timestamps
- ✅ **HTML Reports**: Professional test reports
- ✅ **Clean Code**: DRY principles, proper abstraction
- ✅ **Type Hints**: Better code documentation
- ✅ **Error Handling**: Graceful failures with detailed messages
- ✅ **Reusable Components**: PageHelper class and utilities

## 🐛 Troubleshooting

### Browser doesn't open
```bash
playwright install chromium
```

### Import errors
```bash
pip install -r requirements.txt
```

### Tests fail with timeout
- Check internet connection
- GitHub might be slow, tests auto-retry
- Increase timeout in `config.py`

### Permission errors on Windows
Run terminal as Administrator

## 📚 Dependencies

```
playwright==1.57.0
pytest==9.0.2
pytest-playwright==0.7.2
pytest-html==4.1.1
loguru==0.7.3
requests==2.32.5
```

## 🎓 Best Practices Implemented

1. **Page Object Pattern**: Encapsulated in `PageHelper`
2. **Explicit Waits**: No hardcoded sleeps (except where necessary)
3. **Descriptive Assertions**: Clear failure messages
4. **Test Independence**: Each test can run standalone
5. **Proper Fixtures**: Browser context isolation
6. **Clean Up**: Automatic browser/context closure
7. **Logging**: Comprehensive for debugging
8. **Error Handling**: Graceful degradation

---

**Happy Testing! 🚀**

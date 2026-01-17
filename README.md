# GitHub Public Interface Testing Challenge

## Overview
This project contains automated UI and API tests for GitHub’s public interface, developed as part of a QA Automation Engineer assessment.

**Tech Stack**
- Language: Python (pytest) or JavaScript
- Framework: Playwright
- Browser: Visible mode only (non-headless)
- Logging: loguru (Python) / winston (JavaScript)

## Prerequisites

### Python
- Python 3.12+
- pytest
- pytest-playwright
- playwright
- requests
- loguru

### JavaScript
- Node.js 20+
- @playwright/test
- axios
- winston

Install Playwright browsers:
```bash
playwright install
```

## Project Structure
tests/
├── conftest.py / playwright.config.js
├── config.py / config.js
├── test_repository_ui.py
├── test_repository_api.py
├── test_search.py
├── helpers.py
├── logs/
│   └── tests.log
├── requirements.txt / package.json
└── README.md

## What Is Tested

### UI Tests
- Repository details validation
- Navigation and file rendering
- Metadata and stats verification

### API Tests
- Repository details
- Contents API
- Error handling
- Rate limit headers

## Logging & Reporting
- Console and file logging
- HTML test report generation

## Test Execution

### Python
```bash
pytest --headed --slowmo=500 --html=report.html
```

### JavaScript
```bash
npx playwright test --headed
```

## Critical Requirements
- Browser must be visible (headless = false)
- slow_mo = 500
- Tests must run successfully before submission

there is no spoon

## Final Note
The goal is to write tests as if GitHub were your own product.

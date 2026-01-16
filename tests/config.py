"""
Configuration for tests.
"""
import os

# URLs for testing
GITHUB_BASE_URL = "https://github.com"
GITHUB_API_BASE_URL = "https://api.github.com"

# Test repositories
TEST_REPO_OWNER = "microsoft"
TEST_REPO_NAME = "vscode"
TEST_REPO_URL = f"{GITHUB_BASE_URL}/{TEST_REPO_OWNER}/{TEST_REPO_NAME}"

# API test repositories
API_TEST_OWNER = "facebook"
API_TEST_REPO = "react"
API_NONEXISTENT_REPO = "microsoft/nonexistent-repo-12345"

# Browser configuration
BROWSER_CONFIG = {
    "headless": False,
    "slow_mo": 500,
}

# Logging configuration
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "tests.log")

# Create logs directory if needed
os.makedirs(LOG_DIR, exist_ok=True)

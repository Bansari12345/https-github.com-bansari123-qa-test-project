"""
API Tests for GitHub Public API.
"""
import pytest
import requests
from loguru import logger
from config import GITHUB_API_BASE_URL, API_TEST_OWNER, API_TEST_REPO, API_NONEXISTENT_REPO


pytestmark = pytest.mark.api


class TestGitHubAPI:
    """Tests for GitHub REST API endpoints."""

    def test_get_react_repository_success(self):
        """Test GET /repos/facebook/react endpoint returns 200 with correct data."""
        endpoint = f"{GITHUB_API_BASE_URL}/repos/{API_TEST_OWNER}/{API_TEST_REPO}"
        logger.info(f"Making GET request to: {endpoint}")
        
        response = requests.get(endpoint)
        logger.info(f"Response status code: {response.status_code}")
        
        # Verify status code is 200
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        logger.info("✓ Status code is 200")
        
        # Parse JSON response
        data = response.json()
        
        # Verify repository name
        logger.info(f"Verifying repository name is '{API_TEST_REPO}'")
        assert data["name"] == API_TEST_REPO, f"Expected name '{API_TEST_REPO}', got '{data['name']}'"
        logger.info(f"✓ Repository name verified: {data['name']}")
        
        # Verify owner login
        logger.info(f"Verifying owner login is '{API_TEST_OWNER}'")
        assert data["owner"]["login"] == API_TEST_OWNER, f"Expected owner '{API_TEST_OWNER}', got '{data['owner']['login']}'"
        logger.info(f"✓ Owner login verified: {data['owner']['login']}")
        
        # Verify stargazers count > 100,000
        stargazers_count = data["stargazers_count"]
        logger.info(f"Stargazers count: {stargazers_count:,}")
        assert stargazers_count > 100000, f"Expected >100,000 stars, got {stargazers_count:,}"
        logger.info(f"✓ Star count is greater than 100,000: {stargazers_count:,}")
        
        # Verify repository is not private
        is_private = data["private"]
        logger.info(f"Repository private status: {is_private}")
        assert is_private is False, f"Expected private=False, got {is_private}"
        logger.info("✓ Repository is public (private=False)")

    def test_get_react_repository_contents(self):
        """Test GET /repos/facebook/react/contents endpoint returns array with files."""
        endpoint = f"{GITHUB_API_BASE_URL}/repos/{API_TEST_OWNER}/{API_TEST_REPO}/contents"
        logger.info(f"Making GET request to: {endpoint}")
        
        response = requests.get(endpoint)
        logger.info(f"Response status code: {response.status_code}")
        
        # Verify status code is 200
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        logger.info("✓ Status code is 200")
        
        # Parse JSON response
        data = response.json()
        
        # Verify response is an array
        logger.info(f"Verifying response is an array")
        assert isinstance(data, list), f"Expected list/array, got {type(data)}"
        logger.info(f"✓ Response is an array with {len(data)} items")
        
        # Get list of file names
        file_names = [item["name"] for item in data]
        logger.info(f"Files found: {', '.join(file_names[:10])}...")
        
        # Verify README.md exists
        logger.info("Checking for README.md")
        assert "README.md" in file_names, "README.md not found in repository contents"
        logger.info("✓ README.md found in contents")
        
        # Verify package.json exists
        logger.info("Checking for package.json")
        assert "package.json" in file_names, "package.json not found in repository contents"
        logger.info("✓ package.json found in contents")

    def test_get_nonexistent_repository_404(self):
        """Test GET request for nonexistent repository returns 404."""
        endpoint = f"{GITHUB_API_BASE_URL}/repos/{API_NONEXISTENT_REPO}"
        logger.info(f"Making GET request to nonexistent repo: {endpoint}")
        
        response = requests.get(endpoint)
        logger.info(f"Response status code: {response.status_code}")
        
        # Verify status code is 404
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        logger.info("✓ Status code is 404 for nonexistent repository")
        
        # Parse JSON response
        data = response.json()
        
        # Verify error message contains "Not Found"
        error_message = data.get("message", "")
        logger.info(f"Error message: {error_message}")
        assert "Not Found" in error_message, f"Expected 'Not Found' in message, got '{error_message}'"
        logger.info("✓ Error message contains 'Not Found'")

    def test_rate_limit_headers_present(self):
        """Test rate limit headers are present in API response."""
        endpoint = f"{GITHUB_API_BASE_URL}/repos/{API_TEST_OWNER}/{API_TEST_REPO}"
        logger.info(f"Making GET request to check rate limit headers: {endpoint}")
        
        response = requests.get(endpoint)
        logger.info(f"Response status code: {response.status_code}")
        
        headers = response.headers
        
        # Verify X-RateLimit-Limit header exists
        logger.info("Checking for X-RateLimit-Limit header")
        assert "X-RateLimit-Limit" in headers, "X-RateLimit-Limit header not found"
        rate_limit = headers["X-RateLimit-Limit"]
        logger.info(f"✓ X-RateLimit-Limit header found: {rate_limit}")
        
        # Verify X-RateLimit-Remaining header exists
        logger.info("Checking for X-RateLimit-Remaining header")
        assert "X-RateLimit-Remaining" in headers, "X-RateLimit-Remaining header not found"
        rate_remaining = headers["X-RateLimit-Remaining"]
        logger.info(f"✓ X-RateLimit-Remaining header found: {rate_remaining}")
        
        logger.info(f"Rate limit info - Limit: {rate_limit}, Remaining: {rate_remaining}")

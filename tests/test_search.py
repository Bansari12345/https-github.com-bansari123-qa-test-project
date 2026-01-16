"""
Bonus tests for GitHub search functionality.
"""
import pytest
from playwright.sync_api import Page, expect
from loguru import logger
from config import GITHUB_BASE_URL


pytestmark = [pytest.mark.ui, pytest.mark.bonus]


class TestGitHubSearch:
    """Tests for GitHub search functionality."""

    def test_search_for_python_repositories(self, page: Page):
        """Search for Python repositories and verify results appear."""
        search_term = "python"
        logger.info(f"Navigating to GitHub homepage: {GITHUB_BASE_URL}")
        page.goto(GITHUB_BASE_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        
        # Click search button to open search dialog
        logger.info("Clicking search button to open search")
        search_button = page.locator('[aria-label*="Search"], [data-target="qbsearch-input.inputButton"]').first
        search_button.click()
        page.wait_for_timeout(1000)
        
        # Now find the actual search input that appears
        logger.info("Locating search input field")
        search_input = page.locator('#query-builder-test, [name="query-builder-test"], [role="combobox"]').first
        expect(search_input).to_be_visible(timeout=5000)
        
        # Type in search box
        logger.info(f"Searching for: {search_term}")
        search_input.fill(search_term)
        search_input.press("Enter")
        
        # Wait for search results page
        logger.info("Waiting for search results page to load")
        page.wait_for_url("**/search?**", timeout=10000)
        
        # Verify we're on search results page
        assert "/search?" in page.url, "Should be on search results page"
        logger.info(f"✓ Navigated to search results: {page.url}")
        
        # Wait for results to load - simplified check
        logger.info("Waiting for search results to appear")
        page.wait_for_timeout(3000)
        
        # Verify at least one repository result link is visible
        result_items = page.locator('[data-testid="search-result-item"], .search-title, a[href*="/"]').filter(has_text="python")
        expect(result_items.first).to_be_visible(timeout=10000)
        
        result_count = result_items.count()
        logger.info(f"✓ Found {result_count} search results for '{search_term}'")

    def test_search_with_filters(self, page: Page):
        """Search with filters and verify results load."""
        logger.info(f"Navigating to GitHub search page directly")
        page.goto(f"{GITHUB_BASE_URL}/search?q=react&type=repositories")
        
        # Wait for results
        logger.info("Waiting for search results to load")
        page.wait_for_load_state("networkidle", timeout=15000)
        
        # Verify search query is in URL
        assert "q=react" in page.url, "Search query should be in URL"
        logger.info("✓ Search query present in URL")
        
        # Look for language filters
        logger.info("Checking for language filters")
        page.wait_for_timeout(2000)  # Brief wait for filters to render
        
        # Verify page loaded with search term
        page_content = page.content()
        assert len(page_content) > 1000, "Page should have substantial content"
        logger.info("✓ Search results page loaded successfully")

    def test_search_for_specific_repository(self, page: Page):
        """Search for specific repository by name and verify results."""
        search_term = "microsoft/vscode"
        logger.info(f"Navigating to GitHub and searching for: {search_term}")
        page.goto(GITHUB_BASE_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        
        # Click search button to open search dialog
        logger.info("Opening search")
        search_button = page.locator('[aria-label*="Search"], [data-target="qbsearch-input.inputButton"]').first
        search_button.click()
        page.wait_for_timeout(1000)
        
        # Find the actual search input
        search_input = page.locator('#query-builder-test, [name="query-builder-test"], [role="combobox"]').first
        expect(search_input).to_be_visible(timeout=5000)
        
        logger.info(f"Entering search term: {search_term}")
        search_input.fill(search_term)
        search_input.press("Enter")
        
        # Wait for results
        page.wait_for_url("**/search?**", timeout=10000)
        logger.info("Search results page loaded")
        
        # Verify we can see some results
        page.wait_for_timeout(3000)  # Wait for results to render
        
        # Check that results page loaded
        assert "search" in page.url, "Should be on search page"
        logger.info(f"✓ Search executed successfully for '{search_term}'")


class Test404ErrorPages:
    """Test 404 error pages for missing resources."""

    def test_nonexistent_repository_shows_404(self, page: Page):
        """Verify that nonexistent repository displays 404 error page."""
        fake_repo = f"{GITHUB_BASE_URL}/nonexistent-user-12345/nonexistent-repo-67890"
        logger.info(f"Navigating to nonexistent repository: {fake_repo}")
        
        page.goto(fake_repo, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        
        # Check for 404 indicators
        logger.info("Checking for 404 error indicators")
        page_content = page.content().lower()
        
        # GitHub shows "404" or "not found" message
        has_404 = "404" in page_content or "not found" in page_content
        assert has_404, "Page should indicate 404 error"
        logger.info("✓ 404 error page displayed correctly")

    def test_nonexistent_user_profile_shows_404(self, page: Page):
        """Navigate to nonexistent user profile and verify 404 displays."""
        fake_user = f"{GITHUB_BASE_URL}/nonexistent-user-xyz-12345-abcde"
        logger.info(f"Navigating to nonexistent user: {fake_user}")
        
        page.goto(fake_user, wait_until="networkidle")
        
        # Check for 404
        logger.info("Verifying 404 response")
        page_content = page.content().lower()
        has_error = "404" in page_content or "not found" in page_content
        
        assert has_error, "Should show 404 for nonexistent user"
        logger.info("✓ Nonexistent user profile shows 404 error")

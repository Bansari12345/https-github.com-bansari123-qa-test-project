"""
UI Tests for GitHub Repository Pages.
Tests the microsoft/vscode repository with comprehensive validation.
"""
import pytest
from playwright.sync_api import Page, expect
from loguru import logger
from config import TEST_REPO_URL, TEST_REPO_OWNER, TEST_REPO_NAME
from helpers import PageHelper, log_test_step, extract_number_from_text, verify_url_contains


pytestmark = pytest.mark.ui


class TestRepositoryPage:
    """Tests for repository page basic information and display."""

    def test_repository_loads_and_displays_basic_info(self, page: Page):
        """Verify repository page loads with correct name and owner."""
        helper = PageHelper(page)
        log_test_step("Load repository page and verify basic information")
        
        helper.navigate_and_wait(TEST_REPO_URL)
        
        # Verify repository name
        logger.info(f"Verifying repository name: {TEST_REPO_NAME}")
        repo_name = helper.verify_element_visible('a[data-testid="repository-name-link"], strong a[href="/microsoft/vscode"]')
        helper.verify_text_contains(repo_name, TEST_REPO_NAME)
        
        # Verify owner name
        logger.info(f"Verifying owner: {TEST_REPO_OWNER}")
        owner = helper.verify_element_visible('a[href="/microsoft"]')
        helper.verify_text_contains(owner, TEST_REPO_OWNER)
        
        logger.info("✓ Repository name and owner verified")

    def test_star_count_visible_and_significant(self, page: Page):
        """Verify star count is visible and exceeds 100k."""
        helper = PageHelper(page)
        log_test_step("Check repository star count")
        
        helper.navigate_and_wait(TEST_REPO_URL)
        
        star_button = helper.verify_element_visible('#repo-stars-counter-star')
        star_text = star_button.inner_text()
        star_count = extract_number_from_text(star_text)
        
        logger.info(f"Star count: {star_count:,}")
        assert star_count > 100000, f"Expected >100k stars, got {star_count:,}"
        logger.info("✓ Star count exceeds 100k")

    def test_fork_count_visible(self, page: Page):
        """Verify fork count is displayed."""
        helper = PageHelper(page)
        log_test_step("Check repository fork count")
        
        helper.navigate_and_wait(TEST_REPO_URL)
        
        fork_element = helper.verify_element_visible('#repo-network-counter')
        fork_text = fork_element.inner_text()
        fork_count = extract_number_from_text(fork_text)
        
        logger.info(f"Fork count: {fork_count:,}")
        assert fork_count > 0, "Fork count should be greater than 0"
        logger.info("✓ Fork count verified")

    def test_readme_content_rendered(self, page: Page):
        """Verify README markdown is properly rendered as HTML."""
        helper = PageHelper(page)
        log_test_step("Check README content rendering")
        
        helper.navigate_and_wait(TEST_REPO_URL)
        
        readme_section = helper.verify_element_visible('article[itemprop="text"]')
        readme_html = readme_section.inner_html()
        
        logger.info(f"README HTML length: {len(readme_html)} characters")
        assert len(readme_html) > 100, "README content should be substantial"
        assert any(tag in readme_html for tag in ['<h1', '<h2', '<p>', '<a']), \
            "README should contain rendered HTML elements"
        
        logger.info("✓ README content properly rendered")


class TestCodeNavigation:
    """Tests for navigating through repository folders and files."""

    def test_navigate_to_src_folder(self, page: Page):
        """Verify navigation to src folder works correctly."""
        helper = PageHelper(page)
        log_test_step("Navigate to src folder")
        
        helper.navigate_and_wait(TEST_REPO_URL)
        page.wait_for_timeout(2000)
        
        # Navigate directly to src folder
        logger.info("Navigating to src folder")
        page.goto(f"{TEST_REPO_URL}/tree/main/src")
        page.wait_for_url("**/src", timeout=10000)
        
        verify_url_contains(page, "/src")
        
        page_content = page.content()
        assert "src" in page_content, "Page should show src directory content"
        logger.info("✓ Successfully navigated to src folder")

    def test_navigate_to_typescript_file_with_line_numbers(self, page: Page):
        """Verify TypeScript file displays with line numbers and syntax highlighting."""
        helper = PageHelper(page)
        log_test_step("Navigate to TypeScript file and verify display")
        
        # Navigate to vs folder
        logger.info("Navigating to src/vs folder")
        page.goto(f"{TEST_REPO_URL}/tree/main/src/vs")
        page.wait_for_timeout(3000)
        
        # Get first TypeScript file
        logger.info("Finding TypeScript file")
        ts_file_link = page.locator('a[href*=".ts"]').first
        ts_href = ts_file_link.get_attribute('href')
        page.goto(f"https://github.com{ts_href}")
        page.wait_for_timeout(3000)
        
        # Verify line numbers
        logger.info("Verifying line numbers displayed")
        line_numbers = helper.verify_element_visible('[data-line-number], .blob-num, td.blob-num')
        
        # Verify code content
        logger.info("Verifying code content displayed")
        code_content = helper.verify_element_visible('td.blob-code, .blob-code, .react-code-text')
        
        # Verify syntax highlighting container
        logger.info("Verifying syntax highlighting present")
        code_container = helper.verify_element_visible('[role="presentation"], .react-code-lines, .blob-wrapper', timeout=5000)
        
        logger.info("✓ TypeScript file displays correctly with line numbers and syntax highlighting")


class TestRepositoryMetadata:
    """Tests for repository metadata like description, license, and topics."""

    def test_about_section_has_description(self, page: Page):
        """Verify About section contains repository description."""
        helper = PageHelper(page)
        log_test_step("Check About section description")
        
        helper.navigate_and_wait(TEST_REPO_URL)
        
        about_section = helper.verify_element_visible('div.BorderGrid-cell:has-text("About")')
        description = about_section.locator('p').first
        expect(description).to_be_visible()
        
        description_text = description.inner_text()
        assert len(description_text) > 10, "Description should be meaningful"
        logger.info(f"✓ About section has description: {description_text[:50]}...")

    def test_license_information_displayed(self, page: Page):
        """Verify license information is displayed."""
        helper = PageHelper(page)
        log_test_step("Check license information")
        
        helper.navigate_and_wait(TEST_REPO_URL)
        page.wait_for_timeout(2000)
        
        license_element = page.locator('a[href*="LICENSE"], a:has-text("MIT License"), [aria-label*="License"]').first
        license_text = license_element.text_content(timeout=10000)
        
        logger.info(f"License found: {license_text}")
        assert len(license_text) > 0, "License information should not be empty"
        logger.info(f"✓ License displayed: {license_text}")

    def test_topics_tags_visible(self, page: Page):
        """Verify repository topics/tags are visible."""
        helper = PageHelper(page)
        log_test_step("Check repository topics/tags")
        
        helper.navigate_and_wait(TEST_REPO_URL)
        
        # Find topics in About section - they may have different selectors
        topics = page.locator('a[data-octo-click="topic"]').or_(page.locator('a[href*="/topics/"]'))
        
        topic_count = topics.count()
        logger.info(f"Found {topic_count} topics")
        assert topic_count > 0, "Repository should have at least one topic"
        
        first_topic = topics.first.inner_text()
        logger.info(f"✓ Topics visible, first topic: {first_topic}")

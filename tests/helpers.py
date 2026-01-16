"""
Helper functions for tests - reusable utilities following DRY principles.
Provides common functionality for page navigation, element interaction, and data extraction.
"""
from typing import Optional
from loguru import logger
from playwright.sync_api import Page, Locator, expect
import re


class PageHelper:
    """Helper class for common page operations."""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate_and_wait(self, url: str, timeout: int = 10000) -> None:
        """
        Navigate to URL and wait for page to be ready.
        
        Args:
            url: URL to navigate to
            timeout: Maximum wait time in milliseconds
        """
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_timeout(3000)  # Wait for dynamic content
        logger.info("✓ Page loaded successfully")
    
    def get_element(self, selector: str, timeout: int = 10000) -> Locator:
        """
        Get element with logging and timeout.
        
        Args:
            selector: CSS selector for element
            timeout: Maximum wait time
            
        Returns:
            Locator object
        """
        logger.debug(f"Locating element: {selector}")
        return self.page.locator(selector).first
    
    def verify_element_visible(self, selector: str, timeout: int = 10000) -> Locator:
        """
        Verify element is visible with explicit logging.
        
        Args:
            selector: CSS selector for element
            timeout: Maximum wait time
            
        Returns:
            Locator object if visible
        """
        element = self.get_element(selector)
        expect(element).to_be_visible(timeout=timeout)
        logger.debug(f"✓ Element visible: {selector}")
        return element
    
    def verify_text_contains(self, element: Locator, expected_text: str) -> None:
        """
        Verify element contains expected text with logging.
        
        Args:
            element: Element to check
            expected_text: Text that should be present
        """
        expect(element).to_contain_text(expected_text)
        logger.debug(f"✓ Text verified: '{expected_text}'")


def wait_for_github_page_load(page: Page, timeout: int = 10000) -> None:
    """
    Wait for GitHub page to fully load.
    
    Args:
        page: Playwright page object
        timeout: Maximum wait time in milliseconds
    """
    logger.info(f"Waiting for page load (timeout: {timeout}ms)")
    try:
        page.wait_for_load_state("domcontentloaded", timeout=timeout)
        page.wait_for_timeout(2000)
        logger.info("✓ Page loaded successfully")
    except Exception as e:
        logger.warning(f"Page load timeout: {e}")
        # Continue anyway


def safe_get_text(page: Page, selector: str, default: str = "") -> str:
    """
    Safely get text content from element with error handling.
    
    Args:
        page: Playwright page object
        selector: CSS selector for element
        default: Default value if element not found
    
    Returns:
        Text content of element or default value
    """
    try:
        element = page.locator(selector).first
        if element.is_visible(timeout=5000):
            text = element.inner_text()
            logger.debug(f"Got text from '{selector}': {text[:50]}...")
            return text
        logger.warning(f"Element '{selector}' not visible, returning default")
        return default
    except Exception as e:
        logger.warning(f"Could not get text from '{selector}': {e}")
        return default


def extract_number_from_text(text: str) -> int:
    """
    Extract number from GitHub-formatted text (e.g., "160k", "1,234").
    
    Args:
        text: Text containing number
    
    Returns:
        Integer value extracted, 0 if parsing fails
    """
    text = text.strip().lower()
    logger.debug(f"Extracting number from: {text}")
    
    try:
        # Handle "k" suffix (e.g., "160k" -> 160000)
        if 'k' in text:
            number_str = re.findall(r'[\d.]+', text)[0]
            number = int(float(number_str) * 1000)
            logger.debug(f"Parsed 'k' format: {number}")
            return number
        
        # Handle comma-separated (e.g., "1,234" -> 1234)
        number_str = text.replace(',', '')
        number_match = re.findall(r'\d+', number_str)
        if number_match:
            number = int(number_match[0])
            logger.debug(f"Parsed number: {number}")
            return number
        
        logger.warning(f"Could not parse number from: {text}")
        return 0
    except Exception as e:
        logger.error(f"Error parsing number from '{text}': {e}")
        return 0


def log_test_step(step_description: str) -> None:
    """
    Log test step with enhanced visibility for debugging.
    
    Args:
        step_description: Description of test step
    """
    logger.info(f">>> STEP: {step_description}")


def verify_url_contains(page: Page, expected_path: str) -> None:
    """
    Verify current URL contains expected path.
    
    Args:
        page: Playwright page object
        expected_path: Path that should be in URL
    """
    current_url = page.url
    assert expected_path in current_url, f"Expected '{expected_path}' in URL, got: {current_url}"
    logger.info(f"✓ URL verified contains: {expected_path}")

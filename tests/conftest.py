"""
Pytest configuration and fixtures for test setup.
"""
import pytest
from playwright.sync_api import Browser, BrowserContext, Page
from loguru import logger
import sys
from config import BROWSER_CONFIG, LOG_FILE


# Configure loguru logger
logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
logger.add(LOG_FILE, format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}", rotation="10 MB")


def pytest_addoption(parser):
    """Add command line options for browser selection."""
    parser.addoption(
        "--browser-name",
        action="store",
        default="chromium",
        help="Browser to run tests on: chromium, firefox, or webkit",
        choices=["chromium", "firefox", "webkit"],
    )


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context with viewport size."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch arguments for visible testing."""
    logger.info("Configuring browser launch arguments")
    return {
        **browser_type_launch_args,
        **BROWSER_CONFIG,
        "args": ["--start-maximized", "--disable-blink-features=AutomationControlled"],
    }


@pytest.fixture(scope="function")
def context(browser: Browser, browser_context_args):
    """Create a new browser context for each test."""
    context = browser.new_context(**browser_context_args)
    yield context
    try:
        context.close()
    except Exception:
        pass


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create a new page for each test."""
    page = context.new_page()
    yield page
    try:
        page.close()
    except Exception:
        pass


def pytest_runtest_setup(item):
    """Log test start."""
    logger.info(f"========== Starting test: {item.nodeid} ==========")


def pytest_runtest_teardown(item, nextitem):
    """Log test completion."""
    logger.info(f"========== Finished test: {item.nodeid} ==========\n")

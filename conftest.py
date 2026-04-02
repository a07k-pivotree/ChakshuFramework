# conftest.py — root level
# This file runs automatically before any test.
# It sets up: browser fixture, base URL config, logger, allure environment.

import os
import pytest
from dotenv import load_dotenv
from utils.logger import setup_logger, get_logger

load_dotenv()


class Config:
    BASE_URL = os.getenv("BASE_URL")


# ── Session-scoped: runs ONCE for the entire pytest session ───────────────────
@pytest.fixture(scope="session", autouse=True)
def initialize_logger(request):
    """
    Automatically initializes the logger at the start of every test session.
    Detects the test module name from the first collected test item.
    autouse=True means you never need to call this manually.
    """
    # Get the name of the test file being run (e.g. "test_login" or "test_favourites")
    # request.config.args contains what was passed to pytest on the command line
    test_args = request.config.args
    if test_args:
        # Extract just the filename without path and .py extension
        raw = os.path.basename(test_args[0])
        module_name = os.path.splitext(raw)[0]  # "test_favourites"
    else:
        module_name = "test_run"

    logger = setup_logger(module_name)
    logger.info("=" * 60)
    logger.info(f"Test session started — module: {module_name}")
    logger.info(f"Base URL: {Config.BASE_URL}")
    logger.info("=" * 60)

    yield  # tests run here

    logger.info("=" * 60)
    logger.info("Test session ended")
    logger.info("=" * 60)


# ── Function-scoped: runs before and after EACH test function ─────────────────
@pytest.fixture(autouse=True)
def log_test_boundaries(request):
    """
    Automatically logs the start and end of every individual test.
    autouse=True means it applies to every test without being called.
    """
    logger = get_logger()
    logger.info(f">>> START: {request.node.name}")
    yield
    logger.info(f">>> END:   {request.node.name}")
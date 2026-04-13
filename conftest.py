# conftest.py — root level
# This file runs automatically before any test.
# It sets up: browser fixture, base URL config, logger, allure environment.

import os
import allure
import pytest
from datetime import datetime
from dotenv import load_dotenv
from utils.excel_reader import ExcelDataReader
from utils.logger import setup_logger, get_logger

load_dotenv()


class Config:
    BASE_URL = os.getenv("BASE_URL")


@pytest.fixture(scope="session")
def excel_data_reader():
    return ExcelDataReader()


@pytest.fixture(scope="session")
def login_data(excel_data_reader):
    return excel_data_reader.get_login_data()


@pytest.fixture(scope="session")
def product_data(excel_data_reader):
    return excel_data_reader.get_products()


@pytest.fixture(scope="session")
def cart_products(excel_data_reader):
    return excel_data_reader.get_products(limit=3)


# ── Session-scoped: runs ONCE for the entire pytest session ───────────────────
@pytest.fixture(scope="session", autouse=True)
def initialize_logger(request):
    test_args = request.config.args
    if test_args:
        raw = os.path.basename(test_args[0])
        module_name = os.path.splitext(raw)[0]
    else:
        module_name = "test_run"

    logger = setup_logger(module_name)
    logger.info("=" * 60)
    logger.info(f"Test session started — module: {module_name}")
    logger.info(f"Base URL: {Config.BASE_URL}")
    logger.info("=" * 60)

    yield

    logger.info("=" * 60)
    logger.info("Test session ended")
    logger.info("=" * 60)


# ── Function-scoped: runs before and after EACH test function ─────────────────
@pytest.fixture(autouse=True)
def log_test_boundaries(request):
    logger = get_logger()
    logger.info(f">>> START: {request.node.name}")
    yield
    logger.info(f">>> END:   {request.node.name}")


# ── Page fixture — stores page object so failure hook can access it ───────────
@pytest.fixture(autouse=True)
def attach_page_to_request(request, page):
    request.node._page = page
    yield


# ── Failure hook — runs after EACH test phase (setup/call/teardown) ───────────
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Automatically runs after every test.
    If the test FAILED during the 'call' phase:
      1. Takes a screenshot and saves to screenshots/failures/
      2. Logs the failure reason + screenshot path in the log file
      3. Attaches the screenshot to Allure report
      4. Attaches the full log file to Allure report
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        logger = get_logger()
        page = getattr(item, "_page", None)

        # ── Build timestamp and safe test name ────────────────────────────────
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_test_name = item.name.replace("[", "_").replace("]", "").replace(" ", "_")

        # ── Screenshot ────────────────────────────────────────────────────────
        screenshot_path = None
        if page:
            screenshot_filename = f"{timestamp}_{safe_test_name}.png"
            screenshots_dir = os.path.join(
                os.path.dirname(__file__), "screenshots", "failures"
            )
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, screenshot_filename)
            page.screenshot(path=screenshot_path, full_page=True)

        # ── Log the failure ───────────────────────────────────────────────────
        logger.error("!" * 60)
        logger.error(f"FAILED: {item.name}")

        if hasattr(report.longrepr, "reprcrash"):
            failure_reason = report.longrepr.reprcrash.message
            failure_line   = report.longrepr.reprcrash.lineno
            failure_file   = report.longrepr.reprcrash.path
            logger.error(f"Reason:   {failure_reason}")
            logger.error(f"Location: {failure_file} — line {failure_line}")
        else:
            logger.error(f"Reason: {report.longrepr}")

        if screenshot_path:
            logger.error(f"Screenshot: {screenshot_path}")
        logger.error("!" * 60)

        # ── Attach screenshot to Allure ───────────────────────────────────────
        # This makes the screenshot appear inside the Allure report
        # under the Attachments tab of the failed test
        if screenshot_path and os.path.exists(screenshot_path):
            with open(screenshot_path, "rb") as f:
                allure.attach(
                    f.read(),
                    name=f"Failure screenshot — {safe_test_name}",
                    attachment_type=allure.attachment_type.PNG
                )

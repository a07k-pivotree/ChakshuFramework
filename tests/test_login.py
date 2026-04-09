import re

from playwright.sync_api import expect

from conftest import Config
from pages.login.login_page import LoginPage
from utils.screenshot_helper import ScreenshotHelper


def test_bstackdemo_login(page, login_data):
    page.goto(Config.BASE_URL)

    login_page = LoginPage(page)
    login_page.click_sign_in_menu()
    login_page.select_username(login_data.username)
    login_page.select_password(login_data.password)
    login_page.click_login()

    expect(login_page.get_logout()).to_be_visible()
    expected_url_pattern = re.escape(login_data.expected_url_after_login.rstrip("/")) + r"/?$"
    expect(page).to_have_url(re.compile(expected_url_pattern))
    ScreenshotHelper.take_validation_screenshot(page, "Login_Success")

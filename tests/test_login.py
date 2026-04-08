from playwright.sync_api import expect

from conftest import Config
from pages.login.login_page import LoginPage
from utils.screenshot_helper import ScreenshotHelper


def test_bstackdemo_login(page):
    # Navigation
    page.goto(Config.BASE_URL)

    # Initialize page object
    login_page = LoginPage(page)

    #action
    login_page.click_sign_in_menu()
    login_page.select_username("demouser")
    login_page.select_password("testingisfun99")
    login_page.click_login()

    # Validate
    expect(login_page.get_logout()).to_be_visible()
    ScreenshotHelper.take_validation_screenshot(page, "Login_Success")

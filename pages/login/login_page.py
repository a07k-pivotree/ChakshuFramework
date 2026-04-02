# Include functions for the login page
from pages.login.locator_login_page import LoginLocators
from utils.logger import get_logger

logger = get_logger()

class LoginPage:
    def __init__(self, page):
        self.page = page

    def click_sign_in_menu(self):
        logger.info("Action: clicking 'Sign In' menu link")
        self.page.locator(LoginLocators.sign_in_link).click()

    def select_username(self, username):
        logger.info(f"Action: selecting username — '{username}'")
        self.page.locator(LoginLocators.username_dropdown).click()
        self.page.locator(LoginLocators.username_option(username)).click()

    def select_password(self, password):
        # Note: We usually log that we are entering a password, but not the password itself if it's sensitive.
        # Since these are dropdown options (likely for test environments), logging is fine here.
        logger.info(f"Action: selecting password option for user")
        self.page.locator(LoginLocators.password_dropdown).click()
        self.page.locator(LoginLocators.password_option(password)).click()

    def click_login(self):
        logger.info("Action: clicking the Login button")
        self.page.locator(LoginLocators.login_button).click()

    def get_logout(self):
        logger.info("Check: verifying if logout link is present (login status)")
        return self.page.locator(LoginLocators.logout_link)
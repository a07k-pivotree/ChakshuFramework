# Include function for the
from pages.login.locator_login_page import LoginLocators

class LoginPage:
    def __int__(self,page):
        self.page = page

    def click_sign_in_menue(self):
        self.page.locator(LoginLocators.sign_in_link()).click()

    def select_username(self,username):
        self.page.locator(LoginLocators.username_dropdown()).click()
        self.page.locator(LoginLocators.username_option(username)).click()


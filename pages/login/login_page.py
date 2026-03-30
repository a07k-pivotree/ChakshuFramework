# Include function for the
from pages.login.locator_login_page import LoginLocators
class LoginPage:
    def __init__(self,page):
        self.page = page

    def click_sign_in_menu(self):
        self.page.locator(LoginLocators.sign_in_link).click()

    def select_username(self,username):
        self.page.locator(LoginLocators.username_dropdown).click()
        self.page.locator(LoginLocators.username_option(username)).click()

    def select_password(self,password):
        self.page.locator(LoginLocators.password_dropdown).click()
        self.page.locator(LoginLocators.password_option(password)).click()

    def click_login(self):
        self.page.locator(LoginLocators.login_button).click()

    def get_logout(self):
        return self.page.locator(LoginLocators.logout_link)


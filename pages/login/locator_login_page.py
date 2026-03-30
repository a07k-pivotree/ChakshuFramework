# This file contain path of elements

class LoginLocators:
    sign_in_link = "//nav//span[text()='Sign In']"
    username_dropdown = "div#username"
    password_dropdown = "div#password"
    login_button = "#login-btn"
    logout_link = "//nav//span[text()='Logout']"

    @staticmethod
    def username_option(username_text):
        return f"div:text-is('{username_text}')"

    @staticmethod
    def password_option(password_text):
        return f"div:text-is('{password_text}')"
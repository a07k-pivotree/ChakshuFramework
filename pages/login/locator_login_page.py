# This file contain path of elements

class LoginLocators:
    @staticmethod
    def sign_in_link():
        return "//nav//span[text()='Sign In']"

    @staticmethod
    def username_dropdown():
        return "div#username"

    @staticmethod
    def username_option(username_text):
        return f"div:has-text('{username_text}')"

    @staticmethod
    def password_dropdown():
        return "div#password"

    @staticmethod
    def password_option(password_text):
        return f"div:has-text('{password_text}')"

    @staticmethod
    def login_button():
        return "#login-btn"

    @staticmethod
    def logout_link():
        return "//nav//span[text()='Logout']"
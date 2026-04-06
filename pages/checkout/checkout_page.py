from pages.checkout.locator_checkout_page import CheckoutLocators
from pages.home.home_page import logger


class CheckoutPage:
    def __init__(self, page):
        self.page = page

    def fill_shipping_details(self, first_name, last_name, address, province, post_code):

        logger.info("Action: filling shipping details")
        logger.info(f"First Name: {first_name}")
        self.page.locator(CheckoutLocators.first_name_input).fill(first_name)
        logger.info(f"Last Name: {last_name}")
        self.page.locator(CheckoutLocators.last_name_input).fill(last_name)
        logger.info(f"Address: {address}")
        self.page.locator(CheckoutLocators.address_input).fill(address)
        logger.info(f"Province: {province}")
        self.page.locator(CheckoutLocators.province_input).fill(province)
        logger.info(f"Postcode: {post_code}")
        self.page.locator(CheckoutLocators.post_code_input).fill(post_code)

    def click_submit(self):
        logger.info("Action: clicking submit")
        self.page.locator(CheckoutLocators.submit_buton).click()

    #  Methods to return locators for assertions in our tests  #

    def get_order_confirmation(self):
        logger.info("Action: getting order confirmation")
        return self.page.locator(CheckoutLocators.order_confirmation)

    def get_cart_items(self):
        logger.info("Action: getting cart items")
        return self.page.locator(CheckoutLocators.cart_items)

    def get_total_displayed_text(self):
        logger.info("Action: getting total displayed text")
        return self.page.locator(CheckoutLocators.total_displayed).inner_text().strip()

    def get_calculated_total_of_items(self):
        logger.info("Action: getting calculated total text")
        #Loops through all items in the cart and adds up their individual prices
        cart_items = self.get_cart_items()
        cart_items.first.wait_for(state="visible")

        total_calculated = 0.0
        for i in range(cart_items.count()):
            # Get the text, remove the $ sign, and convert to a float
            price_text = cart_items.nth(i).locator("xpath=./div/div[2]/div").inner_text().strip()
            total_calculated += float(price_text.replace("$", "").strip())

        return round(total_calculated, 2)

    def get_displayed_total_value(self):
        logger.info("Action: getting displayed total value")
        #Gets the total displayed at the bottom and converts it to a clean float.
        total_text = self.get_total_displayed_text()
        total_displayed = float(total_text.replace("$", "").strip())
        return round(total_displayed, 2)

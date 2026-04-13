from playwright.sync_api import expect

from pages.home.locator_home_page import HomeLocators
from utils.logger import get_logger

logger = get_logger()



class HomePage:
    def __init__(self,page):
        self.page = page

    def add_product_to_cart(self,product_name):
        logger.info("Action: adding product to cart")
        self.page.locator(HomeLocators.add_to_cart_btn(product_name)).first.click()

    def close_cart(self):
        logger.info("Action: closing cart")
        self.page.locator(HomeLocators.close_cart_button).click()

    def open_cart(self):
        logger.info("Action: opening cart")
        self.page.locator(HomeLocators.cart_button).click()

    def click_checkout(self):
        logger.info("Action: clicking checkout")
        self.page.locator(HomeLocators.buy_button).click()

    # For Cart
    def get_cart_items(self):
        logger.info("Action: getting cart items")
        return self.page.locator(HomeLocators.cart_items_in_modal)

    def remove_itm_from_cart(self):
        logger.info("Action: removing item from cart")
        cart_item = self.get_cart_items()
        cart_item.first.locator(HomeLocators.delete_item_btn).click()

    def get_item_quantity(self):
        logger.info("Action: getting item quantity")
        quantity_text = self.page.locator(HomeLocators.item_quantity_text).inner_text()
        return int(quantity_text.split(":")[-1].strip())

    def validate_product_details(self, product):
        logger.info(f"Validation: checking website data for product '{product.product_name}'")
        product_card = self.page.locator(HomeLocators.product_card_by_sku(product.sku))
        expect(product_card).to_be_visible()
        expect(product_card).to_contain_text(product.product_name)
        expect(product_card).to_contain_text(product.expected_price)

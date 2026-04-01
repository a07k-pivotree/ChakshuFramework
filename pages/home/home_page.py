from pages.home.locator_home_page import HomeLocators


class HomePage:
    def __init__(self,page):
        self.page = page

    def add_product_to_cart(self,product_name):
        self.page.locator(HomeLocators.add_to_cart_btn(product_name)).first.click()

    def close_cart(self):
        self.page.locator(HomeLocators.close_cart_button).click()

    def open_cart(self):
        self.page.locator(HomeLocators.cart_button).click()

    def click_checkout(self):
        self.page.locator(HomeLocators.buy_button).click()

    # For Cart
    def get_cart_items(self):
        return self.page.locator(HomeLocators.cart_items_in_modal)

    def remove_itm_from_cart(self):
        cart_item = self.get_cart_items()
        cart_item.first.locator(HomeLocators.delete_item_btn).click()

    def get_item_quantity(self):
        quantity_text = self.page.locator(HomeLocators.item_quantity_text).inner_text()
        return int(quantity_text.split(":")[-1].strip())

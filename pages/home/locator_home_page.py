class HomeLocators:
    cart_button = "div.float-cart >span"
    close_cart_button = "div.float-cart__close-btn"
    buy_button = "div.buy-btn"
    cart_items_in_modal = "//div[@class='float-cart__shelf-container']//div[@class='shelf-item']"
    delete_item_btn = ".shelf-item__del"
    item_quantity_text = "//div[@class='shelf-item__details']/p[2]"

    @staticmethod
    def add_to_cart_btn(product_name):
        return f".shelf-item:has-text('{product_name}') >> text=Add to cart"
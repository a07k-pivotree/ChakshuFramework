def add_products(home_page, product):
    for product in product:
        home_page.add_product_to_cart(product)
        home_page.close_cart()
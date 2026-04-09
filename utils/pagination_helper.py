def add_products(home_page, products):
    for product in products:
        product_name = getattr(product, "product_name", product)
        home_page.add_product_to_cart(product_name)
        home_page.close_cart()

# This file contains all locators for the Favourites section

class FavouritesLocators:

    # ── Navigation ────────────────────────────────────────────────────────────
    favourites_nav_link = "a#favourites"

    # ── Favourites page validation ────────────────────────────────────────────
    # Shown when 0 products are in favourites
    zero_products_text = "small.products-found h3"

    # All product cards currently shown on the favourites page
    all_fav_product_cards = "div.shelf-item"

    # All product titles currently shown on the favourites page
    all_fav_product_titles = ".shelf-item__title"

    # ── Product shelf (main listing page) ─────────────────────────────────────
    # Heart icon that is NOT yet clicked (unfilled) — targets by SKU
    @staticmethod
    def unfilled_heart_by_sku(sku):
        return f"div.shelf-item[data-sku='{sku}'] button.MuiIconButton-root"

    # Product card on the main listing page
    @staticmethod
    def product_card_by_sku(sku):
        return f"div.shelf-item[data-sku='{sku}']"

    # Heart icon that IS already clicked (filled) — by SKU, used on fav page
    @staticmethod
    def filled_heart_by_sku(sku):
        # Button WITH 'clicked' class = already favourited
        return f"div.shelf-item[data-sku='{sku}'] button.MuiIconButton-root.clicked"

    # "Add to cart" button for a specific product by SKU
    @staticmethod
    def add_to_cart_by_sku(sku):
        return f"div.shelf-item[data-sku='{sku}'] .shelf-item__buy-btn"

    # ── Cart validation ───────────────────────────────────────────────────────
    # A specific product title inside the cart sidebar
    @staticmethod
    def cart_item_title(title):
        return f".shelf-item__details p.title:text-is('{title}')"

    # Cart item quantity text for a product
    @staticmethod
    def cart_item_quantity(title):
        return f".shelf-item__details:has(p.title:text-is('{title}')) p.desc"

# This file contains path of elements for the Favourites section

class FavouritesLocators:
    # Header navigation link
    favourites_nav_link = "a#favourites"

    # Heart icon button on each product card (unfilled = not yet favourited)
    heart_icon_button = ".shelf-item .MuiIconButton-root"

    # Specific product's heart icon by SKU (data-sku attribute on shelf-item)
    @staticmethod
    def heart_icon_by_sku(sku):
        return f"div.shelf-item[data-sku='{sku}'] .MuiIconButton-root"

    # Product title on the main shelf
    @staticmethod
    def product_title_on_shelf(title):
        return f".shelf-item__title:text-is('{title}')"

    # Product title inside the Favourites page
    @staticmethod
    def product_title_in_favourites(title):
        return f".shelf-item__title:text-is('{title}')"

    # All product titles inside the Favourites page (for counting/validation)
    all_product_titles_in_favourites = ".shelf-item__title"
# This file contains all interaction functions for the Favourites section

from playwright.sync_api import expect

from pages.favourites.locator_favourites_page import FavouritesLocators


class FavouritesPage:

    def __init__(self, page):
        self.page = page

    # ── Navigation ────────────────────────────────────────────────────────────

    def click_favourites_nav(self):
        """Clicks the Favourites link in the header."""
        self.page.locator(FavouritesLocators.favourites_nav_link).click()

    def go_back(self):
        """Goes back to the previous page using browser back."""
        self.page.go_back()
        self.page.wait_for_load_state("domcontentloaded")
        self.page.locator(
            FavouritesLocators.product_card_by_sku("iPhone11-device-info.png")
        ).wait_for(state="visible")

    # ── Favourites page reads ─────────────────────────────────────────────────

    def get_zero_products_message(self):
        """
        Returns the locator for the '0 Product(s) found.' message.
        Used with expect().to_be_visible() to validate empty favourites.
        """
        return self.page.locator(FavouritesLocators.zero_products_text)

    def get_all_favourite_titles(self):
        """
        Returns a Python list of all product title strings on the favourites page.
        Used to count and compare against expected number of favourited products.
        """
        title_elements = self.page.locator(FavouritesLocators.all_fav_product_titles).all()
        return [el.inner_text().strip() for el in title_elements]

    def get_favourites_count(self):
        """
        Returns how many products are currently showing on the favourites page.
        """
        return self.page.locator(FavouritesLocators.all_fav_product_cards).count()

    # ── Heart icon actions ────────────────────────────────────────────────────

    def add_to_favourites(self, sku):
        unfilled_heart = self.page.locator(FavouritesLocators.unfilled_heart_by_sku(sku))
        filled_heart = self.page.locator(FavouritesLocators.filled_heart_by_sku(sku))
        product_card = self.page.locator(FavouritesLocators.product_card_by_sku(sku))

        if filled_heart.count() > 0:
            return

        product_card.wait_for(state="visible")
        unfilled_heart.wait_for(state="visible")
        unfilled_heart.scroll_into_view_if_needed()

        for _ in range(3):
            if filled_heart.count() > 0:
                return
            unfilled_heart.click(force=True)
            self.page.wait_for_timeout(300)

        expect(filled_heart).to_be_visible()

    def remove_from_favourites(self, sku):
        """
        Clicks the filled (active) heart icon for a product (removes from favourites).
        The heart has class 'clicked' when already favourited.
        """
        locator = self.page.locator(FavouritesLocators.filled_heart_by_sku(sku))
        locator.wait_for(state="visible")
        locator.click()

    # ── Cart actions ──────────────────────────────────────────────────────────

    def add_product_to_cart(self, sku):
        """
        Clicks the 'Add to cart' button for a specific product by SKU.
        """
        locator = self.page.locator(FavouritesLocators.add_to_cart_by_sku(sku))
        locator.wait_for(state="visible")
        locator.click()

    def get_cart_item_title(self, title):
        """
        Returns the locator for a product title inside the cart sidebar.
        Used with expect().to_be_visible() to confirm product was added to cart.
        """
        return self.page.locator(FavouritesLocators.cart_item_title(title))

    def get_cart_item_quantity_text(self, title):
        """
        Returns the raw quantity text (e.g. 'Samsung \\nQuantity: 1') for a cart item.
        """
        return self.page.locator(FavouritesLocators.cart_item_quantity(title)).inner_text()

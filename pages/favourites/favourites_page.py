# This file contains functions to interact with the Favourites section

from pages.favourites.locator_favourites_page import FavouritesLocators


class FavouritesPage:

    def __init__(self, page):
        self.page = page

    def click_favourites_nav(self):
        # Clicks the 'Favourites' link in the header navigation
        self.page.locator(FavouritesLocators.favourites_nav_link).click()

    def go_back(self):
        # Goes back to the previous page (browser back)
        self.page.go_back()

    def add_product_to_favourites_by_sku(self, sku):
        # Clicks the heart icon of a specific product identified by its SKU
        self.page.locator(FavouritesLocators.heart_icon_by_sku(sku)).click()

    def get_all_favourite_titles(self):
        # Returns a list of all product title strings visible on the Favourites page
        title_elements = self.page.locator(FavouritesLocators.all_product_titles_in_favourites).all()
        return [el.inner_text() for el in title_elements]

    def get_product_in_favourites(self, title):
        # Returns the locator for a specific product title on the Favourites page
        # Used for validation with expect()
        return self.page.locator(FavouritesLocators.product_title_in_favourites(title))
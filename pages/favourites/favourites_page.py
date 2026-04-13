# This file contains all interaction functions for the Favourites section.
from playwright.sync_api import expect

from pages.favourites.locator_favourites_page import FavouritesLocators
from utils.logger import get_logger

logger = get_logger()


class FavouritesPage:
    def __init__(self, page):
        self.page = page

    def click_favourites_nav(self):
        logger.info("Action: clicking Favourites nav link")
        self.page.locator(FavouritesLocators.favourites_nav_link).click()

    def go_back(self):
        logger.info("Action: navigating back to previous page")
        self.page.go_back()
        self.page.wait_for_load_state("domcontentloaded")
        logger.info("Wait: page loaded, waiting for first product card to be visible")
        self.page.locator(
            FavouritesLocators.product_card_by_sku("iPhone11-device-info.png")
        ).wait_for(state="visible")

    def get_zero_products_message(self):
        logger.info("Check: looking for 0 products message on favourites page")
        return self.page.locator(FavouritesLocators.zero_products_text)

    def get_all_favourite_titles(self):
        logger.info("Check: reading all product titles from favourites page")
        title_elements = self.page.locator(FavouritesLocators.all_fav_product_titles).all()
        titles = [element.inner_text().strip() for element in title_elements]
        logger.info(f"Check: titles found - {titles}")
        return titles

    def get_all_favourite_card_texts(self):
        logger.info("Check: reading all favourites card text")
        cards = self.page.locator(FavouritesLocators.all_fav_product_cards)
        return [cards.nth(index).inner_text().strip() for index in range(cards.count())]

    def get_favourites_count(self):
        count = self.page.locator(FavouritesLocators.all_fav_product_cards).count()
        logger.info(f"Check: favourites count = {count}")
        return count

    def add_to_favourites(self, sku):
        logger.info(f"Action: adding product to favourites - SKU: {sku}")
        unfilled_heart = self.page.locator(FavouritesLocators.unfilled_heart_by_sku(sku))
        filled_heart = self.page.locator(FavouritesLocators.filled_heart_by_sku(sku))
        product_card = self.page.locator(FavouritesLocators.product_card_by_sku(sku))

        if filled_heart.count() > 0:
            logger.info(f"Skip: product already in favourites - SKU: {sku}")
            return

        product_card.wait_for(state="visible")
        unfilled_heart.wait_for(state="visible")
        unfilled_heart.scroll_into_view_if_needed()

        for attempt in range(1, 4):
            if filled_heart.count() > 0:
                logger.info(f"Success: product hearted on attempt {attempt} - SKU: {sku}")
                return
            logger.info(f"Attempt {attempt}: clicking heart - SKU: {sku}")
            unfilled_heart.click(force=True)
            self.page.wait_for_timeout(300)

        logger.info(f"Success: heart confirmed visible - SKU: {sku}")
        expect(filled_heart).to_be_visible()

    def remove_from_favourites(self, sku):
        logger.info(f"Action: removing product from favourites - SKU: {sku}")
        locator = self.page.locator(FavouritesLocators.filled_heart_by_sku(sku))
        locator.wait_for(state="visible")
        locator.click()
        logger.info(f"Success: product removed from favourites - SKU: {sku}")

    def add_product_to_cart(self, sku):
        logger.info(f"Action: adding product to cart - SKU: {sku}")
        locator = self.page.locator(FavouritesLocators.add_to_cart_by_sku(sku))
        locator.wait_for(state="visible")
        locator.click()
        logger.info(f"Success: Add to cart clicked - SKU: {sku}")

    def get_cart_item_title(self, title):
        logger.info(f"Check: verifying cart contains - '{title}'")
        return self.page.locator(FavouritesLocators.cart_item_title(title))

    def get_cart_item_quantity_text(self, title):
        logger.info(f"Check: reading cart quantity text for - '{title}'")
        return self.page.locator(FavouritesLocators.cart_item_quantity(title)).inner_text()

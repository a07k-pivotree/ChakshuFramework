# Test: Favourites section - Happy Path
# Steps:
#   1. Click Favourites nav link
#   2. Go back to homepage
#   3. Add products to favourites by clicking heart icons
#   4. Click Favourites nav link again
#   5. Validate that added products are visible in Favourites

from playwright.sync_api import expect

from conftest import Config
from pages.login.login_page import LoginPage
from pages.favourites.favourites_page import FavouritesPage

# Products to add: (product_name_for_validation, sku_attribute_value)
# SKU comes from data-sku on the div.shelf-item element
PRODUCTS_TO_FAVOURITE = [
    ("iPhone 11 Pro",      "infocardiphone11Pro.png"),
    ("iPhone 12",          "infocardiphone12.png"),
]


def test_favourites_happy_path(page):

    # ── Step 0: Navigate to site and log in ──────────────────────────────────
    page.goto(Config.BASE_URL)
    login_page = LoginPage(page)
    login_page.click_sign_in_menu()
    login_page.select_username("demouser")
    login_page.select_password("testingisfun99")
    login_page.click_login()

    # ── Step 1: Click Favourites nav link ────────────────────────────────────
    fav_page = FavouritesPage(page)
    fav_page.click_favourites_nav()

    # ── Step 2: Go back to product listing ───────────────────────────────────
    fav_page.go_back()

    # ── Step 3: Add products to favourites by clicking heart icons ───────────
    for product_name, sku in PRODUCTS_TO_FAVOURITE:
        fav_page.add_product_to_favourites_by_sku(sku)
        # Small wait so the UI registers each click before the next
        page.wait_for_timeout(500)

    # ── Step 4: Click Favourites nav link again ──────────────────────────────
    fav_page.click_favourites_nav()

    # ── Step 5: Validate each added product is visible on Favourites page ────
    for product_name, sku in PRODUCTS_TO_FAVOURITE:
        product_locator = fav_page.get_product_in_favourites(product_name)
        expect(product_locator).to_be_visible()
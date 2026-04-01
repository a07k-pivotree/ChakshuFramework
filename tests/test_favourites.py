# Test: Favourites section — Happy Path
#
# Flow:
#   Login (if not already) → validate /favourites URL + 0 products
#   → go back → add 4 products to favourites
#   → open favourites → validate count
#   → remove 1 product → validate count updated
#   → add 1 product to cart → validate in cart

import pytest
import re
from playwright.sync_api import expect

from conftest import Config
from pages.login.login_page import LoginPage
from pages.favourites.favourites_page import FavouritesPage

# ── Test data ─────────────────────────────────────────────────────────────────
# (display_name, data-sku attribute value)
# Inspect each div.shelf-item's data-sku on bstackdemo.com to confirm these values
PRODUCTS = [
    #("iPhone 11",           "iPhone11-device-info.png"),
    ("iPhone 11 Pro",       "infocardiphone11Pro.png"),
    ("Galaxy Note 20",      "Note20-device-info.png"),
    ("Galaxy Note 20 Ultra","Note20Ultra-device-info.png"),
]

# Product we will remove from favourites in validation step
PRODUCT_TO_REMOVE = PRODUCTS[0]   # iPhone 11

# Product we will add to cart in validation step
PRODUCT_TO_CART = PRODUCTS[2]     # Galaxy Note 20 Ultra


def test_favourites_happy_path(page):

    # ── Step 0: Navigate + Login ──────────────────────────────────────────────
    page.goto(Config.BASE_URL)
    login_page = LoginPage(page)

    # If the sign-in menu is visible, we are not logged in — do login
    # If we are already logged in, this block is skipped
    if login_page.get_logout().count() == 0:
        login_page.click_sign_in_menu()
        login_page.select_username("demouser")
        login_page.select_password("testingisfun99")
        login_page.click_login()

    # ── Step 1: Open Favourites ───────────────────────────────────────────────
    fav_page = FavouritesPage(page)
    fav_page.click_favourites_nav()

    # ── Validation A: URL ends with /favourites ───────────────────────────────

    expect(page).to_have_url(re.compile(r".*/favourites$"))

    # ── Validation B: 0 products shown on first visit ─────────────────────────
    expect(fav_page.get_zero_products_message()).to_be_visible()

    # ── Step 2: Go back to product listing ───────────────────────────────────
    fav_page.go_back()

    # ── Step 3: Add all 4 products to favourites ──────────────────────────────
    for product_name, sku in PRODUCTS:
        fav_page.add_to_favourites(sku)
        # Small pause so the UI registers the heart toggle before next click
        page.wait_for_timeout(1000)

    # ── Step 4: Open Favourites again ────────────────────────────────────────
    fav_page.click_favourites_nav()

    # ── Validation 1: Count of products matches what we added ─────────────────
    actual_count = fav_page.get_favourites_count()
    expected_count = len(PRODUCTS)
    assert actual_count == expected_count, (
        f"Expected {expected_count} products in favourites, but found {actual_count}"
    )

    # ── Validation 2: Remove 1 product, count should decrease by 1 ───────────
    remove_name, remove_sku = PRODUCT_TO_REMOVE
    fav_page.remove_from_favourites(remove_sku)
    page.wait_for_timeout(500)  # wait for DOM to update after removal

    updated_count = fav_page.get_favourites_count()
    assert updated_count == expected_count - 1, (
        f"After removing '{remove_name}', expected {expected_count - 1} products "
        f"but found {updated_count}"
    )

    # ── Validation 3: Add a product to cart, confirm it appears in cart ───────
    cart_name, cart_sku = PRODUCT_TO_CART
    fav_page.add_product_to_cart(cart_sku)
    page.wait_for_timeout(500)  # wait for cart sidebar to update

    expect(fav_page.get_cart_item_title(cart_name)).to_be_visible()

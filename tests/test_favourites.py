import re

from playwright.sync_api import expect

from conftest import Config
from pages.favourites.favourites_page import FavouritesPage
from pages.home.home_page import HomePage
from pages.login.login_page import LoginPage
from utils.screenshot_helper import ScreenshotHelper


def test_favourites_happy_path(page, login_data, product_data):
    page.goto(Config.BASE_URL)
    login_page = LoginPage(page)

    if login_page.get_logout().count() == 0:
        login_page.click_sign_in_menu()
        login_page.select_username(login_data.username)
        login_page.select_password(login_data.password)
        login_page.click_login()

    fav_page = FavouritesPage(page)
    fav_page.click_favourites_nav()

    expect(page).to_have_url(re.compile(r".*/favourites$"))
    expect(fav_page.get_zero_products_message()).to_be_visible()
    ScreenshotHelper.take_validation_screenshot(page, "Favourites_Empty_State")

    fav_page.go_back()
    home_page = HomePage(page)

    for product in product_data:
        home_page.validate_product_details(product)
        fav_page.add_to_favourites(product.sku)
        page.wait_for_timeout(500)

    fav_page.click_favourites_nav()

    actual_titles = fav_page.get_all_favourite_titles()
    actual_count = fav_page.get_favourites_count()
    expected_titles = [product.product_name for product in product_data]
    expected_count = len(product_data)

    assert actual_count == expected_count, (
        f"Expected {expected_count} products in favourites, but found {actual_count}"
    )
    assert set(actual_titles) == set(expected_titles), (
        f"Favourite titles did not match Excel data. Expected {expected_titles}, found {actual_titles}"
    )

    cards_text = fav_page.get_all_favourite_card_texts()
    for product in product_data:
        assert any(
            product.product_name in card_text and product.expected_price in card_text
            for card_text in cards_text
        ), f"Favourites page did not match Excel data for '{product.product_name}'"

    ScreenshotHelper.take_validation_screenshot(page, "Favourites_Count_Match")

    product_to_remove = product_data[0]
    fav_page.remove_from_favourites(product_to_remove.sku)
    page.wait_for_timeout(500)

    updated_count = fav_page.get_favourites_count()
    assert updated_count == expected_count - 1, (
        f"After removing '{product_to_remove.product_name}', expected {expected_count - 1} products "
        f"but found {updated_count}"
    )
    ScreenshotHelper.take_validation_screenshot(page, "Favourites_Remove_Item")

    product_to_cart = product_data[2]
    fav_page.add_product_to_cart(product_to_cart.sku)
    page.wait_for_timeout(500)
    expect(fav_page.get_cart_item_title(product_to_cart.product_name)).to_be_visible()
    ScreenshotHelper.take_validation_screenshot(page, "Favourites_Add_To_Cart")

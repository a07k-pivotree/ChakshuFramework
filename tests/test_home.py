import pytest
from playwright.sync_api import expect

from conftest import Config
from pages.home.home_page import HomePage
from pages.home.locator_home_page import HomeLocators
from pages.login.login_page import LoginPage
from utils.pagination_helper import add_products
from utils.screenshot_helper import ScreenshotHelper


@pytest.fixture
def logged_in_page(page, login_data):
    page.goto(Config.BASE_URL)
    login_page = LoginPage(page)
    login_page.click_sign_in_menu()
    login_page.select_username(login_data.username)
    login_page.select_password(login_data.password)
    login_page.click_login()
    yield page


def test_empty_cart(logged_in_page):
    home_page = HomePage(logged_in_page)
    home_page.open_cart()
    buy_button = logged_in_page.locator(HomeLocators.buy_button)
    expect(buy_button).not_to_have_text("Check out")
    ScreenshotHelper.take_validation_screenshot(logged_in_page, "Empty_Cart_Validation")


def test_add_same_item_twice(logged_in_page, cart_products):
    home_page = HomePage(logged_in_page)
    product = cart_products[0]

    home_page.validate_product_details(product)
    home_page.add_product_to_cart(product.product_name)
    home_page.close_cart()
    home_page.add_product_to_cart(product.product_name)

    quantity = home_page.get_item_quantity()
    assert quantity == 2, f"Expected quantity 2, but got {quantity}"
    ScreenshotHelper.take_validation_screenshot(logged_in_page, "Add_Same_Item_Twice")


def test_remove_item_from_cart(logged_in_page, page, cart_products):
    home_page = HomePage(logged_in_page)

    for product in cart_products:
        home_page.validate_product_details(product)
    add_products(home_page, cart_products)

    home_page.open_cart()
    cart_items = home_page.get_cart_items()
    initial_count = cart_items.count()
    assert initial_count == len(cart_products), f"Cart must have exactly {len(cart_products)} items"

    home_page.remove_itm_from_cart()
    page.locator("//div[@class='float-cart__header']").click()
    expect(cart_items).to_have_count(initial_count - 1, timeout=10000)
    ScreenshotHelper.take_validation_screenshot(page, "Remove_Item_From_Cart")

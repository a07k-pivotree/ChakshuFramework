from asyncio import timeout
from idlelib.mainmenu import default_keydefs
from timeit import default_timer

import pytest
from playwright.sync_api import expect
from conftest import Config
from pages.home.home_page import HomePage
from pages.home.locator_home_page import HomeLocators
from pages.login import login_page
from pages.login.login_page import LoginPage
from utils.pagination_helper import add_products


@pytest.fixture
def logged_in_page(page):
    # Login in before test start
    page.goto(Config.BASE_URL)
    login_page = LoginPage(page)
    login_page.click_sign_in_menu()
    login_page.select_username("demouser")
    login_page.select_password("testingisfun99")
    login_page.click_login()
    yield page

def test_empty_cart(logged_in_page):
    # Verify empty cart checkout
    home_page = HomePage(logged_in_page)
    home_page.open_cart()
    buy_button = logged_in_page.locator(HomeLocators.buy_button)
    expect(buy_button).not_to_have_text("Check out")
    print("Empty cart test passed")

def test_add_same_item_twice(logged_in_page):
    # Verify adding same item twice to cart
    home_page = HomePage(logged_in_page)
    home_page.add_product_to_cart("iphone 12 Mini")
    home_page.close_cart()

    home_page .add_product_to_cart("iphone 12 Mini")
    quantity = home_page.get_item_quantity()
    assert quantity == 2, f"Expected quantity 2, but got {quantity}"
    print(" Quantity updated correctly")

def test_remove_item_from_cart(logged_in_page,page):
    home_page = HomePage(logged_in_page)

    products = ["iphone 12 Mini", "Galaxy S20", "One Plus 8 Pro"]
    add_products(home_page, products)

    home_page.open_cart()

    cart_items = home_page.get_cart_items()
    initial_count = cart_items.count()
    assert initial_count == len(products), "Cart must have exactly 3 items"

    home_page.remove_itm_from_cart()
    a = page.locator('//div[@class="float-cart__header"]')
    a.click()

    # expect(cart_items).to_have_count(initial_count - 1)

    expect(cart_items).to_have_count(initial_count - 1, timeout=10000)


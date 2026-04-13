import pytest
import re
from playwright.sync_api import expect

from conftest import Config
from pages.checkout.checkout_page import CheckoutPage
from pages.home.home_page import HomePage
from pages.login.login_page import LoginPage
from utils.pagination_helper import add_products
from utils.screenshot_helper import ScreenshotHelper


def _extract_checkout_name(item_text: str) -> str:
    return item_text.splitlines()[0].strip()


def _extract_checkout_price_value(item_text: str) -> float:
    match = re.search(r"\$[\d,]+(?:\.\d{1,2})?", item_text)
    if not match:
        raise AssertionError(f"Could not find a price in checkout row: {item_text!r}")
    return float(match.group(0).replace("$", "").replace(",", ""))


@pytest.fixture
def checkout_ready_page(page, login_data, cart_products):
    page.goto(Config.BASE_URL)
    login_page = LoginPage(page)
    login_page.click_sign_in_menu()
    login_page.select_username(login_data.username)
    login_page.select_password(login_data.password)
    login_page.click_login()

    home_page = HomePage(page)
    for product in cart_products:
        home_page.validate_product_details(product)
    add_products(home_page, cart_products)

    home_page.open_cart()
    home_page.click_checkout()
    yield page


def test_total_calculation(checkout_ready_page, cart_products):
    checkout_page = CheckoutPage(checkout_ready_page)
    checkout_items = checkout_page.get_checkout_item_texts()
    checkout_names = [_extract_checkout_name(item_text) for item_text in checkout_items]
    checkout_prices = [_extract_checkout_price_value(item_text) for item_text in checkout_items]

    calculated_total = checkout_page.get_calculated_total_of_items()
    displayed_total = checkout_page.get_displayed_total_value()
    expected_products = {product.product_name: product.price_value for product in cart_products}
    expected_total = round(sum(expected_products.values()), 2)

    assert set(checkout_names) == set(expected_products), (
        f"Checkout item names do not match Excel data. Expected {list(expected_products)}, got {checkout_names}"
    )
    for item_name, item_price in zip(checkout_names, checkout_prices):
        assert item_price == expected_products[item_name], (
            f"Checkout price mismatch for '{item_name}'. UI: {item_price}, Excel: {expected_products[item_name]}"
        )

    assert calculated_total == expected_total, (
        f"Mismatch with Excel data! Calculated: {calculated_total}, expected: {expected_total}"
    )
    assert displayed_total == expected_total, (
        f"Displayed total does not match Excel data! Displayed: {displayed_total}, expected: {expected_total}"
    )
    ScreenshotHelper.take_validation_screenshot(checkout_ready_page, "Total_Calculation_Match")


def test_shipping_and_order(checkout_ready_page):
    checkout_page = CheckoutPage(checkout_ready_page)

    checkout_page.fill_shipping_details(
        first_name="Ram",
        last_name="Sharma",
        address="123,Maple Street",
        province="Springfield",
        post_code="12345",
    )
    checkout_page.click_submit()

    order_confirmation = checkout_page.get_order_confirmation()
    expect(order_confirmation).to_be_visible()
    ScreenshotHelper.take_validation_screenshot(checkout_ready_page, "Order_Placed_Success")


def test_total_displayed(checkout_ready_page, cart_products):
    page = checkout_ready_page
    home_page = HomePage(page)
    checkout_page = CheckoutPage(page)

    page.go_back()
    page.go_forward()
    home_page.open_cart()
    home_page.remove_itm_from_cart()
    home_page.click_checkout()

    checkout_items = checkout_page.get_checkout_item_texts()
    checkout_names = [_extract_checkout_name(item_text) for item_text in checkout_items]
    calculated_total = checkout_page.get_calculated_total_of_items()
    displayed_total = checkout_page.get_displayed_total_value()
    expected_products = {product.product_name: product.price_value for product in cart_products}

    assert all(name in expected_products for name in checkout_names), (
        f"Checkout contains product not present in Excel data: {checkout_names}"
    )
    expected_total = round(sum(expected_products[name] for name in checkout_names), 2)

    assert calculated_total == expected_total, (
        f"Mismatch after removing item against Excel data! Calculated: {calculated_total}, expected: {expected_total}"
    )
    assert displayed_total == expected_total, (
        f"Displayed total after removal does not match Excel data! Displayed: {displayed_total}, expected: {expected_total}"
    )
    ScreenshotHelper.take_validation_screenshot(page, "Total_After_Removal_Match")

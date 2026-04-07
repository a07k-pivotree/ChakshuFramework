import pytest
from playwright.sync_api import expect

from conftest import Config
# from config import Config
from pages.checkout.checkout_page import CheckoutPage
from pages.home.home_page import HomePage
from pages.login.login_page import LoginPage
from utils.pagination_helper import add_products
from utils.screenshot_helper import ScreenshotHelper


@pytest.fixture
def checkout_ready_page(page):
    # Login  add product in cart and navigate to checkout page
    page.goto(Config.BASE_URL)
    login_page = LoginPage(page)
    login_page.click_sign_in_menu()
    login_page.select_username("demouser")
    login_page.select_password("testingisfun99")
    login_page.click_login()

    # Add item to cart
    home_page = HomePage(page)
    products = ["iPhone 12 Mini", "Galaxy S20", "One Plus 8 Pro"]
    add_products(home_page, products)

    home_page.open_cart()
    home_page.click_checkout()
    yield page


def test_total_calculation(checkout_ready_page):
    checkout_page = CheckoutPage(checkout_ready_page)

    calculated_total = checkout_page.get_calculated_total_of_items()
    displayed_total = checkout_page.get_displayed_total_value()

    assert calculated_total == displayed_total, f"Mismatch! Calculated: {calculated_total}, displayed: {displayed_total}"

    # <-- 2. Capture proof that the totals match
    ScreenshotHelper.take_validation_screenshot(checkout_ready_page, "Total_Calculation_Match")
    print("Total calculation matches")


def test_shipping_and_order(checkout_ready_page):
    checkout_page = CheckoutPage(checkout_ready_page)

    checkout_page.fill_shipping_details(
        first_name="Ram",
        last_name="Sharma",
        address="123,Maple Street",
        province="Springfield",
        post_code="12345"
    )
    checkout_page.click_submit()

    order_confirmation = checkout_page.get_order_confirmation()
    expect(order_confirmation).to_be_visible()

    # <-- 3. Capture proof that the order was placed
    ScreenshotHelper.take_validation_screenshot(checkout_ready_page, "Order_Placed_Success")
    print(f"Order number: {order_confirmation.inner_text()}")


def test_total_displayed(checkout_ready_page):
    page = checkout_ready_page
    home_page = HomePage(page)
    checkout_page = CheckoutPage(page)

    page.go_back()
    page.go_forward()
    home_page.open_cart()
    home_page.remove_itm_from_cart()  # Note: I updated this to match your POM method

    home_page.click_checkout()

    calculated_total = checkout_page.get_calculated_total_of_items()
    displayed_total = checkout_page.get_displayed_total_value()

    assert calculated_total == displayed_total, f"Mismatch after removing item! Calculated: {calculated_total}, displayed: {displayed_total}"

    # <-- 4. Capture proof that the totals match after removal
    ScreenshotHelper.take_validation_screenshot(page, "Total_After_Removal_Match")
    print("Total after removal is correct")
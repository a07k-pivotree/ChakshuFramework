class CheckoutLocators:
    first_name_input = "#firstNameInput"
    last_name_input = "#lastNmaeInput"
    address_input = "#addreshLine1Input"
    province_input = "#provinceInput"
    post_code_input = "#postCodeInput"
    submit_buton = "//button[contains(text(),'Submit')]"

    # Validation Locators
    order_confirmation = "//div[@class='checkout-form']/div[2]/strong"
    cart_items = "//section[@class='cart-section optimizedCheckout-orderSummary-cartSection'][1]/ul/li"
    total_displayed = "//div[contains(@class,'cart-priceItem--total')]//span[2]"
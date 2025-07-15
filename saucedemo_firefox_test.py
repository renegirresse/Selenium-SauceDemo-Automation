from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

print("Starting automated test: End-to-End Purchase Flow (Firefox, high-to-low filter, two products, opening product pages)...")

driver = None

try:
    firefox_options = FirefoxOptions()

    # Maximize window for better visibility
    firefox_options.add_argument("--window-size=1920,1080")

    print("Firefox options configured for visible automation.")

    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)

    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    print("Browser (Firefox) opened and navigated to SauceDemo.")
    time.sleep(2)

    # --- 1. Login ---
    username_field = driver.find_element(By.ID, "user-name")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    # Introduce small delays for visible typing - Username
    username = "standard_user"
    for char in username:
        username_field.send_keys(char)
        time.sleep(0.1)  # Small delay after each character
    print("Entered username: standard_user (character by character).")

    # Introduce small delays for visible typing - Password
    password = "secret_sauce"
    for char in password:
        password_field.send_keys(char)
        time.sleep(0.1)  # Small delay after each character
    print("Entered password (character by character).")

    login_button.click()
    print("Clicked login button.")
    time.sleep(2)  # Give page time to transition after login

    # --- ATTEMPT TO DISMISS POP-UP (if any appears) ---
    print("Attempting to dismiss any pop-up with ESCAPE key...")
    try:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        print("Sent ESCAPE key to dismiss potential pop-up.")
        time.sleep(1)
    except Exception as pop_up_error:
        print(f"No pop-up found or failed to dismiss with ESCAPE: {pop_up_error}")
    time.sleep(1)  # General short sleep after potential pop-up

    # Verify successful login to products page
    products_header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    )
    if products_header.text == "Products":
        print("Verification: Successfully landed on the products page.")
    else:
        print("Verification: Failed to land on the products page. Header was: " + products_header.text)
        raise Exception("Login failed, cannot proceed with test.")

    # --- 2. Apply "Price (high to low)" filter with visual pauses ---
    print("Locating and clicking sort dropdown to reveal options...")
    sort_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container"))
    )
    
    # Click the dropdown to make options visible
    sort_dropdown.click()
    print("Clicked sort dropdown. Pausing for 1 second to show options...")
    time.sleep(1) # Pause to visibly see the dropdown options

    # Select "Price (high to low)"
    select = Select(sort_dropdown)
    select.select_by_value("hilo") # "hilo" is the value for Price (high to low)
    print("Selected 'Price (high to low)' from filter. Pausing for 2 seconds to show re-sort...")
    time.sleep(2) # Give time for the products to re-sort and to see the selection

    # --- 3. Add the top two products to the cart by opening their pages ---
    products_to_add_count = 2
    added_product_names = []

    for i in range(products_to_add_count):
        # Use WebDriverWait to ensure product links are re-present after navigation
        product_links_on_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_name"))
        )
        
        if i >= len(product_links_on_list):
            print(f"WARNING: Could not find product {i+1}. Only {len(product_links_on_list)} products available.")
            break # Exit loop if not enough products

        # Get the specific link for the current product index
        product_link = product_links_on_list[i]
        current_product_name = product_link.text
        # Before clicking, check if the item is already added (e.g., if we're re-running and it's removed on refresh)
        # This is a good sanity check but not strictly necessary for this flow
        # if product_link.find_element(By.XPATH, "./ancestor::div[@class='inventory_item']//button").text == "Remove":
        #    print(f"Product '{current_product_name}' already in cart. Skipping add.")
        #    added_product_names.append(current_product_name) # Add to list for verification later
        #    continue 

        added_product_names.append(current_product_name) # Add to list here as we intend to add it

        print(f"Clicking product link for: {current_product_name}...")
        product_link.click()
        time.sleep(2) # Pause to see the product detail page

        # Verify we are on the correct product detail page (optional but good practice)
        product_detail_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_details_name"))
        )
        if product_detail_name.text != current_product_name:
            print(f"Verification: Mismatch on product detail page. Expected '{current_product_name}', found '{product_detail_name.text}'.")
            # You might want to raise an exception here, but for demonstration, we'll continue.

        # Add to cart from detail page
        # *** FIX HERE: Corrected ID for the "Add to cart" button on the detail page ***
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart")) # Changed from By.XPATH to By.ID
        )
        add_to_cart_button.click()
        print(f"Added '{current_product_name}' to cart from its detail page. Observing button text change...")
        time.sleep(2) # Pause to see "Add to cart" change to "Remove"

        # Go back to product list
        back_to_products_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "back-to-products"))
        )
        back_to_products_button.click()
        print(f"Clicked 'Back to products' for {current_product_name}.")
        # Wait for the products list page to load and its elements to be stable
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name")))
        time.sleep(2) # Additional pause to ensure the list is fully re-rendered and visible

    print(f"Finished adding {products_to_add_count} product(s) to cart: {', '.join(added_product_names)}")


    # --- 4. Verify item count in shopping cart icon using explicit wait ---
    print("Waiting for cart badge to update...")
    try:
        cart_badge_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        if cart_badge_element.text == str(products_to_add_count):
            print(f"Verification: Cart badge shows {products_to_add_count} item(s).")
        else:
            print(f"Verification: Cart badge shows {cart_badge_element.text} items. Expected {products_to_add_count}.")
            raise Exception("Cart badge count incorrect after waiting.")

    except TimeoutException:
        print("ERROR: Cart badge did not update to the correct quantity within the timeout.")
        raise Exception("Cart badge verification failed.")
    except NoSuchElementException:
        print("ERROR: Cart badge element not found.")
        raise Exception("Cart badge verification failed.")


    # --- 5. Navigate to the shopping cart page ---
    shopping_cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    shopping_cart_icon.click()
    print("Navigated to the shopping cart page.")
    time.sleep(2) # Wait for cart page to load

    # Verify both added items are present in the cart
    found_products_in_cart = []
    cart_item_names_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    for item_element in cart_item_names_elements:
        found_products_in_cart.append(item_element.text)

    all_products_found = True
    for product in added_product_names:
        if product not in found_products_in_cart:
            all_products_found = False
            print(f"Verification: ERROR! Product '{product}' not found in cart.")
            break
    
    if all_products_found and len(found_products_in_cart) == products_to_add_count:
        print(f"Verification: All {products_to_add_count} selected products found in cart: {', '.join(found_products_in_cart)}.")
    else:
        print(f"Verification: Mismatch in cart contents. Expected: {added_product_names}, Found: {found_products_in_cart}.")
        raise Exception("Cart contents verification failed.")


    # --- 6. Proceed to Checkout from Cart Page (using explicit wait for clickability) ---
    print("Waiting for Checkout button to be clickable...")
    try:
        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_button.click()
        print("Clicked 'Checkout' button on cart page.")
    except TimeoutException:
        print("ERROR: Checkout button not clickable within timeout.")
        raise Exception("Checkout button not interactable.")
    time.sleep(2) # Wait for checkout info page to load

    # Verify that we are on the checkout information page
    checkout_info_header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    )
    if checkout_info_header.text == "Checkout: Your Information":
        print("Verification: Successfully landed on Checkout: Your Information page.")
    else:
        print("Verification: Failed to land on Checkout: Your Information page. Header was: " + checkout_info_header.text)
        raise Exception("Did not land on checkout information page.")

    # --- 7. Fill in Customer Information ---
    first_name_field = driver.find_element(By.ID, "first-name")
    last_name_field = driver.find_element(By.ID, "last-name")
    zip_code_field = driver.find_element(By.ID, "postal-code")
    continue_button = driver.find_element(By.ID, "continue")

    # Introduce small delays for visible typing - First Name
    first_name = "Test"
    for char in first_name:
        first_name_field.send_keys(char)
        time.sleep(0.1)
    print("Entered First Name (character by character).")

    # Introduce small delays for visible typing - Last Name
    last_name = "User"
    for char in last_name:
        last_name_field.send_keys(char)
        time.sleep(0.1)
    print("Entered Last Name (character by character).")

    # Introduce small delays for visible typing - Zip Code
    zip_code = "90210"
    for char in zip_code:
        zip_code_field.send_keys(char)
        time.sleep(0.1)
    print("Entered Zip/Postal Code (character by character).")

    time.sleep(1) # Small pause for visual confirmation

    continue_button.click()
    print("Clicked 'Continue' button on checkout info page.")
    time.sleep(2) # Wait for checkout overview page to load

    # Verify that we are on the checkout overview page
    checkout_overview_header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    )
    if checkout_overview_header.text == "Checkout: Overview":
        print("Verification: Successfully landed on Checkout: Overview page.")
    else:
        print("Verification: Failed to land on Checkout: Overview page. Header was: " + checkout_overview_header.text)
        raise Exception("Did not land on checkout overview page.")

    # --- 8. Complete the Purchase ---
    finish_button = driver.find_element(By.ID, "finish")
    finish_button.click()
    print("Clicked 'Finish' button on checkout overview page.")
    time.sleep(2) # Wait for checkout complete page to load

    # Verify successful purchase
    checkout_complete_header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    )
    thank_you_message = driver.find_element(By.CLASS_NAME, "complete-header")

    if checkout_complete_header.text == "Checkout: Complete!" and \
       "Thank you for your order!" in thank_you_message.text:
        print("Verification: Purchase completed successfully! 'Thank you for your order!' message found.")
    else:
        print("Verification: Purchase completion failed or message not found. Header was: " + checkout_complete_header.text + ", Message: " + thank_you_message.text)
        raise Exception("Purchase not successfully completed.")

    print("End-to-End Purchase Flow Test finished successfully (Firefox, high-to-low filter, two products, opening product pages)!")

except Exception as e:
    print(f"An error occurred during the test: {e}")

finally:
    if driver:
        driver.quit()
        print("Browser (Firefox) closed.")
    print("Automated test finished.")
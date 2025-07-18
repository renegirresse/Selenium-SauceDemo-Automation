# SauceDemo E-commerce Automation with Selenium + Python

## 🎥 **VIDEO DEMONSTRATION**
https://github.com/user-attachments/assets/118955fe-a9ba-4295-9549-1069830cca1a

## 📄 **Terminal Output**
<img width="1150" height="583" alt="Image" src="https://github.com/user-attachments/assets/10b4a51b-ab12-4c65-98ad-44a447ee4f94" />

## 🚀 **Project Overview** 

This project demonstrates a robust end-to-end automation test for the SauceDemo e-commerce website, built using Python and Selenium WebDriver. 
The script simulates a typical user purchase flow, from logging in and Browse products to adding items to the cart and completing the checkout process.

A key focus of this automation is on **emulating realistic user interaction** by navigating to individual product detail pages before adding items to the cart, 
rather than adding them directly from the product listing. It also incorporates essential **Selenium best practices**, such as explicit waits, 
to ensure test stability and reliability against dynamic web elements.

### 🔥 **FEATURES**

This automation script performs the following sequence of actions:

1.  **User Login:** Logs into the SauceDemo application with standard user credentials.
2.  **Product Sorting:** Applies the "Price (high to low)" filter to re-arrange products.
3.  **Individual Product Browse & Addition:**
    * Navigates to the detail page of the **highest-priced product**.
    * Adds the product to the shopping cart from its detail page.
    * Returns to the main product listing page.
    * Repeats the process for the **second highest-highest-priced product**.
    * *Visual Observation Point:* The script includes pauses to allow observation of the "Add to cart" button changing to "Remove" on the product detail pages.
4.  **Cart Verification:** Verifies that the shopping cart badge accurately reflects the number of items added.
5.  **Navigate to Cart:** Proceeds to the shopping cart page.
6.  **Cart Contents Verification:** Confirms that both selected products are present in the cart.
7.  **Checkout Information:** Proceeds to the checkout information page and fills in dummy customer details (First Name, Last Name, Zip/Postal Code).
8.  **Checkout Overview:** Advances to the checkout overview page.
9.  **Complete Purchase:** Finalizes the order.
10. **Purchase Confirmation:** Verifies the "Thank you for your order!" message on the final confirmation page.

### 🔧 **Technologies Used**

* **Python:** The primary programming language used for the automation script.
* **Selenium WebDriver:** The automation framework for interacting with web browsers.
* **`webdriver-manager`:** A library that automatically downloads and manages browser drivers (like GeckoDriver for Firefox), eliminating manual setup.
* **Firefox (GeckoDriver):** The browser used for executing the test.

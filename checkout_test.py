from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import os
BASE = "https://www.saucedemo.com/"
def screenshot(driver, name):
    os.makedirs("screenshots/checkout", exist_ok=True)
    driver.save_screenshot(f"screenshots/checkout/{name}.png")
   
    

def login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE)
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    wait.until(EC.url_contains("inventory.html"))
def test_checkout_ok():
    driver = webdriver.Chrome()
    try:
        login(driver)
        wait = WebDriverWait(driver, 10)

        # Add product
        add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory")))
        add_btn.click()

        # Go to cart
        cart = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")))
        cart.click()
        wait.until(EC.url_contains("cart.html"))

        # Checkout
        checkout = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
        checkout.click()
        wait.until(EC.url_contains("checkout-step-one"))

        # Fill form
        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Test")
        driver.find_element(By.ID, "last-name").send_keys("User")
        driver.find_element(By.ID, "postal-code").send_keys("1000")
        driver.find_element(By.ID, "continue").click()

        # Finish
        wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()

        # Check confirmation
        msg = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))).text
        assert "THANK YOU" in msg.upper()

        print("TC-CHECKOUT-01: PASS")
        screenshot(driver, "checkout_ok_PASS")
    except Exception as e:
        print("TC-CHECKOUT-01: FAIL")
        print(traceback.format_exc())
        screenshot(driver, "checkout_ok_fail")
        raise

    finally:
        driver.quit()


def test_checkout_missing_lastname():
    driver = webdriver.Chrome()
    try:
        login(driver)
        wait = WebDriverWait(driver, 10)

        # Add product
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory"))).click()

        # Cart
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))).click()
        wait.until(EC.url_contains("cart.html"))

        # Checkout
        wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
        wait.until(EC.url_contains("checkout-step-one"))

        # Fill only firstname + postal
        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Test")
        driver.find_element(By.ID, "postal-code").send_keys("1000")
        driver.find_element(By.ID, "continue").click()

        # Error
        error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container")))
        assert error.is_displayed()

        print("TC-CHECKOUT-02: PASS")
        screenshot(driver, "checkout_missing_last_name_PASS")
    except Exception as e:
        print("TC-CHECKOUT-02: FAIL")
        print(traceback.format_exc())
        screenshot(driver, "checkout_missing_lastname_fail")
        raise

    finally:
        driver.quit()


def test_total_price():
    driver = webdriver.Chrome()
    try:
        login(driver)
        wait = WebDriverWait(driver, 10)

        # Add 2 products
        buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.btn_inventory")))
        buttons[0].click()
        buttons[1].click()

        # Cart
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))).click()
        wait.until(EC.url_contains("cart.html"))

        # Checkout
        wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

        # Info
        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Test")
        driver.find_element(By.ID, "last-name").send_keys("User")
        driver.find_element(By.ID, "postal-code").send_keys("1000")
        driver.find_element(By.ID, "continue").click()

        # Total
        total = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "summary_total_label"))).text
        assert "$" in total

        print("TC-CHECKOUT-03: PASS")
        screenshot(driver, "checkout_total_PASS")
    except Exception as e:
        print("TC-CHECKOUT-03: FAIL")
        print(traceback.format_exc())
        screenshot(driver, "checkout_total_fail")
        raise

    finally:
        driver.quit()


if __name__ == "__main__":
    test_checkout_ok()
    test_checkout_missing_lastname()
    test_total_price()

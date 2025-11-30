# add_to_cart_test.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time

BASE = "https://www.saucedemo.com/"

def screenshot(driver, name):
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot(f"screenshots/{name}.png")

def login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE)
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))

def test_add_product():
    driver = webdriver.Chrome()
    try:
        login(driver)
        wait = WebDriverWait(driver, 10)
        # Add first product
        add_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.btn_inventory")))
        add_buttons[0].click()
        # check badge
        badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))).text
        assert badge == "1"
        print("TC add one product: PASS")
        # Add two more
        add_buttons[1].click()
        add_buttons[2].click()
        badge2 = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))).text
        assert badge2 == "3"
        print("TC add multiple products: PASS")
    except Exception as e:
        print("TC add product: FAIL", e)
        screenshot(driver, "add_product_fail")
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    test_add_product()
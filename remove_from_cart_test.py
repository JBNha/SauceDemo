from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

BASE = "https://www.saucedemo.com/"

def screenshot(driver, name):
    os.makedirs("screenshots/remove", exist_ok=True)
    driver.save_screenshot(f"screenshots/remove/{name}.png")

def login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE)
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    wait.until(EC.url_contains("inventory.html"))

# TC-R01
def test_remove_from_inventory():
    driver = webdriver.Chrome()
    try:
        login(driver)
        wait = WebDriverWait(driver, 10)

        btn_add = driver.find_element(By.CSS_SELECTOR, "button.btn_inventory")
        btn_add.click()

        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert badge.text == "1"

        btn_remove = driver.find_element(By.CSS_SELECTOR, "button.btn_inventory")
        btn_remove.click()

        badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        assert len(badges) == 0

        screenshot(driver, "remove_inventory")
        print("TC-R01: PASS")
    except Exception as e:
        screenshot(driver, "remove_inventory_fail")
        print("TC-R01: FAIL", e)
    finally:
        driver.quit()

# TC-R02
def test_remove_from_cart_page():
    driver = webdriver.Chrome()
    try:
        login(driver)
        wait = WebDriverWait(driver, 10)

        driver.find_element(By.CSS_SELECTOR, "button.btn_inventory").click()
        driver.find_element(By.ID, "shopping_cart_container").click()

        wait.until(EC.url_contains("cart.html"))

        driver.find_element(By.CSS_SELECTOR, "button.cart_button").click()

        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items) == 0

        screenshot(driver, "remove_cart")
        print("TC-R02: PASS")
    except Exception as e:
        screenshot(driver, "remove_cart_fail")
        print("TC-R02: FAIL", e)
    finally:
        driver.quit()

# TC-R03
def test_empty_cart():
    driver = webdriver.Chrome()
    try:
        login(driver)

        driver.find_element(By.ID, "shopping_cart_container").click()
        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items) == 0

        screenshot(driver, "empty_cart")
        print("TC-R03: PASS")
    except Exception as e:
        screenshot(driver, "empty_cart_fail")
        print("TC-R03: FAIL", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    test_remove_from_inventory()
    test_remove_from_cart_page()
    test_empty_cart()

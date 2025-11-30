<<<<<<< HEAD
=======
# add_to_cart_test.py
>>>>>>> rayan
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
<<<<<<< HEAD
import os
=======
import os, time
>>>>>>> rayan

BASE = "https://www.saucedemo.com/"

def screenshot(driver, name):
<<<<<<< HEAD
    os.makedirs("screenshots/add", exist_ok=True)
    driver.save_screenshot(f"screenshots/add/{name}.png")
=======
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot(f"screenshots/{name}.png")
>>>>>>> rayan

def login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE)
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
<<<<<<< HEAD
    wait.until(EC.url_contains("inventory.html"))

# TC-A01
def test_add_one_product():
=======
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))

def test_add_product():
>>>>>>> rayan
    driver = webdriver.Chrome()
    try:
        login(driver)
        wait = WebDriverWait(driver, 10)
<<<<<<< HEAD
        btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory")))
        btn.click()
        badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        assert badge.text == "1"
        screenshot(driver, "add_one")
        print("TC-A01: PASS")
    except Exception as e:
        screenshot(driver, "add_one_fail")
        print("TC-A01: FAIL", e)
    finally:
        driver.quit()

# TC-A02
def test_add_three_products():
    driver = webdriver.Chrome()
    try:
        login(driver)
        wait = WebDriverWait(driver, 10)
        buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.btn_inventory")))
        for i in range(3):
            buttons[i].click()
        badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        assert badge.text == "3"
        screenshot(driver, "add_three")
        print("TC-A02: PASS")
    except Exception as e:
        screenshot(driver, "add_three_fail")
        print("TC-A02: FAIL", e)
    finally:
        driver.quit()

# TC-A03
def test_cart_page_products():
    driver = webdriver.Chrome()
    try:
        login(driver)
        wait = WebDriverWait(driver, 10)
        driver.find_elements(By.CSS_SELECTOR, "button.btn_inventory")[0].click()
        driver.find_element(By.ID, "shopping_cart_container").click()
        wait.until(EC.url_contains("cart.html"))
        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items) >= 1
        screenshot(driver, "cart_page")
        print("TC-A03: PASS")
    except Exception as e:
        screenshot(driver, "cart_page_fail")
        print("TC-A03: FAIL", e)
=======
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
>>>>>>> rayan
    finally:
        driver.quit()

if __name__ == "__main__":
<<<<<<< HEAD
    test_add_one_product()
    test_add_three_products()
    test_cart_page_products()
=======
    test_add_product()
>>>>>>> rayan

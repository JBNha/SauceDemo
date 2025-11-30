from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os, traceback

BASE = "https://www.saucedemo.com/"


# ----------------- DRIVER SETUP AUTO -----------------
def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(), options=options)


# ----------------- SCREENSHOT -----------------
def screenshot(driver, name):
    os.makedirs("screenshots/sort", exist_ok=True)
    path = f"screenshots/sort/{name}.png"
    driver.save_screenshot(path)
    print("Screenshot :", path)


# ----------------- LOGIN -----------------
def login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE)

    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    wait.until(EC.url_contains("inventory.html"))


# ----------------- UTILS -----------------
def get_product_names(driver):
    return [p.text.lower() for p in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]


def get_product_prices(driver):
    return [float(p.text.replace("$", "")) for p in driver.find_elements(By.CLASS_NAME, "inventory_item_price")]


# ----------------- TEST 01 AZ -----------------
def test_sort_az():
    driver = create_driver()
    try:
        login(driver)
        wait = WebDriverWait(driver, 10)

        select_box = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container")))
        Select(select_box).select_by_value("az")

        wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "inventory_item_name")) > 0)

        names = get_product_names(driver)
        assert names == sorted(names)

        print("TC-SORT-01 AZ: PASS")
        screenshot(driver, "sort_az__PASS")
    except Exception:
        print("TC-SORT-01 AZ: FAIL")
        print(traceback.format_exc())
        screenshot(driver, "sort_az_fail")

    finally:
        driver.quit()


# ----------------- TEST 02 LOW HIGH -----------------
def test_sort_low_high():
    driver = create_driver()
    try:
        login(driver)
        wait = WebDriverWait(driver, 10)

        select_box = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container")))
        Select(select_box).select_by_value("lohi")

        wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "inventory_item_price")) > 0)

        prices = get_product_prices(driver)
        assert prices == sorted(prices)

        print("TC-SORT-02 LOHI: PASS")
        screenshot(driver, "sort_lohi__PASS")
    except Exception:
        print("TC-SORT-02 LOHI: FAIL")
        print(traceback.format_exc())
        screenshot(driver, "sort_lohi_fail")

    finally:
        driver.quit()


# ----------------- TEST 03 HIGH LOW -----------------
def test_sort_high_low():
    driver = create_driver()
    try:
        login(driver)
        wait = WebDriverWait(driver, 10)

        select_box = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container")))
        Select(select_box).select_by_value("hilo")

        wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "inventory_item_price")) > 0)

        prices = get_product_prices(driver)
        assert prices == sorted(prices, reverse=True)

        print("TC-SORT-03 HILO: PASS")
        screenshot(driver, "sort_hilo__PASS")
    except Exception:
        print(" TC-SORT-03 HILO: FAIL")
        print(traceback.format_exc())
        screenshot(driver, "sort_hilo_fail")

    finally:
        driver.quit()


# ----------------- RUN -----------------
if __name__ == "__main__":
    test_sort_az()
    test_sort_low_high()
    test_sort_high_low()
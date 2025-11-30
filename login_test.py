from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

BASE = "https://www.saucedemo.com/"

def screenshot(driver, name):
    os.makedirs("screenshots/login", exist_ok=True)
    driver.save_screenshot(f"screenshots/login/{name}.png")

def test_login_valid():
    driver = webdriver.Chrome()
    try:
        driver.get(BASE)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        wait.until(EC.url_contains("inventory.html"))
        screenshot(driver, "login_valid")
        print("TC-L01: PASS")
    except Exception as e:
        screenshot(driver, "login_valid_fail")
        print("TC-L01: FAIL", e)
    finally:
        driver.quit()

def test_login_wrong_password():
    driver = webdriver.Chrome()
    try:
        driver.get(BASE)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("wrong_pass")
        driver.find_element(By.ID, "login-button").click()

        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container")))
        screenshot(driver, "login_wrong_password")
        print("TC-L02: PASS")
    except Exception as e:
        screenshot(driver, "login_wrong_password_fail")
        print("TC-L02: FAIL", e)
    finally:
        driver.quit()

def test_login_locked_out():
    driver = webdriver.Chrome()
    try:
        driver.get(BASE)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("locked_out_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container")))
        screenshot(driver, "login_locked_out")
        print("TC-L03: PASS")
    except Exception as e:
        screenshot(driver, "login_locked_out_fail")
        print("TC-L03: FAIL", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    test_login_valid()
    test_login_wrong_password()
    test_login_locked_out()

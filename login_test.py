# login_test.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os

BASE = "https://www.saucedemo.com/"

def screenshot(driver, name):
    os.makedirs("screenshots", exist_ok=True)
    path = f"screenshots/{name}.png"
    driver.save_screenshot(path)
    print("Saved screenshot:", path)

def test_login_valid():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(BASE)
        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        # assert redirected to inventory
        wait.until(EC.url_contains("inventory.html"))
        title = driver.title
        assert "Swag Labs" in title
        print("TC login valid: PASS")
    except Exception as e:
        print("TC login valid: FAIL", e)
        screenshot(driver, "login_valid_fail")
        raise
    finally:
        driver.quit()

def test_login_invalid_password():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(BASE)
        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("badpass")
        driver.find_element(By.ID, "login-button").click()
        err = wait.until(EC.visibility_of_element_located((By.XPATH, "//h3[@data-test='error']"))).text
        assert len(err) > 0
        print("TC login invalid password: PASS")
    except Exception as e:
        print("TC login invalid password: FAIL", e)
        screenshot(driver, "login_invalid_fail")
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    test_login_valid()
    test_login_invalid_password()
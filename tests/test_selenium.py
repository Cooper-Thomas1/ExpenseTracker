import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_register_valid_user(driver):
    driver.get("http://127.0.0.1:5000/register")
    driver.find_element(By.NAME, "username").send_keys("newuser")
    driver.find_element(By.NAME, "email").send_keys("newuser@example.com")
    driver.find_element(By.NAME, "password").send_keys("abc")
    driver.find_element(By.NAME, "confirm_password").send_keys("abc")
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 10).until(
        EC.url_contains("/login")
    )

def test_register_existing_username(driver):
    driver.get("http://127.0.0.1:5000/register")
    driver.find_element(By.NAME, "username").send_keys("newuser")
    driver.find_element(By.NAME, "email").send_keys("newuser@example.com")
    driver.find_element(By.NAME, "password").send_keys("abc")
    driver.find_element(By.NAME, "confirm_password").send_keys("abc")
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "That username is already taken.")
    )
    # Confirm the user is still on the register page
    assert driver.current_url == "http://127.0.0.1:5000/register"
    
def test_login_form(driver):
    driver.get("http://127.0.0.1:5000/login")
    driver.find_element(By.NAME, "email").send_keys("newuser@example.com")
    driver.find_element(By.NAME, "password").send_keys("abc")
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Logout"))

def test_manual_expense_form(driver):
    driver.get("http://127.0.0.1:5000/upload")
    driver.find_element(By.NAME, "date").send_keys("2025-05-01")
    driver.find_element(By.NAME, "category").send_keys("Food")
    driver.find_element(By.NAME, "amount").send_keys("15.75")
    driver.find_element(By.NAME, "description").send_keys("Dinner at restaurant")
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Expense added successfully"))

def test_share_valid_username(driver):
    driver.get("http://127.0.0.1:5000/share")
    driver.find_element(By.NAME, "username").send_keys("123")
    driver.find_element(By.NAME, "start_date").send_keys("2024-01-01")
    driver.find_element(By.NAME, "end_date").send_keys("2024-12-31")
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Successfully shared expenses.")
    )

def test_share_invalid_username(driver):
    driver.get("http://127.0.0.1:5000/share")
    driver.find_element(By.NAME, "username").send_keys("doesnotexist")
    driver.find_element(By.NAME, "start_date").send_keys("2024-01-01")
    driver.find_element(By.NAME, "end_date").send_keys("2024-12-31")
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "No account with that username found.")
    )
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

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
    driver.find_element(By.NAME, "primary_saving_goal").send_keys("new car")
    driver.find_element(By.NAME, "submit").click()
    assert WebDriverWait(driver, 10).until(
        EC.url_contains("/login")
    )

def test_register_existing_username(driver):
    driver.get("http://127.0.0.1:5000/register")
    driver.find_element(By.NAME, "username").send_keys("newuser")
    driver.find_element(By.NAME, "email").send_keys("newuser@example.com")
    driver.find_element(By.NAME, "password").send_keys("abc")
    driver.find_element(By.NAME, "confirm_password").send_keys("abc")
    driver.find_element(By.NAME, "primary_saving_goal").send_keys("new car")
    driver.find_element(By.NAME, "submit").click()
    # Confirm the user is still on the register page
    assert WebDriverWait(driver, 10).until(
        EC.url_contains("/register")
    )

def test_register_existing_email(driver):
    driver.get("http://127.0.0.1:5000/register")
    driver.find_element(By.NAME, "username").send_keys("newusertwo")
    driver.find_element(By.NAME, "email").send_keys("newuser@example.com")
    driver.find_element(By.NAME, "password").send_keys("abc")
    driver.find_element(By.NAME, "confirm_password").send_keys("abc")
    driver.find_element(By.NAME, "primary_saving_goal").send_keys("new car")
    driver.find_element(By.NAME, "submit").click()
    # Confirm the user is still on the register page
    assert WebDriverWait(driver, 10).until(
        EC.url_contains("/register")
    )
    
def test_login_form(driver):
    driver.get("http://127.0.0.1:5000/login")
    driver.find_element(By.NAME, "email").send_keys("newuser@example.com")
    driver.find_element(By.NAME, "password").send_keys("abc")
    driver.find_element(By.NAME, "submit").click()
    # successful login redirects to the dashboard
    assert WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard")
    )

def test_manual_expense_form(driver):
    driver.get("http://127.0.0.1:5000/upload")
    driver.find_element(By.NAME, "date").send_keys("01/05/2025")
    driver.find_element(By.NAME, "category").send_keys("Food")
    driver.find_element(By.NAME, "amount").send_keys("15.75")
    driver.find_element(By.NAME, "description").send_keys("Dinner at restaurant")
    driver.find_element(By.NAME, "manual_submit").click()
    # successful expense input redirects to the dashboard
    assert WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard")
    )

def test_share_valid_username(driver):
    # add another user to share expenses with
    driver.get("http://127.0.0.1:5000/register")
    driver.find_element(By.NAME, "username").send_keys("shareuser")
    driver.find_element(By.NAME, "email").send_keys("shareuser@example.com")
    driver.find_element(By.NAME, "password").send_keys("abc")
    driver.find_element(By.NAME, "confirm_password").send_keys("abc")
    driver.find_element(By.NAME, "primary_saving_goal").send_keys("new car")
    driver.find_element(By.NAME, "submit").click()
    assert WebDriverWait(driver, 10).until(
        EC.url_contains("/login")
    )

    driver.get("http://127.0.0.1:5000/share")
    driver.find_element(By.NAME, "username").send_keys("shareuser")
    driver.find_element(By.NAME, "start_date").send_keys("01/01/2024")
    driver.find_element(By.NAME, "end_date").send_keys("11/12/2024")
    driver.find_element(By.CLASS_NAME, "btn").click()
    assert WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Successfully shared expenses.")
    )

def test_share_invalid_username(driver):
    driver.get("http://127.0.0.1:5000/share")
    driver.find_element(By.NAME, "username").send_keys("doesnotexist")
    driver.find_element(By.NAME, "start_date").send_keys("01/01/2024")
    driver.find_element(By.NAME, "end_date").send_keys("11/12/2024")
    driver.find_element(By.CLASS_NAME, "btn").click()
    assert WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "No account with that username found.")
    )

def test_delete_expense(driver):
    driver.get("http://127.0.0.1:5000/expense-history")
    table_size = int(driver.find_element(By.TAG_NAME, "tbody").get_attribute("childElementCount"))
    assert table_size == 1 # should be 1 after the previous tests
    print(table_size)
    
    driver.find_element(By.CLASS_NAME, "btn").click() # click the delete button
    assert WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Expense deleted successfully!")
    )

    table_size = int(driver.find_element(By.TAG_NAME, "tbody").get_attribute("childElementCount"))
    assert table_size == 0 # should be 0 after deleting the expense
    print(table_size)

def test_delete_shared_expense(driver):
    driver.get("http://127.0.0.1:5000/share")
    table_size = int(driver.find_element(By.TAG_NAME, "tbody").get_attribute("childElementCount"))
    assert table_size == 1 # should be 1 after the previous tests
    print(table_size)
    
    driver.find_element(By.CLASS_NAME, "btn-danger").click() # click the delete button
    assert WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Shared expense deleted successfully!")
    )

    table_size = int(driver.find_element(By.TAG_NAME, "tbody").get_attribute("childElementCount"))
    assert table_size == 0 # should be 0 after deleting the expense
    print(table_size)

def test_upload_expenses(driver):
    driver.get("http://127.0.0.1:5000/upload")
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type=file]")
    file_input.send_keys(os.path.abspath("uploads/test1.csv"))
    driver.find_element(By.NAME, "file_submit").click()
    # successful upload redirects to the dashboard
    assert WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard")
    )


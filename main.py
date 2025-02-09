from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import argparse

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Parse CLI arguments (optional for automation)
parser = argparse.ArgumentParser(description="Selenium Login Tester")
parser.add_argument("--login_url", type=str, default="http://urbanlink.net.ph/urban/urbanlogin.html", help="Custom login URL")
parser.add_argument("--wrong_url", type=str, default="http://urbanlink.net.ph/urban/login", help="Wrong login redirect URL")
args = parser.parse_args()

# Login page URLs
login_url = args.login_url
wrong_login_url = args.wrong_url

# Predefined credentials
usernames = ["MHG8HFEBUVMH", "MHG8HFEB8YN5"]
passwords = ["17J8", "4W94"]

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors=yes")
chrome_options.add_argument("--disable-features=NetworkService,VizDisplayCompositor")
chrome_options.add_argument("--headless")  # Runs in headless mode (no UI)

# Start WebDriver using a context manager (ensures cleanup)
with webdriver.Chrome(options=chrome_options) as driver:
    wait = WebDriverWait(driver, 10)

    # Open login page
    driver.get(login_url)

    for username in usernames:
        for password in passwords:
            try:
                # If redirected to the wrong login page, go back
                if driver.current_url == wrong_login_url:
                    logging.warning("Redirected to wrong login page. Retrying...")
                    driver.get(login_url)

                # Locate username and password fields
                user_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
                pass_input = driver.find_element(By.NAME, "password")

                # Clear and enter credentials
                user_input.clear()
                pass_input.clear()
                user_input.send_keys(username)
                pass_input.send_keys(password)
                pass_input.send_keys(Keys.RETURN)

                # Wait for response (dynamic content)
                wait.until(lambda d: d.current_url != login_url)

                logging.info(f"Trying: {username} / {password} -> {driver.current_url}")

                # Check if login is successful
                if "dashboard" in driver.current_url or "success_page" in driver.current_url or "status" in driver.current_url:
                    logging.info(f"✅ Success! Username: {username}, Password: {password} - Redirected to status page")
                    exit(0)

                # Alternative: Check for login success message
                success_indicator = driver.find_elements(
                    By.XPATH, "//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'welcome')]"
                )
                if success_indicator:
                    logging.info(f"✅ Success! Username: {username}, Password: {password}")
                    exit(0)

                logging.info(f"❌ Failed: {username} / {password}")

            except TimeoutException:
                logging.error(f"⏳ Timeout waiting for elements. Retrying login for {username}/{password}...")
            except NoSuchElementException:
                logging.error(f"⚠️ Login form not found. Skipping {username}/{password}...")
            except Exception as e:
                logging.error(f"🚨 Unexpected error: {e}")

    logging.info("❌ No valid credentials found.")

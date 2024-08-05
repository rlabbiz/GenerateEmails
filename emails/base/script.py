from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

# Function to create an incognito browser instance
def create_incognito_browser():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

# Function to log into Outlook
def login_to_outlook(browser, email, password):
    try:
        browser.get("https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=157&ct=1722710547&rver=7.0.6738.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26deeplink%3dowa%252f%26RpsCsrfState%3db555fb94-4a7a-1813-b00d-996cbb7888a3&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c")
        
        # Enter email
        email_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="i0116"]'))
        )
        email_input.send_keys(email)
        browser.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
        
        # Enter password
        password_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "passwd"))
        )
        password_input.send_keys(password)
        browser.find_element(By.ID, "idSIButton9").click()
        
        # Optionally, handle "Stay signed in?" prompt
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="declineButton"]'))
        ).click()
        
        # Wait to ensure the login process completes
        time.sleep(5)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"An error occurred: {e}")

# Main function to execute the script
def main(email_password):
    try:
        email, password = email_password.split(':', 1)
    except ValueError:
        print("Error: Please provide email and password in the format email:password")
        sys.exit(1)

    browser = create_incognito_browser()
    try:
        login_to_outlook(browser, email, password)
        input("Press Enter to close the browser...")
    finally:
        browser.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py email:password")
        sys.exit(1)
    
    email_password = sys.argv[1]
    
    main(email_password)

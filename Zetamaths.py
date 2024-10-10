import time
from PIL import Image
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Base URL of the website
base_url = "https://ebooks.zetamaths.com/pwxlk/A0XyG9#p"

# Maximum page number to open
max_page_number = 339

# Timeout for waiting (in seconds)
timeout = 10  # Maximum time to wait for an element to load

# Password to enter
password = "Mrnsc"

# Setup the WebDriver for Firefox using the WebDriver Manager
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)

# Wait for elements to load using WebDriverWait
wait = WebDriverWait(driver, timeout)

# Open the first page
driver.get(f"{base_url}1")

# Wait for the password input field to be present
try:
    password_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="access_code"]')))
    password_field.send_keys(password)
    password_field.submit()  # Submit the form after entering the password

    # Wait for the page to load fully after entering the password by checking for a specific element that indicates the page has loaded
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "page-loaded-indicator")]')))
except Exception as e:
    print(f"An error occurred while entering the password on the first page: {e}")

# PDF setup in portrait mode
pdf = FPDF(orientation='P', unit='mm', format='A4')

# Loop through every page
for page_number in range(1, max_page_number + 1):
    if page_number != 1:
        # Construct the URL with the current page number
        url = f"{base_url}{page_number}"

        # Open the URL in the browser
        driver.get(url)

        # Adjust the window size to capture full content in portrait mode
        driver.set_window_size(800, 1050)

        # Refresh the page to ensure it fits the new window size
        driver.refresh()

        # Wait for the page to load fully by checking for a specific element
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "page-loaded-indicator")]')))
        except Exception as e:
            print(f"An error occurred while loading page {page_number}: {e}")

    # Take a screenshot and save it
    screenshot_path = f"screenshot_page_{page_number}.png"
    driver.save_screenshot(screenshot_path)

    # Open the screenshot image using PIL
    image = Image.open(screenshot_path)

    # Convert the screenshot to a format suitable for PDF
    image = image.convert('RGB')

    # Add the screenshot to the PDF in portrait mode
    pdf.add_page()
    pdf.image(screenshot_path, 0, 0, 210, 297)  # A4 portrait size

# Close the browser
driver.quit()

# Save the PDF
pdf.output("ebook_screenshots.pdf")

print("PDF created successfully.")

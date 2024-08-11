from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup the WebDriver for Firefox using the WebDriver Manager
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)

try:
    # Open the website
    driver.get('https://taxinformation.cbic.gov.in/')
    time.sleep(5)  # Adjust time as needed for the page to fully load

    # Wait for the "Customs" button element to be clickable and then click it
    customs_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/cbic-main/div[1]/div[1]/cbic-navbar/div/header/div/div[2]/div/nav/div/ul/cbic-mega-menu-item[2]/li/a'))
    )
    customs_button.click()
    time.sleep(2)  # Wait for the dropdown to appear

    # Wait for the "Rules" tab to be clickable using the full XPath and then click it
    rules_tab = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/cbic-main/div[1]/div[1]/cbic-navbar/div/header/div/div[2]/div/nav/div/ul/cbic-mega-menu-item[2]/li/ul/div/div/div/a[2]'))
    )
    rules_tab.click()
    time.sleep(5)  # Wait for the "Rules" page to load

    # Extract the correct tab names from the left-hand side under "Rules"
    tab_elements = driver.find_elements(By.XPATH, "//p[@class='title']")

    # Save the tab names to 'rules.txt'
    with open('rules.txt', 'w') as file:
        file.write('Rules Tabs:\n')
        for tab in tab_elements:
            tab_name = tab.text.strip()
            file.write(f'{tab_name}\n')
            print(tab_name)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()

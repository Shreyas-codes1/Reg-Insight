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

def extract_sections():
    """ Extract section names from the left-hand section under the active tab. """
    section_elements = driver.find_elements(By.CSS_SELECTOR, 'p.name')
    return [section.text for section in section_elements]

def extract_cbic_inner_components(section_id):
    """ Extract content from <cbic-inner-component> tags within the specified section. """
    # Wait for the section element to be visible
    section_element = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, section_id))
    )

    # Find all <cbic-inner-component> elements within the section
    inner_components = section_element.find_elements(By.TAG_NAME, 'cbic-inner-component')

    # Extract and return the content of each inner component
    inner_components_data = [component.get_attribute('innerHTML') for component in inner_components]
    return inner_components_data

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

    # Extract all tab names from the dropdown menu
    dropdown_tabs = driver.find_elements(By.XPATH, "//ul[contains(@class, 'dropdown-menu')]//a")

    # Save tab names to a text file
    with open('customs_tabs.txt', 'w') as file:
        file.write('Customs Dropdown Tabs:\n')
        print('Customs Dropdown Tabs:\n')

        for tab in dropdown_tabs:
            tab_name = tab.text
            file.write(f'{tab_name}\n')
            print(f'{tab_name}\n')

    # Click the "Acts" button using the full XPath
    acts_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/cbic-main/div[1]/div[1]/cbic-navbar/div/header/div/div[2]/div/nav/div/ul/cbic-mega-menu-item[2]/li/ul/div/div/div/a[1]'))
    )
    acts_button.click()
    time.sleep(5)  # Wait for the "Acts" page to load

    # Extract and save section names from the "Acts" page
    with open('acts_sections.txt', 'w') as file:
        # Write the "Acts" under Customs
        file.write('Customs > Acts\n')
        print('Customs > Acts\n')

        # Extract and write section names
        sections = extract_sections()
        for section in sections:
            file.write(f' {section}\n')
            print(f' {section}\n')

    # Extract data from <cbic-inner-component> tags under the specified section ID
    section_id = "accordionFlushExample"
    cbic_inner_components_data = extract_cbic_inner_components(section_id)

    # Save the data from the inner components to a text file
    with open('cbic_inner_components_data.txt', 'w') as file:
        file.write('Data from <cbic-inner-component> tags:\n')
        for idx, data in enumerate(cbic_inner_components_data):
            file.write(f'Component {idx + 1}:\n{data}\n\n')
            print(f'Component {idx + 1}:\n{data}\n')

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()

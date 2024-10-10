def forms():
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

        # Wait for the "Customs" button to be clickable and then click it
        customs_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/cbic-main/div[1]/div[1]/cbic-navbar/div/header/div/div[2]/div/nav/div/ul/cbic-mega-menu-item[2]/li/a'))
        )
        customs_button.click()
        time.sleep(2)  # Wait for the dropdown to appear

        # Wait for the "Forms" tab to be clickable and then click it
        forms_tab = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/cbic-main/div[1]/div[1]/cbic-navbar/div/header/div/div[2]/div/nav/div/ul/cbic-mega-menu-item[2]/li/ul/div/div/div/a[4]'))
        )
        forms_tab.click()
        time.sleep(5)  # Wait for the "Forms" page to load

        # Extract section tabs on the left
        section_tabs_xpath = '//*[@id="v-pills-c1-tab"]/p'
        section_tabs = driver.find_elements(By.XPATH, section_tabs_xpath)

        # Open the file to write the data
        with open('forms.txt', 'w') as file:
            file.write('Forms:\n')

            # Iterate through each section tab
            for tab in section_tabs:
                tab_name = tab.text.strip()
                file.write(f'Section: {tab_name}\n')

                # Click the tab to load its content
                driver.execute_script("arguments[0].scrollIntoView(true);", tab)
                time.sleep(1)  # Ensure the scrolling is complete
                driver.execute_script("arguments[0].click();", tab)
                time.sleep(3)  # Wait for the content to load

                # Define XPaths for form number and form name within the section
                form_number_xpath = '//*[@id="forms"]/div[2]/div[2]/cbic-forms-read/div[2]/div/table/tbody/tr/td[1]/div/a'
                form_name_xpath = '//*[@id="forms"]/div[2]/div[2]/cbic-forms-read/div[2]/div/table/tbody/tr/td[2]/div/a'

                # Extract form numbers and names
                form_numbers = driver.find_elements(By.XPATH, form_number_xpath)
                form_names = driver.find_elements(By.XPATH, form_name_xpath)

                for form_number, form_name in zip(form_numbers, form_names):
                    form_number_text = form_number.text.strip() if form_number else "No form number found"
                    form_name_text = form_name.text.strip() if form_name else "No form name found"
                    file.write(f'Form Number: {form_number_text}\n')
                    file.write(f'Form Name: {form_name_text}\n\n')

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

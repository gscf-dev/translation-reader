from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from langdetect import detect

url = "https://gis.qa.peridotplatform.com/login"
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(url)
driver.find_element(By.XPATH, '//input[@name="username"]').send_keys('GIS2_Approve')
driver.find_element(By.XPATH, '//input[@name="password"]').send_keys('Superman01')
driver.find_element(By.XPATH, '//button[@type="submit"]').click()

# Wait for the page to load properly
time.sleep(15)
desired_language = 'en'
urls = [
    "https://gis.qa.peridotplatform.com/CIS01/overview",
    "https://gis.qa.peridotplatform.com/CIS01/upload-transactional-data;uploadDate=2024-02-22",
    "https://gis.qa.peridotplatform.com/CIS01/utilization/portfolio",
    "https://gis.qa.peridotplatform.com/CIS01/file-actions;creationDate=2024-02-22"
]

for url in urls:
    print(f"Checking URL: {url}")
    driver.get(url)

    # Wait for the page to load properly
    time.sleep(15)

    try:
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//body//*[not(self::script or self::style)]'))
        )
    except Exception as e:
        print(f"Error waiting for text elements: {e}")
        continue

    all_text = []
    for element in elements:
        try:
            text = element.text.strip()
            if text:
                all_text.extend(text.split())
        except StaleElementReferenceException:
            continue  # Skip this element and move to the next

    non_matching_words = set()

    for word in all_text:
        if re.fullmatch(r'[A-Za-z]+', word):
            try:
                language = detect(word)
                if language != desired_language:
                   non_matching_words.add(word)
            except Exception as e:
                print(f"Error detecting language for word: '{word}': {e}")

    print(f"Words not in the defined language for {url}:")
    for word in non_matching_words:
        print(word)

    print("\n")

driver.quit()

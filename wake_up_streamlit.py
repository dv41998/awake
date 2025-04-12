from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from streamlit_app import STREAMLIT_APPS
import datetime

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

with open("wakeup_log.txt", "a") as log_file:
    log_file.write(f"Execution started at: {datetime.datetime.now()}\n")

    for url in STREAMLIT_APPS:
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            driver.get(url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            try:
                wake_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Yes, get this app back up!')]"))
                )
                driver.execute_script("arguments[0].click();", wake_button)
                log_file.write(f"{datetime.datetime.now()} ✅ Clicked wake button at: {url}\n")
            except TimeoutException:
                log_file.write(f"{datetime.datetime.now()} ⏱️ Wake button not found at: {url} (already up?)\n")

            driver.quit()
        except Exception as e:
            log_file.write(f"{datetime.datetime.now()} ❌ Error on {url}: {str(e)}\n")

print("🔥 wake_up_streamlit.py started running")

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from webdriver_manager.chrome import ChromeDriverManager
    from streamlit_app import STREAMLIT_APPS
    import datetime

    print("✅ All imports successful")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    for url in STREAMLIT_APPS:
        try:
            print(f"[{datetime.datetime.now()}] Trying: {url}")
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
                print(f"[{datetime.datetime.now()}] ✅ Clicked wake button at: {url}")
            except TimeoutException:
                print(f"[{datetime.datetime.now()}] ⏱️ Wake button not found at: {url}")

            driver.quit()
        except Exception as e:
            print(f"[{datetime.datetime.now()}] ❌ Error on {url}: {str(e)}")

except Exception as import_err:
    print(f"❌ Import or config failed: {import_err}")

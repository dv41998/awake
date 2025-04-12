print("🔥 wake_up_streamlit.py started running")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from webdriver_manager.chrome import ChromeDriverManager
    from streamlit_app import STREAMLIT_APPS
    import datetime
    import time

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
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
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
                time.sleep(8)
                driver.get(url)
                print(f"[{datetime.datetime.now()}] 🔁 Reloaded app after waking")
            except TimeoutException:
                print(f"[{datetime.datetime.now()}] ⏱️ Wake button not found at: {url} (already active?)")

            # 🔁 Ping again twice to keep app alive
            for i in range(2):
                time.sleep(450)  # wait 7.5 minutes
                driver.get(url)
                print(f"[{datetime.datetime.now()}] 🔁 Pinged app again to keep it awake ({i+1}/2)")

            driver.quit()
        except Exception as e:
            print(f"[{datetime.datetime.now()}] ❌ Error on {url}: {str(e)}")

except Exception as import_err:
    print(f"❌ Import or config failed: {import_err}")

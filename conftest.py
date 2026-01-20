import os
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def get_gecko_driver_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "drivers", "geckodriver.exe")

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Geckodriver introuvable : {path}")

    return path


# 🟢 NAVIGATEUR PROPRE POUR CHAQUE TEST
@pytest.fixture(scope="function")
def driver():
    options = Options()

    # 🔥 HEADLESS (CI / Jenkins)
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ Préférences Firefox
    options.set_preference("dom.security.https_only_mode", True)
    options.set_preference("dom.security.https_only_mode_pbm", True)
    options.set_preference("webdriver_accept_untrusted_certs", True)
    options.set_preference("webdriver_assume_untrusted_issuer", False)

    service = Service(executable_path=get_gecko_driver_path())

    driver = webdriver.Firefox(service=service, options=options)
    driver.set_window_size(1920, 1080)
    # 🔒 Nettoyage TOTAL
    driver.delete_all_cookies()


    yield driver

    driver.quit()


# 🟢 LOGIN REFAIT À CHAQUE TEST
@pytest.fixture(scope="function")
def login(driver):
    wait = WebDriverWait(driver, 60)

    driver.get("https://dev.nitacashhub.com/login")

    wait.until(EC.visibility_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys("ALINA466")

    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys("111111111")

    wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "submit-btn"))
    ).click()

    # ✅ PREUVE UNIQUE, RÉELLE, STABLE
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "nav-links"))
    )

    # 4️⃣ ASSERT FINAL
    current_url = driver.current_url
    assert "/coordinateur" in current_url, f"LOGIN ÉCHOUÉ : {current_url}"

    print("✅ LOGIN OK →", current_url)

    yield driver
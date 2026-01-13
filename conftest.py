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


@pytest.fixture(scope="class")
def driver():
    options = Options()

    # 🔥 HEADLESS (CI / Jenkins)
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ Préférences Firefox (BONNE MÉTHODE)
    options.set_preference("dom.security.https_only_mode", True)
    options.set_preference("dom.security.https_only_mode_pbm", True)
    options.set_preference("webdriver_accept_untrusted_certs", True)
    options.set_preference("webdriver_assume_untrusted_issuer", False)
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)
    options.set_preference("general.useragent.override",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"
                           )

    service = Service(executable_path=get_gecko_driver_path())

    driver = webdriver.Firefox(service=service, options=options)
    driver.set_window_size(1920, 1080)

    yield driver
    driver.quit()
@pytest.fixture(autouse=True)
def clear_browser_data(driver):
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    yield
@pytest.fixture(scope="class")
def login(driver):
    wait = WebDriverWait(driver, 30)

    driver.get("https://dev.nitacashhub.com/login")

    wait.until(EC.visibility_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys("ALINA466")
    driver.find_element(By.NAME, "password").send_keys("111111111")

    btn = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "submit-btn"))
    )
    btn.click()

    # ✅ ATTENTE D’UN ÉLÉMENT POST-LOGIN
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "nav-links"))
    )

    print("✅ Connexion réussie")
    print("URL actuelle :", driver.current_url)

    yield driver
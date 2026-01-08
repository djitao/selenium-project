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

    service = Service(executable_path=get_gecko_driver_path())

    driver = webdriver.Firefox(service=service, options=options)
    driver.set_window_size(1920, 1080)

    yield driver
    driver.quit()

@pytest.fixture(scope="class")
def login(driver):
    driver.get("https://dev.nitacashhub.com/login")

    try:
        driver.find_element(By.ID, "username").send_keys("ALINA466")
        driver.find_element(By.NAME, "password").send_keys("111111111")
        driver.find_element(By.CLASS_NAME, "submit-btn").click()

        # Attente que l’URL contienne “index”
        WebDriverWait(driver, 20).until(
            EC.url_contains("index")
        )

        current_url = driver.current_url
        print("✅ Connexion réussie, URL actuelle :", current_url)

        # Vérifie que la connexion a réussi
        if "error" in current_url:
            pytest.fail("❌ Échec de la connexion : URL contient 'error'")

        yield True

    except Exception as e:
        pytest.fail(f"❌ Problème pendant le login : {str(e)}")

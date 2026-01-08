import os
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_gecko_driver_path():
    """
    Retourne le chemin ABSOLU vers geckodriver.exe,
    compatible PyCharm, terminal, Jenkins, etc.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "drivers", "geckodriver.exe")

    print("🔍 Vérification du driver :", path)

    if not os.path.isfile(path):
        raise FileNotFoundError(f"❌ Geckodriver introuvable : {path}")

    return path


@pytest.fixture(scope="class")
def driver():
    options = Options()

    # 🔥 Mode headless obligatoire pour Jenkins
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    # 🟢 Profil Firefox
    profile = webdriver.FirefoxProfile()
    profile.set_preference("dom.security.https_only_mode", True)
    profile.set_preference("dom.security.https_only_mode_pbm", True)
    profile.set_preference("webdriver_accept_untrusted_certs", True)
    profile.set_preference("webdriver_assume_untrusted_issuer", False)

    options.profile = profile

    # 🔧 Service Geckodriver (ABSOLU)
    gecko_path = get_gecko_driver_path()
    service = Service(executable_path=gecko_path)

    # 🚀 Démarrage Firefox headless
    driver = webdriver.Firefox(service=service, options=options)
    driver.set_window_size(1920, 1080)

    yield driver
    driver.quit()


@pytest.fixture(scope="class")
def login(driver):
    wait = WebDriverWait(driver, 30)
    driver.get("https://dev.nitacashhub.com/login")

    try:
        # Attente formulaire
        wait.until(EC.presence_of_element_located((By.ID, "username")))

        # Saisie credentials
        driver.find_element(By.ID, "username").send_keys("ALINA466")
        driver.find_element(By.NAME, "password").send_keys("11111111")
        driver.find_element(By.CLASS_NAME, "submit-btn").click()

        # ✅ Attente URL finale exacte
        wait.until(
            EC.url_contains("/coordinateur/index")
        )

        # ✅ Sécurité supplémentaire : menu visible
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "nav-links"))
        )

        print("✅ Login réussi :", driver.current_url)
        yield True

    except Exception as e:
        print("❌ Login échoué")
        print("URL actuelle :", driver.current_url)

        driver.save_screenshot("reports/login_error.png")

        pytest.fail(f"❌ Problème pendant le login : {type(e).__name__}")